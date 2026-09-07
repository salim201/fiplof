# coding: utf-8
import sys
import os
import json
import urllib2
from PyQt4 import Qt, QtGui, QtCore
from PyQt4.QtGui import *
from EnvoiMiseAJour import Ui_EnvoiMiseAJour

from api_config import getApiBaseUrl
from db_utils import connection_is_broken, reconnect_connection

class EnvoiMiseAJourRun(QDialog):
    def __init__(self, connection):
        self.connection = connection
        QDialog.__init__(self)
        self.setModal(True)
        self.ui = Ui_EnvoiMiseAJour()
        self.ui.setupUi(self)

        self.progressBar = QtGui.QProgressBar(self.ui.groupBox)
        self.progressBar.setRange(0, 0)
        self.progressBar.setFixedHeight(20)
        self.progressBar.setTextVisible(True)
        self.progressBar.setFormat(u" Envoi en cours...")
        self.progressBar.hide()
        self.ui.verticalLayout_2.insertWidget(0, self.progressBar)

        self.initActions()
        self.chargerDonnees()

    def initActions(self):
        self.ui.checkBoxCocherTous.stateChanged.connect(self.onCocherTous)
        self.ui.pushButtonEnvoyer.clicked.connect(self.envoyerSelection)
        self.ui.comboBoxFiltreStatut.currentIndexChanged.connect(self.onFiltreChange)

    def onFiltreChange(self):
        print("DEBUG [onFiltreChange] index:", self.ui.comboBoxFiltreStatut.currentIndex())
        self.chargerDonnees()

    def getFiltreWhere(self):
        idx = self.ui.comboBoxFiltreStatut.currentIndex()
        if idx == 0:
            return ""
        elif idx == 1:
            return "AND (statut_retour IS NULL OR statut_retour = '' OR statut_retour = 'EMPTY')"
        elif idx == 2:
            return "AND statut_retour = 'RETURNED'"
        return ""

    def chargerDonnees(self):
        try:
            filtre = self.getFiltreWhere()
            query = """
                SELECT id, code_parcelle, numero, type_numero,
                       statut_retour, date_statut_retour
                FROM retour_externe
                WHERE 1=1 %s
                ORDER BY id DESC
            """ % filtre
            print("DEBUG [chargerDonnees] SQL:", query)
            self._ensureConnection()
            cur = self.connection.cursor()
            cur.execute(query)
            rows = cur.fetchall()
            cur.close()
            print("DEBUG [chargerDonnees] %d lignes trouvees" % len(rows))
            self.alimenterTableau(rows)
        except Exception as e:
            print("DEBUG [chargerDonnees] Erreur:", str(e))

    def alimenterTableau(self, rows):
        table = self.ui.tableWidget_retour
        table.setUpdatesEnabled(False)
        table.setRowCount(0)
        n = len(rows)
        table.setRowCount(n)

        header_font = QtGui.QFont()
        header_font.setBold(True)
        header_font.setPointSize(10)
        table.horizontalHeader().setFont(header_font)

        for i, row in enumerate(rows):
            checkbox = QtGui.QCheckBox()
            widget = QtGui.QWidget()
            layout = QtGui.QHBoxLayout(widget)
            layout.addWidget(checkbox)
            layout.setAlignment(QtCore.Qt.AlignCenter)
            layout.setContentsMargins(0, 0, 0, 0)
            table.setCellWidget(i, 0, widget)

            vals = [
                self._u(row[1]),
                self._u(row[2]),
                self._u(row[3]),
            ]
            for col, v in enumerate(vals, start=1):
                item = QtGui.QTableWidgetItem(v)
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                table.setItem(i, col, item)

            st = self._u(row[4])
            if st == "RETURNED":
                self._setBadgeCell(table, i, 4, u"Retourn\u00e9", "#4CAF50")
            elif st == "VIEWED":
                self._setBadgeCell(table, i, 4, u"Consult\u00e9", "#FF9800")
            else:
                table.setItem(i, 4, QtGui.QTableWidgetItem(""))

            table.setItem(i, 5, QtGui.QTableWidgetItem(self._u(row[5])))

            table.item(i, 1).setData(QtCore.Qt.UserRole, str(row[0]))

        largeurs = {0: 50, 1: 200, 2: 180, 3: 60, 4: 120, 5: 160}
        for col, w in largeurs.items():
            table.setColumnWidth(col, w)

        table.setUpdatesEnabled(True)
        table.repaint()

    def onCocherTous(self, state):
        table = self.ui.tableWidget_retour
        cocher = (state == QtCore.Qt.Checked)
        for row in range(table.rowCount()):
            w = table.cellWidget(row, 0)
            if w:
                cb = w.findChild(QtGui.QCheckBox)
                if cb:
                    cb.blockSignals(True)
                    cb.setChecked(cocher)
                    cb.blockSignals(False)

    def getIdsCoches(self):
        table = self.ui.tableWidget_retour
        ids = []
        for row in range(table.rowCount()):
            w = table.cellWidget(row, 0)
            if w and w.findChild(QtGui.QCheckBox) and w.findChild(QtGui.QCheckBox).isChecked():
                item = table.item(row, 1)
                if item:
                    id_val = item.data(QtCore.Qt.UserRole)
                    if id_val is not None:
                        try:
                            ids.append(int(str(id_val)))
                        except:
                            ids.append(int(id_val.toPyObject()))
        return ids

    def _push_ids(self, ids, url):
        payload = {"ids": ids}
        data = json.dumps(payload)
        print("DEBUG [envoyerSelection] URL:", url)
        print("DEBUG [envoyerSelection] Payload:", data)
        req = urllib2.Request(url, data, {"Content-Type": "application/json"})
        resp = urllib2.urlopen(req, timeout=30)
        body = resp.read()
        resp.close()
        print("DEBUG [envoyerSelection] Reponse API:", body)
        return json.loads(body)

    def _ensureConnection(self):
        if connection_is_broken(self.connection):
            self.connection = reconnect_connection()

    def _idsEnvoyes(self, ids, errors):
        ids_erreur = set()
        for err in errors or []:
            if isinstance(err, dict):
                v = err.get("id") or err.get("retour_id") or err.get("index")
            else:
                v = err
            if v is None:
                continue
            try:
                ids_erreur.add(int(v))
            except (TypeError, ValueError):
                pass
        return [i for i in ids if i not in ids_erreur]

    def envoyerSelection(self):
        print("DEBUG [envoyerSelection] DEBUT")
        try:
            ids = self.getIdsCoches()
            print("DEBUG [envoyerSelection] IDs:", ids)
            if not ids:
                QtGui.QMessageBox.warning(self, "Attention", u"Veuillez cocher au moins un retour.")
                return

            self.progressBar.show()
            self.ui.labelStatutEnvoi.setText(u"Envoi en cours...")
            QtGui.QApplication.processEvents()

            url = getApiBaseUrl() + "/api/ui/retours/push"

            try:
                result = self._push_ids(ids, url)
            except urllib2.HTTPError as e:
                err_body = e.read()
                retry = QtGui.QMessageBox.question(
                    self, u"Erreur serveur " + str(e.code),
                    u"Le serveur a retourn\u00e9 une erreur (HTTP " + str(e.code) + ").\n\n" +
                    u"D\u00e9tail: " + err_body + u"\n\n" +
                    u"Voulez-vous r\u00e9essayer ?",
                    QtGui.QMessageBox.Yes | QtGui.QMessageBox.No
                )
                if retry == QtGui.QMessageBox.Yes:
                    result = self._push_ids(ids, url)
                else:
                    raise

            self.progressBar.hide()
            QtGui.QApplication.processEvents()

            # 2. Mise à jour base locale
            print("DEBUG [envoyerSelection] Mise a jour base locale...")
            sent_ids = []
            if result:
                sent = result.get("sent", 0)
                errors = result.get("errors") or []
                if sent > 0:
                    sent_ids = self._idsEnvoyes(ids, errors)
            rowcount = 0
            if sent_ids:
                self._ensureConnection()
                cur = self.connection.cursor()
                cur.execute("""
                    UPDATE retour_externe
                    SET statut_retour = 'RETURNED',
                        date_statut_retour = NOW()
                    WHERE id = ANY(%s)
                """, (sent_ids,))
                rowcount = cur.rowcount
                cur.close()
                self.connection.commit()

            msg = u"Envoi r\u00e9ussi.\n%d retour(s) marqu\u00e9(s) comme envoy\u00e9(s)." % rowcount
            self.ui.labelStatutEnvoi.setText(u"Envoi termin\u00e9")
            QtGui.QMessageBox.information(self, u"R\u00e9sultat", msg)
            self.chargerDonnees()

        except urllib2.HTTPError as e:
            err_body = e.read()
            print("DEBUG [envoyerSelection] HTTPError code:", e.code)
            print("DEBUG [envoyerSelection] HTTPError body:", err_body)
            self.progressBar.hide()
            self.ui.labelStatutEnvoi.setText(u"Erreur HTTP")
            QtGui.QMessageBox.critical(self, u"Erreur " + str(e.code),
                u"Le serveur a retourn\u00e9 une erreur.\nAucune mise \u00e0 jour effectu\u00e9e.\n\nD\u00e9tail: " + err_body)

        except urllib2.URLError as e:
            print("DEBUG [envoyerSelection] URLError reason:", str(e.reason))
            self.progressBar.hide()
            self.ui.labelStatutEnvoi.setText(u"Erreur de connexion")
            QtGui.QMessageBox.critical(self, u"Erreur de connexion",
                u"Impossible de contacter le serveur.\nAucune mise \u00e0 jour effectu\u00e9e.\n\nD\u00e9tail: " + str(e.reason))

        except Exception as e:
            print("DEBUG [envoyerSelection] Exception:", str(e))
            import traceback
            traceback.print_exc()
            self.progressBar.hide()
            self.ui.labelStatutEnvoi.setText(u"Erreur")
            QtGui.QMessageBox.critical(self, u"Erreur",
                u"Aucune mise \u00e0 jour effectu\u00e9e.\n\nD\u00e9tail: " + str(e))

    def _badgeLabel(self, text, color):
        lbl = QLabel(text)
        lbl.setAlignment(QtCore.Qt.AlignCenter)
        lbl.setStyleSheet("background:%s;color:#fff;padding:2px 8px;border-radius:3px;font-weight:bold;font-size:11px;" % color)
        lbl.setSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        return lbl

    def _setBadgeCell(self, table, row, col, text, color):
        w = QtGui.QWidget()
        lay = QtGui.QHBoxLayout(w)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setAlignment(QtCore.Qt.AlignCenter)
        lay.addWidget(self._badgeLabel(text, color))
        table.setCellWidget(row, col, w)

    def _u(self, val):
        if val is None:
            return u''
        if isinstance(val, unicode):
            return val
        if isinstance(val, str):
            return val.decode('utf-8')
        return unicode(val)

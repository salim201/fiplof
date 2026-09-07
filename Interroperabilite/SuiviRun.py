# coding: utf-8
import sys
import os
import json
import urllib2
import psycopg2
import psycopg2.extras
from datetime import datetime
from PyQt4 import Qt, QtGui, QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import *

from api_config import getApiBaseUrl
from db_utils import connection_is_broken, reconnect_connection

class SuiviRun(QDialog):
    def __init__(self, connection):
        self.connection = connection
        QDialog.__init__(self)
        self.setWindowTitle(u"FiPLOF \u00b7 Suivi")
        self.setModal(True)
        self.resize(1100, 650)
        self._buildUI()
        self._chargerTout()

    def _buildUI(self):
        layout = QVBoxLayout(self)
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

        self.tabRecep = self._creerOnglet("receptions")
        self.tabRetours = self._creerOnglet("retours")
        self.tabProcessing = self._creerOnglet("processing")
        self.tabBatch = self._creerOnglet("batch")

        self.tabs.addTab(self.tabRecep, u"Dossiers re\u00e7us")
        self.tabs.addTab(self.tabProcessing, u"Processing ARQ")
        self.tabs.addTab(self.tabBatch, u"Gestion Batch")

        self.tabs.currentChanged.connect(self._onTabChange)

    def _creerOnglet(self, name):
        w = QWidget()
        lay = QVBoxLayout(w)
        top = QHBoxLayout()
        lblSync = QLabel(u"\u27f3 Donn\u00e9es BD locale")
        lblSync.setStyleSheet("font-size:11px; color:#888;")
        top.addWidget(lblSync)
        top.addStretch()
        lblMsg = QLabel("")
        lblMsg.setStyleSheet("font-weight:bold; color:#c00;")
        top.addWidget(lblMsg)
        lay.addLayout(top)
        table = QTableWidget()
        table.setSelectionBehavior(QAbstractItemView.SelectRows)
        table.setAlternatingRowColors(True)
        table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        table.verticalHeader().setVisible(False)
        lay.addWidget(table, 1)
        btnLay = QHBoxLayout()
        btnLay.addStretch()
        setattr(w, '_table', table)
        setattr(w, '_lblMsg', lblMsg)
        setattr(w, '_lblSync', lblSync)
        setattr(w, '_layoutBtn', btnLay)
        lay.addLayout(btnLay)
        return w

    def _onTabChange(self, idx):
        self._chargerOnglet(idx)

    def _chargerTout(self):
        for i in range(self.tabs.count()):
            self._chargerOnglet(i)

    def _chargerOnglet(self, idx):
        if idx == 0:
            self._chargerReceptions()
        elif idx == 1:
            self._chargerProcessing()
        elif idx == 2:
            self._chargerBatch()

    def _ensureConnection(self):
        if connection_is_broken(self.connection):
            self.connection = reconnect_connection()

    def _fetchRows(self, sql, params=None, retry=True):
        if not self.connection:
            return []
        try:
            self._ensureConnection()
            cur = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute(sql, params or ())
            rows = cur.fetchall()
            cur.close()
            return rows
        except psycopg2.OperationalError as e:
            msg = str(e).lower()
            broken = (self.connection.closed or
                      "connection already closed" in msg or
                      "closed the connection" in msg or
                      "connection reset" in msg or
                      "server closed" in msg)
            if broken and retry:
                try:
                    self.connection.rollback()
                except Exception:
                    pass
                return self._fetchRows(sql, params, retry=False)
            print("Suivi DB error:", str(e))
            raise
        except Exception as e:
            print("Suivi DB error:", str(e))
            raise

    # ---------- Onglet Receptions ----------
    def _chargerReceptions(self):
        tab = self.tabRecep
        try:
            rows = self._fetchRows("""
                SELECT id, source_transfer_id, source_system, internal_status,
                       callback_status, callback_error, created_at, updated_at
                FROM inbound_dossiers
                ORDER BY created_at DESC
                LIMIT 200
            """)
            self._remplirTableau(tab, [u"R\u00e9f. transfert", u"Syst\u00e8me source", u"R\u00e9ception", "Traitement", u"Rappel", u"Mise \u00e0 jour"],
                                 rows, self._rowRecep)
        except Exception as e:
            tab._lblMsg.setText(u"Erreur BD: " + str(e))

    def _rowRecep(self, r, table, row):
        table.setItem(row, 0, QTableWidgetItem(self._u(r.get("source_transfer_id"))))
        table.setItem(row, 1, QTableWidgetItem(self._u(r.get("source_system"))))
        self._setBadgeCell(table, row, 2, u"Re\u00e7u", "#2196F3")
        st = self._u(r.get("internal_status"))
        self._setBadgeCell(table, row, 3,
            {"queued":u"En file","done":u"Trait\u00e9","rejected":u"Rejet\u00e9"}.get(st, st),
            {"queued":"#FF9800","done":"#4CAF50","rejected":"#F44336"}.get(st, "#9E9E9E"))
        cb = self._u(r.get("callback_status"))
        cb_txt = {"pending":u"En attente","sent":u"Envoy\u00e9","failed":u"\u00c9chec"}.get(cb, cb)
        cb_cls = {"pending":"#9E9E9E","sent":"#4CAF50","failed":"#F44336"}.get(cb, "#9E9E9E")
        w = QWidget()
        h = QHBoxLayout(w)
        h.setContentsMargins(0,0,0,0)
        h.addWidget(self._badgeLabel(cb_txt, cb_cls))
        cb_err = r.get("callback_error")
        if cb == "failed" and cb_err:
            l = QLabel("(d\u00e9tail)")
            l.setStyleSheet("color:#999;font-size:10px;")
            l.setToolTip(self._u(cb_err))
            h.addWidget(l)
        h.addStretch()
        table.setCellWidget(row, 4, w)
        updated = r.get("updated_at")
        table.setItem(row, 5, QTableWidgetItem(str(updated or "")))
        if table.item(row, 5):
            table.item(row, 5).setForeground(QColor("#999"))

    # ---------- Onglet Retours ----------
    def _chargerRetours(self):
        tab = self.tabRetours
        try:
            rows = self._fetchRows("""
                SELECT id, code_parcelle, numero, type_numero, statut_retour
                FROM retour_externe
                ORDER BY id DESC
            """)
            self._viderBoutons(tab)
            btn = QPushButton(u"Push s\u00e9lection")
            btn.setStyleSheet("font-weight:bold;padding:6px 16px;")
            btn.clicked.connect(lambda: self._pushRetours(tab))
            tab._layoutBtn.insertWidget(0, btn)
            tab._pushBtn = btn
            self._remplirTableau(tab, ["", "Code parcelle", u"Num\u00e9ro", "Type", "Statut"], rows, self._rowRetour)
        except Exception as e:
            tab._lblMsg.setText(u"Erreur BD: " + str(e))

    def _rowRetour(self, r, table, row):
        cb = QCheckBox()
        w = QWidget()
        h = QHBoxLayout(w)
        h.setContentsMargins(0,0,0,0)
        h.addWidget(cb)
        h.setAlignment(Qt.AlignCenter)
        table.setCellWidget(row, 0, w)
        cb._retourId = r["id"]
        table.setItem(row, 1, QTableWidgetItem(self._u(r.get("code_parcelle"))))
        table.setItem(row, 2, QTableWidgetItem(self._u(r.get("numero"))))
        typ = self._u(r.get("type_numero"))
        table.setItem(row, 3, QTableWidgetItem(u"Fangatahana" if typ == "F" else u"Karatany" if typ == "K" else typ))
        st = self._u(r.get("statut_retour"))
        if st:
            self._setBadgeCell(table, row, 4,
                {"RETURNED":u"Retourn\u00e9","VIEWED":u"Consult\u00e9"}.get(st, st),
                {"RETURNED":"#4CAF50","VIEWED":"#FF9800"}.get(st, "#9E9E9E"))
        else:
            self._setBadgeCell(table, row, 4, u"En attente", "#9E9E9E")

    def _pushRetours(self, tab):
        ids = []
        table = tab._table
        for r in range(table.rowCount()):
            w = table.cellWidget(r, 0)
            if w:
                cb = w.findChild(QCheckBox)
                if cb and cb.isChecked() and hasattr(cb, '_retourId'):
                    ids.append(cb._retourId)
        if not ids:
            QMessageBox.warning(self, u"Attention", u"S\u00e9lectionnez au moins un retour.")
            return
        try:
            url = getApiBaseUrl() + "/api/ui/retours/push"
            data = json.dumps({"ids": ids})
            print("DEBUG Suivi push retours", ids)
            req = urllib2.Request(url, data, {"Content-Type":"application/json"})
            resp = urllib2.urlopen(req, timeout=30)
            result = json.loads(resp.read())
            resp.close()
            sent = result.get("sent", 0)
            errors = result.get("errors") or []
            if sent > 0:
                self._marquerEnvoyes(ids, errors)
            msg = u"Push termin\u00e9 : %d envoy\u00e9(s)" % sent
            if errors:
                msg += u", %d erreur(s)" % len(errors)
            QMessageBox.information(self, u"R\u00e9sultat", msg)
            self._chargerRetours()
        except Exception as e:
            QMessageBox.critical(self, u"Erreur", u"\u00c9chec du push: " + str(e))

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

    def _marquerEnvoyes(self, ids, errors):
        ids_envoyes = self._idsEnvoyes(ids, errors)
        if not ids_envoyes:
            return
        try:
            self._ensureConnection()
            cur = self.connection.cursor()
            cur.execute("""
                UPDATE retour_externe
                SET statut_retour = 'RETURNED',
                    date_statut_retour = NOW()
                WHERE id = ANY(%s)
            """, (ids_envoyes,))
            cur.close()
            self.connection.commit()
        except Exception as e:
            print("Suivi DB error (marquage envoi):", str(e))


    # ---------- Onglet Processing ----------
    def _chargerProcessing(self):
        tab = self.tabProcessing
        try:
            rows = self._fetchRows("""
                SELECT id, source_transfer_id, source_system, internal_status,
                       callback_status, callback_error, created_at, updated_at
                FROM inbound_dossiers
                ORDER BY created_at DESC
                LIMIT 200
            """)
            self._viderBoutons(tab)
            # Summary stats from the same data
            total = len(rows)
            queued = sum(1 for r in rows if r["internal_status"] == "queued")
            done = sum(1 for r in rows if r["internal_status"] == "done")
            rejected = sum(1 for r in rows if r["internal_status"] == "rejected")
            row_h = QHBoxLayout()
            for label, val, cls in [
                (u"En file", queued, "#FF9800"),
                (u"Trait\u00e9s", done, "#4CAF50"),
                (u"Rejet\u00e9s", rejected, "#F44336"),
                (u"Total", total, "#2196F3"),
            ]:
                c = QFrame()
                c.setStyleSheet("background:%s;border-radius:6px;padding:8px;margin:4px;" % cls)
                l = QVBoxLayout(c)
                l.addWidget(QLabel(str(val), alignment=Qt.AlignCenter))
                l.addWidget(QLabel(label, alignment=Qt.AlignCenter))
                row_h.addWidget(c)
            tab._layoutBtn.insertLayout(0, row_h)
            self._remplirTableau(tab, [u"R\u00e9f. transfert", u"Syst\u00e8me source", "Traitement", u"Rappel", u"Actions"], rows, self._rowProcessing)
        except Exception as e:
            tab._lblMsg.setText(u"Erreur BD: " + str(e))

    def _rowProcessing(self, r, table, row):
        table.setItem(row, 0, QTableWidgetItem(self._u(r.get("source_transfer_id"))))
        table.setItem(row, 1, QTableWidgetItem(self._u(r.get("source_system"))))
        st = self._u(r.get("internal_status"))
        self._setBadgeCell(table, row, 2,
            {"queued":u"En file","done":u"Trait\u00e9","rejected":u"Rejet\u00e9"}.get(st, st),
            {"queued":"#FF9800","done":"#4CAF50","rejected":"#F44336"}.get(st, "#9E9E9E"))
        cb = self._u(r.get("callback_status"))
        cb_txt = {"pending":u"En attente","sent":u"Envoy\u00e9","failed":u"\u00c9chec"}.get(cb, cb)
        cb_cls = {"pending":"#9E9E9E","sent":"#4CAF50","failed":"#F44336"}.get(cb, "#9E9E9E")
        self._setBadgeCell(table, row, 3, cb_txt, cb_cls)
        w = QWidget()
        h = QHBoxLayout(w)
        h.setContentsMargins(2,0,2,0)
        h.addStretch()
        inbound_id = r["id"]
        if cb == "failed":
            btn = QPushButton(u"\u21bb CB")
            btn.setFixedSize(50, 24)
            btn.clicked.connect(lambda checked, iid=inbound_id: self._retryCallback(iid))
            h.addWidget(btn)
        if st == "rejected":
            btn = QPushButton(u"\u21bb Re")
            btn.setFixedSize(50, 24)
            btn.clicked.connect(lambda checked, iid=inbound_id: self._reprocess(iid))
            h.addWidget(btn)
        h.addStretch()
        table.setCellWidget(row, 4, w)

    def _retryCallback(self, inbound_id):
        try:
            url = getApiBaseUrl() + "/api/ui/processing/" + str(inbound_id) + "/retry-callback"
            req = urllib2.Request(url, data="", headers={"Content-Type":"application/json"})
            resp = urllib2.urlopen(req, timeout=10)
            data = json.loads(resp.read())
            resp.close()
            QMessageBox.information(self, u"R\u00e9sultat",
                u"Callback relanc\u00e9" if data.get("sent") else u"Callback: " + str(data.get("callback_error","")))
            self._chargerProcessing()
        except Exception as e:
            QMessageBox.critical(self, u"Erreur", str(e))

    def _reprocess(self, inbound_id):
        try:
            url = getApiBaseUrl() + "/api/ui/processing/" + str(inbound_id) + "/reprocess"
            req = urllib2.Request(url, data="", headers={"Content-Type":"application/json"})
            resp = urllib2.urlopen(req, timeout=10)
            data = json.loads(resp.read())
            resp.close()
            QMessageBox.information(self, u"R\u00e9sultat",
                u"Reprocess termin\u00e9: " + str(data.get("internal_status","")))
            self._chargerProcessing()
        except Exception as e:
            QMessageBox.critical(self, u"Erreur", str(e))

    # ---------- Onglet Batch ----------
    def _chargerBatch(self):
        tab = self.tabBatch
        try:
            rows = self._fetchRows("""
                SELECT id, source_systeme, commune, statut, erreur,
                       valid_parcelle, error_parcelle,
                       traitement_statut, traitement_parcelle_valide, traitement_parcelle_refuse,
                       created_at
                FROM fiplof_raw_ingestion
                WHERE statut IN ('DONE', 'PARTIAL_SUCCESS')
                  AND (traitement_statut IS NULL OR traitement_statut != 'SUCCESS')
                ORDER BY created_at DESC
            """)
            self._remplirTableau(tab, [u"Syst\u00e8me source", "Commune", u"Validation", "Traitement", "Parcelles", u"Re\u00e7u le"],
                                 rows, self._rowBatch)
        except Exception as e:
            tab._lblMsg.setText(u"Erreur BD: " + str(e))

    def _rowBatch(self, r, table, row):
        table.setItem(row, 0, QTableWidgetItem(self._u(r.get("source_systeme"))))
        table.setItem(row, 1, QTableWidgetItem(self._u(r.get("commune"))))
        st = self._u(r.get("statut"))
        self._setBadgeCell(table, row, 2,
            {"RECEIVED":u"Re\u00e7u","PROCESSING":u"En cours","DONE":u"Valid\u00e9","PARTIAL_SUCCESS":u"Partiel","ERROR":u"Erreur"}.get(st, st),
            {"RECEIVED":"#2196F3","PROCESSING":"#FF9800","DONE":"#4CAF50","PARTIAL_SUCCESS":"#FF9800","ERROR":"#F44336"}.get(st, "#9E9E9E"))
        ts = self._u(r.get("traitement_statut"))
        if ts:
            self._setBadgeCell(table, row, 3,
                {"SUCCESS":u"Succ\u00e8s","PARTIAL_SUCCESS":u"Partiel"}.get(ts, ts),
                {"SUCCESS":"#4CAF50","PARTIAL_SUCCESS":"#FF9800"}.get(ts, "#9E9E9E"))
        else:
            self._setBadgeCell(table, row, 3, u"En attente", "#9E9E9E")
        pcell = QWidget()
        ph = QHBoxLayout(pcell)
        ph.setContentsMargins(2,0,2,0)
        nb_ok = 0
        nb_err = 0
        vp = r.get("valid_parcelle")
        if vp:
            try:
                nb_ok = len(json.loads(vp))
            except:
                pass
        ep = r.get("error_parcelle")
        if ep:
            try:
                nb_err = len(json.loads(ep))
            except:
                pass
        l1 = self._badgeLabel(str(nb_ok) + " OK", "#4CAF50")
        ph.addWidget(l1)
        if nb_err:
            l2 = self._badgeLabel(str(nb_err) + " Err", "#F44336")
            ph.addWidget(l2)
        ph.addStretch()
        table.setCellWidget(row, 4, pcell)
        table.setItem(row, 5, QTableWidgetItem(str(r.get("created_at","") or "")))
        if table.item(row, 5):
            table.item(row, 5).setForeground(QColor("#999"))

    # ---------- M\u00e9thodes utilitaires ----------
    def _remplirTableau(self, tab, headers, rows, rowFn):
        table = tab._table
        table.setUpdatesEnabled(False)
        table.clear()
        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)
        table.setRowCount(len(rows))
        hfont = QFont()
        hfont.setBold(True)
        hfont.setPointSize(10)
        table.horizontalHeader().setFont(hfont)
        table.horizontalHeader().setResizeMode(QHeaderView.Stretch)
        for i, r in enumerate(rows):
            rowFn(r, table, i)
            table.setRowHeight(i, 28)
        table.setUpdatesEnabled(True)
        tab._lblMsg.setText("")

    def _badgeLabel(self, text, color):
        lbl = QLabel(text)
        lbl.setAlignment(Qt.AlignCenter)
        lbl.setStyleSheet("background:%s;color:#fff;padding:2px 8px;border-radius:3px;font-weight:bold;font-size:11px;" % color)
        lbl.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        return lbl

    def _setBadgeCell(self, table, row, col, text, color):
        w = QWidget()
        lay = QHBoxLayout(w)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setAlignment(Qt.AlignCenter)
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

    def _viderBoutons(self, tab):
        while tab._layoutBtn.count():
            item = tab._layoutBtn.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                while item.layout().count():
                    c = item.layout().takeAt(0)
                    if c.widget():
                        c.widget().deleteLater()

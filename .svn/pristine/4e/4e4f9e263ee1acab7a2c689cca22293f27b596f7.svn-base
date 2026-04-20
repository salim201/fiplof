from PyQt4 import QtGui, Qt

from Utilisateur.EditGroupe import Ui_Dialog
from main import Ui_MainWindow
from models.Acces import Acces
from models.Groupe import Groupe
from models.GroupeAcces import GroupeAcces


class EditGroupeRun(QtGui.QDialog):
    access = None  # type: list[GroupeAcces]

    def __init__(self, parent, connection, gid=0):
        # type: (Ui_MainWindow, object, int) -> object
        QtGui.QDialog.__init__(self)
        self.parent, self.connection, self.gid = parent, connection, gid
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.init_actions()
        self.prefill()
        model = GroupeAcces(self.connection)
        self.access = model.find_by_gid(self.gid)
        self.fill_tree()
        self.ui.treeWidget_2.expandAll()
        for i in range(0, self.ui.treeWidget_2.columnCount()):
            self.ui.treeWidget_2.resizeColumnToContents(i)
        self.ui.tabWidget.setTabEnabled(1, int(self.gid) != 1)

    def init_actions(self):
        self.ui.pushButtonAnnuler.clicked.connect(self.reject)
        self.ui.pushButtonEnregistrer.clicked.connect(self.save)

    def prefill(self):
        m = Groupe(self.connection)
        g = m.find_by_id(self.gid)
        if g is None:
            return
        self.ui.lineEditNom.setText(g.nom)
        self.ui.plainTextEditDescription.setPlainText(g.description)

    def save(self):
        if self.ui.lineEditNom.text().isEmpty():
            return
        g = Groupe(self.connection)
        g.id = self.gid
        g.nom = str(self.ui.lineEditNom.text())
        g.description = " " if self.ui.plainTextEditDescription.toPlainText().isEmpty() \
            else str(self.ui.plainTextEditDescription.toPlainText())
        gid = g.save()
        if gid:
            self.save_acces(gid)
        self.accept()
        
    def save_acces(self, gid):
        # type: (int) -> None
        print("saving access")
        if gid == "1":
            return
        root = self.ui.treeWidget_2.topLevelItem(0)  # type: QtGui.QTreeWidgetItem
        for i in range(0, root.childCount()):
            for j in range(0, root.child(i).childCount()):
                child = root.child(i).child(j)
                acces_id = child.data(0, Qt.Qt.UserRole).toInt()[0]  # type: int
                if acces_id:
                    m = GroupeAcces(self.connection)
                    m.acces_id = acces_id
                    m.groupe_id = gid
                    m.find_existant()
                    m.autorise = child.checkState(1) == Qt.Qt.Checked
                    m.save()

    def category_item(self, category_name):
        top = self.ui.treeWidget_2.topLevelItem(0)  # type: QtGui.QTreeWidgetItem
        for i in range(0, top.childCount()):
            if top.child(i).text(0) == category_name:
                return top.child(i)
        return None

    def fill_tree(self):
        model = Acces(self.connection)
        results = model.find_all()
        top = self.ui.treeWidget_2.topLevelItem(0)  # type: QtGui.QTreeWidgetItem
        if top is None:
            return
        for r in results:  # type: Acces
            item = self.category_item(r.category_name())
            if item is None:
                item = QtGui.QTreeWidgetItem(0)
                item.setText(0, r.category_name())
                item.setData(0, Qt.Qt.UserRole, 0)
                top.addChild(item)
            f = filter(lambda a: a.acces_id == r.id, self.access)
            autorise = False
            if len(f):
                autorise = f[0].autorise
            child = QtGui.QTreeWidgetItem(0)
            child.setText(0, r.libelle)
            child.setData(0, Qt.Qt.UserRole, r.id)
            child.setCheckState(1, Qt.Qt.Checked if autorise else Qt.Qt.Unchecked)
            item.addChild(child)

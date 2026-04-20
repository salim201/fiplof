# -*- coding: utf-8 -*-
class FiPlofFile:
    def __init__(self):
        self.file = None
        self.lines=None

    @staticmethod
    def readFile(self,path):
        try:
            self.file = open(path, "r")
            self.lines = self.file.readlines()
            self.file.close()
            return self.lines
        except Exception as e:
            print 'erreur dans FiPlofFile-readFile'
            print(e.message)

    @staticmethod
    def list_in_file(self,path,max_row,index_data):
        try:
            param=[]
            content=FiPlofFile.readFile(self, path)
            print ("*********len content*****")
            print (len(content))
            for i in range(len(content)):
                if i != 0 and i < max_row:
                    data = content[i].split()
                    param.append(data[index_data])
            return param
        except Exception as e:
            print 'erreur dans FiPlofFile-list_in_file'
            print(e.message)

    @staticmethod
    def list_in_file_(self, path):
        try:
            param = []
            content = FiPlofFile.readFile(self, path)
            for i in range(1, len(content)):  # On traite toutes les lignes sauf la première
                data = content[i].split()  # Sépare la ligne en mots (par défaut, séparé par les espaces)
                param.append(data)  # Ajouter la ligne complète sous forme de liste de mots à param

            return param

        except Exception as e:
            print("Erreur dans FiPlofFile.list_in_file_")
            print(str(e))
            return []
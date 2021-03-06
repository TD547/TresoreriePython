import csv

from modele.BilanFinancier import BilanFinancier
from modele.Operation import Operation


class StockageBilanFinancier:

    def __init__(self):
        self.fichier_bilan = "data/Bilan_financier_2020/budget_2019.csv"
        self.bilan = []

    def initialiser_fichier(self):
        with open(self.fichier_bilan, 'w', newline='') as csvfile:
            fieldnames = ['type', 'categorie', 'date', 'montant', 'description']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

    def lire_fichier(self):
        with open(self.fichier_bilan, newline='') as csvfile:
            csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            boolean = False
            for row in csvreader:
                if not boolean:
                    boolean = True
                else:
                    if len(row) == 5:
                        operation = Operation()
                        operation.set_type(row[0])
                        operation.set_categorie(row[1])
                        operation.set_date(row[2])
                        operation.set_montant(row[3])
                        operation.set_description(row[4])
                        self.bilan.append(operation)
            return self.bilan

    def lire_fichier_recettes(self):
        bilan2 = []
        with open(self.fichier_bilan, newline='') as csvfile:
            csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            cpt = 0
            for row in csvreader:
                if cpt != 0:
                    if len(row) == 5 and row[0] == 'recette' and row[3] != "":
                        row2 = [row[1], row[2], row[3], row[4]]
                        bilan2.append(row2)
                cpt = cpt + 1
        return bilan2

    def lire_fichier_depenses(self):
        bilan2 = []
        with open(self.fichier_bilan, newline='') as csvfile:
            csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            cpt = 0
            for row in csvreader:
                if cpt != 0:
                    if len(row) == 5 and row[0] == 'depense' and row[2] != "":
                        row2 = [row[1], row[2], row[3], row[4]]
                        bilan2.append(row2)
                cpt = cpt + 1
        return bilan2

    def lire_fichier_complets(self):
        bilan2 = []
        with open(self.fichier_bilan, newline='') as csvfile:
            csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            cpt = 0
            for row in csvreader:
                if cpt != 0:
                    if row[2] != '':
                        bilan2.append(row)
                cpt = cpt + 1
        return bilan2

    def lire_fichier_complets_avec_categorie_vide(self):
        bilan2 = []
        with open(self.fichier_bilan, newline='') as csvfile:
            csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            cpt = 0
            for row in csvreader:
                if cpt != 0:
                    bilan2.append(row)
                cpt = cpt + 1
        return bilan2

    def lire_fichier_categories(self):
        bilan2 = []
        type = []
        categories = []
        montant_total = []
        with open(self.fichier_bilan, newline='') as csvfile:
            csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            cpt = 0
            for row in csvreader:
                if cpt != 0:
                    if not categories.__contains__(row[1]):
                        type.append(row[0])
                        categories.append(row[1])
                        montant_total.append(0.0)
                    if row[3] != '':
                        indice = categories.index(row[1])
                        montant_total[indice] = montant_total[indice] + float(row[3])
                cpt = cpt + 1
        i = 0
        for categorie in categories:
            ligne = [type[i], categorie, str(montant_total[i])]
            bilan2.append(ligne)
            i = i + 1
        return bilan2

    def lire_fichier_categorie(self,type):
        categories = []
        with open(self.fichier_bilan, newline='') as csvfile:
            csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            cpt = 0
            for row in csvreader:
                if cpt != 0:
                    if not categories.__contains__(row[1]) and type == row[0]:
                        categories.append(row[1])
                cpt = cpt + 1
        return categories

    def ajouter_operation(self, operation):

        type = operation.get_type()
        categorie = operation.get_categorie()
        date = operation.get_date()
        montant = operation.get_montant()
        description = operation.get_description()

        with open(self.fichier_bilan, 'a', newline='') as csvfile:
            fieldnames = ['type','categorie','date', 'montant', 'description']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow({'type' : type,'categorie' : categorie,'date': date, 'montant' : montant, 'description' : description})

    def contient_operation(self, operation):

        contient = False
        type = operation.get_type()
        categorie = operation.get_categorie()
        date = operation.get_date()
        montant = operation.get_montant()
        description = operation.get_description()

        with open(self.fichier_bilan, newline='') as csvfile:
            csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in csvreader:
                if len(row) == 5:
                    if row[0] == type and row[1] == categorie and row[2] == date and row[3] == montant and row[4] == description:
                        contient = True
                        return contient
        return contient

    def contient_categorie(self, categorie):
        contient = False

        with open(self.fichier_bilan, newline='') as csvfile:
            csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in csvreader:
                if len(row) == 5:
                    if row[1] == categorie:
                        contient = True
                        return contient
        return contient


    def supprimer_operation(self, operation):

        bilan2 = self.lire_fichier_complets()
        type = operation.get_type()
        categorie = operation.get_categorie()
        date = operation.get_date()
        montant = operation.get_montant()
        description = operation.get_description()

        ligne = [type, categorie, date, montant, description]
        ligne2 = [type, categorie,'','','']
        bilan2.remove(ligne)
        if not bilan2.__contains__(ligne2):
            bilan2.append(ligne2)
        self.initialiser_fichier()
        for nv_ligne in bilan2:
            if len(nv_ligne) == 5:
                operation1 = Operation()
                operation1.set_type(nv_ligne[0])
                operation1.set_categorie(nv_ligne[1])
                operation1.set_date(nv_ligne[2])
                operation1.set_montant(nv_ligne[3])
                operation1.set_description(nv_ligne[4])
                self.ajouter_operation(operation1)

    def supprimer_categorie(self, categorie):

        bilan2 = self.lire_fichier_complets_avec_categorie_vide()
        self.initialiser_fichier()
        for nv_ligne in bilan2:
            if len(nv_ligne) == 5:
                operation1 = Operation()
                operation1.set_type(nv_ligne[0])
                operation1.set_categorie(nv_ligne[1])
                operation1.set_date(nv_ligne[2])
                operation1.set_montant(nv_ligne[3])
                operation1.set_description(nv_ligne[4])
                if nv_ligne[1] != categorie[1]:
                    self.ajouter_operation(operation1)
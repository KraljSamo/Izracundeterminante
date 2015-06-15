from tkinter import *

# Stanje = 0 pomoc zaprta
# Stanje = 1 pomoc odprta
# Stanje1 = 0 matrika ni izpisana
# Stanje1 = 1 matrika je izpisana

class Determinanta():
    def __init__(self, master):

        self.stanje = 0
        self.stanje1 = 0
        
        self.datoteka = StringVar(master, value = None)
        self.det = DoubleVar(master, value = None)
        self.sled = DoubleVar(master, value = None)
        self.opozorilo = StringVar(master, value = None)
        self.pomagaj = StringVar(master, value = None)
        self.mat = StringVar(master, value = None)
        
        polje_1 = Entry(master, textvariable = self.datoteka, bg = "lightyellow" )
        polje_1.grid(row=0,column=2)

        tekst_3 = Label(text = "Kodiranje naj bo UTF-8 brez BOMa")
        tekst_3.grid(row = 1, column = 0)

        tekst_4 = Label(text = "Sled matrike:")
        tekst_4.grid(row = 3, column = 0)
        tekst_5 = Label(textvariable = self.sled)
        tekst_5.grid(row = 3, column = 1)
        
        tekst = Label(text = "Vnesi ime datoteke: ", width = 40)
        tekst.grid(row = 0, column = 0)
        tekst_1 = Label(text = "Determinanta matrike: ")
        tekst_1.grid(row = 2, column = 0)
        tekst_2 = Label(textvariable = self.det, width = 10)
        tekst_2.grid(row = 2, column = 1)
        tekst_6 = Label(textvariable = self.opozorilo, fg = "red")
        tekst_6.grid(row = 2, column = 2)

        tekst_7 = Label(textvariable = self.pomagaj, fg = "green")
        tekst_7.grid(row = 5, columnspan = 3)

        tekst_8 = Label(textvariable = self.mat, fg = "green")
        tekst_8.grid(row = 6, columnspan = 3) 

        gumb = Button(master, text = "Izračunaj", command = self.izracunaj)
        gumb.grid(row = 4, column = 2)

        gumb = Button(master, text = "Pomoč", command = self.pomoc)
        gumb.grid(row = 4, column = 0)

        gumb = Button(master, text = "Izpis matrike", command = self.izpisi)
        gumb.grid(row = 4, column = 1)

    def pomoc(self):
        if self.stanje == 0:
            self.pomagaj.set("""
        V polje zgoraj desno vnesi ime datoteke oziroma vključi pot v primeru, da datoteka
        ni v isti mapi.\n
        Datoteka naj bo kodirana v UTF -8 brez BOM-a. Izgled naj bo približno takšen: \n
        x1, x2, x3
        x4, x5, x6
        x7, x8, x9
        Racionalna števila naj bodo zapisana v obliki p/q.
        Seveda je matrika lahko poljubne kvadratne velikosti. Vendar ne pretiravaj:)

        """)
            self.stanje = 1
        elif self.stanje == 1:
            self.pomagaj.set("")
            self.stanje = 0

    def izpisi(self):
        if self.stanje1 == 0:
            matrika = []
            pot = self.datoteka.get()
            try:
                with open(pot, encoding ="UTF-8") as f:
                    for line in f:
                        line = line.strip("\n")
                        vrstica = line.split(",")
                        matrika.append(vrstica)
                izpis = "Vnešena matrika je takšna: \n \n"
                najdaljsi = 0
                for vrstica in matrika:
                    for element in vrstica:
                        if len(element) > najdaljsi:
                            najdaljsi = len(element)
                for vrstica in matrika:
                    for element in vrstica:
                        izpis += element + (najdaljsi -len(element)+1)*"  "
                    izpis += "\n"
                self.mat.set(izpis)
                self.stanje1 = 1
            except:
                self.mat.set("Najverjetneje datoteka ne obstaja, za boljša navodila, klikni pomoč")
        elif self.stanje1 == 1:
            self.mat.set("")
            self.stanje1 = 0
            
    def izracunaj(self):
        matrika = []
        pot = self.datoteka.get()
        try:
            with open(pot, encoding ="UTF-8") as f:
                for line in f:
                    line = line.strip("\n")
                    vrstica = line.split(",")
                    for a in range(len(vrstica)):
                        try:
                            vrstica[a] = int(vrstica[a])
                        except:
                            število = vrstica[a].split("/")
                            vrstica[a] = int(število[0])/int(število[1])
                    matrika.append(vrstica)

            def poddet(matrika,n): #naredi poddeterminatno(0,i) determinante matrike
                podmatrika = []
                i = 1
                while i < len(matrika):
                    vrstica = []
                    for j in range(len(matrika[i])):
                        if j == n:
                            pass
                        else:
                            vrstica.append(matrika[i][j])
                    podmatrika.append(vrstica)
                    i = i + 1
                return podmatrika

            def determinanta(matrika):
                if len(matrika) == 0:
                    return 0
                if len(matrika) == 1:
                    return matrika[0][0]
                if len(matrika) == 2:
                    return matrika[0][0] * matrika[1][1] - matrika[0][1]*matrika[1][0]
                else: #uporabi formulo za poddeterminante
                    vsota = 0
                    for i in range(len(matrika[0])):
                        dodaj = matrika[0][i]*determinanta(poddet(matrika,i))*pow(-1,i)
                        vsota += dodaj
                    return vsota

            def sled(matrika):
                return sum(matrika[i][i] for i in range(len(matrika)))

            def kvadratna(matrika):
                n = len(matrika)
                for vrstica in matrika:
                    if len(vrstica) == n:
                        pass
                    else:
                        return False
                return True
            
            nezaokrozeno = determinanta(matrika)
            if kvadratna(matrika) == False:
                self.opozorilo.set("Matrika ni kvadratna!")
                self.det.set(0.00)
                self.sled.set(0.00)
                self.mat.set("")
                self.stanje1 = 0
                self.izpisi()
            else:
                self.opozorilo.set("")
                zaokrozeno = "{0:.2f}".format(nezaokrozeno)
                self.det.set(zaokrozeno)

                sled1 = sled(matrika)
                sled2 = "{0:.2f}".format(sled1)
                self.sled.set(sled2)
                self.mat.set("")
                self.stanje1 = 0
                self.izpisi()
        except:
            self.opozorilo.set("Datoteka ne obstaja!")
            self.det.set(0.00)
            self.sled.set(0.00)
            self.mat.set("")
            self.stanje1 = 0
            self.izpisi()
root = Tk()
program = Determinanta(root)
root.mainloop()

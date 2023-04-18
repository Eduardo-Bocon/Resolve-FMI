import tkinter as tk

# definições de cores
darkGrey = '#363636'
lightGrey = '#DCDCDC'
midGrey = '#A9A9A9'

# Definições da Janela
root = tk.Tk()
root.title("Resolve FMI")
root.geometry("600x500")
root.minsize(600, 500)
root.configure(bg=darkGrey)

#icone
icon = "cat.ico"
root.iconbitmap(default=icon)

# Definições da entrada do usuario
userInput = tk.StringVar()
userInput.set("")

lastColumn = tk.IntVar()

# Funções para entrada do usuario
def addP():
    if checkCharLimit() and checkLastCharPQ():
        userInput.set(userInput.get() + "P")

def addQ():
    if checkCharLimit() and checkLastCharPQ():
        userInput.set(userInput.get() + "Q")

def addNeg():
    if checkCharLimit():
        userInput.set(userInput.get() + "¬")

def addOpP():
    if checkCharLimit():
        userInput.set(userInput.get() + "(")

def addClP():
    if checkCharLimit():
        userInput.set(userInput.get() + ")")

def addOr():
    if checkCharLimit() and checkLastCharAndOr():
        userInput.set(userInput.get() + "∨")

def addAnd():
    if checkCharLimit() and checkLastCharAndOr():
        userInput.set(userInput.get() + "∧")

def delet():
    userInput.set(userInput.get()[:-1])

def checkCharLimit():
    inputMaximo = 15
    if len(userInput.get()) > inputMaximo:
        return False
    return True

def checkLastCharPQ():
    if len(userInput.get()) > 0:
        if userInput.get()[-1] == "P" or userInput.get()[-1] == "Q":
            return False
    return True

def checkLastCharAndOr():
    if len(userInput.get()) > 0:
        if userInput.get()[-1] == "∨" or userInput.get()[-1] == "∧":
            return False
    return True

# funcoes para a tabela da verdade
def printTruthTable(truthTable, numOfVar):
    spaceBetwColumns = 30
    spaceBetwLines = 50
    for i in range(1,(2**numOfVar)+1):
        for k in range(len(userInput.get())):
            char = tk.Label(root, text=truthTable[i][k], font="Verdana, 20", bg=darkGrey, fg=lightGrey)
            char.place(x=8+spaceBetwColumns*k, y=200+spaceBetwLines*i)
    i = i + 1
    lastColumnLabel = tk.Label(root, text="Ultima coluna: " + str(lastColumn.get()+1), font="Verdana, 20", bg=darkGrey, fg=lightGrey)
    lastColumnLabel.place(x=8+spaceBetwColumns, y=200+spaceBetwLines*i)

def putTruthVariables(truthTable, auxTable, numOfVar):
    for i in range(1,(2**numOfVar)+1):
        binary = bin(i-1)[2:]
        binary = str(binary)

        # botar zeros antes caso precise
        while len(binary) < numOfVar:
            binary = '0' + binary

        for k in range(len(userInput.get())):
            if truthTable[0][k] == "P":
                if binary[0] == '0':
                    truthTable[i][k] = "T"
                    auxTable[i][k] = "T"
                else:
                    truthTable[i][k] = "F"
                    auxTable[i][k] = "F"
            elif truthTable[0][k] == "Q":
                if binary[1] == '0':
                    truthTable[i][k] = "T"
                    auxTable[i][k] = "T"
                else:
                    truthTable[i][k] = "F"
                    auxTable[i][k] = "F"
            else:
                truthTable[i][k] = "-"

def putTruthAndOr(truthTable, auxTable, numOfVar):
    for i in range(len(userInput.get())):
        if truthTable[0][i] == '∨':
            for k in range(1, (2**numOfVar)+1):
                if auxTable[k][i-1] == "T" or auxTable[k][i+1] == "T":
                    truthTable[k][i] = "T"
                    auxTable[k][i] = "T"
                    auxTable[k][i+1] = "T"
                    auxTable[k][i-1] = "T"
                else:
                    truthTable[k][i] = "F"
                    auxTable[k][i] = "F"
                    auxTable[k][i+1] = "F"
                    auxTable[k][i-1] = "F"
            lastColumn.set(i)
            print(i)
        if truthTable[0][i] == '∧':
            for k in range(1, (2**numOfVar)+1):
                if auxTable[k][i-1] == "T" and auxTable[k][i+1] == "T":
                    truthTable[k][i] = "T"
                    auxTable[k][i] = "T"
                    auxTable[k][i + 1] = "T"
                    auxTable[k][i - 1] = "T"
                else:
                    truthTable[k][i] = "F"
                    auxTable[k][i] = "F"
                    auxTable[k][i + 1] = "F"
                    auxTable[k][i - 1] = "F"
            lastColumn.set(i)

def putNeg(truthTable, auxTable, numOfVar):
    for i in range(len(userInput.get())):
        if truthTable[0][i] == "¬":
            for k in range(1, (2**numOfVar)+1):
                if auxTable[k][i+1] == "T":
                    truthTable[k][i] = "F"
                    auxTable[k][i] = "F"
                    auxTable[k][i + 1] = "F"
                elif auxTable[k][i+1] == "F":
                    truthTable[k][i] = "T"
                    auxTable[k][i] = "T"
                    auxTable[k][i + 1] = "T"
            lastColumn = i

# Função principal da tabela da verdade
def truthTable():

    # limpa a parte de baixo da tela
    clearTable = tk.Label(root, text=" "*30, font=("Arial, 200"), bg=darkGrey)
    clearTable.place(x=0, y=200)

    # cria uma matriz para a tabela
    numOfVar = 2
    truthTable = []
    for i in range((2**numOfVar)+1):
        row = []
        for j in range(len(userInput.get())):
            row.append(0)
        truthTable.append(row)
    truthTable[0] = userInput.get()

    auxTable = []
    for i in range((2 ** numOfVar) + 1):
        row = []
        for j in range(len(userInput.get())):
            row.append(0)
        auxTable.append(row)
    auxTable[0] = userInput.get()

    # coloca a formula da parte de cima da tabela da verdade
    for i in range(len(userInput.get())):
        upperTable = tk.Label(root, text=truthTable[0][i], font=("Arial, 20"), bg=darkGrey, fg=lightGrey)
        spaceBetwChar = 30
        upperTable.place(x=5+spaceBetwChar*i, y=200)

    # Coloca os verdadeiros e falsos nas variaveis
    putTruthVariables(truthTable, auxTable, numOfVar)

    # faz as negações
    putNeg(truthTable, auxTable, numOfVar)

    # Faz And e Or
    putTruthAndOr(truthTable, auxTable, numOfVar)



    # Mostra a tabela
    printTruthTable(truthTable, numOfVar)

# Textos e Botões iniciais

formula = tk.Label(root, textvariable = userInput, font=("Verdana, 20"), bg=darkGrey, fg='#DCDCDC')

buttonSize = 20

buttonP = tk.Button(root, text="P", padx=buttonSize, pady=buttonSize, bg = midGrey, command=addP)
buttonQ = tk.Button(root, text="Q", padx=buttonSize, pady=buttonSize,bg = midGrey, command=addQ)
buttonNeg = tk.Button(root, text="¬", padx=buttonSize, pady=buttonSize,bg = midGrey, command=addNeg)
buttonOpParentesis = tk.Button(root, text="(", padx=buttonSize, pady=buttonSize,bg = midGrey, command=addOpP)
buttonCloParentesis = tk.Button(root, text=")", padx=buttonSize, pady=buttonSize,bg = midGrey, command=addClP)
buttonOr = tk.Button(root, text="∨", padx=buttonSize, pady=buttonSize,bg = midGrey, command=addOr)
buttonAnd = tk.Button(root, text="∧", padx=buttonSize, pady=buttonSize,bg = midGrey, command=addAnd)
buttonDel = tk.Button(root, text="Del", padx=buttonSize, pady=buttonSize,bg = midGrey, command=delet)
buttonTruthTable = tk.Button(root, text="Ver a tabela da verdade", padx=buttonSize, pady=buttonSize,bg = midGrey, command=truthTable)

# Organização na tela

row1 = 0
row2 = 50
row3 = 130

columnSpace = 60

formula.place(x=5, y=row1)
buttonP.place(x=2, y=row2)
buttonQ.place(x=columnSpace, y=row2)
buttonNeg.place(x=columnSpace*2, y=row2)
buttonOpParentesis.place(x=columnSpace*3, y=row2)
buttonCloParentesis.place(x=columnSpace*4, y=row2)
buttonOr.place(x=columnSpace*5, y=row2)
buttonAnd.place(x=columnSpace*6, y=row2)
buttonDel.place(x=columnSpace*7, y=row2)
buttonTruthTable.place(x=140, y=row3)

# loop principal
root.mainloop()
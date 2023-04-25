import tkinter as tk

# definições de cores
darkGrey = '#363636'
lightGrey = '#DCDCDC'
midGrey = '#A9A9A9'
blue = '#1E90FF'

# Definições da Janela
windWidth = 700
windHeight = 700
root = tk.Tk()
root.title("Resolve FMI")
root.geometry("700x700")
root.minsize(windWidth, windHeight)
root.configure(bg=darkGrey)

#icone
icon = "cat.ico"
root.iconbitmap(default=icon)

# Definições da entrada do usuario
userInput = tk.StringVar()
userInput.set("")
# teste: P∨Q∨R∧¬(P∧Q)∧¬(P∧R)∧¬(Q∧R)

lastColumn = tk.IntVar() # salva qual foi a ultima coluna calculada

numOfVar = tk.IntVar() # salva o numero de variaveis

# Funções para entrada do usuario
def addP():
    if checkCharLimit() and checkLastCharVar():
        userInput.set(userInput.get() + "P")

def addQ():
    if checkCharLimit() and checkLastCharVar():
        userInput.set(userInput.get() + "Q")

def addR():
    if checkCharLimit() and checkLastCharVar():
        userInput.set(userInput.get() + "R")
def addNeg():
    if checkCharLimit() and checkLastCharNeg():
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

def addImp():
    if checkCharLimit() and checkLastCharAndOr():
        userInput.set(userInput.get() + "→")

def addEqui():
    if checkCharLimit() and checkLastCharAndOr():
        userInput.set(userInput.get() + "↔")

def delet():
    userInput.set(userInput.get()[:-1])

def checkCharLimit():
    inputMaximo = 30
    if len(userInput.get()) > inputMaximo:
        return False
    return True

def checkLastCharVar():
    if len(userInput.get()) > 0:
        if userInput.get()[-1] == "P" or userInput.get()[-1] == "Q" or userInput.get()[-1] == "R":
            return False
    return True

def checkLastCharAndOr():
    if len(userInput.get()) > 0:
        if userInput.get()[-1] == "∨" or userInput.get()[-1] == "∧" or userInput.get()[-1] == "¬" or userInput.get()[-1] == "→":
            return False
    return True

def checkLastCharNeg():
    if len(userInput.get()) > 0:
        if userInput.get()[-1] == "¬" or userInput.get()[-1] == "P" or userInput.get()[-1] == "Q" or userInput.get()[-1] == "R":
            return False
    return True

# funcoes para a tabela da verdade
def printTruthTable(truthTable):
    spaceBetwColumns = 30
    spaceBetwLines = 50
    for i in range(1,(2**numOfVar.get())+1):
        for k in range(len(userInput.get())):
            if k == lastColumn.get():
                char = tk.Label(root, text=truthTable[i][k], font="Verdana, 20", bg=darkGrey, fg=blue)
                char.place(x=8 + spaceBetwColumns * k, y=200 + spaceBetwLines * i)
            else:
                char = tk.Label(root, text=truthTable[i][k], font="Verdana, 20", bg=darkGrey, fg=lightGrey)
                char.place(x=8+spaceBetwColumns*k, y=200+spaceBetwLines*i)
    i = i + 1
    lastColumnLabel = tk.Label(root, text="Ultima coluna", font="Verdana, 20", bg=darkGrey, fg=lightGrey)
    lastColumnLabel.place(x=50, y=200+spaceBetwLines*i)
    canvas = tk.Canvas(root, width=20, height=20, bg=blue, highlightthickness=0)
    canvas.place(x=20, y=208 + spaceBetwLines*i)


def printAuxTable(auxTable):
    spaceBetwColumns = 30
    spaceBetwLines = 50
    for i in range(0,(2**numOfVar.get())+1):
        for k in range(len(userInput.get())):
            char = tk.Label(root, text=auxTable[i][k], font="Verdana, 20", bg=darkGrey, fg=lightGrey)
            char.place(x=250+spaceBetwColumns*k, y=200+spaceBetwLines*i)
    i = i + 1
    lastColumnLabel = tk.Label(root, text="Ultima coluna: " + str(lastColumn.get()+1), font="Verdana, 20", bg=darkGrey, fg=lightGrey)
    lastColumnLabel.place(x=8+spaceBetwColumns, y=200+spaceBetwLines*i)

def putTruthVariables(truthTable, auxTable):
    for i in range(1,(2**numOfVar.get())+1):
        binary = bin(i-1)[2:]
        binary = str(binary)

        # botar zeros antes caso precise
        while len(binary) < numOfVar.get():
            binary = '0' + binary

        binPosition = [0,1,2]
        if not "P" in truthTable[0]:
            binPosition.insert(0, 0)
        if not "Q" in truthTable[0]:
            binPosition.insert(1, 0)
        if not "R" in truthTable[0]:
                binPosition.insert(2,0)

        for k in range(len(userInput.get())):
            if truthTable[0][k] == "P":
                if binary[binPosition[0]] == '0':
                    truthTable[i][k] = "T"
                    auxTable[i][k] = "T"
                else:
                    truthTable[i][k] = "F"
                    auxTable[i][k] = "F"
            elif truthTable[0][k] == "Q":
                if binary[binPosition[1]] == '0':
                    truthTable[i][k] = "T"
                    auxTable[i][k] = "T"
                else:
                    truthTable[i][k] = "F"
                    auxTable[i][k] = "F"
            elif truthTable[0][k] == "R":
                if binary[binPosition[2]] == '0':
                    truthTable[i][k] = "T"
                    auxTable[i][k] = "T"
                else:
                    truthTable[i][k] = "F"
                    auxTable[i][k] = "F"
            else:
                truthTable[i][k] = "-"

def putTruthAndOr(truthTable, auxTable, startIndex, finishIndex):
    for i in range(startIndex, finishIndex):
        if auxTable[0][i] == '∨':
            for k in range(1, (2**numOfVar.get())+1):
                if auxTable[k][i-1] == "T" or auxTable[k][i+1] == "T":
                    truthTable[k][i] = "T"
                    auxTable[k][i] = "T"
                    auxTable[k][i+1] = "T"
                    if truthTable[0][i+1] == "¬":
                        auxTable[k][i + 2] = "T"
                        if truthTable[0][i+2] == "(":
                            j = 2
                            while 1:
                                auxTable[k][i+j] = "T"
                                if truthTable[0][i+j] == ")":
                                    break
                                j = j + 1
                    elif truthTable[0][i + 1] == "(":
                        j = 2
                        while 1:
                            auxTable[k][i + j] = "T"
                            if truthTable[0][i + j] == ")":
                                break
                            j = j + 1
                    auxTable[k][i-1] = "T"
                else:
                    truthTable[k][i] = "F"
                    auxTable[k][i] = "F"
                    auxTable[k][i+1] = "F"
                    if truthTable[0][i + 1] == "¬":
                        auxTable[k][i + 2] = "F"
                        if truthTable[0][i + 2] == "(":
                            j = 2
                            while 1:
                                auxTable[k][i + j] = "F"
                                if truthTable[0][i + j] == ")":
                                    break
                                j = j + 1
                    elif truthTable[0][i + 1] == "(":
                            j = 2
                            while 1:
                                auxTable[k][i + j] = "F"
                                if truthTable[0][i + j] == ")":
                                    break
                                j = j + 1
                    auxTable[k][i-1] = "F"
            lastColumn.set(i)
        if auxTable[0][i] == '∧':
            for k in range(1, (2**numOfVar.get())+1):
                if auxTable[k][i-1] == "T" and auxTable[k][i+1] == "T":
                    truthTable[k][i] = "T"
                    auxTable[k][i] = "T"
                    auxTable[k][i + 1] = "T"
                    if truthTable[0][i+1] == "¬":
                        auxTable[k][i + 2] = "T"
                        if truthTable[0][i+2] == "(":
                            j = 2
                            while 1:
                                auxTable[k][i+j] = "T"
                                if truthTable[0][i+j] == ")":
                                    break
                                j = j + 1
                    elif truthTable[0][i + 1] == "(":
                        j = 2
                        while 1:
                            auxTable[k][i + j] = "T"
                            if truthTable[0][i + j] == ")":
                                break
                            j = j + 1
                    auxTable[k][i - 1] = "T"
                else:
                    truthTable[k][i] = "F"
                    auxTable[k][i] = "F"
                    auxTable[k][i + 1] = "F"
                    if truthTable[0][i+1] == "¬":
                        auxTable[k][i + 2] = "T"
                        if truthTable[0][i+2] == "(":
                            j = 2
                            while 1:
                                auxTable[k][i+j] = "F"
                                if truthTable[0][i+j] == ")":
                                    break
                                j = j + 1
                    elif truthTable[0][i + 1] == "(":
                        j = 2
                        while 1:
                            auxTable[k][i + j] = "F"
                            if truthTable[0][i + j] == ")":
                                break
                            j = j + 1
                    auxTable[k][i - 1] = "F"
            lastColumn.set(i)

def putNeg(truthTable, auxTable, startIndex, finishIndex):
    for i in range(startIndex, finishIndex):
        if auxTable[0][i] == "¬":
            for k in range(1, (2**numOfVar.get())+1):
                if auxTable[k][i+1] == "T":
                    truthTable[k][i] = "F"
                    auxTable[k][i] = "F"
                    if truthTable[0][i+1] == "(":
                        j = 1
                        while 1:
                            auxTable[k][i+j] = "F"
                            if truthTable[0][i+j] == ")":
                                break
                            j = j + 1
                    else:
                        auxTable[k][i + 1] = "F"
                elif auxTable[k][i+1] == "F":
                    truthTable[k][i] = "T"
                    auxTable[k][i] = "T"
                    if truthTable[0][i + 1] == "(":
                        j = 1
                        while 1:
                            auxTable[k][i + j] = "T"
                            if truthTable[0][i + j] == ")":
                                break
                            j = j + 1
                    else:
                        auxTable[k][i + 1] = "T"
            lastColumn.set(i)

def putImp(truthTable, auxTable, startIndex, finishIndex):
    for i in range(finishIndex-1, startIndex-1,-1):
        if auxTable[0][i] == '→':
            for k in range(1, (2 ** numOfVar.get()) + 1):
                if auxTable[k][i - 1] == "T" and auxTable[k][i + 1] == "F":
                    truthTable[k][i] = "F"
                    auxTable[k][i] = "F"
                    auxTable[k][i + 1] = "F"
                    if truthTable[0][i + 1] == "¬":
                        auxTable[k][i + 2] = "F"
                        if truthTable[0][i + 2] == "(":
                            j = 2
                            while 1:
                                auxTable[k][i + j] = "F"
                                if truthTable[0][i + j] == ")":
                                    break
                                j = j + 1
                    elif truthTable[0][i + 1] == "(":
                        j = 2
                        while 1:
                            auxTable[k][i + j] = "F"
                            if truthTable[0][i + j] == ")":
                                break
                            j = j + 1
                    if truthTable[0][i - 1] == ")":
                        j = 1
                        while 1:
                            auxTable[k][i - j] = "F"
                            if truthTable[0][i - j] == "(":
                                break
                            j = j + 1
                    else:
                        auxTable[k][i - 1] = "F"
                else:

                    truthTable[k][i] = "T"
                    auxTable[k][i] = "T"
                    auxTable[k][i + 1] = "T"
                    if truthTable[0][i + 1] == "¬":
                        auxTable[k][i + 2] = "T"
                        if truthTable[0][i + 2] == "(":
                            j = 2
                            while 1:
                                auxTable[k][i + j] = "T"
                                if truthTable[0][i + j] == ")":
                                    break
                                j = j + 1
                    elif truthTable[0][i + 1] == "(":
                        j = 2
                        while 1:
                            auxTable[k][i + j] = "T"
                            if truthTable[0][i + j] == ")":
                                break
                            j = j + 1
                    if truthTable[0][i - 1] == ")":
                        j = 1
                        while 1:
                            auxTable[k][i - j] = "T"
                            if truthTable[0][i - j] == "(":
                                break
                            j = j + 1
                    else:
                        auxTable[k][i - 1] = "T"
            lastColumn.set(i)

def putEqui(truthTable, auxTable, startIndex, finishIndex):
    for i in range(finishIndex-1, startIndex-1,-1):
        if auxTable[0][i] == '↔':
            for k in range(1, (2 ** numOfVar.get()) + 1):
                if auxTable[k][i - 1] == auxTable[k][i + 1]:
                    truthTable[k][i] = "T"
                    auxTable[k][i] = "T"
                    auxTable[k][i + 1] = "T"
                    if truthTable[0][i + 1] == "¬":
                        auxTable[k][i + 2] = "T"
                        if truthTable[0][i + 2] == "(":
                            j = 2
                            while 1:
                                auxTable[k][i + j] = "T"
                                if truthTable[0][i + j] == ")":
                                    break
                                j = j + 1
                    elif truthTable[0][i + 1] == "(":
                        j = 2
                        while 1:
                            auxTable[k][i + j] = "T"
                            if truthTable[0][i + j] == ")":
                                break
                            j = j + 1
                    if truthTable[0][i - 1] == ")":
                        j = 1
                        while 1:
                            auxTable[k][i - j] = "T"
                            if truthTable[0][i - j] == "(":
                                break
                            j = j + 1
                    else:
                        auxTable[k][i - 1] = "T"
                else:

                    truthTable[k][i] = "F"
                    auxTable[k][i] = "F"
                    auxTable[k][i + 1] = "F"
                    if truthTable[0][i + 1] == "¬":
                        auxTable[k][i + 2] = "F"
                        if truthTable[0][i + 2] == "(":
                            j = 2
                            while 1:
                                auxTable[k][i + j] = "F"
                                if truthTable[0][i + j] == ")":
                                    break
                                j = j + 1
                    elif truthTable[0][i + 1] == "(":
                        j = 2
                        while 1:
                            auxTable[k][i + j] = "F"
                            if truthTable[0][i + j] == ")":
                                break
                            j = j + 1
                    if truthTable[0][i - 1] == ")":
                        j = 1
                        while 1:
                            auxTable[k][i - j] = "F"
                            if truthTable[0][i - j] == "(":
                                break
                            j = j + 1
                    else:
                        auxTable[k][i - 1] = "T"
            lastColumn.set(i)

def setNumberOfVariables():
    numOfVar.set(0)
    if 'P' in userInput.get():
        numOfVar.set(numOfVar.get() + 1)
    if 'Q' in userInput.get():
        numOfVar.set(numOfVar.get() + 1)
    if 'R' in userInput.get():
        numOfVar.set(numOfVar.get() + 1)

# Função principal da tabela da verdade
def truthTable():

    # limpa a parte de baixo da tela
    clearTable = tk.Label(root, text=" "*30, font=("Arial, 400"), bg=darkGrey)
    clearTable.place(x=0, y=200)

    setNumberOfVariables()

    # cria uma matriz para a tabela que vai ser exibida ao usuario
    truthTable = []
    for i in range((2**numOfVar.get())+1):
        row = []
        for j in range(len(userInput.get())):
            row.append(0)
        truthTable.append(row)
    truthTable[0] = userInput.get()

    #cria uma matriz auxiliar para os calculos
    auxTable = []
    for i in range((2 ** numOfVar.get()) + 1):
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
    putTruthVariables(truthTable, auxTable)

    # Separa e calcula primeiro o que ta em parenteses
    indexesOpenParenth = []
    indexesCloseParenth = []
    for i in range(len(userInput.get())):
        if userInput.get()[i] == '(':
            indexesOpenParenth.append(i)
        elif userInput.get()[i] == ')':
            indexesCloseParenth.append(i)

    for i in range(len(indexesCloseParenth)):
        startString = 0
        finishString = indexesCloseParenth[0]
        for k in range(len(indexesOpenParenth)):
            if indexesOpenParenth[k] > startString and indexesOpenParenth[k] < finishString:
                startString = indexesOpenParenth[k]

        # Remove os indices escolhidos para não serem escolhidos denovo
        indexesOpenParenth.remove(startString)
        indexesCloseParenth.remove(finishString)

        # Faz as negações
        putNeg(truthTable, auxTable, startString, finishString)

        # Faz And e Or
        putTruthAndOr(truthTable, auxTable, startString, finishString)

        # Faz as implicações
        putImp(truthTable,auxTable,startString,finishString)

        putEqui(truthTable, auxTable, 0, len(userInput.get()))

        # Bota os V e F nas colunas dos parenteses na tabela auxiliar
        if auxTable[0][startString] == "(":
            for k in range(1, (2 ** numOfVar.get()) + 1):
                auxTable[k][startString] = auxTable[k][lastColumn.get()]
                auxTable[k][finishString] = auxTable[k][lastColumn.get()]

        # Tira o que estava entre parenteses da formula
        auxTable[0] = auxTable[0][:startString] + " " * (finishString - startString + 1) + auxTable[0][finishString + 1:]


    # faz as negações
    putNeg(truthTable, auxTable, 0, len(userInput.get()))

    # Faz And e Or
    putTruthAndOr(truthTable, auxTable, 0, len(userInput.get()))

    # Faz as implicações
    putImp(truthTable, auxTable, 0, len(userInput.get()))

    putEqui(truthTable, auxTable, 0, len(userInput.get()))

    # Mostra a tabela
    printTruthTable(truthTable)

# Textos e Botões iniciais

formula = tk.Label(root, textvariable = userInput, font=("Verdana, 20"), bg=darkGrey, fg='#DCDCDC')

buttonSize = 20

buttonP = tk.Button(root, text="P", padx=buttonSize, pady=buttonSize, bg = midGrey, command=addP)
buttonQ = tk.Button(root, text="Q", padx=buttonSize, pady=buttonSize,bg = midGrey, command=addQ)
buttonR = tk.Button(root, text="R", padx=buttonSize, pady=buttonSize, bg=midGrey, command=addR)
buttonNeg = tk.Button(root, text="¬", padx=buttonSize, pady=buttonSize,bg = midGrey, command=addNeg)
buttonOpParentesis = tk.Button(root, text="(", padx=buttonSize, pady=buttonSize,bg = midGrey, command=addOpP)
buttonCloParentesis = tk.Button(root, text=")", padx=buttonSize, pady=buttonSize,bg = midGrey, command=addClP)
buttonOr = tk.Button(root, text="∨", padx=buttonSize, pady=buttonSize,bg = midGrey, command=addOr)
buttonAnd = tk.Button(root, text="∧", padx=buttonSize, pady=buttonSize,bg = midGrey, command=addAnd)
buttonImp = tk.Button(root, text="→", padx=buttonSize, pady=buttonSize,bg = midGrey, command=addImp)
buttonEqui = tk.Button(root, text="↔", padx=buttonSize, pady=buttonSize,bg = midGrey, command=addEqui)
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
buttonR.place(x=columnSpace*2, y=row2)
buttonNeg.place(x=columnSpace*3, y=row2)
buttonOpParentesis.place(x=columnSpace*4, y=row2)
buttonCloParentesis.place(x=columnSpace*5, y=row2)
buttonOr.place(x=columnSpace*6, y=row2)
buttonAnd.place(x=columnSpace*7, y=row2)
buttonImp.place(x=columnSpace*8, y=row2)
buttonEqui.place(x=columnSpace*9, y=row2)
buttonDel.place(x=columnSpace*10, y=row2)
buttonTruthTable.place(x=140, y=row3)

# loop principal
root.mainloop()
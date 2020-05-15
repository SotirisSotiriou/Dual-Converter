import sys as system
import os

def convert(filename):
    #input
    cPrimal, APrimal, bPrimal, maxminPrimal, eqinPrimal, variablesPrimal = parse(filename)
    variablesEqinPrimal = len(cPrimal)*[1]

    print(2*"\n" + "Primal LP:")
    print("A = " + str(APrimal))
    print("c = " + str(cPrimal))
    print("b = " + str(bPrimal))
    print("maxmin = " + str(maxminPrimal))
    print("eqin = " + str(eqinPrimal))
    print("variables = " + str(variablesPrimal))
    print("variablesEqin = " + str(variablesEqinPrimal))

    #conversion
    print(2*"\n" + "Converting...")

    ADual = inverse(APrimal)
    cDual = bPrimal
    bDual = cPrimal
    maxminDual = -maxminPrimal
    eqinDual = setDualEquations(maxminPrimal, variablesEqinPrimal)
    variablesDual = setDualVariables(len(bPrimal))
    variablesEqinDual = setDualVariablesEquations(maxminPrimal, eqinPrimal)

    newFile = createNewFile(filename)
    writeNewFile(newFile, cDual, ADual, bDual, eqinDual, maxminDual, variablesDual, variablesEqinDual)


    return ADual, cDual, bDual, maxminDual, eqinDual, variablesDual, variablesEqinDual




#--------------------------------- Dual Converter Methods ----------------------------------------------------

def inverse(table):
    return [list(x) for x in zip(*table)]


def setDualEquations(maxminPrimal, variablesEqinPrimal):
    eqinDual = len(variablesEqinPrimal)*[None]
    if maxminPrimal == -1:
    #if variable >= 0 (variablesEqin = 1) then eqinDual = "<="
    #if variable <= 0 (variablesEqin = -1) then eqinDual = ">="
    #if variable free (variablesEqin = 0) then eqinDual = "="
        for i in range(len(variablesEqinPrimal)):
            if variablesEqinPrimal[i] == 1:
                eqinDual[i] = -1
            elif variablesEqinPrimal == 0:
                eqinDual[i] = 0
            elif variablesEqinPrimal == -1:
                eqinDual = 1
            else:
                print("Error: wrong variables equation")
                system.exit(0)
    elif maxminPrimal == 1:
    #if dual variable >= 0 (variablesEqin = 1) then primal eqinDual = ">=" (eqin = 1)
    #if dual variable <= 0 (variablesEqin = -1) then primal eqinDual = "<=" (eqin = -1)
    #if dual variable free (variablesEqin = 0) then primal eqinDual = "=" (eqin = 0)
        for i in range(len(variablesEqinPrimal)):
            if variablesEqinPrimal[i] == 1:
                eqinDual[i] = 1
            elif variablesEqinPrimal == 0:
                eqinDual[i] = 0
            elif variablesEqinPrimal == -1:
                eqinDual = -1
            else:
                print("Error: wrong variables equation")
                system.exit(0)
    else:
        print("Wrong primal LP type")
        system.exit(0)
    return eqinDual


def setDualVariablesEquations(maxminPrimal, eqinPrimal):
    variablesEqinDual = len(eqinPrimal)*[None]

    if maxminPrimal == -1:
    #if primal equation = ">=" (eqinPrimal = 1) then dual variable >= 0 (variablesEqin = 1)
    #if prinal equation = "<=" (eqinPrimal = -1) then dual variable <=0 (variablesEqin = -1)
    #if primal equation = "=" (eqinPrimal = 0) then dual variable free (variablesEqin = 0)
        for i in range(len(eqinPrimal)):
            if eqinPrimal[i] == 1:
                variablesEqinDual[i] = 1
            elif eqinPrimal[i] == -1:
                variablesEqinDual[i] = -1
            elif eqinPrimal[i] == 0:
                variablesEqinDual[i] = 0
            else:
                print("Error: wrong primal LP equation")
                system.exit(0)
    elif maxminPrimal == 1:
    #if primal equation = ">=" (eqinPrimal = 1) then dual variable <= 0 (variablesEqin = -1)
    #if prinal equation = "<=" (eqinPrimal = -1) then dual variable >=0 (variablesEqin = 1)
    #if primal equation = "=" (eqinPrimal = 0) then dual variable free (variablesEqin = 0)
        for i in range(len(eqinPrimal)):
            if eqinPrimal[i] == 1:
                variablesEqinDual[i] = -1
            elif eqinPrimal[i] == -1:
                variablesEqinDual[i] = 1
            elif eqinPrimal[i] == 0:
                variablesEqinDual[i] = 0
            else:
                print("Error: wrong primal LP equation")
                system.exit(0)
    else:
       print("Wrong primal LP type")
       system.exit(0)
    return variablesEqinDual


def setDualVariables(bPrimalLen):
    variablesDual = bPrimalLen*[None]
    for i in range(bPrimalLen):
        variablesDual[i] = "w"+str(i+1)
    return variablesDual


def export(oldfilename, c, A, b, eqin, maxmin):
    newfile = createNewFile(oldfilename)
    writeNewFile(newfile, c, A, b, eqin, maxmin)



def createNewFile(filename):
        noExtensionName = ""
        extension = ""
        index = 0
        while filename[index] != '.':
            noExtensionName += filename[index]
            index += 1
        while index < len(filename):
            extension += filename[index]
            index += 1
        newFileName =  noExtensionName + "Dual" + extension
        file = None
        try:
            if os.path.exists(newFileName):
                os.remove(newFileName)
            file = open(newFileName, "w")
        except FileNotFoundError:
            print("File not found\n")

            system.exit(0)
        except PermissionError:
            print("You have not permission to write in this file\n")

            system.exit(0)
        return file



def writeNewFile(file, c, A, b, eqin, maxmin, variables, variablesEqin): 
    #the tables c, A, b, Equin, maxmin, variables are refering to dual problem
    if maxmin == 1:
        file.write("max ")
    elif maxmin == -1:
        file.write("min ")
    file.write("z = ")
    
    index = 0
    while index < len(c):
        if c[index] >= 0:
            file.write("+ " + str(c[index]))
        else:
            file.write("- " + str(abs(c[index])))
        file.write(str(variables[index]) + " ")
        index += 1
    file.write("\ns.t.\n")
    for row in range(0,len(A)):
        for col in range(0, len(A[row])):
            if A[row][col] >= 0:
                file.write('+ ' + str(A[row][col]))
                file.write(str(variables[col]) + " ")
            else:
                file.write("- " + str(abs(A[row][col])))
                file.write(str(variables[col]) + " ")
        if eqin[row] == -1:
            file.write("<= ")
            file.write(str(b[row]) + "\n")
        elif eqin[row] == 0:
            file.write("= ")
            file.write(str(b[row]) + "\n")
        elif eqin[row] == 1:
            file.write(">= ")
            file.write(str(b[row]) + "\n")
    file.write(2*"\n")
    for i in range(len(variablesEqin)):
        file.write(str(variables[i]))
        if variablesEqin[i] == 1:
            file.write(" >= 0\n")
        elif variablesEqin[i] == -1:
            file.write(" <= 0\n")
        elif variablesEqin == 0:
            file.write(" -> free\n")
        else:
            print("Error: wrong variable equation")
            system.exit(0)



#------------------------------------ Parser ------------------------------------------------------------


def parse(filename):
    file = None
    maxmin = 0
    Eqin = []
    A = []
    b = []
    c = []
    Variables = []  # a list of the problem variable names e.g. x1, x2, x3, ... or x, y, z, w, ...

    print("Parsing...")

    try:
        file = open(filename, "r")
        lines = file.readlines()
    except FileNotFoundError:
        print("File not found\n")
        system.exit(0)
    except PermissionError:
        print("You have not permission to write in this file\n")
        system.exit(0)

    firstLine = 0
    while maxmin == 0:
        maxmin, firstLine = readProblemType(lines[firstLine], firstLine)
    if maxmin == 1 or maxmin == -1:
        print("\nMaxmin check = True")
    index = 3
    index = readFunc(lines[firstLine], index)
    c, Variables = readVariablesAndC(lines[firstLine], index)

    subjectLine = firstLine + 1
    subjectLineFound = False
    while not subjectLineFound:
        check, subjectLine, subjectLineFound = subjectCheck(lines[subjectLine], subjectLine)
    print("Subject check = ", str(check))
    if check == False:
        print("Syntax Error. 2nd line must be st, s.t. or subject\n")
        system.exit(0)

    columnsNum = len(Variables)

    for line in lines[subjectLine+1:]:
        Arow, belement, eqinelement = readConstraint(line, Variables, columnsNum)
        if Arow:
            A.append(Arow)
        if belement != "":
            b.append(belement)
        if eqinelement is not None:
            Eqin.append(eqinelement)
    file.close()
    return c, A, b, maxmin, Eqin, Variables


# ------------------------------------Parser Methods --------------------------------------

def readProblemType(line, lineIndex):
    if lineIsEmpty(line):
        lineIndex += 1
        return 0, lineIndex
    if line.startswith("max"):
        return 1, lineIndex
    elif line.startswith("min"):
        return -1, lineIndex
    else:
        print("\nMaxmin check = False")
        print("Syntax Error. Wrong problem type.\n")
        system.exit(0)


def readVariablesAndC(line, index):
    var = []
    c = []
    number = ""
    vartext = ""
    number, vartext, index = readFirstElementI(line, index)
    if number is not None and vartext is not None:
        c.append(number)
        var.append(vartext)
    while index < len(line) - 1:
        number, vartext, index = readElementI(line, index)
        if number is not None and vartext is not None:
            c.append(number)
            var.append(vartext)
    return c, var


def readConstraint(line, var, columns):
    index = 0
    Arow = [0]*columns
    belement = ""
    number = ""
    elementindex = 0
    eqinelement = None

    if lineIsEmpty(line):
        return [], belement, eqinelement
    if not equationExists(line):
        print("Syntax Error. Equation is missing\n")
        system.exit(0)
    number, elementindex, index = readFirstElementII(line, var, index)
    if number != "":
        Arow[elementindex] = number
    while index < len(str(line))-1:
        number, belement, elementindex, eqinelement, index = readElementII(line, var, index)
        if number != "":
                Arow[elementindex] = number
    if belement != "":
        return Arow, int(belement), eqinelement
    return Arow, belement, eqinelement


# ------------------------------------- TOOLS ---------------------------------------

def subjectCheck(line, subIndex):
    checktext = ""
    index = 0
    while not ( str(line[index]).isalpha() or lineIsEmpty(line) ):
        index += 1
    if str(line[index]).isalpha():
        while not str(line[index]).isspace():
            checktext += str(line[index])
            index += 1
    elif lineIsEmpty(line):
        subIndex += 1
        return False, subIndex, False
    else:
        print("Subject check = False")
        print("Syntax Error. Subject line error.\n")
        system.exit(0)
    while not ( str(line[index]).isalpha() or str(line[index]) == '\n' ):
        index += 1
    if str(line[index]).isalpha():
        print("Subject check = False")
        print("Syntax Error. Subject line error\n")
        system.exit(0)
    elif checktext == "subject".lower() or checktext == "st".lower() or checktext == "s.t.".lower():
        return True, subIndex, True
    else:
        return False, subIndex, True


def readVariable(text, index):
    vartext = ""
    while not (str(text[index]).isalpha() or index == len(str(text))-1):
        index += 1
    if str(text[index]).isalpha():
        while (str(text[index]).isalpha() or str(text[index]).isdigit()) and index < len(str(text))-1:
            vartext += str(text[index])
            index += 1
        if index == len(str(text)) - 1:
            if str(text[index]).isalpha():
                vartext += str(text[index])
    return vartext, index


def readNumber(text, index):
    numbertext = ""
    if str(text[index]).isdigit():
        while str(text[index]).isdigit():
            numbertext += str(text[index])
            index += 1
        return numbertext, index
    index += 1
    while not (str(text[index]).isdigit() or str(text[index]).isalpha() or str(text[index]) == '\n' or index == len(str(text))-1
                or str(text[index]) == '-' or str(text[index]) == '+' ):
        index += 1
    if str(text[index]).isdigit():
        while not ( str(text[index]).isdigit() or  index<len(str(text))-1):
            index += 1
        while str(text[index]).isdigit() and index<len(str(text))-1:
            numbertext += str(text[index])
            index += 1
        if index == len(str(text))-1:
            if str(text[index]).isdigit():
                numbertext += str(text[index])
        if str(text[index]) == '-':
            numbertext = '-' + numbertext
    elif str(text[index]).isalpha():
        numbertext = "1"
    elif str(text[index]) == '-' or str(text[index]) == '+':
        print("Syntax Error. sign typed twice.\n")
        system.exit(0)
    return numbertext, index


#read first element from
def readFirstElementI(line, index):
    numbertext = ""
    vartext = ""
    while not (str(line[index]).isalpha() or str(line[index]).isdigit() or line[index] == '-' or line[
        index] == '+' or str(line[index]) == "\n"):
        index += 1
    if str(line[index]).isalpha():
        numbertext = "1"
        vartext, index = readVariable(line, index)
    elif str(line[index]).isdigit():
        numbertext, index = readNumber(line, index)
        vartext, index = readVariable(line, index)
    elif str(line[index]) == '+':
        numbertext, index = readNumber(line, index)
        vartext, index = readVariable(line, index)
    elif str(line[index]) == '-':
        numbertext, index = readNumber(line, index)
        vartext, index = readVariable(line, index)
        numbertext = "-" + numbertext
    if numbertext is not None:
        return int(numbertext), vartext, index
    return numbertext, vartext, index


#read first element from the constraints
def readFirstElementII(line, var, index):
    numbertext = ""
    vartext = ""
    elementIndex = None
    while not (str(line[index]).isdigit() or str(line[index]).isalpha() or str(line[index]) == '-' or
                str(line[index]) == '+' or str(line[index]) == '\n'):
        index += 1
    if str(line[index]) == '\n':
        print("Syntax Error...")
        system.exit(0)
    elif str(line[index]) == '+' or str(line[index]).isdigit():
        numbertext, index = readNumber(line, index)
        vartext, index = readVariable(line, index)
        try:
            elementIndex = var.index(vartext)
        except ValueError:
            print("Syntax Error. Variable name not found.\n")

            system.exit(0)
    elif str(line[index]) == '-':
        numbertext, index = readNumber(line, index)
        vartext, index = readVariable(line, index)
        numbertext = "-" + numbertext
        try:
            elementIndex = var.index(vartext)
        except ValueError:
            print("Syntax Error. Variable name not found.\n")
            system.exit(0)
    if numbertext != "":
        return int(numbertext), elementIndex, index
    return numbertext, elementIndex, index


#read an element from
def readElementI(line, index):
    numbertext = ""
    vartext = ""
    while not (str(line[index]).isdigit() or str(line[index]).isalpha() or str(line[index]) == '-' or str(
            line[index]) == '+' or str(line[index]) == "\n"):
        index += 1
    if str(line[index]).isdigit() or str(line[index]).isalpha():
        print("Syntax Error. Sign is missing.\n")

        system.exit(0)
    elif str(line[index]) == '+':
        numbertext, index = readNumber(line, index)
        vartext, index = readVariable(line, index)
    elif str(line[index]) == '-':
        numbertext, index = readNumber(line, index)
        vartext, index = readVariable(line, index)
        numbertext = "-" + numbertext
    elif str(line[index]) == "\n":
        return None, None, index
    if numbertext != "":
        return int(numbertext), vartext, index
    return numbertext, vartext, index


#read an element from the constraints
def readElementII(line, var, index):
    numbertext = ""
    vartext = ""
    belement = ""
    elementIndex = None
    eqinelement = None
    isNegative = False
    while not (str(line[index]).isdigit() or str(line[index]).isalpha() or str(line[index]) == '-' or str(line[index]) == '+' or
                str(line[index]) == '\n' or str(line[index]) == '>' or str(line[index]) == '<' or str(line[index]) == '=' or index == len(line)-1):
        index += 1
    if str(line[index]).isdigit() or str(line[index]).isalpha():
        print("Syntax Error. Sign is missing.")

        system.exit(0)
    elif str(line[index]) == '<' or str(line[index]) == '>' or str(line[index]) == '=':
        eqinelement, index = readEquation(line, index)
        while not ( str(line[index]).isdigit() or str(line[index]) == '+' or str(line[index]) == '-' ):
            index += 1
        if str(line[index]) == '-':
            isNegative = True
        belement, index = readNumber(line, index)
        if isNegative:
            belement = "-" + belement
    elif str(line[index]) == '+' or str(line[index]) == '-':
        if str(line[index]) == '-':
            isNegative = True
        numbertext, index = readNumber(line, index)
        vartext, index = readVariable(line, index)
        try:
            elementIndex = var.index(vartext)
        except ValueError:
            print("Syntax Error. Variable name not found.\n")

            system.exit(0)
        if isNegative:
            numbertext = "-" + numbertext
    if numbertext != "":
        if belement != "":
            return int(numbertext), int(belement), elementIndex, eqinelement, index
        return int(numbertext), belement, elementIndex, eqinelement, index
    return numbertext, belement, elementIndex, eqinelement, index


def readEquation(text, index):
    equationtext = ""
    while not ( str(text[index]) == '>' or str(text[index]) == '<' or str(text[index]) == '=' or str(text[index]) == '\n' ):
        index += 1
    if str(text[index]) == '\n':
        print("Syntax Error. Wrong equation.\n")

        system.exit(0)
    while not ( str(text[index]).isspace() or str(text[index]) == '\n' or str(text[index]) == '-' or str(text[index]) == '+' ):
        equationtext += str(text[index])
        index += 1
    if equationtext == ">=":
        return 1, index
    elif equationtext == "<=":
        return -1, index
    elif equationtext == "=":
        return 0, index
    else:
        print("Syntax Error. Wrong equation.\n")

        system.exit(0)
    return equationtext, index


def equationExists(line):
    if ">" in line or "<" in line or "=" in line:
        return True
    else:
        return False

def lineIsEmpty(line):
    isEmpty = True
    index = 0
    while index < len(line)-1:
        if str(line[index]).isalnum():
            isEmpty = False
            break
        index += 1
    return isEmpty


def readFunc(text, index):
    while not ( str(text[index]).isalnum() or str(text[index]) == '\n' or str(text[index]) == '-' or str(text[index]) == '+'):
        index += 1
    if str(text[index]).isalpha():
        while str(text[index]).isalpha() or str(text[index]).isdigit():
            index += 1
        while not (str(text[index]) == '=' or str(text[index]) == '\n'):
            index += 1
        if str(text[index]) == '=':
            return index
        else:
            print("Syntax Error. '=' symbol is missing.\n")

            system.exit(0)
    else:
        print("Syntax Error. Function name is missing or is wrong.\n")

        system.exit(0)
    return index




def main():
    filename = str(input("\nEnter problem file name: "))
    A, c, b, maxmin, eqin, variables, variablesEqin = convert(filename)
    print(2*"\n" + "Dual LP:")
    print("A = " + str(A))
    print("c = " + str(c))
    print("b = " + str(b))
    print("maxmin = " + str(maxmin))
    print("eqin = " + str(eqin))
    print("variables = " + str(variables))
    print("variablesEqin = " + str(variablesEqin))


if __name__ == "__main__":
    main()



from Parser import parse

def convert(filename):
    cDual = []
    ADual = []
    bDual = []
    eqinDual = []
    maxminDual = []
    #input
    cPrimal, APrimal, bPrimal, maxminPrimal, eqinPrimal = parse(filename)

    #conversion






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



def writeNewFile(file, c, A, b, eqin, maxmin, variables): 
    #the tables c, A, b, Equin, maxmin, variables are refering to dual problem
    if maxmin == 1:
        file.write("max ")
    elif maxmin == -1:
        file.write("min ")
    file.write("z = ")
    
    index = 0
    while index < len(c):
        file.write(str(c[index]))
        file.write(str(variables[index]))
    file.write("\ns.t.\n")
    for row in range(0,len(A)):
        for col in range(0, len(A[0])):
            if A[row][col] >= 0:
                file.write('+' + str(A[row][col]))
                file.write(str(variables[col]) + " ")
            else:
                file.write(str(A[row][col]))
                file.write(str(variables[col]) + " ")
        if eqin[row] == -1:
            file.write("<= ")
            file.write(str(b[row]))
        elif eqin[row] == 0:
            file.write("= ")
            file.write(str(b[row]))
        elif eqin[row] == 1:
            file.write(">= ")
            file.write(str(b[row]))



def main():
    filename = str(input("\nEnter problem file name: "))
    convert(filename)


if __name__ == "__main__":
    main()



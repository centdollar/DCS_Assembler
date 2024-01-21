import vfm6849_SymbolInfo
valid_start_symbols = vfm6849_SymbolInfo.valid_start_symbols

assemblyFile = "test.asm"
reg = {'r0':'00000', 'r1':'00001', 'r2':'00010', 'r3':'00011', 'r4':'00100', 'r5':'00101', 'r6':'00110', 'r7':'00111'}

class Section:
    def __init__(self, sectName):
        self.sectName = sectName
    def disp(self):
        print("sectName         : " + self.sectName)
        print("startIndex       : " + str(self.startIndex))
        print("endIndex         : " + str(self.endIndex))
        print("data             : " + str(self.data))
        print("translatedData   : " + str(self.translatedData))
        print("originalLineNum  : " + str(self.originalLineNum))
    
    sectName = ''
    startIndex = 0
    endIndex = 0
    data = []
    originalLineNum = []
    translatedData = []
    
    


def main():
    # TODO: add file not found checking
    sectList = getSections(assemblyFile)
    sectList = parseSections(sectList)
    sectList = translateSections(sectList)
    sectList[0].disp()



    return 1

def translateSections(sectList):
    translateList = []
    for sect in sectList:
        if (sect.sectName == 'data'):
            for line in range(len(sect.data)):
                # split line into tokens
                token = sect.data[line].split(" ")

                # add 
                if (token[0] == 'add'):
                    if (token[1] not in reg):
                        print("Error: Invalid Syntax in line {} -> {}".format(sect.originalLineNum[line],token))
                        continue
                    if (token[2] not in reg):
                        print("Error: Invalid Syntax in line {} -> {}".format(sect.originalLineNum[line],token))
                        continue
                    sect.translatedData.append('0101' + reg[token[1]] + reg[token[2]])


                # addc
                elif (token[0] == 'addc'):
                    if(token[1] not in reg):
                        print("Error: Invalid Syntax in line {} -> {}".format(sect.originalLineNum[line],token))
                        continue
                    if(token[2][0] != "#"):
                        print("Error: Invalid Syntax in line {} -> {}".format(sect.originalLineNum[line],token))
                        continue
                    if(int(token[2][1:]) > 31):
                        print("Error: Invalid Syntax in line {} -> {}".format(sect.originalLineNum[line],token))
                        continue
                    sect.translatedData.append('0110' + reg[token[1]] + "{0:b}".format(int(token[2][1:])))
                
                
                
                else:
                    print("Error: Invalid Syntax -> {}".format(token))
    
        translateList.append(sect)

    return translateList




# gets rid of redundant lines and excludes comments from going onto translation
def parseSections(sectList):
    retList = []
    for sect in sectList:
        if (sect.sectName == 'data'):

            for line in range(len(sect.data)):
                if sect.data[line] == "":
                    continue
                else:
                    sect.originalLineNum.append(line + 2)
            # remove empty spaces
            while ("" in sect.data):
                sect.data.remove("")
        retList.append(sect)
    # sectList[0].disp()
    return retList


def getSections(fileName):
    sectList = []
    with open(fileName, "r") as f:
        dataSection = Section('data')
        F = f.readlines()
        for line in range(len(F)):
            F[line] = F[line].strip("\n")
        
        # Get the info in each section
        for line in range(len(F)):
            if (F[line] == '.code'):
                dataSection.startIndex = line
            if (F[line] == '.endcode'):
                dataSection.endIndex = line
        dataSection.data = F[dataSection.startIndex + 1:dataSection.endIndex]
        sectList.append(dataSection)

    return sectList
        


main()
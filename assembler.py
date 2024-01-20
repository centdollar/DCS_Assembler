import vfm6849_SymbolInfo
valid_start_symbols = vfm6849_SymbolInfo.valid_start_symbols

assemblyFile = "test.asm"
reg = {'r0':'00000', 'r1':'00001'}

class Section:
    def __init__(self, sectName):
        self.sectName = sectName
    def disp(self):
        print(self.sectName)
        print(self.startIndex)
        print(self.endIndex)
        print(self.data)
        print(self.translatedData)
    
    sectName = ''
    startIndex = 0
    endIndex = 0
    data = []
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
                # add instr
                if (token[0] == 'add' and (token[1] in reg) and (token[2] in reg)):
                    sect.translatedData.append('0101' + reg[token[1]] + reg[token[2]])
    
        translateList.append(sect)

    return translateList




# gets rid of redundant lines and excludes comments from going onto translation
def parseSections(sectList):
    retList = []
    for sect in sectList:
        if (sect.sectName == 'data'):
            # remove empty spaces
            while ("" in sect.data):
                sect.data.remove("")
        retList.append(sect)
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
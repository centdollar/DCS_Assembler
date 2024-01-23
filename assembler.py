import vfm6849_SymbolInfo
instructionDict = vfm6849_SymbolInfo.valid_start_symbols

assemblyFile = "test.asm"

regRegInstr = {'add'   :'000101', 'sub'   :'000110', 'and'   :'001010', 'or'    :'001011', 'vadd'  :'001110', 'vsub'  :'001111', 'mul'   :'010000', 'div'   :'010001', 'xor'   :'010010', 'in'    :'011101', 'out'   :'011110', 'swp'   :'000011', 'cpy'   :'000010',}
regImmedInstr = {'addc'  :'000111', 'subc'  :'001000', 'rrc'   :'001101', 'srl'   :'010011', 'sra'   :'010100', 'rotl'  :'010101', 'rotr'  :'010110', 'rln'   :'010111', 'rlz'   :'011000', 'rrn'   :'011001', 'rrz'   :'011010'}

jumpInstr = {'ju'    :'000100*0000', 'jc1'   :'000100*1000', 'jn1'   :'000100*0100', 'jv1'   :'000100*0010', 'jz1'   :'000100*0001', 'jc0'   :'000100*0111', 'jn0'   :'000100*1011', 'jv0'   :'000100*1101', 'jz0'   :'000100*1110',}


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
        print("dataSectionLabels: " + str(self.dataSectionLabels))
    
    sectName = ''
    startIndex = 0
    endIndex = 0
    data = []
    originalLineNum = []
    translatedData = []
    dataSectionLabels = {}


    
    


def main():
    # TODO: add file not found checking
    # TODO: make one sectList object instead of passing all these copies around
    sectList = getSections(assemblyFile)
    sectList = parseSections(sectList)
    sectList = translateSections(sectList)
    sectList = calculateJumps(sectList)
    sectList[0].disp()



    return 1

def calculateJumps(sectList):
    postJumpCalc = []
    for sect in sectList:
        if (sect.sectName == 'data'):
            for line in range(len(sect.translatedData)):
                if (sect.translatedData[line][1:] in sect.dataSectionLabels):
                    sect.translatedData[line] = "{:16b}".format(calculateOffset(line, sect.dataSectionLabels[sect.translatedData[line][1:]]), 16)[1:]

    postJumpCalc.append(sect)

    return postJumpCalc

def calculateOffset(currAddr, labelAddr):
    if currAddr > labelAddr:
        return twosComp(currAddr - labelAddr + 1, 16)
    else: return labelAddr - currAddr - 1

def twosComp(val, bits):
    val = val - (1 << bits)
    return val

def translateSections(sectList):
    translateList = []
    for sect in sectList:
        if (sect.sectName == 'data'):
            for line in range(len(sect.data)):
                # split line into tokens
                token = sect.data[line].split(" ")

                # Label support
                if (token[0][0] == '@'):
                    if (token[1] in regRegInstr):
                        if (token[2] not in reg):
                            print("Error: Invalid Syntax in line {} -> {}".format(sect.originalLineNum[line],token))
                            continue
                        if (token[3] not in reg):
                            print("Error: Invalid Syntax in line {} -> {}".format(sect.originalLineNum[line],token))
                            continue
                    if (token[0][1:] not in sect.dataSectionLabels):
                        sect.dataSectionLabels[token[0][1:]] = line
                    
                    sect.translatedData.append(regRegInstr[token[1]] + reg[token[2]] + reg[token[3]])
                    continue

                # handles instructions with the reg reg parameters
                if (token[0] in regRegInstr):
                    if (token[1] not in reg):
                        print("Error: Invalid Syntax in line {} -> {}".format(sect.originalLineNum[line],token))
                        continue
                    if (token[2] not in reg):
                        print("Error: Invalid Syntax in line {} -> {}".format(sect.originalLineNum[line],token))
                        continue
                    sect.translatedData.append(regRegInstr[token[0]] + reg[token[1]] + reg[token[2]])
                    continue

                # handles instructions with the reg immediate parameters
                if (token[0] in regImmedInstr):
                    if(token[1] not in reg):
                        print("Error: Invalid Syntax in line {} -> {}".format(sect.originalLineNum[line],token))
                        continue
                    if(token[2][0] != "#"):
                        print("Error: Invalid Syntax in line {} -> {}".format(sect.originalLineNum[line],token))
                        continue
                    if(int(token[2][1:]) > 31):
                        print("Error: Invalid Syntax in line {} -> {}".format(sect.originalLineNum[line],token))
                        continue
                    sect.translatedData.append(regImmedInstr[token[0]] + reg[token[1]] + "{0:b}".format(int(token[2][1:])))
                    continue

                if (token[0] in jumpInstr):
                    if(token[1] not in reg):
                        print("Error: Invalid Syntax in line {} -> {}".format(sect.originalLineNum[line],token))
                        continue
                    if(token[2][0] != "@"):
                        print("Error: Invalid Syntax in line {} -> {}".format(sect.originalLineNum[line],token))
                        continue
                    sect.translatedData.append(jumpInstr[token[0]].replace("*", reg[token[1]]))
                    sect.translatedData.append(token[2])
                    continue

                


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
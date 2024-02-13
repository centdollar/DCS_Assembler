import vfm6849_SymbolInfo
instructionDict = vfm6849_SymbolInfo.valid_start_symbols

assemblyFile = "test.asm"

regRegInstr = {
'in'    :'100000', 
'out'   :'100001',

'swp'   :'100010', 
'cpy'   :'100011',

'add'   :'101000', 
'sub'   :'101001', 
'mul'   :'101010', 
'div'   :'101011',

'xor'   :'100100', 
'and'   :'100101', 
'or'    :'100110',
'not'   :'100111',

'fadd'  :'001000',
'fsub'  :'001001',
'fmul'  :'001010',
'fdiv'  :'001011',

'vadd'  :'110000', 
'vsub'  :'110001',
'vmul'  :'110010', 
'vdiv'  :'110011'
}


regImmedInstr = {
'cmp'   :'010000',

'srl'   :'010001', 
'sra'   :'010010',
'rotl'  :'010011', 
'rotr'  :'010100', 

'addc'  :'010101', 
'subc'  :'010110', 

'rrc'   :'011000',
'rrn'   :'011001', 
'rrz'   :'011010',

'rln'   :'011100', 
'rlz'   :'011101'
}


jumpInstr = {
'ju'   :'000100*00000', 
'jc1'   :'000100*10000', 
'jn1'   :'000100*01000', 
'jv1'   :'000100*00100', 
'jz1'   :'000100*00010', 
'jc0'   :'000100*01110', 
'jn0'   :'000100*10110', 
'jv0'   :'000100*11010', 
'jz0'   :'000100*11100'
}


memInstr = {
'ld'    :'000000', 
'st'     :'000001'
}


reg = {'r0' :'00000', 'r1' :'00001', 'r2' :'00010', 'r3' :'00011', 'r4' :'00100', 'r5' :'00101', 'r6' :'00110', 'r7' :'00111', 
       'r8' :'01000', 'r9' :'01001', 'r10':'01010', 'r11':'01011', 'r12':'01100', 'r13':'01101', 'r14':'01110', 'r15':'01111',
       'r16':'10000', 'r17':'10001', 'r18':'10010', 'r19':'10011', 'r20':'10100', 'r21':'10101', 'r22':'10110', 'r23':'10111', 
       'r24':'11000', 'r25':'11001', 'r26':'11010', 'r27':'11011', 'r28':'11100', 'r29':'11101', 'r30':'11110', 'r31':'11111'}

MIF_FILE_HEADER = 'WIDTH = 16;\n' + 'DEPTH = 16384;\n' + 'ADDRESS_RADIX = DEC;\n' + 'DATA_RADIX = BIN;\n\n\n' + 'CONTENT BEGIN\n'
ADDR_RANGE = 16384

WRITE_TO_MODELSIM = True

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
        print("translateListComments: " + str(self.translateListComments))

    
    sectName = ''
    startIndex = 0
    endIndex = 0
    data = []
    originalLineNum = []
    translatedData = []
    dataSectionLabels = {}
    translateListComments = []

class constSection:
    def __init__(self, sectName):
        self.sectName = sectName

    def disp(self):
        print("sectName         : " + self.sectName)
        print("constData             : " + str(self.constData))
        print("constDict             : " + str(self.constDict))
        print("originalLineNum  : " + str(self.originalLineNum))


    sectName = ''
    constData = []
    constDict = {}
    originalLineNum = []

class dataSect:
    def __init__(self, sectName):
        self.sectName = sectName

    def disp(self):
        print("sectName         : " + self.sectName)
        print("data         : " + str(self.data))
        print("originalLineNum         : " + str(self.originalLineNum))
        print("dataDict         : " + str(self.dataDict))

    sectName = ''
    data = []
    originalLineNum = []
    dataDict = {}


def main():
    # TODO: add file not found checking
    # TODO: make one sectList object instead of passing all these copies around
    sectList = getSections(assemblyFile)
    sectList = parseSections(sectList)
    dataSect = sectList[2]
    constSect = sectList[1]
    sectList = translateSections(sectList)
    sectList = calculateJumps(sectList)
    writeOutMifFile(sectList[0], dataSect)
    sectList[0].disp()
    return 1





def writeOutMifFile(codeSect, dataSect):
    if WRITE_TO_MODELSIM:
        
        # Write out the instruction data to the proper mif file
        with open("../DCS/simulation/modelsim/test16.mif", "w") as f:
            f.write(MIF_FILE_HEADER)
            for index in range(len(codeSect.translatedData)):
                f.write("{}:{}; % {} %\n".format(index, codeSect.translatedData[index], codeSect.translateListComments[index]))
            f.write('[{} .. {}] : 0000000000000000; %EMPTY MEMORY LOCATIONS %\n'.format(index + 1, ADDR_RANGE - 1))
            f.write('END;\n')

        
        # Write out the data to go into MM
        with open("../DCS/simulation/modelsim/test16_MM.mif", "w") as f:
            f.write(MIF_FILE_HEADER)
            if not dataSect.dataDict:
                f.write('[{} .. {}] : 0000000000000000; %EMPTY MEMORY LOCATIONS %\n'.format(0, ADDR_RANGE - 1))
            else:
                i = 0
                usedDataSegs = []

                for addr in dataSect.dataDict:
                    usedDataSegs.append(int(dataSect.dataDict[addr], 16))

                # Loop through all possible addresses
                # if the current addr is not in usedDataSegs[]
                    notUsedStart = 0
                    notUsedEnd = 0
                for i in range(ADDR_RANGE - 1):

                    if i not in usedDataSegs:
                        notUsedEnd = notUsedEnd + 1
                        continue
                    else:

                        if notUsedEnd != notUsedStart:
                            f.write('[{} .. {}] : 0000000000000000; %EMPTY MEMORY LOCATIONS %\n'.format(notUsedStart, notUsedEnd - 1))
                        notUsedStart = i+1
                        notUsedEnd = i + 1
                        # index = usedDataSegs.find("i")
                        f.write("{}:{}; % {} %\n".format(str(i), "0000000000000000", "used"))
            f.write('END;\n')


            
                
                # f.write("{}:{}; % {} %\n".format(str(i), "0000000000000000", dataSect.dataDict[index]))
                # i = i + 1
            # f.write('[{} .. {}] : 0000000000000000; %EMPTY MEMORY LOCATIONS %\n'.format(i + 1, ADDR_RANGE - 1))
            # f.write('END;\n')

    
    with open("../DCS/test16.mif", "w") as f:
            f.write(MIF_FILE_HEADER)
            for index in range(len(codeSect.translatedData)):
               f.write("{}:{}; % {} %\n".format(index, codeSect.translatedData[index], codeSect.translateListComments[index]))
            f.write('[{} .. {}] : 0000000000000000; %EMPTY MEMORY LOCATIONS %\n'.format(index + 1, ADDR_RANGE - 1))
            f.write('END;\n')

    with open("../DCS/test16_MM.mif", "w") as f:
            f.write(MIF_FILE_HEADER)
            if not dataSect.dataDict:
                f.write('[{} .. {}] : 0000000000000000; %EMPTY MEMORY LOCATIONS %\n'.format(0, ADDR_RANGE - 1))
            else:
                i = 0
                usedDataSegs = []

                for addr in dataSect.dataDict:
                    usedDataSegs.append(int(dataSect.dataDict[addr], 16))

                # Loop through all possible addresses
                # if the current addr is not in usedDataSegs[]
                    notUsedStart = 0
                    notUsedEnd = 0
                for i in range(ADDR_RANGE - 1):

                    if i not in usedDataSegs:
                        notUsedEnd = notUsedEnd + 1
                        continue
                    else:

                        if notUsedEnd != notUsedStart:
                            f.write('[{} .. {}] : 0000000000000000; %EMPTY MEMORY LOCATIONS %\n'.format(notUsedStart, notUsedEnd - 1))
                        notUsedStart = i+1
                        notUsedEnd = i + 1
                        # index = usedDataSegs.find("i")
                        f.write("{}:{}; % {} %\n".format(str(i), "0000000000000000", "used"))
            f.write('END;\n')

    with open("test16.mif", "w") as f:
        f.write(MIF_FILE_HEADER)
        for index in range(len(codeSect.translatedData)):
            f.write("{}:{}; % {} %\n".format(index, codeSect.translatedData[index], codeSect.translateListComments[index]))
        f.write('[{} .. {}] : 0000000000000000; %EMPTY MEMORY LOCATIONS %\n'.format(index + 1, ADDR_RANGE - 1))
        f.write('END;\n')

    with open("test16_MM.mif", "w")as f:
            f.write(MIF_FILE_HEADER)
            if not dataSect.dataDict:
                f.write('[{} .. {}] : 0000000000000000; %EMPTY MEMORY LOCATIONS %\n'.format(0, ADDR_RANGE - 1))
            else:
                i = 0
                usedDataSegs = []

                for addr in dataSect.dataDict:
                    usedDataSegs.append(int(dataSect.dataDict[addr], 16))

                # Loop through all possible addresses
                # if the current addr is not in usedDataSegs[]
                    notUsedStart = 0
                    notUsedEnd = 0
                for i in range(ADDR_RANGE - 1):

                    if i not in usedDataSegs:
                        notUsedEnd = notUsedEnd + 1
                        continue
                    else:

                        if notUsedEnd != notUsedStart:
                            f.write('[{} .. {}] : 0000000000000000; %EMPTY MEMORY LOCATIONS %\n'.format(notUsedStart, notUsedEnd - 1))
                        notUsedStart = i+1
                        notUsedEnd = i + 1
                        # index = usedDataSegs.find("i")
                        f.write("{}:{}; % {} %\n".format(str(i), "0000000000000000", "used"))
            f.write('END;\n')

def calculateJumps(sectList):
    postJumpCalc = []
    sect = sectList
    # for sect in sectList:
    if (sect.sectName == 'code'):
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


def validAddr(token):
    token = list(token)
    if (token[0] != 'm'):
        return False
    if (token[1] != '['):
        return False
    for char in token[2:]:
        if char == ']':
            return True
        
def toBin(addr):

    hex_int = int(addr, 16)

    bin_string = bin(hex_int)
    bin_test = bin_string[2:].zfill(16)

    return bin_test

def translateSections(sectList):
    translateList = []
    numForLoops = 0
    numMemAccess = 0
    for sect in sectList:
        if (sect.sectName == 'code'):
            for line in range(len(sect.data)):
                # split line into tokens
                token = sect.data[line].split(" ")

                # Label support
                if (token[0][0] == '@'):

                    # Check if the label is already in the label dict
                    if (token[0][1:] not in sect.dataSectionLabels):
                        sect.dataSectionLabels[token[0][1:]] = line
                    else: print("Warning: Label already used in line {} used again on line {} -> {}".format(sect.dataSectionLabels[token[0][1:]], line, token[0][1:]))

                    # Check if reg reg instr is used
                    if (token[1] in regRegInstr):
                        if (token[2] not in reg):
                            print("Error: Invalid Syntax in line {} -> {}".format(sect.originalLineNum[line],token))
                            continue
                        if (token[3] not in reg):
                            print("Error: Invalid Syntax in line {} -> {}".format(sect.originalLineNum[line],token))
                            continue
                        sect.translatedData.append(regRegInstr[token[1]] + reg[token[2]] + reg[token[3]])
                        sect.translateListComments.append(token)
                        continue
                    
                    # Check if a reg imm instr is used
                    if (token[1] in regImmedInstr):
                        if(token[2] not in reg):
                            print("Error: Invalid Syntax in line {} -> {}".format(sect.originalLineNum[line],token))
                            continue
                        if(token[3][0] != "#"):
                            print("Error: Invalid Syntax in line {} -> {}".format(sect.originalLineNum[line],token))
                            continue
                        if(int(token[3][1:]) > 31):
                            print("Error: Invalid Syntax in line {} -> {}".format(sect.originalLineNum[line],token))
                            continue
                        sect.translatedData.append(regImmedInstr[token[1]] + reg[token[2]] + "{:05b}".format(int(token[2][1:]), 5))
                        sect.translateListComments.append(token)

                        continue

                    # handles jump instructions after a label
                    if (token[1] in jumpInstr):
                        if(token[2] not in reg):
                            print("Error: Invalid Syntax in line {} -> {}".format(sect.originalLineNum[line],token))
                            continue
                        if(token[3][0] != "@"):
                            print("Error: Invalid Syntax in line {} -> {}".format(sect.originalLineNum[line],token))
                            continue
                        sect.translatedData.append(jumpInstr[token[1]].replace("*", reg[token[2]]))
                        sect.translateListComments.append(token)
                        sect.translatedData.append(token[3])
                        sect.translateListComments.append(token[3])
                        continue
                    continue

                
                if (token[0] == 'for'):
                    if(token[3] >= str(32)):
                        print("Error: Iterator Amount too high {} -> {}".format(token[3], token))
                        continue
                    
                    # The + 1 is used to move the label jump address to be the first instruction in the for loop scope
                    sect.dataSectionLabels['for{}'.format(numForLoops)] = line + 1 + 3*numForLoops + numMemAccess
                    
                    sect.translatedData.append(regRegInstr['sub'] + reg['r19'] + reg['r19'])
                    sect.translateListComments.append('sub r19 r19'+ '@for{}'.format(numForLoops))
                    
                    continue

                
                if (token[0] == 'endfor'):
                    if(int(token[3]) >= 32):
                        print("Error: Iterator Check too high {} -> {}".format(token[3], token))
                        continue

                    sect.translatedData.append(regImmedInstr['addc'] + reg['r19'] + "00001")
                    sect.translateListComments.append('addc r19 #1')
                    
                    sect.translatedData.append(regImmedInstr['cmp'] + reg['r19'] + "{:05b}".format(int(token[3])))
                    sect.translateListComments.append('cmp r19 ' + token[3])
                    
                    sect.translatedData.append(jumpInstr['jz0'].replace("*", reg['r1']))
                    sect.translateListComments.append('jz0 r19' + '@for{}'.format(numForLoops))
                    
                    sect.translatedData.append('@for{}'.format(numForLoops))
                    sect.translateListComments.append('@for{}'.format(numForLoops))
                    numForLoops = numForLoops + 1
                    continue

                    # addc r1 #1
                    # cmp r1 #(#-1)
                    # jz0

                # handles instructions with the reg reg parameters

                if token[0] == "not":
                    if (token[1] not in reg):
                        print("Error: Invalid Syntax in line {} -> {}".format(sect.originalLineNum[line],token))
                        continue
                    sect.translatedData.append(regRegInstr[token[0]] + reg[token[1]] + "00000")
                    sect.translateListComments.append(token)
                    continue

                if (token[0] in regRegInstr):
                    if (token[1] not in reg):
                        print("Error: Invalid Syntax in line {} -> {}".format(sect.originalLineNum[line],token))
                        continue
                    if (token[2] not in reg):
                        print("Error: Invalid Syntax in line {} -> {}".format(sect.originalLineNum[line],token))
                        continue
                    sect.translatedData.append(regRegInstr[token[0]] + reg[token[1]] + reg[token[2]])
                    sect.translateListComments.append(token)
                    continue

                
                if (token[0] in memInstr):
                    if (token[1] not in reg):
                        print("Error: Invalid Syntax in line {} -> {}".format(sect.originalLineNum[line],token))
                        continue
                    if (token[2] not in reg):
                        print("Error: Invalid Syntax in line {} -> {}".format(sect.originalLineNum[line],token))
                        continue
                    
                    # if (validAddr(token[3])):
                    #     print("Error: Invalid Syntax in line {} -> {}".format(sect.originalLineNum[line],token))
                    #     continue

                    sect.translatedData.append(memInstr[token[0]] + reg[token[1]] + reg[token[2]])
                    sect.translateListComments.append(token)
                    
                    addr = ''
                    for char in token[3][2:]:
                        if char == ']':
                            break
                        addr = addr + char
                    
                    
                    if addr[0:2] != '0x' and (addr not in sectList[1].constDict) and (addr not in sectList[2].dataDict):
                        print("ERROR: Not a valid address")
                        continue
                    
                    if addr[0:2] == '0x':
                        sect.translatedData.append(toBin(addr))
                        sect.translateListComments.append(addr)
                        numMemAccess = numMemAccess + 1
                        continue
                    if addr in sectList[1].constDict:
                        sect.translatedData.append(toBin(sectList[1].constDict[addr]))
                        sect.translateListComments.append(addr)
                        numMemAccess = numMemAccess + 1
                        continue

                    if addr in sectList[2].dataDict:
                        sect.translatedData.append(toBin(sectList[2].dataDict[addr]))
                        sect.translateListComments.append(addr)
                        numMemAccess = numMemAccess + 1
                        continue
                        
                        



                    # sect.translatedData.append(getBinAddr())

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
                    sect.translatedData.append(regImmedInstr[token[0]] + reg[token[1]] + "{:05b}".format(int(token[2][1:]), 5))
                    sect.translateListComments.append(token)
                    continue

                # handles jump instructions
                if (token[0] in jumpInstr):
                    if(token[1] not in reg):
                        print("Error: Invalid Syntax in line {} -> {}".format(sect.originalLineNum[line],token))
                        continue
                    if(token[2][0] != "@"):
                        print("Error: Invalid Syntax in line {} -> {}".format(sect.originalLineNum[line],token))
                        continue
                    sect.translatedData.append(jumpInstr[token[0]].replace("*", reg[token[1]]))
                    sect.translateListComments.append(token)
                    sect.translatedData.append(token[2])
                    sect.translateListComments.append(token[2])
                    continue

                        

        translateList.append(sect)

    return translateList[0]


def getBinAddr(token):
    token = token.strip()

# gets rid of redundant lines and excludes comments from going onto translation
def parseSections(sectList):
    retList = []
    for sect in sectList:
        if (sect.sectName == 'code'):

            for line in range(len(sect.data)):
                if sect.data[line] == "":
                    continue
                else:
                    sect.originalLineNum.append(line + 2)
            # remove empty spaces
            while ("" in sect.data):
                sect.data.remove("")
        
        if (sect.sectName == 'const'):
            for line in range(len(sect.constData)):
                if sect.constData[line] == "":
                    continue
                else:
                    sect.originalLineNum.append(line + 2)
            # remove empty spaces
            while ("" in sect.constData):
                sect.constData.remove("")

            # parses and evaluates the .const section for substitution later
            for line in range(len(sect.constData)):
                token = sect.constData[line].split(" ")
                if token[0] == 'const':
                    if token[2] != '=':
                        print("ERROR: Invalid Syntax on line {} -> {}".format(sect.originalLineNum[line]), token)
                        continue

                    

                    if token[3][0:2] != '0x':
                        print("ERROR: Constants need to be hex values starting with '0x' -> {}".format(token))
                        continue
                    if token[1] not in sect.constDict:
                        sect.constDict[token[1]] = token[3][2:]


        if (sect.sectName == 'data'):
            for line in range(len(sect.data)):
                if sect.data[line] == "":
                    continue
                else:
                    sect.originalLineNum.append(line + 2)

            while ("" in sect.data):
                sect.data.remove("")


            for line in range(len(sect.data)):
                token = sect.data[line].split(" ")
                if token[0] != "let":
                    print("ERROR: Syntax error")
                    continue
                if token[1] not in sect.dataDict:
                    sect.dataDict[token[3]] = token[1]
                



        retList.append(sect)
    sectList[0].disp()
    return retList



def getSections(fileName):
    sectList = []
    with open(fileName, "r") as f:
        codeSection = Section('code')
        F = f.readlines()
        for line in range(len(F)):
            F[line] = F[line].strip("\n")
        
        # Get the info in each section
        for line in range(len(F)):
            if (F[line] == '.code'):
                codeSection.startIndex = line
            if (F[line] == '.endcode'):
                codeSection.endIndex = line
        
        codeSection.data = F[codeSection.startIndex + 1:codeSection.endIndex]

        for line in range(len(F)):
            if (F[line] == '.const'):
                startIndex = line
            if (F[line] == '.endconst'):
                endIndex = line

        sectConst = constSection('const')
        sectConst.constData = F[startIndex + 1: endIndex]


        for line in range(len(F)):
            if (F[line] == '.data'):
                startIndex = line
            if (F[line] == '.enddata'):
                endIndex = line

        
        dSect = dataSect('data')

        dSect.data = F[startIndex + 1: endIndex]
        
       
        sectList.append(codeSection)
        sectList.append(sectConst)
        sectList.append(dSect)

    return sectList
        


main()
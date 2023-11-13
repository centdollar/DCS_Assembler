import vfm6849_SymbolInfo

# IMPORTANT NOTE:
# You cannot have two consecutive ld/st or call/jmp (at least with load and store for sure) so add an operation between them, issue is MC3 still holds stall and then MC0 gets unstalled due to this

valid_start_symbols = vfm6849_SymbolInfo.valid_start_symbols
flow_control_symbols = vfm6849_SymbolInfo.flow_control_symbols

ASM_FILE = 'simd_labcode.asm'
# ASM_FILE = 'cache_asm.asm'

count = 0

# Open the files from command line below using like file pointers or look up best practice
lineNumber = 0
address = 0
instructionCount = 0
machineLanguageLine = 0
comment = []
dbg_errorlist = []
decodedFile = []
decodedComment = []
label = []
constants = {}
constantsKey = []

#holds the keys for the constant dictionary
constSecConstsKey = []

#dictionary that stores info like this {"constantName" : [Address, Data]}
constSecConsts = {}

DATA_DEPTH = 16384
MIF_FILE_HEADER = 'WIDTH = 14;\n' + 'DEPTH = 16384;\n' + 'ADDRESS_RADIX = DEC;\n' + 'DATA_RADIX = BIN;\n\n\n' + 'CONTENT BEGIN\n'

# Possible sections in the asm file
sections = ['.code', '.dir', '.constants']




def decode_int(symbol):
    return '{:04b}'.format(int(symbol))

def decode_hex(symbol):
    return '{:04b}'.format(int(symbol), 16)

def decode_memory_hex(symbol):
    return '{:014b}'.format(int(symbol, 16))


# Checks current symbol in line and decodes it
def decode_symbol(symbolIndex, symbol, decodedLine, currentLine, comment):
    global label
    # first index is the decoded values
    # second is the iw1 value   value of 'f' means no iw1
    # third is if jumping to a label 0: none found 1: found
    # fourth is the comment, which holds the original asm code
    # fifth element is if an error has occured
    decode_info = []
    iw1 = 0

    # Replaces symbols that are in the constant section here
    if symbol in constSecConstsKey:
        symbol = 'm[{}]'.format(constSecConsts[symbol])

    # Checks if label appears in the first symbol of the line
    # This would be a destination point and we store that for later use

    global count
    count = count + 1
    print(count)
    print(symbol[0])
    if (symbol[0] == '@') and (symbolIndex == 0):
        label.append([symbol[1:], currentLine])
        comment = comment + symbol + ' '
        decode_info = ['', 'f', 0, comment, 0]
        return decode_info

    # Check to see if the current symbol is a valid symbol (operation)
    if (symbol in valid_start_symbols):

        # adds the opcode or instruction to the decodedLine
        decodedLine = decodedLine + valid_start_symbols[symbol]
        comment = comment + symbol + ' '
        decode_info = [decodedLine, 'f', 0, comment, 0]
        return decode_info

    # Checks to see if the symbol is indexing a register
    if symbol[0] == 'r':

        # Throw error if register index is over 15
        if int(symbol[1:]) > 15:
            decode_info = ['', 'f', 0, comment, 1 ]
            return decode_info
        else:
            if(decodedLine[0:6] == "000100"):
                decodedLine = decodedLine.replace('*', (decode_int(symbol[1:])))
                comment = comment + symbol + ' '
                # print('here' + decodedLine)
                decode_info = [decodedLine, 'f', 0, comment, 0]
            # decode reg index and add it to the line
            elif (decodedLine[0:6] == "011011"):
                decodedLine = decodedLine.replace('*', (decode_int(symbol[1:])))
                comment = comment + symbol + ' '
                # print('here' + decodedLine)
                decode_info = [decodedLine, 'f', 0, comment, 0]
            else:
                decodedLine = decodedLine + decode_int(symbol[1:])
                comment = comment + symbol + ' '
                decode_info = [decodedLine, 'f', 0, comment, 0]
            
        return decode_info

    if symbol[0] == '#':
        if int(symbol[1:]) > 15:
            decode_info = ['', 'f', 0, comment, 1 ]
            return decode_info
        else:
            decodedLine = decodedLine + decode_int(symbol[1:])
            comment = comment + symbol + ' '
            decode_info = [decodedLine, 'f', 0, comment, 0]
            return decode_info

    # print(symbol[0:1])
    if symbol[0:2] == 'm[':
        newSymbol = symbol[2:]
        if (symbol[2:-1] in constSecConstsKey):
            iw1 = decode_memory_hex(constSecConsts[symbol[2:-1]][0]).zfill(14)
            comment = comment + symbol + ' '
            decode_info = [decodedLine, iw1, 1, comment, 0]
        elif (newSymbol in constantsKey):
            iw1 = decode_memory_hex(constants[newSymbol]).zfill(14)
            comment = comment + symbol + '] '
            decode_info = [decodedLine, iw1, 1, comment, 0]
        else:
            # decode memory location for the load and store and then add it to iw1
            # print('symbol:' + symbol)
            iw1 = decode_memory_hex(symbol[2:-1]).zfill(14)
            comment = comment + symbol + ' '
            decode_info = [decodedLine, iw1, 1, comment, 0]
            # print(decode_info)
        return decode_info

    if (symbol[0] == '@') and (symbolIndex != 0):
        # print(decode_info)
        comment = comment + symbol + ' '
        decode_info = [decodedLine, '!' + symbol[1:], 1, comment, 0]
        return decode_info
    
    if symbol in constantsKey:

        comment = comment + symbol + ' '
        decodedLine = decodedLine + decode_hex(constants[symbol])
        decode_info = [decodedLine, 'f', 0, comment, 0]
        return decode_info
    
    if (symbol not in valid_start_symbols):
        comment = comment + symbol + ' '
        decode_info = [decodedLine, 'f', 0, comment, 1]
        return decode_info




# Function Definitions
def syntax_check_x_decode(asmFile):
    global labelLocations
    global instructionCount
    # print(asmFile)
    global machineLanguageLine
    machineLanguageLine = 0
    currentSection = ''
    for assemblyLine in range(len(asmFile)):
        # print("assembly line:" + asmFile[assemblyLine])
        decoded_symbol = ['', 'f', 0, '', 0]
        asmFile[assemblyLine] = asmFile[assemblyLine][0:-1]
        splitLine = asmFile[assemblyLine].split(' ')
        machineLanguageLine = machineLanguageLine + 1
        #check line for incorrect expected characters
        if splitLine[0] == '':
            continue
        curr_decodedLine = ''

        if splitLine[0] == '//':
            continue

        if currentSection == '':
            if splitLine[0] == '.code':
                currentSection = '.code'
                continue
            elif splitLine[0] == '.dir':
                currentSection = '.dir'
                continue
            elif splitLine[0] == '.constants':
                currentSection = '.constants'
                continue
        
        if currentSection in sections:
            if splitLine[0] == '.endcode':
                currentSection = ''
                continue
            elif splitLine[0] == '.enddir':
                currentSection = ''
                continue
            elif splitLine[0] == '.endconstants':
                currentSection = ''
                continue

        if (currentSection == '.dir'):
            if splitLine[0] == '.equ':
                constantsKey.append(splitLine[1])
                constants.update({splitLine[1]: splitLine[2]})
                    

        if (currentSection == '.constants'):
            if splitLine[0] == '.word':
                constSecConstsKey.append(splitLine[1])
                constSecAddressDataPair = [splitLine[2], splitLine[3]]
                constSecConsts.update({splitLine[1]: constSecAddressDataPair})


        if (currentSection == '.code'):
            for symbol in range(len(splitLine)):

                if splitLine[symbol] in sections:
                    continue
                if splitLine == '':
                    continue
                
                # Get the list of attributes from the current symbol
                decoded_symbol = decode_symbol(symbol, splitLine[symbol], decoded_symbol[0], instructionCount, decoded_symbol[3]) 
                if(decoded_symbol[4] == 1):
                    print("ERROR: Line {} with decodeded symbol: {}".format((assemblyLine + 1), decoded_symbol))


            # Check if there is a second instruciton word
            curr_decodedLine = decoded_symbol[0]
            curr_comment = decoded_symbol[3]
            decodedFile.append(curr_decodedLine)
            decodedComment.append(curr_comment)
            instructionCount = instructionCount + 1
            if decoded_symbol[2] == 1: 
                iw1 = decoded_symbol[1]
                decodedFile.append(iw1)
                decodedComment.append('jumpOffset')
                instructionCount = instructionCount + 1
            
            # print("curr_line:" + curr_decodedLine + '\n')
        
            # print(decoded_symbol[2])
    # print(decodedComment)
    # print('IC:' + str(instructionCount))
    return dbg_errorlist

	

# first symbol options
# instruction, label, comment

def writeout(File, decodedFile):
    with open(File, 'w') as f:
        for line in range(len(decodedFile)):
            # print(line)
            f.write(str(line) + ':' + decodedFile[line] + ';' + '\n')
            # f.write(str(line) + ':' + decodedFile[line] + ';' + '%' + decodedComment[line] + '%' +'\n')

def writeoutOffsets(File, decodedFile):
    with open(File, 'w') as f:
        f.write(MIF_FILE_HEADER)
        for line in range(len(decodedFile)):
            # print(line)
            # f.write(str(line) + ':' + decodedFile[line] + ';' + '\n')
            f.write(decodedFile[line][0:-1]  + '  %  ' + decodedComment[line] + '  %' +'\n')
        f.write('[{} .. {}] : 11111111111111; %EMPTY MEMORY LOCATIONS %\n'.format(len(decodedFile), DATA_DEPTH - len(constSecConsts) - 1))
        for i in range(len(constSecConstsKey)):
            y = len(constSecConstsKey) - i
            curr_constant = constSecConsts[constSecConstsKey[i]][0]
            curr_constant_data = constSecConsts[constSecConstsKey[i]][1]
            f.write(str(int(curr_constant, 16)) + ':' + str(curr_constant_data) + '; %' + str(constSecConstsKey[i]) +'%' + '\n')


        f.write('END;\n')

def twosComp(val, bits):
    val = val - (1 << bits)
    return val

def calculateOffset(currentLine, labelIndex):
    if currentLine > label[labelIndex][1]:
        return   '{:014b}'.format(twosComp(currentLine - label[labelIndex][1] + 1, 14))
    else: return '{:014b}'.format(label[labelIndex][1] - currentLine - 1, 14)


def calculateJumps(file):
    with open(file, 'r') as mifFile:
        mifFileList = mifFile.readlines()

        for line in range(len(mifFileList)):
            currentLine = mifFileList[line].split(":")
            # print(currentLine)
            if(currentLine[1][0] == '!'):
                labelNameEnd = currentLine[1].find(';')
                # print(labelNameEnd)
                for labelIndex in range(len(label)):
                    if currentLine[1][1:labelNameEnd] == label[labelIndex][0]:
                        # print("LabelFound")
                        # print(line)
                        currentLine[1].replace(currentLine[1][1:labelNameEnd], calculateOffset(int(currentLine[0]), labelIndex))
                        currentLine = str(line) + ':' + str(calculateOffset(int(currentLine[0]), labelIndex)) + ';' + '\n'
                        currentLine = currentLine.replace('-','')

                        mifFileList[line] = currentLine
    return mifFileList


# Name of the mif file to write to, no need to add the .mif
mifFileName = input()


# 
with open(ASM_FILE, 'r') as asm_file:
    error = syntax_check_x_decode(asm_file.readlines(), )

# print(error)


# writeout to machine file
writeout('decode.mif', decodedFile)


final_decode = calculateJumps('decode.mif')

# print(final_decode)

writeoutOffsets(mifFileName + '.mif', final_decode)

# print(label)
# print(final_decode)
#generate_decode()


# insert_jumpaddresses()





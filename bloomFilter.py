#
##
## Bloom Filter - Python Software
## Elias W. Harvik-Wright // 583619
##
#

## Imports
import pathlib  
from math import prod
import time

## Global Variables
inputList = [] # List to store password imported from given file
Prime = pow(2,24)-3 # prime
valuesList = []  # List to store ASCII Values per password
bloomLen = pow(2,24) # Defines the length of the Bloom Filter
bloom = [0] * bloomLen # Creates the actual Bloom Filter, list of 0's times the length. 


## Fetch Passwords from file (on the same level as Script) ##
# Switch file name with path to file to test against.
with open('TrainingBF.txt') as f:
    inputList = f.read().splitlines()

## Function to feed each end-value after hashing into the bloom-filter
def feedToBloom(pwValue:int):
    bloom[pwValue] = 1

## Function to Convert the bits in bit-array(bloom filter) to actual characters.
# Calculates the difference between the given values in assignment-table to ASCII character values. 
def converter(bloom: list):
    bitString = "00"
    listOfChar = ""
    for x in bloom:
        bitString = bitString + str(x)
        if len(bitString) == 6:
            bit = int(bitString, base=2)
            if bit <= 25: # A --> Z
                bit += 65 
            elif bit <= 51: # a --> z
                bit += 71
            elif bit <= 61: # 0 --> 9
                bit -= 4
            elif bit == 62: # +
                bit = 43
            elif bit == 63: # /
                bit = 47
            listOfChar += (chr(bit))
            bitString = ""
    return listOfChar

## Function to write given final output to a file.
def writeToFile(string :str):
    BFFile = open('BF_583619.txt', "w")
    BFFile.write(string)
    BFFile.close()

## Feed X into Function to get ASCII Value from input.
def valuesToList(pw: str) -> int:
    listed = []
    for x in pw:
        value = ord(x)
        #print(x, value) # DEBUGGING
        listed.append(value)
    return listed

## Define all hashes according to slides.
def hashOne(valList) -> int: ## h1() - TIMES
    result = 1
    for x in valList:
        result = result * x
        result = result % Prime
    return result   
def hashTwo(valuesList) -> int: ## h2() - SUM
    result = 0
    for x in valuesList:
        result = result + x
        result = result % Prime
    return result
def hashThree(listValues) -> int: ## h3() - GROUPED SUMS OF THREE
    valuesList = listValues.copy()
    subRes = []
    result = 1
    i = 0
    N = 3
    length = len(valuesList)
    while(length % N) != 0:
        valuesList.insert(len(valuesList), 32)
        length += 1
    if(length % N) == 0:
        subList = [valuesList[n:n+N] for n in range(0, len(valuesList), N)]
        for x in subList:
            subRes.append(sum(subList[i]))
            i+=1
        for x in subRes:
            result = result * x
            result = result % Prime
        return result
def hashFour(listValues) -> int: ## h4() - GROUPED SUMS OF FIVE
    valuesList = listValues.copy()
    subRes = []
    result = 1
    i = 0
    N = 5
    length = len(valuesList)
    while(length % N) != 0:
        valuesList.insert(len(valuesList), 32)
        length += 1
    if(length % N) == 0:
        subList = [valuesList[n:n+N] for n in range(0, len(valuesList), N)]
        for x in subList:
            subRes.append(sum(subList[i]))
            i+=1
        for x in subRes:
            result = result * x
            result = result % Prime
        return result
def hashFive(listValues) -> int: ## h5() - GROUPED SUMS OF THREE, but addition and multiplication swapped
    valuesList = listValues.copy()
    subRes = []
    result = 0
    N = 3
    v = 1
    length = len(valuesList)
    while(length % N) != 0:
        valuesList.insert(len(valuesList), 32)
        length += 1
    if(length % N) == 0:
        subList = [valuesList[n:n+N] for n in range(0, len(valuesList), N)]
        for x in subList:
            for y in x:
                v *= y
            subRes.append(v)
            v = 1
        #print(subRes)
        for x in subRes:
            result += x
            result = result % Prime
        return result
def hashSix(listValues) -> int: ## h6() - GROUPED SUMS OF FIVE, but addition and multiplication swapped
    valuesList = listValues.copy()
    subRes = []
    result = 0
    i = 0
    N = 5
    length = len(valuesList)
    while(length % N) != 0:
        valuesList.insert(len(valuesList), 32)
        length += 1
    if(length % N) == 0:
        subList = [valuesList[n:n+N] for n in range(0, len(valuesList), N)]
        for x in subList:
            subRes.append(prod(subList[i]))
            i+=1
        for x in subRes:
            result = result + x
            result = result % Prime
        return result
def hashSeven(valuesList) -> int: ## h7() - product of O and E modulo the prime p = 2^24 - 3
    # O = sum of the odd indexed ascii values
    # E = sum of the even indexed ascii values
    O = []
    Ox = 0
    E = []
    Ex = 0
    result = 0
    for index, s in enumerate(valuesList):
        if (index % 2) == 0:
            O.append(s)
        else:
            E.append(s)
    Ox = sum(O)
    Ex = sum(E)
    result = Ox * Ex 
    result = result % Prime
    return result
def hashEight(valuesList) -> int: ## h8() - 
    q = 31
    i = 1
    list = []
    result = 0
    y = 0
    for x in valuesList:
        y = pow(q, i-1) #Prime = pow(2,24)-3 # prime
        result = x * y 
        i+=1
        list.append(result)
    result = sum(list)
    result = result % Prime
    return result
## Function to controll the flow, iterate through hashes together with the other functions.
def hashes():
    for pw in inputList:
        var = valuesToList(pw)
    ## HASH - h1
        variable = hashOne(var)
        #print(pw,':', variable)
        feedToBloom(variable)
        #print(bloom[variable])   
    ## HASH - h2
        variable = hashTwo(var)
        #print(pw,':', variable)
        feedToBloom(variable)
        #print(bloom[variable])   
    ## HASH - h3
        variable = hashThree(var)
        #print(pw,':', variable)
        feedToBloom(variable)
        #print(bloom[variable])   
    ## HASH - h4
        variable = hashFour(var)
        #print(pw,':', variable)
        feedToBloom(variable)
        #print(bloom[variable])   
    ## HASH - h5
        variable = hashFive(var)
        #print(pw,':', variable)
        feedToBloom(variable)
        #print(bloom[variable])   
    ## HASH - h6
        variable = hashSix(var)
        #print(pw,':', variable)
        feedToBloom(variable)
        #print(bloom[variable])   
    ## HASH - h7
        variable = hashSeven(var)
        #print(pw,':', variable)
        feedToBloom(variable)
        #print(bloom[variable])   
    ## HASH - h8
        variable = hashEight(var)
        #print(pw,':', variable)
        feedToBloom(variable)
        #print(bloom[variable])   

## Function to check given password up against bloom filter. Accept if its not found in the bloom filter already. Visa versa reject if found.
def checkBloom(pw) -> str:
    var = valuesToList(pw)
    if bloom[hashOne(var)] == 0:
        print("Password Accepted:", pw)
    elif bloom[hashTwo(var)] == 0:
        print("Password Accepted:", pw)
    elif bloom[hashThree(var)] == 0:
        print("Password Accepted:", pw)
    elif bloom[hashFour(var)] == 0:
        print("Password Accepted:", pw)
    elif bloom[hashFive(var)] == 0:
        print("Password Accepted:", pw)
    elif bloom[hashSix(var)] == 0:
        print("Password Accepted:", pw)
    elif bloom[hashSeven(var)] == 0:
        print("Password Accepted:", pw)
    elif bloom[hashEight(var)] == 0:
        print("Password Accepted:", pw)
    else:
        print("Password Rejected:", pw)

## Main Function to call the rest of the functions. 
def master():
    tick = time.time()
    print("Timer started!")
    print("Drinking coffee whilst checking hashes:")
    hashes()
    print("Doing Bloom stuff...")
    writeToFile(converter(bloom))
    checkBloom("Password!") # Input of whatever is being tested against the Bloom Filter
    print("~~~ It took", time.time()-tick, "seconds to run ~~~")
master()
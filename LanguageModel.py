import sys
import math

# read the data from the file and store into a list
def loadData(inFile, datalist):
    NLine = 0.0
    with open(inFile) as inFile:
        for line in inFile:
            NLine += 1
            tempLine = ' <s> ' + line.lower() + ' </s> '
            datalist.append(tempLine.split())
    return NLine


# count the number of word pattern and store into a dictionary(w,c) for later processing
def Count(datalist, dictionary, signal):
    typeofwords = 0.0
    if signal == 'unigram':
        for i in range(len(datalist)):
            for j in range(len(datalist[i])):
                key = datalist[i][j]
                if key in dictionary:
                    dictionary[key] += 1
                else:
                    dictionary[key] = 1
                    typeofwords += 1
    elif signal == 'bigram':
        for i in range(len(datalist)):
            for j in range(1, len(datalist[i])):
                key = datalist[i][j] + '|' + datalist[i][j - 1]
                if key in dictionary:
                    dictionary[key] += 1
                else:
                    dictionary[key] = 1
                    typeofwords += 1
    return typeofwords

# replace every word in the test data not seen in training with the token <unk>.
# pass keys and values of old dictionary(before replacement) to a new dictionary(after replacement)
def replaceTestToken(trainDic, testDic, testDicCopy, testlist):
    typeofunk = 0.0
    numofunk = 0.0
    for key in testDic:
        if key not in trainDic:
            typeofunk += 1
            testDic[typeofunk] = testDic.pop(key)
    for key in testDic:
        if isinstance(key, float):
            numofunk += testDic.get(key)
        else:
            testDicCopy[key] = testDic.get(key)
    testDicCopy['<unk>'] = numofunk
    for i in range(len(testlist)):
        for j in range(len(testlist[i])):
            if testlist[i][j] not in testDicCopy:
                testlist[i][j] = '<unk>'
    return typeofunk


# replace all words occurring in the training data once with the token <unk>
def replaceTrainToken(dictionary, datalist):
    for i in range(len(datalist)):
        for j in range(len(datalist[i])):
            if dictionary.get(datalist[i][j]) == 1:
                datalist[i][j] = '<unk>'


# compute the probability and log probability of words under unigram maximum childhood model
def unigram(dictionary, nUnigram, pdictionary):
    print('Unigram maximum childhood model:')
    for key in dictionary:
        if not (key == '</s>' or key == '<s>'):
            p = dictionary.get(key) / nUnigram
            pdictionary[key] = math.log10(p)
            print('p' + '(' + key + ')' + ' = ', p)
    print('\n')


# compute the probability and log probability of words under bigram maximum childhood model
def bigram(dictionary1, dictionary2, dictionary3):
    print('Bigram maximum childhood model:')
    for key in dictionary1:
        tempKey = key.split('|')
        p = dictionary1.get(key) / dictionary2.get(tempKey[1])
        print('p' + '(' + key + ')' + ' = ', p)
        dictionary3[key] = math.log10(p)
    print('\n')


# compute the probability and log probability of words under bigram model with Add-one Smoothing
def addOne(dictionary1, dictionary2, dictionary3, typeofwords):
    print('Bigram model with Add-one Smoothing:')
    for key in dictionary1:
        tempKey = key.split('|')
        p = (dictionary1.get(key)+1) / (dictionary2.get(tempKey[1])+typeofwords)
        print('p' + '(' + key + ')' + ' = ', p)
        dictionary3[key] = math.log10(p)
    print('\n')


# check whether a key of a dictionary in another dictionary or not
def bigramCheck(dictionary1, dictionary2, dictionary1copy):
    typeofBunk = 0.0
    numofBunk = 0.0
    for key in dictionary2:
        if key not in dictionary1:
            typeofBunk += 1
            numofBunk += dictionary2.get(key)
        else:
            dictionary1copy[key] = dictionary2.get(key)

    dictionary1copy['<unk>'] = numofBunk
    return typeofBunk


# compute the number of tokens
def totalTokens(dictionary):
    return sum(dictionary.values())


# compute types of words
def typeofword(dictionary):
    typeofwords = 0.0
    for key in dictionary:
        typeofwords += 1
    return typeofwords


# store word patterns of a string in a dictionary
def stringD(sentence, signal):
    stringDic = {}
    if signal == 'unigram':
        for token in sentence.lower().split():
            if token in stringDic:
                stringDic[token] += 1
            else:
                stringDic[token] = 1
    elif signal == 'bigram':
        sentence = ' <s> ' + sentence + ' </s>'
        temp = sentence.lower().split()
        for i in range(1, len(temp)):
            key = temp[i] + '|' + temp[i-1]
            if key in stringDic:
                stringDic[key] += 1
            else:
                stringDic[key] = 1
    return stringDic


# compute log probability
def plog(dictionary1, dictionary2, M):
    summation = 0.0
    for key in dictionary1:
        if dictionary2.get(key) is None:
            summation += dictionary2.get('<unk>')
        else:
            summation += dictionary2.get(key)
    return 1/M*summation


# compute perplexity
def perplexity(l):
    return math.pow(2,-l)


# display the result of file after pre-processing
def printFile(datalist):
    print('Corpus after pre-processing:')
    for sentence in datalist:
        print(' '.join(str(word) for word in sentence))
    print('\n')



trainList = []
testList1 = []
testList2 = []

# create a dictionary to store the num of every unique word
trainUDic = {}
testUDic1 = {}
testUDic2 = {}

# unigram dictionary after replacement
testUDic11 = {}
testUDic22 = {}

# create a dictionary to store the num of two consecutive words
trainBDic = {}
testBDic1 = {}
testBDic2 = {}

unigramPDic = {} # create a dictionary to store log P under unigram model
bigramPDic = {} # create a dictionary to store log P under bigram model
bigramPADic = {} # create a dictionary to store log P under bogram model with add-one smoothing

# bigram dictionary after replacement
testBDic11 = {}
testBDic22 = {}

trainLine = loadData('brown-train.txt', trainList)
Count(trainList, trainUDic, 'unigram')
test1Line = loadData('brown-test.txt', testList1)
test2Line = loadData('learner-test.txt', testList2)
typeofUword1 = Count(testList1, testUDic1, 'unigram')
typeofUword2 = Count(testList2, testUDic2, 'unigram')
typeofunk1 = replaceTestToken(trainUDic, testUDic1, testUDic11, testList1)
typeofunk2 = replaceTestToken(trainUDic, testUDic2, testUDic22, testList2)


#Question3
# probability of unk types
#typeofunk1/typeofUword1
#typeofunk2/typeofUword2
# probability of unk tokens, total token does not include start symbol
pNumofunkTokenU1 = testUDic11.get('<unk>')/(totalTokens(testUDic11)-test1Line)
pNumofunkTokenU2 = testUDic22.get('<unk>')/(totalTokens(testUDic22)-test2Line)

replaceTrainToken(trainUDic, trainList)
trainUDic.clear()

# trainUDic store every unique word and its count after replacement
#Question1&2
typeofTrainUwords = Count(trainList, trainUDic, 'unigram')
totalUtokens = totalTokens(trainUDic)-trainLine

# unigram model
numUnigram = totalTokens(trainUDic)-2*trainLine
unigram(trainUDic, numUnigram, unigramPDic)

#bigram model
typeofTrainBwords = Count(trainList, trainBDic, 'bigram')
bigram(trainBDic, trainUDic, bigramPDic)

#bigram model with add-one smoothing
addOne(trainBDic, trainUDic, bigramPADic, typeofTrainBwords)

#Question4
typeofTestBwords1 = Count(testList1, testBDic1, 'bigram')
typeofTestBunk1 = bigramCheck(trainBDic, testBDic1, testBDic11)
pNumofunkTokenB1 = testBDic11.get('<unk>') / totalTokens(testBDic11)

typeofTestBwords2 = Count(testList2, testBDic2, 'bigram')
typeofTestBunk2 = bigramCheck(trainBDic, testBDic2, testBDic22)
pNumofunkTokenB2 = testBDic22.get('<unk>') / totalTokens(testBDic22)

bigramPDic['<unk>'] = trainUDic.get('<unk>')
bigramPADic ['<unk>'] = trainUDic.get('<unk>')

#Question5&6
a = 'He was laughed off the screen .'
b = 'There was no compulsion behind them .'
c = 'I look forward to hearing your reply .'

aUDic = stringD(a, 'unigram')
laU = plog(aUDic, unigramPDic, 7)
bUDic = stringD(b, 'unigram')
lbU = plog(bUDic, unigramPDic, 7)
cUDic = stringD(c, 'unigram')
lcU = plog(cUDic, unigramPDic, 8)

aBDic = stringD(a, 'bigram')
laB = plog(aBDic, bigramPDic, 8)
bBDic = stringD(b, 'bigram')
lbB = plog(bBDic, bigramPDic, 8)
cBDic = stringD(c, 'bigram')
lcB = plog(cBDic, bigramPDic, 9)

aBADic = stringD(a, 'bigram')
laBA = plog(aBADic, bigramPDic, 8)
bBADic = stringD(b, 'bigram')
lbBA = plog(bBADic, bigramPDic, 8)
cBADic = stringD(c, 'bigram')
lcBA = plog(cBADic, bigramPDic, 9)


print('1. How many word types (unique words) are there in the training corpus? Please include '
      'the padding symbols and the unknown token.')
print('   ', typeofTrainUwords, '\n')
print('2. How many word tokens are there in the training corpus?(not including start symbol)')
print('   ', totalUtokens, '\n')
print('3. What percentage of word tokens and word types in each of the test corpora did not '
      'occur in training (before you mapped the unknown words to <unk> in training and test data)?')
print('   word tokens:')
print('   brown-test:', pNumofunkTokenU1, '   learner-test:', pNumofunkTokenU2)
print('   word types:')
print('   brown-test:', typeofunk1/typeofUword1, '   learner-test:', typeofunk2/typeofUword2, '\n')

print('4. What percentage of bigrams (bigram types and bigram tokens) in each of the test corpora '
      'that did not occur in training (treat <unk> as a token that has been observed).')
print('   word tokens:')
print('   brown-test:', pNumofunkTokenB1,'   learner-test:', pNumofunkTokenB2)
print('   word types:')
print('   brown-test:', typeofTestBunk1/typeofTestBwords1,'   learner-test:', typeofTestBunk2/typeofTestBwords2, '\n')

print('5. Compute the log probabilities of the following sentences under the three models (ignore '
      'capitalization and pad each sentence as described above). Please list all of the '
      'parameters required to compute the probabilities and show the complete calculation. '
      'Which of the parameters have zero values under each model?)')

print('   unigram maximum likelihood model')
print(a)
print('   log probability=', laU)
print(b)
print('   log probability=', lbU)
print(c)
print('   log probability=', lcU, '\n')

print('   Bigram maximum likelihood model')
print(a)
print('   log probability=', laB)
print(b)
print('   log probability=', lbB)
print(c)
print('   log probability=', lcB, '\n')

print('   Bigram model with Add-One smoothing')
print(a)
print('   log probability=', laBA)
print(b)
print('   log probability=', lbBA)
print(c)
print('   log probability=', lcBA, '\n')

print('6. Compute the perplexities of each of the sentences above under each of the models.')

print('   unigram maximum likelihood model')
print(a)
print('   perplexity=', perplexity(laU))
print(b)
print('   perplexity=', perplexity(lbU))
print(c)
print('   perplexity=', perplexity(lcU), '\n')

print('   Bigram maximum likelihood model')
print(a)
print('   perplexity=', perplexity(laB))
print(b)
print('   perplexity=', perplexity(lbB))
print(c)
print('   perplexity=', perplexity(lcB) ,'\n')

print('   Bigram model with Add-One smoothing')
print(a)
print('   perplexity=', perplexity(laBA))
print(b)
print('   perplexity=', perplexity(lbBA))
print(c)
print('   perplexity=', perplexity(lcBA), '\n')

print('7. Compute the perplexities of the entire test corpora, separately for the brown-test.txt and '
      'learner-test.txt under each of the models. Discuss the differences in the results you obtained.')

print('   Perplexity under unigram maximum likelihood model')
print('   brown-test', perplexity(plog(testUDic11, unigramPDic, totalTokens(testUDic11)-test1Line)))
print('   learner-test', perplexity(plog(testUDic22, unigramPDic, totalTokens(testUDic22)-test2Line)), '\n')

print('   Perplexity under bigram maximum likelihood model')
print('   brown-test', perplexity(plog(testBDic11, bigramPDic, totalTokens(testBDic11))))
print('   learner-test', perplexity(plog(testBDic22, bigramPDic, totalTokens(testBDic22))), '\n')

print('   Perplexity under bigram model with Add-One smoothing')
print('   brown-test', perplexity(plog(testBDic11, bigramPADic, totalTokens(testBDic11))))
print('   learner-test', perplexity(plog(testBDic22, bigramPADic, totalTokens(testBDic22))), '\n')
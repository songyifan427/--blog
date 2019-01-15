import numpy as np
import jieba

class isgentry():
    def __init__(self,testWords):
        self.testWords=testWords
    def loadData(self):
        wordList=[
                    ['你','傻逼'],
                    ['我','朋友','她','很','厉害'],
                    ['你','看起来','非常','聪明','我','喜欢','你'],
                    ['她','很','恶心'],
                    ['弱智'],['愚蠢'],['狗'],['神经病'],['笨蛋'],['脑残'],['垃圾'],['丑'],['讨厌'],
                    ['美丽'],['睿智'],['好'],['赞'],['博学'],['漂亮'],['实用'],['爱']
                    ]          
        classList=[1,0,0,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0]
        return wordList,classList

    def creatVocabList(self,wordList):
        vocabSet=set([])
        for document in wordList:
            vocabSet=vocabSet|set(document)
        vocabList=list(vocabSet)
        return vocabList

    def setOfWords2Vec(self,vocabList,words):
        wordVec=[0]*len(vocabList)
        for word in words:
            if word in vocabList:
                wordVec[vocabList.index(word)]=1        
        return wordVec

    def bagOfWords2Vec(self,vocabList,words):
        wordVec=[0]*len(vocabList)
        for word in words:
            if word in vocabList:
                wordVec[vocabList.index(word)]+=1 
            else:
                pass             
        return wordVec

    def trainNB(self,vocabList,trainMat,classList):
        numWords=len(vocabList)
        pSpam=(sum(classList)+1)/(len(classList)+2)
        p1Num=np.ones(numWords)
        p0Num=np.ones(numWords)
        p1Denom=0
        p0Denom=0
        for i in range(len(classList)):
            if classList[i]==1:
                p1Num+=trainMat[i]
                p1Denom+=sum(trainMat[i])
            else:
                p0Num+=trainMat[i]
                p0Denom+=sum(trainMat[i])
        p1Denom+=numWords
        p0Denom+=numWords
        p1Vec=np.log(p1Num/p1Denom)     
        p0Vec=np.log(p0Num/p0Denom)
        return p1Vec,p0Vec,pSpam

    def classifyNB(self,vocabList,trainMat,newWordVec,classList):
        p1Vec,p0Vec,pSpam=self.trainNB(vocabList,trainMat,classList)
        p1=sum(newWordVec*p1Vec)+np.log(pSpam)
        print(p1)
        p0=sum(newWordVec*p0Vec)+np.log(1-pSpam)
        print(p0)
        return True if p1>p0 else False

    def runTest(self):
        wordList,classList=self.loadData()
        vocabList=self.creatVocabList(wordList)
        trainMat=[]
        for words in wordList:
            trainMat.append(self.setOfWords2Vec(vocabList,words))
        
        testWords=jieba.cut(self.testWords)
        newWordVec=self.setOfWords2Vec(vocabList,testWords)
        result=self.classifyNB(vocabList,trainMat,newWordVec,classList)  
        return True if result else False
            

# testWords='你真丑，我讨厌你'
# result=isgentry(testWords).runTest()
# 返回布尔值，真为粗鲁语言             
 





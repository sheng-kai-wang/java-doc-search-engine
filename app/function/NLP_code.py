# import yaml
import json
import jsonpath
import math
import numpy as np
import pandas as pd
from collections import defaultdict
import statistics
from itertools import product

# 安裝 WordNet
import nltk
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('omw-1.4')
from nltk.corpus import wordnet as wn

data = open("JAVA_DOC.json", "r", encoding='UTF-8').read()
data = json.loads(data)

seeAlsoData = open("see_also.json", "r", encoding='UTF-8').read()
seeAlsoData = json.loads(seeAlsoData)

lemmatizer = nltk.stem.WordNetLemmatizer()
stop_words = set(nltk.corpus.stopwords.words('english'))

'''----------生產權重文件----------'''
'''
classNameList = []
#nltkDescribeList = []
nullClassNameList = []
index = []

#javaDocNltkDict = {}
nullJavaDocDict = {}
javaDocDFTF = {}

for className in data:
    if type(data[className]['Describe']) != list:
        classNameList.append(className) 
        
        word_set = nltk.word_tokenize(data[className]['Describe'].lower())        
        # remove stop words
        word_set = [w for w in word_set if w not in stop_words]
        # lemmatization
        word_set = [lemmatizer.lemmatize(w) for w in word_set]
        
        #nltkDescribeList.append(word_set)
        #javaDocNltkDict.setdefault(className, word_set)
        
        for word in word_set:
            if word not in javaDocDFTF:
                javaDocDFTF.setdefault(word, {'df':1, 'inv_list':[]})
                javaDocDFTF[word]['inv_list'].append({'className':className, 'tf':1})
                index.append(word)
            
            else:
                if className == javaDocDFTF[word.lower()]['inv_list'][-1]['className']:
                    javaDocDFTF[word]['inv_list'][-1]['tf'] += 1
                    
                else:
                    javaDocDFTF[word]['df'] += 1
                    javaDocDFTF[word]['inv_list'].append({'className':className, 'tf':1})
        
    else:
        nullClassNameList.append(className)
        nullJavaDocDict.setdefault(className, data[className])
        
value = np.zeros((len(javaDocDFTF), len(classNameList)), dtype=float)
javaDocWeights = pd.DataFrame(value, index=index, columns=classNameList)

for word in javaDocDFTF:
    for invList in javaDocDFTF[word]['inv_list']:
        javaDocWeights[invList['className']][word] = (1 + math.log(invList['tf'], 10)) * math.log(len(classNameList) / javaDocDFTF[word]['df'], 10)
'''
'''----------生產 class 相似度文件----------'''
'''
value = np.zeros((len(classNameList), len(classNameList)), dtype=float)
javaDocSimilarity = pd.DataFrame(value, index=classNameList, columns=classNameList)

for num, i in enumerate(javaDocWeights):
    print('現在進度： ' + str(num))
    lit = []
    norm_a = (javaDocWeights[i] * javaDocWeights[i]).sum() ** 0.5
    
    for j in javaDocWeights:
        if i != j:
            dot = (javaDocWeights[i] * javaDocWeights[j]).sum()            
            norm_b = (javaDocWeights[j] * javaDocWeights[j]).sum() ** 0.5
            similarity = dot / (norm_a*norm_b)
            javaDocSimilarity[i][j] = similarity
        
        else:
            javaDocSimilarity[i][j] = 1
'''
'''----------生產 function 的相似度文件----------'''
'''
javaDocFunctionDFTF = {}
javaDocFunctionWeights = {}
javaDocFunctionNullDescribe = {}
javaDocNullFunction = {}
javaDocFunctionSimilarity = {}

for num, className in enumerate(data):
    functionDFTF = {}
    functionNameList = []
    index = []
    
    if len(data[className]['Method Summary']) != 0:        
        for functionName in data[className]['Method Summary']:
            if len(data[className]['Method Summary'][functionName]) != 0:                
                functionNameList.append(functionName)             
                word_set = nltk.word_tokenize(data[className]['Method Summary'][functionName].lower())        
                # remove stop words
                word_set = [w for w in word_set if w not in stop_words]
                # lemmatization
                word_set = [lemmatizer.lemmatize(w) for w in word_set]
                
                for word in word_set:
                    if word not in functionDFTF:
                        functionDFTF.setdefault(word, {'df':1, 'inv_list':[]})
                        functionDFTF[word]['inv_list'].append({'functionName':functionName, 'tf':1})
                        index.append(word)
                    
                    else:
                        if className == functionDFTF[word.lower()]['inv_list'][-1]['functionName']:
                            functionDFTF[word]['inv_list'][-1]['tf'] += 1
                            
                        else:
                            functionDFTF[word]['df'] += 1
                            functionDFTF[word]['inv_list'].append({'functionName':functionName, 'tf':1})
                        
        if len(functionDFTF) != 0:
            javaDocFunctionDFTF.setdefault(className, functionDFTF)
        
            value = np.zeros((len(functionDFTF), len(functionNameList)), dtype=float)
            functionWeights = pd.DataFrame(value, index=index, columns=functionNameList)
        
            for word in functionDFTF:
                for invList in functionDFTF[word]['inv_list']:
                    functionWeights[invList['functionName']][word] = (1 + math.log(invList['tf'], 10)) * math.log(len(functionNameList) / functionDFTF[word]['df'], 10)
                
            javaDocFunctionWeights.setdefault(className, functionWeights)
            
            value = np.zeros((len(functionNameList), len(functionNameList)), dtype=float)
            functionSimilarity = pd.DataFrame(value, index=functionNameList, columns=functionNameList)
            
            for i in functionWeights:                
                lit = []
                norm_a = (functionWeights[i] * functionWeights[i]).sum() ** 0.5
                
                for j in functionWeights:
                    if i != j:
                        dot = (functionWeights[i] * functionWeights[j]).sum()            
                        norm_b = (functionWeights[j] * functionWeights[j]).sum() ** 0.5
                        similarity = dot / (norm_a*norm_b)
                        functionSimilarity[i][j] = similarity
        
                    else:
                        functionSimilarity[i][j] = 1
                        
            javaDocFunctionSimilarity.setdefault(className, functionSimilarity.to_dict())
            
        else:
            javaDocFunctionNullDescribe.setdefault(className, data[className]['Method Summary'])
            
    else:
        javaDocNullFunction.setdefault(className, data[className]['Method Summary'])

    print('現在進度：' + str(num + 1))
'''
'''----------生產功能三(See Also)實驗評估文件----------'''

classNameList = []

for className in data:
    if type(data[className]['Describe']) != list:
        classNameList.append(className)
        

name = []
sameSeeAlsoList = []
sameSeeAlsoDict = {}

for className in seeAlsoData:
    if className.split('_')[1] in classNameList:
        sameSeeAlsoList.append(className.split('_')[1])
        sameClassList = []
        
        for sameClass in seeAlsoData[className]:
            if sameClass in classNameList:
                sameClassList.append(sameClass)
        
        if len(sameClassList) != 0:
            sameSeeAlsoDict.setdefault(className.split('_')[1], sameClassList)

'''----------輸出文件----------'''
'''
javaDocWeights.to_csv('Java_Doc_Weights.csv')

javaDocSimilarity.to_csv('Java_Doc_Similarity.csv')

with open('Java_Doc_Function_Similarity.json', 'w') as f:
    json.dump(javaDocFunctionSimilarity, f, indent=2)
    
with open('See_Also_Data_in_Class.json', 'w') as f:
    json.dump(sameSeeAlsoDict, f, indent=2)
'''
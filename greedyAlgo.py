from collections import OrderedDict
import json
import html
import os
from flask import Blueprint, render_template 

#fix poping problem 


def greedyAlgo(budget,tNutrition,inputLis,repItem):
    
    file =   file = open(os.path.join("./target-project/database.json"), "r")
     
    data = json.load(file)

    currentBudget = 0
    curData = getDict()
    noMoney = False
    recList = []
    leftOver = []
    confStatement = False
    fListCost = 0
    sListCost = 0
    

    if not inputLis:
        refRecom = ['Carbohydrate', 'Fiber', 'Protein', 'Fatty acids',
            'Vitamin A', 'Vitamin C', 'Vitamin D (D2 + D3)', 'Vitamin E',
            'Vitamin K (phylloquinone)','Niacin', 'Calcium', 'Iron',
            'Potassium','Zinc']
        inputLis = refRecom


    for keys in curData.keys():
        if not keys in inputLis:
            leftOver.append(keys)

        
    while currentBudget <= budget:
        if inputLis and not noMoney:
            updRecList = getRecList(data,currentBudget,budget,inputLis,recList,noMoney,repItem,curData,tNutrition)
            recList =  updRecList[0]
            currentBudget = updRecList[1]
            curData = updRecList[2]
            noMoney = updRecList[3]
            inputLis =  updRecList[4]
            fListCost = currentBudget 
            
        elif not inputLis:
            if currentBudget >= budget: #Got the require nutrinets
                confStatement = True #but no more money
                currentBudget = [currentBudget,fListCost,sListCost]
                break
            else:
                updSubList = getSublist(data,leftOver,currentBudget,budget,recList,repItem,curData)
                secList = updSubList[0]
                currentBudget = updSubList[1]
                curData = updSubList[2]
                confStatement = True
                sListCost = currentBudget - fListCost
                currentBudget = [currentBudget,fListCost,sListCost]
                recList = [recList] + [secList]
                break
        else:
            currentBudget = [currentBudget,0,0]
            break
            
    
  
    return [recList,currentBudget,confStatement,curData]




def getRecList(data,currentBudget,budget,inputLis,recList,noMoney,repItem,curData,tNutrition):
    categoryFull = False
    sotDict = sortDictBy(data,inputLis)
    for items in sotDict:
        counter = 0
        for product in recList:
            if product[2] == sotDict[items][2]:
                counter = counter + 1
        
        if counter < repItem:
            if (currentBudget + sotDict[items][1]) <= budget and not categoryFull:
                currentBudget = currentBudget + sotDict[items][1]
                recList.append(sotDict[items])
                nutrintDict = sotDict[items][3]
                for nutrients in nutrintDict:
                    if nutrients in curData.keys():
                        curData[nutrients] = round(curData[nutrients] + nutrintDict[nutrients][0],2)
                
                temp = inputLis
                for category in inputLis:
                    if curData[category] >= tNutrition[category]:
                        print(category)
                        temp.pop(temp.index(category))
                        categoryFull = True
                inputLis = temp
            elif (currentBudget + sotDict[items][1]) >= budget and not recList:
                continue 

            elif categoryFull:
                break
                        
            else:
                noMoney = True
                break
    return [recList,currentBudget,curData,noMoney,inputLis]


def getSublist(data,leftOver,currentBudget,budget,recList,repItem,curData):
    secList = []
    finished = False
    sotDict = sortDictBy(data,leftOver)
    for items in sotDict:
        if not finished:
            counter = 0 
            for product in recList:
                if product[2] == sotDict[items][2]:
                    counter = counter + 1
            if counter < repItem:
                if (currentBudget + sotDict[items][1]) < budget:
                    currentBudget = currentBudget + sotDict[items][1]
                    secList.append(sotDict[items])
                    nutrintDict = sotDict[items][3]
                    for nutrients in nutrintDict:
                        if nutrients in curData.keys():
                            curData[nutrients] = round(curData[nutrients] + nutrintDict[nutrients][0],2)
                            
                elif (currentBudget + sotDict[items][1]) >= budget and not leftOver:
                    continue 

                else:
                    finished = True
        else:
            break
    return [secList,currentBudget,curData]


            
def sortDictBy(data, sortBy):
    targetDict = {}
    for categary in sortBy:
        for items in data:
            updatedInfo = prodNutCal(data[items],sortBy)
            targetDict[items] = updatedInfo
            
    targetDict = OrderedDict(sorted(targetDict.items(), key=lambda x:x[1][4],reverse = True))
    
    return targetDict


def prodNutCal(product,sortBy):
    nuTotal = 0
    allNutrients = product[3]
    for nutrients in allNutrients:#gets the keys(name of nutrients)
        if nutrients in sortBy:#if name on list then add item
            nutrintInfo = allNutrients[nutrients]
            nuGrams = convToGrams(nutrintInfo[0],nutrintInfo[1])
            nuTotal = nuTotal + nuGrams

    try:
        ratio = nuTotal/product[1]
    except ZeroDivisionError:
        ratio=0
    try:
        if product[4]:
            product.pop(4)
            product.append(ratio)
            
    except IndexError:
        product.append(ratio)
        
    return product

    

def convToGrams(amount,unit):
    grams = 0
    if unit ==  "MG":
         grams = amount * (1/1000)
    elif unit ==  "KCAL":
        grams = 0
    elif unit == "IU":
        grams = ((amount * 0.3) * (1/1000)) * (1/10000)
    elif unit == 'UG':
        grams = amount * (1/1000000)
    else:
        grams = amount
    return grams










def getDict():
    totalNutrition = {'Carbohydrate': 0, 'Protein': 0, 'α-Linolenic Acid': 0, 'Linoleic Acid': 0,
                      'Vitamin A': 0, 'Vitamin C': 0, 'Vitamin B6': 0, 'Vitamin E': 0, 'Thiamin': 0,
                      'Vitamin B12': 0, 'Riboflavin': 0, 'Folate': 0, 'Niacin': 0, 'Choline': 0,
                      'Biotin': 0, 'Carotenoids': 0, 'Calcium': 0, 'Chloride': 0, 'Chromium': 0, 
                      'Copper': 0, 'Fluoride': 0, 'Iodine': 0, 'Iron': 0, 'Magnesium': 0,
                      'Manganese': 0, 'Molybdenum': 0, 'Phosphorus': 0, 'Potassium': 0,
                      'Selenium': 0, 'Sodium': 0, 'Zinc': 0, 'Fiber': 0, 'Fatty acids': 0,
                      'Vitamin D (D2 + D3)': 0, 'Vitamin K (phylloquinone)': 0,
                      'Pantothenic acid': 0}

    return totalNutrition






from collections import OrderedDict
import json
import html
import os

#fix poping problem 

def greedyAlgo(budget,tNutrition,inputLis,repItem):
    
    file = open("itemDatabase.json") 
    data = json.load(file)        

    tNutrition = tNutrition[0]
    currentBudget = 0
    curData = getDict()
    noMoney = False
    recList = []
    subList = []
    leftOver = []
    confStatement = ''
    fListCost = 0
    sListCost = 0
    notEnough = False

    if not inputLis:
        refRecom = ['Carbohydrate', 'Fiber', 'Protein', 'Fatty acids',
            'Vitamin A', 'Vitamin C', 'Vitamin D (D2 + D3)', 'Vitamin E',
            'Vitamin K (phylloquinone)','Niacin', 'Calcium', 'Iron',
            'Potassium','Zinc']
        inputLis = refRecom


    for keys in curData.keys():
        if not keys in inputLis:
            leftOver.append(keys)

#Creates the shopping list
    updRecList = getRecList(data,currentBudget,budget,inputLis,recList,subList,noMoney,repItem,curData,tNutrition,True)
    recList =  updRecList[0]
    recList.sort(key = lambda recList: recList[0])
    currentBudget = updRecList[1]
    curData = updRecList[2]
    noMoney = updRecList[3]
    inputLis =  updRecList[4]
    notEnough =  updRecList[5]
    fListCost = currentBudget

    if not inputLis:
        print('sublist')
        updSubList = getRecList(data,currentBudget,budget,leftOver,recList,subList,noMoney,repItem,curData,tNutrition,False)
        subList =  updSubList[0]
        subList.sort(key = lambda updSubList: updSubList[0])  
        currentBudget = updSubList[1]
        curData = updSubList[2]
        recList = [recList,subList]
        currentBudget = [currentBudget,fListCost,currentBudget-fListCost]
        confStatement = "green"
       
    else:
        if noMoney and not notEnough:
            confStatement = 'red'
            currentBudget = [currentBudget,0,0]

        else:
            confStatement = 'orange'
            currentBudget = [currentBudget,0,0]

    return [recList,currentBudget,confStatement,curData]


def getRecList(data,currentBudget,budget,inputLis,recList,subList,noMoney,repItem,curData,tNutrition,isRectList):
    categoryFull = False
    sotDict = sortDictBy(data,inputLis)
    keys = list(sotDict.keys())
    index = 0
    notEnough = False
    
    while (inputLis) and (not noMoney) and (not notEnough):
        ids = keys[index]
        items = data[ids]
        name = items[0]
        price = items[1][0]
        counter = 0
        index = index + 1
        
        if index == len(keys):
            notEnough = True

        for product in recList: #check how many of the same 
            if product[0] == name: #item have been added 
                counter = counter + 1 #if more than listed then
                                    #add to counter and skip
        if not isRectList:
            for product in subList: #check how many of the same 
                if product[0] == name: #item have been added 
                    counter = counter + 1 #i
            
        if (counter < repItem) and (currentBudget + price) <= budget and not categoryFull:
            currentBudget = currentBudget + price
            if isRectList:
                recList.append(items)
            else:
                recList.append(items)
            nutrintDict = items[2]
            for nutrients in nutrintDict:
                if nutrients in curData.keys():
                    curData[nutrients] = round(curData[nutrients] + nutrintDict[nutrients][0],2)
            temp = inputLis
            for category in inputLis:
                if curData[category] >= tNutrition[category]:
                    temp.pop(temp.index(category))
                    categoryFull = True
            inputLis = temp
            
        else:
            if index == len(keys):
                if ((currentBudget/budget) * 100) >= 95:
                    noMoney = True
                else:
                    notEnough == True
            elif categoryFull:
                sotDict = sortDictBy(data,inputLis)
                keys = list(sotDict.keys())
                categoryFull = False
                index = 0
                if not sotDict:
                    notEnough = True
            else:
                continue
            
    if isRectList:  
        return [recList,currentBudget,curData,noMoney,inputLis,notEnough]
    else:
        return [subList,currentBudget,curData,noMoney,inputLis,notEnough]
        
def sortDictBy(data, sortBy):
    targetDict = {}

    for items in data:
        item = data[items]
        updatedInfo = prodNutCal(item,sortBy)
        targetDict[items] = updatedInfo
    
    targetDict = OrderedDict(sorted(targetDict.items(), key=lambda x:x[1][1][1],reverse = True))
    
    return targetDict


def prodNutCal(product,sortBy):
    nuTotal = 0
    allNutrients = product[2]
    for nutrients in allNutrients:#gets the keys(name of nutrients)
        if nutrients in sortBy:#if name on list then add item
            nutrintInfo = allNutrients[nutrients]
            nuGrams = convToGrams(nutrintInfo[0],nutrintInfo[1])
            nuTotal = nuTotal + nuGrams
    price = product[1][0]
        
    
    try:
        ratio = nuTotal/price
    except ZeroDivisionError:
        ratio = 0
        
    product[1][1] = ratio
    
        
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






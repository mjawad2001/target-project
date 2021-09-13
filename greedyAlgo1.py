from collections import OrderedDict
import json
import html
import os

#fix poping problem 

def greedyAlgo1(budget,tNutrition,inputLis,repItem,mPCat):
    
    file =   file = open(os.path.join("./project/FinalTdataBase.json"), "r")
    data = json.load(file)
    tempt = []
 
    
    currentBudget = 1
    curData = getDict()
    noMoney = False
    recList = []
    subPleList = []
    leftOver = []
    confStatement = False
    
    

    if not inputLis:
        refRecom =  refRecom = ['Carbohydrate', 'Fiber', 'Protein', 'Fatty acids',
                                'Vitamin A', 'Vitamin C', 'Vitamin D (D2 + D3)', 'Vitamin E',
                                'Vitamin K (phylloquinone)','Niacin', 'Calcium', 'Iron',
                                'Potassium','Zinc']
        inputLis = refRecom

    for keys in curData.keys():
        if not keys in inputLis:
            leftOver.append(keys)

    
    attributes = getRecList(data,currentBudget,budget,inputLis,recList,noMoney,repItem,curData,tNutrition,mPCat)
    recList =  attributes[0]
    currentBudget = attributes[1]
    curData = attributes[2]
    noMoney = attributes[3]
    inputLis =  attributes[4]
    currentBudget = [currentBudget,0,0]
    if not noMoney and not inputLis:
        confStatement = True 
        origMSent = currentBudget[0]
        attributes = getSubList(data,currentBudget[0],budget,leftOver,subPleList,noMoney,repItem,curData,tNutrition,mPCat,recList)
        
        subPleList =  attributes[0]
        recList = [recList] + [subPleList]
        
        tot = attributes[1]
        currentBudget[0] = tot
        currentBudget[1] = origMSent
        currentBudget[2] = tot - origMSent
        

        curData = attributes[2]
   
       
        

        
        
        
        
    



    return [recList, currentBudget,confStatement,curData]



def getRecList(data,currentBudget,budget,inputLis,recList,noMoney,repItem,curData,tNutrition,mPCat):

    recDict = {'Protein':[], 'Fruits':[], 'Vegetable':[], 'Grains':[],'Dairy':[]} #just to check items 
    totNutDict = tNutrition[0]
    totMyPlate = tNutrition[1]

    categoryFull = False
    sortDict = sortDictBy(data,inputLis)
    changCat = False
    nextCat = mPCat[0]
    
    noEnoughM = False
    oldBudg = 0
    oldCats = 0

    breakCount = 0 
    while currentBudget <= budget or inputLis:
        oldBudg = currentBudget
        oldCats = len(inputLis)
            
        for cat in mPCat:
            catData = sortDict[cat]
            catItemFound = False
            changCat = False
            if cat == nextCat:
                index = mPCat.index(cat)
                if index == len(mPCat) - 1:
                    nextCat = mPCat[0]
                else:
                    nextCat = mPCat[index + 1]
                    
                for item in catData:
                    itemDetails = catData[item]
                    counter = 0 
                    for product in recList:
                        if product[0] == itemDetails[0]:
                            counter = counter + 1
        
                    if counter < repItem:
                        if ((currentBudget + itemDetails[1]) <= budget - 2) and (not catItemFound) and (totMyPlate[cat]/10 >= itemDetails[4][0]):
                            catItemFound = True
                            currentBudget = currentBudget + itemDetails[1]
                            recDict[cat].append(itemDetails)
                            recList.append(itemDetails)
                            nutrintDict = itemDetails[2]
                            for nutrients in nutrintDict:
                    
                                if nutrients in curData.keys():
                                    curData[nutrients] = round(curData[nutrients] + nutrintDict[nutrients][0],2)
                                else:
                                    if nutrients in 'Total lipid (fat)':
                                        curData["Fatty acids"] = round(curData["Fatty acids"] + nutrintDict['Total lipid (fat)'][0],2)    
                            temp = inputLis
                        
                            for category in inputLis:
                                if curData[category] >= tNutrition[0][category]:
                                   
                                    temp.pop(temp.index(category))
                                    categoryFull = True
                            inputLis = temp
                
                        elif (currentBudget + itemDetails[1]) >= budget and not recList:
                            continue
                        
                        elif categoryFull or catItemFound:
                            if catItemFound:
                                catItemFound = False
                                break
                            else:
                                break
                    else:
                        continue 
            else:
                continue 
                            
            if categoryFull:
                if inputLis:
                    categoryFull = False
                    sortDict = sortDictBy(data,inputLis)
                    break
                else:
                    break
            
        if (currentBudget == oldBudg and oldCats == len(inputLis)):
            breakCount = breakCount + 1
            if breakCount >= 10:
                print('stuck')
                break
        if not inputLis:
            break
    if  currentBudget >= budget:
        noMoney = True
        
    return [recList,currentBudget,curData,noMoney,inputLis,recDict]


def getSubList(data,currentBudget,budget,inputLis,recList,noMoney,repItem,curData,tNutrition,mPCat,mainRecList):

    recDict = {'Protein':[], 'Fruits':[], 'Vegetable':[], 'Grains':[],'Dairy':[]} #just to check items 
    totNutDict = tNutrition[0]
    totMyPlate = tNutrition[1]

    categoryFull = False
    sortDict = sortDictBy(data,inputLis)
    changCat = False
    nextCat = mPCat[0]
    
    noEnoughM = False
    oldBudg = 0
    oldCats = 0
    breakCount = 0
    while currentBudget <= budget or inputLis:
        oldBudg = currentBudget
        oldCats = len(inputLis) 
            
        for cat in mPCat:
            catData = sortDict[cat]
            catItemFound = False
            changCat = False
            if cat == nextCat:
                index = mPCat.index(cat)
                if index == len(mPCat) - 1:
                    nextCat = mPCat[0]
                else:
                    nextCat = mPCat[index + 1]
                    
                for item in catData:
                    itemDetails = catData[item]
                    notInList = True
                    counter = 0 
                    for product in recList:
                        if product[0] == itemDetails[0]:
                            counter = counter + 1
                    for items in mainRecList:
                        if itemDetails[0] == items[0]:
                            notInList = False 
                            
                        
                    if counter < repItem and notInList:
                        if ((currentBudget + itemDetails[1]) <= budget - 2) and (not catItemFound) and (totMyPlate[cat]/10 >= itemDetails[4][0]):
                            catItemFound = True
                            currentBudget = currentBudget + itemDetails[1]
                            recDict[cat].append(itemDetails)
                            recList.append(itemDetails)
                            nutrintDict = itemDetails[2]
                            for nutrients in nutrintDict:
                    
                                if nutrients in curData.keys():
                                    curData[nutrients] = round(curData[nutrients] + nutrintDict[nutrients][0],2)
                                else:
                                    if nutrients in 'Total lipid (fat)':
                                        curData["Fatty acids"] = round(curData["Fatty acids"] + nutrintDict['Total lipid (fat)'][0],2)    
                            temp = inputLis
                           
                            for category in inputLis:
                                if curData[category] >= tNutrition[0][category]:
                                    temp.pop(temp.index(category))
                                    categoryFull = True
                            inputLis = temp
                
                        elif (currentBudget + itemDetails[1]) >= budget and not recList:
                            continue
                        
                        elif catItemFound:
                            break
                    else:
                        continue 
            else:
                continue 
                            
            if categoryFull:
                if inputLis:
                    categoryFull = False
                    sortDict = sortDictBy(data,inputLis)
                    break
                else:
                    break
            
        if (currentBudget == oldBudg and oldCats == len(inputLis)):
            breakCount = breakCount + 1
            if breakCount >= 10:
                break
        if not inputLis:
            break
    if  currentBudget >= budget:
        noMoney = True
        
    return [recList,currentBudget,curData,noMoney,inputLis,recDict]
            
def sortDictBy(data,sortBy):
    tempDict = {}
    targetDict = {}
    checkRepeats = []
    dictRep = {}
    
    for cat in data:
        catName = data[cat]
        for items in catName:
            if not items in checkRepeats:
                checkRepeats.append(items)
                item = catName[items]
                updatedInfo = prodNutCal(item,sortBy)
                tempDict[items] = updatedInfo
        tempDict = OrderedDict(sorted(tempDict.items(), key=lambda x:x[1][3][0],reverse = True))
        targetDict[cat] = tempDict
        tempDict = {}
    return targetDict


def prodNutCal(product,sortBy):
    nuTotal = 0
    allNutrients = product[2]
    for nutrients in allNutrients:#gets the keys(name of nutrients)
        if nutrients in sortBy:#if name on list then add item
            nutrintInfo = allNutrients[nutrients]
            nuGrams = convToGrams(nutrintInfo[0],nutrintInfo[1])
            nuTotal = nuTotal + nuGrams
    try:
        ratio = nuTotal/product[1]
    except ZeroDivisionError:
        ratio = 0


    if len(product) == 3:
        product.append([ratio,'ratio'])
        product.append([nuTotal,'nuTotal'])
    else:
        product[3] = [ratio,'ratio']
        product[4] = [nuTotal,'totMass']

      
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





##    rt = json.dumps(data, sort_keys=True, indent=4)
##    print(rt)

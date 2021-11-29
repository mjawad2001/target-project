from collections import OrderedDict
import json
import html
import os

#64 or less 

def budgetAlgo(budget,tNutrition,inputLis,repItem):
    
    file =   file = open(os.path.join("./target-project/itemDatabase.json"), "r")
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
                    'Vitamin A', 'Vitamin C', 'Vitamin D (D2 + D3)',
                    'Vitamin B-6', 'Vitamin E', 'Vitamin K (phylloquinone)',
                    'Thiamin', 'Vitamin B-12', 'Riboflavin', 'Folate', 'Niacin', 'Calcium',
                    'Iodine', 'Iron', 'Phosphorus','Potassium',
                    'Sodium', 'Sugars', 'Cholesterol', 'Zinc',
                    'Pantothenic acid','Manganese','Magnesium','Molybdenum','Selenium','Biotin','Choline']
        
        inputLis = refRecom

    for keys in curData.keys():
        if not keys in inputLis:
            leftOver.append(keys)



    tempMeas = itemRateTemp()
    sortTotNut = {}
    for cats in inputLis:
        unit = tempMeas[cats]
        amount = tNutrition[cats]
        newVal = convToGrams(amount,unit)
        sortTotNut[cats] = newVal

        

    sortTotNut = dict(sorted(sortTotNut.items(), key=lambda item: item[1],reverse = True))
    keys = list(sortTotNut.keys())
    
    splitedSize = 4
    splitList = [keys[x:x+splitedSize] for x in range(0, len(keys), splitedSize)]
  
    done = False
    while not done:
        if not noMoney and not notEnough and splitList:
            updRecList = getRecList(data,currentBudget,budget,splitList[0],recList,subList,noMoney,repItem,curData,tNutrition,True)
            recList = updRecList[0]
            currentBudget = updRecList[1]
            curData = updRecList[2]
            noMoney = updRecList[3]
            catFul =  updRecList[4]
            notEnough =  updRecList[5]
            popList = updRecList[6]
            
            for popCats in popList:
                for sets in splitList:
                    if popCats in sets:
                        sets.pop(sets.index(popCats))
            for sets in splitList:
                if not sets:
                    splitList.pop(splitList.index(sets))
                    
            splitList = list(filter(None, splitList))
           
        else:
            done = True
    
    if splitList:
        if noMoney and not notEnough:
            confStatement = 'red'
            currentBudget = [currentBudget,0,0]
            recList = [recList,subList]

        else:
            confStatement = 'orange'
            currentBudget = [currentBudget,0,0]
            recList = [recList,subList]
    else:
        fListCost = currentBudget
        updSubList = getRecList(data,currentBudget,budget,leftOver,recList,subList,noMoney,repItem,curData,tNutrition,False)
        subList = updSubList[0]
        subList.sort(key = lambda updSubList: updSubList[0])  
        currentBudget = updSubList[1]
        curData = updSubList[2]
        recList = [recList,subList]
        currentBudget = [currentBudget,fListCost,currentBudget-fListCost]
        confStatement = "green"
       
                
        
    
        


    return [recList,currentBudget,confStatement,curData]


def getRecList(data,currentBudget,budget,inputLis,recList,subList,noMoney,repItem,curData,tNutrition,isRectList):
    categoryFull = False
    sotDict = sortDictBy(data,inputLis)
    keys = list(sotDict.keys())
    index = 0
    notEnough = False
    catFul = False
    popList = []
    
    
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
                    if curData[nutrients] >=  tNutrition[nutrients]:
                        popList.append(nutrients)
                    
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
        return [recList,currentBudget,curData,noMoney,catFul,notEnough,popList]
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
    wantedMass = 0
    for sortCat in sortBy:
        if sortCat in allNutrients.keys():
            info = allNutrients[sortCat]
            nuGrams = convToGrams(info[0],info[2])
            wantedMass = wantedMass + nuGrams
  
            
    price = product[1][0]
    try:
        ratio = wantedMass/price
    except ZeroDivisionError:
        ratio = 0
        
    product[1][1] = ratio
    
        
    return product

def getDict():
    totalNutrition =  {'Carbohydrate': 0, 'Fiber': 0, 'Protein': 0, 'Fatty acids': 0, 'Vitamin A': 0, 'Vitamin C': 0,
                       'Vitamin D (D2 + D3)': 0, 'Vitamin B-6': 0, 'Vitamin E': 0, 'Vitamin K (phylloquinone)': 0,
                       'Thiamin': 0, 'Vitamin B-12': 0, 'Riboflavin': 0, 'Folate': 0, 'Niacin': 0, 'Choline': 0,
                       'Pantothenic acid': 0, 'Biotin': 0, 'Calcium': 0, 'Chromium': 0, 'Copper': 0, 'Iodine': 0,
                       'Iron': 0, 'Magnesium': 0, 'Manganese': 0, 'Molybdenum': 0, 'Phosphorus': 0, 'Potassium': 0,
                       'Selenium': 0, 'Sodium': 0, 'Zinc': 0, 'Sugars': 0, 'Cholesterol': 0}
    
    return totalNutrition

def itemRateTemp():
    itemRating = {'Chromium': 'mcg', 'Molybdenum': 'mcg', 'Iodine': 'mcg', 'Selenium': 'mcg', 'Biotin': 'mcg', 'Manganese': 'mg',
                  'Pantothenic acid': 'mg', 'Vitamin E': 'mg', 'Vitamin B-12': 'mcg', 'Vitamin D (D2 + D3)': 'mcg', 'Choline': 'mg',
                  'Vitamin K (phylloquinone)': 'ug', 'Copper': 'mg', 'Zinc': 'mg', 'Phosphorus': 'mg', 'Magnesium': 'mg',
                  'Vitamin B-6': 'mg', 'Cholesterol': 'mg', 'Folate': 'ug', 'Riboflavin': 'mg', 'Thiamin': 'mg', 'Vitamin C': 'mg',
                  'Niacin': 'mg', 'Vitamin A': 'ug', 'Iron': 'mg', 'Fiber': 'g', 'Calcium': 'mg', 'Sugars': 'g', 'Potassium': 'mg',
                  'Carbohydrate': 'g', 'Protein': 'g', 'Sodium': 'mg', 'Fatty acids': 'g'}

    return itemRating




def convToGrams(amount,unit):
    unit = unit.lower().strip()
   
    grams = 0
    if unit ==  "mg":
         grams = amount * (1/1000)
    elif unit ==  "kcal":
        grams = 0
    elif unit == "ui":
        grams = ((amount * 0.3) * (1/1000)) * (1/10000)
    elif unit == 'mcg dfe':
        grams = amount * (1/1000000)
    elif unit == 'ug':
        grams = amount * (1/1000000)
    elif unit == 'mcg':
        grams = amount * 0.000001
    else:
        grams = amount
        
    if amount < 0:
        grams = 0
        
    return grams









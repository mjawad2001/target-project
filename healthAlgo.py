from collections import OrderedDict
from operator import itemgetter
import json
import html
import os
import math
#add itmes measuremenst to returning dict
#get the cheapest items to compared and detemrined if a sublist needs too be made
#get the average between a couple of items in each category and start looping through the cat
#wiht the most nutrion value from all
#check to see the not enough nutrion found problem 

def healthAlgo(budget,tNutrition,inputLis,repItem,mPCat):
    file =   file = open(os.path.join("./target-project/itemDatabase.json"), "r")
    itemData = json.load(file)
    

    file =   file = open(os.path.join("./target-project/indexDatabase.json"), "r")
    indexData = json.load(file)   

    tNutrition = tNutrition[0]
    currentBudget = 0
    curData = getDict()
    noMoney = False
    recList = []
    subList = []
    leftOver = []
    confStatement = False
    fListCost = 0
    sListCost = 0
    succRecList = True

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
    createRecList = True
    updRecList = getLists(itemData,indexData,currentBudget,budget,inputLis,subList,recList,noMoney,repItem,curData,tNutrition,mPCat,createRecList)
    recList =  updRecList[0]
    recList.sort(key = lambda recList: recList[0])
    currentBudget = updRecList[1]
    curData = updRecList[2]
    noMoney = updRecList[3]
    inputLis =  updRecList[4]
    notEnough =  updRecList[5]
    fListCost = currentBudget

    print(notEnough,noMoney)

    if not inputLis:
        print('sublist')
        createRecList = False
        updSubList = getLists(itemData,indexData,currentBudget,budget,leftOver,subList,recList,noMoney,repItem,curData,tNutrition,mPCat,createRecList)
        subList =  updSubList[0]
        subList.sort(key = lambda updSubList: updSubList[0])  
        currentBudget = updSubList[1]
        curData = updSubList[2]
        noMoney = updSubList[3]
        inputLis =  updSubList[4]
        recList = [recList,subList]
        currentBudget = [currentBudget,fListCost,currentBudget-fListCost]
        confStatement = 'green'
        
       
    else:
        if noMoney and not notEnough:
            confStatement = 'red'
            currentBudget = [currentBudget,0,0]
            recList = [recList,subList]

        else:
            confStatement = 'orange'
            currentBudget = [currentBudget,0,0]
            recList = [recList,subList]

      
    return [recList,currentBudget,confStatement,curData]

def getLists(itemData,indexData,currentBudget,budget,inputLis,subList,recList,noMoney,repItem,curData,tNutrition,mPCat,createRecList):
    sotDict = sortDictBy(itemData,indexData,inputLis,mPCat)    
    categoryFull = False
    nextCat = False
    notEnough = False
    tempCats = list(sotDict.keys())
    if tempCats:
        cats = tempCats[0]
    else:
        notEnough = True
    track = {"Protein":0,"Vegetable":0,"Fruits":0,"Grains":0,'Dairy':0}
    
    

    while (inputLis) and (not noMoney) and (not notEnough):
        if nextCat:
            cats = getNexttCat(tempCats,cats)
            nextCat = False
            
        keys = sotDict[cats]
        while (not categoryFull) and (not noMoney) and (not notEnough) and (not nextCat):
            index = track[cats]
            if index + 1 == len(keys):
                tempCats.pop(tempCats.index(cats))
                if not tempCats:
                    if ((currentBudget/budget) * 100) >= 80:
                        noMoney = True
                    else:
                        notEnough = True
                else:
                    nextCat = True

            ids = keys[index]
            track[cats] = index + 1
            item = itemData[ids]
            name = item[0]
            price = item[1][0]
            repeats = 0
                          
            for product in recList: #check how many of the same 
                if product[0] == name: #item have been added 
                    repeats = repeats + 1 #if more than listed then
                                        #add to counter and skip
            if  not createRecList:
                for product in subList: #check how many of the same 
                    if product[0] == name: #item have been added 
                        repeats = repeats + 1 #if more than listed then
                                            #add to counter and skip
            if (repeats < repItem) and ((currentBudget + price) <= budget) and (index + 1 <= len(keys)):
                if createRecList:
                    print('|',currentBudget,'|',len(inputLis),'|',name,'|',ids,'|',cats,'|',price)
##                    print(item[2])
                currentBudget = currentBudget + price

                if createRecList:
                    recList.append(item)
                else:
                    subList.append(item)
                    
                nutrintDict = item[2]
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
                if not categoryFull:
                    nextCat = True
                print()
            else:
                if  (track[cats] == len(cats) - 1) and (cats in tempCats):
                    tempCats.pop(tempCats.index(cats))
                    if tempCats:
                        nextCat = True
                    else:
                        if ((currentBudget/budget) * 100) >= 80:
                            noMoney = True
                        else:
                            notEnough = True

        if categoryFull:
            categoryFull = False
            nextCat = False
            sotDict = sortDictBy(itemData,indexData,inputLis,mPCat)
            tempCats = list(sotDict.keys())
            if tempCats:
                cats = getNexttCat(tempCats,cats)
            for cat in track:
                track[cat] = 0
                
    if createRecList:
        return [recList,currentBudget,curData,noMoney,inputLis,notEnough]
    else:
        return [subList,currentBudget,curData,noMoney,inputLis,notEnough]
        

def getNexttCat(tempCats,oldCat):
    ref = ["Protein","Vegetable","Fruits","Grains",'Dairy']
    done = False
    count = 0
    if oldCat in tempCats:
        try:
            oldIndex = tempCats.index(oldCat)
            newCat = tempCats[oldIndex + 1]
        except IndexError:
            newCat = tempCats[0] 
        
    else:
        while not done:
            try:
                nIndex = ref.index(oldCat)
                count = count + 1
                tempCat = ref[nIndex + count]
                if tempCat in tempCats:
                    newCat = tempCat
                    done = True
            except IndexError:
                newCat = tempCats[0]
                done = True
        
    return newCat  
  
    
    

            
def sortDictBy(itemData,indexData,sortBy,mPCat):
    tempDict = {}
    targetDict = {}
    checkRepeats = []
    dictRep = {}
    
    for cat in mPCat:
        catName = indexData[cat]
        for tcin in catName:
            item = itemData[tcin]
            updatedInfo = prodNutCal(item,sortBy)
            if not updatedInfo[1]:#truncate the items with a ratio of 0
                tempDict[tcin] = updatedInfo[0] #b/c they have no useful val 
            else:
                continue
        if len(tempDict) > 0: 
            tempDict = OrderedDict(sorted(tempDict.items(), key=lambda x:x[1][1][1],reverse = True))
            targetDict[cat] = list(tempDict.keys())
            tempDict = {}
            
    return targetDict


def prodNutCal(product,sortBy):
    nuTotal = 0
    allNutrients = product[2]
    for nutrients in allNutrients:#gets the keys(name of nutrients)
        if nutrients in sortBy:#if name on list then add item
            nutrintInfo = allNutrients[nutrients]
            nuGrams = convToGrams(nutrintInfo[0],nutrintInfo[2])
            nuTotal = nuTotal + nuGrams
    price = product[1][0]

    
    try:
        ratio = nuTotal/price
    except ZeroDivisionError:
        ratio = 0
        
##        ratio = truncate(ratio,5)
        
    product[1][1] = ratio

    
    if ratio == 0:
        return [product,True]
    else:
        return [product,False]
        
    
    

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




def truncate(number, digits):
    stepper = 10.0 ** digits
    return math.trunc(stepper * number) / stepper







def getDict():
    totalNutrition =  {'Carbohydrate': 0, 'Fiber': 0, 'Protein': 0, 'Fatty acids': 0, 'Vitamin A': 0, 'Vitamin C': 0,
                       'Vitamin D (D2 + D3)': 0, 'Vitamin B-6': 0, 'Vitamin E': 0, 'Vitamin K (phylloquinone)': 0,
                       'Thiamin': 0, 'Vitamin B-12': 0, 'Riboflavin': 0, 'Folate': 0, 'Niacin': 0, 'Choline': 0,
                       'Pantothenic acid': 0, 'Biotin': 0, 'Calcium': 0, 'Chromium': 0, 'Copper': 0, 'Iodine': 0,
                       'Iron': 0, 'Magnesium': 0, 'Manganese': 0, 'Molybdenum': 0, 'Phosphorus': 0, 'Potassium': 0,
                       'Selenium': 0, 'Sodium': 0, 'Zinc': 0, 'Sugars': 0, 'Cholesterol': 0}
    
    return totalNutrition


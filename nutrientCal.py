from bs4 import BeautifulSoup
import re, json
import mechanicalsoup
from decimal import Decimal
from fractions import Fraction
import ast

def nutrientCal(people,timeDays):
    totalMass = 0
    totalNutrition = getDict()
    totalNutrition = getDict()
    for individual in people:
        individual = ast.literal_eval(individual)
        for nutrients in individual:
            totalAmount = totalNutrition[nutrients] 
            totalNutrition[nutrients] = totalAmount + individual[nutrients] * timeDays
            
     
    for cat in totalNutrition:
        grams = convToGrams(cat,totalNutrition[cat])
        totalMass = totalMass + grams
   
    myPlate = getMyplate(totalMass)
    return [totalNutrition,myPlate]

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


def getMyplate(totMass):
    totalMyPLate = getPLate()
    for cat in totalMyPLate:
        if cat == 'Fruits':
            totalMyPLate[cat] = round(0.1 * totMass,2)
        elif cat == 'Vegetable':
            totalMyPLate[cat] = round(0.4 * totMass,2)
        elif cat == 'Grains':
            totalMyPLate[cat] = round(0.3 * totMass,2)
        elif cat == 'Protein':
            totalMyPLate[cat] = round(0.2 * totMass,2)
            
   
    return totalMyPLate
                        
    
                
def getPLate():
    totalMyPLate = {"Protein": 0,"Vegetable":0,"Fruits": 0,"Grains": 0,'Dairy':0}

    return totalMyPLate
    
def convToGrams(cat,amount):
    #The dri cal list nutrients in different measurements so we need to convert all the nutrients in to grams
    #to get the total nutritent mass fro that person
    
    alrGrams = ['Carbohydrate','Fiber','Protein','Fatty acids','α-Linolenic Acid',
                'Linoleic Acid','Choline','Chloride','Phosphorus']
    
    mcg = ['Vitamin A','Vitamin D (D2 + D3)','Vitamin K (phylloquinone)','Vitamin B12',
           'Folate','Biotin','Chromium','Copper','Iodine','Molybdenum','Selenium','Carotenoids']

    mg = ['Vitamin C','Vitamin B6','Vitamin E','Thiamin','Vitamin B12','Riboflavin',
          'Niacin','Pantothenic acid','Calcium','Fluoride', 'Iron','Magnesium',
          'Manganese','Potassium','Sodium','Zinc']

    if cat in alrGrams:
        return amount
    
    elif cat in mcg:
        amount = amount * (1/1000000)
        return amount
    
    else:
        amount = amount * (1/1000)
        return amount
    
 
        
          









    
    

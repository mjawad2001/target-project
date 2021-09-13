from bs4 import BeautifulSoup
import re
import mechanicalsoup

def nutrientRequest(people):
    individualInfo = {}
    for i in range(len(people)):
       
        if people[i][1].upper() == 'MALE':
            browser = mechanicalsoup.StatefulBrowser()
            browser.open('https://www.nal.usda.gov/fnic/dri-calculator/') 
            browser.select_form('form[action="results.php"]')
            browser.form['SEX'] = people[i][1].upper()
            browser.form['AGE'] = people[i][2]
            browser.form['HEIGHT_FEET'] = people[i][3][0]
            browser.form['HEIGHT_INCHES'] = people[i][3][1]
            browser.form['WEIGHT'] = people[i][4]
            browser.form['ACTIVITY'] = people[i][5]
            #browser.launch_browser()
            response = browser.submit_selected()
            soup = BeautifulSoup(response.text, 'lxml')
            indDict = getDict()
            filledDict = bNutrientDict(soup,indDict)
            individualInfo[people[i][0]] = indDict
        else:
            browser = mechanicalsoup.StatefulBrowser()
            browser.open('https://www.nal.usda.gov/fnic/dri-calculator/') 
            browser.select_form('form[action="results.php"]')
            browser.form['SEX'] = people[i][1].upper()
            browser.form['AGE'] = people[i][2]
            browser.form['HEIGHT_FEET'] = people[i][3][0]
            browser.form['HEIGHT_INCHES'] = people[i][3][1]
            browser.form['WEIGHT'] = people[i][4]
            browser.form['ACTIVITY'] = people[i][5]
            browser.form['F_STATUS'] = "Not Pregnant or Lactating"
            #browser.launch_browser()
            response = browser.submit_selected()
            soup = BeautifulSoup(response.text, 'lxml')
            indDict = getDict()
            filledDict = bNutrientDict(soup,indDict)
            individualInfo[people[i][0]] = indDict
    return individualInfo
            
            

    
def bNutrientDict(soup,pDict):
    ntable = soup.find_all("table", {"class": "results-table"})
    nName = list(pDict.keys())
    for nutrients in ntable:
        tableLines = nutrients.text.splitlines()
        for words in tableLines:
            for categories in nName:
                if categories in words:
                    grams = re.findall(r"[-+]?\d*\.\d+|\d+", words) #splits 1,000 to ['1','000']
                    lGrams = len(grams)
                    if lGrams > 3:
                        if len(grams[1]) == 3:
                            pDict[categories] = float(grams[0] + grams[1])    
                    else:
                        if grams:
                            pDict[categories] = float(grams[0])
    return pDict

def getDict():
    totalNutrition = {'Carbohydrate':0,'Total Fiber':0,'Protein':0,'Fat':0,'α-Linolenic Acid':0,
                      'Linoleic Acid':0,'Vitamin A':0,'Vitamin C':0,'Vitamin D':0,'Vitamin B6':0,
                      'Fat':0,'α-Linolenic Acid':0,'Linoleic Acid':0,'Vitamin A':0, 'Linoleic Acid':0,
                      'Vitamin E':0,'Vitamin K':0,'Thiamin':0,'Vitamin B12':0,'Riboflavin':0,'Folate':0,
                      'Niacin':0,'Choline':0,'Biotin':0,'Pantothenic Acid':0,'Carotenoids':0,'Calcium':0,
                      'Chloride':0,'Chromium':0,'Copper':0,'Fluoride':0,'Iodine':0,'Iron':0,'Magnesium':0,
                      'Manganese':0,'Molybdenum':0,'Phosphorus':0,'Potassium':0,'Selenium':0,'Sodium':0,
                      'Zinc':0}
    return totalNutrition






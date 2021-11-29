from bs4 import BeautifulSoup
import re, json
import mechanicalsoup


#list of people 
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
            reqDict = bNutrientDict(soup)
            individualInfo[people[i][0]] = reqDict
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
##            browser.form['F_STATUS'] = people[i][6]
            #browser.launch_browser()
            response = browser.submit_selected()
            soup = BeautifulSoup(response.text, 'lxml')
            reqDict = bNutrientDict(soup)
            individualInfo[people[i][0]] = reqDict
    return individualInfo
            
            

    
def bNutrientDict(soup,):
    ntable = soup.find_all("table", {"class": "results-table"}) 

    retuDict = {}
    for nutrients in ntable:
        cap = nutrients.find('caption')
        if cap.text == 'Results:':
            retuDict = getTableResults(nutrients,retuDict)
        elif cap.text == 'Macronutrients:':
            retuDict = getTableResults(nutrients,retuDict)
        elif cap.text == 'Vitamins:':
            retuDict = getTableResults(nutrients,retuDict)
        elif cap.text == 'Minerals (Elements):':
            retuDict = getTableResults(nutrients,retuDict)

    retuDict = getExtraInfo(retuDict)
    
    return retuDict

def getExtraInfo(retuDict):
    retuDict['Sugars'] = 50
    retuDict['Cholesterol'] = 300

    return retuDict
    


def getTableResults(table,retuDict):
    origItems = getList()
    for items in table:
        temp = []
        for words in items:
            if not isinstance(words, str):
                temp.append(words.text)
        if temp:
            if temp[0] in origItems:
                quant = re.findall(r"[-+]?\d*\.\d+|\d+", temp[1])
                if quant:
                    retuDict[temp[0]] = float(quant[0])
            else:
                if len(temp) >= 2:
                    quant = re.findall(r"[-+]?\d*\.\d+|\d+", temp[1])
                    if quant:
                        name = resultHelper(temp[0])
                        if name:
                            retuDict[name] = float(quant[0])
                

    return retuDict
        
def resultHelper(oldName):
    if oldName == 'Total Fiber':
        name = 'Fiber'
        
    elif oldName == 'Fat':
        name = "Fatty acids"
        
    elif oldName == 'Vitamin D':
        name = "Vitamin D (D2 + D3)"
        
    elif oldName == 'Vitamin K':
        name = "Vitamin K (phylloquinone)"
        
    elif oldName == 'Pantothenic Acid':
        name = "Pantothenic acid"
        
    elif oldName == 'Vitamin B6':
        name = 'Vitamin B-6'
        
    elif oldName == 'Vitamin B12':
        name = 'Vitamin B-12'
    else:
        name = ''


    return name
        


def getList():
    totalNutrition = ['Carbohydrate', 'Sodium', 'Fatty acids', 'Fiber', 'Sugars', 'Protein', 'Calcium', 'Iron',
                      'Potassium', 'Cholesterol', 'Total lipid (fat)', 'Energy', 'Water', 'Magnesium', 'Phosphorus',
                      'Zinc', 'Copper', 'Vitamin A', 'Carotene', 'Vitamin E (alpha-tocopherol)', 'Cryptoxanthin',
                      'Lutein + zeaxanthin', 'Vitamin C', 'Thiamin', 'Riboflavin', 'Niacin', 'Vitamin B-6', 'Folate',
                      'Choline', 'Vitamin K (phylloquinone)', 'SFA 14:0', 'SFA 16:0', 'SFA 18:0', 'MUFA 18:1', 'PUFA 18:2',
                      'PUFA 18:3', 'Vitamin D (D2 + D3)','Selenium', 'Manganese', 'Vitamin E', 'Pantothenic acid',
                      'Vitamin B-12', 'Iodine', 'Biotin', 'Molybdenum', 'Chromium']
    return totalNutrition











        





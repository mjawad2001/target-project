from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from flask_login import login_required, current_user
from .models import User
from .models import Fut
from . import db
from bs4 import BeautifulSoup
import re
import mechanicalsoup
#from nutrientRequest import*
#from nutrientCal import*


auth = Blueprint('auth', __name__)




@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get("password")
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()
    print(user)
    print(password)

    if not user:
        flash("User Doesn't exist.")
        return redirect(url_for('auth.login'))
    elif user and not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))

    login_user(user, remember=remember)
    #new =User.query.filter_by(name=current_user.name).first()
    test=Fut.query.filter(Fut.user_id ==current_user.id ).all()
    print(test)
    #post = Fut(fame = family,calinfo =  con,user=current_user)
    if test== None:

        print(new.info)
        return redirect(url_for('auth.info'))
    return redirect(url_for('main.profile'))

@auth.route('/info')
def info():
    return render_template('info.html')

@auth.route('/info', methods=['POST'])
def info_post():
    family = request.form.get('faname').capitalize()
    age = request.form.get('fage')
    feet=request.form.get('ffeet')
    inches=request.form.get('finches')
    gender=request.form.get('Gender')
    Active=request.form.get('Activity')
    Weight=request.form.get("Weight")

    people =[[family ,gender, age,[feet,inches],Weight,Active]]

    nCal = nutrientRequest(people)
    nCal = nCal[family]
    #nCal = nutrientCal(nRequest)
    #print(nCal)
    
    con=str(nCal)


 
    print(family)
    print(age)
    print(feet)
    print(inches)
    print(gender)
    print(Active)
    print(Weight)
    print(con)
    #print(ch)
   # print(nCal)
    #new = User.query.filter_by(name=current_user.name).first()
    #ter=Fut(fame = family)
    #m=new.ter(family)
    post = Fut(fame = family,calinfo =  con,user=current_user)
    #post2 = Fut(calinfo = con,user=current_user)

    db.session.add(post)
  
    db.session.commit()

    kep=nCal
    
    #return redirect(url_for('auth.option',kep=kep))
    return render_template('option.html',kep=kep)

@auth.route('/option')
def option():
    return render_template('option.html') 

@auth.route('/option', methods=['POST'])
def option_post():




    return redirect(url_for('main.profile'))

@auth.route('/addmore')
def addmore():
    return redirect(url_for('auth.info')) 

@auth.route('/addmore', methods=['POST'])
def addmore_post():
    return redirect(url_for('auth.info')) 


@auth.route('/Continue')
def continu():
    return redirect(url_for('main.profile')) 
    #return render_template('profile.html',name=current_user.name, test=Fut.query.filter(Fut.user_id ==current_user.id ).all())

@auth.route('/Continue', methods=['POST'])
def Continue_post():
    return redirect(url_for('main.profile'))


@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()

    if user:
        flash('Email address already exists.')
        return redirect(url_for('auth.signup'))

    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))



@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

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

    pDict = changeNames(pDict)    
    return pDict


def changeNames(dictionary):

    dictionary["Fiber"] = dictionary.pop('Total Fiber')
    dictionary["Fatty acids"] = dictionary.pop('Fat')
    dictionary["Vitamin D (D2 + D3)"] = dictionary.pop('Vitamin D')
    dictionary["Vitamin K (phylloquinone)"] = dictionary.pop('Vitamin K')
    dictionary["Pantothenic acid"] = dictionary.pop('Pantothenic Acid')
    

    return dictionary

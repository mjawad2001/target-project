from flask import Blueprint, render_template 
from flask_login import login_required, current_user
from flask import Flask, request, render_template 
from flask import Flask, render_template, json, url_for
import os
import functools
import operator 
from pprint import pprint
from .models import User
from .models import Fut
from . import db
from bs4 import BeautifulSoup
import ast
import re



main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')
@main.route('/about')
def about():
    return render_template('about.html')



@main.route('/profile')

@login_required
def profile():
    return render_template('profile.html', name=current_user.name, test=Fut.query.filter(Fut.user_id ==current_user.id ).all(),nutri=['Carbohydrate', 'Fiber', 'Protein', 'Fatty acids','Vitamin A', 'Vitamin C', 'Vitamin D (D2 + D3)', 'Vitamin E','Vitamin K (phylloquinone)','Niacin', 'Calcium', 'Iron','Potassium','Zinc'])

@main.route('/profile', methods=["GET", "POST"])
def student():
    if request.method == "POST": 
        
        #npeople = request.form["Number"]
        #nchildren = request.form["children"]
        bbudget  = request.form["Budget"]
        numOfDItems = request.form["Iteam"]
        people = request.form.getlist("checkbox")

        check1= request.form.getlist("check1")

        nutCal = nutrientCal(people,1)
        print("--------------------------------")
        print(nutCal)

       

        

        file = open(os.path.join("/Users/mdjawad/Desktop/spring2021/research project version /version 3.5/database.json"), "r")
        data = json.load(file)

        budget = float(bbudget)
        
        


        tProtein = 70
        #numOfDItems = 2 
        
        sDic = dict(sorted(data.items(), key = lambda items: items[1][3], reverse = True))
        iList = list(sDic.items())
        kLis = list(sDic.keys())

       

        pLis = []
        cTotal = 0
        cProtein = 0

        print(type(budget))
        print(type(sDic[kLis[1]][0]))
        print(type(cTotal))
        keep=False
        skeep=False
        
        
        for i in range(len(sDic)):
            if cTotal + sDic[kLis[i]][0] <=  budget and cProtein + sDic[kLis[i]][1] <= tProtein and  sDic[kLis[i]][1] != 0:
                cTotal = cTotal + sDic[kLis[i]][0] 
                cProtein = cProtein + sDic[kLis[i]][1]    
                pLis.append(iList[i])
                #pLis.append("/")

            else:
                if cProtein == tProtein:
                    k="Got enough protein"
                    a1=str(k)
                    p=("Money Spent", cTotal)
                    a2=str(p)
                    q=("Protein", cProtein)
                    a3=str(q)
                    e=str(pLis)
                    print(type(e))
                    a4=e
                    print(pLis[0][0])
                    new =User.query.filter_by(name=current_user.name).first()
                    new.info=(new.info or "")+"////"+e
                    


                    test=Fut.query.filter(Fut.user_id ==current_user.id ).all()

                    """ for i in test:
                        print(i.fame) """
                    #f'Order number: {order.order_number}'
                    #new1 =Fut.query.filter_by(user_id=1).count()
                    #test=new1.fmember[0].fame
                    print(test,"here")
                    print(people)
                   # print(numc)
                    db.session.commit()
                  
                    a4=pLis

                    return render_template('result.html',a1=a1,a2=a2,a3=a3,a4=a4)

                    break
                
                elif cTotal + sDic[kLis[i]][0] >= budget and cProtein + sDic[kLis[i]][1] < tProtein:
                    prt=sDic[kLis[i]][0],"Not enough money","Next item if it were put in the list",cTotal + sDic[kLis[i]][0],"Money Spent", cTotal,"out of",budget,"Protein", cProtein, "out of ", tProtein,pLis
                    we=str(prt)
                    
               
                    
                    print(prt)

                    
                   
                    skeep=True
                    #print(sDic[kLis[i]][0])
                    b1="Not enough money"
                    b11=str(b1)
                    b2="Next item if it were put in the list",cTotal + sDic[kLis[i]][0]
                    b22=str(b2)
                    b3="Money Spent", cTotal,"out of",budget
                    b33=str(b3)
                    b4="Protein", cProtein, "out of ", tProtein 
                    b44=str(b4)
                    b5=str(pLis)

                    new =User.query.filter_by(name=current_user.name).first()
                   
                    new.info=(new.info or "")+"////"+ b5
                    

                   
                    db.session.commit()
                    b55=pLis
                    
                    return render_template('result1.html',b11=b11,b22=b22,b33=b33,b44=b44,b55=b55)

                    break
                      


def nutrientCal(people,timeDays):
    totalNutrition = getDict()
    for individual in people:
        individual = ast.literal_eval(individual)
        for nutrients in individual:
            totalAmount = totalNutrition[nutrients] 
            totalNutrition[nutrients] = totalAmount + individual[nutrients] * timeDays

    return totalNutrition

  


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


    

    #print(username, npeople, nchildren,budget,iteam)
    #print(type(request.form)) 
    #if keep==True:
        #return tr
    #return render_template('index.html')
    #elif skeep==True:
        
        #return  ret
    #return render_template('index.html')



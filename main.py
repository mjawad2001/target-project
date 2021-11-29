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
from collections import OrderedDict


#------
import sys
#sys.path.append('/Users/mdjawad/Desktop/research/project/main.py')
sys.path.insert(1, './target-project')
import healthAlgo
#------
#import sys
#sys.path.append('/Users/mdjawad/Desktop/research/project/nutrientCal.py')
#sys.path.insert(1, '/Users/mdjawad/Desktop/research/project/')
import nutrientCal
#------
#import sys
#sys.path.append('/Users/mdjawad/Desktop/research/project/nutrientCal.py')
#sys.path.insert(1, '/Users/mdjawad/Desktop/research/project/greedyAlgo1.py')
import budgetAlgo
import myPlateAlgo

#global mUsed
#global stimate
#global recomended
#global nutCal

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')
@main.route('/about')
def about():
    return render_template('about.html')


@main.route('/fruit')
def fruit():
    file =   file = open(os.path.join("./target-project/itemDatabase.json"), "r")
    itemData = json.load(file)


    file =   file = open(os.path.join("./target-project/indexDatabase.json"), "r")
    indexData = json.load(file)

    temp=[]
    for i in indexData['Fruits']:
        temp.append(itemData[i])
        

    return render_template('fruit.html',temp=temp)

@main.route('/protein')
def protein():
    file =   file = open(os.path.join("./target-project/itemDatabase.json"), "r")
    itemData = json.load(file)
    

    file =   file = open(os.path.join("./target-project/indexDatabase.json"), "r")
    indexData = json.load(file) 

    temp=[]
    for i in indexData['Protein']:
        temp.append(itemData[i])

    return render_template('protien.html',temp=temp)

@main.route('/vegetables')
def vegetables():
    file =   file = open(os.path.join("./target-project/itemDatabase.json"), "r")
    itemData = json.load(file)
    

    file =   file = open(os.path.join("./target-project/indexDatabase.json"), "r")
    indexData = json.load(file) 

    temp=[]
    for i in indexData['Vegetable']:
        temp.append(itemData[i])

    return render_template('vegetables.html',temp=temp)

@main.route('/grain')
def grain():
    file =   file = open(os.path.join("./target-project/itemDatabase.json"), "r")
    itemData = json.load(file)
    

    file =   file = open(os.path.join("./target-project/indexDatabase.json"), "r")
    indexData = json.load(file) 

    temp=[]
    for i in indexData['Grains']:
        temp.append(itemData[i])
    return render_template('grain.html',temp=temp)

@main.route('/profile')

@login_required
def profile():
    return render_template('profile.html', name=current_user.name, test=Fut.query.filter(Fut.user_id ==current_user.id ).all(),nutri=['Carbohydrate', 'Fiber', 'Protein', 'Fatty acids','Vitamin A', 'Vitamin C', 'Vitamin D (D2 + D3)', 'Vitamin E','Vitamin K (phylloquinone)','Niacin', 'Calcium', 'Iron','Potassium','Zinc'])

@main.route('/profile', methods=["GET", "POST"])
def student():
    if request.method == "POST": 
      
        repItem = request.form["max"]
        budget  = request.form["Budget"]
        time = request.form["Iteam"]
        
        people = request.form.getlist("checkbox")

        inputLis= request.form.getlist("check1")
        
        algo0 = request.form['options']

        print("------------------------")
        print(people)
        nutCal = nutrientCal.nutrientCal(people,int(time))
        print("------------------------")
        print(nutCal)
       
        
        if algo0 == 'low':
            
            sReturn = budgetAlgo.budgetAlgo(int(budget),nutCal,inputLis,int(repItem))
            recomended = sReturn[0]#rec index 0 = items needed
            mUsed =  sReturn[1] #rec index 1 = sublist
            gSearch =  sReturn[2]
            stimate =  sReturn[3]
            mUsed=[round( mUsed[0],2),round( mUsed[1],2),round( mUsed[2],2)]


            if gSearch == "green":
                return render_template('result.html',mUsed=mUsed,stimate=stimate,recomended=recomended,nutCal=nutCal)

        
            elif gSearch == "orange":
                return render_template('result1.html',mUsed=mUsed,stimate=stimate,recomended=recomended,nutCal=nutCal)

                #print("not enough")
                #print(mUsed)
            ##        print(len(recomended))
            ##      
            elif gSearch == "red":
                return render_template('result1.html',mUsed=mUsed,stimate=stimate,recomended=recomended,nutCal=nutCal)
            
         
        

        elif algo0 == 'mid':
            mPCat = ["Protein","Vegetable","Fruits","Grains",'Dairy']
            sReturn = myPlateAlgo.myPlateAlgo(int(budget),nutCal,inputLis,int(repItem),mPCat)
            recomended = sReturn[0]#rec index 0 = items needed
            mUsed =  sReturn[1] #rec index 1 = sublist
            gSearch =  sReturn[2]
            stimate =  sReturn[3]
            mUsed=[round( mUsed[0],2),round( mUsed[1],2),round( mUsed[2],2)]
            print("***********")
            print(recomended )
            if gSearch == "green":
                return render_template('result.html',mUsed=mUsed,stimate=stimate,recomended=recomended,nutCal=nutCal)

        
            elif gSearch == "orange":
                return render_template('result1.html',mUsed=mUsed,stimate=stimate,recomended=recomended,nutCal=nutCal)

                #print("not enough")
                #print(mUsed)
            ##        print(len(recomended))
            ##      
            elif gSearch == "red":
                return render_template('result1.html',mUsed=mUsed,stimate=stimate,recomended=recomended,nutCal=nutCal)
            
         
        else:
            mPCat = ["Protein","Vegetable","Fruits","Grains",'Dairy']
            sReturn = healthAlgo.healthAlgo(int(budget),nutCal,inputLis,int(repItem),mPCat)
            recomended = sReturn[0]#rec index 0 = items needed
            mUsed =  sReturn[1] #rec index 1 = sublist
            gSearch =  sReturn[2]
            stimate =  sReturn[3]
            mUsed=[round( mUsed[0],2),round( mUsed[1],2),round( mUsed[2],2)]

            if gSearch == "green":
                return render_template('result.html',mUsed=mUsed,stimate=stimate,recomended=recomended,nutCal=nutCal)

        
            elif gSearch == "orange":
                return render_template('result1.html',mUsed=mUsed,stimate=stimate,recomended=recomended,nutCal=nutCal)

                #print("not enough")
                #print(mUsed)
            ##        print(len(recomended))
            ##      
            elif gSearch == "red":
                return render_template('result1.html',mUsed=mUsed,stimate=stimate,recomended=recomended,nutCal=nutCal)
            
         

#@main.route('/test')
#def test():
    #mUsed,stimate,recomended,nutCal = student()
    #return render_template('test.html',mUsed=mUsed,stimate=stimate,recomended=recomended,nutCal=nutCal) 















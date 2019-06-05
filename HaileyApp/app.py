# -*- coding: UTF-8 -*-
#Author: Tjeerd van der Veen
#Date: 4-6-2019
#Funcionality: Rendering the webpage and sending the correct pages to the user as well as collecting data to be displayed on the webpage.

from flask import Flask, render_template, request, redirect, jsonify
import subprocess
import json
import sys
import os
import time

app = Flask(__name__)

@app.route('/')
def index():
    """
    This function sends the HTML template for the home page to the user.
    """
    return render_template('index.html')
    
@app.route('/about')
def team():
    """
    This function opens and reads files containing the names, compounds and diseases used
    for datamining. These names are saved as lists and given to the about page which is
    then send to the user.
    """
    gourd_names = open("/home/vmadmin/ProjectCourse8/HaileyBackEnd/names.txt", "r", encoding="ISO-8859-1").readlines()
    compound_names = open("/home/vmadmin/ProjectCourse8/HaileyBackEnd/compounds.txt", "r", encoding="ISO-8859-1").readlines()
    disease_names = open("/home/vmadmin/ProjectCourse8/HaileyBackEnd/diseases.txt", "r", encoding="ISO-8859-1").readlines()
    return render_template('about.html', gourd_names=(gourd_names), compound_names=(compound_names), disease_names=(disease_names))
    
@app.route('/database')
def database():
    """
    This function sends the HTML template for the database page to the user. 
    It retrieves the time the database is last updated and sets it to be readable by the user and gives the readable date to the HTML template.
    """
    modTimesinceEpoc = os.path.getmtime("/home/vmadmin/ProjectCourse8/HaileyBackEnd/text_mining_results.json")
    modificationTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(modTimesinceEpoc))
    return render_template('database.html', last_updated=modificationTime)
    
#background process happening without any refreshing
@app.route('/background_process')
def background_process():
    """
    This function starts the text mining application as a subprocess so the user can keep using
    the site while the database is being updated.
    """
    subprocess.Popen(["sudo python3.7 /home/vmadmin/ProjectCourse8/HaileyBackEnd/webapp.py > out.txt"], shell=True,
             stdin=None, stdout=None, stderr=None, close_fds=True)
    return "nothing"
    
@app.route('/application')
def application():
    """
    This function sends the HTML template for the application page.
    """
    return render_template('application.html')

def read_json():
    """
    This function opens and reads the database (Json file) and returns the data stored in it 
    as a dictionary.
    """
    with open("/home/vmadmin/ProjectCourse8/HaileyBackEnd/text_mining_results.json") as json_file:
        data = json.load(json_file)
    return data


@app.route('/resultaten', methods=['GET', 'POST'])
def resultaten():
    """
    This function imports variables from javascript and gives it to the application_results page
    if at least 2 arguments for it are given, if they are not given it will redirect the user
    to the application page.
    """
    try: 
        if request.method == 'POST':
            words = request.form["words"]
            disease = words.split(",")[1].strip("\"")
            compound = words.split(",")[2].strip("]}\"")    
            return render_template("application_result.html", results=read_json(), compound=compound, disease=disease)
    except IndexError:
        return render_template('application.html')

if __name__ == '__main__':
    """
    Runs the application if it's set up correctly.
    """
    app.run(host="0.0.0.0", port=80)

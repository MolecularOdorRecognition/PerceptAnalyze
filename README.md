# PerceptAnalyze

This Repo focusses on Data Extraction and Network Analysis using Google 2 gram Dataset

Google N-gram dataset link http://storage.googleapis.com/books/ngrams/books/datasetsv2.html

# Requirements 
# NOTE (Your files and code should be in the same folder or place)
Python Installed on PC preferably(Python 3.5 or Python 3)

Two .csv perceptual data files for example here they are flavornetPercepts.csv & superscentPercepts.csv

# For Python 2.7
Change urllib.request to urllib everywhere in the program

Remove encoding="utf8" everywhere in the program

# For running script.py (Data extraction)

Open Command Prompt

cd to the loaction of code and flavornetPercepts.csv , superscentPercepts.csv files

type "python script.py"

THE CODE WILL START

The errors and information will be logged in sample.log file which will be automatically created in the same folder

The final output in JSON format for flavornetPercepts will be in json.txt and for superscentPercepts will be in newjson.txt

# For running graph.py (Data Analysis)

Run this after running script.py

Additional Requirements/Dependecies

pip install networkx
Two .csv perceptualEdges files i.e in this case edgesFlav.csv and edgesSuperSc.csv 



Open Command Prompt

cd to the loaction of code and PerceptualEdges files

type "python graph.py"

THE CODE WILL START

The final output similarity comparing Superscent and Flavournet will be printed on screen 



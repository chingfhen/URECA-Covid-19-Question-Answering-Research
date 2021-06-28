# CONTAINS CONSTANTS USED IN THE COVID QA SYSTEM


# username and password for elastic search authentication 
AUTH = {'username':'CovidQASystem',                                   
        'password':'Tan978775'}

# name of the elastic search index that stores the data
INDEX_NAME = "covid_datastore"

# Folder containing covid 19 related text files
RAW_TEXT_FOLDER = r"C:\Users\tanch\Documents\GitHub\Covid-19-QA-System\Raw Data"


MODEL_NAME = 'deepset/roberta-base-squad2'

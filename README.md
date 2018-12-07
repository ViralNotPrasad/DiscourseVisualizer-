# Agree2Disagree

## Developers - 
Dhruva Sahasrabudhe - https://www.github.com/sahasradude

Viral Pasad - https://www.github.com/viralnotprasad

## Data collection pipeline dependencies:

* python3
* nltk
* wordnet
* praw
* pandas
* sklearn

## System dependencies:

* python3
* flask
* numpy


## Instructions to Run:
To run the system, first ensure all dependences are met
then, navigate to the flask folder, and run: 

python3 hello.py

to start the server on the localhost
127.0.0.1:5000


## What each file does:

### Web Application-
* flask/app.py - Main logic of the front end flask web application,
which handles routing, loading data from pickled dictionary *finaldict.pickle*, time logging, 
and data collection about user clicks, etc.

* flask/templates/* - Contains the html code for the pages

* flask/static/* - contains the static images, and the css files

### Data collection - 
* collect_data.py - Collects top posts from r/changemyview using PRAW 
* process_json.py - Collects and processes json data from the r/changemyview dataset provided by Tan et. al.
in *Winning Arguments: Interaction Dynamics and Persuasion Strategies in Good-faith Online Discussions
Chenhao Tan, Vlad Niculae, Cristian Danescu-Niculescu-Mizil, Lillian Lee.*
Dataset available at https://chenhaot.com/pages/changemyview.html

*(Note: Datasets will be stored as data\_(current day)\_(current hour)\_(current minute).pickle) according to the time that they are generated*

### Data processing - 
* segregate_data.py - Provides the bulk of the data processing functionality. 
* classify_opinion.py - Uses the paralleldots api to try topic modelling, sentiment, intent, emotional
analysts, etc. (not used in project, as classification is done manually)
* stats_data.py - Loads the pickle file and finds out statistics about the 
* flask/analytics.py - Generates corpus level statistics about the data collected, along with relevance labels
* flask/exit_processing.py - Conducts analytics on the time/interaction data which was collected
during the user interaction phase, and the entry form results (stored as form_result.pickle).


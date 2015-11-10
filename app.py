### IMPORTS #############################################

import random
import re
from flask import Flask, render_template, request, redirect, url_for, flash
from twython import Twython, TwythonError #may not need this at all
import psycopg2
import urlparse

### FLASK SETUP  ########################################

app = Flask(__name__, static_folder='static',static_url_path='/static')
app.config['DEBUG'] = True
app.config['TRAP_BAD_REQUEST_ERRORS'] = True

### DATABASE CONNECTION ################################

urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ["DATABASE_URL"])

### database heroku
con = None
try:

	con = psycopg2.connect(
	    database=url.path[1:],
	    user=url.username,
	    password=url.password,
	    host=url.hostname,
	    port=url.port
	)
	cur = con.cursor()
except psycopg2.DatabaseError, e:
	if con:
		con.rollback()
	print 'Error %s' % e


### FUNCTIONS ##########################################

def fetchName():

	cur.execute("SELECT * FROM bwords ORDER BY RANDOM() LIMIT 1;")
	rows = cur.fetchall()
	fetchedB = rows[0][1]
	

	cur.execute("SELECT * FROM cwords ORDER BY RANDOM() LIMIT 1;")
	rows = cur.fetchall()
	fetchedC = rows[0][1]

	nameReturn = [fetchedB,fetchedC]
	return nameReturn

def makeName():
	yerp = fetchName()
	sendName = []

	cEndings = ['batch','ball','buff','butt','brute','boff']
	bEndings = ['dict','tich','chip','lip','rip','trip','sip']

	bW = yerp[0].capitalize() + random.choice(bEndings)
	cW = yerp[1].capitalize() + random.choice(cEndings)

	sendName.append(bW)
	sendName.append(cW)

	return sendName


### ROUTES ################################################

@app.route("/",methods=['GET','POST'])

def main():
	finalName = makeName()
	firstName = finalName[0]
	lastName = finalName[1]
	return render_template('display.html',firstName=firstName, lastName=lastName)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

### RUN IT ####################################################################

if __name__ == '__main__': 
    app.run()
from flask import Flask, render_template, request
from sklearn.externals import joblib
import datetime as dt
import pandas as pd
import xgboost as xgb
import numpy as np

app = Flask(__name__)

model = joblib.load("Models/rf_regressor.pkl")

@app.route("/")
def home():
    return render_template('index.html')

@app.route('/', methods = ['POST'])
def main():
    if request.method == 'POST':
        fName = request.form['fName'] 
        lName = request.form['lName']  
        source = request.form['source']  
        destination = request.form['destination']  
        doj = pd.to_datetime(request.form['doj'], format = "%Y-%m-%d") 
        dTime = request.form['dTime']  
        duration = request.form['duration'] 
        carrier = request.form['carrier']   
        nStops = request.form['nStops'] 

        # Monday = 0

        # Model Variables.
        Total_Stops = nStops
        Date = doj.day
        Month = doj.month
        M = 0
        Sa = 0
        Su = 0
        Th = 0
        Tu = 0
        W = 0
        Dep_hrs = int(dTime.strip(':')[:2])
        Dep_min = int(dTime.strip(':')[3:])
        No_info = 1
        Duration_min = (int(duration.strip(':')[:2]))*60 + int(duration.strip(':')[3:])
        src__Chennai = 0
        src__Delhi = 0
        src__Kolkata = 0 
        src__Mumbai = 0
        dest__Cochin = 0
        dest__Delhi = 0
        dest__Hyderabad = 0
        dest__Kolkata = 0
        Air_India = 0
        IndiGo = 0
        Jet_Airways = 0
        Multiple_carriers = 0 # ye miss kara dropdown mein
        SpiceJet = 0
        Vistara = 0 
        other_flight = 0


        if (doj.weekday() == 0):
            M = 1
        elif (doj.weekday() == 1):
            Tu = 1
        elif (doj.weekday() == 2):
            W = 1
        elif (doj.weekday() == 3):
            Th = 1
        elif (doj.weekday() == 5):
            Sa = 1
        elif (doj.weekday() == 6):
            Su = 1

        if (source == 'Chennai'):
            src__Chennai = 1
        elif(source == 'Delhi'):
            src__Delhi = 1
        elif(source == 'Kolkata'):
            src__Kolkata = 1
        elif(source == 'Mumbai'):
            src__Mumbai = 1

        if (destination == 'Cochin'):
            dest__Cochin = 1
        elif (destination == 'Delhi'):
            dest__Delhi = 1
        elif (destination == 'Hyderabad'):
            dest__Hyderabad = 1
        elif (destination == 'Kolkata'):
            dest__Kolkata = 1

        if (carrier == 'Air India'):
            Air_India = 1
        elif (carrier == 'IndiGo'):
            IndiGo = 1
        elif (carrier == 'Jet Airways'):
            Jet_Airways = 1
        elif (carrier == 'SpiceJet'):
            SpiceJet = 1
        elif (carrier == 'Vistara'):
            Vistara = 1
        elif (carrier == 'Other'):
            other_flight = 1

        X = pd.DataFrame({
            'Total_Stops' : [nStops],
            'Date' : [Date],
            'Month' : [Month],
            'M' : [M],
            'Sa' : [Sa],
            'Su' : [Su],
            'Th' : [Th],
            'Tu' : [Tu],
            'W': [W],
            'Dep_hrs' : [Dep_hrs],
            'Dep_min' : [Dep_min],
            'No_info' : [No_info],
            'Duration_min' : [Duration_min],
            'src__Chennai' : [src__Chennai],
            'src__Delhi' : [src__Delhi],
            'src__Kolkata' : [src__Kolkata],
            'src__Mumbai' : [src__Mumbai],
            'dest__Cochin' : [dest__Cochin],
            'dest__Delhi' : [dest__Delhi],
            'dest__Hyderabad' : [dest__Hyderabad],
            'dest__Kolkata' : [dest__Kolkata],
            'Air_India' : [Air_India],
            'IndiGo' : [IndiGo],
            'Jet_Airways' : [Jet_Airways],
            'SpiceJet' : [SpiceJet],
            'Vistara' : [Vistara], 
            'other_flight' : [other_flight],
            'Other' : [0],
            'Multiple_carriers' : [0]
        })

        prediction = model.predict(X)

    return render_template("result.html", prediction = np.round(prediction[0], 3), fName = fName, lName = lName)

if __name__ == "__main__":
    app.run(debug = True)
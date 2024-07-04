from flask import Flask,request,jsonify,render_template
from flask import url_for
import pickle,csv
import numpy as np
import pandas as pd
import smtplib
from email.message import EmailMessage
columns=['gender', 'SeniorCitizen', 'Partner', 'Dependents', 'PhoneService', 'MultipleLines', 'InternetService', 'OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies', 'Contract', 'PaperlessBilling', 'PaymentMethod']
#Create Flask apps
app=Flask(__name__)
##Load pickle model
model=pickle.load(open("DecisionTree.pkl","rb"))
encoder=pickle.load(open("encoder.pkl","rb"))
@app.route("/")
def index():
    return render_template('index.html')


@app.route('/predict',methods=["POST"])
def predict():
    if request.method=="POST":
        Gender=request.form["Gender"]
        SeniorCitizen=request.form["SeniorCitizen"]
        Partner=request.form["Partner"]
        Dependents=request.form["Dependents"]
        tenur=int(request.form["tenur"])
        PhoneService=request.form["PhoneService"]
        MultipleLines=request.form["MultipleLines"]
        InternetService=request.form["InternetService"]
        OnlineSecurity=request.form["OnlineSecurity"]
        OnlineBackup=request.form["OnlineBackup"]
        DeviceProtection=request.form["DeviceProtection"]
        TechSupport=request.form["TechSupport"]
        StreamingTV=request.form["StreamingTV"]
        StreamingMovies=request.form["StreamingMovies"]
        Contract=request.form["Contract"]
        PaperlessBilling=request.form["PaperlessBilling"]
        PaymentMethod=request.form["PaymentMethod"]
        MonthlyCharges=float(request.form["MonthlyCharges"])
        TotalCharges=float(request.form["TotalCharges"])
        recipient=request.form["r_emails"]
        list_request=[Gender,SeniorCitizen,Partner,Dependents,tenur,PhoneService,MultipleLines,InternetService,OnlineSecurity,OnlineBackup,DeviceProtection,TechSupport,StreamingTV,StreamingMovies,Contract,PaperlessBilling,PaymentMethod]
        float_list=[MonthlyCharges,TotalCharges]
        
        features=[int(x) for x in  list_request]
        floats=[float(x) for x in  float_list]
        for i in floats:
         features.append(i)
        
        prediction=model.predict([features])
        for j in prediction:
           features.append(j)
        if prediction[0]==float(0):
           churn="Thanks for your participation!"
           
        else:
           churn="Congradulations! You got 20 percent discount"
        ########################################################################################################
        subject = "!!!!!!تخفیف ویژه "
        body = "ما این فصل را با یک فروش ویژه فقط برای شما جشن می گیریم! از تخفیف تا ۴۰٪ در همه محصولات ما برخوردار شوید. عجله کنید، فروش به زودی به پایان می رسد"
        sender = "sabaabaszade3@gmail.com"
        password = "daxvfurlcrgfydpe"
        server = smtplib.SMTP("smtp.gmail.com" , 587)
        server.starttls()

        server.login(sender,password)
        user_input_mail = recipient

        email=EmailMessage()
        email['From'] = sender
        email['To'] = user_input_mail
        email['Subject'] = subject
        email.set_content(body)
        server.send_message(email)
        ######################################################################################################
        # name of csv file
        fieldnames=['gender', 'SeniorCitizen', 'Partner', 'Dependents', 'tenure',
       'PhoneService', 'MultipleLines', 'InternetService', 'OnlineSecurity',
       'OnlineBackup', 'DeviceProtection', 'TechSupport', 'StreamingTV',
       'StreamingMovies', 'Contract', 'PaperlessBilling', 'PaymentMethod',
       'MonthlyCharges', 'TotalCharges', 'Churn']
        new_results = "Datasfromurl.csv"
        # writing to csv file
        # opening the csv file in 'a+' mode
        file = open("Datasfromurl.csv", 'a+', newline ='')
 
        
        with file:    
          write = csv.writer(file)
          write.writerows([features])
        return render_template('index.html',prediction_text='Price of House will be Rs. {}'.format(churn))
       
if __name__=="__main__":
   app.run(debug=True)

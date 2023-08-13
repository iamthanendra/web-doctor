from flask import Flask, render_template, request, send_file, Response,  redirect, url_for

from db_work import insert_doctor
from db_work import check_email_exist_or_not
from db_work import check_email_exist_or_not_patient
from db_work import insert_patient
from db_work import doctor_authentication
from db_work import patient_authentication
from db_work import load_all_patient_data
from db_work import retrive_doctor_list
from db_work import get_patient_history
from db_work import check_all_patient_list
from db_work import generate_report_data

from predict_health import predict_client_health

#For Extracting Resume
"""
from pyresparser import ResumeParser

from resume_parser import pdf_reader


from db_work import insert_data
from db_work import load_graduation
from db_work import load_all_data
from db_work import load_training
from db_work import load_certificate
from db_work import load_experience
from db_work import load_user_level
from db_work import load_skills_data
from db_work import apply_filter_and_search
from db_work import create_compare_list
# from db_work import recommendation_system
from recommendation import recommendation_system1

from MyPlots import generated_graphs
from MyPlots import generated_user_dropdown

import base64, random


import time, datetime
"""

#Session Tracking
from flask_session import Session
from flask import session

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
def index():
    # return "Hello"
    return render_template("index.html", result=False)

@app.route("/doctor-auth")
def doctor_auth():
    # return "Hello"
    return render_template("doctor-login.html", result=False)

@app.route("/doctor-registration")
def doctor_registration():
    # return "Hello"
    return render_template("doctor-resister.html")

# @app.route("/doctor-registration")
# def doctor_registration():
#     # return "Hello"
#     return render_template("doctor-create.html", result=False)

@app.route("/patient-auth")
def patient_auth():
    # return "Hello"
    return render_template("patient-login.html", result=False)

@app.route("/patient-registration")
def patient_registration():
    # return "Hello"
    return render_template("patient-registration.html", result=False)

@app.route("/doctors")
def doctors():
    # return "Hello"
    if not session.get("doctor_email"):
        return redirect("/doctor-auth")
    return render_template("doctors-page.html", result=False)

@app.route("/check-health-pateint")
def check_health():
    #Checking Patient is Authurised or not
    if not session.get("patient_email"):
        return redirect("/patient-auth")

    #Getting Patient Id    
    id = session.get("patient_id")

    #Retriving doctor list from database
    data = retrive_doctor_list()
    print("###############################################\n"*12,data)
    
    return render_template("check-health-pateint.html", result = False, data=data)

@app.route("/Check-All-Patient-List")
def check_all_patient():
    #Checking Patient is Authurised or not
    if not session.get("doctor_email"):
        return redirect("/doctor-auth")

    #Getting Patient Id    
    doctor_id = session.get("doctor_id")
    data = check_all_patient_list(doctor_id)
    return render_template("check_all_patient_list.html", data=data)

@app.route("/Check-Patient-List")
def check_patient_list():
    #Checking Patient is Authurised or not
    if not session.get("doctor_email"):
        return redirect("/doctor-auth")

    #Getting Patient Id    
    doctor_id = session.get("doctor_id")
    data = check_patient_list(doctor_id)
    return render_template("Check-Patient-List.html", data=data)

@app.route("/Gererate-Report")
def generate_report():
    #Checking Patient is Authurised or not
    if not session.get("patient_email"):
        return redirect("/patient-auth")

    #Getting Patient Id    
    patient_id = session.get("patient_id")
    patient_name, age, sex, weight, blood_group, tel, symptoms, diseases, doctor_name = generate_report_data(patient_id)
    return render_template("generate-report.html", patient_name=patient_name, age=age, sex=sex, weight=weight, blood_group=blood_group, tel=tel, symptoms=symptoms, diseases=diseases, doctor_name=doctor_name)

@app.route("/logout-doctors")
def logout_doctors():
    # return "Hello"
    session["doctor_email"] = None
    return redirect("/doctor-auth")
    # return render_template("doctors-page.html", result=False)

@app.route("/prediction", methods=["GET", "POST"])
def prediction():
    #
    if not session.get("patient_email"):
        return redirect("/patient-auth")
    
    return render_template("prediction.html")

@app.route("/patient-history", methods=["GET", "POST"])
def patient_history():

    if not session.get("patient_email"):
        return redirect("/patient-auth")
    
    #Getting Patient Id
    patient_id = session.get("patient_id")

    data = get_patient_history(patient_id)

    
    return render_template("patient-history.html", data=data)

@app.route("/predict", methods=["GET", "POST"])
def predict():
    #
    if not session.get("patient_email"):
        return redirect("/patient-auth")
    
    if request.method == "POST":
        #Getting Symptoms List
        print(request.form.getlist('symptoms'))
        symptoms = request.form.getlist('symptoms')
        print("Symptoms are ", symptoms)

        #Getting Patient Id
        patient_id = session.get("patient_id")

        #Getting Doctor Id
        doctor_id = request.form["doctor_list"]

        #Predicting
        output, summary1 = predict_client_health(patient_id, doctor_id, symptoms)

        # return mylist, summary1, summary2
        return render_template("prediction.html", mylist=output, summary1=summary1)
    return "invalid enter"


@app.route("/patients")
def patients():
    # If Session will be expired
    if not session.get("patient_email"):
        return redirect("/patient-auth")
    id = session.get("patient_id")
    username, email, dob, gender, weight, tel = load_all_patient_data(id)
    return render_template("patient-page.html", result=False, username=username, email=email, dob=dob, gender=gender, weight=weight, tel=tel)

@app.route("/logout-patients")
def logout_patients():
    # return "Hello"
    session["patient_email"] = None
    return redirect("/patient-auth")
    # return render_template("doctors-page.html", result=False)

# @app.route("/patients")
# def patients():
#     # return "Hello"
#     if not session.get("patient_email"):
#         return redirect("/patient-auth")
#     return render_template("patient-page.html", result=False)

# @app.route("/patients")
# def patients():
#     # return "Hello"
#     if not session.get("patient_email"):
#         return redirect("/patient-auth")
#     return render_template("patient-page.html", result=False)


@app.route("/authenticate-doctor", methods=["GET", "POST"])
def authenticate_doctor():
    email = request.form["email"]
    password = request.form["password"]
    is_doctor_authenticated, user, id = doctor_authentication(email, password)
    if is_doctor_authenticated:
        #If Verified then redirect

        #Storing in session
        session["doctor_username"] = user
        session["doctor_email"] = email
        session["doctor_id"] = id

        return redirect(url_for('doctors'))
        # return render_template("doctors-page.html", username=user)
    else:
        #Failed
        return render_template("doctor-auth.html", result=True)
    
@app.route("/authenticate-patient", methods=["GET", "POST"])
def authenticate_patient():
    email = request.form["email"]
    password = request.form["password"]
    is_doctor_authenticated, user, id = patient_authentication(email, password)
    if is_doctor_authenticated:
        #If Verified then redirect
        # return redirect(url_for('doctors', username=user))

        #Storing in session
        session["patient_email"] = email
        session["patient_username"] = user
        session["patient_id"] = id

        return redirect(url_for('patients'))
        # return render_template("patient-page.html", username=user)
    else:
        #Failed
        return render_template("patient-auth.html", result=True)

@app.route("/create-doctor", methods=["POST", "GET"])
def create_doctor():
    if request.method == "POST":

        #Getting All Form data
        username = request.form['username']
        email = request.form['email']
        dob = request.form['dob']
        gender = request.form['gender']
        specialization = request.form['specialization']
        tel = request.form['tel']
        reg_no = request.form['reg_no']
        qualification = request.form['qualification']
        password = request.form['password']

        #Getting password Encryptor
        global bcrypt

        #Checking Email Id or Registration Id is exist or not
        is_created = check_email_exist_or_not(email, reg_no)
        if not is_created : #If not exist
            insert_doctor(username, email, dob, gender, specialization, tel, reg_no, qualification, password)
        else: #If exist
            return render_template("doctor-create.html", result=True, msg="This registration no/email is already Registed")
        
        return render_template("doctor-create.html", result=True, msg="Id Created Successfully")

@app.route("/create-patient", methods=["POST", "GET"])
def create_patient():
    if request.method == "POST":

        #Getting All Form data
        name = request.form['name']
        email = request.form['email']
        dob = request.form['dob']
        gender = request.form['gender']
        weight = request.form["weight"]
        no_of_pregnancy = request.form["pregnancy"]
        blood_group = request.form["blood_group"]
        p_h_issue = request.form['p_h_issue']
        address = request.form['address']
        tel = request.form['tel']
        password = request.form['password']

        #Checking Email Id is exist or not
        is_created = check_email_exist_or_not_patient(email)
        if not is_created : #If not exist
            insert_patient(name, email, dob, gender, weight, no_of_pregnancy, blood_group, p_h_issue, address, tel, password)
        else: #If exist
            return render_template("patient-registration.html", result=True, msg="This email is already Registed")
        
        return render_template("patient-registration.html", result=True, msg="Id Created Successfully")


if __name__ == '__main__':
    app.run(debug=True)

# import streamlit as st
# import nltk
# import spacy
# nltk.download('stopwords')
# spacy.load('en_core_web_sm')

# import pandas as pd
# import base64, random
# import time, datetime
# from pyresparser import ResumeParser
# from pdfminer3.layout import LAParams, LTTextBox
# from pdfminer3.pdfpage import PDFPage
# from pdfminer3.pdfinterp import PDFResourceManager
# from pdfminer3.pdfinterp import PDFPageInterpreter
# from pdfminer3.converter import TextConverter
# import io, random
# from streamlit_tags import st_tags
# from PIL import Image
import pymysql
import random
import database_credentials
import datetime

# from Courses import ds_course, web_course, android_course, ios_course, uiux_course, resume_videos, interview_videos
# import pafy
# import plotly.express as px
# import youtube_dl

# import html

#Table Data
data_table_sheet = None

#Creating Connection
# connection = pymysql.connect(host='localhost',port=3306, user='root', password='', db='ai_doctor')
connection = pymysql.connect(host=database_credentials.host, port=database_credentials.port_code, user=database_credentials.user, password=database_credentials.password, db=database_credentials.database_name)
cursor = connection.cursor()

# Create the DB
db_sql = """CREATE DATABASE IF NOT EXISTS ai_doctor;"""
cursor.execute(db_sql)
connection.select_db("ai_doctor")

# Create Doctor table
DB_table_name = 'doctor_data'
table_sql = "CREATE TABLE IF NOT EXISTS " + DB_table_name + """
                    ( join_id INT AUTO_INCREMENT,
                      username varchar(50) NOT NULL,
                      generated_id varchar(30) NOT NULL,
                      email VARCHAR(50) NOT NULL,
                      dob VARCHAR(15) not null,
                      gender VARCHAR(8) not null,
                      specialization VARCHAR(20) not null,
                      tel VARCHAR(15) not null,
                      reg_no VARCHAR(25) not null,
                      qualification VARCHAR(10) NOT NULL,
                      password VARCHAR(20) NOT NULL,
                      PRIMARY KEY (join_id));
                    """

cursor.execute(table_sql)

# Create table
DB_table_name = 'patient_data'
table_sql = "CREATE TABLE IF NOT EXISTS " + DB_table_name + """
                    ( id INT AUTO_INCREMENT,
                      username varchar(50) NOT NULL,
                      email VARCHAR(50) NOT NULL,
                      generated_id varchar(30) NOT NULL,
                      dob VARCHAR(15) not null,
                      gender VARCHAR(8) not null,
                      weight int not null,
                      no_of_pregnancy int,
                      blood_group varchar(5),
                      p_h_issue varchar(50),
                      address varchar(80),
                      tel VARCHAR(15) not null,
                      password VARCHAR(20) NOT NULL,
                      PRIMARY KEY (id));
                    """

                    
cursor.execute(table_sql)

# Create table
DB_table_name = 'patient_history'
table_sql = "CREATE TABLE IF NOT EXISTS " + DB_table_name + """
                    ( 
                      patient_id int ,
                      symptoms varchar(50) NOT NULL,
                      diseases varchar(50),
                      doctor_id int,
                      timestamp varchar(30) NOT NULL
                      );
                    """

                    
cursor.execute(table_sql)


def insert_doctor(username, email, dob, gender, specialization, tel, reg_no, qualification, password):
  insert_data = "INSERT INTO doctor_data (username, email, generated_id, dob, gender, specialization, tel, reg_no, qualification, password ) " + """
                  VALUES (
                        %s, 
                        %s, 
                        %s,
                        %s, 
                        %s, 
                        %s, 
                        %s, 
                        %s, 
                        %s, 
                        %s
                        )"""
  
  generated_random_value = random.randint(100000000000000000000000000000, 999999999999999999999999999999)
  
  rec_values = (
    str(username), str(email),str(generated_random_value), str(dob), str(gender),  str(specialization), str(tel), str(reg_no), str(qualification), str(password)
    )
  cursor.execute(insert_data, rec_values)
  connection.commit()

def check_email_exist_or_not(email, reg_no):
  
  cursor.execute("SELECT email FROM doctor_data where email ='"+email+"' or reg_no = '"+reg_no+"'")
  data = cursor.fetchall()

  counter = 0
  for row in data:
    counter += 1
  
  if counter >= 1:
    return True # Email Already Exist
  else :
    return False # Email Not Exist

def check_email_exist_or_not_patient(email):
  cursor.execute("SELECT email FROM patient_data where email ='"+email+"'")
  data = cursor.fetchall()
  counter = 0
  for row in data:
    counter += 1
  
  if counter >= 1:
    return True # Email Already Exist
  else :
    return False # Email Not Exist

# def insert_patient(name, email, dob, gender, weight, tel, password):
def insert_patient(name, email, dob, gender, weight, no_of_pregnancy, blood_group, p_h_issue, address, tel, password):
  insert_data = "INSERT INTO patient_data (username, email, generated_id, dob, gender, weight, no_of_pregnancy, blood_group, p_h_issue, address, tel, password ) " + """
                  VALUES (
                        %s, 
                        %s, 
                        %s,
                        %s, 
                        %s, 
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s, 
                        %s
                        )"""
  generated_random_value = random.randint(100000000000000000000000000000, 999999999999999999999999999999)
  rec_values = (
    str(name), str(email),str(generated_random_value), str(dob), str(gender), int(weight), no_of_pregnancy, str(blood_group), str(p_h_issue), str(address), str(tel), str(password)
    )
  cursor.execute(insert_data, rec_values)
  connection.commit()

def doctor_authentication(email, password):
  #Checking User Exist in database or not
  verification_query = "Select username, email, join_id from doctor_data where email = %s and password = %s"
  credential = (str(email), str(password))
  cursor.execute(verification_query, credential)
  data = cursor.fetchall()

  is_exist = False 

  username = "Guest"
  id = -1
  for row in data:
    username = row[0]
    id = row[2]
    is_exist = True
  
  return is_exist, username, id

def patient_authentication(email, password):
  #Checking User Exist in database or not
  verification_query = "Select username, email, id from patient_data where email = %s and password = %s"
  credential = (str(email), str(password))
  cursor.execute(verification_query, credential)
  data = cursor.fetchall()

  is_exist = False 

  username = "Guest"
  id = -1
  for row in data:
    username = row[0]
    id = row[2]
    is_exist = True
  
  return is_exist, username, id

def load_all_patient_data(id):
  query = "select username, email, dob, gender,weight, tel from patient_data where id = "+str(id)
  cursor.execute(query)
  data = cursor.fetchall()

  for row in data:
    username = row[0]
    email = row[1]
    dob = row[2]

    #Formatting Date from yyyy-mm-dd to dd-mm-yyyy
    date = datetime.datetime.strptime(dob, "%Y-%m-%d")
    dob = date.strftime("%d-%m-%Y")

    gender = row[3]
    weight = row[4]
    tel = row[5]
  return username, email, dob, gender,weight, tel

def insert_patient_history(patient_id, diseases, doctor_id, symptoms):
    query = "insert into patient_history (patient_id, symptoms, diseases, doctor_id, timestamp) values (%s, %s, %s, %s, %s)"

    #Getting Current Date and Time

    #date
    now = datetime.datetime.now()
    current_data = now.strftime("%Y-%m-%d")
    
    #time
    current_time = now.strftime("%I-%M-%S-%p")

    #concatenate
    time = str(current_data)+"_"+str(current_time)

    print(time)


    credential = (patient_id, str(symptoms), str(diseases), doctor_id, str(time))
    cursor.execute(query, credential)
    connection.commit()
    # data = cursor.fetchall()
    
def retrive_doctor_list():
  query = "select join_id, username from doctor_data"
  cursor.execute(query)
  data = cursor.fetchall()

  return data

def get_patient_history(patient_id):
  query = "select ph.symptoms, ph.diseases, ph.timestamp, d.username, d.email from patient_history ph, doctor_data d where ph.doctor_id = d.join_id ORDER BY ph.timestamp DESC "
  cursor.execute(query)
  data = cursor.fetchall()

  return data 

def check_all_patient_list(doctor_id):
  query = "select p.username, p.dob, p.gender, p.weight, p.no_of_pregnancy, p.blood_group, p.tel,  ph.symptoms, ph.diseases, ph.timestamp from patient_data p, patient_history ph, doctor_data d where "+str(doctor_id)+" = ph.doctor_id and ph.patient_id = p.id ORDER BY ph.timestamp DESC "
  cursor.execute(query)
  data = cursor.fetchall()

  return data 

def calculate_age(birthday_string):
  """Calculates the age of a person given their birthday string in the format yyyy-mm-dd."""

  today = datetime.date.today()
  birthday_date = datetime.date.fromisoformat(birthday_string)
  age = today.year - birthday_date.year - ((today.month, today.day) < (birthday_date.month, birthday_date.day))

  return age

def generate_report_data(patient_id):
  query = "select p.username, p.dob, p.gender, p.weight, p.blood_group, p.tel, ph.symptoms, ph.diseases, d.username from patient_data p, patient_history ph, doctor_data d where d.join_id = ph.patient_id and p.id = "+str(patient_id) + " ORDER BY ph.timestamp DESC Limit 1"
  cursor.execute(query)
  data = cursor.fetchall()

  for row in data:
    patient_name = row[0]

    dob = str(row[1])
    age = calculate_age(dob)

    sex = row[2]
    weight = row[3]
    blood_group = row[4]
    tel = row[5]
    symptoms = row[6]
    diseases = row[7]
    doctor_name = row[8]
  
  return patient_name, age, sex, weight, blood_group, tel, symptoms, diseases, doctor_name


"""
#Comment Hai Bhai Log
#Comment Hai Bhai Log
#Comment Hai Bhai Log
#Comment Hai Bhai Log
#Comment Hai Bhai Log
#Comment Hai Bhai Log
#Comment Hai Bhai Log
#Comment Hai Bhai Log
#Comment Hai Bhai Log
#Comment Hai Bhai Log
#Comment Hai Bhai Log
#Comment Hai Bhai Log
#Comment Hai Bhai Log
#Comment Hai Bhai Log
#Comment Hai Bhai Log
#Comment Hai Bhai Log
#Comment Hai Bhai Log
#Comment Hai Bhai Log
#Comment Hai Bhai Log
#Comment Hai Bhai Log
#Comment Hai Bhai Log
"""

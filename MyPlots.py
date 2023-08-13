import matplotlib.pyplot as plt
# import seaborn as sns
import sqlalchemy
import pandas as pd
import pymysql

engine = sqlalchemy.create_engine( "mysql+pymysql://root:@localhost:3306/sra")
# Create a Pandas DataFrame from the user_data table.
df = pd.read_sql_table("user_data", engine, columns=["id", "name", "Actual_skills"])

#Creating Connection
connection = pymysql.connect(host='localhost',port=3306, user='root', password='', db='sra')
cursor = connection.cursor()

# Create the DB
db_sql = """CREATE DATABASE IF NOT EXISTS SRA;"""
cursor.execute(db_sql)
connection.select_db("sra")

# Create table
DB_table_name = 'user_data'
table_sql = "CREATE TABLE IF NOT EXISTS " + DB_table_name + """
                    ( id INT AUTO_INCREMENT,
                      name varchar(100) NOT NULL,
                      email_id VARCHAR(50) NOT NULL,
                      contact_no VARCHAR(15) not null,
                      ug_stream VARCHAR(100) not null,
                      training VARCHAR(3) not null,
                      certificate VARCHAR(3) not null,
                      experience VARCHAR(200) not null,
                      Timestamp VARCHAR(50) NOT NULL,
                      total_page VARCHAR(5) NOT NULL,
                      User_level VARCHAR(30) NOT NULL,
                      Actual_skills VARCHAR(300) NOT NULL,
                      resume_link VARCHAR(100) Null,
                      PRIMARY KEY (ID));
                    """
                    
cursor.execute(table_sql)

def generated_user_dropdown():
    tem = ""
    data = cursor.execute('''SELECT id, name  FROM user_data''')
    for row in data:
        tem += "<option value='"+row[0]+"'>"+row[1]+"<option>"
    
    return tem
    

def generated_graphs(Query):
    global cursor
    print(type(Query))
    if Query is None:
        cursor.execute('''SELECT * FROM user_data''')
    else:
        cursor.execute(Query)

    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=['Id', 'Name', 'Email Id', 'Contact No', 'UG', 'Any Training', 'Any Certificate', 'Any Experience', 'Uploading Time (YYYY-MM-DD_HH-MIN-SEC)', 'Total Page', 'Candidate Level', 'Skills', 'Resume Link'])

    skills_list = df["Skills"].str.split(", ").tolist()


    # # Count the number of times each skill appears in the list
    # skill_counts = {}
    # for skills in skills_list:
    #     for skill in skills:
    #         if skill not in skill_counts:
    #             skill_counts[skill] = 0
    #         skill_counts[skill] += 1

    # # Create a pie chart of the skill counts
    # plt.pie(skill_counts.values(), labels=skill_counts.keys(), autopct="%1.1f%%")
    # plt.title("Skills")


    # Count the number of times each skill appears in the list
    skill_counts = {}
    for skills in skills_list:
        for skill in skills:
            if skill not in skill_counts:
                skill_counts[skill] = 0
            skill_counts[skill] += 1

    # Get the top 5 skills by count
    top_5_skills = sorted(skill_counts.items(), key=lambda x: x[1], reverse=True)[:5]

    # Create a pie chart of the top 5 skills
    plt.pie([skill[1] for skill in top_5_skills], labels=[skill[0] for skill in top_5_skills], autopct="%1.1f%%")

    # Save the pie chart as a PNG file
    plt.savefig("skills_pie_chart.png")

    plt.show()

    # Create a bar graph of the skill counts
    plt.bar(skill_counts.keys(), skill_counts.values())
    plt.title("Skills")
    plt.show()

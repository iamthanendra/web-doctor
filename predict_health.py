from all_symptomes_list import symptoms_list

from db_work import insert_patient_history

import wikipedia as wiki

import pandas as pd
import numpy as np
data = pd.read_csv('new_data.csv')

X, y = data.iloc[:,:-1], data.iloc[:,-1]

from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
decisiontree = DecisionTreeClassifier()
decisiontree.fit(X,y)



def predict_client_health(patient_id, doctor_id, symptoms_index):
    mylist = []
    symptoms_str = ", "

    for index in symptoms_index:
        print(symptoms_list[int(index)])
        mylist.append(symptoms_list[int(index)])
    print(mylist)
    symptoms_str = symptoms_str.join(mylist)

    features = np.zeros((1, 407))

    for index in symptoms_index:
        features[0, int(index)] = 1
    
    print(features)

    global decisiontree
    output = decisiontree.predict(features)
    print(output)
    output = str(output).replace("'","").replace("[","").replace("]", "")

    summary1 = wiki.summary(output)
    # summary1 = """gdsjdjksjdk"""

    # global gaussian
    # output1 = gaussian.predict(features)
    # print(output1)
    # output1 = str(output1).replace("'","").replace("[","").replace("]", "")

    # summary2 = wiki.summary(output1)

    # out = str(output) + " / " + str(output1)

    #inserting history
    insert_patient_history(patient_id, output, doctor_id, symptoms_str)


    return output, summary1

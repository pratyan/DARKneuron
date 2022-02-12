
import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score

def create_disease_hash():
    dataset = pd.read_csv('dataset.csv')
    disease_name = [x for x in dataset['Disease'].unique()]
    disease_hash = {}
    for x in range(len(disease_name)):
        disease_hash[disease_name[x]] = x
    return disease_hash

def get_symp_hash():
  symp_severity = pd.read_csv('Symptom-severity.csv')  
  symp_hash = {}
  for i in range(len(symp_severity)):
    symp_hash[symp_severity['Symptom'][i]] = i
  return symp_hash

def label_encoding(dataset):
    for i in disease_hash:
        df['Disease'] = df['Disease'].replace(i,disease_hash[i])
    y = df['Disease']
    df.drop(['Disease'],axis=1,inplace=True)
    return y

def extract_information(disease):
    desc_index = symp_Description.loc[symp_Description['Disease']==disease]['Description']._index[0]
    desc = symp_Description.loc[symp_Description['Disease']==disease]
    
    precautions = []
    for i in symp_precaution.columns:
        if i != 'Disease' or i != 'Index':
            precautions.append(symp_precaution.loc[symp_precaution['Disease']==disease][i][desc_index])
    return desc['Description'][desc_index],precautions[1:len(precautions)-1]

if __name__ == '__main__':
    dataset = pd.read_csv("dataset.csv")
    symp_severity = pd.read_csv("Symptom-severity.csv")
    symp_Description = pd.read_csv("symptom_Description.csv")
    symp_precaution = pd.read_csv("symptom_precaution.csv")

    symp_Description['Index'] = pd.Series([a for a in range(len(symp_Description))])
    symp_severity['Index'] = pd.Series([a for a in range(len(symp_severity))])
    symp_precaution['Index'] = pd.Series([a for a in range(len(symp_precaution))])

    disease_hash = create_disease_hash()

    symp_hash = get_symp_hash()

    symptoms = []
    for i in symp_severity['Symptom']:
        if i not in symptoms:
            symptoms.append(i)
            
    symptoms.append('Disease')
    df = pd.DataFrame(columns = symptoms,data = np.zeros(dtype=int,shape=(len(dataset),len(symptoms))))

    for i in range(len(dataset)):
      record = dataset.iloc[i]
      for col in dataset.columns:
            if col != 'Disease':
                if str(record[col]).replace(' ','') != 'nan':
                    column = str(record[col].replace(' ',''))
                    df.loc[i,column] = 1
    
    y = label_encoding(df)
    train_data,test_data,train_label,test_label = train_test_split(df,y,test_size=0.2,shuffle=True)

    rf = RandomForestClassifier()
    rf.fit(train_data,train_label)


    pkl_filename = "rf.pkl"
    with open(pkl_filename, 'wb') as file:
        pickle.dump(rf, file)

    with open(pkl_filename, 'rb') as file:
        pickle_model = pickle.load(file)    

    # Calculate the accuracy score and predict target values
    score = pickle_model.score(test_data, test_label)
    print("Test score: {0:.2f} %".format(100 * score))

import pandas as pd
import numpy as np
from scipy.spatial.distance import pdist

csv_db = pd.read_csv('toy_input.csv')
guy = pd.read_csv('toy_profile.csv')
FEATURES = ['label_1','label_2','label_3','label_4','label_5','label_6','label_7','label_8','label_9','label_10','label_11']

ID = 'Name_id'

def match_people(data):
    """
    Matches people that are closest to each other in personality profile penalizing big differences more.
    Removes matched people form the dataframe
    :param csv_profile: 
    :return: names of matched people
    """
    df = data.set_index([ID])
    distances = pdist(df, metric='sqeuclidean')
    best_match = str(np.argmax(distances))
    index1 = int(best_match[0])
    index2 = int(best_match[1])
    name1 = str(df.index[index1])
    name2 = str(df.index[index2])
    df.drop(name1, axis=0, inplace=True)
    df.drop(name2, axis=0, inplace=True)
    return name1, name2

def add_person(csv_db, data):
    """
    add csv_profile to csv_db
    :param csv_db:
    :param csv_profile:
    :return:  None
    """
    csv_profile = data.set_index([ID])
    csv_db = pd.concat([csv_db, csv_profile], axis=0)
    return csv_db

def remove_person(csv_db, name):
    """
    Removes given name from csv_db
    :param csv_db:
    :param name:
    :return: csv_db with name removed
    """
    name = str(name)
    return csv_db.drop(name, axis=0)

def init_db(columns):
    """
    :return: empty db
    """
    df = pd.DataFrame(columns=columns)
    return df




name1, name2 = match_people(csv_db)
name = 'ad'
df = init_db(FEATURES)
df = add_person(df, csv_db)
df = add_person(df,guy)
df = remove_person(df, 'cd')
print(df)




import pandas as pd
import numpy as np
from scipy.spatial.distance import pdist
from scipy.spatial.distance import sqeuclidean
from jason_transform import *





FEATURES = ['label_1','label_2','label_3','label_4','label_5','label_6','label_7','label_8','label_9','label_10','label_11']
RESTAURANT = ['Fast Food', ]
ID = 'id'
BASE_DISCOUNT = 0.15
MAX_DISCOUNT = 0.35



def match_people(data):
    """
    Matches people that are closest to each other in personality profile penalizing big differences more.
    Removes matched people form the dataframe
    :param csv_profile: 
    :return: names of matched people
    """
    df = data.set_index([ID])
    if data.empty or len(data) < 2:
        return None, None, None
    distances = pdist(df, metric='sqeuclidean')
    best_match = str(np.argmax(distances))
    index1 = int(best_match[0])
    index2 = int(best_match[1])
    name1 = str(df.index[index1])
    name2 = str(df.index[index2])
    feature = get_most_similar_feature(df, name1, name2)
    df.drop(name1, axis=0, inplace=True)
    df.drop(name2, axis=0, inplace=True)
    return name1, name2, feature

def get_most_similar_feature(data, name1, name2):
    """

    :param data:
    :param name1:
    :param name2:
    :return:
    """
    diff = abs(data.loc[name1] - data.loc[name2])
    feature = diff.idxmin(axis=1)
    return feature

def add_person(csv_db, data):
    """
    add csv_profile to csv_db. can add more than one profile
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
    try:
        return csv_db.drop(name, axis=0)
    except ValueError:
        return csv_db

def init_db(columns):
    """
    :return: empty db
    """
    df = pd.DataFrame(columns=columns)
    return df


def match_person(df, person, threshold=0.0):
    """
    Finds the match for the person among people in the DB
    :param df:
    :param person:
    :param threshold: maximum distance for which person if matched. if Min distance > threshold, None is returned
    :return: name of the match or None
    """
    person = person.set_index([ID])
    distances = {}
    if df.empty:
        return None, None
    for row in df.iterrows():
        name, value = row
        distances[name] = sqeuclidean(person, value)
    best = sorted(distances, key=distances.get)[0]
    if distances[best] > threshold:
        return None, None
    diff = abs(person - value)
    feature = diff.idxmin(axis=1)[0]
    return best, feature


def add_user_to_user_dict(u_dict,user):
    """
    Adds user to the dict
    :param dict:
    :param user:
    :return: None
    """
    key = user[ID][0]
    if key in u_dict:
        pass
    else:
        u_dict[key] = 0

def remove_user_from_user_dict(u_dict,user):
    """
    guess
    :param dict:
    :param user:
    :return: None
    """
    key = user[ID][0]
    if key in u_dict:
        del u_dict[key]
    else:
        pass

def add_experience(u_dict, user, exp):
    """

    :param user_dict:
    :param user:
    :param exp:
    :return:
    """
    key = user[ID][0]
    if key in u_dict:
        u_dict[key] = u_dict[key] + exp
    else:
        pass


def get_discount(u_dict, user, BASE_DISCOUNT,MAX_DISCOUNT):
    """

    :param user:
    :param BASE_DISCOUNT:
    :return: discount to use
    """
    key = user[ID][0]
    if key not in u_dict:
        return BASE_DISCOUNT
    else:
        discount = BASE_DISCOUNT + (u_dict[key]**0.5)/100
        if discount > MAX_DISCOUNT:
            return MAX_DISCOUNT
        else:
            return discount

#init data structures
df = init_db(FEATURES)
dict_user = {}

#TESTING

with open('ex22.json') as data_file:
    data = json.load(data_file)

csv_db = transform_json_to_csv(data, 'Oprah')



# csv_db = pd.read_csv('toy_input.csv')
guy = pd.read_csv('JayZ.csv')
girl = pd.read_csv('Donald.csv')
print(csv_db.shape, guy.shape)


add_user_to_user_dict(dict_user, guy)
remove_user_from_user_dict(dict_user, girl)
add_experience(dict_user, guy, 0)
discount = get_discount(dict_user, guy, BASE_DISCOUNT, MAX_DISCOUNT)
print(discount)


name1, name2, feature = match_people(csv_db)
name = 'ad'
df = init_db(FEATURES)
df = add_person(df, csv_db)
df = add_person(df,guy)
df = remove_person(df, 'cd')
match, diff = match_person(df, girl)
print(match, diff)
print(name1, name2, feature)







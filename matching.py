import pandas as pd
import numpy as np
from scipy.spatial.distance import pdist, squareform
from scipy.spatial.distance import sqeuclidean
from jason_transform import *





FEATURES = ['Adventurousness', 'Artistic interests', 'Emotionality', 'Imagination',
       'Intellect', 'Authority-challenging', 'Achievement striving',
       'Cautiousness', 'Dutifulness', 'Orderliness', 'Self-discipline',
       'Self-efficacy', 'Activity level', 'Assertiveness', 'Cheerfulness',
       'Excitement-seeking', 'Outgoing', 'Gregariousness', 'Altruism',
       'Cooperation', 'Modesty', 'Uncompromising', 'Sympathy', 'Trust',
       'Fiery', 'Prone to worry', 'Melancholy', 'Immoderation',
       'Self-consciousness', 'Susceptible to stress']


RESTAURANT = ['Fast Food', ]
ID = 'id'
BASE_DISCOUNT = 0.15
MAX_DISCOUNT = 0.35



def match_people(df):
    """
    Matches people that are closest to each other in personality profile penalizing big differences more.
    Removes matched people form the dataframe
    :param csv_profile: 
    :return: names of matched people
    """
    if df.empty:
        return None, None, None
    dist = pdist(df, metric='sqeuclidean')
    distances = squareform(dist)
    best_match = np.amin(distances[np.nonzero(distances)])
    itemindex = np.where(distances == best_match)
    index1 = itemindex[0][0]
    index2 = itemindex[1][0]
    name1 = str(df.index[index1])
    name2 = str(df.index[index2])
    feature = get_most_similar_feature(df, name1, name2)
    df = remove_person(df, name1)
    df = remove_person(df, name1)
    return name1, name2, feature, df

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
            return round(discount,2)

#init data structures
df = init_db(FEATURES)
dict_user = {}

#TESTING

with open('ex44.json') as data_file:
    hillary = json.load(data_file)
with open('trump.json') as data_file:
    trump_data = json.load(data_file)

hillary = transform_json_to_csv(hillary, 'hillary')
trump = transform_json_to_csv(trump_data, 'trump')
trump2 = transform_json_to_csv(trump_data, 'trump2')


add_user_to_user_dict(dict_user, trump)
remove_user_from_user_dict(dict_user, hillary)
add_experience(dict_user, trump, 20)
discount = get_discount(dict_user, trump, BASE_DISCOUNT, MAX_DISCOUNT)

df = init_db(FEATURES)
df = add_person(df, trump)
df = remove_person(df, 'trump')
df = add_person(df, hillary)
df = add_person(df, trump2)
name1, name2, feature, df = match_people(df)

df = add_person(df, hillary)

match, diff = match_person(df, trump)
print(match, diff)
print(name1, name2, feature)







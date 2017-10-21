import pandas as pd
import numpy as np
from scipy.spatial.distance import pdist, squareform
from scipy.spatial.distance import sqeuclidean
from jason_transform import *
from get_text_py import get_text_py






FEATURES = ['Adventurousness', 'Artistic interests', 'Emotionality', 'Imagination',
       'Intellect', 'Authority-challenging', 'Achievement striving',
       'Cautiousness', 'Dutifulness', 'Orderliness', 'Self-discipline',
       'Self-efficacy', 'Activity level', 'Assertiveness', 'Cheerfulness',
       'Excitement-seeking', 'Outgoing', 'Gregariousness', 'Altruism',
       'Cooperation', 'Modesty', 'Uncompromising', 'Sympathy', 'Trust',
       'Fiery', 'Prone to worry', 'Melancholy', 'Immoderation',
       'Self-consciousness', 'Susceptible to stress']


ID = 'id' # id column
BASE_DISCOUNT = 0.15 # disccount with no Exp points
MAX_DISCOUNT = 0.35 # maximum Exp points
PATH = 'db.csv'



def match_people(path):
    """
    Matches people that are closest to each other in personality profile penalizing big differences more.
    Removes matched people form the dataframe
    :param csv_profile: 
    :return: names of matched people
    """
    df = pd.read_csv(path)
    df.set_index(['Unnamed: 0'], inplace=True)
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
    remove_person(path, name1)
    remove_person(path, name1)
    df.to_csv(path)
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

def add_person(path, data):
    """
    add csv_profile to csv_db. can add more than one profile
    :param csv_db:
    :param csv_profile:
    :return:  None
    """
    csv_db = pd.read_csv(path)
    csv_db.set_index(['Unnamed: 0'], inplace=True)
    if 'Unnamed: 0.1' in csv_db.columns:
        del csv_db['Unnamed: 0.1']
    csv_profile = data.set_index([ID])
    csv_db = pd.concat([csv_db, csv_profile], axis=0)
    csv_db.to_csv(path)
    return None


def remove_person(path, name):
    """
    Removes given name from csv_db
    :param csv_db:
    :param name:
    :return: csv_db with name removed
    """
    csv_db = pd.read_csv(path)
    csv_db.set_index(['Unnamed: 0'], inplace=True)
    if 'Unnamed: 0.1' in csv_db.columns:
        del csv_db['Unnamed: 0.1']
    name = str(name)
    try:
        csv_db.drop(name, axis=0).to_csv(path)
    except ValueError:
        csv_db.to_csv(path)


def init_db(columns, path):
    """
    :return: None
    """
    df = pd.DataFrame(columns=columns)
    df.to_csv(path)


def match_person(path, person, threshold=0.0):
    """
    Finds the match for the person among people in the DB
    :param df:
    :param person:
    :param threshold: maximum distance for which person if matched. if Min distance > threshold, None is returned
    :return: name of the match or None
    """
    df = pd.read_csv(path)

    df.set_index(['Unnamed: 0'], inplace=True)
    if 'Unnamed: 0.1' in df.columns:
        del df['Unnamed: 0.1']
    person = person.set_index([ID])
    distances = {}
    if df.empty:
        return None, None
    for row in df.iterrows():
        name, value = row
        distances[name] = sqeuclidean(person, value)
    best = sorted(distances, key=distances.get)[0]
    if distances[best] < threshold:
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

def add_user_all(handle,PATH):
    get_text_py(handle, name_text_output="output.txt",
                path_Rscript='./get_text.R')
    with open('output.json') as data_file:
        user_json = json.load(data_file)
    user = transform_json_to_csv(user_json, str(handle))
    add_user_to_user_dict(dict_user, user)
    add_person(PATH, user)

#init data structures
init_db(FEATURES, PATH)
dict_user = {}

#TESTING

with open('ex44.json') as data_file:
    hillary = json.load(data_file)
with open('trump.json') as data_file:
    trump_data = json.load(data_file)

hillary = transform_json_to_csv(hillary, 'hillary')
trump = transform_json_to_csv(trump_data, 'trump')
trump2 = transform_json_to_csv(trump_data, 'trump2')


# GAMIFICATION
# Add when we get handle
# Returns nothing, just updates a global dictionary
add_user_to_user_dict(dict_user, trump)
remove_user_from_user_dict(dict_user, hillary)
add_experience(dict_user, trump, 20)
discount = get_discount(dict_user, trump, BASE_DISCOUNT, MAX_DISCOUNT)

add_person(PATH, trump)
remove_person(PATH, 'trump')
add_person(PATH, hillary)
add_person(PATH, trump2)
name1, name2, feature = match_people(PATH)

add_person(PATH, hillary)

match, diff = match_person(PATH, trump)
print(match, diff)
print(name1, name2, feature)







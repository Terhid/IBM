# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20 18:55:49 2017
# # input json from API
# output panda df with names of qualities and name_id

@author: david
"""
import os
import random
import numpy as np
import pandas as pd
import json
from pprint import pprint




def transform_json_to_csv(data, twitter_name):
    """
    :param path:
    :return: df
    """


    names = []
    values = []



    for key, value in data.items():
        if key == "personality":
            temp = data[key]

            for index in range(len(temp)):
                new_temp = temp[index]
                names, values = get_values(new_temp, names, values)
    ######### end of jason data extraction =)

    # create df with random data
    #df = pd.DataFrame(np.random.random(size=(rows_to_add, len(names))), columns=names)
    #df.loc[0] = values # put opera winfrey values here
    values.append(twitter_name)
    df = pd.DataFrame([values], columns=names + ['id'])
    return df


def get_values(dict, names, values):
    """ return arrays filled with values  """
    for key, value in dict.items():
        if type(value) is list:
            new_val = value

            for x in range(len(new_val)):
                name_var = new_val[x]["name"]
                val_var = new_val[x]["raw_score"]
                names.append(name_var)
                values.append(val_var)

    return names, values



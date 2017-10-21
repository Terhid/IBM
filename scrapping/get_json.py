# -*- coding: utf-8 -*-
import requests, json
"""

calling get_json needs an handler for the person to scrape
output is output.json


@author: david
"""
import subprocess


def get_text_py(tweetUser= "HillaryClinton", name_text_output= "output.txt",
                path_Rscript ='./get_text.R'):
    """
    :param tweetUser : the tweeter name of who we want to scrape
    :param name_text ouput : the name of the txt file given as output
    :param path_Rscript : path to Rscript i.e. 'C:\\Users\\david\\HACKATON\\get_text.R'
    :output a txt file in current working dir
    """
    # Define command and arguments
    command = 'Rscript'
    # Arguments to be called in a list
    args = [tweetUser, name_text_output]    
    # Build subprocess command
    cmd = [command, path_Rscript] + args    
    # check_output will run the command [and store to result]
    subprocess.check_output(cmd, universal_newlines=True)
    
def get_json(tweetUser= "HillaryClinton", name_text_output= "output.txt", path_Rscript = './get_text.R'):
    # only the first element is necessary (the handler), the rest should be stable
    # KEEP name_text_output as it is, because is is hardcoded in the curl call
    # OUTPUT IS 'output.json'
    
    get_text_py(tweetUser, name_text_output, path_Rscript)

    url = 'https://gateway.watsonplatform.net/personality-insights/api/v3/profile?version=2017-10-13'
    payload = open("output.txt", 'rb').read()
    headers = {'content-type': 'text/plain', 'Accept-Charset': 'UTF-8'}
    r = requests.post(url, data = payload, headers=headers, 
            auth = ("2e946b17-9226-47d0-8110-b17f90fb52f1", "MO8G1qjWLCYT"))

    print(r)
    return r

    

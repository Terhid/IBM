import subprocess

def get_text_py(tweetUser, name_text_output, path_Rscript):
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
    

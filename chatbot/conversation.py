import json
from watson_developer_cloud import ConversationV1
import sys

conversation = ConversationV1(
    username='d1fe3542-a6e8-44d6-bb09-9981011100f2',
    password='ntguGSN3Mfn6',
    version='2017-04-21')

# For each action, choose the corresponding workspace
# Obtained manuallly. Could also be obtained by querying the api
workspace_id = 'd14f9ce4-effc-45e7-b7da-6a65ac4e72eb'

def next_context_start(old_context): 
    products = [{"product": "beer", "price":5, "deal": 4}, 
            {"product": "caffe", "price":2, "deal": 1}, 
            {"product": "soft drink", "price":3, "deal": 2}, 
            {"product": "juice", "price":4, "deal": 3} 
            ]
    new_context = old_context
    new_context["menu"] = products
    return old_context # inicialization
def next_context_1(old_context): return old_context # welcome node
def next_context_11(old_context): return old_context # no-matching 
def next_context_12(old_context): return old_context # yes-matching, asks name
def next_context_121(old_context): return old_context # asks twitter

# extracts the twitter handle, matches with a user, sends it in variable $match
def next_context_1211(old_context): # thanks for twitter
    twitter_handle = old_context["twitter_handle"]
    matches = {"@cesar": "@mauro", "@david": "@wojtek"}
    new_context = old_context
    new_context["match"] = matches[twitter_handle]
    return new_context




node_id = 0
rec_context = {}
node_handlers = {0: next_context_start, 1: next_context_1, 11: next_context_11,
        12: next_context_12, 121: next_context_121, 1211: next_context_1211}
        #2: next_context_2}

while True:
    data = input('> ')
    if not data: sys.exit(0)
    # unhandled nodes keep the old context
    if node_id in node_handlers.keys():
        new_context = node_handlers[node_id](rec_context)
    else:
        context = rec_context

    # Sends request
    response = conversation.message(
        workspace_id = workspace_id,
        message_input={
            'text': data 
        },
        context = new_context
    )

    # Response received
    rec_context = response["context"]
    node_id = rec_context["node_id"]
    print("The node id is " + str(rec_context["node_id"]))
    print("The context is " + str(rec_context.keys()))
    print(json.dumps(response["output"]["text"][0], indent=2))







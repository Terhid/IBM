import json
from watson_developer_cloud import ConversationV1

#########################
# message
#########################

conversation = ConversationV1(
    username='d1fe3542-a6e8-44d6-bb09-9981011100f2',
    password='ntguGSN3Mfn6',
    version='2017-04-21')

## Returns existing workspaces. 
# response = conversation.list_workspaces()
# print(json.dumps(response, indent=2))

# For each action, choose the corresponding workspace
# Obtained manuallly. Could also be obtained by querying the api
workspace_id = '6de751b6-6522-4484-a4a7-5714f0d96c33'

response = conversation.message(
    workspace_id = workspace_id,
    message_input={
        'text': 'Hello'
    }
)

print(json.dumps(response["input"]["text"], indent=2))
print(json.dumps(response["output"]["text"][0], indent=2))


response = conversation.message(
    workspace_id = workspace_id,
    message_input={
        'text': 'goodbye'
    }
)

print(json.dumps(response["input"]["text"], indent=2))
print(json.dumps(response["output"]["text"][0], indent=2))


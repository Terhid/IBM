import json
from watson_developer_cloud import ConversationV1


conversation = ConversationV1(
    username='d1fe3542-a6e8-44d6-bb09-9981011100f2',
    password='ntguGSN3Mfn6',
    version='2017-04-21')


# For each action, choose the corresponding workspace
# Obtained manuallly. Could also be obtained by querying the api
workspace_id = '6de751b6-6522-4484-a4a7-5714f0d96c33'

while True:
    data = input('> ')
    if not data: sys.exit(0)
    response = conversation.message(
        workspace_id = workspace_id,
        message_input={
            'text': data 
        }
    )
    print(json.dumps(response["output"]["text"][0], indent=2))





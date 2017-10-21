import json
from watson_developer_cloud import ConversationV1
import sys

class Watson:

    def __init__(self):
        self.conversation = ConversationV1(
            username='d1fe3542-a6e8-44d6-bb09-9981011100f2',
            password='ntguGSN3Mfn6',
            version='2017-04-21')
        # For each action, choose the corresponding workspace
        # Obtained manuallly. Could also be obtained by querying the api
        self.workspace_id = 'd14f9ce4-effc-45e7-b7da-6a65ac4e72eb'
        self.node_id = 0
        self.rec_context = {}
        self.node_handlers = {0: self.next_context_start, 1: self.next_context_1, 
                11: self.next_context_11, 12: self.next_context_12,
                121: self.next_context_121, 1211: self.next_context_1211}

    def next_context_start(self, old_context): 
        products = [{"product": "beer", "price":5, "deal": 4}, 
                {"product": "caffe", "price":2, "deal": 1}, 
                {"product": "soft drink", "price":3, "deal": 2}, 
                {"product": "juice", "price":4, "deal": 3} 
                ]
        new_context = old_context
        new_context["menu"] = products
        return old_context # inicialization

    def next_context_1(self, old_context): return old_context # welcome node
    def next_context_11(self, old_context): return old_context # no-matching 
    def next_context_12(self, old_context): return old_context # yes-matching, asks name
    def next_context_121(self, old_context): return old_context # asks twitter

    # extracts the twitter handle, matches with a user, sends it in variable $match
    def next_context_1211(self, old_context): # thanks for twitter
        twitter_handle = old_context["twitter_handle"]
        matches = {"@cesar": "@mauro", "@david": "@wojtek", "@mauro": "@cesar",
                "@mauro": "@donaldtrump", "@hillary": "@donaldtrump",
                "@BarackObama": "@donaldtrump"}
        new_context = old_context
        new_context["match"] = matches[twitter_handle]
        return new_context


    def send_message(self, input_text):
        if self.node_id in self.node_handlers.keys():
            new_context = self.node_handlers[self.node_id](self.rec_context)
        else:
            new_context = self.rec_context

        response = self.conversation.message(
            workspace_id = self.workspace_id,
            message_input={
                'text': input_text 
            },
            context = new_context
        )
        self.rec_context = response["context"]
        self.node_id = self.rec_context["node_id"]
        print("The node id is " + str(self.rec_context["node_id"]))
        print("The context is " + str(self.rec_context.keys()))
        answer = "\n".join([r for r in response["output"]["text"]])
        return(answer)








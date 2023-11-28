from characterai import PyCAI

class CharAI():

    def __init__(self):
        self.client = PyCAI("0a38a9ea1077724b91aefae04030556a49808d15")  # my account token
        self.chat = self.client.chat.get_chat("YU_x3uvz4KYFJbVGDHIlmMcsEJp5y1VlKSsXmr1U79k")  # therapist character
        self.participants = self.chat['participants']
        if not self.participants[0]['is_human']:
            self.tgt = self.participants[0]['user']['username']
        else:
            self.tgt = self.participants[1]['user']['username']

    def get_response(self, query):
        data = self.client.chat.send_message(self.chat['external_id'], self.tgt, query)
        name = data['src_char']['participant']['name']
        text = data['replies'][0]['text']
        return text

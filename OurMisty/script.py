from mistyPy.Robot import Robot
import json


class Script():

    def __init__(self):
        with open("script.json", "r") as f:
            self.script = json.load(f)
            self.state = "start"
            self.name = None

    def get_text(self):
        return self.script[self.state]["message"].format(name=self.name)

    def next_state(self, response):
        if self.state == "start" or self.state == "wrong_name":
            self.name = response
            self.state = "name_given"
        else:
            for option in self.script[self.state]["options"]:
                if option["response"] in response:
                    self.state = option["next"]
                    return
            print("User's answer does not match any responses defined in the script")

    def get_response(self, speech_result):
        response = speech_result
        if "ja" in speech_result.lower():
            response = "JA"
        elif "nee" in speech_result.lower():
            response = "NEE"
        self.next_state(response)
        return self.get_text()


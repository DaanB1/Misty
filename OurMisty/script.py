from mistyPy.Robot import Robot
import json


class Script():

    def __init__(self):
        with open("script.json", "r") as f:
            self.script = json.load(f)
            self.state = "start"
            self.name = None

    def get_text(self):
        print("getting text")
        return self.script[self.state]["message"].format(name=self.name)

    def next_state(self, response):
        print("updating state")
        if self.state == "start" or self.state == "wrong_name":
            self.name = response
            self.state = "name_given"
        else:
            for option in self.script[self.state]["options"]:
                if option["response"] in response:
                    self.state = option["next"]
                    return
            print("NO STATE FOUND")


import re
import json


class Script():

    def __init__(self, file):
        with open(file, "r") as f:
            self.script = json.load(f)
            self.state = "start"
            self.name = None

    def get_text(self):
        return self.script[self.state]["message"].format(name=self.name)

    def get_response(self, speech_result):
        if self.state == "start" or self.state == "wrong_name" or self.state == "startyes":
            self.name = speech_result
            self.state = "name_given"
            return self.get_text()
        else:
            words = re.sub(r'[^\w\s]', '', speech_result).lower().split(" ")
            for option in self.script[self.state]["options"]:
                if len(option["keywords"]) == 0:
                    self.state = option["next"]
                    return self.get_text()
                for keyword in option["keywords"]:
                    if keyword in words:
                        result = []
                        if "remark" in option:
                            result.append(option["remark"])
                        self.state = option["next"]
                        text = self.get_text()
                        if isinstance(text, list):
                            result.extend(text)
                        else:
                            result.append(text)
                        return result
            print("User's answer does not match any responses defined in the script")
            #return "Sorry, geef alsjeblieft antwoord met ja of nee."


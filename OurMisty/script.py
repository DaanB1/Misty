import re
import json


class Script():

    def __init__(self, file):
        self.name = None
        self.script = None
        self.state = None
        self.loadScript(file)

    def loadScript(self, file):
        with open(file, "r") as f:
            self.script = json.load(f)
            self.state = "start"

    def get_text(self):
        return self.script[self.state]["message"].format(name=self.name)

    def get_name(self, speech_result):
        words = re.sub(r'[^\w\s]', '', speech_result).lower().split(" ")
        if len(words) == 1:
            return words[0]
        result = re.search(r"\b(ben|heet|is)\b\.?\s*(\w+)", speech_result)
        return result.group(2)

    def get_response(self, speech_result):
        if self.state == "start" or self.state == "wrong_name":
            self.name = self.get_name(speech_result)
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
                        if "loadScript" in option:
                            self.loadScript(option["loadScript"])
                            return result
                        if "next" in option:
                            self.state = option["next"]
                            text = self.get_text()
                            if isinstance(text, list):
                                result.extend(text)
                            else:
                                result.append(text)
                        return result
            print("User's answer does not match any responses defined in the script")
            #return "Sorry, geef alsjeblieft antwoord met ja of nee."


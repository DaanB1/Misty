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
            self.scriptFile = file
            self.script = json.load(f)
            self.state = "start"

    def get_text(self):
        text = self.script[self.state]["message"]
        print("realtext:", text)
        if isinstance(text, list):
            return text
        else:
            return text.format(name=self.name)

    def get_name(self, speech_result):
        words = re.sub(r'[^\w\s]', '', speech_result).lower().split(" ")
        if len(words) == 1:
            return words[0]
        result = re.search(r"\b(ben|heet|is)\b\.?\s*(\w+)", speech_result)
        if result:
            return result.group(2)
        else:
            return None

    def get_response(self, speech_result):
        #Hard coded name extraction functionality
        if (self.state == "start" or self.state == "wrong_name") and self.scriptFile == "scriptOpening.json":
            self.name = self.get_name(speech_result)
            if self.name is None:
                self.state = "start"
                return "Sorry, kan je dat herhalen?"
            else:
                self.state = "name_given"
                return self.get_text()
        #The main function
        else:
            words = re.sub(r'[^\w\s]', '', speech_result).lower().split(" ")
            for option in self.script[self.state]["options"]:
                if len(option["keywords"]) == 0:
                    return self.process_option(option)
                for keyword in option["keywords"]:
                    if keyword in words:
                        return self.process_option(option)
            print("User's answer does not match any responses defined in the script")
            return "Sorry, kan je dat herhalen?"

    def process_option(self, option):
        result = []
        if "remark" in option:
            result.append(option["remark"])
        if "loadScript" in option:
            self.loadScript(option["loadScript"])
        if "next" in option:
            self.state = option["next"]
            text = self.get_text()
            if isinstance(text, list):
                result.extend(text)
            else:
                result.append(text)
        return result

from mistyPy.Robot import Robot


class Script():

    def __init__(self):
        self.messageList = []
        self.index = 0

    def get_next(self):
        if self.index == len(self.messageList):
            raise Exception("Reached end of script")
        message = self.messageList[self.index]
        self.index += 1
        return message

    def add_message(self, message):
        self.messageList.append(message)

    def restart(self):
        self.index = 0

    def load_default_script(self):
        self.messageList = []
        self.index = 0
        self.add_message("Hallo. Ik ben misty, hoe gaat het met jou?")
        self.add_message("Dat is fijn om te horen! Wat zijn je hobbies?")
        self.add_message("Leuk! Ik zelf houd van schaken.")

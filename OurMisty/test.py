from ttsazure import CustomSpeak
from charai import CharAI
import time

misty = None
azure_key = "8bd093f509044052933c510c26336633"
azure_region = "westeurope"

speak = CustomSpeak(misty, azure_key, azure_region)
charAI = CharAI()

start = time.time()
response = charAI.get_response("Hallo, zou je me kunnen helpen?")
print(response)
speak.speak(response)
end = time.time()
print(f"Finished in {end - start} seconds")
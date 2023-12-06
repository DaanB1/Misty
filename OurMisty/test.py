from ttsazure import CustomSpeak
from charai import CharAI
import time

misty = None
azure_key = "5cea5747535f427b889651b335da74f7"
azure_region = "westeurope"

speak = CustomSpeak(misty, azure_key, azure_region)
charAI = CharAI()

start = time.time()
response = charAI.get_response("Hoi, hoe gaat het?")
print(response)
speak.speak(response, utteranceId="utterance")
end = time.time()
print(f"Finished in {end - start} seconds")
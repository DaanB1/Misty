from mistyPy.Robot import Robot
from mistyPy.Events import Events
from charai import CharAI
from ttsazure import CustomSpeak
import time


azure_key = "8bd093f509044052933c510c26336633"
azure_region = "westeurope"
misty = Robot("192.168.39.213")
misty.set_default_volume(30)
speak = CustomSpeak(misty, azure_key, azure_region)

# misty's head position
headPitch = 0
headYaw = 0

# Connect to Character.ai
charAI = CharAI()

def test_head_positions():
    for pitch in range(-5, 5):
        for yaw in range(-5, 5):
            misty.move_head(pitch, 0, yaw, units="position")
            print(f"position: {pitch}, 0, {yaw}")
            time.sleep(3)
    pass


def tts_complete(event):
    print("tts", event)
    misty.capture_speech_azure(silenceTimeout=10000, maxSpeechLength=10000, azureSpeechKey=azure_key, azureSpeechRegion=azure_region)

def voice_record_complete( event):
    print("vrc", event)
    if "message" in event:
        message = event["message"]
        if message["errorMessage"] == "NoMatch":
            speak.speak("Sorry, could you repeat that?")
            return
        result = message["speechRecognitionResult"]
        print(f"misty heard: {result}")
        response = charAI.get_response(result)
        print(f"misty's response: {response}")
        #speak.speak(response)
        misty.speak(response, utteranceId="utterance")


# work in progress
def look_at_face(event):
    global headYaw
    global headPitch
    if "message" in event:
        message = event["message"]
        bearing = message["bearing"]
        distance = message["distance"]
        elevation = message["elevation"]
        if abs(bearing) > 3 and abs(elevation) > 3:
            misty.move_head(headPitch + 180 / 33 * elevation, 0, headYaw + 180 / 66 * bearing, duration=7 / abs(bearing))
        elif abs(bearing) > 3:
            misty.move_head(headPitch, 0, headYaw + 180 / 6 * bearing, duration=7 / abs(bearing))
        else:
            misty.move_head(headPitch + 180 / 33 * elevation, 0, headYaw, duration=5 / abs(elevation))
        #bearing: negative values = look to the right
        #distance: not used currently
        #elevation: positive values = look up

def update_position(event):
    #print(event)
    global headYaw
    global headPitch
    if "message" in event:
        message = event["message"]
        if message["sensorId"] == "ahy":
            headYaw = message["value"]
        if message["sensorId"] == "ahp":
            headPitch = message["value"]




# called after misty hears "hey misty" for the first time
def start_session():
    misty.stop_object_detector()
    misty.stop_face_detection()
    misty.move_head(0,0,0)
    misty.register_event(Events.VoiceRecord, "voicerecord", keep_alive=True, callback_function=voice_record_complete)
    misty.register_event(Events.AudioPlayComplete, "ttscomplete", keep_alive=True, callback_function=tts_complete)
    misty.register_event(Events.TextToSpeechComplete, "ttscomplete2", keep_alive=True, callback_function=tts_complete)
    misty.register_event(Events.ActuatorPosition, "actuatorposition", keep_alive=True, callback_function=update_position)
    misty.register_event(Events.FaceRecognition, "facedetection", keep_alive=True, debounce=5000, callback_function=look_at_face)
    #misty.speak("Hey! Lets start our session", utteranceId="utterance")
    #speak.speak("Hey! Lets start our session")
    print("a")
    speak.speak("Hallo, laten we onze sessie beginnen")
    misty.start_face_detection()
    #test_head_positions()
    print("session started")

start_session()
#speak.test()

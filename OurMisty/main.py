from mistyPy.Robot import Robot
from mistyPy.Events import Events
from charai import CharAI
from ttsazure import CustomSpeak
from deepface import DeepFace
from script import Script
import numpy as np
import cv2
import time
import base64

azure_key = "5cea5747535f427b889651b335da74f7"
azure_region = "westeurope"
misty = Robot("192.168.237.213")
misty.set_default_volume(25)

script_file = "scriptOpening.json"
script = Script(script_file)
settings = {"useScript": True, "useMaleVoice": False, "mimicEmotion": False, "lookAtFace": True}

# speakModule = misty #for built in voice
speakModule = CustomSpeak(misty, azure_key, azure_region, male=settings["useMaleVoice"])  # for custom voice
messageQueue = []

# misty's position
headPitch = 0
headYaw = 0
bodyYaw = 0

# perceived emotional state
emotion = "neutral"
displayed_emotion = "neutral"

# Connect to Character.ai
charAI = CharAI()


# This function enables misty to speak multiple lines with pauses between them
def speak(messages):
    if isinstance(messages, ):
        messageQueue.extend(messages)
    else:
        messageQueue.append(messages)

    while len(messageQueue) != 0:
        text = messageQueue.pop()
        if text.startswith("#"):
            time.sleep(int(text.lstip(1)))
        else:
            if len(messageQueue) == 0:
                misty.register_event(Events.AudioPlayComplete, "ttscomplete", callback_function=tts_complete)
            speakModule.speak(text, utteranceId="utterance")


def tts_complete(event):
    print("tts", event)
    misty.register_event(Events.VoiceRecord, "voicerecord", callback_function=voice_record_complete)
    misty.capture_speech_azure(speechRecognitionLanguage="nl-NL", azureSpeechKey=azure_key,
                               azureSpeechRegion=azure_region)


def voice_record_complete(event):
    print("vrc", event)
    if "message" in event:
        message = event["message"]
        if not message["success"]:
            speak("Sorry, kan je dat herhalen?")
            return
        result = message["speechRecognitionResult"]
        print(f"misty heard: {result}")

        if settings["useScript"]:
            response = script.get_response(result)
        else:
            response = charAI.get_response(result)
        speak(response)
        print(f"misty's response: {response}")


def look_at_audio(event):
    print(event)
    global bodyYaw
    if "message" in event:
        message = event["message"]
        heading = message["degreeOfArrivalSpeech"]
        heading2 = np.argmax(message["voiceActivityPolar"])
        print(f"bodyYaw: {bodyYaw}, heading: {heading}, heading2: {heading2}")
        print(f"changing bodyYaw to: {(bodyYaw - heading) % 360}")
        result = misty.drive_arc(heading=(bodyYaw - heading) % 360, radius=0, timeMs=3000, reverse=False)
        print(result.json())


def look_at_face(event):
    if not settings["lookAtFace"]:
        return
    global headYaw
    global headPitch
    if "message" in event:
        message = event["message"]
        bearing = message["bearing"]
        distance = message["distance"]
        elevation = message["elevation"]
        newYaw = headYaw
        newPitch = headPitch
        if abs(elevation) > 3:
            newPitch = headPitch + elevation * 2
        if abs(bearing) > 3:
            newYaw = headYaw + bearing * 2
        misty.move_head(newPitch, 0, newYaw)
        detect_emotion_basic()


def detect_emotion_basic():
    global emotion
    result = misty.take_picture(base64=True, width=800, height=600)
    b64 = result.json()['result']['base64']
    nparr = np.fromstring(base64.b64decode(b64), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    analysis = DeepFace.analyze(img, actions="emotion")
    emotion = analysis[0]["dominant_emotion"]
    if settings["mimicEmotion"]:
        display_emotion(emotion)  # mimic detected emotion
    print(emotion)


def display_emotion(emotion):
    global displayed_emotion
    if displayed_emotion == emotion:
        return
    match emotion:
        case "neutral":
            misty.display_image("e_DefaultContent.jpg")
        case "sad":
            misty.display_image("e_Sadness.jpg")
        case "angry":
            misty.display_image("e_Anger.jpg")
        case "surprised":
            misty.display_image("e_Surprise.jpg")
        case "fear":
            misty.display_image("e_Fear.jpg")
        case "happy":
            misty.display_image("e_Joy.jpg")
        case "disgust":
            misty.display_image("e_Disgust.jpg")
    displayed_emotion = emotion


def update_position_head(event):
    global headYaw
    global headPitch
    if "message" in event:
        message = event["message"]
        if message["sensorId"] == "ahy":
            headYaw = message["value"]
        if message["sensorId"] == "ahp":
            headPitch = message["value"]


def update_position_body(event):
    global bodyYaw
    if "message" in event:
        message = event["message"]
        bodyYaw = message["yaw"]


def start_session():
    misty.stop_object_detector()
    misty.stop_face_detection()
    misty.unregister_all_events()
    misty.start_action("body-reset", useVisionData=False)
    # misty.register_event(Events.VoiceRecord, "voicerecord", callback_function=voice_record_complete)
    misty.register_event(Events.AudioPlayComplete, "ttscomplete", callback_function=tts_complete)
    # misty.register_event(Events.TextToSpeechComplete, "ttscomplete2", keep_alive=True, callback_function=tts_complete)
    misty.register_event(Events.ActuatorPosition, "actuatorposition", keep_alive=True,
                         callback_function=update_position_head)
    misty.register_event(Events.FaceRecognition, "facedetection", keep_alive=True, debounce=1000,
                         callback_function=look_at_face)
    # misty.register_event(Events.SourceTrackDataMessage, "audiolocalization", keep_alive=True, debounce=2000, callback_function=look_at_audio)
    misty.register_event(Events.IMU, "imu", keep_alive=True, debounce=1000, callback_function=update_position_body)
    print("starting session")
    misty.cancel_skill("cloud_connector")
    if settings["useScript"]:
        speak(script.get_text())
    else:
        speak("Hallo! Wat leuk dat je even de tijd neemt om met me te praten. Mijn naam is Misty, wat is jouw naam?")
    misty.start_face_detection()


start_session()

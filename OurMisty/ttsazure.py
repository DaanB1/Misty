
import azure.cognitiveservices.speech as speechsdk
import base64
import time

class CustomSpeak():

    def __init__(self, misty, speech_key, service_region, male=True):
        self.audiofile = "outputaudio.wav"
        speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
        # Set the voice name, refer to https://aka.ms/speech/voices/neural for full list.
        if male:
            speech_config.speech_synthesis_voice_name = "nl-NL-MaartenNeural"
        else:
            speech_config.speech_synthesis_voice_name = "nl-NL-FennaNeural"
        self.speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)
        self.misty = misty

    def speak(self, text, **kwargs):
        result = self.speech_synthesizer.speak_text_async(text).get()
        stream = speechsdk.AudioDataStream(result)
        stream.save_to_wav_file(self.audiofile)

        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            enc = base64.b64encode(open(self.audiofile, "rb").read()).decode()
            self.misty.save_audio(self.audiofile, data=enc, overwriteExisting=True, immediatelyApply=True)
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print("Speech synthesis canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                if cancellation_details.error_details:
                    print("Error details: {}".format(cancellation_details.error_details))
            print("Did you update the subscription info?")




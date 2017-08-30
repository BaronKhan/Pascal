from src import houndify
from src import client_defines
from src import client_matches
from src import pygame_gdt as gdt
from gtts import gTTS
import RPi.GPIO as GPIO
import os
import sys
import wave
import random
import signal
import snowboydecoder
import time
import pygame
import pprint
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--gui", help="display the GUI",
                    action="store_true")
parser.add_argument("--full", help="start in fullscreen mode",
                    action="store_true")
args = parser.parse_args()

using_gui = False
start_fullscreen = False
screen = None

if args.gui:
    print("GUI turned on")
    using_gui = True
else:
    print("GUI turned off")

if args.full:
    print("Starting in fullscreen mode")
    start_fullscreen = True
else:
    print("Starting in windowed mode")

if using_gui:
    pygame.init()

voice_lang="-ven-us"
voice_speed="-s175" # default: 175
voice_type="m7"     # current: m7
voice_gap=""        # default: -g10

BUFFER_SIZE = 512

name = "pascal"

interrupted = False
detected = False
error = False
arc_pos = 0.0

def on_client_match(intent):
    global interrupted, screen
    print("Client match detected, executing "+str(intent)+" intent...")
    if intent == "SHUTDOWN":
        interrupted = True
    elif intent == "FULLSCREEN_START":
        if using_gui:
            screen = pygame.display.set_mode((640,480), pygame.FULLSCREEN)
    elif intent == "FULLSCREEN_STOP":
        if using_gui:
            screen = pygame.display.set_mode((640,480))

def play_random_error():
    error_reponses =    [
                            "I'm sorry. I didn't catch that.",
                            "Could you repeat, please?",
                            "I'm sorry. I didn't understand that.",
                            "Can you see that again, please?",
                            "Sorry, I didn't quite hear you just now."
                        ]
    play_voice(random.choice(error_reponses))

class MyListener(houndify.HoundListener):
    def onPartialTranscript(self, transcript):
        global screen, arc_pos
        print("Partial transcript: " + transcript)
        if using_gui:
            font_comic = pygame.font.SysFont("comicsansms", 24)
            screen.fill((0,0,0))
            pt_text = font_comic.render(transcript, 1, (255,255,0))
            screen.blit(pt_text, (320 - pt_text.get_width()//2, 30))
            pygame.draw.arc(screen, (89,136,255), (220,140,200,200), arc_pos+0.628, arc_pos+5.645, 10)
            pygame.display.update()
            arc_pos += 0.1

    def onFinalResponse(self, response):
        global screen
        if using_gui:
            screen.fill((0,0,0))
        print("Final response:")
        pp = pprint.PrettyPrinter()
        pp.pprint(response)
        if len(response["AllResults"]) > 0:
            responseSpeech = ""
            if "SpokenResponseLong" in response["AllResults"][0]:
                responseSpeech = response["AllResults"][0]["SpokenResponseLong"]
            else:
                responseSpeech = response["AllResults"][0]["WrittenResponseLong"]
            if responseSpeech != "Didn't get that!":
                play_voice(responseSpeech)

                # Execute client match
                if "Result" in response["AllResults"][0]:
                    if "Intent" in response["AllResults"][0]["Result"]:
                        on_client_match(response["AllResults"][0]["Result"]["Intent"])
            else:
                play_random_error()
        else:
            play_random_error()

    def onError(self, err):
        global error
        print("Error: " + str(err))
        error = True

def group_words(s, n):
    words = s.split()
    for i in range(0, len(words), n):
        yield ' '.join(words[i:i+n])

def play_voice(voice_text):
    # gTTS
    tts = gTTS(text=voice_text, lang='en-uk')
    tts.save("response.mp3")
    os.system("play response.mp3")
    os.remove("response.mp3")

def test_voice():
    voice_text = "Hello. I am "+name+". Nice to meet you."
    play_voice(voice_text)
    voice_text = "The temperature is sixteen degrees celsius."
    play_voice(voice_text)
    voice_text = "I am sorry to hear that, but I am just a robot."
    play_voice(voice_text)

def run_voice_request(client):
    global interrupted, error, arc_pos, partial_transcript
    i = 0
    finished = False
    arc_pos = 0.0
    try:
        client.start(MyListener())
        os.system("amixer sset PCM mute")
        GPIO.output(18,GPIO.HIGH)
        print("Starting voice control")
        if using_gui:
            font_comic = pygame.font.SysFont("comicsansms", 72)
            screen.fill((0,0,0))
            help_text = font_comic.render("How may I help you?", 1, (89,136,255))
            screen.blit(help_text, (320 - help_text.get_width()//2, 180 - help_text.get_height()//2))
            pygame.display.update()
        while not finished and i<5:
            os.system("arecord temp"+str(i)+".wav -D sysdefault:CARD=1 -r 16000 -f S16_LE -d 1")
            audio = wave.open("temp"+str(i)+".wav")
            samples = audio.readframes(BUFFER_SIZE)
            while len(samples) != 0 and not finished:
                finished = client.fill(samples)
                samples = audio.readframes(BUFFER_SIZE)
            audio.close()
            os.remove("temp"+str(i)+".wav")
            i+=1
        os.system("amixer sset PCM unmute")
        client.finish()
        if error:
            interrupted = True
            raise Exception("Error")
        GPIO.output(18,GPIO.LOW)
        print("Finished voice control")
    except:
        GPIO.output(18,GPIO.LOW)
        os.system("amixer sset PCM unmute")
        interrupted = True

def signal_handler(signal, frame):
    global interrupted
    interrupted = True

def detection_callback():
    global detected
    detected = True
    os.system("play resources/dong.wav")

def interrupt_callback():
    global interrupted, detected
    return interrupted or detected

if __name__ == '__main__':
    if using_gui:
        if start_fullscreen:
            screen = pygame.display.set_mode((640,480),pygame.FULLSCREEN)
        else:
            screen = pygame.display.set_mode((640,480))

    print("client id: "+client_defines.CLIENT_ID+"\nclient key: "+client_defines.CLIENT_KEY)

    play_voice("Hello.")

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(18,GPIO.OUT)

    client = houndify.StreamingHoundClient(client_defines.CLIENT_ID, client_defines.CLIENT_KEY, "ai_robot")
    client.setLocation(51.654022,-0.038691)
    client.setHoundRequestInfo('ClientMatches', client_matches.clientMatches)
    client.setHoundRequestInfo('UnitPreference', 'METRIC')
    client.setHoundRequestInfo('FirstPersonSelf', name)
    client.setSampleRate(16000)

    signal.signal(signal.SIGINT, signal_handler)

    models = ["pascal_model.umdl", "hello_model.umdl", "hi_model.umdl"]
    sensitivity = [0.41, 0.1, 0.35]

    if not len(models) == len(sensitivity):
        raise AssertionError()

    while not interrupted:
        detected = False
        detector = snowboydecoder.HotwordDetector(models, sensitivity=sensitivity)
        callbacks = [lambda: detection_callback(),
                     lambda: detection_callback(),
                     lambda: detection_callback()]
        print('Listening... Press Ctrl+C to exit')
        if using_gui:
            pygame.draw.circle(screen, (89,136,255), (320,240), 100, 10)
            pygame.display.update()
        detector.start(detected_callback=callbacks,
                       interrupt_check=interrupt_callback,
                       sleep_time=0.03)
        detector.terminate()
        if not interrupted:
            run_voice_request(client)

    if error:
        play_voice("I'm very sorry, but I've had enough for today. Goodbye.")
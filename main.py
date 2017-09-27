from src import houndify
from src import client_defines
from src import client_matches
from src import client_state
from src import snowboydecoder
from src import pygame_gdt as gdt
from src import transmit_rf as rf
from gtts import gTTS
import RPi.GPIO as GPIO
import os
import sys
import wave
import random
import signal
import time
import pygame
import pprint
import argparse
import pyaudio
import textwrap

using_gui = False
start_fullscreen = False
screen = None

voice_lang="-ven-us"
voice_speed="-s200" # default: 175
voice_type="m7"     # current: m7
voice_gap=""        # default: -g10

BUFFER_SIZE = 2048

name = "pascal"

interrupted = False
detected = False
error = False
arc_pos = 0.0
first_time = True

# RF signals
a_on =  '1110111110101010110011001'
a_off = '1110111110101010110000111'
b_on =  '1110111110101010001111001'
b_off = '1110111110101010001100111'
c_on =  '1110111110101000111111001'
c_off = '1110111110101000111100111'
d_on =  '1110111110100010111111001'
d_off = '1110111110100010111100111'
e_on =  '1110111110001010111111001'
e_off = '1110111110001010111100111'

# Custom RF signals
f_on =  '1111111111110101010101111'
f_off = '1111111111111010101010000'

# Devices
DEVICE_NIGHT_LIGHT = 1 # Yes, I have a night light. Don't judge me.
DEVICE_BED_LAMP = 2
DEVICE_FAN = 3
DEVICE_LIGHT = 4
DEVICE_LIGHTS = 5

parser = argparse.ArgumentParser()
parser.add_argument("--gui", help="display the GUI",
                    action="store_true")
parser.add_argument("--full", help="start in fullscreen mode",
                    action="store_true")
parser.add_argument('-t', '--text', type=str, help='execute a text string command')
args = parser.parse_args()

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
    pygame.mouse.set_visible(False)

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

def on_home_automation(device_id, operation):
    if device_id == DEVICE_NIGHT_LIGHT:
        if operation == "TurnOn":
            rf.transmit_code(a_on)
        elif operation == "TurnOff":
            rf.transmit_code(a_off)
    elif device_id == DEVICE_BED_LAMP:
        if operation == "TurnOn":
            rf.transmit_code(b_on)
        elif operation == "TurnOff":
            rf.transmit_code(b_off)
    elif device_id == DEVICE_FAN:
        if operation == "TurnOn":
            rf.transmit_code(c_on)
        elif operation == "TurnOff":
            rf.transmit_code(c_off)
    elif ((device_id == DEVICE_LIGHT) or
        (device_id == DEVICE_LIGHTS)):
        if operation == "TurnOn":
            rf.transmit_code(f_on)
        elif operation == "TurnOff":
            rf.transmit_code(f_off)
    else:
        return False
    return True

def play_voice(voice_text):
    print("|"+str(voice_text)+"|")
    if using_gui:
        font_comic = pygame.font.SysFont("comicsansms", 36)
        # Split text into lines of 45 characters
        voice_text_list = textwrap.wrap(voice_text, 55, break_long_words=False)
        i=0
        for voice_text_chunk in voice_text_list:
            voice_str = font_comic.render(voice_text_chunk, 1, (255,255,255))
            screen.blit(voice_str, (320 - voice_str.get_width()//2, 370+(voice_str.get_height()*i)))
            i+=1
        pygame.display.update()
    # gTTS
    tts = gTTS(text=voice_text, lang='en-uk')
    tts.save("response.mp3")
    os.system("play response.mp3")
    os.remove("response.mp3")

def play_random_error():
    error_reponses =    [
                            "I'm sorry. I didn't catch that.",
                            "Could you repeat, please?",
                            "I'm sorry. I didn't understand that.",
                            "Can you see that again, please?",
                            "Sorry, I didn't quite hear you just now."
                        ]
    play_voice(random.choice(error_reponses))

def do_final_response(response):
    global screen
    if not using_gui:
        print("Final response:")
        pp = pprint.PrettyPrinter()
        pp.pprint(response)
    if len(response["AllResults"]) > 0:
            first_result = response["AllResults"][0]
            if ("CommandKind" in first_result) and (first_result["CommandKind"] == "HomeAutomationControlCommand"):
                if "DeviceSpecifier" in first_result and len(first_result["DeviceSpecifier"]["Devices"]) > 0:
                    success = on_home_automation(int(first_result["DeviceSpecifier"]["Devices"][0]["ID"]), first_result["Operation"])
                    if success:
                        responseSpeech = first_result["ClientActionSucceededResult"]["SpokenResponseLong"]
                        play_voice(responseSpeech)
                    else:
                        play_voice("I'm sorry, I currently cannot access this device.")
            else:
                responseSpeech = ""
                if "SpokenResponseLong" in first_result:
                    responseSpeech = first_result["SpokenResponseLong"]
                else:
                    responseSpeech = first_result["WrittenResponseLong"]
                if ((responseSpeech != "Didn't get that!") and
                ("Home Automation commands" not in responseSpeech)):
                    play_voice(responseSpeech)

                    # Execute client match
                    if "Result" in first_result:
                        if "Intent" in first_result["Result"]:
                            on_client_match(first_result["Result"]["Intent"])
                else:
                    play_random_error()
    else:
        play_random_error()

class MyListener(houndify.HoundListener):
    def onPartialTranscript(self, transcript):
        global screen, arc_pos
        if using_gui:
            font_comic = pygame.font.SysFont("comicsansms", 28)
            screen.fill((0,0,0))
            pt_text = font_comic.render(transcript, 1, (255,255,255))
            screen.blit(pt_text, (320 - pt_text.get_width()//2, 30))
            pygame.draw.arc(screen, (89,136,255), (220,140,200,200), arc_pos+0.628, arc_pos+5.645, 10)
            pygame.display.update()
            arc_pos += 0.1
        else:
            print("Partial transcript: " + transcript)

    def onFinalResponse(self, response):
        do_final_response(response)

    def onError(self, err):
        global error
        print("Error: " + str(err))
        error = True

def test_voice():
    voice_text = "Hello. I am "+name+". Nice to meet you."
    play_voice(voice_text)
    voice_text = "The temperature is sixteen degrees celsius."
    play_voice(voice_text)
    voice_text = "I am sorry to hear that, but I am just a robot."
    play_voice(voice_text)

def run_voice_request(client):
    global interrupted, error, arc_pos, partial_transcript, first_time
    finished = False
    arc_pos = 0.0
    try:
        # Send device list to Houndify
        if first_time:
            textClient = houndify.TextHoundClient(client_defines.CLIENT_ID, client_defines.CLIENT_KEY, "ai_robot")
            textClient.setHoundRequestInfo('ClientState', client_state.clientState)
            response = textClient.query("index_user_devices_from_request_info")
            pp = pprint.PrettyPrinter()
            pp.pprint(response)
            print("Devices sent successfully")
            first_time = False

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

        audio = pyaudio.PyAudio()
        stream = audio.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=BUFFER_SIZE)
        for i in range(0, int(16000 / BUFFER_SIZE * 5)):
            data = stream.read(BUFFER_SIZE)
            finished = client.fill(data)
            if finished:
                break
        stream.stop_stream()
        stream.close()
        audio.terminate()

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
    if args.text:
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(18,GPIO.OUT)
        textClient = houndify.TextHoundClient(client_defines.CLIENT_ID, client_defines.CLIENT_KEY, "ai_robot")
        textClient.setHoundRequestInfo('ClientState', client_state.clientState)
        response = textClient.query("index_user_devices_from_request_info")
        pp = pprint.PrettyPrinter()
        pp.pprint(response)
        print("Devices sent successfully")
        response = textClient.query(args.text)
        do_final_response(response)
        GPIO.cleanup()
        exit(0)

    if using_gui:
        if start_fullscreen:
            screen = pygame.display.set_mode((640,480),pygame.FULLSCREEN)
        else:
            screen = pygame.display.set_mode((640,480))

    print("client id: "+client_defines.CLIENT_ID+"\nclient key: "+client_defines.CLIENT_KEY)

    if using_gui:
            pygame.draw.arc(screen, (89,136,255), (220,140,200,200), 2.199, 7.216, 10)
            pygame.draw.lines(screen, (89,136,255), False, [(290,120), (290,200)], 10)
            pygame.draw.lines(screen, (89,136,255), False, [(350,120), (350,200)], 10)
            pygame.display.update()

    play_voice("Hello. I am Pascal.")

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

    models = ["pascal_model.umdl", "pascal_female_model.umdl", "hello_model.umdl", "hi_model.umdl"]
    sensitivity = [0.43, 0.41, 0.1, 0.35]

    if not len(models) == len(sensitivity):
        raise AssertionError()

    while not interrupted:
        detected = False
        detector = snowboydecoder.HotwordDetector(models, sensitivity=sensitivity)
        callbacks = [lambda: detection_callback(),
                     lambda: detection_callback(),
                     lambda: detection_callback(),
                     lambda: detection_callback()]
        print('Listening... Press Ctrl+C to exit')
        if using_gui:
            screen.fill((0,0,0))
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

    GPIO.cleanup()
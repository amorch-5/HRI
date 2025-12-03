# RUN WITH PYTHON 3.9. SHOULD LOOK SOMETHING LIKE THE BELOW
#  & C:/Users/alex/AppData/Local/Programs/Python/Python39/python.exe c:/Users/alex/Documents/Programming/python/CS436/Lab9/project/nao_tts.py

import time
from naoqi import ALProxy
import qi
import math
import random


tts = ALProxy

ip = "10.60.218.114"

# text to speech proxy
tts = ALProxy("ALTextToSpeech",ip , 9559)

# mood proxy
mood = ALProxy("ALMood", ip, 9559)
session = qi.Session()
session.connect("tcp://" + ip + ":9559")
mood = session.service("ALMood")

# animated speech proxy
animated_speech = ALProxy("ALAnimatedSpeech",ip, 9559)

# posture proxy
posture_proxy = ALProxy("ALRobotPosture", ip, 9559)

current_posture = posture_proxy.getPosture()

text_old = ""

# posture_proxy.goToPosture("StandInit", 1.0)

# tracker proxy
tracker = ALProxy("ALTracker", ip, 9559)
frame = 2
speed = 0.5
use_whole_body = False
# target_position = [1.0, 0.0, 0.0]
# tracker.lookAt(target_position, frame, speed, use_whole_body)

# # Sound function
# def sound_located_callback(key, value):
#     azimuth = value[1][0]
#     elevation = value[1][1]
#     print(azimuth, elevation)

# Memory proxy
memory = ALProxy("ALMemory", ip, 9559)
soundLoc = ALProxy("ALSoundLocalization", ip, 9559)
soundLoc.subscribe("SoundLocated")



# if current_posture != "Stand":
#     # Make NAO stand up
#     posture_proxy.goToPosture("StandInit", 1.0)

with open("listen.txt", "w") as f:
    f.write("no")

with open("response.txt", "w") as f:
    f.write(" ")

while True:
    try:
        data = memory.getData("ALSoundLocalization/SoundLocated")
        azimuth = data[1][0]
        elevation = data[1][1]
        confidence = data[1][2]

        sound_x = math.cos(elevation) * math.cos(azimuth)
        sound_y = math.cos(elevation) * math.sin(azimuth)
        sound_z = math.sin(elevation) + 1

        # personmood = mood.currentPersonState()['smile']
        # print("Current person state: ", personmood)

        with open("response.txt", "r") as f:
            text = f.read().replace('\n', ' ')


        # random_look = random.randint(1,100)
        # if random_look > 90:
        #     target_position = [1, 0.3, -0.5]
        #     print("Looking at hand")
        #     tracker.lookAt(target_position, frame, speed, use_whole_body)
        #     fillers = ["Mm-hmm", "uh huh", "okay", "I see"]
        #     speech = animated_speech.say("^start(animations/Stand/Gestures/Explain_11) " + random.choice(fillers))
            
        # else:
        #     if confidence < 0.8:
        #         target_position = [sound_x, sound_y, sound_z]
        #         print("Target Pos:", target_position)
        #         tracker.lookAt(target_position, frame, speed, use_whole_body)


        # have the NAO speak ChatGPT's response
        if text != "":
            if text != text_old:
                animated_speech.say(text)
                print(text)
                text_old = text
                with open("listen.txt", "w") as f:
                    f.write("yes")
                
        time.sleep(1)
    except Exception as e:
        print("An error occurred: ", e)
        time.sleep(1)

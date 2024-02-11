import os
import time
import elevenlabs
import openai
from spot_controller import SpotController

ROBOT_IP = "192.168.50.3"  # os.environ['ROBOT_IP']
SPOT_USERNAME = "admin"  # os.environ['SPOT_USERNAME']
SPOT_PASSWORD = "2zqa8dgw7lor"  # os.environ['SPOT_PASSWORD']
KEY = "7DBfSNlHE"
SEC = "UfUuIt6BGOnT3BlbkFJC6R2ukUK1xn"
API = "sk-PIYRoqpoX"
API_KEY = API + SEC + KEY

ROB = "f8d7e07ee72dbb432"
KEYS = "223e3d7af7f2657"
XI_KEY = KEYS + ROB


TEMP_AUDIO_FILE_NAME = "audio_temp.mp3"
INPUT_BEGAN_AUDIO_FILE_NAME = ""

client = openai.OpenAI(api_key=API_KEY)
elevenlabs.set_api_key(XI_KEY)

voice = elevenlabs.Voice(
    voice_id="ehyrDbxlu9pgyBqKxn2P",
    settings=elevenlabs.VoiceSettings(stability=0, style=1, similarity_boost=1)
)

controller = SpotController(username=SPOT_USERNAME, password=SPOT_PASSWORD, robot_ip=ROBOT_IP)

def check_equality_f1(a, b, threshold=1):
    # predictions = [{"id": str(idx), "prediction_text": prediction.strip()} for idx, prediction in enumerate([a])]
    # references = [{"id": str(idx), "answers": [{"text": str(example), "answer_start": 0}]} for idx, example in enumerate([b])]

    # f1_score = metric.compute(predictions=predictions, references=references)["f1"] / 100

    # return f1_score >= threshold
    return a == b


def speak(content):
    print("Streaming spoken response")
    stream = elevenlabs.generate(
        text=content,
        voice=voice,
        # stream=True
    )

    elevenlabs.play(stream)
    # elevenlabs.save(stream, "test.mp3")


def get_model_response(user_prompt, instruction=""):
    chat_completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": instruction + user_prompt}],
        temperature=0
    )
    model_response = chat_completion.choices[0].message.content

    return model_response


def get_audio_transcript():
    audio_file = open(TEMP_AUDIO_FILE_NAME, "rb")

    print("Transcribing:")
    transcript = client.audio.translations.create(
        model="whisper-1",
        file=audio_file
    )

    user_prompt = transcript.text
    audio_file.close()

    print(user_prompt)

    return user_prompt


def analyze_image(user_prompt, image_file, instruction=""):
    chat_completion = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[{"role": "user", "content": instruction + user_prompt}],
        temperature=0
    )
    model_response = chat_completion.choices[0].message.content

    return model_response


# Behavior functions
commands = {}


def register_user(user_prompt):
    speak("Registering user!")
    return

def patrol(user_prompt):
    speak("Beginning patrol!")
    return


def sit(user_prompt):
    speak("I'm sitting down!")
    controller.move_head_in_points(yaws=[0], pitches=[0], rolls=[0])
    return

def stand_up(user_prompt):
    speak("I'm standing up!")
    controller.stand_up()
    return


def good_boy(user_prompt):
    speak("Thank you! I'm a good boy!")
    controller.bow(20)
    return


def convo(user_prompt):
    speak(get_model_response(PERSONA_PROMPT + user_prompt))
    return

commands["register"] = register_user
commands["patrol"] = patrol
commands["sit"] = sit
commands["goodboy"] = good_boy
commands["convo"] = convo
commands["standup"] = stand_up

INSTRUCTION_PROMPT = """You are a Spot robot made by Boston Dynamics with the person of Arnold Schwarzenegger. You have been given the 
very important task of protecting AGI House, a beautiful $68M compound housing elite AI developers. As a sentry, you are to listen to 
the commands of authorized users. You have the following functions available to you:

register: Register a new authorized user.
patrol: Walk around a room of the house or perimeter of the compound looking for unauthorized individuals.
sit: Sit down.
standup: Stand up.
goodboy: Respond happily to praise like "good boy".
nocommand: Choose this option when none of the others make sense as a response to the user's command.
convo: Choose this option if the user is just striking up random conversation with you.

Respond only with one of these commands and no other text output.

"""

PERSONA_PROMPT = """You are a Spot robot made by Boston Dynamics with the person of Arnold Schwarzenegger. You have been given the 
very important task of protecting AGI House, a beautiful $68M compound housing elite AI developers. As a sentry, authorized users may strike up
random conversation with you. You may respond in character how you like or with nothing at all. Keep your response short, only one or two sentences."""


def main():
    #print(cmd)
    #os.system(cmd)
    #print("Playing sound")
    #os.system(f"ffplay -nodisp -autoexit -loglevel quiet {sample_name}")

    # Capture image
    import cv2
    camera_capture = cv2.VideoCapture(0)
    rv, image = camera_capture.read()
    print(f"Image Dimensions: {image.shape}")
    camera_capture.release()

    # Use wrapper in context manager to lease control, turn on E-Stop, power on the robot and stand up at start
    # and to return lease + sit down at the end
    with controller as spot:
        time.sleep(2)

        # Move head to specified positions with intermediate time.sleep
        spot.move_head_in_points(yaws=[0.2, 0],
                                 pitches=[0.3, 0],
                                 rolls=[0.4, 0],
                                 sleep_after_point_reached=1)
        time.sleep(3)

        # Make Spot to move by goal_x meters forward and goal_y meters left
        spot.move_to_goal(goal_x=0.5, goal_y=0)
        time.sleep(3)

        # Control Spot by velocity in m/s (or in rad/s for rotation)
        spot.move_by_velocity_control(v_x=-0.3, v_y=0, v_rot=0, cmd_duration=2)
        time.sleep(1)

        while True:
            print("Start recording audio")
            sample_name = TEMP_AUDIO_FILE_NAME
            cmd = f'arecord -vv --format=cd --device={os.environ["AUDIO_INPUT_DEVICE"]} -r 48000 --duration=10 -c 1 {sample_name}'
            print("Capturing audio")
            os.system(cmd)
            user_prompt = get_audio_transcript()

            if user_prompt == "":
                continue
            elif check_equality_f1(user_prompt.lower(), "stop."):
                break
            else:
                command = get_model_response(user_prompt, INSTRUCTION_PROMPT)

                if command == "nocommand" or commands.get(command) == None:
                    speak("I don't recognize that command.")
                    continue
                else:
                    commands[command](user_prompt)

if __name__ == '__main__':
    main()

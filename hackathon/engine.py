import openai, elevenlabs
import speech_recognition as sr
import threading
import evaluate
from dotenv import load_dotenv
import os
# import robot

load_dotenv()

OAI_API = os.getenv("OPENAI_API_KEY")
XIL_API = os.getenv("XI_API_KEY")

TEMP_AUDIO_FILE_NAME = "audio_temp.mp3"
INPUT_BEGAN_AUDIO_FILE_NAME = ""

client = openai.OpenAI(api_key=OAI_API)

elevenlabs.set_api_key(XIL_API)

# Loop: User speech -> transcribe -> LLM response -> spoken response
recorder = sr.Recognizer()
metric = evaluate.load("squad")

# Helpers
def check_equality_f1(a, b, threshold=1):
    predictions = [{"id": str(idx), "prediction_text": prediction.strip()} for idx, prediction in enumerate([a])]
    references = [{"id": str(idx), "answers": [{"text": str(example), "answer_start": 0}]} for idx, example in enumerate([b])]
    
    f1_score = metric.compute(predictions=predictions, references=references)["f1"] / 100

    if f1_score >= threshold:
        return True
    
    return False

def speak(content):
    print("Streaming spoken response")
    stream = elevenlabs.generate(
        text = content,
        voice = "InspectorMax",
        model = "eleven_multilingual_v2",
        # stream=True
    )

    elevenlabs.play(stream)
    elevenlabs.save(stream)

# speak("TEST")

def get_model_response(user_prompt, instruction = ""):
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

def register_user():
    speak("Registering user!")
    return

def patrol():
    speak("Beginning patrol!")
    return

def sit():
    speak("Sitting down!")
    # robot.sit()
    return

def good_boy():
    speak("I'm a good boy!")
    return

commands["register"] = register_user
commands["patrol"] = patrol
commands["sit"] = sit
commands["goodboy"] = good_boy

INSTRUCTION_PROMPT = """You are a Spot robot made by Boston Dynamics. You have been given the very important task of protecting AGI House,
a beautiful $68M compound housing elite AI developers. As a sentry, you are to listen to the commands of authorized users. You have the 
following functions available to you:

register: Register a new authorized user.
patrol: Walk around a room of the house or perimeter of the compound looking for unauthorized individuals.
sit: Sit down.
goodboy: Respond happily to praise like "good boy".
nocommand: Choose this option when none of the others make sense as a response to the user's command.

Respond only with one of these commands and no other text output.

"""

with sr.Microphone() as source:
    recorder.adjust_for_ambient_noise(source)

# Input loop
while True:
    print("Capturing audio")
    # winsound.PlaySound(INPUT_BEGAN_FILE_NAME, winsound.SND_FILENAME)

    with sr.Microphone() as source: 
        audio = recorder.listen(source)

    with open(TEMP_AUDIO_FILE_NAME, "wb") as f:
        f.write(audio.get_wav_data())
        f.close()

    user_prompt = get_audio_transcript()

    if user_prompt == "":
        continue
    elif check_equality_f1(user_prompt.lower(), "stop."):
        break
    else:
        command = get_model_response(user_prompt, INSTRUCTION_PROMPT)

        if command == "nocommand" or commands.get(command) == None:
            continue
        else:
            t = threading.Thread(target=commands[command], args=())
            t.start()
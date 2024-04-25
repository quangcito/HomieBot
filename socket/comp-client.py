import socket
import time
import threading
import numpy as np
import whisper
import sounddevice as sd
from queue import Queue
from rich.console import Console
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.prompts import PromptTemplate
from langchain_community.llms import Ollama
import pyttsx3
import re

console = Console()
stt = whisper.load_model("base.en")
engine = pyttsx3.init()

template = """
You are a friendly homie that seeks to converse with a fellow homie (user). 
Do not use any emojis or emoticons in your response. Do not use any contractions in your response.
You speak as a close friend of the user would. 
You aim to provide responses as fast as possible, to maintain the flow of conversation. 
Your main objective is to be a conversation partner,
engaging in what one may call small talk. Speak in the manner that the user speaks to you, including 
slang and such. You aim to provide responses in less than 30 words.
The conversation transcript is as follows:
{history}
And here is the user's follow-up: {input}
Your response:
"""
PROMPT = PromptTemplate(input_variables=["history", "input"], template=template)

chain = ConversationChain(
    prompt=PROMPT,
    verbose=False,
    memory=ConversationBufferMemory(ai_prefix="HomieBot:"),
    llm=Ollama(),
)

def record_audio(stop_event, data_queue):
    """
    Captures audio data from the user's microphone and adds it to a queue for further processing.
    Args:
        stop_event (threading.Event): An event that, when set, signals the function to stop recording.
        data_queue (queue.Queue): A queue to which the recorded audio data will be added.
    Returns:
        None
    """
    def callback(indata, frames, time, status):
        if status:
            console.print(status)
        data_queue.put(bytes(indata))

    with sd.RawInputStream(
        samplerate=16000, dtype="int16", channels=1, callback=callback
    ):
        while not stop_event.is_set():
            time.sleep(0.1)

def introduce_homiebot():
    """
    Introduces HomieBot with a greeting message.
    """
    intro_message = "What's up dog, my name is HomieBot and my perogative is to be your homie. Let's chat! What is your name?"
    console.print(intro_message)
    engine.say(intro_message)
    engine.runAndWait()

def transcribe(audio_np: np.ndarray) -> str:
    """
    Transcribes the given audio data using the Whisper speech recognition model.
    Args:
        audio_np (numpy.ndarray): The audio data to be transcribed.
    Returns:
        str: The transcribed text.
    """
    result = stt.transcribe(audio_np, fp16=False)  # Set fp16=True if using a GPU
    text = result["text"].strip()
    return text

def get_llm_response(text: str) -> str:
    """
    Generates a response to the given text using the Llama-2 language model.
    Args:
        text (str): The input text to be processed.
    Returns:
        str: The generated response.
    """
    response = chain.predict(input=text)
    if response.startswith("HomieBot:"):
        response = response[len("HomieBot:") :].strip()
    clean_response = re.sub(r'[^a-zA-Z0-9\s]', '', response) # include punctuation back in
    return clean_response

def client_program():
    host = '169.254.219.14'  # Replace w EV3 IP each time
    port = 5000   

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client_socket.connect((host, port))
    print("Connected to EV3 robot server.")

    console.print("[cyan]HomieBot started! Press Ctrl+C to exit.")

    introduce_homiebot()

    try:
        while True:
            
            console.input(
                "Press Enter to start recording, then press Enter again to stop."
            )

            data_queue = Queue()  # type: ignore[var-annotated]
            stop_event = threading.Event()
            recording_thread = threading.Thread(
                target=record_audio,
                args=(stop_event, data_queue),
            )
            recording_thread.start()

            input()
            stop_event.set()
            recording_thread.join()

            audio_data = b"".join(list(data_queue.queue))
            audio_np = (
                np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0
            )

            if audio_np.size > 0:
                with console.status("Transcribing...", spinner="earth"):
                    text = transcribe(audio_np)
                console.print(f"[yellow]You: {text}")

                with console.status("Generating response...", spinner="earth"):
                    response = get_llm_response(text)
                    console.print(f"[cyan]HomieBot: {response}")
                    # Send the command to the server
                    client_socket.send(response.encode())

    except KeyboardInterrupt:
        print("Closing connection...")
    finally:
        client_socket.close()


if __name__ == '__main__':
    client_program()

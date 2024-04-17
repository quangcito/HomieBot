import asyncio
import time
import numpy as np
import whisper
import sounddevice as sd
from queue import Queue
from rich.console import Console
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.prompts import PromptTemplate
from langchain_community.llms import Ollama
from textToSpeech import TextToSpeechService

console = Console()
stt = whisper.load_model("base.en")  # Initialize the Whisper model for speech recognition
tts = TextToSpeechService()

template = """
You are a friendly companion that seeks to entertain conversation with a user. You speak as intimately as a close friend of the user would 
address them. You aim to provide responses as fast as possible, to maintain the flow of conversation. Your main objective is to be a conversation partner,
engaging in what one may call small talk. You aim to provide responses in less than 30 words.
The conversation transcript is as follows:
{history}
And here is the user's follow-up: {input}
Your response:
"""
PROMPT = PromptTemplate(input_variables=["history", "input"], template=template)
chain = ConversationChain(
    prompt=PROMPT,
    verbose=False,
    memory=ConversationBufferMemory(ai_prefix="Assistant:"),
    llm=Ollama(),
)

async def record_audio(stop_event, data_queue):
    def callback(indata, frames, time, status):
        if status:
            console.print(status)
        data_queue.put(bytes(indata))

    with sd.RawInputStream(
        samplerate=16000, dtype="int16", channels=1, callback=callback
    ):
        while not stop_event.is_set():
            await asyncio.sleep(0.1)

async def transcribe(audio_np: np.ndarray) -> str:
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, stt.transcribe, audio_np, False)  # Set fp16=True if using a GPU
    text = result["text"].strip()
    return text

async def get_llm_response(text: str) -> str:
    loop = asyncio.get_event_loop()
    response = await loop.run_in_executor(None, chain.predict, text)
    if response.startswith("Assistant:"):
        response = response[len("Assistant:") :].strip()
    return response

def play_audio(sample_rate, audio_array):
    sd.play(audio_array, sample_rate)
    sd.wait()

async def main():
    console.print("[cyan]Assistant started! Press Ctrl+C to exit.")

    try:
        while True:
            console.input(
                "Press Enter to start recording, then press Enter again to stop."
            )

            data_queue = Queue()
            stop_event = asyncio.Event()
            recording_task = asyncio.create_task(record_audio(stop_event, data_queue))

            input()
            stop_event.set()
            await recording_task

            audio_data = b"".join(list(data_queue.queue))
            audio_np = (
                np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0
            )

            if audio_np.size > 0:
                with console.status("Transcribing...", spinner="earth"):
                    text = await transcribe(audio_np)
                console.print(f"[yellow]You: {text}")

                with console.status("Generating response...", spinner="earth"):
                    response = await get_llm_response(text)

                console.print(f"[cyan]Assistant's response: {response}")
                sample_rate, audio_array = tts.long_form_synthesize(response)
                play_audio(sample_rate, audio_array)
            else:
                console.print(
                    "[red]No audio recorded. Please ensure your microphone is working."
                )

    except KeyboardInterrupt:
        console.print("\n[red]Exiting...")

    console.print("[blue]Session ended.")

if __name__ == "__main__":
    asyncio.run(main())
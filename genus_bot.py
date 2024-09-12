import os
import io
import time
import wave
import json
import requests
from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse
from moviepy.editor import VideoFileClip
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import google.cloud.speech as speech
import google.cloud.texttospeech as tts
import openai
from ibm_watson import ToneAnalyzerV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import datetime

# Initialize Flask app
app = Flask(__name__)

# Google Cloud setup for speech-to-text and text-to-speech
speech_client = speech.SpeechClient()
tts_client = tts.TextToSpeechClient()

# OpenAI API Key
openai.api_key = "your_openai_api_key"

# IBM Watson Tone Analyzer setup
authenticator = IAMAuthenticator('your_ibm_watson_api_key')
tone_analyzer = ToneAnalyzerV3(
    version='2021-08-01',
    authenticator=authenticator
)
tone_analyzer.set_service_url('your_ibm_watson_url')

# Buffer API setup
BUFFER_ACCESS_TOKEN = "your_buffer_access_token"
BUFFER_PROFILE_ID = "your_buffer_profile_id"
BUFFER_API_URL = "https://api.bufferapp.com/1/updates/create.json"

# Initialize conversation state storage (in-memory)
conversation_state = {}

# Directory to watch for new video files
WATCHED_DIR = "/path/to/your/video/folder"

# Function to extract audio from video
def extract_audio_from_video(video_path):
    clip = VideoFileClip(video_path)
    audio = clip.audio
    audio_path = video_path.replace('.mp4', '.wav')
    audio.write_audiofile(audio_path, codec='pcm_s16le')
    return audio_path

# Function to transcribe audio to text
def transcribe_audio(audio_content):
    audio = speech.RecognitionAudio(content=audio_content)
    config = speech.RecognitionConfig(
        language_code="en-US",
        sample_rate_hertz=16000,
        audio_channel_count=2
    )
    response = speech_client.recognize(config=config, audio=audio)
    return response.results[0].alternatives[0].transcript if response.results else ""

# Function to synthesize speech from text
def synthesize_speech(text):
    synthesis_input = tts.SynthesisInput(text=text)
    voice = tts.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Wavenet-D",
        ssml_gender=tts.SsmlVoiceGender.NEUTRAL
    )
    audio_config = tts.AudioConfig(
        audio_encoding=tts.AudioEncoding.MP3,
        pitch=2.0,
        speaking_rate=1.1
    )
    response = tts_client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
    return response.audio_content

# Function to analyze tone from text
def analyze_tone(text):
    tone_analysis = tone_analyzer.tone(
        {'text': text},
        content_type='application/json'
    ).get_result()
    return tone_analysis

# Function to interact with ChatGPT and generate captions
def ask_chatgpt_for_caption(transcript):
    prompt = f"""Create a social media caption for Facebook, Instagram, and TikTok that talks about how viewers can learn about this topic and more by clicking the link in the bio to get a free workbook to help them secure their first sale. Add a call to action to download the free workbook in the link in the bio.

Transcript: {transcript}"""
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response['choices'][0]['message']['content']

# Function to schedule a post with Buffer
def schedule_post(caption, media_url, post_time):
    headers = {
        "Authorization": f"Bearer {BUFFER_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "profile_ids": [BUFFER_PROFILE_ID],
        "text": caption,
        "media": {
            "link": media_url
        },
        "scheduled_at": post_time.timestamp()
    }
    response = requests.post(BUFFER_API_URL, headers=headers, json=data)
    return response.json()

# Function to handle new video files
class VideoHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return None
        
        if event.src_path.endswith('.mp4'):
            video_path = event.src_path
            print(f"New video detected: {video_path}")

            # Extract audio and transcribe
            audio_path = extract_audio_from_video(video_path)
            with io.open(audio_path, "rb") as audio_file:
                audio_content = audio_file.read()
            transcript = transcribe_audio(audio_content)
            print(f"Transcript: {transcript}")

            # Generate caption
            caption = ask_chatgpt_for_caption(transcript)
            print(f"Generated Caption: {caption}")

            # Determine next posting time
            now = datetime.datetime.now()
            post_time = now + datetime.timedelta(days=1)
            print(f"Scheduled Post Time: {post_time}")

            # Schedule post on Buffer
            media_url = f"URL_TO_YOUR_VIDEO/{os.path.basename(video_path)}"  # Adjust as needed
            response = schedule_post(caption, media_url, post_time)
            print(f"Buffer Response: {response}")

# Function to start the watcher
def start_watcher():
    event_handler = VideoHandler()
    observer = Observer()
    observer.schedule(event_handler, path=WATCHED_DIR, recursive=False)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

# Flask route to handle incoming Twilio calls
@app.route("/answer_call", methods=["POST"])
def answer_call():
    resp = VoiceResponse()
    resp.say("Hello! Thank you for calling. Please tell us what you are interested in.")
    resp.record(timeout=5, transcribe=False, play_beep=True, action="/process_caller_input")
    return str(resp)

# Flask route to process caller input
@app.route("/process_caller_input", methods=["POST"])
def process_caller_input():
    # Get the caller's recording URL from Twilio
    recording_url = request.form['RecordingUrl']
    recording_audio = requests.get(recording_url).content

    # Convert Twilio WAV format to Google-compatible byte stream
    audio_stream = io.BytesIO(recording_audio)
    with wave.open(audio_stream, 'rb') as wav_file:
        audio_content = wav_file.readframes(wav_file.getnframes())

    # Transcribe the caller's audio
    caller_transcription = transcribe_audio(audio_content)

    # Analyze tone
    tone_analysis = analyze_tone(caller_transcription)

    # Determine current state
    call_sid = request.form['CallSid']
    if call_sid not in conversation_state:
        conversation_state[call_sid] = {
            'state': 'intro',
            'context': "You are guiding the caller through a sales process. The goal is to understand their needs, confirm how our solution can help, discuss pricing, and get their email to send further details."
        }
    
    state = conversation_state[call_sid]['state']
    context = conversation_state[call_sid]['context']

    # Generate the response using ChatGPT
    bot_response = ask_chatgpt(caller_transcription, context)

    # Update state based on ChatGPT's guidance
    if 'interested' in caller_transcription.lower() and state == 'intro':
        conversation_state[call_sid]['state'] = 'pain'
    
    elif 'pain' in caller_transcription.lower() and state == 'pain':
        conversation_state[call_sid]['state'] = 'price'
    
    elif 'price' in caller_transcription.lower() and state == 'price':
        conversation_state[call_sid]['state'] = 'email'

    elif '@' in caller_transcription and state == 'email':
        bot_response = "Thank you! I've sent the details to your email. Is there anything else I can assist you with today?"
        conversation_state[call_sid]['state'] = 'end'

    # Synthesize speech for bot response
    audio_response = synthesize_speech(bot_response)

    # Send response and decide whether to continue or end the call
    resp = VoiceResponse()
    resp.play(audio_response)

    if conversation_state[call_sid]['state'] == 'end':
        resp.hangup()
    else:
        resp.record(timeout=5, transcribe=False, play_beep=True, action="/process_caller_input")

    return str(resp)

# Flask route to start autonomous video processing
@app.route("/start", methods=["GET"])
def start_autonomous_processing():
    start_watcher()
    return "Started watching folder for new videos."

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

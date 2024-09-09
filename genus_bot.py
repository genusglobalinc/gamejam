from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse
import openai
import google.cloud.speech as speech
import google.cloud.texttospeech as tts
from ibm_watson import ToneAnalyzerV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import requests
import io
import wave
import json

app = Flask(__name__)

# Google Cloud setup
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

# Initialize conversation state storage (in-memory for simplicity)
conversation_state = {}

# Function to transcribe audio to text (handling Twilio audio format)
def transcribe_audio(audio_content):
    audio = speech.RecognitionAudio(content=audio_content)
    config = speech.RecognitionConfig(
        language_code="en-US",
        sample_rate_hertz=8000,
        audio_channel_count=1
    )
    response = speech_client.recognize(config=config, audio=audio)
    return response.results[0].alternatives[0].transcript if response.results else ""

# Function to synthesize speech from text using WaveNet with inflections
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

# Function to interact with ChatGPT and adjust tone if necessary
def ask_chatgpt(caller_input, context):
    prompt = f"Conversation Context:\n{context}\n\nCaller said: '{caller_input}'\n\nWhat should be the agent's response to guide the conversation?"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a sales agent guiding the conversation through a structured sales process."},
            {"role": "user", "content": prompt}
        ]
    )
    return response['choices'][0]['message']['content']

# Flask route to handle the incoming call
@app.route("/answer_call", methods=["POST"])
def answer_call():
    resp = VoiceResponse()
    resp.say("Hello! Thank you for calling. Please tell us what you are interested in.")
    resp.record(timeout=5, transcribe=False, play_beep=True, action="/process_caller_input")
    return str(resp)

# Flask route to process the caller's response
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

    # Synthesize speech for bot response
    audio_response = synthesize_speech(bot_response)

    # Send response and continue conversation if necessary
    resp = VoiceResponse()
    resp.play(audio_response)
    resp.record(timeout=5, transcribe=False, play_beep=True, action="/process_caller_input")

    return str(resp)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

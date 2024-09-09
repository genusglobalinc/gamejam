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

# Function to transcribe audio to text (handling Twilio audio format)
def transcribe_audio(audio_content):
    # Twilio audio comes in 8kHz format, so configure Google STT accordingly
    audio = speech.RecognitionAudio(content=audio_content)
    config = speech.RecognitionConfig(
        language_code="en-US",
        sample_rate_hertz=8000,  # Twilio records in 8kHz format
        audio_channel_count=1  # Mono channel
    )
    response = speech_client.recognize(config=config, audio=audio)
    return response.results[0].alternatives[0].transcript if response.results else ""

# Function to synthesize speech from text using WaveNet with inflections
def synthesize_speech(text):
    synthesis_input = tts.SynthesisInput(text=text)
    
    # Use a WaveNet voice for more human-like qualities
    voice = tts.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Wavenet-D",  # WaveNet voice
        ssml_gender=tts.SsmlVoiceGender.NEUTRAL
    )

    # Apply some prosody changes to simulate natural human intonation
    audio_config = tts.AudioConfig(
        audio_encoding=tts.AudioEncoding.MP3,
        pitch=2.0,  # Slightly increase pitch
        speaking_rate=1.1  # Slightly faster speech rate for a lively tone
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
def ask_chatgpt(caller_input, tone):
    # Determine tone adjustment based on IBM Watson's tone analysis
    if tone and 'tones' in tone:
        dominant_tone = tone['tones'][0]['tone_id']
        if dominant_tone == 'sadness':
            tone_description = "You are a caring, empathetic sales agent."
        elif dominant_tone == 'anger':
            tone_description = "You are calm and understanding."
        elif dominant_tone == 'joy':
            tone_description = "You are friendly and enthusiastic."
        else:
            tone_description = "You are a helpful sales agent."
    else:
        tone_description = "You are a helpful sales agent."

    # Use ChatGPT to generate response based on the caller input
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": tone_description},
            {"role": "user", "content": caller_input}
        ]
    )
    return response['choices'][0]['message']['content']

# Flask route to handle the incoming call
@app.route("/answer_call", methods=["POST"])
def answer_call():
    # Start conversation with the caller
    resp = VoiceResponse()
    resp.say("Hello! Thank you for calling. Please tell us what you are interested in.")
    resp.record(timeout=5, transcribe=False, play_beep=True, action="/process_caller_input")
    return str(resp)

# Flask route to process the caller's response
@app.route("/process_caller_input", methods=["POST"])
def process_caller_input():
    # Get the caller's recording URL from Twilio
    recording_url = request.form['RecordingUrl']
    
    # Download the audio from Twilio
    recording_audio = requests.get(recording_url).content

    # Convert Twilio WAV format to Google-compatible byte stream
    audio_stream = io.BytesIO(recording_audio)
    with wave.open(audio_stream, 'rb') as wav_file:
        audio_content = wav_file.readframes(wav_file.getnframes())

    # Step 1: Transcribe the audio using Google STT
    caller_transcription = transcribe_audio(audio_content)

    # Step 2: Analyze tone using IBM Watson Tone Analyzer
    tone_analysis = analyze_tone(caller_transcription)

    # Step 3: Get bot response from ChatGPT based on transcription and tone
    bot_response = ask_chatgpt(caller_transcription, tone_analysis)

    # Step 4: Synthesize speech for bot response using Google WaveNet with inflection
    audio_response = synthesize_speech(bot_response)

    # Step 5: Play the response back to the caller
    resp = VoiceResponse()
    resp.play(audio_response)

    # Step 6: Continue the conversation if needed
    resp.record(timeout=5, transcribe=False, play_beep=True, action="/process_caller_input")
    
    return str(resp)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

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

# Initialize conversation state
call_state = {}

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
def ask_chatgpt(caller_input, tone):
    tone_description = "You are a helpful sales agent."
    if tone and 'tones' in tone:
        dominant_tone = tone['tones'][0]['tone_id']
        if dominant_tone == 'sadness':
            tone_description = "You are a caring, empathetic sales agent."
        elif dominant_tone == 'anger':
            tone_description = "You are calm and understanding."
        elif dominant_tone == 'joy':
            tone_description = "You are friendly and enthusiastic."
    prompt = f"{tone_description} The caller said: '{caller_input}'. How should we respond based on this context?"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a sales agent helping a customer."},
            {"role": "user", "content": prompt}
        ]
    )
    return response['choices'][0]['message']['content']

@app.route("/answer_call", methods=["POST"])
def answer_call():
    resp = VoiceResponse()
    resp.say("Hello! Thank you for calling. Please tell us what you are interested in.")
    resp.record(timeout=5, transcribe=False, play_beep=True, action="/process_caller_input")
    return str(resp)

@app.route("/process_caller_input", methods=["POST"])
def process_caller_input():
    recording_url = request.form['RecordingUrl']
    recording_audio = requests.get(recording_url).content

    audio_stream = io.BytesIO(recording_audio)
    with wave.open(audio_stream, 'rb') as wav_file:
        audio_content = wav_file.readframes(wav_file.getnframes())

    caller_transcription = transcribe_audio(audio_content)
    tone_analysis = analyze_tone(caller_transcription)

    if 'state' not in call_state:
        call_state['state'] = 'intro'
    
    if call_state['state'] == 'intro':
        bot_response = ask_chatgpt(caller_transcription, tone_analysis)
        if 'interested' in caller_transcription.lower():
            call_state['state'] = 'pain'
            bot_response = "Can you describe the main challenge you are facing? Our solution might be able to help."
        else:
            bot_response = "Could you please tell us more about why you are calling?"
    
    elif call_state['state'] == 'pain':
        bot_response = ask_chatgpt(caller_transcription, tone_analysis)
        if 'pain' in caller_transcription.lower():
            call_state['state'] = 'price'
            bot_response = "Thank you for sharing. Our solution is priced around $475, which is quite competitive compared to similar solutions."
        else:
            bot_response = "Could you provide more details about your pain point?"
    
    elif call_state['state'] == 'price':
        bot_response = ask_chatgpt(caller_transcription, tone_analysis)
        if 'price' in caller_transcription.lower():
            call_state['state'] = 'email'
            bot_response = "To provide you with more details, could you please share your email address? I'll send you an explainer video and further information."
        else:
            bot_response = "Here's the pricing information. Do you have any questions about it?"
    
    elif call_state['state'] == 'email':
        bot_response = ask_chatgpt(caller_transcription, tone_analysis)
        if '@' in caller_transcription:
            bot_response = "Thank you! I've sent the details to your email. Is there anything else I can assist you with today?"
        else:
            bot_response = "I didn't catch your email address. Could you please repeat it?"

    audio_response = synthesize_speech(bot_response)
    resp = VoiceResponse()
    resp.play(audio_response)
    resp.record(timeout=5, transcribe=False, play_beep=True, action="/process_caller_input")
    
    return str(resp)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

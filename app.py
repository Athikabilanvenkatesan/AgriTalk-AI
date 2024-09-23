import os
from flask import Flask, render_template, request, jsonify, url_for
from werkzeug.utils import secure_filename
import google.generativeai as genai
import requests
from gtts import gTTS
import asyncio
import string
import random
from dotenv import load_dotenv
import time


# Load the API keys from the .env file
load_dotenv()

hugging_face = os.getenv('hugging_face')
gemini_key = os.getenv('gemini_key')

# Configure the Gemini API
genai.configure(api_key=gemini_key)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'webm'}


def get_answer_gemini(question):
    # List of agriculture-related keywords
    agriculture_keywords = [
        "farm", "crop", "irrigation", "soil", "plant", "season", "harvest", "agriculture", "farmer", "pest", "fertilizer", "weeds"
        "disease", "yield", "seeds", "livestock", "weather", "monsoon", "organic", "insecticide", "horticulture", "agronomy"
    ]

    # Check if the question contains agriculture-related keywords
    if not any(keyword in question.lower() for keyword in agriculture_keywords):
        return "Please ask agriculture-related questions only."

    # Define a system role or context
    system_role = "You are AgriTalk AI, an expert bot that answers only agriculture-related questions and provides relevant advice to farmers. If users ask general questions like 'hello, who are you?', respond by saying, 'I am AgriTalk AI, here to assist you with any agriculture-related queries.' Focus exclusively on agriculture topics and provide valuable insights for farmers."

    # Create an instance of the Gemini model
    model = genai.GenerativeModel("gemini-1.5-flash")

    # Generate content using the model with the system role for context
    response = model.generate_content(f"{system_role}\n{question}")

    return response.text


def text_to_audio(text, filename):
    tts = gTTS(text)
    tts.save(f'static/audio/{filename}.mp3')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    if 'audio' in request.files:
        audio = request.files['audio']
        if audio and allowed_file(audio.filename):
            filename = secure_filename(audio.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            audio.save(filepath)
            transcription = process_audio(filepath)
            return jsonify({'text': transcription})

    text = request.form.get('text')
    if text:
        response = process_text(text)
        return {'text': response['text'], 'voice': url_for('static', filename='audio/' + response['voice'])}

    return jsonify({'text': 'Invalid request'})


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def process_audio(filepath):
    API_URL = "https://api-inference.huggingface.co/models/jonatasgrosman/wav2vec2-large-xlsr-53-english"
    headers = {"Authorization": f"Bearer {hugging_face}"}
    
    # Retry parameters
    max_retries = 3
    retry_delay = 10  # seconds
    
    for attempt in range(max_retries):
        with open(filepath, "rb") as f:
            data = f.read()
        
        response = requests.post(API_URL, headers=headers, data=data)
        response_data = response.json()
        
        if 'error' in response_data:
            if 'Model' in response_data['error'] and 'loading' in response_data['error']:
                # Model is loading, wait and retry
                print(f"Model is loading. Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                # Some other error occurred
                return f"Error: {response_data.get('error', 'Unknown error occurred')}"
        else:
            # Successful response
            return response_data.get('text', 'No text found in response')
    
    return "Error: Model could not be loaded after multiple attempts."


def process_text(text):
    # Get the answer from the Gemini model
    return_text = get_answer_gemini(text)
    
    # Preprocess the text by applying formatting
    formatted_text = format_response(return_text)
    
    # Generate a random filename for the audio output
    res = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    text_to_audio(formatted_text, res)
    
    return {"text": formatted_text, "voice": f"{res}.mp3"}


def format_response(text):
    # Remove markdown-like bold indicators and headers
    text = text.replace('**', '').replace('*', '').replace('##', '').replace('#', '')

    # Return the plain text without any additional HTML tags
    return text

if __name__ == '__main__':
    app.run(debug=True)

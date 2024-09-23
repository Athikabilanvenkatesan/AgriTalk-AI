# AgriTalk AI

This project is a web-based chatbot application that integrates with the Gemini AI model to answer agriculture-related questions and convert the responses into audio using the Google Text-to-Speech (gTTS) API. It also includes functionality for speech-to-text using Hugging Face's `wav2vec2-large-xlsr-53-english` model.

## Features

- **Chatbot Interface**: Accepts text or audio input from users, processes the input through the Gemini AI model for agriculture-related queries, and generates an appropriate response.
- **Text-to-Speech**: Converts the text response from Gemini into an audio file using Google Text-to-Speech (gTTS).
- **Audio Input Support**: Accepts `.webm` audio files, transcribes them using Hugging Face’s `wav2vec2` model, and responds in text and voice formats.
- **Agriculture Expert System**: Responds only to agriculture-related questions.

## Technologies Used

- **Flask**: A micro web framework for Python.
- **Google Generative AI (Gemini)**: Provides AI-powered agriculture-related answers.
- **gTTS**: Google Text-to-Speech for converting text responses to audio.
- **Hugging Face**: API integration for speech-to-text conversion.
- **HTML/CSS/JavaScript**: Frontend for user interaction.

## Requirements

1. Python 3.7+
2. Virtual environment (recommended)
3. Google Generative AI (Gemini) API key
4. Hugging Face API key
5. Flask dependencies

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/flask-chatbot-gemini.git
cd flask-chatbot-gemini 
```

### 2.Create a Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3.Install Dependencies
```bash
pip install -r requirements.txt
```
### 4.Setup Environment Variable
```bash
.env


hugging_face=your_huggingface_api_key
gemini_key=your_gemini_api_key
```

### 4.Run the application
```bash
python app.py
```


![image](https://github.com/user-attachments/assets/5130ee44-68d8-4ab8-b569-3e83ff3be5bf)


# MedBot - Hospital Room Assistant

A medical AI agent that runs locally using Ollama with Llama 3.2, designed to assist doctors and patients in a hospital setting.

## Project Overview

This project consists of two main components:

1. **Hardware** (planned):
   - Jetson Nano
   - Speakers
   - OLED screen
   - Temperature sensor
   - O2 meter
   - Infrared camera
   - Panic button
   - Other diagnostic sensors

2. **Software** (current implementation):
   - AI agent running locally through Ollama using Llama 3.2
   - Flask web application interface
   - Dummy patient data for testing
   - Role-based interaction (doctor/patient modes)

## Setup Instructions

### Prerequisites

1. Install [Ollama](https://ollama.ai/)
2. Install Python 3.8+ and pip
3. For voice capabilities:
   - A microphone for speech input
   - Speakers for audio output
   - FFmpeg (required for Whisper)

### Installation

1. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```

2. Create the MedBot model in Ollama:
   ```
   ollama create medbot -f Modelfile
   ```

3. Start the Ollama service:
   ```
   ollama serve
   ```

4. In a new terminal, start the Flask application:
   ```
   python app.py
   ```

5. Open your browser and navigate to:
   ```
   http://localhost:5000
   ```

## Usage

- Select a patient from the dropdown menu to view their information
- Choose your role (doctor or patient) using the buttons
- Text input:
  - Type your message in the input field and press Send
- Voice input:
  - Click the microphone button to start recording
  - Speak your message (recording stops automatically after 10 seconds)
  - Click the microphone button again to stop recording early
  - Your speech will be transcribed and sent to the AI
  - The AI's response will be both displayed and spoken aloud
- Click "Refresh" to update the vital signs (simulated changes)

## Features

- Role-based interaction (doctor/patient)
- Patient information display
- Vital signs monitoring with visual alerts
- Medical history and medications display
- Chat interface with the AI agent
- Voice input using Whisper speech recognition
- Text-to-speech output for spoken responses

## Technical Details

- The AI uses the Llama 3.2 model through Ollama
- The web interface is built with Flask, HTML, CSS, and JavaScript
- Implements a full RAG (Retrieval-Augmented Generation) system with vector database
- Uses sentence-transformers for generating embeddings
- ChromaDB for vector storage and semantic search
- Comprehensive medical knowledge base for conditions, medications, and vital signs
- The system adapts its responses based on user role and patient context
- Voice input uses Web Speech API for speech recognition
- Text-to-speech uses pyttsx3 for generating spoken responses

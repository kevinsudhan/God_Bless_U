from flask import Flask, render_template, request, jsonify, send_file
import requests
import json
import random
import os
import tempfile
import speech_recognition as sr
import pyttsx3
import threading
import time
import datetime
import base64
import io

from simple_rag import get_rag_engine
from medical_knowledge import get_medical_knowledge
from multilingual import get_multilingual_support

app = Flask(__name__)

print("Using simplified speech recognition for demo")

tts_engine = pyttsx3.init()

medical_knowledge = get_medical_knowledge()

# Function to fetch data from Supabase
def fetch_supabase_vitals():
    supabase_url = "https://wghhrmgntnzudopyvshe.supabase.co/rest/v1/vitals"
    headers = {
        "apikey": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndnaGhybWdudG56dWRvcHl2c2hlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDc0Nzc0ODAsImV4cCI6MjA2MzA1MzQ4MH0.n2k0oaI4xD1bIRs4Yu9zkTIQ9uMdeyrizkVodjJlxk8",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndnaGhybWdudG56dWRvcHl2c2hlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDc0Nzc0ODAsImV4cCI6MjA2MzA1MzQ4MH0.n2k0oaI4xD1bIRs4Yu9zkTIQ9uMdeyrizkVodjJlxk8"
    }
    
    try:
        response = requests.get(supabase_url, headers=headers)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching data from Supabase: {e}")
        return []

patients = {
    "P001": {
        "name": "John Smith",
        "age": 45,
        "gender": "Male",
        "diagnosis": "Type 2 Diabetes",
        "admission_date": "2025-05-10",
        "vital_signs": {
            "temperature": 37.2,
            "heart_rate": 72,
            "blood_pressure": "120/80",
            "oxygen_saturation": 98
        },
        "medications": ["Metformin", "Lisinopril"],
        "allergies": ["Penicillin"],
        "medical_history": ["Hypertension", "Appendectomy (2020)"]
    },
    "P002": {
        "name": "Emily Johnson",
        "age": 32,
        "medication_history": [
            "Started on oral antibiotics for pneumonia on 2025-05-11",
            "Switched to IV antibiotics on 2025-05-13 due to poor response",
            "Started on bronchodilators on 2025-05-14"
        ],
        "gender": "Female",
        "diagnosis": "Pneumonia",
        "admission_date": "2025-05-15",
        "vital_signs": {
            "temperature": 38.5,
            "heart_rate": 90,
            "blood_pressure": "110/70",
            "oxygen_saturation": 94
        },
        "medications": ["Azithromycin", "Ibuprofen"],
        "allergies": ["Sulfa drugs"],
        "medical_history": ["Asthma"]
    },
    "P003": {
        "name": "Robert Chen",
        "age": 68,
        "gender": "Male",
        "diagnosis": "Myocardial Infarction",
        "admission_date": "2025-05-14",
        "vital_signs": {
            "temperature": 36.9,
            "heart_rate": 85,
            "blood_pressure": "140/90",
            "oxygen_saturation": 96
        },
        "medications": ["Aspirin", "Atorvastatin", "Metoprolol"],
        "allergies": [],
        "medical_history": ["Coronary Artery Disease", "Hyperlipidemia"]
    },
    "P004": {
        "name": "RAHUL",
        "age": 40,
        "gender": "Male",
        "diagnosis": "Real-time Monitoring",
        "admission_date": "2025-05-17",
        "vital_signs": {
            "temperature": 36.8,
            "heart_rate": 75,
            "blood_pressure": "120/80",
            "oxygen_saturation": 97
        },
        "medications": ["Vitamin D", "Multivitamin"],
        "allergies": ["None"],
        "medical_history": [
            "Patient with real-time health monitoring",
            "Remote patient monitoring program",
            "Wellness assessment"
        ],
        "medication_history": [
            "Started on daily supplements on 2025-05-17"
        ],
        "supabase_data": True,  # Flag to indicate this patient uses Supabase data
        "supabase_patient_id": "P001"  # Actual ID in Supabase
    }
}

@app.route('/splash')
@app.route('/')
def splash():
    return render_template('splash.html')

@app.route('/main')
def index():
    return render_template('index.html', patient_ids=list(patients.keys()))

@app.route('/get_patient_data/<patient_id>')
def get_patient_data(patient_id):
    if patient_id in patients:
        return jsonify(patients[patient_id])
    else:
        return jsonify({"error": "Patient not found"}), 404

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    user_role = data.get('role', 'patient')
    patient_id = data.get('patient_id', '')
    is_voice = data.get('is_voice', False)
    language = data.get('language', 'en')
    
    patient_context = ""
    if patient_id in patients:
        patient = patients[patient_id]
        patient_context = f"Patient ID: {patient_id}\n"
        patient_context += f"Name: {patient['name']}\n"
        patient_context += f"Age: {patient['age']} years old\n"
        patient_context += f"Gender: {patient['gender']}\n"
        patient_context += f"Diagnosis: {patient['diagnosis']}\n"
        patient_context += f"Admission Date: {patient['admission_date']}\n\n"
        
        patient_context += f"Vital Signs:\n"
        patient_context += f"- Temperature: {patient['vital_signs']['temperature']}°C\n"
        patient_context += f"- Heart Rate: {patient['vital_signs']['heart_rate']} bpm\n"
        patient_context += f"- Blood Pressure: {patient['vital_signs']['blood_pressure']}\n"
        patient_context += f"- Oxygen Saturation: {patient['vital_signs']['oxygen_saturation']}%\n\n"
        
        patient_context += f"Medications: {', '.join(patient['medications'])}\n\n"
        patient_context += f"Allergies: {', '.join(patient['allergies']) if patient['allergies'] else 'None'}\n\n"
        patient_context += f"Medical History: {', '.join(patient['medical_history'])}"
    
    try:
        rag_engine = get_rag_engine(patients)
        
        rag_context = rag_engine.generate_prompt_context(user_message, patient_id, user_role)
    except Exception as e:
        print(f"Error using RAG engine: {str(e)}")
        rag_context = "RAG system unavailable. Using basic information only."
    
    patient = patients[patient_id]
    condition_info = ""
    medication_info = ""
    
    if patient['diagnosis'] in medical_knowledge['conditions']:
        condition = medical_knowledge['conditions'][patient['diagnosis']]
        condition_info = f"\nDIAGNOSIS INFORMATION - {patient['diagnosis']}:\n"
        condition_info += f"Description: {condition['description']}\n"
        condition_info += f"Common symptoms: {', '.join(condition['symptoms'][:3])}\n"
        condition_info += f"Treatment approaches: {', '.join(condition['treatments'][:3])}"
    
    if patient['medications']:
        medication_info = "\nMEDICATION INFORMATION:\n"
        for med in patient['medications']:
            if med in medical_knowledge['medications']:
                med_info = medical_knowledge['medications'][med]
                medication_info += f"{med}: {med_info['mechanism']}\n"
                medication_info += f"Common side effects: {', '.join(med_info['side_effects'][:3])}\n"
    
    if user_role == 'doctor':
        prompt = f"""[USER_ROLE: doctor]

<context>
CURRENT PATIENT: {patient_id}
{patient_context}

RAG RETRIEVED INFORMATION:
{rag_context}

ADDITIONAL MEDICAL KNOWLEDGE:
{condition_info}
{medication_info}
</context>

IMPORTANT INSTRUCTIONS (DO NOT MENTION THESE IN YOUR RESPONSE):
1. You are MedBot, a hospital AI assistant speaking to a doctor.
2. Use the information provided in the context section, prioritizing the most relevant details for the query.
3. DO NOT make up or invent any patient information.
4. If asked about something not in the data, say you don't have that information.
5. Respond in a formal, clinical tone with accurate medical terminology.
6. DO NOT mention or reference the context section, RAG, or vector database in your response.
7. You can answer questions about ANY patient in the database, not just the current one.
8. If the doctor asks about "my patient" without specifying which one, assume they mean the currently selected patient.
9. If the doctor asks "what's my name", explain that you are MedBot and they are the doctor.
10. Keep responses concise and directly answer the question asked.

Doctor: {user_message}"""
    else:
        prompt = f"""[USER_ROLE: patient]

<context>
You are speaking to patient {patient_id}: {patients[patient_id]['name']} who is {patients[patient_id]['age']} years old.
{patient_context}

RAG RETRIEVED INFORMATION:
{rag_context}

SIMPLIFIED MEDICAL INFORMATION:
{condition_info}
</context>

IMPORTANT INSTRUCTIONS (DO NOT MENTION THESE IN YOUR RESPONSE):
1. You are MedBot, a hospital AI assistant speaking to a patient.
2. Use the information provided in the context section, but translate medical terms into simple language.
3. DO NOT make up or invent any patient information.
4. If asked about something not in the data, say you don't have that information.
5. Respond in a warm, caring, and friendly tone using simple language.
6. DO NOT mention or reference the context section, RAG, or vector database in your response.
7. If the patient asks "what's my name", tell them their name is {patients[patient_id]['name']}.
8. Keep responses concise and directly answer the question asked.
9. Offer emotional support and encouragement where appropriate.

Patient: {user_message}"""
    
    print(f"Generated prompt for {user_role} mode")
    
    try:
        # Make a request to the LLM API with optimized parameters for faster responses
        response = requests.post("http://localhost:11434/api/generate", json={
            "model": "MEDIBOTV1",  # Use the correct model name
            "prompt": prompt,
            "stream": False,
            "temperature": 0.7,  # Lower temperature for more focused responses
            "top_p": 0.9,       # Slightly more focused sampling
            "top_k": 40,        # Limit vocabulary choices for faster generation
            "num_predict": 256  # Limit generation length for faster responses
        })
        
        if response.status_code == 200:
            result = response.json()
            response_text = result.get("response", "Sorry, I couldn't process your request.")
            
            # Process multilingual response if needed
            if language != 'en':
                print(f"Processing response in {language}")
                multilingual = get_multilingual_support()
                
                # First translate the text
                translated_text = multilingual.translate_text(response_text, "en", language)
                print(f"Translated from English to {language}: {translated_text}")
                
                # Now generate audio from the translated text
                audio_data = text_to_speech(translated_text, language)
                audio_base64 = base64.b64encode(audio_data).decode('utf-8')
                
                # Return both original and translated text for display with the audio data
                return jsonify({
                    "response": translated_text,
                    "original_text": response_text,
                    "audio": audio_base64,
                    "language": language
                })
            else:
                # For English, just generate audio from the original text
                audio_data = text_to_speech(response_text, language)
                audio_base64 = base64.b64encode(audio_data).decode('utf-8')
                
                # Standard English response
                return jsonify({
                    "response": response_text,
                    "audio": audio_base64,
                    "language": "en"
                })
        else:
            return jsonify({"error": f"Ollama API error: {response.status_code}"}), 500
    
    except Exception as e:
        return jsonify({"error": f"Error: {str(e)}"}), 500

@app.route('/update_vitals/<patient_id>', methods=['POST'])
def update_vitals(patient_id):
    if patient_id in patients:
        # Special handling for Patient 4 (P004) - fetch real-time data from Supabase
        if patient_id == "P004" and patients[patient_id].get('supabase_data', False):
            try:
                # Fetch the latest vitals from Supabase
                supabase_vitals = fetch_supabase_vitals()
                
                if supabase_vitals and len(supabase_vitals) > 0:
                    # Filter for records matching this patient's Supabase ID
                    patient_supabase_id = patients[patient_id].get('supabase_patient_id', 'P001')
                    patient_records = [record for record in supabase_vitals if record.get('patient_id') == patient_supabase_id]
                    
                    # Sort by timestamp in descending order to get the most recent
                    patient_records.sort(key=lambda x: x.get('timestamp', 0), reverse=True)
                    
                    if patient_records:
                        # Use the most recent record
                        latest_vitals = patient_records[0]
                        
                        # Map Supabase fields to our application fields
                        patients[patient_id]['vital_signs']['heart_rate'] = latest_vitals.get('heart_rate', 75)
                        patients[patient_id]['vital_signs']['oxygen_saturation'] = latest_vitals.get('spo2', 97)
                        
                        # Generate simulated temperature and blood pressure (not in Supabase)
                        patients[patient_id]['vital_signs']['temperature'] = round(36.5 + (latest_vitals.get('heart_rate', 75) - 70) * 0.02, 1)
                        
                        # Calculate systolic and diastolic based on heart rate
                        hr = latest_vitals.get('heart_rate', 75)
                        systolic = 110 + int((hr - 70) * 0.5)
                        diastolic = 70 + int((hr - 70) * 0.3)
                        patients[patient_id]['vital_signs']['blood_pressure'] = f"{systolic}/{diastolic}"
                        
                        # Add condition from Supabase
                        patients[patient_id]['vital_signs']['condition'] = latest_vitals.get('condition', 'normal')
                    
                    # Add timestamp for when the data was fetched
                    patients[patient_id]['vital_signs']['last_updated'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    patients[patient_id]['vital_signs']['data_source'] = "Supabase Live Data"
                    
                    print(f"Updated P004 vitals with Supabase data: {latest_vitals}")
                else:
                    print("No Supabase vitals data found, using default values")
            except Exception as e:
                print(f"Error fetching Supabase data: {e}")
                # Fall back to random updates if Supabase fails
                patients[patient_id]['vital_signs']['temperature'] = round(
                    patients[patient_id]['vital_signs']['temperature'] + random.uniform(-0.3, 0.3), 1)
                patients[patient_id]['vital_signs']['heart_rate'] = max(60, min(100, 
                    patients[patient_id]['vital_signs']['heart_rate'] + random.randint(-5, 5)))
                
                sys, dia = map(int, patients[patient_id]['vital_signs']['blood_pressure'].split('/'))
                sys = max(90, min(160, sys + random.randint(-5, 5)))
                dia = max(60, min(100, dia + random.randint(-3, 3)))
                patients[patient_id]['vital_signs']['blood_pressure'] = f"{sys}/{dia}"
                
                patients[patient_id]['vital_signs']['oxygen_saturation'] = max(90, min(100,
                    patients[patient_id]['vital_signs']['oxygen_saturation'] + random.randint(-2, 2)))
                
                patients[patient_id]['vital_signs']['data_source'] = "Fallback Random Data (Supabase Error)"
        else:
            # Regular random updates for Patients 1-3
            patients[patient_id]['vital_signs']['temperature'] = round(
                patients[patient_id]['vital_signs']['temperature'] + random.uniform(-0.3, 0.3), 1)
            patients[patient_id]['vital_signs']['heart_rate'] = max(60, min(100, 
                patients[patient_id]['vital_signs']['heart_rate'] + random.randint(-5, 5)))
            
            sys, dia = map(int, patients[patient_id]['vital_signs']['blood_pressure'].split('/'))
            sys = max(90, min(160, sys + random.randint(-5, 5)))
            dia = max(60, min(100, dia + random.randint(-3, 3)))
            patients[patient_id]['vital_signs']['blood_pressure'] = f"{sys}/{dia}"
            
            patients[patient_id]['vital_signs']['oxygen_saturation'] = max(90, min(100,
                patients[patient_id]['vital_signs']['oxygen_saturation'] + random.randint(-2, 2)))
            
            patients[patient_id]['vital_signs']['data_source'] = "Simulated Random Data"
        
        return jsonify({"status": "success", "vitals": patients[patient_id]['vital_signs']})
    else:
        return jsonify({"error": "Patient not found"}), 404

@app.route('/speech-to-text', methods=['POST'])
def speech_to_text():
    try:
        if 'text' in request.form:
            transcription = request.form['text']
            return jsonify({"transcription": transcription})
        
        if 'audio' in request.files:
            audio_file = request.files['audio']
            print(f"Received audio file: {audio_file.filename}")
            
            return jsonify({"transcription": "This is a simulated voice transcription for demo purposes."})
        
        return jsonify({"error": "No input provided"}), 400
        
    except Exception as e:
        print(f"Error in speech-to-text: {str(e)}")
        return jsonify({"error": f"Speech processing error: {str(e)}"}), 500

def text_to_speech(text, language='en'):
    # Google Text-to-Speech implementation
    try:
        from gtts import gTTS
        import io
        import base64
        
        print(f"Converting text to speech using Google TTS with language {language}...")
        
        # Map language code to Google TTS language code - handling all supported languages
        tts_lang = 'en'
        
        # Language mapping - focusing on Indian languages as per user's needs
        language_map = {
            'ta': 'ta',   # Tamil
            'hi': 'hi',   # Hindi
            'te': 'te',   # Telugu
            'kn': 'kn',   # Kannada
            'ml': 'ml',   # Malayalam 
            'bn': 'bn',   # Bengali
            'gu': 'gu',   # Gujarati
            'mr': 'mr',   # Marathi
            'pa': 'pa',   # Punjabi
            'es': 'es',   # Spanish
            'fr': 'fr',   # French
            'de': 'de',   # German
        }
        
        # Get the first 2 characters of language code and find matching TTS language
        lang_prefix = language[:2].lower()
        if lang_prefix in language_map:
            tts_lang = language_map[lang_prefix]
        
        print(f"Using Google TTS language code: {tts_lang} for requested language: {language}")
        
        # Create gTTS object with appropriate language setting
        tts = gTTS(text=text, lang=tts_lang, slow=False)
        
        # Save to in-memory file object instead of disk
        mp3_fp = io.BytesIO()
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)
        
        # Get binary data
        audio_data = mp3_fp.read()
        print(f"Successfully created Google TTS audio in {tts_lang} in memory")
        
        # Return the binary audio data directly
        return audio_data
    except Exception as e:
        print(f"Google TTS error: {str(e)}")
        
        # Fallback to original TTS engine if Google TTS fails
        try:
            print(f"TTS error: {str(e)}. Using fallback method.")
            import tempfile
            import os
            
            # Create a BytesIO object for pyttsx3 output
            temp_dir = tempfile.gettempdir()
            output_path = os.path.join(temp_dir, "response.mp3")
            
            # Use pyttsx3 as fallback
            tts_engine.save_to_file(text, output_path)
            tts_engine.runAndWait()
            
            # Read the file into memory and return the binary data
            with open(output_path, 'rb') as f:
                audio_data = f.read()
            
            # Clean up the temporary file
            try:
                os.remove(output_path)
            except:
                pass
                
            return audio_data
        except Exception as inner_e:
            print(f"Even fallback TTS failed: {str(inner_e)}")
            # Return empty binary data if everything fails
            return b''

print("Initializing RAG engine with patient data...")
rag_engine = get_rag_engine(patients)
print("RAG engine initialized!")

if __name__ == "__main__":
    # Run app on all network interfaces so it's accessible on other devices
    app.run(host='0.0.0.0', debug=True, port=5001)

from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import requests
import json
import random
import os
import tempfile
import speech_recognition as sr
import pyttsx3
import threading
import time
import base64
import io

from simple_rag import get_rag_engine
from medical_knowledge import get_medical_knowledge

app = Flask(__name__)
CORS(app)

print("Using simplified speech recognition for demo")

tts_engine = pyttsx3.init()

medical_knowledge = get_medical_knowledge()

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
    }
}

@app.route('/')
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
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "MEDIBOTV1",  
                "prompt": prompt,
                "stream": False
            }
        )
        
        if response.status_code == 200:
            result = response.json()
            response_text = result.get("response", "Sorry, I couldn't process your request.")
            
            audio_file_path = text_to_speech(response_text)
            with open(audio_file_path, "rb") as audio_file:
                audio_data = audio_file.read()
                audio_base64 = base64.b64encode(audio_data).decode('utf-8')
            os.remove(audio_file_path)  
            return jsonify({"response": response_text, "audio": audio_base64})
        else:
            return jsonify({"error": f"Ollama API error: {response.status_code}"}), 500
    
    except Exception as e:
        return jsonify({"error": f"Error: {str(e)}"}), 500

@app.route('/update_vitals/<patient_id>', methods=['POST'])
def update_vitals(patient_id):
    if patient_id in patients:
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

def text_to_speech(text):
    temp_dir = tempfile.gettempdir()
    output_path = os.path.join(temp_dir, "response.mp3")
    
    tts_engine.save_to_file(text, output_path)
    tts_engine.runAndWait()
    
    return output_path

print("Initializing RAG engine with patient data...")
rag_engine = get_rag_engine(patients)
print("RAG engine initialized!")

if __name__ == '__main__':
    app.run(debug=True, port=5000)

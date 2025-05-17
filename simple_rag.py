

import os
import json
from typing import List, Dict, Any, Optional
import re

class SimpleRAG:

    
    def __init__(self):
    
        print("Initializing Simple RAG system...")
        self.documents = []
        self.initialized = True
        print("Simple RAG system initialized")
    
    def _convert_patient_to_documents(self, patients: Dict[str, Dict]) -> List[Dict]:
    
        documents = []
        
        for patient_id, patient_data in patients.items():
            
            overview = f"Patient ID: {patient_id}\n"
            overview += f"Name: {patient_data['name']}\n"
            overview += f"Age: {patient_data['age']} years old\n"
            overview += f"Gender: {patient_data['gender']}\n"
            overview += f"Diagnosis: {patient_data['diagnosis']}\n"
            overview += f"Admission Date: {patient_data['admission_date']}\n"
            
            doc = {
                "content": overview,
                "metadata": {
                    "patient_id": patient_id,
                    "document_type": "patient_overview",
                    "name": patient_data['name']
                }
            }
            documents.append(doc)
            
            
            vitals = f"Patient {patient_id} ({patient_data['name']}) Vital Signs:\n"
            vitals += f"Temperature: {patient_data['vital_signs']['temperature']}°C\n"
            vitals += f"Heart Rate: {patient_data['vital_signs']['heart_rate']} bpm\n"
            vitals += f"Blood Pressure: {patient_data['vital_signs']['blood_pressure']}\n"
            vitals += f"Oxygen Saturation: {patient_data['vital_signs']['oxygen_saturation']}%\n"
            
            doc = {
                "content": vitals,
                "metadata": {
                    "patient_id": patient_id,
                    "document_type": "vital_signs",
                    "name": patient_data['name']
                }
            }
            documents.append(doc)
            
            
            meds = f"Patient {patient_id} ({patient_data['name']}) Medications and Allergies:\n"
            meds += f"Medications: {', '.join(patient_data['medications'])}\n"
            meds += f"Allergies: {', '.join(patient_data['allergies']) if patient_data['allergies'] else 'None'}\n"
            
            doc = {
                "content": meds,
                "metadata": {
                    "patient_id": patient_id,
                    "document_type": "medications_allergies",
                    "name": patient_data['name']
                }
            }
            documents.append(doc)
            
            
            history = f"Patient {patient_id} ({patient_data['name']}) Medical History:\n"
            history += f"{', '.join(patient_data['medical_history'])}\n"
            
            doc = {
                "content": history,
                "metadata": {
                    "patient_id": patient_id,
                    "document_type": "medical_history",
                    "name": patient_data['name']
                }
            }
            documents.append(doc)
        
        return documents
    
    def ingest_patient_data(self, patients: Dict[str, Dict]):
    
        try:
            print(f"Ingesting data for {len(patients)} patients...")
            
            
            self.documents = self._convert_patient_to_documents(patients)
            
            print(f"Created {len(self.documents)} document chunks")
        except Exception as e:
            print(f"Error ingesting patient data: {str(e)}")
    
    def _simple_keyword_match(self, query: str, document: Dict) -> float:
    
        
        query_lower = query.lower()
        content_lower = document["content"].lower()
        
        
        query_words = set(re.findall(r'\b\w+\b', query_lower))
        content_words = set(re.findall(r'\b\w+\b', content_lower))
        
        
        matching_words = query_words.intersection(content_words)
        
        
        if not query_words:
            return 0
        
        return len(matching_words) / len(query_words)
    
    def retrieve_relevant_context(self, query: str, patient_id: Optional[str] = None, k: int = 5) -> List[Dict]:
    
        if not self.documents:
            print("No documents available")
            return []
        
        try:
            
            filtered_docs = self.documents
            if patient_id:
                filtered_docs = [doc for doc in self.documents if doc["metadata"]["patient_id"] == patient_id]
            
            
            scored_docs = [(doc, self._simple_keyword_match(query, doc)) for doc in filtered_docs]
            
            
            scored_docs.sort(key=lambda x: x[1], reverse=True)
            
            
            return [doc for doc, score in scored_docs[:k] if score > 0]
        except Exception as e:
            print(f"Error retrieving context: {str(e)}")
            return []
    
    def generate_prompt_context(self, query: str, patient_id: Optional[str] = None, role: str = "doctor") -> str:
    
        try:
            
            k = 8 if role == "doctor" else 3
            
            
            filter_id = None if role == "doctor" else patient_id
            
            
            docs = self.retrieve_relevant_context(query, filter_id, k)
            
            if not docs:
                return "No relevant information found."
            
            
            if role == "doctor":
                context = "RETRIEVED MEDICAL INFORMATION:\n\n"
                for i, doc in enumerate(docs):
                    context += f"[Document {i+1}]\n"
                    context += f"{doc['content']}\n\n"
            else:
                
                context = "PATIENT INFORMATION:\n\n"
                for doc in docs:
                    
                    content = doc['content'].replace(f"Patient {patient_id}", "Your")
                    context += f"{content}\n\n"
            
            return context
        except Exception as e:
            print(f"Error generating prompt context: {str(e)}")
            return "Unable to retrieve context information."


simple_rag = None

def get_rag_engine(patients=None):

    global simple_rag
    
    try:
        if simple_rag is None:
            simple_rag = SimpleRAG()
            
            
            if patients:
                simple_rag.ingest_patient_data(patients)
        
        return simple_rag
    except Exception as e:
        print(f"Error in get_rag_engine: {str(e)}")
        
        if simple_rag is None:
            simple_rag = SimpleRAG()
        return simple_rag

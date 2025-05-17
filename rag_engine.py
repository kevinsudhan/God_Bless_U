"""
RAG (Retrieval-Augmented Generation) Engine for MedBot

This module implements a proper RAG system with vector database storage,
embedding generation, and semantic search capabilities.
"""

import os
import json
import pandas as pd
from typing import List, Dict, Any, Optional

# LangChain imports
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

# Create directory for vector database
VECTOR_DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "vector_db")
os.makedirs(VECTOR_DB_PATH, exist_ok=True)

class MedicalRAG:
    """Medical RAG system for patient data retrieval and query answering."""
    
    def __init__(self):
        """Initialize the RAG system with embeddings and vector store."""
        print("Initializing Medical RAG system...")
        
        try:
            # Initialize embedding model
            self.embedding_model = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2",
                model_kwargs={"device": "cpu"},
                encode_kwargs={"normalize_embeddings": True}
            )
            print("Embedding model loaded")
            
            # Initialize vector store
            self.vector_store = None
            
            # Text splitter for chunking documents
            self.text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=500,
                chunk_overlap=50,
                separators=["\n\n", "\n", ". ", ", ", " ", ""]
            )
            
            print("Medical RAG system initialized")
            self.initialized = True
        except Exception as e:
            print(f"Error initializing RAG system: {str(e)}")
            self.initialized = False
    
    def _convert_patient_to_documents(self, patients: Dict[str, Dict]) -> List[Document]:
        """
        Convert patient data to document format for ingestion into vector store.
        
        Args:
            patients: Dictionary of patient data
            
        Returns:
            List of Document objects
        """
        documents = []
        
        for patient_id, patient_data in patients.items():
            # Create a general patient overview document
            overview = f"Patient ID: {patient_id}\n"
            overview += f"Name: {patient_data['name']}\n"
            overview += f"Age: {patient_data['age']} years old\n"
            overview += f"Gender: {patient_data['gender']}\n"
            overview += f"Diagnosis: {patient_data['diagnosis']}\n"
            overview += f"Admission Date: {patient_data['admission_date']}\n"
            
            doc = Document(
                page_content=overview,
                metadata={
                    "patient_id": patient_id,
                    "document_type": "patient_overview",
                    "name": patient_data['name']
                }
            )
            documents.append(doc)
            
            # Create a document for vital signs
            vitals = f"Patient {patient_id} ({patient_data['name']}) Vital Signs:\n"
            vitals += f"Temperature: {patient_data['vital_signs']['temperature']}°C\n"
            vitals += f"Heart Rate: {patient_data['vital_signs']['heart_rate']} bpm\n"
            vitals += f"Blood Pressure: {patient_data['vital_signs']['blood_pressure']}\n"
            vitals += f"Oxygen Saturation: {patient_data['vital_signs']['oxygen_saturation']}%\n"
            
            doc = Document(
                page_content=vitals,
                metadata={
                    "patient_id": patient_id,
                    "document_type": "vital_signs",
                    "name": patient_data['name']
                }
            )
            documents.append(doc)
            
            # Create a document for medications and allergies
            meds = f"Patient {patient_id} ({patient_data['name']}) Medications and Allergies:\n"
            meds += f"Medications: {', '.join(patient_data['medications'])}\n"
            meds += f"Allergies: {', '.join(patient_data['allergies']) if patient_data['allergies'] else 'None'}\n"
            
            doc = Document(
                page_content=meds,
                metadata={
                    "patient_id": patient_id,
                    "document_type": "medications_allergies",
                    "name": patient_data['name']
                }
            )
            documents.append(doc)
            
            # Create a document for medical history
            history = f"Patient {patient_id} ({patient_data['name']}) Medical History:\n"
            history += f"{', '.join(patient_data['medical_history'])}\n"
            
            doc = Document(
                page_content=history,
                metadata={
                    "patient_id": patient_id,
                    "document_type": "medical_history",
                    "name": patient_data['name']
                }
            )
            documents.append(doc)
        
        return documents
    
    def ingest_patient_data(self, patients: Dict[str, Dict]):
        """
        Ingest patient data into the vector store.
        
        Args:
            patients: Dictionary of patient data
        """
        if not hasattr(self, 'initialized') or not self.initialized:
            print("RAG system not properly initialized, skipping ingestion")
            return
            
        try:
            print(f"Ingesting data for {len(patients)} patients...")
            
            # Convert patient data to documents
            documents = self._convert_patient_to_documents(patients)
            
            # Split documents into chunks
            split_documents = self.text_splitter.split_documents(documents)
            print(f"Created {len(split_documents)} document chunks")
            
            # Create or update vector store
            self.vector_store = Chroma.from_documents(
                documents=split_documents,
                embedding=self.embedding_model,
                persist_directory=VECTOR_DB_PATH
            )
            
            # Persist vector store
            self.vector_store.persist()
            print(f"Vector store persisted to {VECTOR_DB_PATH}")
        except Exception as e:
            print(f"Error ingesting patient data: {str(e)}")
            # Fallback to no vector store
            self.vector_store = None
    
    def retrieve_relevant_context(self, query: str, patient_id: Optional[str] = None, k: int = 5) -> List[Document]:
        """
        Retrieve relevant context for a query.
        
        Args:
            query: User query
            patient_id: Optional patient ID to filter results
            k: Number of documents to retrieve
            
        Returns:
            List of relevant documents
        """
        if not hasattr(self, 'initialized') or not self.initialized or self.vector_store is None:
            print("Vector store not initialized")
            return []
        
        try:
            # Create search filters if patient_id is provided
            filter_dict = {"patient_id": patient_id} if patient_id else None
            
            # Retrieve relevant documents
            docs = self.vector_store.similarity_search(
                query=query,
                k=k,
                filter=filter_dict
            )
            
            return docs
        except Exception as e:
            print(f"Error retrieving context: {str(e)}")
            return []
    
    def generate_prompt_context(self, query: str, patient_id: Optional[str] = None, role: str = "doctor") -> str:
        """
        Generate context for the prompt based on retrieved documents.
        
        Args:
            query: User query
            patient_id: Optional patient ID to filter results
            role: User role (doctor or patient)
            
        Returns:
            Context string for the prompt
        """
        if not hasattr(self, 'initialized') or not self.initialized:
            return "RAG system not available. Using basic information only."
            
        try:
            # Adjust k based on role - doctors get more comprehensive context
            k = 8 if role == "doctor" else 3
            
            # For patients, always filter by their patient_id
            filter_id = None if role == "doctor" else patient_id
            
            # Retrieve relevant documents
            docs = self.retrieve_relevant_context(query, filter_id, k)
            
            if not docs:
                return "No relevant information found."
            
            # Format context differently based on role
            if role == "doctor":
                context = "RETRIEVED MEDICAL INFORMATION:\n\n"
                for i, doc in enumerate(docs):
                    context += f"[Document {i+1}]\n"
                    context += f"{doc.page_content}\n\n"
            else:
                # For patients, simplify the context
                context = "PATIENT INFORMATION:\n\n"
                for doc in docs:
                    # Remove technical headers for patient view
                    content = doc.page_content.replace(f"Patient {patient_id}", "Your")
                    context += f"{content}\n\n"
            
            return context
        except Exception as e:
            print(f"Error generating prompt context: {str(e)}")
            return "Unable to retrieve context information."

# Singleton instance
medical_rag = None

def get_rag_engine(patients=None):
    """Get or initialize the RAG engine singleton."""
    global medical_rag
    
    try:
        if medical_rag is None:
            medical_rag = MedicalRAG()
            
            # Ingest patient data if provided
            if patients:
                medical_rag.ingest_patient_data(patients)
        
        return medical_rag
    except Exception as e:
        print(f"Error in get_rag_engine: {str(e)}")
        # Create a minimal RAG engine that won't cause errors
        if medical_rag is None:
            medical_rag = MedicalRAG()
            medical_rag.initialized = False
        return medical_rag

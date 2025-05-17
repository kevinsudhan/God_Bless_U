import os
import tempfile
import base64
import requests
import html
from murf import Murf
import tts

class MultilingualSupport:
    def __init__(self):
        self.murf_client = Murf(api_key="ap2_1c820140-6d84-4efb-b952-91c87dac76fb")
        self.supported_languages = ["en", "hi", "ta", "te", "kn"]
        # Use valid Murf voice IDs based on the working project
        self.voice_ids = {
            "en": "en-US-christopher",
            "hi": "hi-IN-shweta",      # Hindi female voice
            "ta": "ta-IN-iniya"        # Tamil female voice (confirmed working in the other project)
        }
        
        # Try to get available voices
        try:
            self.available_voices = self.get_available_voices()
            print(f"Available voices: {len(self.available_voices)}")
        except Exception as e:
            print(f"Error getting available voices: {str(e)}")
            self.available_voices = []
        
        # Google Translate language codes
        self.google_lang_codes = {
            "en": "en",
            "hi": "hi",
            "ta": "ta",
            "te": "te",
            "kn": "kn"
        }
        
        # No IndicF5 model - using only Murf
        
        print("Initializing multilingual support with Google Translate...")
        
    # No need for reference prompts without IndicF5
        
    def google_translate(self, text, source_lang="en", target_lang="hi"):
        """Use Google Translate API to translate text"""
        try:
            # Convert language codes to Google format
            source = self.google_lang_codes.get(source_lang, "en")
            target = self.google_lang_codes.get(target_lang, "hi")
            
            # Skip translation if source and target are the same
            if source == target:
                return text
                
            # Use Google Translate API
            url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl={source}&tl={target}&dt=t&q={requests.utils.quote(text)}"
            
            print(f"Translating with Google: {source} -> {target}")
            response = requests.get(url)
            
            if response.status_code == 200:
                # Parse the response
                result = response.json()
                translated_text = ""
                
                # Extract translated text from the response
                for sentence in result[0]:
                    if sentence[0]:
                        translated_text += sentence[0]
                
                # Unescape HTML entities
                translated_text = html.unescape(translated_text)
                print(f"Translation result: {translated_text}")
                return translated_text
            else:
                print(f"Translation error: {response.status_code}")
                return text
        except Exception as e:
            print(f"Translation error: {str(e)}")
            return text
    
    def translate_text(self, text, source_lang="en", target_lang="hi"):
        """Translate text using Google Translate"""
        return self.google_translate(text, source_lang, target_lang)
    
    def text_to_speech(self, text, language="en"):
        """Generate speech using Murf API"""
        try:
            return self._murf_tts(text, language)
        except Exception as e:
            print(f"TTS error: {str(e)}")
            return {
                "audio_base64": "",
                "text": text,
                "error": str(e)
            }
    
    def get_available_voices(self):
        """Get list of available voices from Murf API"""
        try:
            # Get available voices from Murf API
            voices = self.murf_client.text_to_speech.voices()
            return voices
        except Exception as e:
            print(f"Error getting available voices: {str(e)}")
            return []
    
    def _murf_tts(self, text, language="en"):
        """Generate speech using the working tts module"""
        # Use the standalone tts module that works
        result = tts.text_to_speech(text, language)
        
        # If there was an error, fall back to the simple audio tone
        if "error" in result:
            print(f"TTS error: {result['error']}. Using fallback method.")
            return self._generate_fallback_audio(text, language)
            
        return result
    
    def _generate_fallback_audio(self, text, language="en"):
        """Generate a simple audio tone as fallback"""
        import wave
        import struct
        import math
        
        # Parameters for the sine wave
        duration = 2  # seconds
        sample_rate = 44100  # Hz
        frequency = 440  # Hz (A4 note)
        
        # Create the audio data
        samples = []
        for i in range(int(duration * sample_rate)):
            sample = int(32767 * 0.5 * math.sin(2 * math.pi * frequency * i / sample_rate))
            samples.append(sample)
        
        # Create a temporary file to store the audio
        temp_file_path = os.path.join(tempfile.gettempdir(), f"response_{language}.wav")
        
        # Write to a WAV file
        with wave.open(temp_file_path, 'w') as wav_file:
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 2 bytes (16 bits)
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(struct.pack('h' * len(samples), *samples))
        
        # Read the file and convert to base64
        with open(temp_file_path, "rb") as audio_file:
            audio_base64 = base64.b64encode(audio_file.read()).decode("utf-8")
        
        # Clean up
        os.remove(temp_file_path)
        
        return {
            "audio_base64": audio_base64,
            "content_type": "audio/wav",
            "text": text,
            "note": "Using fallback audio"
        }
    
    def process_response(self, text, target_lang="en"):
        print(f"Processing response for language: {target_lang}")
        
        if target_lang == "en":
            result = self.text_to_speech(text, "en")
            result["original_text"] = text  # Keep the original text for reference
            return result
        
        # Translate the text
        translated_text = self.translate_text(text, "en", target_lang)
        print(f"Translated text: {translated_text}")
        
        # Convert to speech
        result = self.text_to_speech(translated_text, target_lang)
        
        # Include both original and translated text
        result["original_text"] = text
        result["translated_text"] = translated_text
        
        return result

# Singleton instance
multilingual_support = None

def get_multilingual_support():
    global multilingual_support
    
    if multilingual_support is None:
        multilingual_support = MultilingualSupport()
    
    return multilingual_support

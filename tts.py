import base64
import io

def text_to_speech(text, language="en"):
    """
    Generate speech using Google TTS - in-memory implementation
    """
    from gtts import gTTS
    
    # Map language code to Google TTS language code
    tts_lang = 'en'
    if language.startswith('ta'):
        tts_lang = 'ta'
    elif language.startswith('hi'):
        tts_lang = 'hi'
    elif language.startswith('es'):
        tts_lang = 'es'
    elif language.startswith('te'):
        tts_lang = 'te'
    elif language.startswith('kn'):
        tts_lang = 'kn'
    
    print(f"Converting text to speech using Google TTS with language {tts_lang}...")
    
    try:
        # Create gTTS object
        tts = gTTS(text=text, lang=tts_lang, slow=False)
        
        # Save to in-memory file object instead of disk
        mp3_fp = io.BytesIO()
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)
        
        # Get binary data and encode to base64
        audio_data = mp3_fp.read()
        audio_base64 = base64.b64encode(audio_data).decode('utf-8')
        
        print(f"Successfully created Google TTS audio in {tts_lang} in memory")
        
        return {
            "audio_base64": audio_base64,
            "content_type": "audio/mp3",
            "text": text
        }
    except Exception as e:
        print(f"Google TTS error: {str(e)}")
        return {
            "audio_base64": "",
            "content_type": "audio/mp3",
            "text": text,
            "error": str(e)
        }

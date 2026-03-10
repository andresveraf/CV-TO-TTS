"""
Audio Generation Utility Module
Handles OpenAI TTS API calls for converting text to speech
"""

import os
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI
from config.openai_voices import (
    VOICE_OPTIONS,
    TTS_MODELS,
    SPEED_PRESETS,
    OUTPUT_FORMATS
)

# Load environment variables
load_dotenv()

class AudioGenerator:
    """Handles audio generation using OpenAI TTS API"""
    
    def __init__(self, api_key=None):
        """Initialize the audio generator
        
        Args:
            api_key (str): OpenAI API key (if None, loads from environment)
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key not found. Please set OPENAI_API_KEY in .env file")
        
        self.client = OpenAI(api_key=self.api_key)
        self.audio_dir = "audio"
        
        # Ensure audio directory exists
        os.makedirs(self.audio_dir, exist_ok=True)
    
    def _sanitize_filename(self, filename):
        """Sanitize custom filename for filesystem safety
        
        Args:
            filename (str): Custom filename input
        
        Returns:
            str: Sanitized filename (lowercase, underscores only, max 50 chars)
        """
        import re
        
        # Convert to lowercase
        sanitized = filename.lower()
        
        # Replace spaces and special characters with underscores
        sanitized = re.sub(r'[^a-z0-9_-]', '_', sanitized)
        
        # Remove multiple consecutive underscores
        sanitized = re.sub(r'_+', '_', sanitized)
        
        # Remove leading/trailing underscores
        sanitized = sanitized.strip('_')
        
        # Limit to 50 characters
        sanitized = sanitized[:50]
        
        # If empty after sanitization, return None
        return sanitized if sanitized else None
    
    def generate_audio(self, text, voice, model, speed, output_format="mp3", custom_filename=None):
        """Generate audio from text using OpenAI TTS
        
        Args:
            text (str): Text to convert to speech
            voice (str): Voice name (alloy, echo, fable, onyx, nova, shimmer)
            model (str): Model name (gpt-4o-mini-tts, tts-1, tts-1-hd)
            speed (float): Speed multiplier (0.25 to 4.0)
            output_format (str): Output format (mp3, opus, aac, flac, wav, pcm)
            custom_filename (str): Custom filename base (without extension)
        
        Returns:
            dict: Contains file_path, file_size, duration, metadata
        """
        try:
            # Validate inputs
            if voice not in VOICE_OPTIONS:
                raise ValueError(f"Invalid voice: {voice}. Must be one of: {list(VOICE_OPTIONS.keys())}")
            
            if model not in TTS_MODELS:
                raise ValueError(f"Invalid model: {model}. Must be one of: {list(TTS_MODELS.keys())}")
            
            if not (0.25 <= speed <= 4.0):
                raise ValueError(f"Invalid speed: {speed}. Must be between 0.25 and 4.0")
            
            if output_format not in OUTPUT_FORMATS:
                raise ValueError(f"Invalid format: {output_format}. Must be one of: {list(OUTPUT_FORMATS.keys())}")
            
            # Calculate estimated duration
            word_count = len(text.split())
            avg_words_per_minute = 150 * speed
            estimated_duration_seconds = (word_count / avg_words_per_minute) * 60
            
            # Generate speech
            response = self.client.audio.speech.create(
                model=model,
                voice=voice,
                input=text,
                speed=speed,
                response_format=output_format
            )
            
            # Create output filename with custom name or default
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            if custom_filename:
                # Sanitize custom filename
                sanitized_name = self._sanitize_filename(custom_filename)
                if sanitized_name:
                    filename = f"{sanitized_name}_{timestamp}.{output_format}"
                else:
                    # Fallback to default if sanitization fails
                    filename = f"audio_{timestamp}.{output_format}"
            else:
                # Use default filename
                filename = f"audio_{timestamp}.{output_format}"
            
            file_path = os.path.join(self.audio_dir, filename)
            
            # Save audio file
            with open(file_path, "wb") as f:
                f.write(response.content)
            
            # Get file size
            file_size_bytes = os.path.getsize(file_path)
            file_size_mb = file_size_bytes / (1024 * 1024)
            
            # Return metadata
            return {
                "file_path": file_path,
                "filename": filename,
                "file_size_bytes": file_size_bytes,
                "file_size_mb": round(file_size_mb, 2),
                "duration_seconds": round(estimated_duration_seconds, 1),
                "word_count": word_count,
                "voice": voice,
                "model": model,
                "speed": speed,
                "format": output_format,
                "timestamp": timestamp,
                "voice_info": VOICE_OPTIONS[voice],
                "model_info": TTS_MODELS[model],
                "success": True,
                "message": "Audio generated successfully!"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"Error generating audio: {str(e)}"
            }
    
    def get_voice_options(self):
        """Get available voice options
        
        Returns:
            dict: Voice options with descriptions
        """
        return VOICE_OPTIONS
    
    def get_model_options(self):
        """Get available model options
        
        Returns:
            dict: Model options with descriptions
        """
        return TTS_MODELS
    
    def get_history(self):
        """Get list of generated audio files
        
        Returns:
            list: List of audio file metadata
        """
        history = []
        
        if not os.path.exists(self.audio_dir):
            return history
        
        for filename in sorted(os.listdir(self.audio_dir), reverse=True):
            if filename.endswith(('.mp3', '.opus', '.aac', '.flac', '.wav', '.pcm')):
                file_path = os.path.join(self.audio_dir, filename)
                file_size_bytes = os.path.getsize(file_path)
                file_size_mb = round(file_size_bytes / (1024 * 1024), 2)
                
                # Parse filename to extract metadata
                parts = filename.replace('.mp3', '').replace('.opus', '').replace('.aac', '').replace('.flac', '').replace('.wav', '').replace('.pcm', '').split('_')
                
                history.append({
                    "filename": filename,
                    "file_path": file_path,
                    "file_size_mb": file_size_mb,
                    "created_at": datetime.fromtimestamp(os.path.getctime(file_path)).strftime("%Y-%m-%d %H:%M:%S")
                })
        
        return history
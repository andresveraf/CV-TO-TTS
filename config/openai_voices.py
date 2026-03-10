# Voice configurations for OpenAI Text-to-Speech API
# OpenAI offers 6 built-in voices

# Available voices
# alloy: Androgynous, neutral tone
# echo: Male, American, confident
# fable: British, expressive, storytelling
# onyx: Male, American, deep, authoritative
# nova: Female, American, friendly, upbeat
# shimmer: Female, American, calm, professional

VOICE_OPTIONS = {
    "alloy": {
        "id": "alloy",
        "description": "Androgynous, neutral tone - versatile for various content",
        "gender": "Neutral",
        "accent": "American"
    },
    "echo": {
        "id": "echo",
        "description": "Male voice, confident tone - great for professional presentations",
        "gender": "Male",
        "accent": "American"
    },
    "fable": {
        "id": "fable",
        "description": "British voice, expressive - perfect for storytelling and narratives",
        "gender": "Male",
        "accent": "British"
    },
    "onyx": {
        "id": "onyx",
        "description": "Male voice, deep and authoritative - ideal for serious content",
        "gender": "Male",
        "accent": "American"
    },
    "nova": {
        "id": "nova",
        "description": "Female voice, friendly and upbeat - great for engaging presentations",
        "gender": "Female",
        "accent": "American"
    },
    "shimmer": {
        "id": "shimmer",
        "description": "Female voice, calm and professional - perfect for CV/narrative content",
        "gender": "Female",
        "accent": "American"
    }
}

# Available models
TTS_MODELS = {
    "gpt-4o-mini-tts": {
        "id": "gpt-4o-mini-tts",
        "description": "Economy quality, fastest - best value for cost-effective generation (recommended)",
        "quality": "Economy",
        "cost_per_1m_chars": "$5.00"
    },
    "tts-1": {
        "id": "tts-1",
        "description": "Standard quality, lower latency - optimized for real-time applications",
        "quality": "Standard",
        "cost_per_1m_chars": "$15.00"
    },
    "tts-1-hd": {
        "id": "tts-1-hd",
        "description": "High quality, higher latency - best for audio production and recordings",
        "quality": "High",
        "cost_per_1m_chars": "$30.00"
    }
}

# Speed presets
SPEED_PRESETS = {
    "slow": {
        "speed": 0.85,
        "description": "Slower pace - easier to follow, good for complex content"
    },
    "normal": {
        "speed": 1.0,
        "description": "Normal speed (default) - balanced pace"
    },
    "fast": {
        "speed": 1.15,
        "description": "Faster pace - efficient delivery, good for familiar content"
    },
    "very_fast": {
        "speed": 1.3,
        "description": "Very fast - maximum speed while maintaining clarity"
    }
}

# Output formats
OUTPUT_FORMATS = ["mp3", "opus", "aac", "flac", "wav", "pcm"]

# Recommended combinations for CV narration
RECOMMENDED_PRESETS = {
    # Economy presets (gpt-4o-mini-tts) - Best value, 3-6x cheaper
    "economy_female": {
        "voice": "shimmer",
        "model": "gpt-4o-mini-tts",
        "speed": "normal",
        "description": "Economy professional female voice - best value for CV (recommended)"
    },
    "economy_male": {
        "voice": "onyx",
        "model": "gpt-4o-mini-tts",
        "speed": "normal",
        "description": "Economy professional male voice - cost-effective CV narration"
    },
    "economy_neutral": {
        "voice": "alloy",
        "model": "gpt-4o-mini-tts",
        "speed": "normal",
        "description": "Economy neutral voice - versatile, budget-friendly option"
    },
    "economy_british": {
        "voice": "fable",
        "model": "gpt-4o-mini-tts",
        "speed": "slow",
        "description": "Economy British male voice - elegant storytelling, great value"
    },
    # Standard/High quality presets
    "professional_female": {
        "voice": "shimmer",
        "model": "tts-1-hd",
        "speed": "normal",
        "description": "Professional female voice - ideal for CV"
    },
    "professional_male": {
        "voice": "onyx",
        "model": "tts-1-hd",
        "speed": "normal",
        "description": "Professional male voice - authoritative CV narration"
    },
    "friendly_female": {
        "voice": "nova",
        "model": "tts-1",
        "speed": "normal",
        "description": "Friendly female voice - engaging CV presentation"
    },
    "british_male": {
        "voice": "fable",
        "model": "tts-1-hd",
        "speed": "slow",
        "description": "British male voice - elegant, storytelling style"
    },
    "neutral": {
        "voice": "alloy",
        "model": "tts-1",
        "speed": "normal",
        "description": "Neutral voice - versatile option"
    }
}

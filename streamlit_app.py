"""
CVAudioStudio - Professional Text-to-Speech Converter
Streamlit web interface for generating professional audio from any text using OpenAI TTS
Perfect for CVs, interview preparation, study materials, and practice questions
"""

import streamlit as st
import os
from datetime import datetime
from utils.audio_generator import AudioGenerator

# Page configuration
st.set_page_config(
    page_title="CVAudioStudio - Professional TTS",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
    }
    .info-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
    }
    .stat-card {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'generator' not in st.session_state:
    try:
        st.session_state.generator = AudioGenerator()
    except Exception as e:
        st.session_state.generator = None
        st.error(f"⚠️ Error initializing: {str(e)}")

if 'generated_audio' not in st.session_state:
    st.session_state.generated_audio = None

if 'history' not in st.session_state:
    st.session_state.history = []

# Header
st.markdown('<h1 class="main-header">🎙️ CVAudioStudio - Professional TTS</h1>', unsafe_allow_html=True)
st.markdown("---")

# Check if generator is initialized
if st.session_state.generator is None:
    st.error("❌ OpenAI API key not found!")
    st.info("Please add your OpenAI API key to the `.env` file:")
    st.code("OPENAI_API_KEY=your_api_key_here", language="bash")
    st.stop()

# Sidebar - Configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Voice selection
    st.subheader("🎤 Voice Selection")
    voice_options = st.session_state.generator.get_voice_options()
    voice_names = list(voice_options.keys())
    voice_descriptions = {name: f"{info['gender']}, {info['accent']} - {info['description']}" 
                          for name, info in voice_options.items()}
    
    selected_voice = st.selectbox(
        "Choose a voice:",
        options=voice_names,
        format_func=lambda x: f"{x.capitalize()} ({voice_options[x]['gender']}, {voice_options[x]['accent']})",
        index=voice_names.index('shimmer'),  # Default to shimmer
        help="Select the voice style for your audio"
    )
    
    # Show voice details
    voice_info = voice_options[selected_voice]
    st.info(f"**{selected_voice.capitalize()}**: {voice_info['description']}")
    
    st.markdown("---")
    
    # Model selection
    st.subheader("🔊 Model Selection")
    model_options = st.session_state.generator.get_model_options()
    model_names = list(model_options.keys())
    
    selected_model = st.selectbox(
        "Choose a model:",
        options=model_names,
        format_func=lambda x: f"{x} ({model_options[x]['quality']})",
        index=model_names.index('gpt-4o-mini-tts'),  # Default to economy model
        help="Higher quality = higher cost and slower generation"
    )
    
    # Show model details
    model_info = model_options[selected_model]
    st.info(f"**{selected_model}**: {model_info['description']}")
    
    # Cost estimation
    st.markdown("**Cost Estimate:**")
    if selected_model == "gpt-4o-mini-tts":
        st.success("💰 **$5.00/1M chars** - Best value! (~$0.01 for typical CV)")
    elif selected_model == "tts-1":
        st.warning("💵 **$15.00/1M chars** - Standard quality (~$0.03 for typical CV)")
    else:  # tts-1-hd
        st.error("💎 **$30.00/1M chars** - Premium quality (~$0.06 for typical CV)")
    
    st.markdown("---")
    
    # Speed control
    st.subheader("⚡ Speed Control")
    speed_options = {
        "Slow (0.85x)": 0.85,
        "Normal (1.0x)": 1.0,
        "Fast (1.15x)": 1.15,
        "Very Fast (1.3x)": 1.3
    }
    
    selected_speed_label = st.select_slider(
        "Select playback speed:",
        options=list(speed_options.keys()),
        value="Normal (1.0x)",
        help="Adjust the speaking speed"
    )
    selected_speed = speed_options[selected_speed_label]
    
    st.info(f"Current speed: **{selected_speed}x**")
    
    st.markdown("---")
    
    # Output format
    st.subheader("📁 Output Format")
    output_format = st.selectbox(
        "Choose audio format:",
        options=["mp3", "opus", "aac", "flac", "wav", "pcm"],
        index=0,
        help="MP3 is recommended for best compatibility"
    )
    
    st.markdown("---")
    
    # Quick links
    st.subheader("🔗 Quick Links")
    if st.button("📜 View History"):
        st.switch_page("pages/history.py")

# Main content area
col1, col2 = st.columns([3, 1])

with col1:
    st.header("📝 Enter Your Text")
    
    # Text input area
    default_text = """Andrés Vera is a passionate professional with expertise in data science and automation. 
He has extensive experience working with Python, web scraping, and machine learning technologies.
Andrés is dedicated to creating efficient solutions and leveraging cutting-edge tools to solve complex problems.
His background includes working on various projects involving data analysis, automation, and AI integration."""
    
    text_input = st.text_area(
        "Paste your CV or any text here:",
        value=default_text,
        height=200,
        max_chars=5000,
        help="Enter the text you want to convert to speech (max 5000 characters)"
    )
    
    # Character counter
    char_count = len(text_input)
    word_count = len(text_input.split())
    
    col_info1, col_info2, col_info3 = st.columns(3)
    with col_info1:
        st.metric("Characters", f"{char_count}/5000")
    with col_info2:
        st.metric("Words", word_count)
    with col_info3:
        # Estimate duration based on speed
        estimated_duration = (word_count / (150 * selected_speed)) * 60
        st.metric("Est. Duration", f"{estimated_duration:.1f}s")
    
    # Custom filename input
    st.markdown("---")
    custom_filename = st.text_input(
        "📝 Custom Filename (optional)",
        placeholder="e.g., interview_prep, my_cv, study_notes",
        max_chars=50,
        help="Enter a custom name for your audio file. Leave empty for default name 'audio'. Max 50 characters."
    )
    
    if custom_filename:
        st.info(f"💡 Filename will be: `{custom_filename.lower().replace(' ', '_')}_YYYYMMDD_HHMMSS.mp3`")
    else:
        st.info("💡 Filename will be: `audio_YYYYMMDD_HHMMSS.mp3` (default)")

with col2:
    st.header("📊 Summary")
    
    # Display current configuration
    st.markdown("### Current Settings")
    st.markdown(f"""
    - **Voice:** {selected_voice.capitalize()}
    - **Model:** {selected_model}
    - **Speed:** {selected_speed}x
    - **Format:** {output_format.upper()}
    """)
    
    # Cost estimate
    cost_per_char = {
        "gpt-4o-mini-tts": 5.0 / 1_000_000,
        "tts-1": 15.0 / 1_000_000,
        "tts-1-hd": 30.0 / 1_000_000
    }
    estimated_cost = char_count * cost_per_char[selected_model]
    
    st.markdown("---")
    st.metric("💰 Est. Cost", f"${estimated_cost:.4f}")

# Generate button
st.markdown("---")
generate_col1, generate_col2, generate_col3 = st.columns([2, 2, 1])

with generate_col1:
    generate_button = st.button(
        "🎙️ Generate Audio",
        type="primary",
        use_container_width=True,
        disabled=len(text_input.strip()) == 0
    )

with generate_col2:
    if st.session_state.generated_audio:
        clear_button = st.button(
            "🗑️ Clear Results",
            use_container_width=True
        )
        if clear_button:
            st.session_state.generated_audio = None
            st.rerun()

# Generate audio
if generate_button and len(text_input.strip()) > 0:
    with st.spinner("🎙️ Generating audio... This may take a few seconds..."):
        result = st.session_state.generator.generate_audio(
            text=text_input,
            voice=selected_voice,
            model=selected_model,
            speed=selected_speed,
            output_format=output_format,
            custom_filename=custom_filename.strip() if custom_filename.strip() else None
        )
        
        if result['success']:
            st.session_state.generated_audio = result
            st.success("✅ Audio generated successfully!")
        else:
            st.error(f"❌ Error: {result['message']}")

# Display results
if st.session_state.generated_audio:
    result = st.session_state.generated_audio
    
    st.markdown("---")
    st.header("🎵 Generated Audio")
    
    # Success message
    st.markdown(f'<div class="success-box">✅ {result["message"]}</div>', unsafe_allow_html=True)
    
    # Audio player and download
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Read audio file
        try:
            with open(result['file_path'], 'rb') as audio_file:
                audio_bytes = audio_file.read()
                st.audio(audio_bytes, format=f'audio/{result["format"]}')
        except Exception as e:
            st.error(f"Error loading audio: {str(e)}")
        
        # Download button
        try:
            with open(result['file_path'], 'rb') as audio_file:
                st.download_button(
                    label="⬇️ Download Audio File",
                    data=audio_file,
                    file_name=result['filename'],
                    mime=f'audio/{result["format"]}',
                    use_container_width=True
                )
        except Exception as e:
            st.error(f"Error preparing download: {str(e)}")
    
    with col2:
        # Display metadata
        st.markdown("### 📊 File Details")
        st.markdown(f"""
        <div class="stat-card">
            <strong>Filename:</strong><br>
            {result['filename']}
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="stat-card">
            <strong>Size:</strong><br>
            {result['file_size_mb']} MB
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="stat-card">
            <strong>Duration:</strong><br>
            {result['duration_seconds']}s
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="stat-card">
            <strong>Words:</strong><br>
            {result['word_count']}
        </div>
        """, unsafe_allow_html=True)
    
    # Additional metadata
    with st.expander("🔍 View Full Metadata"):
        st.json({
            "voice": result['voice'],
            "model": result['model'],
            "speed": result['speed'],
            "format": result['format'],
            "timestamp": result['timestamp'],
            "voice_info": result['voice_info'],
            "model_info": result['model_info']
        })

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6c757d; padding: 1rem;">
    <p>Built with ❤️ using Streamlit and OpenAI TTS API</p>
    <p>💡 Tip: Check the History page to view all generated audio files</p>
</div>
""", unsafe_allow_html=True)
"""
CVAudioStudio - Audio Generation History Page
Displays and manages previously generated audio files
"""

import streamlit as st
import os
from datetime import datetime
from utils.audio_generator import AudioGenerator

# Page configuration
st.set_page_config(
    page_title="History - CVAudioStudio",
    page_icon="📜",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .history-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .file-card {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        margin-bottom: 1rem;
    }
    .empty-state {
        text-align: center;
        padding: 3rem;
        color: #6c757d;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'generator' not in st.session_state:
    try:
        st.session_state.generator = AudioGenerator()
    except Exception as e:
        st.session_state.generator = None

# Header
st.markdown('<h1 class="history-header">📜 Audio Generation History</h1>', unsafe_allow_html=True)
st.markdown("---")

# Check if generator is initialized
if st.session_state.generator is None:
    st.error("❌ OpenAI API key not found!")
    st.info("Please add your OpenAI API key to the `.env` file:")
    st.stop()

# Get history
history = st.session_state.generator.get_history()

# Sidebar filters
with st.sidebar:
    st.header("🔍 Filters & Actions")
    
    # Search filter
    search_term = st.text_input(
        "🔎 Search files:",
        placeholder="Enter filename...",
        help="Search by filename"
    )
    
    st.markdown("---")
    
    # Sort options
    sort_by = st.selectbox(
        "📊 Sort by:",
        options=["Newest first", "Oldest first", "Largest files", "Smallest files"],
        index=0
    )
    
    st.markdown("---")
    
    # Refresh button
    if st.button("🔄 Refresh History", use_container_width=True):
        st.rerun()
    
    st.markdown("---")
    
    # Stats
    st.subheader("📈 Statistics")
    total_files = len(history)
    if total_files > 0:
        total_size = sum(item['file_size_mb'] for item in history)
        st.metric("Total Files", total_files)
        st.metric("Total Size", f"{total_size:.2f} MB")
        st.metric("Avg Size", f"{total_size/total_files:.2f} MB")
    else:
        st.info("No files generated yet")

# Main content
if not history:
    st.markdown("""
    <div class="empty-state">
        <h2>📭 No Audio Files Yet</h2>
        <p>You haven't generated any audio files yet.</p>
        <p>Go to the main page to create your first audio!</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🎙️ Go to Generate Audio", type="primary", use_container_width=True):
            st.switch_page("streamlit_app.py")
else:
    # Apply filters
    if search_term:
        history = [item for item in history if search_term.lower() in item['filename'].lower()]
    
    # Apply sorting
    if sort_by == "Newest first":
        history.sort(key=lambda x: x['created_at'], reverse=True)
    elif sort_by == "Oldest first":
        history.sort(key=lambda x: x['created_at'], reverse=False)
    elif sort_by == "Largest files":
        history.sort(key=lambda x: x['file_size_mb'], reverse=True)
    elif sort_by == "Smallest files":
        history.sort(key=lambda x: x['file_size_mb'], reverse=False)
    
    # Display results count
    st.info(f"📊 Showing {len(history)} file(s)")
    
    st.markdown("---")
    
    # Display files in a grid
    for idx, item in enumerate(history):
        with st.expander(f"📄 {item['filename']}", expanded=(idx == 0)):
            col1, col2, col3 = st.columns([3, 2, 1])
            
            with col1:
                st.markdown(f"""
                <div class="file-card">
                    <strong>📁 Filename:</strong> {item['filename']}<br>
                    <strong>📅 Created:</strong> {item['created_at']}<br>
                    <strong>💾 Size:</strong> {item['file_size_mb']} MB
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                # Audio player
                try:
                    with open(item['file_path'], 'rb') as audio_file:
                        audio_bytes = audio_file.read()
                        st.audio(audio_bytes, format='audio/mp3')
                except Exception as e:
                    st.error(f"Error loading audio: {str(e)}")
            
            with col3:
                st.markdown("**Actions:**")
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Download button
                try:
                    with open(item['file_path'], 'rb') as audio_file:
                        st.download_button(
                            label="⬇️ Download",
                            data=audio_file,
                            file_name=item['filename'],
                            mime='audio/mp3',
                            use_container_width=True,
                            key=f"download_{idx}"
                        )
                except Exception as e:
                    st.error(f"Error: {str(e)}")
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Delete button
                if st.button("🗑️ Delete", key=f"delete_{idx}", use_container_width=True):
                    try:
                        os.remove(item['file_path'])
                        st.success(f"✅ Deleted {item['filename']}")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error deleting file: {str(e)}")
    
    st.markdown("---")
    
    # Batch actions
    st.subheader("⚡ Batch Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🗑️ Delete All Files", use_container_width=True):
            if st.session_state.get('confirm_delete_all', False):
                try:
                    for item in history:
                        os.remove(item['file_path'])
                    st.success("✅ All files deleted successfully!")
                    st.session_state.confirm_delete_all = False
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {str(e)}")
            else:
                st.session_state.confirm_delete_all = True
                st.warning("⚠️ Click again to confirm deletion")
    
    with col2:
        if st.button("📁 Open Audio Folder", use_container_width=True):
            audio_dir = "audio"
            if os.path.exists(audio_dir):
                st.info(f"📁 Audio folder location: `{os.path.abspath(audio_dir)}`")
                st.code(f"File path: {os.path.abspath(audio_dir)}")
            else:
                st.error("Audio folder not found")
    
    with col3:
        if st.button("🎙️ Generate New Audio", type="primary", use_container_width=True):
            st.switch_page("streamlit_app.py")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6c757d; padding: 1rem;">
    <p>💡 Files are stored in the <code>audio/</code> directory</p>
</div>
""", unsafe_allow_html=True)
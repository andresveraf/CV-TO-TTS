# 🎙️ CVAudioStudio - Professional Text-to-Speech Converter

[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red)](https://streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

A professional, web-based text-to-speech converter powered by OpenAI's TTS API. Perfect for creating audio versions of CVs, interview preparation materials, study notes, and practice questions.

## ✨ Features

- 🎤 **Multiple Voice Options** - Choose from 6 different professional voices
- 🔊 **3 Quality Models** - Economy, Standard, and Premium TTS models
- ⚡ **Speed Control** - Adjust playback speed from 0.25x to 4.0x
- 📊 **Cost Estimation** - Real-time cost calculator for informed decisions
- 📜 **History Tracking** - View, play, and manage all generated audio files
- 💾 **Multiple Formats** - Support for MP3, Opus, AAC, FLAC, WAV, PCM
- 🎯 **Character Counter** - Live character/word count and duration estimation
- 🚀 **Easy Deployment** - One-click deployment to Streamlit Cloud

## 🎯 Use Cases

- **Professional Audio** - Convert CVs and resumes to audio
- **Interview Prep** - Practice with audio versions of common interview questions
- **Study Materials** - Listen to notes, textbooks, and study guides
- **Language Learning** - Hear correct pronunciation of foreign language texts
- **Accessibility** - Create audio versions of written content
- **Content Creation** - Generate voiceovers for presentations and videos

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/CVAudioStudio.git
cd CVAudioStudio
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up your API key**
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

4. **Run the application**
```bash
streamlit run streamlit_app.py
```

5. **Open your browser**
Navigate to `http://localhost:8501`

## 📖 Usage

### Generate Audio

1. **Enter your text** - Paste your CV, study material, or any text (up to 5000 characters)
2. **Choose a voice** - Select from 6 professional voice options
3. **Select model** - Economy (cheapest), Standard, or Premium (best quality)
4. **Adjust speed** - Control playback speed (0.25x - 4.0x)
5. **Generate** - Click "Generate Audio" and wait a few seconds
6. **Download** - Play in browser or download the audio file

### View History

- Click "📜 View History" in the sidebar
- See all previously generated audio files
- Play, download, or delete files
- Search and sort by date or size

## 💰 Pricing

CVAudioStudio uses OpenAI's TTS API with transparent pricing:

| Model | Price | Quality | Best For |
|-------|-------|---------|----------|
| **gpt-4o-mini-tts** | $5.00/1M chars | High | Most use cases |
| **tts-1** | $15.00/1M chars | Standard | Professional audio |
| **tts-1-hd** | $30.00/1M chars | Premium | Best quality |

**Example costs:**
- Typical CV (500 chars): ~$0.01 (Economy model)
- Study notes (2000 chars): ~$0.03 (Economy model)
- Interview prep (1000 chars): ~$0.02 (Economy model)

## 🎨 Available Voices

| Voice | Gender | Accent | Description |
|-------|--------|--------|-------------|
| **alloy** | Neutral | American | Clear and articulate |
| **echo** | Male | American | Deep and authoritative |
| **fable** | Male | British | Warm and engaging |
| **onyx** | Male | American | Confident and professional |
| **nova** | Female | American | Friendly and clear |
| **shimmer** | Female | American | Expressive and warm |

## 📁 Project Structure

```
CVAudioStudio/
├── streamlit_app.py          # Main application
├── pages/
│   └── 1_📜_History.py      # History page
├── utils/
│   └── audio_generator.py    # TTS generation logic
├── config/
│   ├── openai_voices.py     # Voice configurations
│   └── voices.py            # Voice metadata
├── audio/                    # Generated audio files
├── text/                     # Sample text files
├── logs/                     # Application logs
├── requirements.txt          # Python dependencies
├── .env.example             # Environment variables template
├── README.md                # This file
├── QUICKSTART.md            # 5-minute setup guide
├── DEPLOYMENT.md            # Deployment instructions
└── DEPLOYMENT_COMPARISON.md # FastAPI vs Streamlit comparison
```

## 🚀 Deployment

### Streamlit Cloud (Recommended - Free & Easy)

1. **Push code to GitHub**
```bash
git add .
git commit -m "Initial commit"
git push origin main
```

2. **Deploy to Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Connect your GitHub repository
   - Select `streamlit_app.py`
   - Add your OpenAI API key in "Secrets"
   - Deploy!

Your app will be live at: `https://cvaudiostudio.streamlit.app`

For detailed deployment instructions, see [DEPLOYMENT.md](DEPLOYMENT.md).

## 🛠️ Development

### Local Development

```bash
# Install development dependencies
pip install -r requirements.txt

# Run with auto-reload
streamlit run streamlit_app.py --server.runOnSave true

# View logs
tail -f logs/app.log
```

### Adding New Voices

Edit `config/openai_voices.py` to add custom voice configurations.

### Customizing Models

Modify `utils/audio_generator.py` to add new model options.

## 📚 Documentation

- [Quick Start Guide](QUICKSTART.md) - Get running in 5 minutes
- [Deployment Guide](DEPLOYMENT.md) - Complete deployment instructions
- [Deployment Comparison](DEPLOYMENT_COMPARISON.md) - FastAPI vs Streamlit

## 🔧 Configuration

### Environment Variables

Create a `.env` file:

```bash
# Required
OPENAI_API_KEY=your_api_key_here

# Optional
OPENAI_ORG_ID=your_organization_id
LOG_LEVEL=INFO
MAX_TEXT_LENGTH=5000
```

### Streamlit Configuration

Edit `.streamlit/config.toml` to customize:

```toml
[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"

[client]
showErrorDetails = false

[logger]
level = "info"
```

## 🐛 Troubleshooting

### Common Issues

**"OpenAI API key not found"**
- Ensure `.env` file exists with your API key
- Restart the application after adding the key

**"Error generating audio"**
- Check your OpenAI API key is valid
- Verify you have sufficient API credits
- Check the logs in `logs/app.log`

**Audio not playing**
- Try a different browser
- Check browser console for errors
- Ensure audio format is supported

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [OpenAI](https://openai.com/) for the TTS API
- [Streamlit](https://streamlit.io/) for the amazing framework
- The open-source community

## 📧 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Email: your.email@example.com
- Twitter: [@yourusername](https://twitter.com/yourusername)

## ⭐ Show Your Support

If you find this project useful, please consider:
- ⭐ Starring it on GitHub
- 🐦 Sharing it on Twitter
- 💬 Telling your friends and colleagues

---

**Built with ❤️ using Streamlit and OpenAI TTS API**

**[⬆ Back to Top](#-cvaudiostudio---professional-text-to-speech-converter)**
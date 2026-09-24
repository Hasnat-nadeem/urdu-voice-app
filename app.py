import asyncio
import os
import streamlit as st
import edge_tts

# Page Configuration
st.set_page_config(
    page_title="Urdu AI Voice Generator",
    page_icon="🎙️",
    layout="centered"
)

# Custom CSS for styling and RTL Urdu text support
st.markdown("""
<style>
    .main-title {
        text-align: center;
        color: #FF4B4B;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .sub-title {
        text-align: center;
        color: #555;
        margin-bottom: 25px;
    }
    .urdu-text {
        direction: rtl;
        text-align: right;
        font-size: 20px;
        font-family: 'Nafees Nastaleeq', 'Jameel Noori Nastaleeq', 'Urdu Typesetting', 'Segoe UI', sans-serif;
    }
    .stTextArea textarea {
        direction: rtl;
        text-align: right;
        font-size: 18px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>🎙️ Urdu AI Voice Generator</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>100% Free - High Quality Urdu AI Voices for Shorts & Reels</p>", unsafe_allow_html=True)

st.divider()

# Available Urdu & Regional Voices
VOICES = {
    "🇵🇰 Asad (Male - Natural Urdu)": "ur-PK-AsadNeural",
    "🇵🇰 Uzma (Female - Soft Urdu)": "ur-PK-UzmaNeural",
    "🇮🇳 Madhur (Male - Urdu/Hindi)": "hi-IN-MadhurNeural",
    "🇮🇳 Swara (Female - Urdu/Hindi)": "hi-IN-SwaraNeural"
}

# Sidebar for Settings
st.sidebar.header("⚙️ Audio Settings")

selected_voice_name = st.sidebar.selectbox(
    "🎙️ Voice Choose Karein:",
    list(VOICES.keys())
)
voice_id = VOICES[selected_voice_name]

# Speed Control
speed_option = st.sidebar.select_slider(
    "⚡ Voice Speed:",
    options=["Slow (-20%)", "Slightly Slow (-10%)", "Normal (0%)", "Fast (+10%)", "Very Fast (+20%)"],
    value="Normal (0%)"
)

speed_mapping = {
    "Slow (-20%)": "-20%",
    "Slightly Slow (-10%)": "-10%",
    "Normal (0%)": "+0%",
    "Fast (+10%)": "+10%",
    "Very Fast (+20%)": "+20%"
}
rate_val = speed_mapping[speed_option]

# Pitch Control
pitch_option = st.sidebar.select_slider(
    "🎵 Voice Pitch (Tone):",
    options=["Deep (-10Hz)", "Low (-5Hz)", "Normal (0Hz)", "High (+5Hz)"],
    value="Normal (0Hz)"
)

pitch_mapping = {
    "Deep (-10Hz)": "-10Hz",
    "Low (-5Hz)": "-5Hz",
    "Normal (0Hz)": "+0Hz",
    "High (+5Hz)": "+5Hz"
}
pitch_val = pitch_mapping[pitch_option]

st.subheader("📝 Apna Urdu Script Yahan Likhien:")

# Input text area
user_script = st.text_area(
    label="Urdu Text Input",
    label_visibility="collapsed",
    height=180,
    placeholder="یہاں اپنا اردو متن لکھیں... (مثلاً: کیا آپ جانتے ہیں کہ صبر کا پھل کتنا میٹھا ہوتا ہے؟)"
)

# Async TTS Generation Function
async def generate_speech(text, voice, rate, pitch, output_file):
    communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
    await communicate.save(output_file)

if st.button("🚀 Audio Generate Karein", use_container_width=True):
    if not user_script.strip():
        st.error("⚠️ Meherbani karke pehle kuch Urdu text likhein!")
    else:
        with st.spinner("⏳ Audio generate ho rahi hai, baraye meherbani intezar karein..."):
            try:
                output_filename = "generated_urdu_voice.mp3"
                asyncio.run(generate_speech(user_script, voice_id, rate_val, pitch_val, output_filename))
                
                st.success("✅ Audio kamyabi se tayar ho gayi hai!")
                
                # Read audio file
                with open(output_filename, "rb") as f:
                    audio_bytes = f.read()
                
                # Audio player
                st.audio(audio_bytes, format="audio/mp3")
                
                # Download button
                st.download_button(
                    label="📥 MP3 Audio Download Karein",
                    data=audio_bytes,
                    file_name="Urdu_AI_Voice.mp3",
                    mime="audio/mp3",
                    use_container_width=True
                )
            except Exception as e:
                st.error(f"❌ Error aaya hai: {str(e)}")

st.divider()

# Instructions Section
with st.expander("❓ Help & Information"):
    st.markdown("""
    * **Voices:** `ur-PK-AsadNeural` aur `ur-PK-UzmaNeural` HD audio engines.
    """)

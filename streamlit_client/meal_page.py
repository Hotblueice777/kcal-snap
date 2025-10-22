# meal_page.py
import streamlit as st
import requests, os, time
import base64
import pandas as pd

BACKEND = os.getenv("BACKEND", "http://localhost:8000")

def render():
    st.title("🍽️ My Meal — Daily Summary")

    # 模拟数据
    meals = [
        {"time": "08:20", "name": "Toast + Egg", "cal": 250, "protein": 10, "fat": 8, "carb": 35},
        {"time": "13:10", "name": "Sushi", "cal": 252, "protein": 12.6, "fat": 7.2, "carb": 39.6},
    ]
    df = pd.DataFrame(meals)

    st.subheader("📆 Today's Meals")
    st.dataframe(df, use_container_width=True)

    total = df[["cal","protein","fat","carb"]].sum()
    st.markdown("### 🔢 Daily Totals")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Calories (kcal)", f"{total['cal']:.0f}")
    c2.metric("Protein (g)", f"{total['protein']:.1f}")
    c3.metric("Fat (g)", f"{total['fat']:.1f}")
    c4.metric("Carbs (g)", f"{total['carb']:.1f}")

    st.markdown("---")

    # QnA & Speach
    st.title("🧠 AI Health Assistant")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🎤 Speak Now"):
            st.info("Recording for 5 seconds...")
            import sounddevice as sd
            from scipy.io.wavfile import write
            fs = 44100
            seconds = 5
            myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
            sd.wait()
            write("input.wav", fs, myrecording)
            st.success("Recording complete!")

            files = {"audio_file": open("input.wav", "rb")}
            r = requests.post(f"{BACKEND}/assistant/api/speech_to_text", files=files)
            text = r.json().get("text", "")
            st.write(f"🗣 You said: {text}")

            if text:
                with st.spinner("Thinking..."):
                    r2 = requests.post(f"{BACKEND}/assistant/api/ask", json={"text": text})
                    answer = r2.json().get("answer", "")
                    st.success(answer)

                    # Speak response
                    tts = requests.post(f"{BACKEND}/assistant/api/text_to_speech", json={"text": answer})
                    audio_base64 = tts.json().get("audio", "")
            if audio_base64:
                st.audio(base64.b64decode(audio_base64), format="audio/wav")

    with col2:
        user_input = st.text_input("💬 Or type your question")
        if st.button("Ask Assistant"):
            r = requests.post(f"{BACKEND}/assistant/api/ask", json={"text": user_input})
            st.success(r.json().get("answer", ""))
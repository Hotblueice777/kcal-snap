# streamlit_client/meal_page.py
import streamlit as st
import requests, os, time, base64
import pandas as pd

BACKEND = os.getenv("BACKEND", "http://localhost:8000")

def render():
    st.title("🍽️ My Meal — Daily Summary")

    # ✅ 显示每日统计
    if "meals" not in st.session_state or not st.session_state["meals"]:
        st.info("No meals added yet. Go to Scan & Analyze to add your first meal!")
        return

    df = pd.DataFrame(st.session_state["meals"])
    st.subheader("📆 Today's Meals")
    st.dataframe(df, use_container_width=True)

    total = df[["cal", "protein", "fat", "carb"]].sum()
    st.markdown("### 🔢 Daily Totals")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Calories (kcal)", f"{total['cal']:.0f}")
    c2.metric("Protein (g)", f"{total['protein']:.1f}")
    c3.metric("Fat (g)", f"{total['fat']:.1f}")
    c4.metric("Carbs (g)", f"{total['carb']:.1f}")

    st.markdown("---")
    st.title("🧠 AI Health Assistant")

    col1, col2 = st.columns(2)

    # 🎤 语音提问
    with col1:
        if st.button("🎤 Speak Now"):
            import sounddevice as sd
            from scipy.io.wavfile import write

            fs = 44100
            seconds = 5
            st.info("Recording for 5 seconds...")
            myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
            sd.wait()
            write("input.wav", fs, myrecording)
            st.success("Recording complete!")

            # Step 1️⃣ Speech → Text
            files = {"audio_file": open("input.wav", "rb")}
            r = requests.post(f"{BACKEND}/api/speech_to_text", files=files)
            text = r.json().get("text", "")
            if not text:
                st.warning("Speech not recognized.")
                return
            st.write(f"🗣 You said: {text}")

            # Step 2️⃣ Text → RAG
            with st.spinner("Thinking..."):
                r2 = requests.post(f"{BACKEND}/api/ask_rag", json={"text": text})
                answer = r2.json().get("answer", "No response.")
                st.success(answer)

            # Step 3️⃣ RAG Answer → Speech
            with st.spinner("Converting to speech..."):
                tts = requests.post(f"{BACKEND}/api/text_to_speech", json={"text": answer})
                audio_base64 = tts.json().get("audio", "")
                if audio_base64:
                    st.audio(base64.b64decode(audio_base64), format="audio/wav")

    # 💬 文字输入
    with col2:
        user_input = st.text_input("💬 Type your question")
        if st.button("Ask Assistant"):
            with st.spinner("Thinking..."):
                r = requests.post(f"{BACKEND}/api/ask_rag", json={"text": user_input})
                answer = r.json().get("answer", "No response.")
                st.success(answer)

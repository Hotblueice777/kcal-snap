# assistant_api.py
from fastapi import FastAPI, UploadFile, File, Body
import azure.cognitiveservices.speech as speechsdk
import httpx, os
import base64

app = FastAPI()

# ======= Speech to Text =======
@app.post("/api/speech_to_text")
async def speech_to_text(audio_file: UploadFile = File(...)):
    """Convert speech to text using Azure Speech Service"""
    key = os.getenv("AZURE_SPEECH_KEY")
    region = os.getenv("AZURE_SPEECH_REGION")

    temp_path = "temp_audio.wav"
    with open(temp_path, "wb") as f:
        f.write(await audio_file.read())

    speech_config = speechsdk.SpeechConfig(subscription=key, region=region)
    audio_config = speechsdk.audio.AudioConfig(filename=temp_path)
    recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
    result = recognizer.recognize_once()

    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return {"text": result.text}
    else:
        return {"error": str(result.reason)}

# ======= Text Assistant (QnA) =======
@app.post("/api/ask")
async def ask_assistant(payload: dict = Body(...)):
    endpoint = os.getenv("AZURE_QNA_ENDPOINT")
    key = os.getenv("AZURE_QNA_KEY")
    project = os.getenv("AZURE_QNA_PROJECT")
    deployment = os.getenv("AZURE_QNA_DEPLOYMENT")

    url = f"{endpoint}/language/:query-knowledgebases?projectName={project}&api-version=2021-10-01&deploymentName={deployment}"
    headers = {"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"}

    data = {
        "question": payload.get("question", payload.get("text", "")),
        "top": 3,
        "includeUnstructuredSources": True
    }

    async with httpx.AsyncClient(timeout=15) as client:
        res = await client.post(url, headers=headers, json=data)
        print("Azure QnA Response:", res.text)  # 🔍 调试：打印 Azure 返回原文

    try:
        r_json = res.json()
        answer = r_json["answers"][0]["answer"]
    except Exception:
        answer = "Sorry, I couldn't find an answer."

    return {"answer": answer}

    print(">>> endpoint:", endpoint)
    print(">>> project:", project)
    print(">>> deployment:", deployment)

# ======= Text to Speech =======
@app.post("/api/text_to_speech")
async def text_to_speech(payload: dict = Body(...)):
    """Convert text to speech (TTS)"""
    key = os.getenv("AZURE_SPEECH_KEY")
    region = os.getenv("AZURE_SPEECH_REGION")
    text = payload.get("text", "")

    speech_config = speechsdk.SpeechConfig(subscription=key, region=region)
    speech_config.speech_synthesis_voice_name = "en-US-JennyNeural"
    audio_path = "output_audio.wav"
    audio_config = speechsdk.audio.AudioOutputConfig(filename=audio_path)

    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    result = synthesizer.speak_text_async(text).get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        # 将音频转成 base64 返回前端
        with open(audio_path, "rb") as f:
            audio_base64 = base64.b64encode(f.read()).decode("utf-8")
        return {"audio": audio_base64}
    else:
        return {"error": str(result.reason)}
    
    print(">>> Requesting Azure Language API")
    print("endpoint:", endpoint)
    print("project:", project)
    print("deployment:", deployment)
    print("text:", payload.get("text", ""))
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import os
import wave
import contextlib
import shutil

router = APIRouter()

# Paths for placeholder files
INPUT_AUDIO_PATH = "car-horn.wav"
OUTPUT_AUDIO_PATH = "./car-horn.wav"


@router.get("/status")
async def get_status():
    """Check if stream routes are active."""
    return {"status": "stream routes active"}


# ------------------------
# 🎤 AUDIO INPUT ENDPOINT
# ------------------------
@router.post("/input")
async def audio_input(file: UploadFile = File(None)):
    """
    Receives an uploaded WAV file or uses a placeholder file.
    Later this will represent live microphone input from transmitter.
    """
    if file:
        # Save uploaded audio as input_audio.wav
        with open(INPUT_AUDIO_PATH, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        filename = file.filename
    else:
        # If no file uploaded, use existing placeholder
        filename = "placeholder.wav"
        if not os.path.exists(INPUT_AUDIO_PATH):
            raise HTTPException(status_code=404, detail="No audio input file available.")

    # Read audio metadata
    with contextlib.closing(wave.open(INPUT_AUDIO_PATH, 'rb')) as f:
        channels = f.getnchannels()
        sample_width = f.getsampwidth()
        framerate = f.getframerate()
        frames = f.getnframes()
        duration = frames / float(framerate)

    return {
        "message": "Audio input received successfully",
        "file": filename,
        "channels": channels,
        "sample_width_bytes": sample_width,
        "sample_rate_hz": framerate,
        "duration_sec": round(duration, 2)
    }


# ------------------------
# 🔊 AUDIO OUTPUT ENDPOINT
# ------------------------
@router.get("/output")
async def audio_output():
    """
    Returns a WAV file as output audio.
    Later, this will be replaced with a real-time translated audio stream.
    """
    if not os.path.exists(OUTPUT_AUDIO_PATH):
        raise HTTPException(status_code=404, detail="Output audio file not found.")

    # Serve the WAV file to the listener
    return FileResponse(OUTPUT_AUDIO_PATH, media_type="audio/wav", filename="output.wav")

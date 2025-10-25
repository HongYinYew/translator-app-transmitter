from fastapi import APIRouter, WebSocket
import os
import ffmpeg
import tempfile

router = APIRouter()

@router.get("/status")
async def get_status():
    """Check if stream routes are active."""
    return {"status": "stream routes active"}

@router.websocket("/ws/audio")
async def audio_stream(websocket: WebSocket):
    await websocket.accept()
    print("Client connected")

    # Temporary WebM file to collect audio
    tmp_fd, tmp_path = tempfile.mkstemp(suffix=".webm")
    os.close(tmp_fd)

    try:
        with open(tmp_path, "wb") as f:
            while True:
                data = await websocket.receive_bytes()
                f.write(data)
    except Exception as e:
        print("Connection closed:", e)
    finally:
        print("Received WebM:", tmp_path)

        # Convert to WAV
        output_wav = "received.wav"
        ffmpeg.input(tmp_path).output(output_wav, format='wav').run()
        os.remove(tmp_path)
        print("Converted and saved:", output_wav)
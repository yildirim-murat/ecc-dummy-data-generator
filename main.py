import os
import random
from datetime import datetime, timedelta
from fastapi import FastAPI, WebSocket
import asyncio
from dotenv import load_dotenv

from pydantic import BaseModel
from starlette.responses import StreamingResponse

app = FastAPI()
load_dotenv()
class CallInfo(BaseModel):
    call_id: str
    phone_number: str
    location: dict

def generate_call_id():
    timestamp = (datetime.now()).strftime("%Y%m%d%H%M%S%f")[:-3]
    unique_number = f"{random.randint(0, 999):03d}"
    return f"{timestamp}{unique_number}"

def generate_phone_number():
    start = random.choice(["03", "05"])
    number = start + ''.join(random.choices("0123456789", k=9))
    return number

def generate_location():
    return {
        "latitude": random.uniform(39.9334, 39.9886),
        "longitude": random.uniform(32.8597, 32.9357)
    }

min_value = int(os.getenv('minValue'))
max_value = int(os.getenv('maxValue'))
@app.websocket("/call-info")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            call_id = generate_call_id()
            phone_number = generate_phone_number()
            location = generate_location()
            call_info = CallInfo(
                call_id=call_id,
                phone_number=phone_number,
                location=location
            )
            await websocket.send_json(call_info.dict())
            await asyncio.sleep(random.randint(min_value, max_value))
    except Exception as e:
        print(f"WebSocket connection closed: {e}")
    finally:
        await websocket.close()

@app.get("/audio")
async def stream_audio():
    headers = {
        "Cache-Control": "no-cache, no-store, must-revalidate",
        "Pragma": "no-cache",
        "Expires": "0"
    }

    def generate():
        audio_file_path = os.path.join(os.getcwd(), str(random.randint(1, 5)) + ".mp3")
        chunk_size = 1024
        with open(audio_file_path, "rb") as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    f.seek(0)
                    chunk = f.read(chunk_size)
                if not chunk:
                    break
                yield chunk

    return StreamingResponse(generate(), media_type="audio/mp3", headers=headers)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
import asyncio
import random
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI(title='Dummy Data Generator')



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Geliştirme aşamasında tüm orijinlere izin verilir, ancak prod'da sınırlı olmalı
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def generate_phone_number():
    number = "0312" + "".join([str(random.randint(0, 9)) for _ in range(7)])
    return number


def generate_time():
    return datetime.now().strftime("%H:%M:%S")


def generate_date():
    return datetime.now().strftime("%d.%m.%Y")


def generate_lat_long():
    longitude = random.uniform(36.0, 42.0)
    latitude = random.uniform(26.0, 45.0)
    return latitude, longitude


def generate_data():
    phone_number = generate_phone_number()
    time_stamp = generate_time() + " " + generate_date()
    latitude, longitude = generate_lat_long()

    data = {
        "phone_number": phone_number,
        "time_stamp": time_stamp,
        "latitude": latitude,
        "longitude": longitude
    }
    return data


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    print('Accepting client connection...')
    await websocket.accept()
    while True:
        try:
            delay = random.uniform(5, 10)
            await asyncio.sleep(delay)
            data = generate_data()
            await websocket.send_json(data)
            print("Data sent:", data)

        except Exception as e:
            print('WebSocket Error: ', e)
            break

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001)
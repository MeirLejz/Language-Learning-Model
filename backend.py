# backend.py
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import os
app = FastAPI()

# Mount the static files directory for serving the frontend
# app.mount("/static", StaticFiles(directory="static"), name="static")

messages = []

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        messages.append(data)
        await websocket.send_text(data)

@app.get("/", response_class=HTMLResponse)
async def read_main():
    with open(os.path.join("frontend", "index.html"), "r") as file:
        html_content = file.read()
    return html_content

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8000)

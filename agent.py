import socketio
import subprocess
import os

sio = socketio.Client()
# כתובת השרת המתווך (תחליף בכתובת שתקבל מ-Render)
SERVER_URL = 'https://expert-bot-relay.onrender.com'

@sio.event
def connect():
    print(">>> EXPERT-BOT AGENT ONLINE")

@sio.on('execute_ai_cmd')
def handle_cmd(data):
    cmd = data.get('cmd')
    print(f"Executing System Command: {cmd}")
    try:
        # הרצה אמיתית ב-CMD/Terminal
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=20)
        output = result.stdout if result.returncode == 0 else result.stderr
        sio.emit('task_result', {'output': output})
    except Exception as e:
        sio.emit('task_result', {'output': str(e)})

if __name__ == '__main__':
    sio.connect(SERVER_URL)
    sio.wait()

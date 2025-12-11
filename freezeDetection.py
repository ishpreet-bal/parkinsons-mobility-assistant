from mpu6050 import mpu6050
import time
from datetime import datetime
import math
from flask import Flask, jsonify, request
from flask_socketio import SocketIO, emit
import threading

# ----- Accelerometer Freeze Detection Setup -----

# Initialize the sensor
sensor = mpu6050(0x68)

# Exponential smoothing factor for baseline update
alpha = 0.05  
baseline = sensor.get_accel_data()

# Thresholds for detecting freeze events
ERROR_TOLERANCE = 4.8         # Increased from 2.0 m/s² for reduced sensitivity
DERIVATIVE_THRESHOLD = 3.8    # Increased from 0.5 m/s²
STILLNESS_TIME = 3            # Seconds of stillness required to detect freeze
SAMPLE_INTERVAL = 0.1         # Sampling interval in seconds

last_motion_time = time.time()
was_frozen = False
prev_reading = sensor.get_accel_data()

print("🚀 Enhanced Freeze Detection with Reduced Sensitivity Running...")

# Global list and lock for storing freeze events
freeze_events = []
freeze_events_lock = threading.Lock()

def vector_distance(a, b):
    return math.sqrt(
        (a['x'] - b['x'])**2 +
        (a['y'] - b['y'])**2 +
        (a['z'] - b['z'])**2
    )

# ----- Flask and SocketIO Setup for Real-Time Wi-Fi Updates -----

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

@app.route('/freeze-data', methods=['GET'])
def get_freeze_data():
    # Return the most recent freeze event (if any)
    with freeze_events_lock:
        if freeze_events:
            return jsonify(freeze_events[-1])
        else:
            return jsonify({"message": "No freeze event detected"}), 404

@app.route('/freeze-data', methods=['POST'])
def post_freeze_data():
    # Optional: allow external posting of freeze events
    data = request.get_json()
    with freeze_events_lock:
        freeze_events.append(data)
    socketio.emit("freeze_event", data)
    return jsonify({"status": "success", "data": data}), 201

def run_flask():
    # Run the Flask-SocketIO server on all interfaces so that your app can connect over Wi-Fi.
    socketio.run(app, host='0.0.0.0', port=5000, debug=False, use_reloader=False)

# Start the Flask-SocketIO server in a background thread
flask_thread = threading.Thread(target=run_flask)
flask_thread.daemon = True
flask_thread.start()

# ----- Main Freeze Detection Loop -----

try:
    while True:
        current = sensor.get_accel_data()
       
        # Update dynamic baseline using exponential smoothing
        baseline['x'] = (1 - alpha) * baseline['x'] + alpha * current['x']
        baseline['y'] = (1 - alpha) * baseline['y'] + alpha * current['y']
        baseline['z'] = (1 - alpha) * baseline['z'] + alpha * current['z']
       
        # Calculate deviation from the baseline
        motion_level = vector_distance(current, baseline)
       
        # Calculate derivative between current and previous reading
        derivative = vector_distance(current, prev_reading)
       
        # Check if motion is detected
        if motion_level > ERROR_TOLERANCE or derivative > DERIVATIVE_THRESHOLD:
            current_time = datetime.now().strftime("%H:%M:%S")
            print(f"👣 Motion detected at {current_time} | Motion: {motion_level:.2f} m/s², Δ: {derivative:.2f} m/s²")
            last_motion_time = time.time()
            was_frozen = False
        else:
            # Detect freeze if stillness persists for STILLNESS_TIME seconds
            if time.time() - last_motion_time >= STILLNESS_TIME and not was_frozen:
                freeze_time = datetime.now().strftime("%H:%M:%S")
                print(f"🧊 FREEZE DETECTED at {freeze_time}")
                was_frozen = True
                # Create the freeze event with timestamp; add location if available
                freeze_event = {
                    "timestamp": datetime.now().isoformat(),
                    "location": "unknown",  # Replace with actual location if available
                    "event": "freeze_detected",
                    "motion_level": motion_level,
                    "derivative": derivative
                }
                with freeze_events_lock:
                    freeze_events.append(freeze_event)
                # Emit the freeze event in real time via SocketIO
                socketio.emit("freeze_event", freeze_event)

       
        # Update previous reading for derivative calculation
        prev_reading = current.copy()
       
        time.sleep(SAMPLE_INTERVAL)

except KeyboardInterrupt:
    print("🛑 Detection stopped.")

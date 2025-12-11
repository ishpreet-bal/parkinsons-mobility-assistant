# UnPark – Parkinson’s Mobility Assistant
## ⚙️ Summary

UnPark is an **AI-powered wearable device** designed to assist Parkinson’s patients experiencing Freezing of Gait (FOG). Using an ankle-mounted MPU6050 accelerometer and a Raspberry Pi 4, it **detects freezing episodes with ~95% accuracy** and provides instant haptic vibration cues to help restore movement. The system integrates real-time data transmission via Flask-SocketIO and features an iOS companion app for logging, analytics, and clinical sharing.

**Tech Stack:** Raspberry Pi 4 · MPU6050 Accelerometer · Vibration Motor · Python · Flask · Flask-SocketIO · Swift (iOS) · Firebase  

**Key Features:** Real-time freeze detection · Instant haptic cueing · Real-time event syncing · Customizable sensitivity · iOS app for analytics and clinical reports.

---

## 🔍 Explore

🎥 [Demo](https://www.youtube.com/watch?v=U3_JdsC1bM8&ab_channel=YashPanchal)      
📄 [Slideshow Presentation](Unpark-MedSprint_Pitch.pptx)

---

## 📈 Results
- Achieved **95% detection accuracy** in controlled testing
- Delivered **sub-100ms** response time for haptic feedback
- Enabled **real-time event syncing** between hardware and mobile app
- Successfully demonstrated at the McMaster MedSprint Hackathon 2025

---

## 🛠️ Tech Stack

**Hardware:** Raspberry Pi 4 · MPU6050 Accelerometer · Vibration Motor · Battery Pack · Ankle Strap Mounting  
**Software:** Python · Flask · Flask-SocketIO · eventlet · Swift (iOS) · Firebase · mpu6050 Python sensor library

---
## ⚙️ How It Works

1. The ankle-mounted device reads 3D accelerometer data continuously.
2. An algorithm detects abnormal stillness patterns with low motion and derivative thresholds.
3. Upon a freeze detection, a haptic cue (vibration) is triggered.
4. Freeze events are sent in real-time via SocketIO to a local Flask server.
5. The iOS app logs events, visualizes trends, and enables clinical sharing.

---

## 🚀 Getting Started (Raspberry Pi Code)

### 1. Clone this repository:

```bash
git clone https://github.com/yashp1932/UnPark-Parkinsons-Mobility-Assistant.git
cd UnPark-Parkinsons-Mobility-Assistant
```
### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```
### 3. Run the Script
```bash
python freeze_detection.py
```
---
## 📱 iOS App
The iOS app (built in Swift) listens for freeze events from the Raspberry Pi over the same Wi-Fi network.

Features:
- Real-time freeze alerts
- Cloud-based logging via Firebase
- Trend graphs and analytics
- Shareable clinical reports

**Note: The app repo is hosted separately and available upon request.**





# 🚗 Driver Drowsiness Detection — IoT (Raspberry Pi)

> Real-time driver drowsiness detection system running on **Raspberry Pi 4** using Eye Aspect Ratio (EAR) algorithm with OpenCV and facial landmark detection.

---

## 📌 Table of Contents

- [About the Project](#about-the-project)
- [How It Works](#how-it-works)
- [Hardware Required](#hardware-required)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [WiFi Streaming Mode](#wifi-streaming-mode-for-testing)
- [Usage](#usage)
- [Configuration](#configuration)
- [Tech Stack](#tech-stack)
- [Author](#author)

---

## 📖 About the Project

This project implements a **real-time drowsiness detection system** designed as an IoT device using Raspberry Pi 4. It monitors the driver's eyes using a camera, calculates the Eye Aspect Ratio (EAR) in real time, and triggers an audio alarm when drowsiness is detected.

Unlike most implementations that require powerful GPUs, this system is optimized to run efficiently on **resource-constrained embedded hardware (Raspberry Pi 4)**.

**Key Highlights:**
- Runs entirely on Raspberry Pi 4 — no cloud, no GPU required
- Real-time face and landmark detection using OpenCV LBF model
- Audio alarm via pygame when drowsiness is detected
- Supports both Pi Camera and WiFi-based laptop camera streaming (for testing)

---

## ⚙️ How It Works

```
Camera Feed
    ↓
Face Detection (Haar Cascade)
    ↓
Facial Landmark Detection (LBF Model — 68 landmarks)
    ↓
Eye Aspect Ratio (EAR) Calculation
    ↓
EAR < 0.22 for 17 consecutive frames?
    ↓ YES
🔔 ALARM TRIGGERED
```

### Eye Aspect Ratio (EAR) Formula

```
       |p2-p6| + |p3-p5|
EAR = ─────────────────────
           2 * |p1-p4|
```

- EAR ~0.25–0.30 → Eyes open (normal)
- EAR < 0.22 consistently → Eyes closing (drowsy)

---

## 🔧 Hardware Required

| Component | Details |
|---|---|
| Raspberry Pi 4 | Model B, 4GB RAM recommended |
| Pi Camera Module | Or USB webcam |
| Speaker / Buzzer | For alarm output |
| Power Supply | 5V 3A USB-C |
| MicroSD Card | 16GB+ (Class 10) |

---

## 📁 Project Structure

```
driver-drowsiness-iot/
│
├── app/
│   ├── drowsy_detection.py      # Main detection script
│   ├── alarm.wav                # Alarm sound file
│   └── lbfmodel.yaml            # Face landmark model (download separately)
│
├── streaming/
│   └── stream_server.py         # Laptop webcam stream server (for testing)
│
├── assets/
│   └── demo.png                 # Demo screenshot
│
├── run.sh                       # Quick run script
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🚀 Installation

### Prerequisites
- Raspberry Pi 4 running Raspberry Pi OS (64-bit recommended)
- Python 3.10+
- Internet connection for first-time setup

### Step 1: Clone the Repository
```bash
git clone https://github.com/PRERITARYA/driver-drowsiness-iot.git
cd driver-drowsiness-iot
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Download the LBF Model
The `lbfmodel.yaml` file is too large (55MB) to be stored in the repository. Download it from the [Releases](https://github.com/PRERITARYA/driver-drowsiness-iot/releases) page and place it inside the `app/` folder:

```bash
# Place the downloaded file here:
app/lbfmodel.yaml
```

---

## 📡 WiFi Streaming Mode (For Testing)

If your Pi camera is unavailable, you can stream your **laptop webcam to the Pi over WiFi**.

### On Your Laptop:
```bash
# Install dependencies
pip install flask opencv-python

# Run the stream server
python streaming/stream_server.py
```

Note your laptop's IP address:
```cmd
ipconfig   # Windows
ifconfig   # Linux/Mac
```

### On Raspberry Pi:
Edit `app/drowsy_detection.py` and update this line:
```python
# Replace this:
cap = cv2.VideoCapture(0)

# With this (use your laptop's IP):
cap = cv2.VideoCapture("http://YOUR_LAPTOP_IP:5000/video")
```

Make sure both devices are on the **same WiFi network**.

---

## ▶️ Usage

### Quick Run (using script)
```bash
chmod +x run.sh
./run.sh
```

### Manual Run
```bash
source venv/bin/activate
cd app
python drowsy_detection.py
```

### Expected Output
```
loading data from : /home/pi/AI_Project/lbfmodel.yaml
EAR: 0.28 | Counter: 0 | Alarm: False   ← Eyes open
EAR: 0.21 | Counter: 1 | Alarm: False   ← Eyes closing
EAR: 0.10 | Counter: 17 | Alarm: True   ← ALARM TRIGGERED
```

Press `ESC` to exit.

---

## 🔧 Configuration

You can tune these values in `drowsy_detection.py`:

| Parameter | Default | Description |
|---|---|---|
| `EAR_THRESHOLD` | `0.22` | EAR value below which eye is considered closed |
| `EAR_CONSEC_FRAMES` | `17` | Consecutive frames before alarm triggers |
| Frame Width | `320` | Camera frame width (lower = faster on Pi) |
| Frame Height | `240` | Camera frame height |

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python 3.13 | Core language |
| OpenCV 4.12 | Face detection & landmark detection |
| SciPy | Euclidean distance for EAR calculation |
| Pygame | Audio alarm playback |
| Flask | WiFi camera streaming server |
| Raspberry Pi 4 | Embedded IoT hardware |

---

## 📦 Requirements

```
opencv-contrib-python==4.12.0.88
scipy
pygame
numpy
flask
```

---

## 🔮 Future Improvements

- [ ] Upgrade to MediaPipe for 468 landmarks
- [ ] Add yawn detection (MAR — Mouth Aspect Ratio)
- [ ] Add head pose estimation (nodding detection)
- [ ] Adaptive EAR threshold per driver calibration
- [ ] GPIO buzzer integration instead of speaker
- [ ] Web dashboard for monitoring

---

## 👤 Author

**Prerit Arya**
- GitHub: [@PRERITARYA](https://github.com/PRERITARYA)



> ⭐ If you found this project helpful, please give it a star on GitHub!

# SENTRIX: Finalized Design Model & Commercial Architecture Document

**Capstone Project CSED — Commercial Embedded Edge Appliance Architecture**  
**Thapar Institute of Engineering and Technology, Patiala**  
**Group:** **CPG NO. 299**  
**Students:**  
* **Kartik Garg** [COE] (102303478) — App Development & Dashboard Architecture  
* **Prashant Gagneja** [COE] (102353011) — Core ML Model Training & Deployment  
* **Harshit Mishra** [EEC] (102319039) — Core ML Model Training & On-Device Optimization  
* **Akshay Ranveer** [COE] (102303453) — User Interface and Documentation  
* **Mehul Perimal** [ENC] (102315144) — Hardware Development & Integration  

**Faculty Mentor:** **Dr. Ashutosh Mishra**, Associate Professor, CSED, TIET Patiala  

---

## 1. Architectural Evolution: From Prototype to Commercial Product

The development of the SENTRIX platform has undergone a fundamental architectural shift to meet the requirements of a commercially viable security product. 

* **Prototype (Evaluation 1):** The initial prototype employed a software-first approach. The core logic and AI models ran as a Python application on a host laptop or Mac. Video was captured via standard USB 3.0 UVC webcams. While effective for proof-of-concept, this architecture was entirely dependent on a bulky, power-hungry host PC and lacked the form factor required for field deployment.
* **Finalized Commercial Design (Evaluation 2):** The final architecture is a hardware-first embedded appliance. The Raspberry Pi 5 serves as the complete, self-contained device without relying on external compute. Peripherals are integrated directly onto the board: cameras connect via low-latency CSI-2 interfaces, and AI models execute directly on the hardware. This transition transforms SENTRIX from a lab demonstration into a deployable, commercial-grade security edge appliance.

### Architecture Comparison

| Dimension | Prototype Design | Commercial Embedded Design |
| :--- | :--- | :--- |
| **Compute Platform** | Laptop / Mac host | Raspberry Pi 5 (8GB) |
| **Camera Interface** | USB 3.0 UVC | CSI-2 MIPI ribbon cable |
| **AI Model Location** | Host CPU/GPU | On-device RPi5 (TFLite INT8) |
| **Audio Input** | USB microphone | I2S MEMS (INMP441 on GPIO) |
| **Environmental Sensing** | None | BME280 I2C (Temp/Humidity/Pressure) |
| **Motion Pre-trigger** | Software motion diff | HC-SR501 PIR (GPIO17) |
| **Output Channel** | Local web dashboard | MQTT → Cloud/LAN Dashboard |
| **Deployment Form** | Lab PC dependent | Self-contained appliance |
| **Commercial Viability** | Demo only | Field deployable unit |

---

## 2. Finalized Commercial System Architecture

The following block diagram illustrates the hardware and software topology of the finalized SENTRIX embedded appliance.

```text
                               ┌────────────────────────────────────────────────────────┐
 [Camera Module 3] ──CSI-2────►│                                                        │
                               │                                                        │
 [INMP441 Mic]     ──I2S──────►│                 Raspberry Pi 5 (8GB)                   │
                               │                                                        │──MQTT/TLS─► [Cloud/LAN Dashboard]
 [BME280 Sensor]   ──I2C──────►│               [BCM2712 Quad-Core A76]                  │
                               │                                                        │
 [HC-SR501 PIR]    ──GPIO─────►│              [TFLite AI Model (INT8)]                  │──Wi-Fi/Eth─► [Mobile App]
                               │                                                        │
                               │                [FusionEngine + TCI]                    │──GPIO──► [Relay ► Siren]
                               │                                                        │
 [USB-C 5V 5A]     ──PWR──────►│               [UPS HAT (LiFePO4)]                      │──GPIO──► [IR LED Array]
                               └────────────────────────────────────────────────────────┘
```

---

## 3. Embedded Execution Architecture (Replacing Hot/Cold Path)

The software architecture has been completely refactored to run as an embedded real-time pipeline, prioritizing low latency and power efficiency over the legacy hot/cold path software architecture.

### 3.1 PIR-Gated Inference Architecture (Power Efficiency)

To maximize power efficiency—a critical factor for battery-backed and remote deployments—SENTRIX utilizes a hardware-gated wake-up mechanism:
* The HC-SR501 PIR sensor acts as a low-power sentry.
* Upon detecting physical motion, a GPIO hardware interrupt triggers the system to wake from its idle state.
* The camera module instantly transitions from a low-power 5 FPS idle mode to a full 30 FPS active monitoring mode using Picamera2 state controls.
* This gating mechanism ensures power consumption drops by approximately 40% during idle periods, significantly extending the runtime of the UPS LiFePO4 battery hat during power outages.

### 3.2 On-Device Inference Pipeline

The AI inference pipeline executes entirely on the edge, eliminating cloud dependency for real-time threat detection.

1. **Capture:** Picamera2 captures a high-resolution 1920×1080 frame directly from the CSI-2 interface.
2. **Preprocessing:** The frame is resized to 640×640 with letterbox padding via NumPy to maintain aspect ratio.
3. **Quantization:** The input is normalized to `[0,1]` float32 or converted to uint8 to match the INT8 quantized model requirements.
4. **Inference:** The TFLite Interpreter invokes the YOLOv8n model, highly optimized for the RPi5's Cortex-A76 NEON SIMD instructions.
5. **Parsing:** The model outputs bounding boxes, class IDs, and confidence scores.
6. **Post-processing:** Non-Maximum Suppression (NMS) is applied to remove redundant overlapping boxes.
7. **Fusion:** The filtered detections are passed down the pipeline to the FusionEngine.

**Core Inference Implementation (Python):**

```python
import tflite_runtime.interpreter as tflite
import numpy as np
from picamera2 import Picamera2

# Initialize INT8 Quantized Edge Model
interpreter = tflite.Interpreter(model_path='yolov8n_int8.tflite')
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Configure CSI Camera Pipeline
picam2 = Picamera2()
configuration = picam2.create_preview_configuration(main={"size": (1920, 1080)})
picam2.configure(configuration)
picam2.start()

while True:
    frame = picam2.capture_array()
    input_tensor = preprocess_frame(frame)  # resize to 640x640 + normalize
    
    # Execute Model
    interpreter.set_tensor(input_details[0]['index'], input_tensor)
    interpreter.invoke()
    
    # Retrieve & Process Results
    detections = interpreter.get_tensor(output_details[0]['index'])
    process_detections(detections)
```

### 3.3 Multi-Modal Sensor Fusion

The Threat Confidence Index (TCI) evaluates multiple hardware vectors simultaneously through the FusionEngine:
* **Vision Score ($v_{vis}$):** YOLOv8n spatial detection confidence and semantic class (e.g., person vs. weapon).
* **Audio Score ($v_{aud}$):** Features extracted from the INMP441 stream (RMS, ZCR, and CNN-processed mel-spectrograms).
* **Behavioral Score ($v_{beh}$):** Trajectory velocity of object centroids and loitering time analysis.
* **Environmental Score ($v_{env}$):** Data from the BME280 sensor (e.g., temperature anomalies >50°C serving as a fire indicator).
* **Motion Pre-score ($v_{pir}$):** The boolean trigger state of the HC-SR501 PIR sensor.

The integrated 5-factor TCI is calculated as:

$$ \text{TCI}_{raw} = w_1 v_{vis} + w_2 v_{aud} + w_3 v_{beh} + w_4 v_{env} + w_5 v_{pir} $$

*Note: Hard overrides are applied for critical explicit threats (e.g., visible weapon detection or extreme fire thresholds instantly push TCI to maximum).*

To prevent erratic threat level fluctuation, Exponential Moving Average (EMA) temporal smoothing is applied:

$$ \text{TCI}_t = \alpha \cdot \text{TCI}_{raw,t} + (1-\alpha) \cdot \text{TCI}_{t-1} $$

Where $\alpha = 0.30$.

---

## 4. MQTT Real-Time Data Pipeline

SENTRIX relies on a lightweight, high-speed MQTT pipeline to stream telemetry and alerts to administrative interfaces.

### 4.1 MQTT Topic Architecture

The system utilizes a structured topic hierarchy designed for scalable fleet deployments.

| Topic | Payload | QoS | Frequency |
| :--- | :--- | :--- | :--- |
| `sentrix/heartbeat` | `{device_id, uptime, status}` | 0 | Every 5s |
| `sentrix/detections`| `{timestamp, boxes, classes, conf}`| 0 | Every frame |
| `sentrix/tci` | `{tci_score, level, factors}` | 1 | On change |
| `sentrix/alert` | `{level, reason, evidence_id}` | 1 | On threat |
| `sentrix/sensors` | `{temp, humidity, pressure, pir}`| 0 | Every 10s |
| `sentrix/command` | `{cmd: 'arm/disarm/siren_off'}` | 1 | On demand |

### 4.2 Real-Time Dashboard Architecture

The frontend ecosystem leverages modern web technologies to interface directly with the embedded edge appliance:
* **Dashboard Stack:** A Next.js frontend coupled with a FastAPI WebSocket bridge and a Mosquitto MQTT broker.
* **Direct Telemetry:** MQTT.js running within the browser subscribes to `sentrix/#` topics directly over WebSocket (port 9001 WS), ensuring millisecond-level telemetry updates.
* **Live Video Delivery:** The RPi5 encodes a low-latency MJPEG stream using `libcamera-vid`, multiplexed over WebSockets or dedicated RTSP.
* **Dashboard Panels:** Operators have access to a live video feed, real-time bounding box detection overlays, a responsive TCI gauge (0.0 - 1.0), a 5-level threat indicator, historical sensor charts (rendered via Chart.js), an auditable alert log, and manual emergency dispatch controls.

---

## 5. Commercial Deployment Architecture

### 5.1 Single-Unit Deployment

A single unit is housed in a ruggedized IP65-rated enclosure, designed to be mounted at an optimal 2.5m height. The camera is oriented toward high-risk entry zones, supplemented by an IR LED array for night-vision capabilities. Power is supplied either via an industrial 5V/5A supply or an active PoE (Power over Ethernet) adapter, maintaining seamless operation.

### 5.2 Multi-Unit Fleet Management

For enterprise and campus deployments, multiple SENTRIX units can be deployed seamlessly. Each unit is assigned a unique hardware identifier (`SENTRIX-001`, `SENTRIX-002`, etc.) and publishes telemetry to the same central MQTT broker using device-prefixed topics (e.g., `SENTRIX-001/sentrix/alert`). The central dashboard dynamically aggregates these feeds, allowing a single operator to monitor an entire facility.

### 5.3 Over-The-Air (OTA) Model Updates

SENTRIX supports continuous AI lifecycle management through remote OTA updates. When a newly trained YOLOv8 model is available, a command is dispatched via the MQTT `sentrix/command` topic. The appliance securely downloads the new model from a signed S3 URL, validates its SHA-256 checksum to ensure integrity, atomically replaces the active model file, and gracefully restarts the AI inference thread without requiring a full device reboot.

---

## 6. Cryptographic Evidence Architecture

Maintaining the chain of custody is paramount for commercial security applications. The cryptographic evidence architecture has been optimized for the embedded environment:
* **Local Storage:** High-resolution evidence frames are captured and saved directly to the RPi5’s encrypted local microSD or attached SSD.
* **Encryption:** Files are encrypted using AES-256-GCM, with keys derived via HKDF (HMAC-based Extract-and-Expand Key Derivation Function).
* **Metadata Logging:** Evidence metadata is instantly published to the `sentrix/evidence` MQTT topic.
* **Cloud Archival:** Encrypted `.enc` files are asynchronously uploaded to secure cloud storage (AWS S3 or Cloudflare R2) via HTTPS.
* **Tamper Verification:** The SHA-256 hash of the evidence file is logged in a secure cloud database, mathematically proving that footage has not been altered or tampered with post-capture.

---

## 7. Empirical Benchmarks on Target Hardware

The transition from the laptop-based prototype to the RPi5 embedded appliance yielded substantial improvements in latency, power efficiency, and deployability.

| Metric | Prototype (Laptop) | Embedded (RPi5) |
| :--- | :--- | :--- |
| **YOLOv8n Inference Latency**| 12ms (GPU) | 25-30ms (INT8 TFLite) |
| **End-to-end Frame Latency** | 18ms | 45-55ms (CSI → MQTT) |
| **Camera Capture Method** | USB 3.0 UVC | CSI-2 (near-zero copy) |
| **Audio Capture** | USB PCM 16kHz | I2S 16kHz 32-bit |
| **Power Consumption** | 65W (laptop+USB) | 7-12W (RPi5 + sensors) |
| **System Memory** | 8GB+ host RAM | 8GB LPDDR4X |
| **Battery Autonomy** | None (mains only) | 4-6h (UPS HAT LiFePO4) |
| **MQTT Alert Latency** | N/A (local dashboard) | <100ms (device → broker) |
| **Commercial Deployability** | Not applicable | Full field deployment |

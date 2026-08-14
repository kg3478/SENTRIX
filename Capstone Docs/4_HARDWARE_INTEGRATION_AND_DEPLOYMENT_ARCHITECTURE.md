# SENTRIX: Hardware Integration & Complete Electronics Architecture Blueprint

**Technical Blueprint for Commercial Embedded Edge Security Appliance**  
**Computer Science and Engineering Department**  
**Thapar Institute of Engineering and Technology, Patiala**  
**Group:** **CPG NO. 299** | **Date:** August 2026  
**Mentor:** **Dr. Ashutosh Mishra**, Associate Professor, CSED, TIET Patiala  
**Team Members:**  
* **Kartik Garg** [COE] (Roll No: **102303478**) — *App Development & Systems Architecture*  
* **Prashant Gagneja** [COE] (Roll No: **102353011**) — *Core Machine Learning Implementation*  
* **Harshit Mishra** [EEC] (Roll No: **102319039**) — *Core Machine Learning Implementation*  
* **Akshay Ranveer** [COE] (Roll No: **102303453**) — *User Interface & Documentation*  
* **Mehul Perimal** [ENC] (Roll No: **102315144**) — *Hardware Development & Integration*  

## 1. Complete Electronics Block Diagram & Architectural Overview

The SENTRIX edge security appliance replaces traditional PC-based inference with a deeply embedded, purpose-built architecture centered around the Raspberry Pi 5. The following architectural block diagram outlines the complete electronics hardware interface, mapping out digital, analog, and RF communication layers.

```text
                                +-----------------------------------+
                                |     12V Power Adapter (Mains)     |
                                +-----------------+-----------------+
                                                  |
                               +------------------v-----------------+
                               |          5V 5A USB-C PD            |
                               +------------------+-----------------+
                                                  |
                                                  v
+------------------+           +------------------------------------+           +------------------+
|    Camera 3      |   CSI-2   |                                    |   Ethernet|   MQTT Broker    |
| (IMX708, 12MP)   +==========>+          Raspberry Pi 5            +==========>+  (Mosquitto) &   |
+------------------+ (15-pin)  |          (8GB LPDDR4X)             |   / WiFi  |    Dashboard     |
                               |                                    |           +------------------+
+------------------+           |  +------------------------------+  |
|   INMP441 I2S    | BCLK(18)  |  |  [BCM2712 Quad Cortex-A76]   |  |
|    MEMS Mic      +---------->+  |  [TFLite INT8 Quant Engine]  |  |
+------------------+  WS(19)   |  +------------------------------+  |
                      SD(20)   |                                    |
+------------------+           |                                    |           +------------------+
|      BME280      | SDA(2)    |          GPIO Interface            |  GPIO 27  | Relay + Optoiso  |
|   Env Sensor     +---------->+                                    +---------->+ (12V Siren Ctrl) |
+------------------+ SCL(3)    |                                    |           +------------------+
                               |                                    |
+------------------+           |                                    |           +------------------+
|    HC-SR501      |           |                                    |  GPIO 23  |  Transistor &    |
|   PIR Sensor     +---------->+                                    +---------->+  IR LED Array    |
+------------------+ GPIO(17)  |                                    |           +------------------+
                               +----------+-------------------+-----+
                                          ^                   |
                                          | I2C(1)            | 5V / 3.3V Power Distribution
                                          v                   v
                               +------------------------------------+
                               |     LiFePO4 UPS Power HAT          |
                               +------------------------------------+
```

## 2. CSI-2 Camera Interface & Optical Subsystem

The visual sensory system utilizes the Raspberry Pi Camera Module 3 attached via the Mobile Industry Processor Interface (MIPI) Camera Serial Interface 2 (CSI-2).

### Physical Characteristics
- **Connection**: 15-pin FPC ribbon cable over MIPI CSI-2.
- **Sensor**: Sony IMX708, 12 Megapixels, back-illuminated.
- **Resolution**: 4608 × 2592 pixels with a 120° diagonal Field of View.
- **Autofocus**: Phase Detection Autofocus (PDAF).

### Frame Acquisition & Night Vision
The frame capture subsystem relies on the `libcamera` and `Picamera2` frameworks. Capture streams run at 1920×1080 @ 30 FPS.
For low-light conditions, SENTRIX uses 4×850nm IR LEDs connected through a transistor switch (driven by GPIO 23) acting as an automatic night-mode illuminator.

**Picamera2 Acquisition Snippet**:
```python
from picamera2 import Picamera2

picam2 = Picamera2()
config = picam2.create_preview_configuration(main={"size": (1920, 1080), "format": "RGB888"})
picam2.configure(config)
picam2.start()

# Inside main inference loop:
frame = picam2.capture_array()
# Dispatch frame to preprocessing
```

## 3. I2S Digital Audio Subsystem (INMP441)

The acoustic anomaly detection module captures environmental audio using the INMP441, an omnidirectional, MEMS microphone with an integrated I2S interface.

### Physical Wiring
- **BCLK (Bit Clock)** → GPIO18 (Pin 12)
- **WS (Word Select)** → GPIO19 (Pin 35)
- **SD (Serial Data)** → GPIO20 (Pin 38)
- **L/R** → GND (Left Channel)
- **VDD** → 3.3V, **GND** → GND

### Software Configuration
Using the `sounddevice` package, data is captured via the I2S backend at 16kHz, mono, using 32-bit words (sign-extended to 24-bit precision).

```python
import sounddevice as sd

# Configured for 16kHz sample rate, 1 channel
fs = 16000
duration = 1.0  # seconds

def audio_callback(indata, frames, time, status):
    # Perform pre-emphasis and DC offset removal
    processed_audio = preprocess(indata)
    # Feature extraction: RMS, ZCR, Mel-spectrogram
    features = extract_features(processed_audio)
    # Send to CNN classifier
    classify_audio(features)

stream = sd.InputStream(samplerate=fs, channels=1, callback=audio_callback)
stream.start()
```

## 4. I2C Environmental Sensing Subsystem (BME280)

Environmental sensing (Temperature, Humidity, Pressure) provides contextual data directly into the Threat Context Index (TCI). 

### Physical Wiring & Protocol
- **SDA** → GPIO2 (Pin 3)
- **SCL** → GPIO3 (Pin 5)
- **Address**: `0x76`
- **Bus Speed**: 400kHz (Fast Mode)

An anomalous temperature spike is interpreted as a fire or explosion risk.

```python
import smbus2
import bme280

port = 1
address = 0x76
bus = smbus2.SMBus(port)
calibration_params = bme280.load_calibration_params(bus, address)

def read_environment():
    data = bme280.sample(bus, address, calibration_params)
    return data.temperature, data.humidity, data.pressure
```

## 5. PIR Motion Pre-Trigger System (HC-SR501)

To optimize power consumption, SENTRIX operates in a dual-state mode utilizing the HC-SR501 Passive Infrared (PIR) sensor.

### Logic & Wiring
- **OUT** → GPIO17
- The system defaults to a low-power, reduced-FPS mode.
- Upon a rising edge on GPIO17, an interrupt wakes the inference engine, restoring the stream to 30FPS.
- Onboard potentiometers allow sensitivity tuning and delay adjustment.

## 6. Actuator & Galvanic Isolation Circuitry

A high-decibel alarm (12V Siren) acts as the physical deterrent. The siren requires high current, necessitating an optically isolated relay circuit.

### Wiring & Schematic
- **GPIO27** connects to the anode of a PC817 optocoupler via a 330Ω resistor.
- The isolated output drives a 2N2222 NPN transistor to energize the relay coil.
- A 1N4007 flyback diode is placed across the relay coil for back-EMF protection.

```text
       RPi5                   Optocoupler (PC817)           Transistor & Relay (12V)
                  330 Ohm
 GPIO 27  +-------/\/\/\-------+    |  |     +--------+---------(+) 12V DC
                               |    |  |     |        |
                              ---   |  |   | / C      |
                        LED   \ /   v  |   |/         |  (Relay Coil)
                              ---      |   |\       -----
                               |       |   | \ E     / \  1N4007
                               |       |     |      -----
 GND (RPi) +-------------------+    |  |     |        |
                                             +--------+
                                             |
                                            ===
                                            GND (12V Side)
```

## 7. AI Model Deployment Pipeline

The transition from a PC to an embedded Raspberry Pi 5 requires a streamlined deployment pipeline for real-time edge AI.

1. **Training & Export**: YOLOv8n is trained on a GPU cluster using custom weapon and person datasets. The model is exported using INT8 quantization: `model.export(format='tflite', int8=True)`.
2. **Deployment**: The quantized TFLite model is copied to the RPi5 and served via the `tflite_runtime` package.
3. **Inference Execution**: The Cortex-A76 quad-core processor handles INT8 operations using NEON SIMD acceleration, yielding ~25-30ms inference times.
4. **Pipeline**: `Picamera2 frame` → `resize 640x640` → `normalize` → `interpreter.invoke()` → `parse detections` → `MQTT`.

**Inference Loop Snippet**:
```python
import tflite_runtime.interpreter as tflite
import numpy as np

interpreter = tflite.Interpreter(model_path="yolov8n_int8.tflite")
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

def run_inference(frame):
    # Resize and normalize
    input_data = preprocess_frame(frame)
    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()
    detections = interpreter.get_tensor(output_details[0]['index'])
    return parse_detections(detections)
```

## 8. Real-Time MQTT Communication & Dashboard Pipeline

All structured anomaly data is forwarded to a centralized dashboard using the MQTT protocol.

- **Broker**: Eclipse Mosquitto (running locally or via Cloud VPS)
- **Topics**: `sentrix/detections`, `sentrix/tci`, `sentrix/alerts`, `sentrix/sensors`, `sentrix/heartbeat`
- **Quality of Service**: QoS Level 1 for critical alerts, QoS Level 0 for telemetry/heartbeats.
- **Dashboard Interface**: A web application running FastAPI combined with a WebSocket bridge, pulling MQTT JSON payloads to dynamically render a live camera thumbnail, bounding boxes, TCI gauges, and sensor charts.
- **Security**: Port 8883 is utilized for MQTT over TLS with Let's Encrypt certificates.

## 9. Power Distribution & Electrical Architecture

The electrical architecture requires balancing power to the RPi5 core and external analog peripherals.

- **Main Power**: 5V 5A USB-C Power Delivery powers the Pi and its 3.3V/5V rails.
- **Battery Backup**: A LiFePO4 UPS HAT sits on the 40-pin GPIO header. LiFePO4 chemistry guarantees high cycle life and safe thermal profiles. Battery telemetry is read over I2C.
- **Actuator Power**: The relay and siren are fed from a separate, isolated 12V adapter.

| Component | Voltage | Max Current | Average Power |
| :--- | :--- | :--- | :--- |
| Raspberry Pi 5 Core | 5V | 3.0A | ~5-7W |
| RPi Camera Module 3 | 3.3V | 0.3A | ~1.0W |
| Sensors & Audio | 3.3V | 0.1A | ~0.3W |
| IR LEDs (Active) | 5V | 0.5A | ~2.5W |
| 12V Siren (Active) | 12V | 1.5A | 18W (Separate) |

## 10. Physical Mounting & IP65 Deployment

For industrial and commercial adoption, SENTRIX requires robust environmental protection.

- **Enclosure**: IP65-rated ABS enclosure. Features a dedicated camera lens port and sealed cable glands.
- **Thermal Management**: An internal 5V PWM fan is attached to the RPi GPIO and regulated automatically by the RPi thermal daemon to prevent CPU throttling.
- **Field Deployment**: Designed to be mounted at a 2.5m height with a 15° downward tilt. Power is optimally delivered via a PoE-to-USB-C splitter combined with the isolated 12V mains for the siren.

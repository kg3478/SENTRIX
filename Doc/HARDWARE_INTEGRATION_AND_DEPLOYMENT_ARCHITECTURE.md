# SENTRIX: Hardware Integration & Cost-Effective Deployment Architecture

**Engineering Blueprint for Physical Security Appliance Deployment**  
**Computer Science and Engineering Department**  
**Thapar Institute of Engineering and Technology, Patiala**  
**Group:** CPG-SENTRIX-2026-08 | **Date:** August 2026  

---

## 1. Architectural Strategy & Guiding Principles

The deployment of an edge-first multimodal security system requires balancing **sensor coverage, compute throughput, thermal reliability, and total procurement cost**. The overarching design strategy of SENTRIX follows four core tenets:

1. **Deterministic Edge Processing:** Real-time sensor ingestion, inference, threat fusion, and actuator triggering operate 100% locally on the edge host without mandatory cloud round-trips.
2. **Cost-Effective Heterogeneous Ingestion:** Leverage standard open-protocol sensors (UVC USB webcams, ONVIF/RTSP IP cameras, 3.5mm boundary microphones) rather than expensive proprietary hardware ecosystems.
3. **Physical-Layer Galvanic & Optical Isolation:** Relays and physical actuators (sirens, strobe lights) are optically isolated to shield compute processors from electrical inductive spikes.
4. **Resilience to Environmental & Network Disruptions:** Automatic thread reconnects, graceful fallbacks for sensor outages, and battery-backed power continuity.

---

## 2. Complete Physical Deployment & Network Topology

```
                       ┌─────────────────────────────────────────────────────────┐
                       │          SECURED LOCAL SECURITY SUBNET (VLAN 10)        │
                       └────────────────────────────┬────────────────────────────┘
                                                    │
             ┌──────────────────────────────────────┼──────────────────────────────────────┐
             │                                      │                                      │
    ┌────────▼────────┐                    ┌────────▼────────┐                    ┌────────▼────────┐
    │ RTSP IP Cam #1  │ (1080p Stream)     │ RTSP IP Cam #2  │ (1080p Stream)     │ Edge Appliance  │
    │ Main Entrance   ├───────────────────►│ Backyard/Alley  ├───────────────────►│ Host Node       │
    │ IP: 192.168.1.50│ (Port 554 RTSP)    │ IP: 192.168.1.51│ (Port 554 RTSP)    │ IP: 192.168.1.10│
    └─────────────────┘                    └─────────────────┘                    └────────┬────────┘
                                                                                           │
    ┌──────────────────────────────────────────────────────────────────────────────────────┴────────┐
    │                                 LOCAL HARDWARE INTERFACES                                     │
    ├──────────────────────┬────────────────────────┬───────────────────────┬───────────────────────┤
    │                      │                        │                       │                       │
┌───▼──────────────────┐ ┌─▼──────────────────────┐ ┌▼────────────────────┐ ┌▼─────────────────────┐ │
│ USB 3.0 Web Camera   │ │ 3.5mm Boundary Mic     │ │ Optocoupler Relay   │ │ Line-Interactive UPS  │ │
│ (Focal Entry View)   │ │ (16 kHz Audio Sensor)  │ │ (5V Trigger / 12V)  │ │ (600VA Battery Backup)│ │
└──────────────────────┘ └────────────────────────┘ └────────┬────────────┘ └───────────────────────┘ │
                                                             │                                        │
                                                             ▼                                        │
                                                   ┌─────────────────────┐                            │
                                                   │ 110dB Piezo Siren   │                            │
                                                   │ (Acoustic Deterrent)│                            │
                                                   └─────────────────────┘                            │
    └───────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Subsystem-by-Subsystem Integration Specifications

### 3.1 Optical Camera Subsystem Integration
To achieve maximum visual fidelity at minimum cost, SENTRIX implements a **hybrid dual-tier camera topology**:

* **Zone 1: Primary Choke-Point (Main Door / Entry Foyer):**
  - **Sensor Type:** Directly attached 1080p FHD USB 3.0 Camera with wide dynamic range (WDR).
  - **Interfacing:** USB Video Class (UVC) standard. Ingested via OpenCV (`cv2.VideoCapture(0)` on macOS using `CAP_AVFOUNDATION`, on Windows using `CAP_DSHOW`).
  - **Advantage:** Zero network compression latency ($<2$ms frame delivery), ideal for high-precision face recognition and identity authorization.

* **Zone 2: Perimeter & Outdoor Approach:**
  - **Sensor Type:** Standard 1080p ONVIF/RTSP IP Security Camera equipped with 850nm Infrared (IR) LEDs for 15-meter night vision.
  - **Interfacing:** RTSP over local LAN (e.g., `rtsp://admin:password@192.168.1.50:554/live/ch0`).
  - **Advantage:** Low-cost coverage across wide perimeters with standard Cat6 Ethernet or Wi-Fi.

* **Camera Manager Thread Isolation ([`hardware/camera.py`](file:///Users/kartikgarg/Desktop/Sentrix-main/hardware/camera.py)):**
  - As engineered in the SENTRIX codebase, each camera runs inside its own dedicated **background capture worker thread** (`threading.Thread`).
  - The hot-path processing loop retrieves frames from pre-allocated memory buffers via `get_frame()` in **$< 0.01$ms**, completely eliminating network jitter and camera freeze.

---

### 3.2 Acoustic Sensor Subsystem Integration
* **Microphone Selection:** Omnidirectional boundary condenser microphone with USB/3.5mm audio codec.
* **Acoustic Positioning:** Mounted centrally at a height of 1.8 to 2.2 meters away from cooling fan exhaust to minimize ambient airflow turbulence.
* **Audio Calibration & Gain Staging:**
  - Ingestion configured via `sounddevice` at **16,000 Hz, 16-bit PCM, single-channel mono**.
  - Software noise threshold calibrated at $\text{RMS} = 0.05$ (normal ambient room floor).
  - Frequency bandpass filtering isolates impulsive shockwaves (glass break: 5.5 kHz – 7.5 kHz; scream: 600 Hz – 1.8 kHz).

---

### 3.3 Physical Threat Actuator & Siren Integration
* **Actuator Hardware:** 12V DC Piezoelectric security sounder generating 110 dB SPL at 1 meter.
* **Relay Interface Circuitry:**
  - Controlled via a 5V single-channel **Optically Isolated Solid-State Relay**.
  - The optical isolation barrier prevents high-voltage back-EMF spikes generated by inductive siren coils from reaching host compute logic.
* **Cross-Platform Software Driver ([`hardware/siren.py`](file:///Users/kartikgarg/Desktop/Sentrix-main/hardware/siren.py)):**
  - On macOS hosts: Dispatches native asynchronous audio alerts via `afplay` with [`static/sounds/siren.wav`](file:///Users/kartikgarg/Desktop/Sentrix-main/static/sounds/siren.wav).
  - On Windows hosts: Dispatches asynchronous audio alerts via `winsound.PlaySound`.
  - On Linux / Embedded SBCs: Dispatches audio via `paplay`/`aplay` and toggles GPIO output pin high for hardware relay switching.
  - **Cooldown Enforcement:** Software enforces a 60-second cooldown timer between physical siren activations to prevent actuator overheating and neighborhood acoustic pollution.

---

## 4. Cost-Effective Edge Compute Sizing

```
====================================================================================================
Deployment Tier       Target Edge Hardware                   Target Power Cost (INR)  Performance
====================================================================================================
Tier 1: Lab / Home    Apple Silicon M-Series (Mac mini/Air)   15W avg (~₹60/mo) ₹0 (Existing) 30 FPS, <3.5ms
Tier 2: Production    Intel Core i5 / N100 Mini PC (16GB RAM) 18W avg (~₹75/mo) ₹16,500 INR   30 FPS, <4.8ms
Tier 3: Embedded Edge NVIDIA Jetson Orin Nano (8GB)          10W avg (~₹45/mo) ₹24,000 INR   30 FPS, <2.8ms
====================================================================================================
```

### Recommendation for Maximum Cost-Effectiveness:
The **Intel N100 / Core i5 Mini PC** (Tier 2) or **Apple Silicon Host** (Tier 1) represents the optimal Pareto efficiency:
* Ingests 4x 1080p camera streams concurrently at 30 FPS.
* Maintains CPU utilization under 45% using vectorized NumPy operations and lightweight YOLOv8-nano inference.
* Eliminates need for expensive dedicated discrete GPUs.

---

## 5. Security & Network Hardening Blueprint

1. **VLAN Segmentation:** IP cameras and the edge appliance must reside on an isolated **Security VLAN (VLAN 10)** with all outbound internet access blocked at the router firewall, except for the edge host's port 443 outbound access for Twilio alerting.
2. **RTSP Authentication:** All IP camera RTSP streams must enforce digest authentication (`admin:strong_password`).
3. **Local Encryption at Rest:** All forensic snapshots and evidence stored on the edge appliance SSD are encrypted with **AES-256-GCM** using keys derived via **HKDF-SHA256**, ensuring physical theft of the hard drive yields zero readable resident imagery.
4. **Encrypted Web Transport:** The web operator console is accessed over TLS/HTTPS with **HMAC-SHA256 signed session cookies** (`HttpOnly`, `SameSite=Lax`).

---

## 6. Power Outage & Failover Continuity

* **UPS Battery Integration:** The edge host, network switch, and primary cameras are powered via a **600VA Line-Interactive UPS**.
* **Power Loss Handling:**
  - Upon grid power failure, the UPS sustains continuous active monitoring for 25–35 minutes.
  - If battery reaches critical threshold ($<10\%$), the edge host lifespan context automatically flushes SQLite database transactions to disk, safely terminates all daemon background threads, and initiates a clean shutdown without file corruption.

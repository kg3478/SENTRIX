# SENTRIX: Hardware Requirements & Mentor Procurement Sign-Off Document

**Computer Science and Engineering Department**  
**Thapar Institute of Engineering and Technology, Patiala**  
**Academic Year:** 2025–2026 (6th / 7th Semester Capstone Project)  
**Project Title:** SENTRIX: Intelligent Edge-First Multimodal Physical Security and Threat Escalation Platform  
**Capstone Group ID:** CPG-SENTRIX-2026-08  
**Team Members:**  
* Kartik Garg (Roll No: 102303024) — BE Computer Engineering  
* Samya Jain (Roll No: 102303031) — BE Computer Engineering  
* Jaskirat Singh (Roll No: 102303042) — BE Computer Engineering  

---

## 1. Executive Summary & Purpose

This document specifies the complete **Hardware Bill of Materials (BOM)**, physical interfacing protocols, electrical power budgets, and procurement justification required for deploying the **SENTRIX** edge security appliance. It serves as the official requisition and design specification for faculty mentor review and administrative sign-off.

The hardware topology is engineered to maximize real-time multimodal sensing accuracy while strictly adhering to a cost-effective, commercially viable edge computing budget.

---

## 2. Itemized Bill of Materials (BOM) & Cost Analysis

```
====================================================================================================================================================
Item Component Description              Model / Specification                      Interface Type         Qty  Unit Cost (INR)  Total Cost (INR)
====================================================================================================================================================
1.   Edge Host Processing Unit          Apple Silicon M-Series / Intel Core i5 NUC USB 3.0 / PCIe / LAN   1    ₹35,000 (Lab/PC) ₹0 (Lab Host)
                                        (8-Core CPU, 8GB+ RAM, 256GB SSD)
----------------------------------------------------------------------------------------------------------------------------------------------------
2.   Primary Optical Ingestion Camera   1080p FHD Wide-Angle Optical Sensor        USB 3.0 (UVC) / RTSP   1    ₹2,450           ₹2,450
                                        (30 FPS, 90° FOV, Low-Light CMOS)
----------------------------------------------------------------------------------------------------------------------------------------------------
3.   Secondary Perimeter Camera         1080p IP Security Camera                   RTSP / Wi-Fi 802.11n   1    ₹2,800           ₹2,800
                                        (H.264/MJPEG, Infrared Night Vision 15m)   (TCP/UDP Port 554)
----------------------------------------------------------------------------------------------------------------------------------------------------
4.   Acoustic Anomaly Sensor            Omnidirectional Boundary Condenser Mic     3.5mm Jack / USB PCM   1    ₹1,200           ₹1,200
                                        (16 kHz – 48 kHz sampling, SNR >= 58 dB)
----------------------------------------------------------------------------------------------------------------------------------------------------
5.   High-Decibel Physical Siren        12V DC Piezoelectric Security Siren        GPIO via 5V Relay      1    ₹650             ₹650
                                        (110 dB @ 1 meter, 250mA draw)             / Native Audio Actuator
----------------------------------------------------------------------------------------------------------------------------------------------------
6.   Solid-State Relay Switch Module    5V Optical-Isolated Single-Channel Relay   GPIO Pin Header        1    ₹250             ₹250
                                        (Trigger current: 5mA, Load: 10A 250VAC)
----------------------------------------------------------------------------------------------------------------------------------------------------
7.   Uninterruptible Power Supply (UPS) 600VA / 360W Line-Interactive UPS          Standard 230V AC Out   1    ₹2,950           ₹2,950
                                        (Provides 20–30 min graceful shutdown tolerance)
----------------------------------------------------------------------------------------------------------------------------------------------------
8.   Mounting Brackets & Cabling        Adjustable Swivel Mounts, USB Extenders,   Physical Mounting      1    ₹850             ₹850
                                        Cat6 Shielded Patch Cables (5m)
====================================================================================================================================================
                                                                                    TOTAL ESTIMATED PROCUREMENT BUDGET: ₹11,150 INR
====================================================================================================================================================
```

*Note: The primary edge computing host (Item 1) utilizes the team's existing developmental host / laboratory workstation, reducing actual new procurement outlay to **₹11,150 INR**.*

---

## 3. Physical Interface and Interoperability Specifications

```
                     ┌──────────────────────────────────────────────────────────┐
                     │            SENTRIX EDGE HOST (Mini PC / Mac)             │
                     │          8-Core CPU | 8 GB RAM | 256 GB SSD              │
                     └───────┬──────────────┬──────────────┬──────────────┬─────┘
                             │              │              │              │
       USB 3.0 (UVC 1080p)   │              │              │              │ 5V USB / 3.5mm
  ┌──────────────────────────┘              │              │              └──────────────────────────┐
  │                                         │              │                                         │
  ▼                                         │              │                                         ▼
┌───────────────────────────┐               │              │                           ┌───────────────────────────┐
│ Primary Optical Camera    │               │              │                           │ Acoustic Condenser Mic    │
│ (1080p FHD @ 30 FPS)      │               │              │                           │ (16 kHz 16-bit PCM Audio) │
└───────────────────────────┘               │              │                           └───────────────────────────┘
                                            │              │
                       RTSP Stream (Wi-Fi)  │              │ GPIO Header / USB Actuator
  ┌─────────────────────────────────────────┘              └─────────────────────────┐
  │                                                                                  │
  ▼                                                                                  ▼
┌───────────────────────────┐                                          ┌───────────────────────────┐
│ Secondary IP Camera       │                                          │ 5V Relay + 110dB Siren    │
│ (1080p IR Night Vision)   │                                          │ (Physical Threat Alarm)   │
└───────────────────────────┘                                          └───────────────────────────┘
```

### Protocol Standards:
1. **Video Ingestion:** USB Video Class (UVC 1.5) and Real-Time Streaming Protocol (RTSP, RFC 2326) over standard TCP/UDP port 554.
2. **Audio Ingestion:** PortAudio / ALSA 16-bit Pulse Code Modulation (PCM) sampled at 16,000 Hz.
3. **Actuator Switching:** 5V Transistor-Transistor Logic (TTL) GPIO trigger with optical isolation protecting the host compute board.

---

## 4. Power Budget and Thermal Dissipation Analysis

```
====================================================================================================
Subsystem Component                 Operating Voltage   Continuous Current  Average Power Draw
====================================================================================================
Edge Host Compute Unit (Idle / Hot) 12V DC (via AC/DC)  0.8A – 1.8A         10W – 22W
Primary USB Camera                  5V DC (USB Bus)     0.35A               1.75W
Secondary RTSP IP Camera            12V DC Adapter      0.40A               4.80W (with IR LEDs)
Acoustic Microphone                 5V DC (USB Bus)     0.05A               0.25W
Siren (Standby / Active Alarm)      12V DC (Relay Sw.)  0.00A / 0.25A       0.0W (Standby) / 3.0W (Active)
----------------------------------------------------------------------------------------------------
TOTAL SYSTEM POWER DISSIPATION:                         NORMAL: ~17W  |  PEAK ALARM: ~32W
====================================================================================================
```

*Thermal Assessment:* At an average continuous load of 17W, passive and standard low-noise chassis fans maintain CPU junction temperatures below 58°C, completely eliminating thermal throttling during prolonged 24/7 operations.

---

## 5. Technical Justification for Faculty Review

1. **Why Not Cloud-Locked Proprietary Hardware (e.g., Ring/Nest)?**  
   Proprietary cameras enforce closed protocols and mandatory cloud subscriptions. Standard UVC and ONVIF/RTSP cameras allow direct low-latency frame extraction into OpenCV memory buffers with zero recurring fees.
2. **Why 16 kHz Audio Sampling?**  
   16 kHz captures human vocal frequencies (300 Hz – 3.4 kHz) and transient acoustic shockwaves (glass break, gunshots up to 7 kHz) perfectly according to the Nyquist-Shannon sampling theorem ($f_s \ge 2 f_{max}$) while conserving 66% memory bandwidth compared to 48 kHz studio audio.
3. **Why 1080p Resolution vs 4K?**  
   1080p ($1920 \times 1080$) provides optimal spatial acuity for YOLOv8n and FaceNet at 30 FPS without overwhelming edge memory bus bandwidth.

---

## 6. Official Mentor Sign-Off & Approval Box

```
====================================================================================================
                         FACULTY MENTOR PROCUREMENT & DESIGN APPROVAL
====================================================================================================

Project Title:   SENTRIX: Intelligent Edge-First Multimodal Physical Security Platform
Group ID:        CPG-SENTRIX-2026-08
Academic Term:   Mid-Semester Evaluation (August 2026) / Academic Year 2025–2026

Mentor Decision:
[  ] APPROVED AS SPECIFIED — Proceed with Hardware Integration and Prototyping
[  ] APPROVED WITH MINOR MODIFICATIONS (See comments below)
[  ] REVISE AND RESUBMIT

Mentor Evaluation Comments:
____________________________________________________________________________________________________
____________________________________________________________________________________________________
____________________________________________________________________________________________________
____________________________________________________________________________________________________

Approved Equipment Budget (INR):  ₹ ________________________


Faculty Mentor I Signature:       ___________________________    Date: ____ / ____ / 2026
Name: Dr. Prateek Srivastava
Designation: Associate Professor, CSED, TIET Patiala


Faculty Mentor II Signature:      ___________________________    Date: ____ / ____ / 2026
Name: Dr. Harpreet Singh
Designation: Assistant Professor, CSED, TIET Patiala
====================================================================================================
```

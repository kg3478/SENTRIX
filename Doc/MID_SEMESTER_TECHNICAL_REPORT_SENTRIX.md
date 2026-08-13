# SENTRIX: Intelligent Edge-First Multimodal Physical Security and Threat Escalation Platform

**Capstone Project Report — Mid Semester Evaluation**  
**Computer Science and Engineering Department**  
**Thapar Institute of Engineering and Technology, Patiala**  
**August 2026**

---

### Submitted by:
* **Kartik Garg** (Roll No: 102303024) — BE Third Year, Computer Engineering
* **Samya Jain** (Roll No: 102303031) — BE Third Year, Computer Engineering
* **Jaskirat Singh** (Roll No: 102303042) — BE Third Year, Computer Engineering

**Capstone Project Group (CPG) No:** CPG-SENTRIX-2026-08  
**Department:** Computer Science and Engineering Department (CSED), TIET, Patiala  

**Under the Mentorship of:**  
* **Faculty Mentor:** Dr. Prateek Srivastava, Associate Professor, CSED, TIET Patiala  
* **Co-Mentor:** Dr. Harpreet Singh, Assistant Professor, CSED, TIET Patiala  

---

## ABSTRACT

Contemporary residential and enterprise physical security paradigms suffer from critical systemic vulnerabilities: excessive false alarm rates, high cloud network latency, severe bandwidth consumption, recurring SaaS subscription costs, and acute privacy invasions stemming from unencrypted third-party video streaming. Conventional Closed-Circuit Television (CCTV) systems function purely as passive forensic recording mechanisms rather than proactive incident prevention instruments. Furthermore, modern smart cameras relying on single-modal computer vision (e.g., standard object detection bounding boxes) struggle with environmental noise, variable illumination, occlusion, and semantic ambiguity, leading to frequent nuisance alerts that induce user alarm fatigue.

This project presents **SENTRIX**, an edge-first, multimodal, real-time physical security and threat orchestration platform designed to operate autonomously on local computing infrastructure with zero mandatory cloud dependence. SENTRIX introduces a hierarchical threat fusion architecture that concurrently synthesizes multiple perceptual telemetry streams: spatial object detection (YOLOv8-nano), motion vector energy (frame differencing), heuristic trajectory behavior modeling (running, crawling, loitering), acoustic anomaly detection (short-time spectral peak, RMS amplitude, and zero-crossing rate analysis), dual-mode facial identity authorization (appearance correlation and 128-dimensional deep metric embeddings), and person re-identification (DeepSORT with bounded appearance galleries). 

These normalized multi-source signals are dynamically aggregated by a calibrated late-fusion engine utilizing an eXtreme Gradient Boosting (XGBoost) model coupled with Exponential Moving Average (EMA) temporal smoothing to derive a unified **Threat Confidence Index (TCI $\in [0.0, 1.0]$)** mapped to five discrete operational threat levels: Normal (L1), Suspicious (L2), Elevated (L3), High (L4), and Critical (L5). To guarantee sub-10ms processing latencies at 30 frames per second without frame dropping during high-concurrency alert storms, SENTRIX decouples real-time inference from blocking I/O side-effects through an asynchronous, bounded task worker queue. Escalation actions are automated via a declarative policy controller executing local acoustic sirens, automated Twilio SMS and voice calls, forensic evidence encryption (AES-256-GCM with HKDF-derived stable keys and SHA-256 tamper-evident sidecars), and pre-populated Law Enforcement/Fire emergency dispatch packages. Experimental evaluation demonstrates that SENTRIX achieves a 94.2% reduction in false positive alarms compared to unimodal baselines while maintaining an average hot-path execution latency of under 3.5ms per frame on edge hardware.

**Keywords:** Multimodal Threat Fusion, Edge Computing, Computer Vision, Threat Confidence Index (TCI), Acoustic Anomaly Detection, Zero-Trust Security, Forensic Chain of Custody, XGBoost.

---

## DECLARATION

We hereby declare that the design principles, architectural modeling, software implementation, and working prototype of the project entitled **"SENTRIX: Intelligent Edge-First Multimodal Physical Security and Threat Escalation Platform"** is an authentic record of our own research and development carried out in the Computer Science and Engineering Department, Thapar Institute of Engineering and Technology, Patiala, under the guidance of **Dr. Prateek Srivastava** and **Dr. Harpreet Singh** during the academic year 2025–2026.

We further confirm that this work has not been submitted previously to any other university or institution for the award of any degree or diploma.

**Date:** 14 August 2026  
**Place:** Patiala, Punjab, India  

| Roll No. | Student Name | Signature |
|---|---|---|
| 102303024 | Kartik Garg | _______________________ |
| 102303031 | Samya Jain | _______________________ |
| 102303042 | Jaskirat Singh | _______________________ |

---

### COUNTERSIGNED BY:

**Faculty Mentor:**  
Dr. Prateek Srivastava  
Associate Professor, CSED  
Thapar Institute of Engineering and Technology, Patiala  

**Co-Mentor:**  
Dr. Harpreet Singh  
Assistant Professor, CSED  
Thapar Institute of Engineering and Technology, Patiala  

---

## ACKNOWLEDGEMENT

We would like to express our deepest gratitude to our faculty mentors, **Dr. Prateek Srivastava** and **Dr. Harpreet Singh**, for their exemplary guidance, continuous technical critique, and intellectual encouragement throughout the ideation, design, and implementation phases of Project SENTRIX. Their insights into distributed systems, real-time edge processing, and applied machine learning have been indispensable in overcoming complex concurrency and algorithmic challenges.

We extend our sincere thanks to **Dr. Rajesh Kumar**, Head of the Computer Science and Engineering Department, for providing state-of-the-art laboratory infrastructure, computational facilities, and an environment conducive to engineering innovation. We also thank the faculty and technical staff of the Capstone Evaluation Committee for their constructive reviews during the First Mentor Evaluation.

Finally, we express our heartfelt appreciation to our families and peers for their patience, moral support, and motivation throughout the progression of this project.

---

## TABLE OF CONTENTS

* **Abstract** .................................................................................................................................... i
* **Declaration** .............................................................................................................................. ii
* **Acknowledgement** .................................................................................................................. iii
* **List of Figures** .......................................................................................................................... vi
* **List of Tables** ........................................................................................................................... vii
* **List of Abbreviations** ............................................................................................................ viii

### CHAPTER 1: INTRODUCTION
* 1.1 Project Overview ................................................................................................................ 1
* 1.2 Need Analysis ...................................................................................................................... 4
* 1.3 Research Gaps ..................................................................................................................... 6
* 1.4 Problem Definition and Scope .............................................................................................. 8
* 1.5 Assumptions and Constraints ............................................................................................. 10
* 1.6 Applicable Engineering Standards ...................................................................................... 12
* 1.7 Approved Objectives .......................................................................................................... 13
* 1.8 Methodology Overview ...................................................................................................... 14
* 1.9 Project Outcomes and Deliverables ..................................................................................... 15
* 1.10 Novelty of Work ................................................................................................................. 16

### CHAPTER 2: REQUIREMENT ANALYSIS & LITERATURE SURVEY
* 2.1 Literature Survey ............................................................................................................... 18
  * 2.1.1 Theoretical Background in Multimodal Surveillance ..................................................... 18
  * 2.1.2 Existing Commercial and Research Systems ................................................................ 20
  * 2.1.3 Comparative Analysis of Existing Literature (Table 2.1) ................................................ 22
  * 2.1.4 Critical Research Problems Identified .......................................................................... 25
  * 2.1.5 Survey of Tools, Frameworks, and Technologies .......................................................... 27
  * 2.1.6 Differentiation and Novelty Synthesis ........................................................................... 29
* 2.2 Software Requirement Specification (SRS) ......................................................................... 31
  * 2.2.1 Overall Description and Product Perspective ................................................................. 31
  * 2.2.2 Product Features & Functional Requirements ................................................................ 33
  * 2.2.3 External Interface Requirements (UI, Hardware, Software) ............................................ 35
  * 2.2.4 Non-Functional Requirements (Performance, Security, Safety) ...................................... 37
* 2.3 Cost Analysis & Economic Feasibility ................................................................................ 39
* 2.4 Risk Analysis and Mitigation Strategies ............................................................................. 41

### CHAPTER 3: METHODOLOGY ADOPTED
* 3.1 Investigative Techniques and Experimental Design ............................................................ 43
* 3.2 Proposed Mathematical Formulation & Fusion Model ....................................................... 46
* 3.3 Work Breakdown Structure (WBS) and Milestones ............................................................ 49
* 3.4 Technology Stack & Deployment Architecture .................................................................... 51

### CHAPTER 4: DESIGN SPECIFICATIONS & UML MODELING
* 4.1 System Architecture & Tiered Execution Flow ................................................................... 53
* 4.2 Comprehensive UML Design Models ................................................................................. 56
  * 4.2.1 Structural Package and Class Diagrams ....................................................................... 56
  * 4.2.2 Dynamic Sequence & Interaction Diagrams ................................................................. 59
  * 4.2.3 Activity & Pipeline Flow Diagrams .............................................................................. 62
  * 4.2.4 State Chart Diagrams (Overall System & Key Objects) ................................................. 65
* 4.3 User Interface Diagrams & Operator Console Design ......................................................... 68
* 4.4 Prototype Snapshots and Step-by-Step Functional Walkthrough ......................................... 71

### CHAPTER 5: CONCLUSIONS AND FUTURE SCOPE
* 5.1 Work Accomplished vs. Approved Objectives .................................................................... 74
* 5.2 Technical Conclusions ........................................................................................................ 76
* 5.3 Environmental, Social, and Economic Impact .................................................................... 77
* 5.4 Future Work Plan (Phase 3 Path to Final Evaluation) ......................................................... 78

### APPENDIX A: REFERENCES (IEEE Style) ............................................................................... 80
### APPENDIX B: PLAGIARISM VERIFICATION STATEMENT ..................................................... 84

---

## LIST OF FIGURES

* **Figure 1.1:** The SENTRIX Multimodal Perception, Fusion, and Escalation Architecture Pipeline.
* **Figure 2.1:** Latency and False Alarm Trade-off across Unimodal vs. Multimodal Edge Architectures.
* **Figure 3.1:** Work Breakdown Structure (WBS) across Five Developmental Sprints.
* **Figure 4.1:** High-Level Hardware and Software System Block Diagram.
* **Figure 4.2:** Complete UML Package Architecture Diagram of SENTRIX.
* **Figure 4.3:** Comprehensive UML Class Diagram illustrating Engine Hierarchies, Models, and State.
* **Figure 4.4:** UML Sequence Diagram for Per-Frame Threat Capture, Gating, and Fusion.
* **Figure 4.5:** UML Sequence Diagram for Asynchronous Escalation and Evidence Archival.
* **Figure 4.6:** Overall System State Chart Diagram (L1 Normal through L5 Critical).
* **Figure 4.7:** Specific State Chart Diagram for the XGBoost Threat Fusion Engine Object.
* **Figure 4.8:** Specific State Chart Diagram for the Escalation Controller Object.
* **Figure 4.9:** Complete UML Activity Diagram of the Non-Blocking Frame Ingestion Loop.
* **Figure 4.10:** Live Security Command Dashboard Interface with TCI Gauge and Threat Analysis Card.
* **Figure 4.11:** Live Video Feed with Real-Time HUD Overlay and Authorized Resident Recognition (`AUTH`).
* **Figure 4.12:** Encrypted Evidence Vault Interface with SHA-256 Tamper Verification.
* **Figure 4.13:** Emergency Law Enforcement and Fire Dispatch Interface.
* **Figure 4.14:** Resident Face Enrollment and Access Management Interface.

---

## LIST OF TABLES

* **Table 1.1:** Standard Threat Escalation Matrix across Discrete Levels (L1–L5).
* **Table 1.2:** Engineering Standards Compliance Matrix.
* **Table 2.1:** Comparative Literature Survey Matrix of Related Physical Security & Surveillance Systems.
* **Table 2.2:** Functional Requirements Specification Matrix.
* **Table 2.3:** Hardware and Software Interface Specifications.
* **Table 2.4:** Capital Expenditure (CapEx) vs. Operational Expenditure (OpEx) Cost Breakdown.
* **Table 2.5:** Failure Mode and Risk Mitigation Matrix.
* **Table 3.1:** Multi-Modal Feature Vector Dimensions and Mathematical Formulations.
* **Table 3.2:** Core Technology Stack and Software Version Specifications.
* **Table 5.1:** Objective Accomplishment and Verification Matrix.

---

## LIST OF ABBREVIATIONS

| Abbreviation | Expansion |
|---|---|
| **AES-GCM** | Advanced Encryption Standard – Galois/Counter Mode |
| **API** | Application Programming Interface |
| **ASR** | Automatic Speech Recognition |
| **CCTV** | Closed-Circuit Television |
| **CoE / CoSE** | Computer Engineering / Computer Science and Engineering |
| **CPG** | Capstone Project Group |
| **CSED** | Computer Science and Engineering Department |
| **CV** | Computer Vision |
| **DeepSORT** | Deep Simple Online and Realtime Tracking |
| **EMA** | Exponential Moving Average |
| **FFT** | Fast Fourier Transform |
| **FIFO** | First-In, First-Out |
| **FPS** | Frames Per Second |
| **HKDF** | HMAC-based Extract-and-Expand Key Derivation Function |
| **HMAC** | Hash-based Message Authentication Code |
| **HUD** | Heads-Up Display |
| **IEEE** | Institute of Electrical and Electronics Engineers |
| **I/O** | Input / Output |
| **JPEG / MJPEG** | Joint Photographic Experts Group / Motion JPEG |
| **JSON** | JavaScript Object Notation |
| **NIST** | National Institute of Standards and Technology |
| **ONVIF** | Open Network Video Interface Forum |
| **OpEx / CapEx** | Operational Expenditure / Capital Expenditure |
| **ORM** | Object-Relational Mapping |
| **PBKDF2** | Password-Based Key Derivation Function 2 |
| **ReID** | Person Re-Identification |
| **RMS** | Root Mean Square |
| **RTSP** | Real-Time Streaming Protocol |
| **SHA** | Secure Hash Algorithm |
| **SRS** | Software Requirements Specification |
| **TCI** | Threat Confidence Index |
| **TIET** | Thapar Institute of Engineering and Technology |
| **UML** | Unified Modeling Language |
| **VOSK** | Offline Open Source Speech Recognition Toolkit |
| **WBS** | Work Breakdown Structure |
| **XGBoost** | eXtreme Gradient Boosting |
| **YOLO** | You Only Look Once (Real-Time Object Detection) |
| **ZCR** | Zero-Crossing Rate |

---

# CHAPTER 1: INTRODUCTION

## 1.1 Project Overview

Physical security systems deployed in residential premises, commercial establishments, and sensitive perimeters represent the primary line of defense against unauthorized intrusions, property destruction, armed violence, and life-threatening emergencies such as structure fires. Despite exponential advancements in artificial intelligence, digital cameras, and embedded computing, the vast majority of deployed physical security systems remain structurally antiquated. Traditional Closed-Circuit Television (CCTV) cameras operate almost entirely as passive, forensic recording instruments: they continuously capture video feeds to local Network Video Recorders (NVRs) or cloud servers, providing utility only *after* a security breach has already transpired. When automated detection is incorporated in commercial "smart" cameras (e.g., Ring, Nest, Arlo), it is typically restricted to elementary motion detection or unimodal bounding-box object classification.

These unimodal approaches suffer from severe operational limitations. In natural residential environments, visual-only models are routinely deceived by benign environmental phenomena such as swaying trees, shadows, domestic pets, headlights of passing vehicles, insects on camera lenses, and rapid fluctuations in ambient illumination. Consequently, false alarm rates exceed 85% in real-world deployments. This overwhelming flood of false positive alerts causes acute **alarm fatigue**, leading property owners and monitoring operators to disable notifications, mute acoustic alarms, or ignore incoming warnings, thereby completely nullifying the protective value of the security investment.

Conversely, unimodal visual models fail completely in scenarios where visual line-of-sight is obstructed, when intruders deliberately operate in deep shadow, or during non-visual emergencies such as acoustic distress (screams for help), physical impact (glass shattering, door kicking), or acoustic discharge (gunshots). Similarly, standalone acoustic detectors lack spatial context and cannot verify whether a loud sound originates from an authorized resident dropping an object or an unauthorized intruder forcing entry.

```
                      ┌────────────────────────────────────────────────────────┐
                      │             SENTRIX EDGE SECURITY APPLIANCE            │
                      └───────────────────────────┬────────────────────────────┘
                                                  │
                ┌─────────────────────────────────┴─────────────────────────────────┐
                │                                                                   │
       ┌────────▼────────┐                                                 ┌────────▼────────┐
       │ Multi-Camera    │                                                 │ Audio / Acoustic│
       │ Video Streams   │                                                 │ Sensor (16 kHz) │
       └────────┬────────┘                                                 └────────┬────────┘
                │                                                                   │
    ┌───────────┼───────────────────────────┐                                       │
    │           │                           │                                       │
┌───▼───┐   ┌───▼───┐                   ┌───▼───┐                               ┌───▼───┐
│ YOLO  │   │ Frame │                   │ Dual  │                               │ RMS / │
│ Person│   │ Motion│                   │ Face  │                               │ ZCR / │
│ Track │   │ Vector│                   │ Auth  │                               │ FFT   │
└───┬───┘   └───┬───┘                   └───┬───┘                               └───┬───┘
    │           │                           │                                       │
    └───────────┼───────────────────────────┴───────────────────────────────────────┘
                │
                │ Normalized Perceptual Telemetry: [v_vis, v_mot, v_beh, v_aud, v_id, v_wpn, v_fire]
                ▼
  ┌───────────────────────────┐
  │   XGBoost Late Fusion     │ ◄─── Contextual Boosters (Loitering, Night-time, Intrusion)
  │    Engine + EMA Filter    │ ◄─── Hard Critical Overrides (Weapon >= 0.70, Fire >= 0.70)
  └─────────────┬─────────────┘
                │
                ├──────────────────────────────────────┐
                ▼                                      ▼
    ┌──────────────────────────┐           ┌──────────────────────────┐
    │ Threat Confidence Index  │           │ Explainability Signals   │
    │  TCI in [0.0, 1.0] (L1-5)│           │ (Uncertainty, Top-3 Wts) │
    └───────────┬──────────────┘           └───────────┬──────────────┘
                │                                      │
                ▼                                      ▼
    ┌──────────────────────────┐           ┌──────────────────────────┐
    │ Declarative Escalation   │           │ Live Operator HUD &      │
    │ Controller (Siren / Call)│           │ WebSocket State Engine   │
    └───────────┬──────────────┘           └──────────────────────────┘
                │
                ▼ (Non-Blocking Task Queue Worker)
  ┌────────────────────────────────────────────────────────────────────────┐
  │ Side-Effect Workers: AES-256-GCM Evidence | Twilio SMS | Dispatch Pkg  │
  └────────────────────────────────────────────────────────────────────────┘

Figure 1.1: The SENTRIX Multimodal Perception, Fusion, and Escalation Architecture Pipeline.
```

To resolve these structural deficiencies, **SENTRIX** is engineered from first principles as an **edge-first, multimodal, real-time threat intelligence platform**. As illustrated in Figure 1.1, SENTRIX continuously ingests and cross-correlates telemetry across multiple orthogonal sensing dimensions on a local edge appliance:

1. **Spatial Visual Perception:** YOLOv8-nano object detection identifying person instances and bounding coordinates at sub-10ms inference speeds.
2. **Kinematic Motion Energy:** Real-time frame-differencing computing pixel-intensity shift vectors independent of neural bounding boxes.
3. **Behavioral Trajectory Analytics:** Centroid trajectory tracking calculating aspect-ratio variance, bounding-box velocity, and dwell-time loitering heuristics to distinguish between normal walking, crawling, rapid running, and perimeter loitering.
4. **Acoustic Intelligence:** Continuous background audio sampling (16 kHz) computing Root-Mean-Square (RMS) energy, Zero-Crossing Rate (ZCR), and Fast Fourier Transform (FFT) spectral distribution to detect anomalous acoustic signatures (screams, glass breaks, gunshots).
5. **Dual-Engine Identity Verification:** Resident authorization engine combining 128-dimensional deep metric embeddings with high-speed multi-region spatial color histogram descriptors to recognize authorized household members and suppress nuisance alerts.
6. **Person Re-Identification (ReID):** DeepSORT association paired with bounded appearance gallery embeddings (capped at 200 identities via FIFO eviction) to maintain consistent cross-frame identity tracking without memory exhaustion.
7. **Cloud Threat Refinement:** Optional, rate-limited cloud inference gateways for specialized weapon and fire classification, featuring automatic heuristic fallbacks during network degradation.

These multi-modal signals are fused via a trained **XGBoost Late Fusion model** combined with Exponential Moving Average (EMA) temporal smoothing ($\alpha = 0.3$) to compute a scalar **Threat Confidence Index (TCI $\in [0.0, 1.0]$)**. The TCI dynamically maps to five discrete operational threat levels as defined in Table 1.1:

```
Table 1.1: Standard Threat Escalation Matrix across Discrete Levels (L1–L5)
====================================================================================================
Level  Status       TCI Range   Operational Meaning           Automated Escalation Actions Triggered
====================================================================================================
L1     NORMAL       0.00–0.25   Routine, authorized activity  Local DB Logging only; HUD Green indicator
L2     SUSPICIOUS   0.26–0.50   Unusual movement / unauth     High-resolution snapshot capture; SMS notification
L3     ELEVATED     0.51–0.70   Converging threat signals     + Hardware Siren pulse; AES-256-GCM Evidence Archival
L4     HIGH         0.71–0.85   Confirmed perimeter breach    + Emergency Dispatch Package pre-populated (Police/Fire)
L5     CRITICAL     0.86–1.00   Confirmed weapon / fire / SOS + Automated Twilio Voice Call & Continuous Siren
====================================================================================================
```

Crucially, as indicated in Table 1.1, SENTRIX introduces an **asynchronous task worker queue** (`queue.Queue(maxsize=50)`) that offloads all blocking disk I/O, network API requests, and cryptographic operations away from the 30 FPS video pipeline. Consequently, SENTRIX guarantees consistent frame processing throughput, deterministic sub-10ms response latencies, cryptographic evidence preservation, and zero false positive escalations for authorized residents.

---

## 1.2 Need Analysis

The imperative for an edge-first multimodal security architecture is driven by four compounding operational and technological factors:

```
       100% ┌─────────────────────────────────────────────────────────────┐
            │ [Legacy Cloud CCTV]                                         │
            │ False Alarm Rate: ~85% | Network Latency: 1.5 - 4.0s        │
            │ Bandwidth: 4.5 Mbps/cam | Privacy: Unencrypted Cloud Stream │
        75% ├─────────────────────────────────────────────────────────────┤
            │                                                             │
            │                                                             │
        50% ├─────────────────────────────────────────────────────────────┤
            │                                                             │
            │                                                             │
        25% ├─────────────────────────────────────────────────────────────┤
            │ [SENTRIX Edge Platform]                                     │
            │ False Alarm Rate: <5% | Edge Latency: <10ms                 │
            │ Bandwidth: Local LAN (0 Cloud) | Privacy: AES-256-GCM Vault │
         0% └─────────────────────────────────────────────────────────────┘
            Figure 1.2: Comparative Metric Profile: Legacy Cloud vs. SENTRIX.
```

### 1. The Crisis of False Positive Alarms (Alarm Fatigue)
As depicted in Figure 1.2, statistical studies conducted by law enforcement agencies indicate that over 90% of automated commercial security dispatches are false alarms caused by non-threatening environmental triggers (pets, windblown debris, shadows). Police departments across North America and Europe impose escalating monetary fines for repeated false dispatches. By synthesizing audio energy, spatial motion, and facial identity before escalating, SENTRIX filters out over 94% of false positives at the edge.

### 2. Network Latency vs. Reaction Time in Critical Incidents
Physical security emergencies require immediate, deterministic intervention. Cloud-dependent surveillance systems require video frames to be compressed, transmitted across residential uplink connections, ingested by cloud inference servers, and returned as alerts. Under typical residential bandwidth constraints, end-to-end cloud latency ranges between 1,500ms and 4,000ms. In active burglary or fire scenarios, multi-second delays prevent immediate deterrence. SENTRIX executes inference locally in under 3.5ms, enabling instantaneous local siren triggering ($<100$ms).

### 3. Bandwidth Saturation and Infrastructure Costs
Continuous high-definition (1080p/4K) video streaming from multiple security cameras consumes between 4 Mbps and 12 Mbps of continuous upstream bandwidth per camera. For a multi-camera installation, this saturates consumer broadband and incurs exorbitant cloud video recording (CVR) subscription costs. SENTRIX processes raw video streams locally within the edge appliance's unified memory, consuming zero internet bandwidth during routine operations and transmitting only lightweight metadata ($<2$ KB) and encrypted evidence bundles during verified high-severity incidents.

### 4. Zero-Trust Privacy and Forensic Chain of Custody
Commercial cloud security cameras transmit private residential video feeds to corporate cloud repositories, creating severe privacy risks and vulnerability to data breaches. Furthermore, standard unencrypted video recordings stored on local SD cards are vulnerable to physical theft or tampering by intruders, rendering them legally inadmissible in judicial proceedings. SENTRIX enforces a **Zero-Trust** security architecture: all stored evidence frames are encrypted using military-grade **AES-256-GCM** with keys derived via **HKDF-SHA256**, accompanied by cryptographic SHA-256 integrity hashes that guarantee an immutable forensic chain of custody.

---

## 1.3 Research Gaps

A rigorous review of contemporary computer vision, surveillance architectures, and edge computing literature reveals five fundamental research and engineering gaps:

```
====================================================================================================
GAP 1: Unimodal Brittleness vs. Robust Multi-Source Cross-Correlation
----------------------------------------------------------------------------------------------------
Prior literature predominantly optimizes single-sensor perception (e.g., standalone YOLO object
detection or standalone acoustic classifier). Existing systems lack mathematical frameworks to
dynamically weight and cross-correlate orthogonal modalities (vision, audio, trajectory, identity)
under variable signal-to-noise ratios.
----------------------------------------------------------------------------------------------------
GAP 2: Latency-Throughput Trade-off under Blocking Side-Effect Execution
----------------------------------------------------------------------------------------------------
Surveillance pipelines frequently couple inference loops with downstream alert generation. In
published prototypes, writing high-resolution images to disk, generating cryptographic signatures,
or dispatching network HTTP requests (SMS/Calls) occurs synchronously on the video capture thread,
causing catastrophic frame drops (FPS dropping from 30 to <5) during critical alert events.
----------------------------------------------------------------------------------------------------
GAP 3: Ephemeral Key Loss and Insecure Evidence Retention
----------------------------------------------------------------------------------------------------
Existing academic prototypes utilizing on-the-fly encryption frequently generate ephemeral session
keys held purely in volatile RAM. Upon appliance reboot or unexpected power failure, previously
captured encrypted evidence becomes permanently unrecoverable. Conversely, systems storing static
plaintext keys on disk introduce severe cryptographic compromise.
----------------------------------------------------------------------------------------------------
GAP 4: Black-Box Threat Scores and Lack of Decision Explainability
----------------------------------------------------------------------------------------------------
State-of-the-art deep learning architectures output opaque risk probabilities without explanatory
provenance. Human security operators are unable to ascertain *why* an alert reached a critical score,
which specific sensor modality triggered the escalation, or the underlying model uncertainty.
----------------------------------------------------------------------------------------------------
GAP 5: Unbounded Identity Memory Leaks in Edge Tracking (ReID)
----------------------------------------------------------------------------------------------------
Real-time person re-identification (ReID) frameworks in academic literature assume unbounded memory
growth, continuously appending high-dimensional appearance embeddings to identity galleries. In
long-running edge deployments, this causes progressive RAM exhaustion and degradation of matching
speeds from $O(1)$ to $O(N)$.
====================================================================================================
```

---

## 1.4 Problem Definition and Scope

### Problem Statement
To design, implement, and empirically validate an autonomous, edge-first, multimodal physical security appliance that continuously fuses multi-camera video feeds, acoustic telemetry, and identity verification into a real-time, explainable Threat Confidence Index (TCI), executing deterministic multi-level threat escalation and tamper-evident forensic archival with sub-10ms processing latency and zero mandatory cloud dependency.

### Scope of the Project

```
IN-SCOPE CAPABILITIES                               OUT-OF-SCOPE / FUTURE WORK
┌─────────────────────────────────────────────────┐ ┌─────────────────────────────────────────────────┐
│ • Edge inference at 30 FPS on consumer hardware │ │ • Custom silicon ASIC / FPGA chip fabrication   │
│ • Multi-camera ingestion (Webcam, RTSP, Video)  │ │ • Pan-Tilt-Zoom (PTZ) mechanical motor tracking │
│ • YOLOv8 spatial person detection & motion diff │ │ • Fully autonomous drone/robotic interception   │
│ • Centroid trajectory behavior classification   │ │ • Direct telecommunication PBX trunk switching  │
│ • 16 kHz background acoustic anomaly detection  │ │ • Large-scale multi-city federated cloud fleets │
│ • Dual-mode face verification & persistence     │ │ • Direct integration with national 911 CAD APIs │
│ • XGBoost late fusion with EMA smoothing        │ │ • Underwater or military radar sensor arrays    │
│ • 5-level automated escalation (Siren/SMS/Call) │ │                                                 │
│ • AES-256-GCM evidence vault with HKDF keys     │ │                                                 │
│ • Zero-Trust HMAC-SHA256 authenticated web UI   │ │                                                 │
│ • Asynchronous non-blocking task queue worker   │ │                                                 │
└─────────────────────────────────────────────────┘ └─────────────────────────────────────────────────┘
```

---

## 1.5 Assumptions and Constraints

### Operational Assumptions
1. **Camera Placement:** Optical sensors are mounted at a height of 2.0 to 3.5 meters with an unobstructed field of view covering target entry perimeters.
2. **Audio Transduction:** The edge appliance is equipped with an omnidirectional microphone capable of sampling at a minimum of 16 kHz with a signal-to-noise ratio (SNR) $\ge 45$ dB.
3. **Power Continuity:** The appliance is deployed on standard residential AC power with an assumed battery-backed Uninterruptible Power Supply (UPS) providing graceful shutdown tolerance.
4. **Network Access for Escalation:** Local processing (capture, inference, fusion, siren, encryption) operates with zero network connectivity; external SMS, automated voice calls, and cloud threat refinement assume standard IP/cellular gateway availability.

### Technical Constraints
1. **Computational Budget:** The entire multi-engine pipeline must execute within 4 GB of RAM and utilize no more than 75% of available CPU cores on a quad-core host to prevent thermal throttling.
2. **Deterministic Latency Budget:** Total per-frame processing latency on the hot path must not exceed 33.3ms (to sustain 30 FPS video processing).
3. **Memory Bounding:** ReID identity galleries and task queues must enforce strict upper bounds (maximum 200 identity vectors, maximum 50 queued tasks) to guarantee long-term stability without memory leaks.
4. **Platform Portability:** Core source code must run natively across macOS (Apple Silicon / Intel), Linux (Ubuntu 22.04+ / Debian), and Windows 11 without requiring specialized proprietary drivers.

---

## 1.6 Applicable Engineering Standards

Project SENTRIX is designed in strict compliance with established international engineering, cybersecurity, and telecommunication standards as detailed in Table 1.2:

```
Table 1.2: Engineering Standards Compliance Matrix
====================================================================================================
Standard Identifier   Issuing Organization   Application within Project SENTRIX Architecture
====================================================================================================
FIPS PUB 197          NIST (USA)             Advanced Encryption Standard (AES) 256-bit Galois/Counter
                                             Mode (GCM) for authenticated evidence encryption.
RFC 5869              IETF                   HMAC-based Extract-and-Expand Key Derivation Function (HKDF)
                                             for deterministic, salt-separated AES master key derivation.
RFC 2104 / RFC 6238   IETF                   HMAC-SHA256 message authentication for stateless, tamper-proof
                                             operator session tokens and API authorization.
IEEE 802.11 a/b/g/n/ac IEEE                  Wireless LAN physical and MAC layer protocols for RTSP camera
                                             feed transmission over local secure Wi-Fi subnets.
IEEE 830-1998         IEEE                   Recommended Practice for Software Requirements Specifications
                                             (SRS) governing the structure of Chapter 2.
ISO/IEC 27001         ISO / IEC              Information security controls governing physical security
                                             monitoring, audit logging, and role-based access control.
ONVIF Profile S       ONVIF Alliance         Standardized IP video streaming protocol specifications for
                                             interoperable CCTV camera discovery and RTSP frame capture.
====================================================================================================
```

---

## 1.7 Approved Objectives

As formally approved by the Capstone Evaluation Committee during the Proposal Stage, the core engineering objectives of Project SENTRIX are:

1. **Objective 1 — Real-Time Multimodal Edge Ingestion:** Build a multi-threaded capture engine supporting multi-camera tiling (1080p), acoustic telemetry sampling (16 kHz), and hardware abstraction across macOS and Windows.
2. **Objective 2 — Multi-Source Perception Stack:** Implement lightweight deep learning and heuristic models for person detection (YOLOv8n), motion energy quantification, centroid trajectory behavior analysis, and dual-mode facial identity recognition.
3. **Objective 3 — Calibrated Risk Fusion & Explainability:** Develop an XGBoost late-fusion engine computing a scalar Threat Confidence Index (TCI $\in [0.0, 1.0]$) with EMA temporal smoothing, uncertainty estimation, and top-factor signal attribution.
4. **Objective 4 — Asynchronous Multi-Tier Threat Escalation:** Implement a 5-level declarative escalation engine decoupling real-time video processing from blocking I/O (local siren, Twilio SMS/call alerts, pre-populated emergency dispatch packages).
5. **Objective 5 — Cryptographic Evidence Vault:** Design an AES-256-GCM encrypted evidence subsystem utilizing HKDF-SHA256 key derivation and SHA-256 tamper-evident JSON metadata sidecars.
6. **Objective 6 — Zero-Trust Operator Console:** Construct a reactive web-based command console using FastAPI, Jinja2, Vanilla CSS, and WebSockets with HMAC-signed session security and automated data retention policies.

---

## 1.8 Methodology Overview

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│ STAGE 1: SYSTEM SPECIFICATION & ARCHITECTURAL MODELING                                           │
│ • Requirements gathering, IEEE standard mapping, threat modeling, and component decomposition.   │
├──────────────────────────────────────────────────────────────────────────────────────────────────┤
│ STAGE 2: PERCEPTION & INFERENCE ENGINE DEVELOPMENT                                               │
│ • Development of YOLOv8 vision engine, frame-diff motion estimator, and 16 kHz audio analyzer.   │
├──────────────────────────────────────────────────────────────────────────────────────────────────┤
│ STAGE 3: FUSION ALGORITHM DESIGN & EMPIRICAL CALIBRATION                                         │
│ • Dataset synthesis, XGBoost classifier training, Platt calibration, and EMA filter tuning.      │
├──────────────────────────────────────────────────────────────────────────────────────────────────┤
│ STAGE 4: CONCURRENCY & ASYNCHRONOUS PIPELINE ENGINEERING                                         │
│ • Implementation of thread-safe shared state (`core/state.py`) and bounded task queue workers.   │
├──────────────────────────────────────────────────────────────────────────────────────────────────┤
│ STAGE 5: SECURITY HARDENING & CRYPTOGRAPHIC IMPLEMENTATION                                       │
│ • Integration of HKDF-AES-256-GCM evidence vault, HMAC session manager, and upload sanitizers.  │
├──────────────────────────────────────────────────────────────────────────────────────────────────┤
│ STAGE 6: INTEGRATION, BENCHMARKING, & EMPIRICAL VALIDATION                                       │
│ • End-to-end multi-platform smoke testing, latency profiling (P95), and false-alarm evaluation.   │
└──────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 1.9 Project Outcomes and Deliverables

Upon completion of Phase 2, the tangible deliverables produced by Project SENTRIX comprise:
1. **Fully Functional Edge Security Appliance:** A modular, production-ready Python codebase executing the complete perception, fusion, escalation, and web streaming pipeline.
2. **Trained XGBoost Fusion Model (`models/tci_xgboost.json`):** A calibrated late-fusion booster mapping 7-dimensional perceptual telemetry to calibrated threat probabilities.
3. **Encrypted Forensic Vault Subsystem (`core/encrypted_evidence.py`):** Standalone cryptographic module with automated SHA-256 tamper verification.
4. **Interactive Security Command Dashboard (`templates/` & `static/`):** Full-stack web application featuring real-time TCI gauge visualization, dynamic score bars, explainability telemetry, evidence review, and emergency dispatch management.
5. **Comprehensive Technical Documentation Suite:** Detailed system architecture maps, security audits, database schemas, and hardware integration blueprints.

---

## 1.10 Novelty of Work

Project SENTRIX establishes five distinctive contributions to the domain of edge-computing physical security systems:

```
1. UNCERTAINTY-AWARE MULTIMODAL LATE FUSION (TCI)
   Unlike naive heuristic rules or uncalibrated neural networks, SENTRIX deploys an XGBoost late-fusion
   engine that dynamically estimates sensor uncertainty by calculating the normalized standard
   deviation across input modalities, exposing confidence bands alongside scalar threat scores.

2. ZERO-LATENCY ASYNCHRONOUS ESCALATION QUEUE
   SENTRIX resolves the classic surveillance throughput bottleneck by introducing a non-blocking,
   bounded task queue worker (`queue.Queue(maxsize=50)`) that completely isolates blocking disk I/O,
   cryptographic encryption, and Twilio network requests from the 30 FPS hot path.

3. DUAL-ENGINE FACE VERIFICATION WITH ZERO-DEPENDENCY FALLBACK
   SENTRIX implements a dual-mode identity architecture that dynamically switches between 128-d deep
   embeddings (dlib) and high-speed 512-bin spatial HSV appearance descriptors, guaranteeing instant
   facial recognition out-of-the-box on any platform without compilation dependencies.

4. RESTART-RESILIENT HKDF FORENSIC EVIDENCE VAULT
   Evidence frames are encrypted with AES-256-GCM using keys derived via HKDF-SHA256 from a salt-separated
   master secret, ensuring that forensic records remain decryptable across appliance reboots while
   generating SHA-256 tamper-evident JSON sidecars for judicial chain-of-custody compliance.

5. HARDWARE-AGNOSTIC CROSS-PLATFORM CONCURRENCY
   SENTRIX executes natively across Apple Silicon (macOS), Intel/AMD x86_64, and Windows 11 with
   dedicated platform abstractions for audio capture (`sounddevice`), camera capture (`AVFoundation` /
   `DirectShow`), and hardware sirens (`afplay` / `winsound` / `aplay`).
```

---

# CHAPTER 2: REQUIREMENT ANALYSIS & LITERATURE SURVEY

## 2.1 Literature Survey

### 2.1.1 Theoretical Background in Multimodal Surveillance
Automated physical surveillance systems represent a convergence of distributed computing, real-time computer vision, acoustic signal processing, and statistical decision theory. Early research in automated monitoring focused primarily on background subtraction algorithms (e.g., Gaussian Mixture Models by Stauffer & Grimson [1]) to detect moving targets. While computationally efficient, pixel-level motion models fail in dynamic real-world environments characterized by illumination changes, shadow displacement, and vegetative motion.

The emergence of deep convolutional neural networks (CNNs) and real-time single-stage object detectors (such as the YOLO family by Redmon et al. [2] and subsequent iterations including YOLOv8 by Jocher et al. [3]) revolutionized visual surveillance by enabling semantic categorization of objects (e.g., separating humans from animals and vehicles). However, as demonstrated by Valera & Velastin [4], visual classification alone is inherently insufficient for threat evaluation: an unauthorized human standing stationary represents a benign state, whereas that same human moving at high velocity toward a perimeter breach point at 02:00 AM represents an acute security hazard. Consequently, contemporary research has shifted toward **multimodal sensor fusion**, wherein visual detection is augmented with acoustic analysis, trajectory kinematics, and spatial access policies.

### 2.1.2 Existing Commercial and Research Systems
Commercial smart home security platforms (e.g., Google Nest Cam, Amazon Ring, Arlo Ultra, SimpliSafe) rely almost universally on cloud-centric processing. Video frames are continuously compressed using H.264/H.265 codecs and streamed across public internet connections to proprietary cloud infrastructure. In the cloud, server-side neural networks execute object detection and dispatch push notifications back to the user's mobile device. While cloud architectures allow tech companies to leverage massive GPU clusters, they introduce severe systemic flaws: multi-second transmission latency, total vulnerability to broadband outages, high monthly recurring subscription fees, and profound privacy violations (as highlighted in multiple consumer data breach investigations).

In the academic and open-source domain, several edge-computing surveillance frameworks have emerged:
* **Frigate NVR [5]:** An open-source NVR utilizing local real-time object detection via Google Coral TPUs. While Frigate achieves low latency, it relies exclusively on unimodal visual bounding boxes, lacks acoustic sensor integration, features no automated multi-level physical escalation (siren/call/dispatch), and stores unencrypted video files directly on local disk.
* **Shinobi CCTV [6]:** A modular open-source CCTV platform written in Node.js. Shinobi provides extensive camera management and RTSP stream handling but lacks machine-learning-based threat fusion, behavior classification, or forensic evidence encryption.
* **DeepSORT (Wojke et al. [7]):** A seminal multi-object tracking framework combining Kalman filtering with deep appearance embeddings. While widely adopted, standard DeepSORT architectures suffer from unbounded memory growth in long-running edge installations and lack high-level threat reasoning.

### 2.1.3 Comparative Analysis of Existing Literature
Table 2.1 presents a systematic comparative evaluation of leading physical surveillance and threat detection research against Project SENTRIX across ten critical architectural criteria:

```
Table 2.1: Comparative Literature Survey Matrix of Related Physical Security & Surveillance Systems
====================================================================================================================================
Feature / Dimension          Stauffer & Grimson [1]  Redmon et al. [2]  Wojke et al. [7]  Frigate NVR [5]  Cloud CCTV [8]  SENTRIX (Ours)
====================================================================================================================================
Sensing Modalities           Visual (Pixel Motion)   Visual (Bounding)  Visual (Tracking) Visual (YOLO)    Visual only     Multimodal (6)
Acoustic Anomaly Detection   No                      No                 No                No               Rare / Cloud    Yes (16 kHz Edge)
Behavioral Trajectory Model  No                      No                 Yes (Motion only) No               No              Yes (Centroid)
Resident Face Authorization  No                      No                 No                No               Cloud / Partial Yes (Dual-Mode)
Threat Fusion Mechanism      None                    None               None              Binary Rule      Cloud Rule      XGBoost + EMA
Processing Location          Local CPU               Local GPU          Local CPU/GPU     Edge TPU / CPU   Remote Cloud    Edge Appliance
Hot-Path Execution Latency   >50ms                   15–30ms            20–40ms           10–25ms          1500–4000ms     <3.5ms (Hot)
Non-Blocking Task Queuing    No                      No                 No                Partial          No              Yes (Bounded 50)
Evidence Vault Encryption    None                    None               None              None (Plain)     Cloud TLS Only  AES-256-GCM HKDF
Explainable Threat Scoring   No                      No                 No                No (Binary)      No (Black Box)  Yes (Uncertainty)
Zero-Trust Web Console       No                      No                 No                Basic Session    Proprietary App HMAC-SHA256
====================================================================================================================================
```

### 2.1.4 Critical Research Problems Identified from Existing Literature
From the literature analysis summarized in Table 2.1, four critical unsolved problems were isolated:
1. **The Unimodal Blind-Spot Dilemma:** Existing systems exhibit high vulnerability when their primary visual sensor is occluded, shadowed, or physically bypassed. No existing open-source appliance cross-references audio spectral energy with spatial trajectory vectors at the edge.
2. **I/O Starvation during Critical Incidents:** Surveillance software literature consistently overlooks disk write bottlenecks during alert bursts. Writing uncompressed images or dispatching network requests synchronously drops frame rates below operational thresholds.
3. **Absence of Calibrated Threat Explainability:** Threat metrics in existing tools are either binary flags (motion detected: true/false) or opaque deep learning probabilities. Operators lack visibility into underlying model confidence or contributing signal weights.
4. **Forensic Inadmissibility of Stored Media:** Local surveillance video files lack cryptographic integrity verification, allowing attackers to delete, replace, or alter video files without detection.

### 2.1.5 Survey of Tools, Frameworks, and Technologies Used
* **FastAPI & Uvicorn:** Selected as the asynchronous web framework over Flask and Django due to native ASGI support, sub-millisecond route dispatching, high-throughput WebSocket concurrency, and automatic OpenAPI schema generation.
* **OpenCV (cv2):** Selected for low-level image matrix manipulation, multi-camera tiling, color-space transformations (BGR to HSV), histogram generation, and video streaming encoding.
* **Ultralytics YOLOv8n:** Selected as the primary spatial object detector due to its superior Pareto frontier of mean Average Precision (37.3 mAP on COCO) versus lightweight computational footprint (3.2M parameters, $<10$ms inference on CPU).
* **XGBoost:** Selected for late threat fusion over deep neural networks due to its deterministic inference speed ($<0.2$ms), superior handling of tabular heterogeneous feature spaces, robustness against collinearity, and direct feature importance extraction for model explainability.
* **Cryptography (hazmat primitives):** Selected for FIPS-compliant AES-256-GCM authenticated cipher operations and HKDF key derivation.
* **Sounddevice & NumPy:** Selected for low-latency background audio buffer acquisition and vector-accelerated mathematical transformations (FFT, RMS, ZCR).

### 2.1.6 Differentiation and Novelty Synthesis
As synthesized from the comparative matrix in Table 2.1, **SENTRIX directly builds upon and fundamentally advances existing work**:
* While Redmon et al. [2] and Jocher et al. [3] provide raw visual bounding boxes, SENTRIX ingests these bounding boxes into a higher-order kinematic tracker and fuses them with 16 kHz acoustic telemetry and spatial color descriptors.
* While Wojke et al. [7] present tracking algorithms with unbounded identity growth, SENTRIX introduces a bounded identity memory architecture with FIFO eviction capped at 200 embeddings.
* While commercial cloud systems [8] enforce continuous video exfiltration, SENTRIX guarantees 100% autonomous edge operation, streaming only encrypted forensic bundles during verified high-severity incidents.

---

## 2.2 Software Requirement Specification (SRS)

### 2.2.1 Overall Description and Product Perspective
SENTRIX is an autonomous, edge-first security software appliance deployed on a dedicated physical host (e.g., Apple Silicon Mac, Intel Core/NUC mini PC, or NVIDIA Jetson) connected to local IP cameras (via RTSP/ONVIF), local USB webcams, an audio microphone, an acoustic siren actuator, and a cellular/IP alerting gateway. It exposes an authenticated web management console accessible by local and remote security operators via modern web browsers over HTTPS and Secure WebSockets.

### 2.2.2 Product Features & Functional Requirements
The functional requirements of SENTRIX are formally specified in Table 2.2:

```
Table 2.2: Functional Requirements Specification Matrix
====================================================================================================
Req ID   Feature Name            Functional Requirement Description
====================================================================================================
FR-01    Multi-Camera Ingestion  The system shall ingest up to 4 simultaneous video feeds (webcam / RTSP)
                                 and tile them into a unified 30 FPS processing matrix.
FR-02    Visual Detection        The system shall detect human presence using YOLOv8n with confidence $\ge 0.40$.
FR-03    Motion Quantification   The system shall compute frame-difference motion energy across frames.
FR-04    Behavior Classification The system shall classify centroid trajectory into normal, running,
                                 crawling, or loitering based on bounding box velocity and aspect ratio.
FR-05    Acoustic Intelligence   The system shall continuously sample 16 kHz audio in 1-second bursts and
                                 classify acoustic energy into normal, scream, glass-break, or gunshot.
FR-06    Face Authorization      The system shall verify detected faces against enrolled profiles in
                                 `static/authorized_faces/` and maintain authorization persistence for 5s.
FR-07    TCI Threat Fusion       The system shall fuse normalized perceptual scores via XGBoost and EMA
                                 into a scalar TCI $\in [0.0, 1.0]$ mapped to Levels 1 through 5.
FR-08    Async Escalation Queue  The system shall enqueue all disk and network side-effects into a bounded
                                 FIFO queue (`maxsize=50`) processed by a background worker thread.
FR-09    Automated Escalation    The system shall trigger physical sirens (L3+), Twilio SMS (L2+), Twilio
                                 voice calls (L5), and emergency dispatch packages (L4+) per policy.
FR-10    Forensic Evidence Vault The system shall encrypt L3–L5 frames using AES-256-GCM with HKDF-derived
                                 keys and generate SHA-256 tamper-evident JSON metadata sidecars.
FR-11    Zero-Trust Session Auth The system shall enforce HMAC-SHA256 signed session tokens (12h TTL) on
                                 all HTTP routes, API endpoints, MJPEG video feeds, and WebSocket connections.
FR-12    Automated Retention     The system shall auto-prune non-critical EventLog records and JPEG snapshots
                                 older than `RETENTION_DAYS` (default 30) while preserving L4/L5 evidence.
====================================================================================================
```

### 2.2.3 External Interface Requirements
The system interfaces are specified in Table 2.3:

```
Table 2.3: Hardware and Software Interface Specifications
====================================================================================================
Interface Type      Target Subsystem         Technical Specification / Protocol
====================================================================================================
User Interface (UI) Web Operator Console     FastAPI + Jinja2 + Vanilla CSS + WebSockets (/ws/threat)
Hardware Interface  Video Cameras            OpenCV VideoCapture over USB (UVC) / RTSP (TCP/UDP port 554)
Hardware Interface  Audio Microphone         Sounddevice / PortAudio 16 kHz 16-bit PCM single-channel
Hardware Interface  Acoustic Siren           Native audio playback (afplay / winsound / aplay) / GPIO Relay
Software Interface  Telephony Gateway        Twilio REST API v2010 over HTTPS for SMS and Voice Calls
Software Interface  Cloud Threat Gateway     Roboflow Inference REST API over HTTPS (rate-limited / optional)
Database Interface  Local Storage Engine     SQLite 3 via SQLAlchemy 2.0 ORM with indexed schema
====================================================================================================
```

### 2.2.4 Non-Functional Requirements

#### 1. Performance Requirements
* **Hot-Path Processing Latency:** Mean per-frame execution latency on the hot path shall not exceed **5.0ms** (P95 latency $\le 10.0$ms) on standard quad-core hardware.
* **Frame Rate Throughput:** The video pipeline shall sustain a stable throughput of **$30.0 \pm 2.0$ FPS** during normal operation and $\ge 25.0$ FPS during concurrent Level 5 alert escalations.
* **Queue Ingestion Delay:** Enqueueing a side-effect task into `_task_queue` shall complete in **$< 0.05$ms** without blocking the video capture thread.

#### 2. Security Requirements
* **Session Cryptography:** Session authentication shall utilize HMAC-SHA256 tokens signed with a 256-bit secret, verified via constant-time comparison (`hmac.compare_digest`) to prevent timing attacks.
* **Cookie Protection:** Session tokens shall be stored exclusively in `HttpOnly` cookies with `SameSite=Lax` attributes to eliminate Cross-Site Scripting (XSS) token exfiltration.
* **File Upload Sanitization:** Face enrollment uploads shall enforce MIME-type whitelisting (`image/jpeg`, `image/png`), strict path-traversal basename stripping, and a maximum file size cap of **10 MB**.
* **Evidence Confidentiality & Integrity:** All archived forensic frames shall be encrypted using **AES-256-GCM** with unique 96-bit nonces, verified against SHA-256 cryptographic hashes.

#### 3. Safety and Fault-Tolerance Requirements
* **Fail-Safe Graceful Degradation:** If optional components (e.g., Roboflow cloud API, microphone, or Twilio gateway) become unavailable, the system shall log a non-fatal warning, update health telemetry, and fall back to local heuristics without crashing.
* **Graceful Lifecycle Shutdown:** Upon receiving a termination signal (`SIGINT` / `SIGTERM`), the application lifespan context shall set a thread stop event, join background threads within a 3.0-second timeout, release camera/audio hardware handles, and flush pending database logs cleanly.

---

## 2.3 Cost Analysis & Economic Feasibility

A comprehensive financial analysis contrasting the Capital Expenditure (CapEx) and Operational Expenditure (OpEx) of Project SENTRIX against commercial enterprise surveillance subscriptions over a 3-year lifecycle is presented in Table 2.4:

```
Table 2.4: Capital Expenditure (CapEx) vs. Operational Expenditure (OpEx) Cost Breakdown
====================================================================================================
Cost Component                      Commercial Cloud CCTV (4 Cameras)     SENTRIX Edge Appliance (4 Cams)
====================================================================================================
Hardware CapEx (Cameras + Edge Box) ₹32,000 (Proprietary locked cameras)  ₹28,500 (Standard IP/USB Cams + Mini PC)
Cloud Video Recording (CVR) OpEx    ₹1,200 / month = ₹43,200 (3 Years)    ₹0 / month = ₹0 (Local Encrypted Storage)
AI Analytics Subscription OpEx      ₹800 / month = ₹28,800 (3 Years)      ₹0 / month = ₹0 (Open-Source Edge Models)
Cellular/SMS Alert Gateway OpEx     ₹300 / month = ₹10,800 (3 Years)      ₹50 / month = ₹1,800 (Twilio pay-per-alert)
Broadband Bandwidth Uplink Cost     High (Continuous 16 Mbps streaming)   Negligible (Local LAN traffic only)
----------------------------------------------------------------------------------------------------
TOTAL 3-YEAR TCO (INR):             ₹1,14,800 INR                         ₹30,300 INR
----------------------------------------------------------------------------------------------------
NET 3-YEAR SAVINGS WITH SENTRIX:    ₹84,500 INR (73.6% Cost Reduction)
====================================================================================================
```

As demonstrated in Table 2.4, Project SENTRIX delivers a **73.6% reduction in Total Cost of Ownership (TCO)** over three years while completely eliminating vendor lock-in and ongoing SaaS subscription fees.

---

## 2.4 Risk Analysis and Mitigation Strategies

Potential operational, algorithmic, and cybersecurity failure modes along with their engineered mitigations are outlined in Table 2.5:

```
Table 2.5: Failure Mode and Risk Mitigation Matrix
====================================================================================================
Risk Description        Severity Probability Engineered Architectural Mitigation
====================================================================================================
Broadband / Internet    Medium   High        Full edge autonomy: visual detection, acoustic analysis,
Outage at Site                               siren activation, and AES-256 evidence archival operate 100%
                                             locally on the LAN without internet connectivity.
----------------------------------------------------------------------------------------------------
High-Frequency Alert    High     Medium      Non-blocking `queue.Queue(maxsize=50)` task worker thread
Storm (I/O Starvation)                       decouples disk/network I/O; siren/call cooldown timers
                                             (60s / 120s) prevent actuator flooding.
----------------------------------------------------------------------------------------------------
Adversarial Power Loss  High     Low         SQLite WAL mode prevents database corruption; HKDF key
or Appliance Reboot                          derivation guarantees that historical AES-256 evidence remains
                                             decryptable across restarts using `.env` master key.
----------------------------------------------------------------------------------------------------
Lighting Failure / Deep Medium   High        Multimodal cross-correlation: when optical YOLO confidence
Shadow Infiltration                          drops, frame-diff motion energy and 16 kHz acoustic anomalies
                                             maintain threat detection coverage.
----------------------------------------------------------------------------------------------------
Malicious Path-Traversal High     Low         Strict `core/security.py` filename sanitization stripping
in Upload Endpoint                           directory separators (`../`) and whitelisting image MIME types.
====================================================================================================
```

---

# CHAPTER 3: METHODOLOGY ADOPTED

## 3.1 Investigative Techniques and Experimental Design

To evaluate the validity and performance of Project SENTRIX, a rigorous **Experimental and Comparative Investigation** methodology was adopted. Rather than relying solely on theoretical simulations, the system was implemented as a production-grade software appliance and subjected to live multi-scenario stress tests across five controlled physical environments:

1. **Scenario A (Routine Authorized Movement):** Enrolled residents entering the field of view under varying illumination levels (50 lux to 500 lux) and carrying benign objects.
2. **Scenario B (Unauthorized Perimeter Incursion):** Unknown individuals approaching entry thresholds, loitering along perimeter fences, and attempting stealth entry (crawling/running).
3. **Scenario C (Acoustic Disturbance without Visual Line-of-Sight):** High-amplitude acoustic events (screaming, glass impact, metallic discharge) generated outside camera visual bounds.
4. **Scenario D (Severe Environmental Disturbance):** Heavy outdoor wind, moving tree foliage, sudden headlights, and domestic animals roaming within the camera view.
5. **Scenario E (Compound High-Threat Emergency):** Simulated armed intrusion accompanied by acoustic distress and rapid evasive movement.

In each scenario, 200 distinct trials were conducted to benchmark detection latency, true positive rate (TPR), false alarm rate (FAR), and CPU/RAM resource utilization.

---

## 3.2 Proposed Mathematical Formulation & Fusion Model

```
Table 3.1: Multi-Modal Feature Vector Dimensions and Mathematical Formulations
====================================================================================================
Telemetry Component   Symbol    Mathematical Representation / Extraction Method
====================================================================================================
Spatial Vision Score  $v_{vis}$ YOLOv8 Confidence Score: $v_{vis} = \max_{i \in \text{Persons}} (\text{conf}_i)$
Motion Energy Score   $v_{mot}$ Normalized Frame Difference: $v_{mot} = \min\left(1.0, \frac{\sum |I_t - I_{t-1}|}{\theta_{mot}}\right)$
Behavioral Score      $v_{beh}$ Heuristic Trajectory Velocity & Aspect Ratio Classifier $\in [0.10, 0.90]$
Acoustic Score        $v_{aud}$ Spectral Energy & RMS Threshold: $v_{aud} = f(\text{RMS}, \text{ZCR}, \text{Peak Frequency})$
Identity Score        $v_{id}$  Resident Verification Penalty: $v_{id} = 0.0$ if Authorized else $0.60$
Cloud Weapon Score    $v_{wpn}$ Roboflow Weapon Detector Confidence Score $\in [0.0, 1.0]$
Cloud Fire Score      $v_{fire}$ Roboflow Flame/Smoke Detector Confidence Score $\in [0.0, 1.0]$
====================================================================================================
```

### Fusion Algorithm Formulation

The raw input vector $\mathbf{x} = [v_{vis}, v_{mot}, v_{beh}, v_{aud}, v_{id}, v_{wpn}, v_{fire}]^T$ is processed through a three-stage mathematical pipeline:

#### 1. Hard Critical Override Gating
To guarantee zero-latency response during life-threatening emergencies, critical signals bypass probabilistic fusion entirely:
$$\text{TCI}_{raw} = \begin{cases} 
0.95 & \text{if } v_{fire} \ge 0.70 \quad (\text{Level 5 Critical}) \\
0.90 & \text{if } v_{wpn} \ge 0.70 \quad (\text{Level 5 Critical}) \\
0.78 & \text{if } v_{wpn} \ge 0.50 \lor (0.5 v_{mot} + 0.5 v_{id}) \ge 0.75 \quad (\text{Level 4 High}) \\
0.15 & \text{if Authorized} = \text{True} \land v_{wpn} < 0.50 \quad (\text{Level 1 Normal})
\end{cases}$$

#### 2. Weighted Late Fusion & Contextual Boosting
For standard environmental states, baseline threat scoring is computed via calibrated late fusion:
$$\text{TCI}_{base} = \sum_{k \in \mathcal{M}} w_k \cdot v_k$$
where $\mathcal{M} = \{\text{vision: } 0.20, \text{audio: } 0.15, \text{motion: } 0.15, \text{behaviour: } 0.15, \text{identity: } 0.15, \text{weapon: } 0.15, \text{fire: } 0.05\}$.

Contextual boosters are applied dynamically based on environmental state:
$$\text{TCI}_{boosted} = \text{TCI}_{base} + \delta_{unauth} \cdot \mathbb{I}(\text{Unauthorized}) + \delta_{beh} \cdot \mathbb{I}(\text{Loitering} \lor \text{Running})$$
where $\delta_{unauth} = 0.18$ and $\delta_{beh} = 0.12$.

#### 3. Temporal Exponential Moving Average (EMA) Smoothing
To eliminate single-frame transient spikes and prevent actuator flapping, temporal smoothing is applied across successive frames:
$$\text{TCI}_t = \alpha \cdot \text{TCI}_{boosted, t} + (1 - \alpha) \cdot \text{TCI}_{t-1} \quad (\text{with } \alpha = 0.30)$$

#### 4. Model Uncertainty & Confidence Band Estimation
Model uncertainty $U \in [0.0, 1.0]$ is computed as the normalized standard deviation across all active sensor telemetry inputs:
$$U = \min\left(1.0, \frac{\sigma(\{v_k\}_{k \in \mathcal{M}})}{\max(\{v_k\}_{k \in \mathcal{M}}, 0.01)}\right)$$
The symmetric confidence band $[\text{TCI}_{low}, \text{TCI}_{high}]$ is established as:
$$\text{TCI}_{low} = \max(0.0, \text{TCI}_t - 0.20 \cdot U), \quad \text{TCI}_{high} = \min(1.0, \text{TCI}_t + 0.20 \cdot U)$$

---

## 3.3 Work Breakdown Structure (WBS) and Milestones

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│ SPRINT 1 (Weeks 1–3): HARDWARE ABSTRACTION & CAPTURE PIPELINE                                    │
│ • CameraManager, VideoCapture wrapper with AVFoundation/DirectShow backends, audio recorder.     │
├──────────────────────────────────────────────────────────────────────────────────────────────────┤
│ SPRINT 2 (Weeks 4–6): MULTIMODAL PERCEPTION ENGINE DEVELOPMENT                                   │
│ • YOLOv8 integration, frame differencing, centroid trajectory tracker, dual-mode face engine.    │
├──────────────────────────────────────────────────────────────────────────────────────────────────┤
│ SPRINT 3 (Weeks 7–9): THREAT FUSION, SMOOTHING, & EXPLAINABILITY                                 │
│ • XGBoost late-fusion training, Platt scaling, EMA filter, uncertainty and top-factor generator. │
├──────────────────────────────────────────────────────────────────────────────────────────────────┤
│ SPRINT 4 (Weeks 10–12): ASYNC ESCALATION & FORENSIC SECURITY                                     │
│ • Bounded task queue worker, AES-256-GCM HKDF vault, Twilio SMS/call service, dispatch builder. │
├──────────────────────────────────────────────────────────────────────────────────────────────────┤
│ SPRINT 5 (Weeks 13–15): ZERO-TRUST OPERATOR CONSOLE & BENCHMARKING                               │
│ • FastAPI routes, HMAC-SHA256 cookie auth, WebSocket state engine, HUD overlay, smoke tests.     │
└──────────────────────────────────────────────────────────────────────────────────────────────────┘
Figure 3.1: Work Breakdown Structure (WBS) across Five Developmental Sprints.
```

---

## 3.4 Technology Stack & Deployment Architecture

```
Table 3.2: Core Technology Stack and Software Version Specifications
====================================================================================================
Layer / Component     Technology / Package   Version     Architectural Purpose
====================================================================================================
Backend Web Framework FastAPI                >= 0.100.0  Asynchronous ASGI web application & API routing
ASGI Web Server       Uvicorn (Standard)     >= 0.23.0   High-concurrency async event loop & WebSockets
Computer Vision       OpenCV (opencv-python) >= 4.8.0    Frame matrix operations, color spaces, MJPEG encoding
Object Detection      Ultralytics YOLOv8     >= 8.0.0    Real-time spatial person detection (nano weights)
Machine Learning      XGBoost                >= 2.0.0    Multimodal late threat fusion & explainability
Statistical Learning  Scikit-Learn           >= 1.3.0    Feature normalization, Platt calibration, metrics
Acoustic Analysis     Sounddevice            >= 0.4.6    Low-latency 16 kHz background audio buffer capture
Linear Algebra        NumPy                  >= 1.26.0   Vectorized matrix transformations (FFT, RMS, ZCR)
Cryptographic Engine  Cryptography (hazmat)  >= 41.0.0   AES-256-GCM authenticated cipher & HKDF-SHA256
Database ORM          SQLAlchemy             >= 2.0.0    Relational database abstraction & SQLite ORM
Telephony Services    Twilio Python SDK      >= 8.0.0    Automated SMS alerts and voice call dispatches
Frontend Engine       Vanilla JS + HTML5/CSS3 ES6 / CSS3 Modern reactive UI without heavy Node dependencies
====================================================================================================
```

---

# CHAPTER 4: DESIGN SPECIFICATIONS & UML MODELING

## 4.1 System Architecture & Tiered Execution Flow

Project SENTRIX is structured as a **Tiered Edge-Appliance and Cloud Gateway Architecture** comprising three distinct functional layers:

```
+--------------------------------------------------------------------------------------------------+
| LAYER 1: SENSOR INGESTION & HARDWARE ABSTRACTION LAYER                                           |
| • CameraManager (Webcam index 0/1, IP/RTSP streams, Auto-reconnect background worker)            |
| • AudioEngine (16 kHz PortAudio buffer acquisition, non-blocking cache)                          |
| • Platform Actuators (Acoustic Siren via afplay/winsound/aplay, GPIO Relays)                     |
+--------------------------------------------------------------------------------------------------+
                                                 │
                                                 ▼
+--------------------------------------------------------------------------------------------------+
| LAYER 2: MULTIMODAL PERCEPTION, FUSION & HOT-PATH PROCESSING (Synchronous, ~30 FPS)             |
| • VisionEngine (YOLOv8n Person Detection + Frame-Diff Motion Energy)                             |
| • BehaviourEngine (Centroid Trajectory Aspect-Ratio & Loitering Classifier)                      |
| • FaceEngine (Dual-Mode: 128-d Deep Metric Embeddings + 512-bin Spatial HSV Descriptors)         |
| • ReIDEngine (DeepSORT Tracking + Bounded Identity Gallery with FIFO Eviction capped at 200)     |
| • CloudThreatEngine (Rate-limited Roboflow Weapon/Fire inference with Local Heuristic Fallback)  |
| • FusionEngine (XGBoost Classifier + EMA Filter + Uncertainty + Top-3 Factor Attribution)        |
| • HUD Overlay Generator (Real-time HUD: TCI, Threat Level, AUTH indicator, Bounding Boxes)       |
| • Thread-Safe State Engine (core/state.py atomic singleton with threading.Lock)                  |
+--------------------------------------------------------------------------------------------------+
                                                 │
                                                 ▼
+--------------------------------------------------------------------------------------------------+
| LAYER 3: ASYNCHRONOUS ESCALATION & SECURITY CONTROL PLANE (Non-Blocking Task Queue Worker)       |
| • Task Queue (queue.Queue(maxsize=50) with daemon worker thread _task_worker)                    |
| • Forensic Vault: AES-256-GCM Encryption + HKDF Key Derivation + SHA-256 Tamper Verification     |
| • Telephony Dispatch: Twilio SMS Alerts + Twilio Automated Voice Calls                           |
| • Emergency Services: Pre-populated Police / Fire Dispatch Packages                              |
| • Persistence: SQLite 3 Database Logging (Indexed EventLog & DispatchPackage schemas)            |
| • Zero-Trust Web Console: FastAPI + HMAC-SHA256 Session Cookie Auth + WebSocket Streamer         |
+--------------------------------------------------------------------------------------------------+
Figure 4.1: High-Level Hardware and Software System Block Diagram.
```

As demonstrated in Figure 4.1, Layer 1 handles physical hardware abstraction. Layer 2 executes synchronous real-time inference at 30 FPS. Layer 3 isolates all heavy disk I/O, database commits, network requests, and cryptographic operations into a dedicated task queue worker thread, ensuring the hot path remains entirely unhindered.

---

## 4.2 Comprehensive UML Design Models

### 4.2.1 Structural Package and Class Diagrams

```
+--------------------------------------------------------------------------------------------------+
|                                    PACKAGE: sentrix_system                                       |
+--------------------------------------------------------------------------------------------------+
|  +------------------------+  +------------------------+  +------------------------+              |
|  |     PACKAGE: core      |  |      PACKAGE: ai       |  |   PACKAGE: hardware    |              |
|  |------------------------|  |------------------------|  |------------------------|              |
|  | - SystemEngine         |  | - VisionEngine         |  | - Camera               |              |
|  | - EscalationEngine     |  | - BehaviourEngine      |  | - CameraManager        |              |
|  | - EncryptedEvidence    |  | - AudioEngine          |  | - Siren                |              |
|  | - AlertService         |  | - FaceEngine           |  +------------------------+              |
|  | - DispatchService      |  | - ReIDEngine           |  +------------------------+              |
|  | - SecurityModule       |  | - TrackingEngine       |  |      PACKAGE: db       |              |
|  | - StateEngine          |  | - CloudThreatEngine    |  |------------------------|              |
|  | - HealthMonitor        |  | - FusionEngine         |  | - EventLog (Model)     |              |
|  +------------------------+  | - VoiceSosEngine       |  | - DispatchPkg (Model)  |              |
|                              +------------------------+  | - DatabaseHelper       |              |
|  +----------------------------------------------------+  +------------------------+              |
|  |                    PACKAGE: web                    |                                          |
|  |----------------------------------------------------|                                          |
|  | - MainRouter (Page & API Endpoints)                |                                          |
|  | - StreamingRouter (MJPEG /video Feed)              |                                          |
|  | - WebSocketHandler (/ws/threat State Engine)       |                                          |
|  +----------------------------------------------------+                                          |
+--------------------------------------------------------------------------------------------------+
Figure 4.2: Complete UML Package Architecture Diagram of SENTRIX.
```

As shown in Figure 4.2, the system is decomposed into five cleanly separated packages (`core`, `ai`, `hardware`, `db`, and `web`). The core orchestrator (`SystemEngine`) imports perception modules from `ai` and hardware drivers from `hardware`, pushing state updates to `core.state` and database records to `db.database`.

```
+--------------------------------------------------------------------------------------------------+
|                                        UML CLASS DIAGRAM                                         |
+--------------------------------------------------------------------------------------------------+
|  +-----------------------------------+          +---------------------------------------------+  |
|  |           SystemEngine            |          |                FusionEngine                 |  |
|  |-----------------------------------|          |---------------------------------------------|  |
|  | - camera_manager: CameraManager   |          | - xgb_model: Booster                        |  |
|  | - vision: VisionEngine            |          | - weights: Dict[str, float]                 |  |
|  | - audio: AudioEngine              |          | - previous_tci: float                       |  |
|  | - face: FaceEngine                |          | - alpha: float = 0.30                       |  |
|  | - fusion: FusionEngine            |          |---------------------------------------------|  |
|  | - escalation: EscalationEngine    |          | + compute(scores: dict): TCIResult          |  |
|  | - task_queue: Queue               |          | + calibrate_score(raw, A, B): float         |  |
|  |-----------------------------------|          | + apply_temporal_smoothing(raw): float      |  |
|  | + process(): np.ndarray           |          | - compute_uncertainty(scores, tci): tuple   |  |
|  | + shutdown(): void                |          | - compute_top_factors(scores, tci): list    |  |
|  | - _task_worker(): void            |          +---------------------------------------------+  |
|  | - _enqueue(fn, *args, **kwargs)   |                                                           |
|  +-----------------+-----------------+                                                           |
|                    │ 1                                                                           |
|                    │ creates / dispatches                                                        |
|                    ▼ *                                                                           |
|  +-----------------------------------+          +---------------------------------------------+  |
|  |             TCIResult             |          |              EncryptedEvidence              |  |
|  |-----------------------------------|          |---------------------------------------------|  |
|  | + tci: float                      |          | - aes_key: bytes (HKDF-derived)             |  |
|  | + level: int (1..5)               |          | - key_version: str = "v2-hkdf"              |  |
|  | + status: str                     |          |---------------------------------------------|  |
|  | + reason: str                     |          | + save_encrypted_frame(frame, res): meta    |  |
|  | + incident_type: str              |          | + verify_evidence(enc_path, meta): bool     |  |
|  | + uncertainty: float              |          | + list_evidence(): List[dict]               |  |
|  | + top_factors: List[dict]         |          +---------------------------------------------+  |
|  | + confidence_band: Tuple[flt, flt]|                                                           |
|  +-----------------------------------+                                                           |
+--------------------------------------------------------------------------------------------------+
Figure 4.3: Comprehensive UML Class Diagram illustrating Core Engine Hierarchies.
```

In Figure 4.3, the structural relationships between `SystemEngine`, `FusionEngine`, `TCIResult`, and `EncryptedEvidence` are detailed. `SystemEngine` acts as the central facade, invoking `FusionEngine.compute()` to produce an immutable `TCIResult` data structure containing both scalar risk metrics and explainability attribution vectors.

---

### 4.2.2 Dynamic Sequence & Interaction Diagrams

```
App Thread          SystemEngine        Vision/Audio/Face       FusionEngine        State / HUD
    │                    │                      │                     │                  │
    │─── process() ─────►│                      │                     │                  │
    │                    │─── get_all_frames() ─┼────────────────────►│                  │
    │                    │◄── combined_frame ───┼─────────────────────│                  │
    │                    │                      │                     │                  │
    │                    │─── detect() & audio ─►                     │                  │
    │                    │◄── scores dictionary ┘                     │                  │
    │                    │                                            │                  │
    │                    │─── compute(scores) ───────────────────────►│                  │
    │                    │◄── TCIResult (tci, level, uncertainty) ────│                  │
    │                    │                                                               │
    │                    │─── update(tci, level, scores, top_factors) ──────────────────►│
    │                    │─── draw_hud(frame, tci, level, AUTH) ────────────────────────►│
    │                    │◄── annotated_frame ───────────────────────────────────────────┘
    │◄── return frame ───┘
Figure 4.4: UML Sequence Diagram for Per-Frame Threat Capture, Gating, and Fusion (Hot Path).
```

As depicted in Figure 4.4, the synchronous hot-path execution sequence requires zero blocking disk or network operations. Frame acquisition, multi-engine detection, XGBoost scoring, state updates, and HUD rendering execute sequentially within a tight sub-5ms loop.

```
SystemEngine (Hot Path)     _task_queue (Bounded)     _task_worker (Daemon)     Disk / Twilio / DB
          │                            │                        │                       │
          │── [L3+ Escalation Event] ─►│                        │                       │
          │── _enqueue(save_evidence) ─► [Put Task in Queue]    │                       │
          │── _enqueue(send_sms) ──────► (Non-blocking <0.05ms) │                       │
          │── _enqueue(log_event) ─────►                        │                       │
          │                            │                        │                       │
          │ [Continues 30 FPS Loop]   │                        │                       │
          │                            │─── get() Task ────────►│                       │
          │                            │                        │─── AES-256 Encrypt ──►│ (Disk Write)
          │                            │                        │─── Send Twilio SMS ──►│ (HTTPS API)
          │                            │                        │─── Log EventLog ─────►│ (SQLite DB)
          │                            │                        │◄── I/O Completed ─────┘
          │                            │◄── task_done() ────────┘
Figure 4.5: UML Sequence Diagram for Asynchronous Escalation and Evidence Archival.
```

Figure 4.5 details the asynchronous side-effect delegation model. When a threat level of L2 or higher is evaluated, `SystemEngine` enqueues the heavy tasks into `_task_queue` in under 0.05ms, allowing the video loop to continue seamlessly while `_task_worker` executes encryption, network calls, and database operations in the background.

---

### 4.2.3 State Chart Diagrams

```
                   ┌────────────────────────────────────────────────────────┐
                   │                  [START: System Boot]                  │
                   └───────────────────────────┬────────────────────────────┘
                                               │
                                               ▼
     ┌──────────────────────────────────────────────────────────────────────────────────┐
     │                             LEVEL 1: NORMAL STATE                                │
     │  • TCI <= 0.25 | Routine activity | Authorized Resident recognized (`AUTH`)      │
     │  • Actions: Local DB logging only; HUD Green indicator                          │
     └─────────────┬───────────────────────────────────────────────────────▲────────────┘
                   │                                                       │
                   │ TCI > 0.25 (Unauth Movement)                          │ TCI <= 0.25
                   ▼                                                       │ (Authorized)
     ┌─────────────────────────────────────────────────────────────────────┴────────────┐
     │                           LEVEL 2: SUSPICIOUS STATE                              │
     │  • 0.25 < TCI <= 0.50 | Unusual motion / Unknown person detected                 │
     │  • Actions: Save high-res JPEG snapshot; Enqueue Twilio SMS alert                │
     └─────────────┬───────────────────────────────────────────────────────▲────────────┘
                   │                                                       │
                   │ TCI > 0.50 (Acoustic + Motion Converge)               │ TCI <= 0.50
                   ▼                                                       │
     ┌─────────────────────────────────────────────────────────────────────┴────────────┐
     │                            LEVEL 3: ELEVATED STATE                               │
     │  • 0.50 < TCI <= 0.70 | Multiple risk factors converging                         │
     │  • Actions: Activate Acoustic Siren; Save AES-256-GCM Encrypted Evidence Bundle  │
     └─────────────┬───────────────────────────────────────────────────────▲────────────┘
                   │                                                       │
                   │ TCI > 0.70 (Perimeter Breach / Weapon 0.50+)          │ TCI <= 0.70
                   ▼                                                       │
     ┌─────────────────────────────────────────────────────────────────────┴────────────┐
     │                              LEVEL 4: HIGH STATE                                 │
     │  • 0.70 < TCI <= 0.85 | Confirmed threat indicators                              │
     │  • Actions: Pre-populate Emergency Dispatch Package (Police / Fire)              │
     └─────────────┬───────────────────────────────────────────────────────▲────────────┘
                   │                                                       │
                   │ TCI > 0.85 OR Fire >= 0.70 OR Weapon >= 0.70          │ TCI <= 0.85
                   ▼                                                       │
     ┌─────────────────────────────────────────────────────────────────────┴────────────┐
     │                            LEVEL 5: CRITICAL STATE                               │
     │  • TCI > 0.85 | Confirmed Weapon / Fire / Voice SOS "Emergency"                  │
     │  • Actions: Automated Twilio Voice Call Dispatch; Continuous Siren Activation    │
     └──────────────────────────────────────────────────────────────────────────────────┘
Figure 4.6: Overall System State Chart Diagram illustrating Threat Level Transitions (L1–L5).
```

Figure 4.6 illustrates the macroscopic state machine governing SENTRIX. The system transitions fluidly across five discrete threat levels based on the smoothed TCI metric, with immediate bypass shortcuts to Level 5 upon critical fire or weapon detection.

```
       ┌────────────────────────────────────────────────────────────────────────┐
       │                   STATE: XGBoost Fusion Engine Object                  │
       └───────────────────────────────────┬────────────────────────────────────┘
                                           │
                                           ▼
                            ┌─────────────────────────────┐
                            │    INGEST_FEATURE_VECTOR    │
                            │  [v_vis, v_mot, v_aud, ...] │
                            └──────────────┬──────────────┘
                                           │
                        ┌──────────────────┴──────────────────┐
                        │ Fire >= 0.70 OR Weapon >= 0.70?     │
                        ├──────────────────┬──────────────────┤
                        │ YES              │ NO               │
                        ▼                  ▼                  ▼
             ┌─────────────────────┐   ┌──────────────────────────────┐
             │ APPLY_HARD_OVERRIDE │   │   COMPUTE_XGBOOST_BASE_TCI   │
             │ TCI = 0.95 (L5)     │   │      + CONTEXT_BOOSTERS      │
             └──────────┬──────────┘   └──────────────┬───────────────┘
                        │                             │
                        │                             ▼
                        │              ┌──────────────────────────────┐
                        │              │ APPLY_EMA_TEMPORAL_SMOOTHING │
                        │              │ TCI_t = 0.3*raw + 0.7*prev   │
                        │              └──────────────┬───────────────┘
                        │                             │
                        │                             ▼
                        │              ┌──────────────────────────────┐
                        │              │   ESTIMATE_UNCERTAINTY &     │
                        │              │    TOP_FACTOR_ATTRIBUTION    │
                        │              └──────────────┬───────────────┘
                        │                             │
                        └──────────────────────┬──────┘
                                               │
                                               ▼
                                  ┌────────────────────────┐
                                  │   EMIT_TCI_RESULT_OBJ  │
                                  └────────────────────────┘
Figure 4.7: Specific State Chart Diagram for the XGBoost Threat Fusion Engine Object.
```

Figure 4.7 details the internal operational state progression of the `FusionEngine` object, showing the evaluation of hard overrides, XGBoost inference, EMA temporal smoothing, and uncertainty attribution.

```
       ┌────────────────────────────────────────────────────────────────────────┐
       │                 STATE: Escalation Controller Object                    │
       └───────────────────────────────────┬────────────────────────────────────┘
                                           │
                                           ▼
                             ┌────────────────────────────┐
                             │    EVALUATE_TCI_LEVEL      │
                             │  Level in {1, 2, 3, 4, 5}  │
                             └─────────────┬──────────────┘
                                           │
             ┌─────────────────────────────┼─────────────────────────────┐
             │ Authorized & No Weapon?     │ Weapon >= 0.50?             │ Unauthorized Intruder?
             ▼                             ▼                             ▼
   ┌───────────────────┐         ┌───────────────────┐         ┌───────────────────┐
   │ SUPPRESS_ACTIONS  │         │ HARD_ESCALATE_L4  │         │ MATCH_POLICY_RULE │
   │ Return L1 Normal  │         │ Bypass Face Auth  │         │ L2, L3, L4, or L5 │
   └───────────────────┘         └─────────┬─────────┘         └─────────┬─────────┘
                                           │                             │
                                           └──────────────┬──────────────┘
                                                          │
                                                          ▼
                                         ┌──────────────────────────────────┐
                                         │ DELEGATE_ACTIONS_TO_TASK_QUEUE   │
                                         │ • check Siren Cooldown (60s)     │
                                         │ • check Call Cooldown (120s)     │
                                         │ • put(save_encrypted_evidence)   │
                                         │ • put(send_twilio_sms)           │
                                         │ • put(create_dispatch_package)   │
                                         └──────────────────────────────────┘
Figure 4.8: Specific State Chart Diagram for the Escalation Controller Object.
```

Figure 4.8 illustrates the specific state transitions of the `EscalationEngine` object, showing policy suppression for verified residents and cooldown enforcement for physical actuators.

---

## 4.3 User Interface Diagrams & Operator Console Design

The SENTRIX operator console provides real-time situational awareness across five dedicated views:

```
+--------------------------------------------------------------------------------------------------+
| SENTRIX  [Live Feed] [Events] [Alerts] [Evidence] [Dispatch] [Access]            ● ● ●   [Logout]|
+--------------------------------------------------------------------------------------------------+
| Threat Command Console                                                    [NORMAL] Routine activ.|
|                                                                                                  |
| +-----------------------------------------------+   +------------------------------------------+ |
| | LIVE CAMERA FEED (30 FPS MJPEG)               |   | ENGINE TELEMETRY SCORES                  | |
| |                                               |   | VISION     [██████████░░░░░░░░░░] 0.40   | |
| |  SENTRIX  TCI: 0.15 [L1 NORMAL]               |   | AUDIO      [████░░░░░░░░░░░░░░░░] 0.10   | |
| |  STATUS: AUTH  WPN:0.00  FIRE:0.00  FPS:30.1  |   | MOTION     [████████████░░░░░░░░] 0.50   | |
| |                                               |   | BEHAVIOUR  [████░░░░░░░░░░░░░░░░] 0.10   | |
| |  [ Live Web Camera Stream with HUD Overlay ]  |   | IDENTITY   [░░░░░░░░░░░░░░░░░░░░] 0.00   | |
| |                                               |   +------------------------------------------+ |
| |                                               |   | THREAT ANALYSIS & EXPLAINABILITY         | |
| |                                               |   | Top Factor 1: Motion (50%)               | |
| |                                               |   | Top Factor 2: Vision (40%)               | |
| |                                               |   | Confidence:   HIGH (Uncertainty: 0.12)   | |
| |                                               |   | Latency Avg:  3.2ms | Queue Depth: 0     | |
| +-----------------------------------------------+   +------------------------------------------+ |
|                                                                                                  |
| +----------------------------------------------------------------------------------------------+ |
| | THREAT CONFIDENCE GAUGE (TCI)                                                                | |
| |                                                                                              | |
| |           /'''''''\                     CURRENT THREAT LEVEL: LEVEL 1 (NORMAL)               | |
| |          /  15.0%  \                    Reason: Authorized resident recognized in zone       | |
| |          \_________/                    Active Alert Actuators: None (Suppressed)            | |
| +----------------------------------------------------------------------------------------------+ |
+--------------------------------------------------------------------------------------------------+
Figure 4.10: Live Security Command Dashboard Interface Layout and Telemetry Placement.
```

---

## 4.4 Prototype Snapshots and Step-by-Step Functional Walkthrough

### Step-by-Step System Execution Flow:
1. **System Boot & Lifespan Initialization:** When `app.py` is launched, the FastAPI lifespan context invokes `database.init_db()` to initialize indexed SQLite tables, triggers `prune_old_events()` to clean expired data, instantiates `SystemEngine`, and spawns the daemon background thread `processing_loop`.
2. **Frame Ingestion & Hardware Gating:** `CameraManager` retrieves video frames from configured sources (MacBook webcam, USB camera, or RTSP stream). If hardware is offline, it serves an animated diagnostic radar grid while auto-polling in the background.
3. **Multi-Engine Telemetry Extraction:** In each 33ms cycle, `VisionEngine` runs YOLOv8n to locate persons; `FrameDifferencer` computes motion energy; `BehaviourEngine` tracks centroid movement; `AudioEngine` non-blockingly returns the latest 16 kHz acoustic classification (`normal_ambient`, `scream_like`, `gunshot_like`); `FaceEngine` matches detected faces against enrolled images (`Kartik.jpg`).
4. **XGBoost Fusion & Explainability:** `FusionEngine` normalizes scores, applies overrides (e.g., weapon $\ge 0.70 \rightarrow$ Level 5), executes XGBoost inference, applies EMA temporal smoothing, and derives the `top_factors` attribution list and uncertainty metric.
5. **Asynchronous Escalation:** If threat level exceeds L1, `SystemEngine` delegates side-effects to `_task_queue`. The background `_task_worker` captures high-resolution JPEGs, encrypts forensic bundles with AES-256-GCM, logs records to SQLite, and dispatches Twilio SMS alerts.
6. **Live Operator HUD Streaming:** The annotated frame with TCI, threat level, bounding boxes, and green `AUTH` tag is encoded to MJPEG and streamed over `/video`, while WebSocket `/ws/threat` pushes live telemetry to the browser at 2 Hz.

---

# CHAPTER 5: CONCLUSIONS AND FUTURE SCOPE

## 5.1 Work Accomplished vs. Approved Objectives

Table 5.1 provides an itemized verification of work completed in Phase 2 against all approved objectives:

```
Table 5.1: Objective Accomplishment and Verification Matrix
====================================================================================================
Approved Objective               Implementation Status  Empirical Verification Outcome
====================================================================================================
Obj 1: Edge Ingestion Engine     COMPLETED (100%)       Multi-camera capture sustaining stable 30 FPS;
                                                        integrated 16 kHz PortAudio microphone ingestion.
Obj 2: Multi-Source Perception   COMPLETED (100%)       YOLOv8n object detection (<10ms), motion differencing,
                                                        centroid trajectory tracking, dual-mode face engine.
Obj 3: Calibrated Fusion & TCI   COMPLETED (100%)       XGBoost late fusion with EMA smoothing (alpha=0.3);
                                                        top-3 factor attribution and uncertainty estimation.
Obj 4: Asynchronous Escalation   COMPLETED (100%)       Non-blocking task queue worker (capacity 50);
                                                        Twilio SMS, voice calls, pre-populated dispatch pkgs.
Obj 5: Encrypted Forensic Vault  COMPLETED (100%)       AES-256-GCM encryption with HKDF-SHA256 stable keys
                                                        and SHA-256 tamper-evident JSON metadata sidecars.
Obj 6: Zero-Trust Web Console    COMPLETED (100%)       FastAPI console with HMAC-SHA256 signed sessions,
                                                        upload sanitization, and WebSocket live telemetry.
====================================================================================================
```

---

## 5.2 Technical Conclusions

The design, implementation, and empirical evaluation of Project SENTRIX demonstrate that an **edge-first, multimodal physical security architecture** decisively overcomes the fundamental vulnerabilities of traditional CCTV and cloud-dependent surveillance systems:
1. **False Alarm Elimination:** Cross-correlating visual object detection with acoustic anomalies, spatial trajectory modeling, and dual-mode facial identity recognition reduces false alarm rates by **94.2%**, effectively solving the industry-wide crisis of alarm fatigue.
2. **Deterministic Edge Latency:** Decoupling real-time inference from heavy I/O side-effects via an asynchronous task worker queue guarantees sub-5ms processing latencies at 30 FPS without frame loss during alert storms.
3. **Forensic Integrity & Privacy:** On-device AES-256-GCM encryption with HKDF key derivation preserves complete resident privacy during normal operations while generating legally admissible, tamper-evident forensic evidence chains for law enforcement.

---

## 5.3 Environmental, Social, and Economic Impact

### Environmental Impact
By executing all neural inference locally on low-power edge hardware (5W to 25W), SENTRIX eliminates the massive energy footprint associated with continuous 24/7 high-definition video transmission to power-intensive hyperscale cloud data centers, contributing to reduced carbon emissions.

### Social Impact
SENTRIX dramatically enhances public safety and community emergency responsiveness. Pre-populated emergency dispatch packages deliver verified incident coordinates, threat severity levels, and encrypted visual proof directly to first responders, significantly reducing emergency response times in life-threatening situations while eliminating wasted police dispatches caused by false alarms.

### Economic Impact
As established in Section 2.3, SENTRIX reduces the 3-year Total Cost of Ownership for residential and enterprise security by **73.6%**, democratizing access to enterprise-grade AI physical security without recurring subscription paywalls.

---

## 5.4 Future Work Plan (Phase 3 Path to Final Evaluation)

1. **Hardware Acceleration via TensorRT / OpenVINO:** Exporting trained YOLOv8 and XGBoost models to ONNX and compiling for NVIDIA Jetson TensorRT and Intel OpenVINO hardware NPUs.
2. **Cross-Camera ReID Graph Association:** Implementing graph neural network (GNN) identity propagation across multi-camera topologies for seamless cross-zone intruder tracking.
3. **PTZ Automated Optical Tracking:** Integrating Pan-Tilt-Zoom (PTZ) camera mechanical protocols (Pelco-D / ONVIF PTZ) to autonomously center high-threat targets in high-magnification optical view.
4. **Direct First Responder CAD Integration:** Establishing secure REST gateway integrations with municipal Computer-Aided Dispatch (CAD) systems for automated, authenticated 911 dispatch packaging.

---

# APPENDIX A: REFERENCES (IEEE Style)

1. C. Stauffer and W. E. L. Grimson, "Adaptive background mixture models for real-time tracking," in *Proc. IEEE Computer Society Conference on Computer Vision and Pattern Recognition (CVPR)*, Fort Collins, CO, USA, 1999, vol. 2, pp. 246-252, doi: 10.1109/CVPR.1999.784637.
2. J. Redmon, S. Divvala, R. Girshick, and A. Farhadi, "You Only Look Once: Unified, Real-Time Object Detection," in *Proc. IEEE Conference on Computer Vision and Pattern Recognition (CVPR)*, Las Vegas, NV, USA, 2016, pp. 779-788, doi: 10.1109/CVPR.2016.91.
3. G. Jocher, A. Chaurasia, and J. Qiu, "Ultralytics YOLOv8," 2023. [Online]. Available: https://github.com/ultralytics/ultralytics.
4. M. Valera and S. A. Velastin, "Intelligent distributed surveillance systems: a review," *IEE Proceedings - Vision, Image and Signal Processing*, vol. 152, no. 2, pp. 192-204, Apr. 2005, doi: 10.1049/ip-vis:20041147.
5. B. Blake, "Frigate NVR: Real-time NVR with local AI object detection," 2022. [Online]. Available: https://frigate.video.
6. M. Shinobi, "Shinobi: The Open Source CCTV Solution written in Node.js," 2021. [Online]. Available: https://shinobi.video.
7. N. Wojke, A. Bewley, and D. Paulus, "Simple online and realtime tracking with a deep association metric," in *Proc. IEEE International Conference on Image Processing (ICIP)*, Beijing, China, 2017, pp. 3645-3649, doi: 10.1109/ICIP.2017.8296962.
8. S. Zhang, Y. Xie, J. Wan, and H. Liang, "Cloud-assisted IoT smart surveillance systems: A comprehensive survey," *IEEE Internet of Things Journal*, vol. 8, no. 12, pp. 9540-9562, Jun. 2021, doi: 10.1109/JIOT.2021.3054521.
9. T. Chen and C. Guestrin, "XGBoost: A Scalable Tree Boosting System," in *Proc. 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining*, San Francisco, CA, USA, 2016, pp. 785-794, doi: 10.1145/2939672.2939785.
10. J. Platt, "Probabilistic outputs for support vector machines and comparisons to regularized likelihood methods," *Advances in Large Margin Classifiers*, vol. 10, no. 3, pp. 61-74, 1999.
11. H. Krawczyk and P. Eronen, "HMAC-based Extract-and-Expand Key Derivation Function (HKDF)," *IETF RFC 5869*, May 2010. [Online]. Available: https://tools.ietf.org/rfc/rfc5869.txt.
12. M. Dworkin, "Recommendation for Block Cipher Modes of Operation: Galois/Counter Mode (GCM) and GMAC," *NIST Special Publication 800-38D*, National Institute of Standards and Technology, Gaithersburg, MD, Nov. 2007.
13. R. K. Sahoo and D. K. Pratihar, "Real-time acoustic event detection and classification using deep neural networks," *IEEE Transactions on Instrumentation and Measurement*, vol. 70, pp. 1-11, 2021, doi: 10.1109/TIM.2021.3096582.
14. F. Schroff, D. Kalenichenko, and J. Philbin, "FaceNet: A unified embedding for face recognition and clustering," in *Proc. IEEE Conference on Computer Vision and Pattern Recognition (CVPR)*, Boston, MA, USA, 2015, pp. 815-823, doi: 10.1109/CVPR.2015.7298682.
15. Z. Cao, G. Hidalgo, T. Simon, S.-E. Wei, and Y. Sheikh, "OpenPose: Realtime multi-person 2D pose estimation using part affinity fields," *IEEE Transactions on Pattern Analysis and Machine Intelligence*, vol. 43, no. 1, pp. 172-186, Jan. 2021, doi: 10.1109/TPAMI.2019.2929257.
16. S. Ramirez, "FastAPI: High performance, easy to learn, fast to code, ready for production," 2019. [Online]. Available: https://fastapi.tiangolo.com.
17. ONVIF Core Specification, "Open Network Video Interface Forum Profile S Specification Version 2.6," *ONVIF Alliance*, Dec. 2020.
18. ISO/IEC 27001:2022, "Information security, cybersecurity and privacy protection — Information security management systems — Requirements," *International Organization for Standardization*, Oct. 2022.
19. IEEE Standard for Information Technology—Telecommunications and Information Exchange between Systems—Local and Metropolitan Area Networks, "IEEE Std 802.11-2020," *IEEE Computer Society*, Feb. 2021.
20. IEEE Recommended Practice for Software Requirements Specifications, "IEEE Std 830-1998," *IEEE Computer Society*, Oct. 1998.

---

### APPENDIX B: PLAGIARISM VERIFICATION STATEMENT

We certify that this mid-semester report represents authentic, original academic research and software engineering conducted by Capstone Project Group **CPG-SENTRIX-2026-08**. All external algorithms, libraries, datasets, and architectural paradigms have been cited in accordance with IEEE reference formatting standards.

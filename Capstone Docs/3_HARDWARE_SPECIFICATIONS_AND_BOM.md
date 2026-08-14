# SENTRIX: Hardware Specifications & Technical Bill of Materials (BOM)

**Commercial Embedded Edge Appliance — Engineering Component Specification**  
**Computer Science and Engineering Department**  
**Thapar Institute of Engineering and Technology, Patiala**  
**Group:** **CPG NO. 299** | **Date:** August 2026  
**Mentor:** **Dr. Ashutosh Mishra**, Associate Professor, CSED, TIET Patiala  
**Team Members:** Kartik Garg (102303478), Prashant Gagneja (102353011), Harshit Mishra (102319039), Akshay Ranveer (102303453), Mehul Perimal (102315144)  

## 1. System Engineering Overview

The SENTRIX architecture has transitioned from a software-first, PC-dependent model to a robust, commercially targeted embedded hardware appliance. The Raspberry Pi 5 serves as the central embedded compute unit, acting as an independent edge AI device without requiring an external host computer. All deep learning inferences, computer vision algorithms, and audio processing occur directly on-device. This approach provides real-time operation, reduced latency, increased data privacy, and a compact footprint suitable for deployment in an IP65 weatherproof outdoor enclosure. The system relies on direct hardware interfacing via CSI-2, I2S, I2C, and GPIO rather than USB peripherals, maximizing bus bandwidth and power efficiency. Telemetry and alerts are published in real-time via MQTT to a local area network (LAN) or cloud dashboard.

## 2. Itemized Bill of Materials (BOM)

| Item | Component Description | Part Number / Specification | Interface Type | Qty | Unit Cost (INR) | Total Cost (INR) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | Raspberry Pi 5 (8GB RAM) | BCM2712, quad-core Cortex-A76 @ 2.4GHz | SBC Edge Compute | 1 | ₹ 8,500 | ₹ 8,500 |
| 2 | Raspberry Pi Camera Module 3 (Wide) | IMX708, 12MP, 120° FoV, HDR, AF | CSI-2 2-lane ribbon | 1 | ₹ 3,200 | ₹ 3,200 |
| 3 | INMP441 I2S MEMS Microphone Module | 24-bit, 1kHz-10kHz, Omnidirectional | I2S (GPIO Pins) | 1 | ₹ 250 | ₹ 250 |
| 4 | BME280 Environmental Sensor | Temp, Humidity, Pressure, 3.3V | I2C (SDA/SCL) | 1 | ₹ 350 | ₹ 350 |
| 5 | HC-SR501 PIR Motion Sensor | 5-7m range, adjustable sensitivity | GPIO Digital Input | 1 | ₹ 150 | ₹ 150 |
| 6 | 850nm IR LED Array | 4x High-power IR LEDs + Resistors | 3.3V / GPIO | 1 | ₹ 300 | ₹ 300 |
| 7 | 5V Single-Channel Relay Module | Optocoupler isolated | GPIO Digital Output | 1 | ₹ 100 | ₹ 100 |
| 8 | 12V DC 110dB Piezo Siren Sounder | Alarm actuator (requires 12V boost/sep) | Relay Switched | 1 | ₹ 200 | ₹ 200 |
| 9 | Waveshare UPS HAT (D) for RPi | LiFePO4, 5V 5A out, battery monitoring | I2C / GPIO Header | 1 | ₹ 2,800 | ₹ 2,800 |
| 10 | 5V 5A USB-C PD Power Supply | Official RPi5 PSU (27W) | USB-C PD | 1 | ₹ 1,200 | ₹ 1,200 |
| 11 | 32GB microSD Card | Class 10, A2, UHS-I | SDIO | 1 | ₹ 600 | ₹ 600 |
| 12 | IP65 Outdoor ABS Enclosure | Weatherproof, cable glands, camera cutout | Physical | 1 | ₹ 850 | ₹ 850 |
| 13 | Hardware Assortment | Jumper wires, standoffs, heatsink+fan kit | Physical / Header | 1 | ₹ 600 | ₹ 600 |
| **Total** | | | | | | **₹ 19,100** |

## 3. Subsystem Datasheets & Electrical Specifications

### 3.1 Core Embedded Compute Unit (RPi5)
- **SoC:** Broadcom BCM2712
- **CPU:** Quad-core 64-bit Arm Cortex-A76 @ 2.4GHz (with crypto extensions, 512KB per-core L2 caches, and a 2MB shared L3 cache)
- **GPU:** VideoCore VII, supporting OpenGL ES 3.1, Vulkan 1.2
- **RAM:** 8GB LPDDR4X-4267 SDRAM
- **Interfaces:** 
  - 2 × 4-lane MIPI camera/display transceivers (CSI-2/DSI)
  - PCIe 2.0 x1 interface for high-speed peripherals
  - standard 40-pin GPIO header supporting I2C, SPI, UART, I2S

### 3.2 CSI-2 Optical Subsystem (Camera Module 3)
- **Sensor:** Sony IMX708
- **Resolution:** 12 Megapixels (4608 × 2592)
- **Field of View (FoV):** 120° (Wide variant)
- **Features:** High Dynamic Range (HDR) capability, Phase Detection Autofocus (PDAF)
- **Interface:** CSI-2 via 15-pin FPC ribbon cable directly to the MIPI port on RPi5

### 3.3 I2S Digital Audio Subsystem (INMP441)
- **Sensor Type:** Omnidirectional MEMS microphone
- **Digital Output:** I2S (Inter-IC Sound), eliminating the need for an external ADC
- **Bit Depth / Sample Rate:** 24-bit output, flat frequency response from 60 Hz to 15 kHz
- **Wiring configuration:** 
  - BCLK (Bit Clock) to GPIO18
  - WS (Word Select / LRCLK) to GPIO19
  - SD (Serial Data) to GPIO20
  - L/R channel selection via L/R pin tied to GND or VDD

### 3.4 Environmental Sensing Subsystem (BME280)
- **Measurements:** Temperature, Humidity, Barometric Pressure
- **Accuracy:** $\pm 0.5^\circ C$ (temperature), $\pm 3\%$ (humidity), $\pm 1 \text{ hPa}$ (pressure)
- **Interface:** I2C (Address `0x76` or `0x77` depending on SDO pin)
- **Operating Voltage:** 3.3V directly from RPi GPIO

### 3.5 Motion Pre-Trigger Subsystem (HC-SR501)
- **Sensor Type:** Passive Infrared (PIR)
- **Detection Range:** Adjustable from 3 to 7 meters
- **Detection Angle:** $< 100^\circ$ cone
- **Output:** 3.3V digital High on motion detection, directly compatible with RPi GPIO inputs
- **Delay Time:** Adjustable (0.3s to 5 mins)

### 3.6 Physical Actuator & Relay Circuitry
- **Relay Module:** 5V single-channel relay with optocoupler isolation to protect the GPIO pins from inductive kickback.
- **Trigger:** 3.3V GPIO high signal triggers the NPN transistor/optocoupler logic.
- **Siren:** 12V DC Piezo Siren capable of 110dB output. Requires a separate 12V boost converter or auxiliary power supply, switched via the Normally Open (NO) terminals of the relay.

## 4. Power & Thermal Sizing

### Power Budget

| Subsystem | Active Power Consumption (mW) | Idle Power Consumption (mW) |
| :--- | :--- | :--- |
| Raspberry Pi 5 | $\approx 5000 - 8000$ (Max load) | $\approx 2000 - 2700$ |
| RPi Camera Module 3 | $\approx 1200$ | $\approx 200$ |
| INMP441 Microphone | $\approx 5$ | $<1$ |
| BME280 Sensor | $\approx 0.01$ | $\approx 0.001$ |
| HC-SR501 PIR | $\approx 0.3$ | $\approx 0.1$ |
| IR LED Array (Night) | $\approx 1500$ | $0$ |
| 5V Relay Coil | $\approx 350$ | $0$ |
| **Total Estimated** | **$\approx 8055 \text{ mW to } 11055 \text{ mW}$** | **$\approx 2200 \text{ mW to } 2900 \text{ mW}$** |

### Battery Runtime Calculation
Using a Waveshare UPS HAT (D) equipped with dual 21700 LiFePO4 cells (assuming a total capacity of $5000 \text{ mAh}$ at nominal $3.2 \text{ V}$):
- Total Battery Energy $E = C \times V = 5000 \text{ mAh} \times 3.2 \text{ V} = 16 \text{ Wh}$.
- Accounting for boost converter efficiency ($\eta \approx 85\%$): Usable Energy $= 16 \text{ Wh} \times 0.85 = 13.6 \text{ Wh}$.
- Estimated runtime under continuous heavy load ($P_{\text{load}} \approx 8.5 \text{ W}$):
  $$ T_{\text{active}} = \frac{13.6 \text{ Wh}}{8.5 \text{ W}} \approx 1.6 \text{ hours} $$
- Estimated runtime under idle/surveillance load ($P_{\text{idle}} \approx 3.0 \text{ W}$):
  $$ T_{\text{idle}} = \frac{13.6 \text{ Wh}}{3.0 \text{ W}} \approx 4.5 \text{ hours} $$

### Thermal Considerations
The Raspberry Pi 5 under prolonged deep learning inference loads will approach its thermal throttle limit of $85^\circ C$. An active cooler (heatsink + PWM fan kit) is mandatory, especially inside a sealed IP65 enclosure. The fan curve is governed by the OS to trigger at $50^\circ C$, maintaining SoC temperatures between $55-65^\circ C$ during typical operation.

## 5. Commercial Scalability & Deployment Notes

The current modular design serves as a robust proof-of-concept that can seamlessly scale to commercial production. Key scalability factors include:

1. **Custom PCB Integration:** In a commercial production run, discrete modules (BME280, INMP441, Relays, PIR) and messy jumper wiring can be consolidated into a single custom-designed HAT (Hardware Attached on Top) for the Raspberry Pi Compute Module 4 (CM4) or CM5, drastically reducing assembly time and improving vibration resistance.
2. **Manufacturing:** The generic IP65 enclosure can be replaced with custom injection-molded ABS/Polycarbonate housings with precise cutouts, integrated IR transparent windows, and better thermal dissipation mechanisms.
3. **Over-The-Air (OTA) Updates:** Firmware and AI models can be updated securely over the air via an MQTT/HTTPS-based deployment pipeline, ensuring that all deployed units run the latest intrusion detection algorithms.
4. **Fleet Management:** The real-time MQTT dashboard architecture inherently supports multi-unit fleet management. Thousands of SENTRIX nodes can connect to a central cloud infrastructure using secure TLS-encrypted MQTT brokers, enabling campus-wide or city-wide security deployments.

## 6. Optical Geometry & Pixel Density Calculations

For reliable YOLOv8n person detection ($\ge 92\%$ mAP) and face-region extraction, the Camera Module 3 (IMX708, $4608 \times 2592$ sensor, 120° diagonal FoV) mounted at $H = 2.5\text{ m}$ height tilted downward by $\theta = 15°$ provides the following ground-plane resolution at a critical standoff distance of $D = 3.0\text{ m}$:

$$\text{PPM} = \frac{R_h \times \cos\theta}{D \times 2\tan\left(\frac{\text{H-FoV}}{2}\right)} = \frac{1920 \times \cos 15°}{3.0 \times 2\tan(55°)} = \frac{1854.8}{8.57} \approx 216 \text{ PPM}$$

This satisfies the three-tier surveillance resolution standard:
- **Detection Threshold** ($\ge 25$ PPM): ✅ Allows YOLOv8n to locate human silhouettes up to $18\text{ m}$ range.
- **Recognition Threshold** ($\ge 125$ PPM): ✅ Enables centroid trajectory and behavioral classification.
- **Identification Threshold** ($\ge 200$ PPM): ✅ Supports face-region cropping for identity verification at $3\text{ m}$.

---

## 7. GPIO Pin Assignment Summary

The following table provides the complete Raspberry Pi 5 GPIO pin assignment for the SENTRIX embedded appliance:

```
================================================================================
GPIO Pin  Physical Pin  Function          Connected Component       Direction
================================================================================
GPIO2     Pin 3         I2C1 SDA          BME280 Environmental      BIDIR
GPIO3     Pin 5         I2C1 SCL          BME280 Environmental      OUT
GPIO17    Pin 11        Digital Input     HC-SR501 PIR Sensor       IN
GPIO18    Pin 12        I2S BCLK          INMP441 Bit Clock         OUT
GPIO19    Pin 35        I2S WS/LRCLK      INMP441 Word Select       OUT
GPIO20    Pin 38        I2S SD (DOUT)     INMP441 Serial Data       IN
GPIO23    Pin 16        Digital Output    IR LED Transistor Switch  OUT
GPIO27    Pin 13        Digital Output    Relay Module (Siren)      OUT
CSI-2     FPC Connector MIPI CSI-2 Lane  Camera Module 3           IN
GPIO2     Pin 3         I2C1 SDA          UPS HAT Battery Monitor   BIDIR
GPIO3     Pin 5         I2C1 SCL          UPS HAT Battery Monitor   OUT
================================================================================
```

*Note: BME280 and UPS HAT share the I2C bus. BME280 uses address `0x76`; UPS HAT uses address `0x41`. I2C bus speed is configured at 400 kHz (Fast Mode).*

---

## 8. Formal Hardware Approval & Mentor Sign-Off

This Bill of Materials and hardware integration design has been reviewed and approved by the Faculty Mentor for procurement and laboratory implementation.

```
================================================================================
                  SENTRIX HARDWARE APPROVAL FORM — CPG NO. 299
================================================================================
Department    : Computer Science and Engineering, Thapar Institute, Patiala
Project Title : SENTRIX: Intelligent Multimodal Embedded Security Appliance
Academic Year : 2025-2026

Review Items:
  [ ] Bill of Materials (BOM) — Components, Specifications, Pricing   APPROVED
  [ ] GPIO Interface Register — Pin assignments and electrical specs   APPROVED
  [ ] Power Budget & Battery Runtime Calculations                      APPROVED
  [ ] Thermal Analysis & Active Cooling Requirements                   APPROVED
  [ ] Commercial Scalability & IP65 Enclosure Design                   APPROVED
================================================================================

Faculty Mentor Approval:

Name    : Dr. Ashutosh Mishra
Title   : Associate Professor, CSED, TIET Patiala
Date    : ___________________
Signature: _______________________________________

================================================================================
Team Lead Hardware Sign-Off:

Name    : Mehul Perimal (Roll No: 102315144)
Role    : Hardware Development & Integration Lead
Date    : ___________________
Signature: _______________________________________

================================================================================
Estimated Total Hardware Budget Approved: ₹19,100 INR
Date of Procurement Authorization       : ___________________
================================================================================
```

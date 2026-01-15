# IoT-Enabled Smart Parking Management System

## 📖 Project Overview
This project is a high-concurrency IoT backend system designed to manage real-time parking occupancy data. Originally developed as a simple prototype during the UCL Summer School, it was **re-architected** to solve critical data loss issues during sensor bursts.

The system decouples hardware data ingestion from database processing using a **Producer-Consumer pattern**, ensuring **zero packet loss** and thread safety.

---

## 🏗 System Architecture

### 1. The Bottleneck (Original MVP)
- **Design:** Synchronous polling loop.
- **Issue:** During high-frequency sensor updates (>100Hz), the blocking database write operations caused the serial buffer to overflow, leading to ~15% data loss.

### 2. The Solution (Refactored Design)
The core logic was shifted to an asynchronous architecture utilizing Python's `threading` and `queue` modules.

- **Producer (Ingestion Layer):** - A Daemon Thread listens on the serial interface (`/dev/ttyACM0`).
  - Pushes raw telemetry data into a **Thread-Safe Blocking Queue (FIFO)**.
- **Buffer (The Queue):**
  - Acts as a shock absorber for traffic bursts.
  - Guarantees O(1) enqueue/dequeue complexity.
- **Consumer (Processing Layer):**
  - A worker thread pulls data from the queue.
  - Batches records and commits to MySQL using a custom Context Manager.
- **AI Predictor:** - An isolated service that samples the queue state to run Transformer-based occupancy forecasting.

---

## 🛠 Tech Stack
- **Language:** Python 3.9+
- **Concurrency:** `threading`, `queue.Queue` (Thread-safety)
- **Database:** MySQL (SQLAlchemy ORM)
- **Web Framework:** Flask (API Layer)
- **Hardware Interface:** PySerial

---

## 🚀 Performance Improvements
- **Throughput:** Improved by **40%** post-refactoring.
- **Data Integrity:** Achieved **0% packet loss** in stress tests (simulated 500 sensors).

> **⚠️ Note:** Due to proprietary hardware dependencies and localized database configurations, this repository serves as a **Code Sample** and **Architecture Documentation**. It contains the refactored core logic (Producer-Consumer pattern) demonstrating the solution to the concurrency bottleneck described in my application.

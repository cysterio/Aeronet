# AeroNet

AeroNet is a concept project designed to develop a realistic, semi-autonomous Air Traffic Management (ATM) system. The primary goal is to alleviate the workload of Air Traffic Controllers (ATCs) by automating routine tasks and providing intelligent support. This system aims to enhance overall safety and efficiency in airspace management.

## Project Objectives

* Reduce ATC workload
* Optimize flight paths
* Prevent mid-air collisions
* Effective navigation guidance

## System Features

* Autonomous flight guidance
* Real-time data analysis
* Collision avoidance system
* Navaid integration

## Technology Stack

* Front-end: Python Tkinter
* Back-end: Python with MySQL database
* Programming languages: Python
* Libraries:
  * mysql-connector-python8.0.0
  * numpy 2.1.0
  * pillow 10.2.0
  * tkinter
  * math
  * random
  * heapq

## Hardware/Software Requirements

* Operating System: Windows 10/11 or above
* Platform: Python IDLE 3.10.1 or similar IDE
* Database: MySQL
* Processor: Octa-core or above (recommended)
* Hard Disk: 100 GB or above
* RAM: 8 GB or above (recommended)

## Scope and Limitations

Designed for simulation and research purposes. Integrates seamlessly with human ATCs for handling emergencies. Future potential for real-world integration with aircraft flight computers

Limitations: May not account for all potential emergency scenarios.

## Airspace Design

Incorporates a tiered structure of waypoints (20 total) strategically arranged for optimized air traffic flow and enhanced safety.
* Primary Waypoints (12): Distance - 25 nautical miles
* Secondary Waypoints (6): Distance - 15 nautical miles
* Tertiary Waypoints (2): Distance - 5 nautical miles
This tiered approach ensures efficient routing and avoids congestion within the airspace.

![Alt text](https://i.ibb.co/XCjfr3R/image.png)

## Getting Started

1. Install required libraries (`pip install mysql-connector-python8.0.0 numpy pillow`).
3. Configure database connection details in the code.
4. Run the main script (`python main.py`).

## Contributing

We welcome contributions to this project! Please create a pull request on GitHub for any bug fixes, enhancements, or new features.

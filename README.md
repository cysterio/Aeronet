# AeroNet

AeroNet is a project designed to develop a realistic, semi-autonomous Air Traffic Management (ATM) system. The primary goal is to alleviate the workload of Air Traffic Controllers (ATCs) by automating routine tasks and providing intelligent support. This system aims to enhance overall safety and efficiency in airspace management.

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

Designed for simulation and research purposes. Integrates seamlessly with human ATCs for handling emergencies. Future potential for real-world integration with aircraft flight computers. Limitations: Requires further development for robust real-world implementation. May not account for all potential emergency scenarios.

## Airspace Design

Incorporates a tiered structure of waypoints (20 total) strategically arranged for optimized air traffic flow and enhanced safety.
* Primary Waypoints (12): Distance - 25 nautical miles
* Secondary Waypoints (6): Distance - 15 nautical miles
* Tertiary Waypoints (2): Distance - 5 nautical miles
This tiered approach ensures efficient routing and avoids congestion within the airspace.

## File Directory

(Please replace this section with the actual directory structure of your project)

## Getting Started

1. Install required libraries (`pip install mysql-connector-python8.0.0 numpy pillow`).
2. Set up a MySQL database.
3. Configure database connection details in the code.
4. Run the main script (`python main.py`).

## Contributing

We welcome contributions to this project! Please create a pull request on GitHub for any bug fixes, enhancements, or new features.

## License

(Specify the license under which you want to distribute your code, e.g., MIT, Apache, etc.)

## Disclaimer

This project is for educational and research purposes only. It is not intended for real-world air traffic management applications without extensive testing and certification.

## Additional Notes

* Consider adding screenshots or a short video demonstrating the system's functionality.
* Include clear instructions for customization (if applicable).
* Provide references for any external resources used (e.g., APIs, libraries).
* Maintain the project's README.md as it evolves.

By following these guidelines, you'll create a comprehensive and informative README.md file for your AeroNet project.

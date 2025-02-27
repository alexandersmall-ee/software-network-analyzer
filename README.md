# software-network-analyzer

**Network Analyzer**

**Project Overview**

This project aims to develop a software-controlled network analyzer using an oscillator, an oscilloscope, and a computer. The analyzer automates frequency sweeps, measures phase and amplitude response, and generates a Bode plot for visualization. It integrates Python for signal generation, a two-channel oscilloscope for measurement, and a web-based UI for data visualization. The system utilizes IEEE 488.2 (USB-TMC) protocol for USB-based instrument control and applies signal processing and data visualization techniques.

**System Architecture**

*Hardware Components*

TDS 1002B oscilloscope (IEEE 488.2 compliant via USB-TMC), Computer with VSCode and development environment, USB-based signal generation.

*Software Stack*

Python (SciPy + Sounddevice) for signal generation, Node.js + Express.js for backend API, Angular + Chart.js for UI visualization, OAuth for secure authentication, Kubernetes + Docker for CI/CD and deployment, AWS/Firebase for hosting and deployment.

*Key Features*

Automated frequency sweeps (20 Hz – 300 kHz), SCPI commands over USB-TMC for oscilloscope control, Real-time data visualization using Chart.js, Bode Plot generation to analyze frequency response, RESTful API for backend communication, OAuth authentication for user access, CI/CD with Kubernetes for automated testing and deployment.

**Installation Steps**

*Clone the repository with:*

git clone https://github.com/YOUR_USERNAME/software-network-analyzer.git. 

Install dependencies by navigating to the project directory and running npm install for Node.js dependencies and pip install -r backend/requirements.txt for Python dependencies. Set up environment variables by creating a .env file in the api/config/ directory and defining API keys, database URLs, and OAuth credentials. Run the backend by navigating to the backend directory and executing python main.py. Run the frontend by navigating to the frontend directory and executing npm start. Access the application in the browser at http://localhost:4200.

**Usage Instructions**

Run frequency sweeps to analyze system response, Generate and visualize Bode plots in real-time, Retrieve oscilloscope data via API.

**Contribution Guidelines**

Fork the repository. Create a feature branch with git checkout -b feature/your-feature. Commit your changes with git commit -m "feat: Add new feature". Push to GitHub using git push origin feature/your-feature. Submit a Pull Request.

**License**

This project is licensed under the MIT License. See the LICENSE file for details.


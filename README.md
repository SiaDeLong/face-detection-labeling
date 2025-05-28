# Real-Time Camera Face Detection and Labelling App

This application performs real-time face detection and labelling using your computer's camera. It leverages computer vision techniques and requires a compatible Python environment along with some build tools.

---

## Prerequisites

Before you begin, ensure your system meets the following requirements:

1. **Python 3.10** (Avoid the Microsoft Store version)  
    - Download and install Python 3.10 from the official [Python website](https://www.python.org/downloads/release/python-3100/).  
    - During installation, **make sure to check the option "Add Python to PATH"**.  
    - Verify installation by running:  
        ```bash
        python --version
        ```  
    - **Note:** If using VSCode, set the Python interpreter to the installed Python 3.10 executable to avoid conflicts.

2. **CMake**  
    - Download and install CMake from the official [CMake website](https://cmake.org/download/).  
    - Add the `bin` directory of CMake installation to your system's PATH environment variable.  
    - Verify by running:  
        ```bash
        cmake --version
        ```

3. **Visual C++ Build Tools**  
    - Install the latest **Visual Studio Build Tools** including the **C++ build tools** workload from the [Microsoft website](https://visualstudio.microsoft.com/visual-cpp-build-tools/).  
    - This is required to compile native dependencies.

---

## Setup Instructions

After installing the prerequisites, follow these steps:

1. **Upgrade pip and essential packages:**  
    Open a terminal or command prompt and run:  
    ```bash
    python -m ensurepip --upgrade
    python -m pip install --upgrade pip setuptools wheel
    ```

2. **Install required Python packages:**
Ensure your terminal is in the project root directory containing requirements.txt, then run:
    ```bash
    cmake --version
    ```

---

## Usage
Run the application to start real-time face detection and labelling using your camera:
    ```bash
    python main.py
    ```

## Notes
   - Make sure your Python interpreter in VSCode or any other IDE points to the manually installed Python 3.10 interpreter, not the Microsoft Store version.
   - If you encounter errors related to native module compilation, double-check that Visual C++ Build Tools are properly installed.


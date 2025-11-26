# **🔒 Advanced Encrypted Keylogger PoC (Proof-of-Concept)**

## **🌟 Project Summary**

This project presents a robust and highly configurable Proof-of-Concept (PoC) keylogger designed exclusively for **educational and security research purposes**. It demonstrates the complete lifecycle of a modern data collection mechanism: from low-level keystroke capture to highly secure data encryption and simulated remote exfiltration.

The primary focus is on implementing **ethical security controls** (like the Kill Switch) alongside powerful, real-world data security techniques (Fernet encryption).

## **🎯 Core Objectives and Fulfillment**

| Objective | Status | Implementation Detail |
| :---- | :---- | :---- |
| **Keystroke Capture** | ✅ Fulfilled | Utilizes pynput to listen for all keys (alphanumeric, special, and control keys). |
| **Strong Encryption** | ✅ Fulfilled | Implements cryptography.fernet using a dynamically loaded or generated secret key (secret.key). |
| **Secure Local Logging** | ✅ Fulfilled | Encrypted ciphertext is written to encrypted\_keys.log along with a timestamp and a unique separator for reliable parsing. |
| **Simulated Exfiltration** | ✅ Fulfilled | The process of packaging, transmitting (simulated HTTP POST), and local cleanup occurs automatically every 30 seconds. |
| **Control Mechanisms** | ✅ Fulfilled | Includes a documented guide for startup persistence and an immediate Kill Switch feature (F12 or KILL\_SWITCH.txt). |

## **💻 Technical Stack**

| Tool / Library | Role in PoC | Why it was chosen |
| :---- | :---- | :---- |
| **Python 3.x** | Core Runtime | Simplicity and extensive library support for security tools. |
| **pynput** | Input Monitoring | Cross-platform, non-blocking listener for keyboard events. |
| **cryptography.fernet** | Data Security Layer | Provides authenticated symmetric encryption, ensuring confidentiality and integrity. |
| **time, datetime** | Timing & Scheduling | Critical for accurate logging timestamps and controlling the exfiltration interval. |

# **⚙️ Setup and Usage Guide**

Hello, Jarvej\! This guide explains the necessary steps to set up and run your **Encrypted Keylogger PoC**.

## **1\. Prerequisites (Essential Requirements)**

Before running this project, ensure that the following software is installed on your system:

* **Python 3.6+:** This is the core programming language.  
* **pip:** This is the Python package installer.

## **2\. Installing Dependencies (Required Libraries)**

We will need two main Python libraries: pynput and cryptography.

**Steps:**

1. Open your Terminal (or Command Prompt/PowerShell) in the project directory where the keylogger\_poc.py file is located.  
2. Run the command below:  
   pip install pynput cryptography

   *(This command will download and install the necessary packages.)*

## **3\. Running the Project**

Once the dependencies are installed, you can execute the program:

1. In the same Terminal window where your project directory is open, run this command:  
   python keylogger\_poc.py

2. If everything is successful, you will see these messages:  
   * \[\*\] Loaded existing encryption key...  
   * \[RUNNING\] Listening for keystrokes...

## **4\. Testing and Data Verification**

After the program is active, you can test it:

1. Open any text editor (like Notepad) or web browser and type some text.  
2. Every **30 seconds**, the program will trigger the simulate\_exfiltration function.  
3. In this output, your data will be **decrypted** and displayed on the screen, proving that both encryption and decryption are working correctly.  
4. Immediately after exfiltration, the encrypted\_keys.log file will be automatically **cleared**.

## **5\. Stopping the Program (Kill Switch)**

There are two easy ways to stop the program gracefully:

1. **Press the F12 Key:** When the program is active, press the **F12** key on your keyboard. The listener will stop immediately.  
2. **Create the KILL\_SWITCH.txt File:** Create an **empty** file named KILL\_SWITCH.txt in the project directory.

## **⚠️ Ethical and Legal Notice (Crucial)**

This repository is maintained with a strict ethical commitment. This software is provided **"as is"** for **educational analysis only**.

* **Non-Malicious Use Required:** You **must not** use this code to access, collect, or store data from any system or device without the express written permission of the owner.  
* **Local Use Only:** Testing must be confined to private, isolated, or virtualized environments owned and controlled by the user.

Author: Sunil
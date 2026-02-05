# 🔐 Steganography Master – Hide Secrets in Images

Steganography Master is a Python-based desktop application that allows users to **securely hide and extract secret text messages inside images** using **LSB (Least Significant Bit) steganography**.  
The project features a **modern animated GUI** built with Tkinter, offering an engaging and user-friendly experience.

---

## ✨ Features

- 🔒 Hide secret text messages inside image files  
- 🔓 Extract hidden messages from stego-images  
- 🖼️ Supports PNG, JPG, JPEG, BMP, and GIF images  
- 🎨 Animated, futuristic Tkinter GUI with particle effects  
- ⚡ Real-time validation and error handling  
- 🔍 Generates a **highlighted image** showing modified pixels  
- 🧠 Uses LSB (Least Significant Bit) steganography technique  

---

## 🛠️ Tech Stack

- **Python**
- **Tkinter** (GUI)
- **Pillow (PIL)** for image processing
- **LSB Steganography**
- Object-Oriented Programming (OOP)

---

## 📸 Application Interface

### Main Interface
![Steganography Master UI](screenshots/main_ui.png)

> The interface includes animated particle backgrounds, glowing buttons, and smooth UI effects for an enhanced user experience.

---

## ⚙️ How It Works

1. The secret message is converted into **binary**
2. Binary bits are embedded into the **least significant bits of image pixels**
3. A delimiter marks the end of the hidden message
4. Modified pixels can be visually highlighted for analysis
5. Extraction reads LSBs until the delimiter is detected

---

## How to Run the Project

### 1️⃣ Install Dependencies
```bash
pip install pillow
2️⃣ Run the Application
python main.py
📂 Project Structure
Steganography-Master/
│
├── main.py              # GUI application
├── stego.py             # Steganography logic
├── screenshots/         # UI screenshots
│   └── main_ui.png
├── highlight_output.png # Highlighted modified pixels
└── README.md
```
###  Example Use Case
- Secure communication

- Data hiding and privacy

- Educational tool for steganography concepts

- Cybersecurity and digital forensics demonstrations

### ⭐ Future Improvements
- Password-based encryption

- Support for audio/video steganography

- Dark/Light theme toggle

- Cross-platform executable

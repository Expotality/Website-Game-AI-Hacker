# 🎮 AI Web Game Hacker Agent

Transform any browser-based idle or incremental game into an intelligent, AI-powered sandbox. This project leverages **Streamlit**, **Playwright**, and the **Google GenAI SDK** to let you control, automate, and hack browser games using plain English commands or custom JavaScript injections.

---

## ✨ Key Features

* **🌐 Cross-Browser Debug Launcher:** Automatically boots popular Chromium-based browsers (Google Chrome, Brave, Microsoft Edge, Opera GX) in remote debugging mode with isolated profiles and smart fallback handling.
* **🎯 Dynamic Tab Targeting:** Seamlessly inspects and lists all open browser tabs so you can attach directly to your target game.
* **🤖 Natural Language AI Agent:** Powered by advanced Gemini models to translate your plain-English goals into raw, executable JavaScript game exploits.
* **🛠️ Manual Injection Console:** A built-in developer console for direct JavaScript testing and execution.

---

## 🛠️ Setup & Installation Guide

Follow these steps to get your local environment configured and ready to run the agent.

### Step 1: Clone or Download the Repository
Clone this repository to your local machine or download it as a ZIP archive and extract it to a folder of your choice. (the top right (<>code^) button leads to it, AND DONT FORGET TO EXTRACT/UNZIP IT!!!) 

### Step 2: Install Python Dependencies
Open your terminal (or command prompt), navigate into the project directory, and install the required packages using the requirements file:

```bash
pip install -r requirements.txt
```

### Step 3: Install Playwright Browsers
Playwright requires browser binaries to connect and automate browser instances. Run the following command in your terminal:

```bash
playwright install
```

### Step 4: Configure Your API Key
1. Open the `app.py` file in any text editor like Notepad or Visual Studio.
2. Locate the configuration block at the very top of the script:
   ```python
   # ====================================================
   # 🔑 USER CONFIGURATION: FILL IN YOUR DETAILS BELOW
   # ====================================================
   GEMINI_API_KEY = "YOUR_API_KEY_HERE"  # Replace with your actual Google Gemini API Key
   ```
3. Replace `"YOUR_API_KEY_HERE"` with your actual Google GenAI API key. *(Note: You can use a **free** API key from [Google AI Studio](https://aistudio.google.com/)).*

---

## 🚀 Running the Application

1. Start the Streamlit application by double clicking the 'run' file in the folder
2. Your web browser will automatically open to the local Streamlit user interface, with advanced "hacker" designs.
3. Select your preferred browser from the launcher panel and click **Launch Browser in Debug Mode**.
4. Open your target game or website in that newly spawned browser window, navigate back to the app, refresh your tabs, select your game tab, and start hacking!
5. If you ever get an error, it's likely because you didnt install something, or you didnt open your browser in debug mode. If you already did those, switch AI models at the top. Sometimes they are overloaded and can't answer.

---

## 🛡️ License

Distributed under the MIT License. See `LICENSE` for more information.

# 💼 Optium Capital – Unified Financial App Platform

This platform combines multiple data apps into one unified, browser-based interface.  
---

## 🛠️ First-Time Setup (Windows)

---

### 1. 📁 Download and Extract the Project

1. Go to: [https://github.com/Optium-Capital/app000_unified_apps](https://github.com/Optium-Capital/app000_unified_apps)  
2. Click the green **"Code"** button  
3. Choose **"Download ZIP"**  
4. Extract the ZIP to a location like your Desktop

---

### 2. 📂 Add Data Files

1. Open Dropbox  
2. Go to:  
   `PATRICIA/Audrey/Olivier/datasets_performant`
3. Select all files inside  
4. Copy them into the `data/` folder inside the extracted project
Your final structure should look like:

app000_unified_apps/  
├── app.py  
├── apps/  
├── data/  
│   ├── 415768196 - 2025-5-15.csv  
│   ├── franchisee_tax_id.parquet  
│   ├── ...

---

### 3. 🐍 Install Python

1. Go to: https://www.python.org/downloads/  
2. Click **Download Python 3.13.3**  
3. Open the installer  
4. ✅ Make sure to check **"Add Python to PATH"**  
5. Complete the installation

---

### 4. 🖥 Open Command Prompt & Navigate to the Folder

1. Press **Windows Key**, search for `command prompt`, open it  
2. Use these commands to navigate:
   - Go up a level: `cd ..`
   - Go into a folder: `cd folder_name`
   - List folder contents: `dir`

Example:

cd Desktop  
cd app000_unified_apps-main

Confirm you're in the right place by checking that `requirements.txt` is listed when you run:

dir

---

### 5. ⚙️ Set Up and Run the App

Paste these lines **one by one** into Command Prompt:

py -m venv venv  
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass  
venv\Scripts\activate.bat  
pip install -r requirements.txt  
streamlit run app.py

✅ This will open the app in your browser. If it doesn’t, copy the link from the terminal into your browser manually.

---

## 🔁 To Use Again Later

Each time you want to use the tool:

1. Open **Command Prompt**
2. Navigate back to your folder:

Hugo:  
cd Desktop\app000_unified_apps-main

Elaine:  
cd "C:\Users\eopti\OneDrive\Desktop\app000_unified_apps-main"

Tony:  
cd "C:\Users\trale\OneDrive\Desktop\app000_unified_apps-main"

3. Then run:

venv\Scripts\activate.bat  
streamlit run app.py

---

## 🔐 100% Local & Secure

- All data stays on your computer  
- No uploads or cloud services involved  
- You can disconnect from internet after install  

---

Made to save hours of repetitive work  
💼 Built by the Data Team @ Optium Capital

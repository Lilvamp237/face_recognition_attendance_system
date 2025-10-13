# 👨‍💼 Face Recognition-Based Attendance System 📸

As technology continues to evolve, many tasks that once required manual effort are now being automated — improving productivity and accuracy. One such area is **attendance monitoring**. Traditional methods like scanning ID cards or signing registers are often tedious and prone to errors.

This **Face Recognition-Based Attendance System** leverages modern face recognition technology to automatically mark attendance simply by scanning a person’s face — no manual input needed! 🙌

✨ **Key Benefits:**
- Accurate and reliable attendance ✅
- Eliminates proxy attendance 🚫
- Real-time processing ⚡
- Suitable for classrooms, workplaces, and events 🏫🏢🎉
- Reduces administrative overheads 💰
- Enhances security 🔐
- Seamless and modern user experience 🌐


## 🛠️ Technologies Used

| Technology             |               Purpose                       |
|------------------------|---------------------------------------------|
| 🐍 **Python**          | Core programming language                   |
| 📷 **OpenCV (cv2)**    | Real-time face detection & recognition      |
| 🤖 **DeepFace**        | Deep learning-based face recognition        |
| 🖼️ **Qt5 / PyQt5**     | GUI framework and Python bindings           |
| ➕ **NumPy**           | Numerical computations                      |
| 🔬 **SciPy (cosine)**  | Cosine similarity for face feature matching |
| 📊 **Matplotlib**      | Data visualization and stats                |

## 🧠 System Overview & Functionalities

The system includes a **multi-page GUI** with 3 main features:

### 1️⃣ Register New Users 📝  
Users can register themselves by taking 5 photos from different angles. These are stored with a **unique name**, and the user can start marking attendance immediately.

### 2️⃣ Mark Attendance 🕵️  
Users mark their daily attendance by scanning their face. The system ensures:
- Face matches a registered user
- Attendance is only marked once per day

### 3️⃣ View Weekly Statistics 📈  
Users can:
- View their attendance history for the past 7 days
- See overall and individual stats (e.g., number of absences)


## 🔍 Advanced Features & AI Pipeline Justification

### 🧬 Facial Recognition-Based System
- Uses OpenCV & DeepFace to detect and recognize users
- Verifies identity by comparing face embeddings

### 🕒 Real-Time Face Detection
- Utilizes Haar cascades for live face detection
- Filters detections based on confidence levels

### 📷 Intelligent Face Registration
- Captures multiple photos per user
- Applies augmentation (e.g., brightness normalization) for accuracy

### 📚 Multi-Page GUI with `QStackedWidget`
- Intuitive navigation across Dashboard, Attendance, Statistics, and Registration pages
- Smooth user flow 🎯

### 📊 Attendance Analysis & Visualization
- Displays:
  - 📅 Daily & weekly attendance
  - 👤 User-specific attendance history

### 💾 Secure & Efficient Data Handling
- Stores user images and attendance records locally for tracking and auditing


---

## 📋 Prerequisites

Before you begin, ensure you have the following installed:
- **Python 3.8+** ([Download here](https://www.python.org/downloads/))
- **pip** (Python package manager)
- **Webcam** (for real-time face detection)
- **Git** (optional, for cloning the repository)

---

## 🚀 Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/Lilvamp237/face_recognition_attendance_system.git
cd face_recognition_attendance_system
```

### 2️⃣ Create a Virtual Environment (Recommended)
**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Install Required Dependencies
```bash
pip install -r requirements.txt
```

> ⚠️ **Note:** The first run will take some time as DeepFace downloads the pre-trained Facenet512 model (~100MB).

### 4️⃣ Create Required Directories
```bash
mkdir known_faces
```

### 5️⃣ (Optional) Add the Kiosk Image
The system expects a `Kiosk-Mode.png` image in the root directory for the main page UI. You can either:
- Add your own image named `Kiosk-Mode.png`, or
- The system will still work without it (the image label will just be empty)

---

## 🏗️ Project Structure

```
face_recognition_attendance_system/
│
├── attendance_system.py          # Main Python script (GUI application)
├── attendance_system.ipynb       # Jupyter notebook version
├── requirements.txt              # Python dependencies
├── README.md                     # Project documentation
├── .gitignore                    # Git ignore rules
│
├── known_faces/                  # User face images (created on first registration)
│   ├── PersonName1/
│   │   ├── 1.jpg
│   │   ├── 2.jpg
│   │   └── ...
│   └── PersonName2/
│       └── ...
│
├── attendance.csv                # Attendance records (auto-generated)
└── Kiosk-Mode.png               # (Optional) Main page display image
```

---

## ▶️ How to Run

### Method 1: Run Python Script
```bash
python attendance_system.py
```

### Method 2: Run Jupyter Notebook
```bash
jupyter notebook attendance_system.ipynb
```
Then run all cells in the notebook.

---

## 🎯 Usage Guide

### Step 1: Launch the Application
Run `python attendance_system.py` - the main dashboard will appear.

### Step 2: Register a New User 📝
1. Click **"Register New User"**
2. Enter your name when prompted
3. Allow camera access
4. The system will capture **5 photos** from different angles
5. Move your face slightly for better coverage
6. Your face data is now saved!

### Step 3: Mark Attendance 🕵️
1. Click **"Mark Attendance"**
2. Face the camera
3. System will automatically detect and recognize your face
4. If matched, attendance is marked (once per day)
5. You'll see a confirmation message

### Step 4: View Statistics 📈
1. Click **"View Statistics"**
2. Select your name from the dropdown
3. See your attendance history for the past 7 days
4. View detailed records in a table format

---

## 🛠️ Troubleshooting

### Issue: "No module named 'cv2'" or similar import errors
**Solution:** Make sure you activated the virtual environment and installed dependencies:
```bash
pip install -r requirements.txt
```

### Issue: Camera not detected
**Solution:** 
- Ensure your webcam is connected and not being used by another application
- Check camera permissions in your OS settings
- Try restarting the application

### Issue: Face not recognized even after registration
**Solution:**
- Ensure good lighting conditions
- Face the camera directly
- Try registering again with clearer photos
- Check that your photos are saved in `known_faces/YourName/`

### Issue: "Could not extract embedding" errors
**Solution:**
- This usually happens with poor quality images
- Ensure faces are clearly visible in registration photos
- Avoid extreme angles or obstructions

### Issue: Slow performance on first run
**Solution:**
- DeepFace downloads AI models on first run (~100MB)
- Subsequent runs will be much faster
- Be patient during initial setup

---

## 🔧 Configuration

### Change Face Recognition Model
Edit line 52 in `attendance_system.py`:
```python
# Current: Facenet512 (most accurate, slower)
embedding = DeepFace.represent(img_path, model_name="Facenet512", enforce_detection=False)[0]['embedding']

# Alternatives:
# embedding = DeepFace.represent(img_path, model_name="Facenet", enforce_detection=False)[0]['embedding']    # Faster
# embedding = DeepFace.represent(img_path, model_name="ArcFace", enforce_detection=False)[0]['embedding']    # Good balance
# embedding = DeepFace.represent(img_path, model_name="SFace", enforce_detection=False)[0]['embedding']      # Fastest
```

---

## 📊 Data Files

### attendance.csv
Stores attendance records in format:
```
Name,Time
John Doe,2025-10-13 09:30:15
Jane Smith,2025-10-13 09:32:45
```

### known_faces/
Directory structure for registered users:
```
known_faces/
  ├── John Doe/
  │     ├── 1.jpg
  │     ├── 2.jpg
  │     ├── 3.jpg
  │     ├── 4.jpg
  │     └── 5.jpg
  └── Jane Smith/
        └── ...
```

---

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

---

## 📄 License

This project is open-source and available for educational purposes.

---

## 👨‍💻 Author

**Lilvamp237**  
GitHub: [@Lilvamp237](https://github.com/Lilvamp237)


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

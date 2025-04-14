#!/usr/bin/env python
# coding: utf-8

# In[1]:
import sys
import os
import cv2
import datetime
import numpy as np
from collections import defaultdict
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QSizePolicy, QStackedWidget, QComboBox, QMessageBox, QLineEdit, QInputDialog, QTableWidget, QTableWidgetItem, QSpacerItem
from PyQt5.QtGui import QPixmap, QImage, QFont, QPalette, QColor
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import Qt
from deepface import DeepFace
from scipy.spatial.distance import cosine
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas



# In[2]:
# Create attendance file
attendance_file = "attendance.csv"
if not os.path.exists(attendance_file):
    with open(attendance_file, "w") as f:
        f.write("Name,Time\n")


# In[3]:
# Load face detector
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')


# In[4]:
# Load known faces
known_faces_dir = "known_faces"
known_faces = {}


# In[5]:
# Precompute face embeddings
for person_name in os.listdir(known_faces_dir):
    person_path = os.path.join(known_faces_dir, person_name)
    if os.path.isdir(person_path):
        known_faces[person_name] = []
        for img_name in os.listdir(person_path):
            img_path = os.path.join(person_path, img_name)
            try:
                #embedding = DeepFace.represent(img_path, model_name="Facenet", enforce_detection=False)[0]['embedding']
                embedding = DeepFace.represent(img_path, model_name="Facenet512", enforce_detection=False)[0]['embedding']
                #embedding = DeepFace.represent(img_path, model_name="ArcFace", enforce_detection=False)[0]['embedding']
                #embedding = DeepFace.represent(img_path, model_name="SFace", enforce_detection=False)[0]['embedding']
                known_faces[person_name].append(embedding)
            except:
                print(f"Skipping {img_path}, could not extract embedding.")


# In[6]:
class MainPage(QWidget):
    def __init__(self, stacked_widget, camera_page, stats_page, register_page):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.camera_page = camera_page
        self.stats_page = stats_page
        self.register_page = register_page
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Face Recognition Attendance System")
        self.setGeometry(100, 100, 800, 600)

        # Apply white background to the entire window using stylesheets
        self.setStyleSheet("background-color: white;")

        # Image Label
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # Allow expansion
        
        image_path = os.path.abspath("Kiosk-Mode.png")
        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            print("Failed to load image!")
        else:
            self.image_label.setPixmap(pixmap)
            #self.image_label.setPixmap(pixmap)
            self.image_label.setScaledContents(True)  # Ensures the image scales within the label
            self.image_label.setFixedSize(615, 450)
        
        self.label = QLabel("Welcome to Attendance System", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(QFont("Arial", 16, QFont.Bold))  # Bigger and Bold
        
        # Center image in layout
        image_layout = QVBoxLayout()
        #image_layout = QHBoxLayout()
        #image_layout.addStretch()
        image_layout.addWidget(self.image_label, alignment=Qt.AlignCenter)
        #image_layout.addStretch()
        image_layout.addWidget(self.label, alignment=Qt.AlignCenter)
        #image_layout.addStretch()
        
        #self.label = QLabel("Welcome to Attendance System", self)
        #self.label.setAlignment(Qt.AlignCenter)
        
        # Spacer to push buttons down
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        
        # Buttons
        self.attendance_button = QPushButton("Mark Attendance", self)
        self.stats_button = QPushButton("View Statistics", self)
        self.register_button = QPushButton("Register New User", self)
        self.exit_button = QPushButton("Exit System", self)

        # Make buttons stretch from left to right
        for button in [self.attendance_button, self.stats_button, self.register_button, self.exit_button]:
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            button.setStyleSheet("")

        self.attendance_button.clicked.connect(self.go_to_camera)
        self.stats_button.clicked.connect(self.view_statistics)
        self.register_button.clicked.connect(self.go_to_register)
        self.exit_button.clicked.connect(self.exit_system)

        # Button Layout (to keep them at the bottom)
        button_layout = QVBoxLayout()
        button_layout.addWidget(self.attendance_button)
        button_layout.addWidget(self.stats_button)
        button_layout.addWidget(self.register_button)
        button_layout.addWidget(self.exit_button)
        button_layout.setAlignment(Qt.AlignBottom)  # Keep buttons at the bottom

        # Main Layout
        layout = QVBoxLayout()
        layout.addLayout(image_layout)  # Centered Image
        layout.addItem(spacer)  # Pushes buttons down
        layout.addLayout(button_layout)  # Buttons stay at the bottom
        layout.setAlignment(Qt.AlignCenter)
        
        self.setLayout(layout)

    def go_to_camera(self):
        """ Switch to CameraPage and start the camera. """
        self.camera_page.start_camera()
        self.stacked_widget.setCurrentWidget(self.camera_page)

    def view_statistics(self):
        self.stacked_widget.setCurrentWidget(self.stats_page)

    def go_to_register(self):
        self.register_page.start_camera()  # Start the camera before switching
        self.stacked_widget.setCurrentWidget(self.register_page)

    def exit_system(self):
        sys.exit()


# In[7]:
class CameraPage(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.cap = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Camera Attendance")
        self.setGeometry(100, 100, 640, 480)
        #self.setGeometry(100, 100, 320, 240)

        self.camera_label = QLabel(self)
        self.camera_label.setFixedSize(640, 480)
        self.camera_label.setStyleSheet("border: 2px solid black;")
        #self.camera_label.setFixedSize(320, 240)

        self.back_button = QPushButton("Back", self)
        self.back_button.clicked.connect(self.go_back)

        layout = QVBoxLayout()
        layout.addWidget(self.camera_label, alignment=Qt.AlignCenter)
        layout.addStretch(1)

        # Make the button stretch left to right
        self.back_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        button_layout = QHBoxLayout()
        #button_layout.addStretch(1)  # Push button to center
        button_layout.addWidget(self.back_button)
        #button_layout.addStretch(1)  # Push button to center

        layout.addLayout(button_layout)  # Add button layout at the bottom

        self.setLayout(layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)

    def start_camera(self):
        """ Starts the webcam when navigating to this page. """
        if self.cap is None or not self.cap.isOpened():
            self.cap = cv2.VideoCapture(0)
            self.timer.start(30)

    def update_frame(self):
        """ Captures frame, detects faces, recognizes them, and updates GUI. """
        ret, frame = self.cap.read()
        if not ret:
            return

        try:
            # Detect faces
            detected_faces = DeepFace.extract_faces(frame, detector_backend="retinaface", enforce_detection=False)

            for face in detected_faces:
                facial_area = face['facial_area']
                x, y, w, h = facial_area['x'], facial_area['y'], facial_area['w'], facial_area['h']
                face_roi = frame[y:y + h, x:x + w]

                try:
                    #face_embedding = DeepFace.represent(face_roi, model_name="Facenet", enforce_detection=False)[0]['embedding']
                    face_embedding = DeepFace.represent(face_roi, model_name="Facenet512", enforce_detection=False)[0]['embedding']
                    #face_embedding = DeepFace.represent(face_roi, model_name="ArcFace", enforce_detection=False)[0]['embedding']
                    #face_embedding = DeepFace.represent(face_roi, model_name="SFace", enforce_detection=False)[0]['embedding']
                except Exception as e:
                    print(f"Error getting embedding: {str(e)}")
                    continue

                name = "Unknown"
                min_distance = 0.4  # Threshold for matching

                for person_name, embeddings in known_faces.items():
                    for stored_embedding in embeddings:
                        distance = cosine(face_embedding, stored_embedding)
                        if distance < min_distance:
                            name = person_name
                            min_distance = distance  # Update best match

                # Mark attendance
                if name != "Unknown":
                    with open(attendance_file, "r+") as f:
                        lines = f.readlines()
                        for line in lines:
                            if name in line:
                                last_time = datetime.datetime.strptime(line.strip().split(",")[1], "%Y-%m-%d %H:%M:%S")
                                if (datetime.datetime.now() - last_time).total_seconds() < 300:
                                    print("Attendance already marked within the last 5 minutes.")
                                    break
                        else:
                            f.write(f"{name},{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

                # Draw rectangle and label
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        except Exception as e:
            print(f"Error in face detection: {str(e)}")

        # Convert frame to Qt format and update GUI
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        height, width, channel = frame.shape
        bytes_per_line = 3 * width
        q_img = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
        self.camera_label.setPixmap(QPixmap.fromImage(q_img))

    def go_back(self):
        """ Releases the camera and stops the feed before going back. """
        if self.cap is not None:
            self.timer.stop()
            self.cap.release()
            self.cap = None
        self.stacked_widget.setCurrentIndex(0)


# In[8]:
class StatisticsPage(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Attendance Statistics")
        self.setGeometry(100, 100, 800, 600)  # Ensure enough space for all elements
    
        self.back_button = QPushButton("Back", self)
        self.back_button.clicked.connect(self.go_back)
    
        # Main layout
        main_layout = QVBoxLayout()
    
        # Bar Chart Section (Occupies More Space)
        self.chart_widget = QLabel(self)
        self.chart_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # Expanding means it will adjust with window resizing
        self.chart_widget.setMinimumHeight(400)  # Ensure a reasonable minimum height
        main_layout.addWidget(self.chart_widget, stretch=2)  # Allocate more space to bar chart
    
        # Name Dropdown
        self.name_dropdown = QComboBox(self)
        self.name_dropdown.addItems(known_faces)
        self.name_dropdown.currentIndexChanged.connect(self.show_person_attendance)
        main_layout.addWidget(self.name_dropdown)
    
        # Bottom layout (Table + Pie Chart)
        bottom_layout = QHBoxLayout()
    
        # Table (Left Side)
        self.attendance_table = QTableWidget(self)
        self.attendance_table.setColumnCount(2)
        self.attendance_table.setHorizontalHeaderLabels(["Date", "Attendance"])
        self.attendance_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # Make table resizable
        self.attendance_table.setMinimumWidth(150)  # Avoid shrinking too much
        self.attendance_table.setMinimumHeight(300)
        bottom_layout.addWidget(self.attendance_table, stretch=3)  # Allocate more space for the table
    
        # Pie Chart (Right Side)
        self.pie_chart_widget = QLabel(self)
        self.pie_chart_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.pie_chart_widget.setMinimumSize(50, 50)  # Ensure a reasonable minimum size
        bottom_layout.addWidget(self.pie_chart_widget, stretch=2)  # Allocate some space for the pie chart
    
        main_layout.addLayout(bottom_layout, stretch=3)  # Bottom section has more space
    
        # Absents Label
        self.absents_label = QLabel(self)
        main_layout.addWidget(self.absents_label)
    
        # Add stretch before button to push it to bottom
        main_layout.addStretch(1)
    
        # Back Button
        main_layout.addWidget(self.back_button)
    
        self.setLayout(main_layout)

        # Show initial statistics
        self.show_statistics()


    def get_attendance_statistics(self):
        """ Returns the attendance statistics for the last 7 days """
        attendance_data = defaultdict(int)
        total_people = len(known_faces)

        # Read attendance file and count people marked present for each day
        if os.path.exists(attendance_file):
            with open(attendance_file, 'r') as f:
                lines = f.readlines()[1:]  # Skip header
                for line in lines:
                    name, time_str = line.strip().split(',')
                    time = datetime.datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
                    day = time.date()

                    if (datetime.datetime.now().date() - day).days < 7:
                        attendance_data[day] += 1

        # Prepare the statistics for plotting
        days = sorted(attendance_data.keys())
        attendance_counts = [attendance_data[day] for day in days]
        dates = [day.strftime('%Y-%m-%d') for day in days]

        # If there are less than 7 days of data, fill in missing days with 0 attendance
        all_dates = [datetime.datetime.now().date() - datetime.timedelta(days=i) for i in range(7)]
        all_dates = sorted(all_dates)

        # Ensure attendance_counts matches the last 7 days
        final_dates = []
        final_attendance_counts = []
        for date in all_dates:
            date_str = date.strftime('%Y-%m-%d')
            final_dates.append(date_str)
            final_attendance_counts.append(attendance_data.get(date, 0))

        return total_people, final_dates, final_attendance_counts

    def show_statistics(self):
        """ Generates and displays the bar chart for the last 7 days attendance """
        total_people, dates, attended_counts = self.get_attendance_statistics()

        # Plot the bar chart
        fig, ax = plt.subplots(1, 1, figsize=(8, 4))
        ax.bar(dates, attended_counts, label="Attendance")
        ax.axhline(y=total_people, color='r', linestyle='--', label="Total People")
        ax.set_xlabel('Date')
        ax.set_ylabel('Attendance Count')
        ax.set_title('Attendance vs Total People (Last 7 Days)')
        ax.legend()

        # Convert the plot to a QPixmap and display it on the QLabel
        canvas = FigureCanvas(fig)
        canvas.draw()
        canvas_width, canvas_height = canvas.get_width_height()
        img = QImage(canvas.buffer_rgba(), canvas_width, canvas_height, QImage.Format_RGBA8888)
        pixmap = QPixmap.fromImage(img)

        self.chart_widget.setPixmap(pixmap)

    def show_person_attendance(self):
        """ Show the attendance of the selected person for the last 7 days """
        selected_name = self.name_dropdown.currentText()
        attendance_data = defaultdict(list)

        # Read attendance file and gather the attendance data for the selected person
        if os.path.exists(attendance_file):
            with open(attendance_file, 'r') as f:
                lines = f.readlines()[1:]  # Skip header
                for line in lines:
                    name, time_str = line.strip().split(',')
                    time = datetime.datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
                    day = time.date()

                    if name == selected_name and (datetime.datetime.now().date() - day).days < 7:
                        attendance_data[day] = 'Yes'

        # Prepare the attendance table
        all_dates = [datetime.datetime.now().date() - datetime.timedelta(days=i) for i in range(7)]
        all_dates = sorted(all_dates)

        # Update the table with attendance data for the selected person
        self.attendance_table.setRowCount(7)
        for i, date in enumerate(all_dates):
            date_str = date.strftime('%Y-%m-%d')
            attendance_status = attendance_data.get(date, 'No')
            self.attendance_table.setItem(i, 0, QTableWidgetItem(date_str))
            self.attendance_table.setItem(i, 1, QTableWidgetItem(attendance_status))

        # Show pie chart and total absents
        self.show_person_pie_chart(attendance_data, all_dates)

    def show_person_pie_chart(self, attendance_data, all_dates):
        """ Generate and display the pie chart for the selected person's attendance """
        # Count the number of "Yes" and "No" for attendance
        yes_count = sum(1 for date in all_dates if attendance_data.get(date, 'No') == 'Yes')
        no_count = 7 - yes_count  # Total is 7, so absents are 7 - yes_count

        # Display total absents (e.g., "4/7")
        self.absents_label.setText(f"Absents: {no_count}/7")

        # Create the pie chart
        fig, ax = plt.subplots(1, 1, figsize=(3, 3))
        ax.pie([yes_count, no_count], labels=["Yes", "No"], autopct='%1.1f%%', startangle=90)
        ax.set_title(f"{attendance_data.get('name', 'Person')} Attendance")

        # Convert the plot to a QPixmap and display it on the QLabel
        canvas = FigureCanvas(fig)
        canvas.draw()
        canvas_width, canvas_height = canvas.get_width_height()
        img = QImage(canvas.buffer_rgba(), canvas_width, canvas_height, QImage.Format_RGBA8888)
        pixmap = QPixmap.fromImage(img)

        self.pie_chart_widget.setPixmap(pixmap)

    def go_back(self):
        """ Go back to the main page """
        self.stacked_widget.setCurrentIndex(0)


# In[9]:
class RegisterPage(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.cap = None
        self.image_count = 0  
        self.image_folder = "known_faces"  
        self.current_user_folder = None  
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Register New User")
        self.setGeometry(100, 100, 640, 480)

        self.camera_label = QLabel(self)
        self.camera_label.setFixedSize(640, 480)

        self.capture_button = QPushButton("Capture Photo", self)
        self.capture_button.clicked.connect(self.capture_photo)

        self.back_button = QPushButton("Back", self)
        self.back_button.clicked.connect(self.go_back)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.capture_button)
        button_layout.addWidget(self.back_button)

        layout = QVBoxLayout()
        layout.addWidget(self.camera_label, alignment=Qt.AlignCenter)
        layout.addLayout(button_layout)
        self.setLayout(layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)

    def start_camera(self):
        """Starts the camera when the page is opened."""
        if self.cap is None or not self.cap.isOpened():
            self.cap = cv2.VideoCapture(0)
            if self.cap.isOpened():
                self.timer.start(30)

    def update_frame(self):
        """Continuously updates the camera feed in the UI."""
        ret, frame = self.cap.read()
        if not ret:
            return

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        height, width, channel = frame.shape
        bytes_per_line = 3 * width
        q_img = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
        self.camera_label.setPixmap(QPixmap.fromImage(q_img))

    def capture_photo(self):
        """Captures a photo and stores it, keeping a count until 5 photos are taken."""
        if self.cap is None or not self.cap.isOpened():
            return

        ret, frame = self.cap.read()
        if not ret:
            return

        if not os.path.exists(self.image_folder):
            os.makedirs(self.image_folder)

        if self.current_user_folder is None:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            self.current_user_folder = os.path.join(self.image_folder, f"user_{timestamp}")
            os.makedirs(self.current_user_folder)

        if self.image_count < 5:  
            image_path = os.path.join(self.current_user_folder, f"face_{self.image_count + 1}.jpg")
            cv2.imwrite(image_path, frame)
            self.image_count += 1
            print(f"Saved: {image_path}")

        if self.image_count == 5:
            self.finish_capture()

    def finish_capture(self):
        """Stops camera and prompts for user name after 5 images."""
        self.timer.stop()
        self.cap.release()
        self.cap = None
        self.get_unique_user_name()

    def get_unique_user_name(self):
        """Prompts the user for their name and ensures it's unique before renaming the folder."""
        while True:
            name, ok = QInputDialog.getText(self, "User Registration", "Enter your name:")
            if not ok or not name.strip():
                QMessageBox.warning(self, "Invalid Name", "You must enter a valid name.")
                continue
    
            new_folder_path = os.path.join(self.image_folder, name.strip())
    
            # Check if folder exists
            if os.path.exists(new_folder_path):
                QMessageBox.warning(self, "Name Exists", "This name is already taken. Please choose another name.")
                continue  # Ask again
    
            # Rename the temporary folder to the new name
            os.rename(self.current_user_folder, new_folder_path)
            print(f"User registered: {name} - Photos saved in {new_folder_path}")
    
            # Process images and compute embeddings
            self.process_new_user_images(name, new_folder_path)
            break  # Exit loop once a unique name is given
    
        self.reset_registration()

    def process_new_user_images(self, user_name, user_folder):
        """Extracts embeddings for the new user's images and updates known faces."""
        global known_faces  # Ensure it's accessible globally
    
        if user_name not in known_faces:
            known_faces[user_name] = []
    
        for img_name in os.listdir(user_folder):
            img_path = os.path.join(user_folder, img_name)
            try:
                # Extract face embedding
                embedding = DeepFace.represent(img_path, model_name="Facenet512", enforce_detection=False)[0]['embedding']
                known_faces[user_name].append(embedding)
            except Exception as e:
                print(f"Skipping {img_path}, could not extract embedding: {e}")
    
        print(f"Processed and stored embeddings for {user_name}.")


    def reset_registration(self):
        """Resets variables and restarts the camera for a new user."""
        self.current_user_folder = None
        self.image_count = 0
        self.start_camera()

    def go_back(self):
        """Stops camera and returns to main menu."""
        if self.cap is not None:
            self.timer.stop()
            self.cap.release()
            self.cap = None
        self.stacked_widget.setCurrentIndex(0)

# In[ ]:
if __name__ == '__main__':
    app = QApplication(sys.argv)
    stacked_widget = QStackedWidget()
    camera_page = CameraPage(stacked_widget)
    stats_page = StatisticsPage(stacked_widget)
    register_page = RegisterPage(stacked_widget)
    main_page = MainPage(stacked_widget, camera_page, stats_page, register_page)

    stacked_widget.addWidget(main_page)
    stacked_widget.addWidget(camera_page)
    stacked_widget.addWidget(stats_page)
    stacked_widget.addWidget(register_page)
    stacked_widget.setCurrentIndex(0)

    stacked_widget.show()
    cv2.destroyAllWindows()
    sys.exit(app.exec_())


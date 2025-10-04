import cv2
import hashlib
import os
import json
from moviepy.editor import VideoFileClip
import tkinter as tk
from tkinter import messagebox, ttk, filedialog


class VideoForensicTool:
    def __init__(self, video_path=None):
        self.video_path = video_path
        # Load Haar Cascade for face detection
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    def record_video(self, duration=5, filename="recorded_video.mp4"):
        cap = cv2.VideoCapture(0)  # Open the default camera
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(filename, fourcc, 20.0, (640, 480))
        print("Recording started...")

        for _ in range(int(duration * 20)):  # Record for the specified duration
            ret, frame = cap.read()
            if ret:
                # Convert frame to grayscale for face detection
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                # Detect faces in the frame
                faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)

                # Draw rectangles around detected faces
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

                # Check if more than one face is detected
                if len(faces) > 0:
                    print(f"More than one person detected! Number of faces: {len(faces)}")

                # Write the frame to the output file
                out.write(frame)

                # Display the frame with face rectangles
                cv2.imshow('Recording', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        print(f"Recording saved as {filename}")
        cap.release()
        out.release()
        cv2.destroyAllWindows()
        self.video_path = filename

    def upload_video(self):
        # Open file dialog to upload video
        file_path = filedialog.askopenfilename(title="Select Video", filetypes=[("MP4 files", "*.mp4")])
        if file_path:
            self.video_path = file_path
            print(f"Video uploaded: {self.video_path}")
            messagebox.showinfo("Info", "Video uploaded successfully!")

    def integrity_check(self):
        if not self.video_path:
            print("No video file loaded for integrity check.")
            return None

        hash_md5 = hashlib.md5()
        with open(self.video_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def extract_metadata(self):
        if self.video_path is None:
            print("No video file loaded.")
            return {}

        # Using moviepy to extract metadata
        video = VideoFileClip(self.video_path)
        metadata = {
            'duration': video.duration,  # Duration in seconds
            'fps': video.fps,  # Frames per second
            'size': video.size,  # Video size (width, height)
            'file_size': os.path.getsize(self.video_path)  # File size in bytes
        }
        return metadata

    def display_metadata(self):
        metadata = self.extract_metadata()
        messagebox.showinfo("Metadata", json.dumps(metadata, indent=4))


class VideoForensicApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Forensic Tool")
        self.tool = VideoForensicTool()
        self.setup_ui()

    def setup_ui(self):
        self.root.geometry("450x350")
        self.root.config(bg="#f4f4f4")

        # Title Frame
        title_frame = tk.Frame(self.root, bg="#302b63", bd=5)
        title_frame.pack(fill="x")

        title_label = tk.Label(title_frame, text="Video Forensic Tool", font=("Arial", 18, "bold"), bg="#302b63",
                               fg="white")
        title_label.pack(pady=10)

        # Button Frame  
        button_frame = tk.Frame(self.root, bg="#f4f4f4")
        button_frame.pack(pady=20)

        # Styled buttons
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 12), padding=10)

        self.record_button = ttk.Button(button_frame, text="Record Video", command=self.record_video)
        self.record_button.grid(row=0, column=0, padx=10, pady=10)

        self.upload_button = ttk.Button(button_frame, text="Upload Video", command=self.upload_video)
        self.upload_button.grid(row=0, column=1, padx=10, pady=10)

        self.integrity_button = ttk.Button(button_frame, text="Check Integrity", command=self.check_integrity)
        self.integrity_button.grid(row=1, column=0, padx=10, pady=10)

        self.metadata_button = ttk.Button(button_frame, text="Extract Metadata", command=self.extract_metadata)
        self.metadata_button.grid(row=1, column=1, padx=10, pady=10)

        self.exit_button = ttk.Button(button_frame, text="Exit", command=self.root.quit)
        self.exit_button.grid(row=2, column=1, padx=10, pady=10)

        # Cybersecurity Prompt Button
        self.cybersecurity_button = ttk.Button(button_frame, text="Cybersecurity Prompt",
                                               command=self.show_cybersecurity_prompt)
        self.cybersecurity_button.grid(row=2, column=0, padx=10, pady=10)

        # Footer Label
        footer_label = tk.Label(self.root, text="Developed by  Grp-19", font=("Arial", 10), bg="#f4f4f4",
                                fg="#283655")
        footer_label.pack(side="bottom", pady=10)

    def record_video(self):
        self.tool.record_video()
        messagebox.showinfo("Info", "Video recorded successfully!")

    def upload_video(self):
        self.tool.upload_video()

    def check_integrity(self):
        if self.tool.video_path is None:
            messagebox.showerror("Error", "No video file available!")
            return
        integrity_hash = self.tool.integrity_check()
        messagebox.showinfo("Integrity Check", f"Integrity Hash: {integrity_hash}")

    def extract_metadata(self):
        if self.tool.video_path is None:
            messagebox.showerror("Error", "No video file available!")
            return
        self.tool.display_metadata()

    def show_cybersecurity_prompt(self):
        messagebox.showinfo("Cybersecurity Prompt",
                            "Remember to regularly check the integrity of your files and avoid downloading videos from untrusted sources to prevent tampering or malware infection.")


if __name__ == "__main__":
    root = tk.Tk()
    app = VideoForensicApp(root)
    root.mainloop()

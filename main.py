from flask import Flask, render_template, request, redirect, url_for
import os
from main_app_course import create_course_structure  # Import from main_app_course
import webbrowser
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QPalette, QColor

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        topic = request.form['topic']
        create_course_structure(topic)  # Generate course structure based on input topic
        return redirect(url_for('course_created', topic=topic))
    return render_template('index.html')

@app.route('/course-created')
def course_created():
    topic = request.args.get('topic')
    
    # Generate the course structure content without saving
    course_content = create_course_structure(topic)
    
    if not course_content or "error" in course_content:
        return f"Error: {course_content.get('error', 'Failed to generate course content.')}", 500
    
    return render_template(
        'course_created.html',
        topic=topic,
        course_outline=course_content.get("course_outline", ""),
        lessons=course_content.get("lessons", []),
        quizzes=course_content.get("quizzes", [])
    )

# Create a custom browser window using PyQt5
class BrowserWindow(QMainWindow):
    def __init__(self, url):
        super().__init__()
        self.setWindowTitle("Flask App Browser")
        self.setWindowFlags(Qt.FramelessWindowHint)  # Frameless window (no close/minimize/maximize buttons)
        
        # Set the palette to remove any background color, ensuring no white borders
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(Qt.black))
        self.setPalette(palette)

        # Create a web view and load the Flask app URL
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl(url))
        
        # Set the layout
        layout = QVBoxLayout()
        layout.addWidget(self.browser)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Set the window to fullscreen (F11-like mode)
        self.showFullScreen()

def run_gui():
    app.run(debug=True, use_reloader=False)

def create_browser_window():
    qt_app = QApplication(sys.argv)
    
    # Create the PyQt5 window with the Flask app URL
    browser_window = BrowserWindow("http://127.0.0.1:5000/")
    
    # Run the PyQt5 application loop
    sys.exit(qt_app.exec_())

if __name__ == '__main__':
    # Run the Flask app and the GUI browser window
    import threading
    flask_thread = threading.Thread(target=run_gui)
    flask_thread.start()

    # Start the PyQt5 browser window
    create_browser_window()

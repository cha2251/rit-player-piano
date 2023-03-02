from PyQt5.QtWidgets import QApplication, QDialog, QProgressBar, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QStackedLayout, QWidget
from src.communication.messages import Message, MessageType
from src.user_interface.home_page import HomePage
from src.user_interface.playing_page import PlayingPage
from src.user_interface.settings_page import SettingsPage
from src.user_interface.ui_comm import UICommSystem

import sys
import os
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QMovie


class WorkerThread(QThread):
    """A worker thread to perform a task that takes time."""
    
    # Define a custom signal that will be emitted during the thread's execution.
    progress_signal = pyqtSignal(int)
    
    def __init__(self):
        super().__init__()
        #self.spinner = LoadingGif()
    
    def run(self):
        """Run the thread."""
        # Perform a task that takes time.
        #self.spinner.startAnimation()
        for i in range(101):
            self.progress_signal.emit(i)
            #self.msleep(1)

        


class LoadingDialog(QDialog):
    """A dialog to display a progress bar and message while a task is running."""
    
    def __init__(self):
        super().__init__()
        
        # Set up the UI elements.
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setAlignment(Qt.AlignCenter)

        
        
        #self.label = QLabel("Loading...", self)
        #self.label.setAlignment(Qt.AlignCenter)
        
        # Set up the layout.
        layout = QVBoxLayout(self)
        layout.addWidget(self.progress_bar)
        #layout.addWidget(self.label)
        
        # Set the dialog properties.
        self.setWindowTitle("Loading")
        self.setFixedSize(250, 75)
        self.setModal(True)
        self.setWindowFlags(Qt.Dialog | Qt.CustomizeWindowHint | Qt.WindowTitleHint)
        
    def update_progress(self, progress):
        """Update the progress bar's value."""
        self.progress_bar.setValue(progress)

class LoadingGif(QWidget):
  
    def __init__(self):
        super().__init__()
        self.setFixedSize(200, 200)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.CustomizeWindowHint)
        self.label_animation = QLabel(self)

  
        # Loading the GIF
        self.movie = QMovie(os.path.join(os.path.dirname(__file__), "..", "..", "UI_Images", "loading_spinner.gif"))
        self.label_animation.setMovie(self.movie)
  
        self.startAnimation()
  
    # Start Animation
  
    def startAnimation(self):
        self.movie.start()
  
    # Stop Animation(According to need)
    def stopAnimation(self):
        self.movie.stop()

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QCheckBox, QTextEdit, QPushButton
import ytm2spt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YouTube to Spotify")
        
        # Create a central widget and set it as the main window's central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        
        # Create layout for the central widget
        layout = QVBoxLayout(central_widget)
        
        # Create input fields
        playlist_label = QLabel("YouTube Playlist Name:")
        self.playlist_input = QLineEdit()
        
        spotify_label = QLabel("Spotify Name:")
        self.spotify_input = QLineEdit()
        
        self.dry_run_checkbox = QCheckBox("Dry Run")
        
        # Create text box to display output
        self.output_textbox = QTextEdit()
        self.output_textbox.setReadOnly(True)
        
        # Create button to run the command
        run_button = QPushButton("Run Command")
        run_button.clicked.connect(self.run_command)
        
        # Add widgets to the layout
        layout.addWidget(playlist_label)
        layout.addWidget(self.playlist_input)
        layout.addWidget(spotify_label)
        layout.addWidget(self.spotify_input)
        layout.addWidget(self.dry_run_checkbox)
        layout.addWidget(self.output_textbox)
        layout.addWidget(run_button)
        
    def run_command(self):
        # Get the input values
        playlist_name = self.playlist_input.text()
        spotify_name = self.spotify_input.text()
        dry_run = self.dry_run_checkbox.isChecked()
        
        # Run the command and display the output in the text box
        command_output = f"Running command with playlist: {playlist_name}, Spotify name: {spotify_name}, Dry run: {dry_run}"
        ytm2spt.main(playlist_name, spotify_name, spotify_name, None, dry_run, False, None)
        self.output_textbox.append(command_output)

# Create the application
app = QApplication(sys.argv)

# Create the main window
window = MainWindow()
window.show()

# Run the event loop
sys.exit(app.exec())
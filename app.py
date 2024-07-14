import os
from shutil import which
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget\
    , QLabel, QLineEdit, QCheckBox, QSpinBox, QTextEdit, QPushButton\
    , QVBoxLayout, QFormLayout, QHBoxLayout, QDialog, QButtonGroup
from PySide6.QtCore import QSettings
import ytm2spt


# {
#   "SPOTIFY_USER_ID": null,
#   "SPOTIFY_CLIENT_ID": null,
#   "SPOTIFY_CLIENT_SECRET": null,
#   "SPOTIFY_REDIRECT_URI": "http://localhost:8888/callback"
# }

SETTINGS = QSettings(QSettings.IniFormat, QSettings.UserScope, "ytm2spt")


def init_settings():
    keys = SETTINGS.allKeys()
    if "SPOTIFY_USER_ID" not in keys:
        SETTINGS.setValue("SPOTIFY_USER_ID", "")
    if "SPOTIFY_CLIENT_ID" not in keys:
        SETTINGS.setValue("SPOTIFY_CLIENT_ID", "")
    if "SPOTIFY_CLIENT_SECRET" not in keys:
        SETTINGS.setValue("SPOTIFY_CLIENT_SECRET", "")
    if "SPOTIFY_REDIRECT_URI" not in keys:
        SETTINGS.setValue("SPOTIFY_REDIRECT_URI", "http://localhost:8888/callback")
    SETTINGS.sync()


class SpotifySettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Spotify Settings")
        self.setMinimumWidth(350)

        layout = QFormLayout(self)

        self.user_id_input = QLineEdit()
        self.user_id_input.setText(SETTINGS.value("SPOTIFY_USER_ID", defaultValue=""))
        # self.user_id_input.setPlaceholderText("This is not email")
        layout.addRow("User ID", self.user_id_input)

        self.client_id_input = QLineEdit()
        self.client_id_input.setText(SETTINGS.value("SPOTIFY_CLIENT_ID", defaultValue=""))
        layout.addRow("Client ID", self.client_id_input)

        self.client_secret_input = QLineEdit()
        self.client_secret_input.setText(SETTINGS.value("SPOTIFY_CLIENT_SECRET", defaultValue=""))
        layout.addRow("Client Secret", self.client_secret_input)

        self.redirect_uri_input = QLineEdit()
        self.redirect_uri_input.setText(SETTINGS.value("SPOTIFY_REDIRECT_URI", defaultValue=""))
        layout.addRow("Redirect URI", self.redirect_uri_input)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_settings)
        layout.addRow(self.save_button)

    def save_settings(self):
        SETTINGS.setValue("SPOTIFY_USER_ID", self.user_id_input.text())
        SETTINGS.setValue("SPOTIFY_CLIENT_ID", self.client_id_input.text())
        SETTINGS.setValue("SPOTIFY_CLIENT_SECRET", self.client_secret_input.text())
        SETTINGS.setValue("SPOTIFY_REDIRECT_URI", self.redirect_uri_input.text())


class YouTubeSettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("YouTube Settings")

        layout = QVBoxLayout(self)

        info_label = QLabel("Only required for private playlists")
        layout.addWidget(info_label)

        self.oauth_button = QPushButton("Get OAuth Token")
        self.oauth_button.clicked.connect(self.get_oauth_token)
        layout.addWidget(self.oauth_button)

        self.message_label = QLabel("")
        layout.addWidget(self.message_label)

    def get_oauth_token(self):
        pass


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YouTube to Spotify")
        
        # Create a central widget and set it as the main window's central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        
        # Create layout for the central widget
        layout = QVBoxLayout(central_widget)

        # Settings buttons
        settings_layout = QHBoxLayout()
        self.sp_settings_button = QPushButton("Spotify Settings")
        self.sp_settings_button.clicked.connect(self.open_spotify_settings)
        settings_layout.addWidget(self.sp_settings_button)

        self.yt_settings_button = QPushButton("YouTube Settings")
        self.yt_settings_button.clicked.connect(self.open_youtube_settings)
        settings_layout.addWidget(self.yt_settings_button)
        layout.addLayout(settings_layout)
        
        # Create input fields
        layout.addWidget(QLabel("YouTube Playlist URL or ID"))
        self.yt_input = QLineEdit()
        layout.addWidget(self.yt_input)
        
        layout.addWidget(QLabel("Spotify Playlist URL or ID"))
        self.sp_input = QLineEdit()
        layout.addWidget(self.sp_input)

        layout.addWidget(QLabel("Spotify Playlist Name"))
        self.spname_input = QLineEdit()
        layout.addWidget(self.spname_input)

        self.create_new_checkbox = QCheckBox("Create New Playlist")
        layout.addWidget(self.create_new_checkbox)

        self.limit_input = QSpinBox()
        self.limit_input.setMinimum(0)
        limit_layout = QFormLayout()
        limit_layout.addRow("Limit", self.limit_input)
        layout.addLayout(limit_layout)
        
        self.dryrun_checkbox = QCheckBox("Dry Run")
        layout.addWidget(self.dryrun_checkbox)
        
        # Create text box to display output
        self.output_textbox = QTextEdit()
        self.output_textbox.setReadOnly(True)
        layout.addWidget(self.output_textbox)
        
        # Create button to run the command
        run_button = QPushButton("Run Command")
        run_button.clicked.connect(self.run_command)
        layout.addWidget(run_button)
        
    def run_command(self):
        # Get the input values
        playlist_name = self.yt_input.text()
        spotify_name = self.sp_input.text()
        dry_run = self.dryrun_checkbox.isChecked()
        
        # Run the command and display the output in the text box
        command_output = f"Running command with playlist: {playlist_name}, Spotify name: {spotify_name}, Dry run: {dry_run}"
        ytm2spt.main(playlist_name, spotify_name, spotify_name, None, dry_run, False, None)
        self.output_textbox.append(command_output)
    
    def open_spotify_settings(self):
        settings_dialog = SpotifySettingsDialog(self)
        settings_dialog.exec()

    def open_youtube_settings(self):
        pass


def guess_terminal() -> str | None:
    """Try to guess terminal."""
    test_terminals = []
    if "WAYLAND_DISPLAY" in os.environ:
        # Wayland-only terminals
        test_terminals += ["foot"]
    test_terminals += [
        "roxterm",
        "sakura",
        "hyper",
        "alacritty",
        "terminator",
        "termite",
        "gnome-terminal",
        "konsole",
        "xfce4-terminal",
        "lxterminal",
        "mate-terminal",
        "kitty",
        "yakuake",
        "tilda",
        "guake",
        "eterm",
        "st",
        "urxvt",
        "wezterm",
        "xterm",
        "x-terminal-emulator",
    ]

    for terminal in test_terminals:
        if not which(terminal, os.X_OK):
            continue
        return terminal

    return None



# Initialize settings
init_settings()

# Create the application
app = QApplication(sys.argv)

# Create the main window
window = MainWindow()
window.setGeometry(100, 100, 400, 600)
window.show()

# Run the event loop
sys.exit(app.exec())
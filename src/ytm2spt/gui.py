import os
import sys
import traceback
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget\
    , QLabel, QLineEdit, QCheckBox, QSpinBox, QTextEdit, QPushButton\
    , QVBoxLayout, QFormLayout, QHBoxLayout, QDialog, QButtonGroup\
    , QRadioButton, QGroupBox, QMessageBox
from PySide6.QtCore import Qt, QSettings, QThread, Signal
from PySide6 import QtCore
from ytmusicapi import setup_oauth

from .transfer import transfer_playlist

SETTINGS = QSettings(QSettings.IniFormat, QSettings.UserScope, "ytm2spt", "config")
YTOAUTH_PATH = os.path.join(os.path.dirname(SETTINGS.fileName()), "oauth.json")


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
    
    if not is_valid_settings():
        settings_dialog = SpotifySettingsDialog()
        settings_dialog.exec()
        if is_valid_settings():
            SETTINGS.sync()
        else:
            SETTINGS.clear()
            exit()


def is_valid_settings():
    return SETTINGS.value("SPOTIFY_USER_ID") != "" \
    and SETTINGS.value("SPOTIFY_CLIENT_ID") != "" \
    and SETTINGS.value("SPOTIFY_CLIENT_SECRET") != "" \
    and SETTINGS.value("SPOTIFY_REDIRECT_URI") != ""


class SpotifySettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Spotify Settings")
        self.setMinimumWidth(350)

        layout = QFormLayout(self)

        info_label = QLabel()
        info_label.setWordWrap(True)
        info_label.setText('<a href="https://github.com/abhishekmj303/ytm2spt?tab=readme-ov-file#spotify-developer-account">Click here for more info</a>')
        info_label.setOpenExternalLinks(True)
        layout.addRow(info_label)

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
        if not is_valid_settings():
            QMessageBox.warning(self, "Error", "Please fill in all fields")
            return
        SETTINGS.sync()
        self.close()


class YouTubeSettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("YouTube Settings")
        self.setMaximumWidth(350)

        layout = QVBoxLayout(self)

        info_label = QLabel("Only required for private playlists")
        layout.addWidget(info_label)

        self.oauth_button = QPushButton("Get OAuth Token")
        self.oauth_button.clicked.connect(self.get_oauth_token)
        layout.addWidget(self.oauth_button)

        self.message_label = QLabel("No OAuth token found")
        self.message_label.setWordWrap(True)
        self.message_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        if os.path.exists(YTOAUTH_PATH):
            self.message_label.setText("OAuth token saved at " + YTOAUTH_PATH)
        layout.addWidget(self.message_label)

    def get_oauth_token(self):
        setup_oauth(filepath=YTOAUTH_PATH, open_browser=True)
        self.message_label.setText("OAuth token saved at " + YTOAUTH_PATH)
        # Qt sleep 3 seconds
        QtCore.QTimer.singleShot(3000, self.close)


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
        
        # YouTube
        yt_group = QGroupBox("YouTube")
        yt_layout = QVBoxLayout(yt_group)
        yt_layout.addWidget(QLabel("Playlist URL or ID"))
        self.yt_input = QLineEdit()
        self.yt_input.textChanged.connect(self.update_command)
        yt_layout.addWidget(self.yt_input)

        self.yt_private_checkbox = QCheckBox("Private Playlist")
        self.yt_private_checkbox.stateChanged.connect(self.yt_private_toggled)
        yt_layout.addWidget(self.yt_private_checkbox)
        layout.addWidget(yt_group)
        
        # Spotify
        self.sp_group = QGroupBox("Spotify (configure)")
        self.sp_group.setCheckable(True)
        self.sp_group.setChecked(False)
        self.sp_group.clicked.connect(self.update_command)
        sp_layout = QVBoxLayout(self.sp_group)

        # Radio buttons for Spotify input choice
        self.spotify_choice_group = QButtonGroup(self)
        self.use_name_radio = QRadioButton("Using Playlist Name (New or Existing)")
        self.use_url_radio = QRadioButton("Using Playlist URL or ID")
        self.spotify_choice_group.addButton(self.use_name_radio)
        self.spotify_choice_group.addButton(self.use_url_radio)
        sp_layout.addWidget(self.use_name_radio)
        sp_layout.addWidget(self.use_url_radio)
        
        # Spotify input widgets
        self.sp_url_label = QLabel("Playlist URL or ID")
        sp_layout.addWidget(self.sp_url_label)
        self.sp_input = QLineEdit()
        self.sp_input.textChanged.connect(self.update_command)
        sp_layout.addWidget(self.sp_input)
        
        self.sp_name_label = QLabel("Playlist Name (Optional)")
        sp_layout.addWidget(self.sp_name_label)
        self.spname_input = QLineEdit()
        # self.spname_input.setPlaceholderText("Default: From YouTube")
        self.spname_input.textChanged.connect(self.update_command)
        sp_layout.addWidget(self.spname_input)
        self.create_new_checkbox = QCheckBox("Create New Playlist")
        self.create_new_checkbox.stateChanged.connect(self.update_command)
        sp_layout.addWidget(self.create_new_checkbox)
        
        # Connect radio buttons to change visibility
        self.use_url_radio.toggled.connect(self.toggle_spotify_inputs)
        self.use_name_radio.toggled.connect(self.toggle_spotify_inputs)

        layout.addWidget(self.sp_group)

        # Other Options
        self.other_group = QGroupBox("Other Options")
        self.other_group.setCheckable(True)
        self.other_group.setChecked(False)
        self.other_group.clicked.connect(self.update_command)
        other_layout = QHBoxLayout(self.other_group)

        self.limit_input = QSpinBox()
        self.limit_input.setRange(0, 1000000)
        self.limit_input.valueChanged.connect(self.update_command)
        limit_layout = QFormLayout()
        limit_layout.addRow("Limit", self.limit_input)
        other_layout.addLayout(limit_layout)
        
        self.dryrun_checkbox = QCheckBox("Dry Run")
        self.dryrun_checkbox.stateChanged.connect(self.update_command)
        other_layout.addWidget(self.dryrun_checkbox)

        layout.addWidget(self.other_group)
        
        # Command
        cmd_group = QGroupBox("Command")
        cmd_layout = QVBoxLayout(cmd_group)

        # Create text box to display command
        self.cmd_textbox = QTextEdit()
        self.cmd_textbox.setReadOnly(True)
        cmd_layout.addWidget(self.cmd_textbox)
        
        # Create button to run the command
        self.run_button = QPushButton("Run Command")
        self.run_button.clicked.connect(self.run_command)
        cmd_layout.addWidget(self.run_button)

        layout.addWidget(cmd_group)

        # Set default selection
        self.use_name_radio.setChecked(True)
        self.toggle_spotify_inputs()
    
    def toggle_spotify_inputs(self):
        use_url = self.use_url_radio.isChecked()
        self.sp_url_label.setVisible(use_url)
        self.sp_input.setVisible(use_url)
        self.sp_name_label.setVisible(not use_url)
        self.spname_input.setVisible(not use_url)
        self.create_new_checkbox.setVisible(not use_url)
        self.update_command()
    
    def update_command(self):
        command = "ytm2spt"
        
        if self.yt_input.text().strip():
            command += f" -yt \"{self.yt_input.text().strip()}\""
        else:
            command = "YouTube playlist URL or ID is required"
            self.cmd_textbox.setText(command)
            return
        
        if self.sp_group.isChecked():
            if self.use_url_radio.isChecked() and self.sp_input.text().strip():
                command += f" -sp \"{self.sp_input.text().strip()}\""
            elif self.use_name_radio.isChecked() and self.spname_input.text().strip():
                command += f" -spname \"{self.spname_input.text().strip()}\""
        
            if self.use_name_radio.isChecked() and self.create_new_checkbox.isChecked():
                command += " -n"
        
        if self.yt_private_checkbox.isChecked():
            command += f' -ytauth "{YTOAUTH_PATH}"'
        
        if self.other_group.isChecked():
            if self.dryrun_checkbox.isChecked():
                command += " -d"
            
            if self.limit_input.value() > 0:
                command += f" -l {self.limit_input.value()}"
        
        self.cmd_textbox.setText(command)
        
    def run_command(self):
        if "Stop" in self.run_button.text():
            self.worker.terminate()
            self.run_button.setText("Run Command")
            return
        else:
            self.run_button.setText("Stop Command")
        # Get the input values
        youtube_arg = self.yt_input.text().strip()
        if not youtube_arg:
            self.cmd_textbox.setText("YouTube playlist URL or ID is required")
            QMessageBox.warning(self, "Error", "Error: Failed to run ytm2spt")
            return
        
        if self.use_url_radio.isChecked():
            spotify_arg = self.sp_input.text().strip()
            spotify_playlist_name = None
        else:
            spotify_arg = None
            spotify_playlist_name = self.spname_input.text().strip()
        
        youtube_oauth = YTOAUTH_PATH if self.yt_private_checkbox.isChecked() else None
        dry_run = self.dryrun_checkbox.isChecked()
        create_new = self.create_new_checkbox.isChecked()
        limit = self.limit_input.value() if self.limit_input.value() > 0 else None

        # Run ytm2spt
        self.worker = RunCommandWorker(youtube_arg, spotify_arg, spotify_playlist_name, youtube_oauth, dry_run, create_new, limit)
        self.worker.completed.connect(self.run_finished)
        self.worker.error.connect(self.run_error)
        self.worker.start()

    def run_finished(self):
        QMessageBox.information(self, "Info", "Finished running ytm2spt")
        self.run_button.setText("Run Command")


    def run_error(self, error):
        self.cmd_textbox.setText("Error running command: " + error)
        QMessageBox.warning(self, "Error", "Error: Failed to run ytm2spt")
        self.run_button.setText("Run Command")

    def open_spotify_settings(self):
        settings_dialog = SpotifySettingsDialog(self)
        settings_dialog.exec()

    def open_youtube_settings(self):
        settings_dialog = YouTubeSettingsDialog(self)
        settings_dialog.exec()
    
    def yt_private_toggled(self):
        self.update_command()
        if self.yt_private_checkbox.isChecked():
            if not os.path.exists(YTOAUTH_PATH):
                self.open_youtube_settings()


class RunCommandWorker(QThread):
    completed = Signal()
    error = Signal(str)

    def __init__(self, youtube_arg, spotify_arg, spotify_playlist_name, youtube_oauth, dry_run, create_new, limit):
        super().__init__()
        self.youtube_arg = youtube_arg
        self.spotify_arg = spotify_arg
        self.spotify_playlist_name = spotify_playlist_name
        self.youtube_oauth = youtube_oauth
        self.dry_run = dry_run
        self.create_new = create_new
        self.limit = limit
    
    def run(self):
        try:
            os.environ["SPOTIFY_USER_ID"] = SETTINGS.value("SPOTIFY_USER_ID")
            os.environ["SPOTIFY_CLIENT_ID"] = SETTINGS.value("SPOTIFY_CLIENT_ID")
            os.environ["SPOTIFY_CLIENT_SECRET"] = SETTINGS.value("SPOTIFY_CLIENT_SECRET")
            os.environ["SPOTIFY_REDIRECT_URI"] = SETTINGS.value("SPOTIFY_REDIRECT_URI")
            transfer_playlist(self.youtube_arg, self.spotify_arg, self.spotify_playlist_name, self.youtube_oauth, self.dry_run, self.create_new, self.limit)
            self.completed.emit()
        except Exception as e:
            print(e)
            print(traceback.format_exc())
            self.error.emit(str(e))


def main():
    # Create the application
    app = QApplication(sys.argv)

    # Initialize settings
    init_settings()

    # Create the main window
    window = MainWindow()
    window.setMinimumWidth(400)
    window.show()

    print("Welcome to ytm2spt!")

    # Run the event loop
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
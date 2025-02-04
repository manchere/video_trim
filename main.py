import os
import sys

from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QSlider, \
    QFileDialog
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from PyQt6.QtMultimediaWidgets import QVideoWidget


class App(QApplication):
    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)
        self.setApplicationDisplayName("Trim Video")


class TrimVideo:
    def __init__(self):
        super(TrimVideo, self).__init__()
        self.video_path = ""
        self.video_duration = 100
        self.start_time = 0
        self.end_time = 100
        self.media_player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self._saved_location = ""

    def ffmpeg_trim(self):
        if self.video_path:
            output_path = os.path.splitext(self.video_path)[0] + "_new.mp4"
            ffmpeg_extract_subclip(self.video_path, self.start_time, self.end_time, targetname=output_path)
            self._saved_location = output_path

    def get_saved_location(self):
        return self._saved_location


class View(QMainWindow):
    def __init__(self):
        super(View, self).__init__()
        self.main_window = QWidget(self)
        self.layout = QVBoxLayout(self.main_window)
        self.setWindowTitle("Trim Video")
        self.setGeometry(100, 100, 800, 500)
        self.video = TrimVideo()

        self.trim_layout = QHBoxLayout()
        self.lbl_validation = QLabel()

        self.lbl_begin = QLabel("Start: 0s")
        self.start_slider = QSlider(Qt.Orientation.Horizontal)
        self.start_slider.setRange(0, 100)
        self.start_slider.valueChanged.connect(self.update_start)

        self.lbl_end = QLabel("End: 100s")
        self.end_slider = QSlider(Qt.Orientation.Horizontal)
        self.end_slider.setRange(0, 100)
        self.end_slider.valueChanged.connect(self.update_end)

        self.btn_load = QPushButton("Load Video")
        self.btn_play = QPushButton("Play")
        self.btn_trim_video = QPushButton("Trim Video")

        self.btn_load.clicked.connect(self.load_video)
        self.btn_play.clicked.connect(self.toggle_play)
        self.btn_trim_video.clicked.connect(self.video.ffmpeg_trim)

        self.video_widget = QVideoWidget()

        self.trim_layout.addWidget(self.lbl_begin)
        self.trim_layout.addWidget(self.start_slider)
        self.trim_layout.addWidget(self.lbl_end)
        self.trim_layout.addWidget(self.end_slider)

        self.video.media_player.setVideoOutput(self.video_widget)
        self.layout.addWidget(self.video_widget, 1)

        self.layout.addLayout(self.trim_layout)
        self.layout.addWidget(self.btn_load)
        self.layout.addWidget(self.btn_play)
        self.layout.addWidget(self.btn_trim_video)
        self.layout.addWidget(self.lbl_validation)

        self.setCentralWidget(self.main_window)

    def load_video(self):
        dialog = QFileDialog()
        video_path, _ = dialog.getOpenFileName(self, "Choose Video", "", "Videos (*.mp4 *.avi *.mov *.mkv)")

        if video_path:
            try:
                self.video.video_path = video_path
                self.video.media_player.setSource(QUrl.fromLocalFile(self.video.video_path))

                # self.video.media_player.mediaStatusChanged.connect(self.update_duration)
                self.video.media_player.play()
            except Exception as e:
                self.lbl_validation.setText(f"error loading video {e}")
                self.lbl_validation.setText("color: red")
            else:
                self.lbl_validation.setText("video loaded")
                self.lbl_validation.setStyleSheet("color: green")


    def update_duration(self):
        print(self.video.media_player.duration())
        if self.video.media_player.duration() > 0:

            self.video.video_duration = self.video.media_player.duration() / 1000
            print(self.video.video_duration)

            self.start_slider.setRange(0, self.video.video_duration)
            self.end_slider.setRange(0, self.video.video_duration)
            self.end_slider.setValue(self.video.video_duration)
            self.video.media_player.mediaStatusChanged.disconnect(self.update_duration)

    def toggle_play(self):
        if self.video.media_player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.video.media_player.pause()
        else:
            self.video.media_player.play()

    def update_start(self, value):
        self.video.start_time = value
        self.lbl_begin.setText(f"Start: {value}s")

    def update_end(self, value):
        self.video.end_time = value
        self.lbl_end.setText(f"End: {value}s")


if __name__ == "__main__":
    app = App(sys.argv)
    view = View()
    view.show()
    sys.exit(app.exec())

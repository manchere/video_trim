import os.path
import sys

from qtpy import QtWidgets, QtCore
from PyQt5.QtMultimedia import QMediaPlayer, QAudioOutput
from qtpy.QtMultimediaWidgets import QVideoWidget
from qtpy.QtCore import Qt, QUrl

from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip  # Trimming function

class App(QtWidgets.QApplication):
    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)
        self.setApplicationDisplayName("trim video")


class TrimVideo:
    def __init__(self):
        super(TrimVideo, self).__init__()
        self.video_path = ""
        self.video_duration = 100  # Default duration
        self.start_time = 0
        self.end_time = 100
        self.media_player = QMediaPlayer()

        self._saved_location = ""

        # self.window = View()

    def ffmpeg_trim(self):
        if self.video_path:
            output_path = os.path.splitext(self.video_path)[0] + "_new.mp4"
            ffmpeg_extract_subclip(self.video_path, self.start_time, self.end_time, targetname=output_path)
            self._saved_location = output_path

    def get_saved_location(self):
        return self._saved_location


class View(QtWidgets.QMainWindow):
    def __init__(self):
        super(View, self).__init__()
        self.main_window = QtWidgets.QWidget(self)
        self.layout = QtWidgets.QVBoxLayout(self.main_window)
        self.setWindowTitle("Trim Video")
        self.setGeometry(100, 100, 800, 100)
        self.video = TrimVideo()

        self.trim_layout = QtWidgets.QHBoxLayout()
        self.lbl_validation = QtWidgets.QLabel()

        self.lbl_begin = QtWidgets.QLabel("Start: 0s")
        self.start_slider = QtWidgets.QSlider(Qt.Orientation.Horizontal)
        self.start_slider.setRange(0, 100)
        self.start_slider.valueChanged.connect(self.update_start)

        self.lbl_end = QtWidgets.QLabel("End: 100s")
        self.end_slider = QtWidgets.QSlider(Qt.Orientation.Horizontal)
        self.end_slider.setRange(0, 100)
        self.end_slider.valueChanged.connect(self.update_end)

        self.btn_trim_video = QtWidgets.QPushButton("trim")
        self.load_button = QtWidgets.QPushButton("Load Video")
        self.play_button = QtWidgets.QPushButton("Play")
        self.trim_button = QtWidgets.QPushButton("Trim Video")

        self.load_button.clicked.connect(self.load_video)
        self.play_button.clicked.connect(self.toggle_play)
        self.trim_button.clicked.connect(self.video.ffmpeg_trim)

        self.video_widget = QVideoWidget()
        self.video.media_player.setVideoOutput(self.video_widget)

        self.trim_layout.addWidget(self.lbl_begin)
        self.trim_layout.addWidget(self.start_slider)
        self.trim_layout.addWidget(self.lbl_end)
        self.trim_layout.addWidget(self.end_slider)

        self.layout.addLayout(self.trim_layout)
        self.layout.addWidget(self.btn_trim_video)
        self.layout.addWidget(self.lbl_validation)

        self.setCentralWidget(self.main_window)

    def load_video(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        options |= QtWidgets.QFileDialog.DontUseCustomDirectoryIcons
        options |= QtWidgets.QFileDialog.ViewMode.List
        dialog = QtWidgets.QFileDialog()
        dialog.setOptions(options)

        video_path, _ = dialog.getOpenFileName(self, "Choose Video", "", "Videos (*.mp4 *.avi *.mov *.mkv)")

        if video_path:
            self.video.video_path = video_path
            self.video.media_player.setSource(QUrl.fromLocalFile(video_path))
            self.media_player.play()

            self.video.video_duration = 100
            self.start_slider.setRange(0, self.video_duration)
            self.end_slider.setRAnge(0, self.video_duration)
            self.video.end_time = self.video_duration

    def toggle_play(self):
        if self.video.media_player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.video.media_player.pause()
        else:
            self.media_player.play()


    def update_start(self, value):
        self.video.start_time = value
        self.start_label.setText(f"Start: {value}s")

    def update_end(self, value):
        self.video.end_time = value
        self.end_label.setText(f"End: {value}s")



if __name__ == "__main__":
    app = App(sys.argv)
    view = View()
    view.show()
    sys.exit(app.exec_())



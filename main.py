import sys

from qtpy import QtWidgets, QtCore
from qtpy.QtMultimedia import QMediaPlayer, QAudioOutput
from qtpy.QtMultimediaWidgets import QVideoWidget
from qtpy.QtCore import Qt, QUrl

from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip  # Trimming function

class TrimVideo(QtWidgets.QApplication):
    def __init__(self, sys_argv):
        super(TrimVideo, self).__init__(sys_argv)
        self.window = View()
        self.setApplicationDisplayName("trim video")




class View(QtWidgets.QMainWindow):
    def __init__(self):
        super(View, self).__init__()
        self.main_window = QtWidgets.QWidget(self)
        self.layout = QtWidgets.QVBoxLayout(self.main_window)
        self.setWindowTitle("Trim Video")
        self.setGeometry(100, 100, 300, 100)

        self.start_trim_layout = QtWidgets.QHBoxLayout()
        self.end_trim_layout = QtWidgets.QHBoxLayout()


        self.lbl_begin = QtWidgets.QLabel("front trim:")
        self.lbl_end = QtWidgets.QLabel("end trim:")

        self.begin_edit = QtWidgets.QTimeEdit()
        self.end_edit = QtWidgets.QTimeEdit()

        self.btn_trim_video = QtWidgets.QPushButton("trim")
        self.load_button = QtWidgets.QPushButton("Load Video")
        self.play_button = QtWidgets.QPushButton("Play")
        self.trim_button = QtWidgets.QPushButton("Trim Video")

        self.video_widget = QVideoWidget()
        self.media_player = QMediaPlayer()
        self.media_player.setVideoOutput(self.video_widget)

        self.start_trim_layout.addWidget(self.lbl_begin)
        self.start_trim_layout.addWidget(self.begin_edit)

        self.end_trim_layout.addWidget(self.lbl_end)
        self.end_trim_layout.addWidget(self.end_edit)

        self.layout.addLayout(self.start_trim_layout)
        self.layout.addLayout(self.end_trim_layout)
        self.layout.addWidget(self.btn_trim_video)


        self.begin_edit.setDisplayFormat("HH:mm:ss")
        self.end_edit.setDisplayFormat("HH:mm:ss")

        self.setCentralWidget(self.main_window)



if __name__ == "__main__":
    app = TrimVideo(sys.argv)
    app.window.show()
    sys.exit(app.exec_())



#!/usr/bin/env python

from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtCore import QCoreApplication, QUrl
import sys

def play_music():
    # Create an application
    app = QCoreApplication(sys.argv)

    # Create a media player
    media_player = QMediaPlayer()
    audio_output = QAudioOutput()
    media_player.setAudioOutput(audio_output)

    # Set the media source (update the file path)
    media_file_path = "/home/adam178/Music/mixed albums/aespa - Lucid Dream.mp3"  # Replace with the actual path to your file
    media_player.setSource(QUrl.fromLocalFile(media_file_path))

    # Play the music
    print("Playing music...")
    media_player.play()

    # Wait until the music finishes
    media_player.mediaStatusChanged.connect(lambda status: app.quit() if status == QMediaPlayer.MediaStatus.EndOfMedia else None)
    sys.exit(app.exec())

if __name__ == "__main__":
    play_music()


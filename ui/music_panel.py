print("music_panel.py loaded")
from pathlib import Path
import os

from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QSpinBox, QPushButton, QFileDialog
)
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput

from modules.audioldm import generate_audio


# ---------- Worker thread -----------------------------------------------------
class AudioGenThread(QThread):
    finished = Signal(str)           # emitted with output WAV path
    error = Signal(str)              # emitted with str(error)

    def __init__(self, prompt: str, length: int):
        super().__init__()
        self.prompt = prompt
        self.length = length
        self.out_path: str | None = None

    def run(self):
        try:
            self.out_path = generate_audio(self.prompt, self.length)
            self.finished.emit(self.out_path)
        except Exception as e:  # pylint: disable=broad-except
            self.error.emit(str(e))


# ---------- Main panel --------------------------------------------------------
class MusicPanel(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        # ── Top controls ───────────────────────────────────────────────────────
        top = QHBoxLayout()
        self.prompt = QLineEdit()
        self.prompt.setPlaceholderText("Describe your music (e.g., 'dark, ambient, synth, no drums')")
        self.prompt.setMinimumWidth(350)

        self.length = QSpinBox()
        self.length.setRange(5, 60)
        self.length.setValue(30)
        self.length.setSuffix(" sec")
        self.length.setFixedWidth(80)

        self.gen_btn = QPushButton("Generate")
        self.gen_btn.setFixedWidth(90)

        top.addWidget(QLabel("Prompt:"))
        top.addWidget(self.prompt, 2)
        top.addWidget(QLabel("Length:"))
        top.addWidget(self.length)
        top.addWidget(self.gen_btn)
        layout.addLayout(top)

        # ── Status / waveform placeholder ─────────────────────────────────────
        self.status = QLabel("Ready.")
        layout.addWidget(self.status)

        wave_box = QVBoxLayout()
        wave_box.addStretch(2)
        self.waveform = QLabel("Waveform will appear here")
        self.waveform.setAlignment(Qt.AlignCenter)
        self.waveform.setStyleSheet(
            "background:#222; color:#aaa; border:1px solid #444; "
            "min-height:60px; min-width:380px;"
        )
        wave_box.addWidget(self.waveform, alignment=Qt.AlignCenter)
        wave_box.addStretch(3)
        layout.addLayout(wave_box)

        # ── Player controls ───────────────────────────────────────────────────
        play_row = QHBoxLayout()
        self.play_btn = QPushButton("Play")
        self.stop_btn = QPushButton("Stop")
        self.open_btn = QPushButton("Open File")
        self.file_label = QLabel("(No file loaded)")

        play_row.addWidget(self.play_btn)
        play_row.addWidget(self.stop_btn)
        play_row.addWidget(self.open_btn)
        play_row.addWidget(self.file_label)
        layout.addLayout(play_row)

        # ── QMediaPlayer setup ────────────────────────────────────────────────
        self.player = QMediaPlayer()
        self.audio_out = QAudioOutput()
        self.player.setAudioOutput(self.audio_out)
        self.filepath: str | None = None

        # ── Signals ───────────────────────────────────────────────────────────
        self.gen_btn.clicked.connect(self.start_generation)
        self.play_btn.clicked.connect(self.play_audio)
        self.stop_btn.clicked.connect(self.player.stop)
        self.open_btn.clicked.connect(self.open_file)

    # --------------------------------------------------------------------- UI
    def start_generation(self):
        prompt = self.prompt.text().strip()
        if not prompt:
            self.status.setText("⚠️  Enter a prompt first.")
            return

        length = self.length.value()
        self.status.setText("⏳ Generating… this may take a few minutes.")
        self.gen_btn.setEnabled(False)

        self.worker = AudioGenThread(prompt, length)
        self.worker.finished.connect(self.generation_done)
        self.worker.error.connect(self.generation_error)
        self.worker.start()

    def generation_done(self, wav_path: str):
        self.gen_btn.setEnabled(True)
        self.status.setText(f"✅ Generated: {Path(wav_path).name}")
        self.file_label.setText(Path(wav_path).name)
        self.filepath = wav_path
        self.player.setSource(wav_path)
        # TODO: draw waveform preview here

    def generation_error(self, err: str):
        self.gen_btn.setEnabled(True)
        self.status.setText(f"❌ Error: {err}")

    # ----------------------------------------------------------------- Player
    def play_audio(self):
        if self.filepath:
            self.player.setSource(self.filepath)
            self.player.play()

    # ------------------------------------------------------------------ Utils
    def open_file(self):
        file, _ = QFileDialog.getOpenFileName(
            self, "Select audio file", "", "Audio Files (*.wav *.mp3)"
        )
        if file:
            self.filepath = file
            self.file_label.setText(Path(file).name)
            self.player.setSource(file)

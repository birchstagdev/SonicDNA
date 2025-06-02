import time
import os
import subprocess
import requests
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

RAW_DIR = os.path.abspath("data/raw")
LM_STUDIO_PATH = r"C:\Users\James\AppData\Local\Programs\LM Studio\LM Studio.exe"
LM_STUDIO_API_URL = "http://localhost:1234"
MODEL_ID = "deepseek-r1-0528-qwen3-8b@q3_k_l"

def is_lm_studio_running():
    try:
        r = requests.get(LM_STUDIO_API_URL, timeout=2)
        return r.status_code == 200
    except Exception:
        return False

def launch_lm_studio():
    print("[Sequence] Launching LM Studio...")
    subprocess.Popen([LM_STUDIO_PATH], shell=True)

def wait_for_lm_studio(timeout=60):
    print("[Sequence] Waiting for LM Studio server to be available...")
    for _ in range(timeout):
        if is_lm_studio_running():
            print("[Sequence] LM Studio server is up!")
            return True
        time.sleep(1)
    print("[Sequence] LM Studio did not start within timeout.")
    return False

def load_model():
    try:
        print(f"[Sequence] Loading model: {MODEL_ID}")
        resp = requests.post(
            f"{LM_STUDIO_API_URL}/v1/models/load",
            json={"model": MODEL_ID}
        )
        if resp.status_code == 200:
            print("[Sequence] Model loaded successfully!")
        else:
            print(f"[Sequence] Error loading model: {resp.text}")
    except Exception as e:
        print(f"[Sequence] Exception loading model: {e}")

class SequenceHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith(".wav"):
            print(f"[Sequence] New WAV created: {event.src_path}")
            self.process(event.src_path)

    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith(".wav"):
            print(f"[Sequence] WAV modified: {event.src_path}")
            self.process(event.src_path)

    def process(self, file_path):
        print(f"[Sequence] Processing {file_path}")
        # TODO: Add AI/worker logic

if __name__ == "__main__":
    print(f"[Sequence] Watching: {RAW_DIR}")

    if not is_lm_studio_running():
        launch_lm_studio()
        if not wait_for_lm_studio():
            print("[Sequence] Failed to connect to LM Studio. Exiting.")
            exit(1)
        time.sleep(3)

    load_model()  # <--- This will try to load your model via API

    event_handler = SequenceHandler()
    observer = Observer()
    observer.schedule(event_handler, path=RAW_DIR, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

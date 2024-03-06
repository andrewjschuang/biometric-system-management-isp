import threading
from recognition.Recognition import Recognition


recognition = Recognition()


def start():
    if not recognition.run:
        recognition.signal_handler(run=True)
        threading.Thread(target=recognition.start).start()


def stop():
    recognition.signal_handler()

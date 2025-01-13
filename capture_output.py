import sys
import threading
from io import StringIO
import time

class ConsoleInterceptor:
    def __init__(self):
        self._stdout = sys.stdout  # Save the original stdout
        self._buffer = StringIO()  # Temporary buffer for intercepted output
        self._lock = threading.Lock()  # Lock for thread safety

    def write(self, message):
        with self._lock:
            self._buffer.write(message)  # Write to the buffer
        self._stdout.write(message)  # Optionally print to the original stdout

    def flush(self):
        self._stdout.flush()  # Ensure flushing of the original stdout

    def start(self):
        sys.stdout = self  # Redirect stdout to this object

    def stop(self):
        sys.stdout = self._stdout  # Restore original stdout

    def get_lines(self):
        """
        Yield new lines as they are written.
        """
        last_position = 0
        while True:
            with self._lock:
                self._buffer.seek(last_position)
                new_data = self._buffer.read()
                last_position = self._buffer.tell()

            if new_data:
                for line in new_data.splitlines():
                    yield line

            # Sleep to avoid tight looping
            time.sleep(0.2)


def capture_output(func_to_run):
    interceptor = ConsoleInterceptor()
    interceptor.start()

    def run_transcription():
        # Simulate transcribe_audio (replace with your actual function)
        func_to_run()

    # Start the transcription in a separate thread
    transcription_thread = threading.Thread(target=run_transcription)
    transcription_thread.start()

    try:
        # Yield lines from the interceptor in real-time
        yield from interceptor.get_lines()
    finally:
        interceptor.stop()
        transcription_thread.join()  # Ensure the thread finishes

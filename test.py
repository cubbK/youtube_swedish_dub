import threading
import time
import sys
import io

# Original black-box function
def print_every_two_seconds_limited(count):
    for _ in range(count):
        print("This message prints every 2 seconds.")
        time.sleep(2)

# Function to capture the output of the black-box function
def capture_output(func, *args, **kwargs):
    # Redirect stdout to a custom StringIO buffer
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()

    # Run the black-box function in a separate thread
    def run_func():
        func(*args, **kwargs)

    thread = threading.Thread(target=run_func)
    thread.start()

    # Capture output in real-time
    try:
        while thread.is_alive():
            sys.stdout.seek(0)
            output = sys.stdout.read()
            sys.stdout.truncate(0)  # Clear the buffer
            sys.stdout.seek(0)
            if output:
                for line in output.splitlines():
                    print(f"Captured in main thread: {line}\n")
            time.sleep(0.1)
    finally:
        thread.join()
        # Capture any remaining output
        sys.stdout.seek(0)
        output = sys.stdout.read()
        sys.stdout = old_stdout
        if output:
            for line in output.splitlines():
                print(f"Captured in main thread: {line}\n")
        print("Thread has finished execution.")

# Main function to test
def main():
    capture_output(print_every_two_seconds_limited, 5)

if __name__ == "__main__":
    main()

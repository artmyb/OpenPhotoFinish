import subprocess
import time
import os

os.environ['PATH'] += os.pathsep + r"C:\Users\mybas\PycharmProjects\photofinish\platform-tools"
print(os.environ['PATH'])

# Define ADB paths
adb_path = "adb"  # Path to ADB executable if not in system PATH


def start_recording():
    try:
        # Start the camera app
        subprocess.run(['adb', 'shell', 'am', 'start', '-a', 'android.media.action.VIDEO_CAPTURE'], check=True)
        time.sleep(5)  # Give the user time to start recording manually
        print("Recording has started. Please stop it manually.")

        # You might want to run this indefinitely or a set amount of time
        # For now, it will just wait for user input to stop the script
        input("Press Enter to exit the script and stop recording...")

    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

def stop_recording():
    # Stop the camera app (not graceful)
    subprocess.run(['adb', 'shell', 'am', 'force-stop', 'com.android.camera'])  # Replace with your camera app's package name


start_recording()  # Start video recording
time.sleep(10)  # Record for 10 seconds (or any desired duration)
stop_recording()  # Stop recording
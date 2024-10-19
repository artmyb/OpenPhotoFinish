import numpy as np
import soundfile as sf

# Sampling rate
sr = 44100
# Duration of the sound in seconds
duration = 60 * 60  # 2 minutes for demonstration
# Initialize the data array with zeros
data = np.zeros(sr * duration)

# Parameters for the waves
square_wave_duration = 0.1  # in seconds
interval = 2  # every two seconds

def generate_square_wave(freq, duration, sr):
    t = np.linspace(0, duration, int(sr * duration), endpoint=False)
    return 0.5 * (1 + np.sign(np.sin(2 * np.pi * freq * t)))

def generate_sine_wave(freq, duration, sr):
    t = np.linspace(0, duration, int(sr * duration), endpoint=False)
    return np.sin(2 * np.pi * freq * t)

for t in range(0, duration, interval):
    # Original square wave (200 Hz)
    start_idx = t * sr
    end_idx = start_idx + int(square_wave_duration * sr)
    if end_idx < len(data):
        data[start_idx:end_idx] = generate_square_wave(200, square_wave_duration, sr)

    # Sine wave starting 0.5 seconds after the 200 Hz wave (500 Hz + 50 Hz each minute, constant frequency within the minute)
    offset = 0.5  # 0.5 seconds after
    freq_base = 500
    freq_increase = 50  # 50 Hz increase each minute
    current_minute = (t // 60)
    freq = freq_base + freq_increase * current_minute
    start_idx = int((t + offset) * sr)
    end_idx = start_idx + int(square_wave_duration * sr)
    if end_idx < len(data):
        data[start_idx:end_idx] = generate_sine_wave(freq, square_wave_duration, sr)

    # Sine wave starting 1 second after the original wave (500 Hz + 100 Hz every 2 seconds, reset every minute)
    offset = 1  # 1 second after
    freq_base = 500
    freq_increase = 100 / 2  # 100 Hz increase every 2 seconds
    current_interval = (t % 60) // 2
    freq = freq_base + freq_increase * current_interval
    start_idx = int((t + offset) * sr)
    end_idx = start_idx + int(square_wave_duration * sr)
    if end_idx < len(data):
        data[start_idx:end_idx] = generate_sine_wave(freq, square_wave_duration, sr)

# Write the signal to a WAV file
sf.write("signal.wav", data, sr)

import pyaudio
import wave
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk) 
import threading
class Recording(pyaudio.PyAudio):
    def __init__(self, config):
        super().__init__()
        self.FORMAT = pyaudio.paInt16
        self.FRAMES_PER_BUFFER = int(config["Audio Configuration"]["frames_per_buffer"])
        self.RATE = int(config["Audio Configuration"]["rate"])
        self.CHANNELS = int(config["Audio Configuration"]["channels"])
        self.recording = False
    def print_config(self):
        print("FRAMES_PER_BUFFER: ", self.FRAMES_PER_BUFFER)
        print("RATE: ", self.RATE)
        print("CHANNELS: ", self.CHANNELS)
    
    def start_recording(self):
        self.print_config()
        self.stream = self.open(format=self.FORMAT, frames_per_buffer=self.FRAMES_PER_BUFFER, rate=self.RATE, channels=self.CHANNELS, input=True)
        # seconds = 5
        self.frames = [] #store the buffer
        # TOTAL_BUFFER_COUNT = self.RATE/self.FRAMES_PER_BUFFER*seconds
        # for buffer in range(0, int(TOTAL_BUFFER_COUNT)):
        #     data = stream.read(self.FRAMES_PER_BUFFER)
        #     frames.append(data)
        # stream.stop_stream()
        # stream.close()
        self.recording = True
        self.record_thread = threading.Thread(target=self.record)
        self.record_thread.start()
        print("Started recording...")
        # Set the parameters of the output file
    
    def record(self):
        while self.recording:
            data = self.stream.read(self.FRAMES_PER_BUFFER)
            self.frames.append(data)
    def stop_recording(self):
        self.recording = False
        self.record_thread.join()
        self.stream.stop_stream()
        self.stream.close()
        self.set_output_file(self.frames)
        print("Ended recording...")
    def set_output_file(self, frames):
        obj = wave.open("output.wav", "wb")
        obj.setframerate(self.RATE)
        obj.setnchannels(self.CHANNELS)
        obj.setsampwidth(self.get_sample_size(self.FORMAT))
        obj.writeframes(b"".join(frames))
        obj.close()
    def show_wave(self, master_frame):
        obj = wave.open("output.wav", "rb")
        signal_array = np.frombuffer(obj.readframes(-1), dtype=np.int16)
        total_duration = obj.getnframes() / obj.getframerate() # no. of samples / sample frequency
        times = np.linspace(0, total_duration, num=len(signal_array))

        # Figure for plotting the signal
        fig = Figure(figsize = (5,5), dpi= 100)

        plt1 = fig.add_subplot(111)
        plt1.plot(times,signal_array)
        plt1.set_title(f"Audio Signal of output.wav")
        plt1.set_ylabel("Signal Wave")
        plt1.set_xlabel("Time in Seconds")
        plt1.set_xlim(0, total_duration)
        
        # Figure Canvas for us to draw the figure inside Tkinter
        canvas = FigureCanvasTkAgg(fig, master = master_frame)
        obj.close()
        return canvas
    
    def open_file(self, buffer, master_frame):
        filename = buffer.split("/")[-1]
        obj = wave.open(buffer, "rb")
        signal_array = np.frombuffer(obj.readframes(-1), dtype=np.int16)
        total_duration = obj.getnframes() / obj.getframerate() # no. of samples / sample frequency
        times = np.linspace(0, total_duration, num=len(signal_array))
        
        fig = Figure(figsize = (5,5), dpi= 100)

        plt1 = fig.add_subplot(111)
        plt1.plot(times,signal_array)
        plt1.set_title(f"Audio Signal of {filename}")
        plt1.set_ylabel("Signal Wave")
        plt1.set_xlabel("Time in Seconds")
        plt1.set_xlim(0, total_duration)
        
        canvas = FigureCanvasTkAgg(fig, master = master_frame)
        print("framerate: ", obj.getframerate())
        print("n frames: ", obj.getnframes())
        print("duration: ", obj.getnframes() / obj.getframerate())

        obj.close()
        return canvas


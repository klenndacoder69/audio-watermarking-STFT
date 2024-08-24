import configparser
import tkinter as tk
import record
import customtkinter
from tkinter import filedialog

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("dark-blue")

class App(customtkinter.CTk):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.record = record.Recording(config)
        self.title("Lorem Ipsum")
        self.geometry(f"{config['Window']['size']}")
        self.resizable(False, False)  # remove if you want to resize

        # Sidebar frame
        self.sidebar = customtkinter.CTkFrame(master=self, width=200)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)

        # Sidebar options
        self.settings_button = customtkinter.CTkButton(master=self.sidebar, text="Settings", command=self.show_settings)
        self.settings_button.pack(pady=10, padx=20)

        # Recording frame
        self.recording_frame = customtkinter.CTkFrame(master=self)
        self.recording_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Matplotlib frame
        self.plot_frame = customtkinter.CTkFrame(master=self.recording_frame, width=500, height=300)
        self.plot_frame.propagate(False) # creates a fixed parent sized plot frame
        self.plot_frame.pack(pady=30)

        # Recording options
        self.start_recording_button = customtkinter.CTkButton(master=self.recording_frame, text="Start Recording", command=self.start_recording)
        self.start_recording_button.pack(pady=20)

        self.stop_recording_button = customtkinter.CTkButton(master=self.recording_frame, text="Stop Recording", command=self.stop_recording)
        self.stop_recording_button.pack(pady=20)

        self.open_file_button = customtkinter.CTkButton(master=self.recording_frame, text="Open File", command=self.open_file)
        self.open_file_button.pack(pady=20)


    def show_settings(self):
        # Clear frames
        for widget in self.recording_frame.winfo_children():
            widget.destroy()

        # Settings frame
        self.settings_frame = customtkinter.CTkFrame(master=self.recording_frame)
        self.settings_frame.pack(fill=tk.BOTH, expand=True)

        # Settings frame options
        frames_per_buffer_label = customtkinter.CTkLabel(master=self.settings_frame, text="Frames per Buffer:")
        frames_per_buffer_label.pack(pady=10)

        self.frames_per_buffer_var = tk.StringVar()
        self.frames_per_buffer_var.set(self.config['Audio Configuration']['frames_per_buffer'])
        frames_per_buffer_menu = customtkinter.CTkOptionMenu(master=self.settings_frame, variable=self.frames_per_buffer_var, values=["3200", "6400", "12800"])
        frames_per_buffer_menu.pack(pady=10)

        rate_label = customtkinter.CTkLabel(master=self.settings_frame, text="Sample Rate:")
        rate_label.pack(pady=10)

        self.rate_var = tk.StringVar()
        self.rate_var.set(self.config['Audio Configuration']['rate'])
        rate_menu = customtkinter.CTkOptionMenu(master=self.settings_frame, variable=self.rate_var, values=["16000", "32000", "44100"])
        rate_menu.pack(pady=10)

        channels_label = customtkinter.CTkLabel(master=self.settings_frame, text="Number of Channels:")
        channels_label.pack(pady=10)

        self.channels_var = tk.StringVar()
        self.channels_var.set(self.config['Audio Configuration']['channels'])
        channels_menu = customtkinter.CTkOptionMenu(master=self.settings_frame, variable=self.channels_var, values=["1", "2"])
        channels_menu.pack(pady=10)

        save_button = customtkinter.CTkButton(master=self.settings_frame, text="Save", command=self.save_settings)
        save_button.pack(pady=20)

        back_button = customtkinter.CTkButton(master=self.settings_frame, text="Back", command=self.show_recording)
        back_button.pack(pady=10)

    def save_settings(self):
        self.config['Audio Configuration']['frames_per_buffer'] = self.frames_per_buffer_var.get()
        self.config['Audio Configuration']['rate'] = self.rate_var.get()
        self.config['Audio Configuration']['channels'] = self.channels_var.get()

        # Re-write config file
        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)

        self.record = record.Recording(self.config)

    def show_recording(self):

        for widget in self.recording_frame.winfo_children():
            widget.destroy()

        # Re-add the recording frame
        self.reset_widgets()

    def start_recording(self):
        self.record.start_recording()
        canvas = self.record.show_wave(master_frame=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH)
    def stop_recording(self):
        print("stop recording")
        
    def open_file(self):
        for widget in self.plot_frame.winfo_children():
            widget.destroy()
        # buffer = filedialog.askopenfile(mode='r', filetypes=[('Audio Files', ".wav")])
        buffer = filedialog.askopenfilename(filetypes=[('Audio Files', ".wav")])
        canvas = self.record.open_file(buffer=buffer, master_frame=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH)

    def reset_widgets(self):
        self.plot_frame = customtkinter.CTkFrame(master=self.recording_frame, width=500, height=300)
        self.plot_frame.propagate(False) # creates a fixed parent sized plot frame
        self.plot_frame.pack(pady=30)

        self.start_recording_button = customtkinter.CTkButton(master=self.recording_frame, text="Start Recording", command=self.start_recording)
        self.start_recording_button.pack(pady=20)

        self.stop_recording_button = customtkinter.CTkButton(master=self.recording_frame, text="Stop Recording", command=self.stop_recording)
        self.stop_recording_button.pack(pady=20)

        self.open_file_button = customtkinter.CTkButton(master=self.recording_frame, text="Open File", command=self.open_file)
        self.open_file_button.pack(pady=20)

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("config.ini")
    app = App(config)
    app.mainloop()

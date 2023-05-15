import socket
import tkinter as tk
import threading
import os
from tkinter import ttk

class Downloader:
    def __init__(self, url, output_path):
        self.url = url
        self.host = self.get_host()
        self.path = self.get_path()
        self.output_path = output_path

    def get_host(self):
        # Extract the host name from the URL
        return self.url.split('/')[2]

    def get_path(self):
        # Extract the path from the URL
        return '/' + '/'.join(self.url.split('/')[3:])

    def download(self, progress_callback):
        # Open a TCP socket connection to the web server
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(f"Connecting to {self.host}...")
        s.connect((self.host, 80))
        print(f"Connected to {self.host}.")

        # Send an HTTP GET request to the server
        request = f"GET {self.path} HTTP/1.1\r\nHost: {self.host}\r\nAccept:text/html\r\n\r\n"
        s.send(request.encode())

        # Receive the response from the server
        response = ''
        total_length = 0
        while True:
            data = s.recv(1024)
            if not data:
                break
            response += data.decode('utf-8', errors='replace')
            total_length += len(data)
            progress_callback(total_length)

        # Close the socket connection
        s.close()

        # Save the response to a file
        try:
            with open(self.output_path, "w", encoding="utf-8") as f:
                content = response.split('\r\n\r\n')[1]
                print(f"Writing {len(content)} bytes to file...")
                f.write(content)
                print("File write completed successfully!")
        except Exception as e:
            print(f"Error writing file: {e}")

class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("400x200")
        self.root.title("Web Page Downloader")

        self.url_label = tk.Label(self.root, text="Enter URL:")
        self.url_label.pack()

        self.url_entry = tk.Entry(self.root)
        self.url_entry.pack()

        self.output_path_label = tk.Label(self.root, text="Enter Output Path:")
        self.output_path_label.pack()

        self.output_path_entry = tk.Entry(self.root)
        self.output_path_entry.pack()

        self.progress_bar = ttk.Progressbar(self.root, length=200, mode="determinate", style="custom.Horizontal.TProgressbar")
        self.progress_bar.pack(pady=10)

        self.result_label = tk.Label(self.root, text="", font=("Arial", 14))
        self.result_label.pack(pady=10)

        self.download_button = tk.Button(self.root, text="Download", command=self.download)
        self.download_button.pack()

        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('custom.Horizontal.TProgressbar', troughcolor='#bfbfbf', bordercolor='#bfbfbf', background='#1caad9', lightcolor='#1caad9', darkcolor='#1caad9')

        self.root.mainloop()

    def download(self):
        url = self.url_entry.get()
        output_path = self.output_path_entry.get()

        # Validate the output path
        if not os.path.isabs(output_path):
            self.result_label.config(text="Invalid output path. Please provide an absolute path.")
            return

        # Create the directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        downloader = Downloader(url, output_path)
        t = threading.Thread(target=downloader.download, args=(self.update_progress,))
        t.start()

    def update_progress(self, total_length):
        self.progress_bar["value"] = total_length

        # Update the progress bar
        self.progress_bar.update()

        # Check if download is complete
        if total_length >= self.progress_bar["maximum"]:
            self.result_label.config(text="Download complete!")
        else:
            self.result_label.config(text="Downloading...")

if __name__ == '__main__':
    gui = GUI()

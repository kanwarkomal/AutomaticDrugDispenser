import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import cv2
from pyzbar.pyzbar import decode
import json
# from test1 import function_motor1, function_motor2, function_motor3, function_motor4
import re
import time


class QRScannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("QR Code Scanner")
        #self.medicine_data = None  #Initialize medicine_data as None
        #self.qr_code_frame = qr_code_frame
        
        

        
        # Create a frame for holding the QR code scanner
        self.qr_frame = ttk.Frame(root)
        self.qr_frame.pack(padx=10, pady=10)

        # Create a label to display the "Scan the QR code" statement
        self.scan_label = ttk.Label(self.qr_frame, text="Scan the QR code", font=("Arial", 16))
        self.scan_label.pack(pady=10)

        # Create a label to display the camera feed
        self.camera_label = ttk.Label(self.qr_frame)
        self.camera_label.pack(pady=10)

        

        # Initialize camera capture
        self.cap = cv2.VideoCapture(0)
        self.show_camera_feed()
        
        #dictionary to map ids to name 
        self.id_to_name = {
            2: "Amritarishta",
            8: "Balarishta",
            9: "Chandanasava",
            11: "Drakshasava"
        }
        self.qr_scanned =False
            

    def show_camera_feed(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(frame)
            image = ImageTk.PhotoImage(image)
            self.camera_label.configure(image=image)
            self.camera_label.image = image
        self.start_scanning()
        self.root.after(10, self.show_camera_feed)

    def start_scanning(self):
        ret, frame = self.cap.read()
        if ret:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            decoded_objects = decode(gray)
            for obj in decoded_objects:
                qr_data = obj.data.decode('utf-8')
                print("QR Code Data:", qr_data)
                # Redirect to the QR data page
                self.redirect_to_qr_data_page(qr_data)
                self.qr_scanned = True
                break

   
    def redirect_to_qr_data_page(self, qr_data):
        # Hide the current frame
        self.qr_frame.pack_forget()

        # Display the QR data in the data frame
        self.display_qr_data(qr_data)
        
    def extract_medicines(self, qr_data):
        medicines = re.findall(r'Md\(id=(.*?), q=(\d+), p=(\d+)', qr_data)
        
        medicine_data = {}
        
        for medicine in medicines:
            id, quantity, price = map(int,medicine)
            name=self.id_to_name.get(id,'Unknown')
            medicine_data[name] = {"quantity": quantity, "id": id, "price":price}
            
        return medicine_data
            

    def display_qr_data(self, qr_data):
        
        self.medicine_data = self.extract_medicines(qr_data)

        # Create a list to hold the data for each row in the table
        data = []
        
        total_sum = 0

        # Insert rows based on medicine data and populate the data list
        for medicine_name, medicine_info in self.medicine_data.items():
            quantity = medicine_info.get('quantity', 'N/A')
            price= medicine_info.get('price', 'N/A')
            data.append([medicine_name, quantity, price])
            total_sum += quantity*price
            print(total_sum)

        # Determine the maximum number of rows required for the table
        #max_rows = max(len(self.medicine_data), 1)

        # Create a frame for displaying QR data
        self.qr_data_frame = ttk.Frame(self.root)
        self.qr_data_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Create a treeview to display the data
        tree = ttk.Treeview(self.qr_data_frame, columns=('Medicine Name', 'Quantity', 'Price'))
        tree.heading('#0', text='Item')
        tree.heading('#1', text='Medicine Name')
        tree.heading('#2', text='Quantity')
        tree.heading('#3', text='Price')
        tree.column('#0', stretch=tk.YES, minwidth=30, width=70)
        tree.column('#1', stretch=tk.YES, minwidth=30, width=70)
        tree.column('#2', stretch=tk.YES, minwidth=30, width=70)
        tree.column('#3', stretch=tk.YES, minwidth=30, width=70)

        # Insert rows based on medicine data
        for row in data:
                
         tree.insert('', 'end', text='Data', values=row)

        tree.pack(padx=10, pady=10, side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Calculate the total amount to pay
        #total_sum = sum(int(row[1]) * int(row[2]) for row in data[1:])  # Skip the header row

        # Display the total amount below the table
        #ttk.Label(self.qr_data_frame, text=f"Total Amount to Pay: {total_sum}").pack()

        # Create a frame for displaying QR code
        qr_code_frame = ttk.Frame(self.root)
        qr_code_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Display payment QR code label
        ttk.Label(qr_code_frame, text="Payment QR Code").pack()

        # Display payment QR code image
        qr_image = Image.open('aadharfront.jpg')
        self.qr_photo = ImageTk.PhotoImage(qr_image)
        qr_label = ttk.Label(qr_code_frame, image=self.qr_photo)
        qr_label.image = self.qr_photo
        qr_label.pack(padx=10, pady=10)
            
        # Create and configure the Dispense Medicine button
        dispense_button = ttk.Button(qr_code_frame, text="Dispense Medicine", command=lambda: self.dispense_medicine(self.medicine_data))
        dispense_button.pack(pady=5)

        
        
    def dispense_medicine(self,medicine_data):
        # Add logic to dispense medicine here
        
        if'Amritarishta' in medicine_data:
           repeat_times1 = medicine_data['Amritarishta'].get('quantity', 0)
           print(repeat_times1)
           for _ in range(repeat_times1):
            # function_motor1(repeat_times1)
            print("amritarishta dispensed!")
        
        if'Balarishta' in medicine_data:
           repeat_times2 = medicine_data['Balarishta'].get('quantity', 0)
           for _ in range(repeat_times2):
            # function_motor2(repeat_times2)
             print("ashokarishta dispensed!")
        
        if'Chandrasava' in medicine_data:
           repeat_times3 = medicine_data['Chandrasava'].get('quantity', 0)
           for _ in range(repeat_times3):
            # function_motor3(repeat_times3)
             print("ashokarishta dispensed!")
        
        if'Darkshasava' in medicine_data:
           repeat_times4 = medicine_data['Darkshasava'].get('quantity', 0)
           for _ in range(repeat_times4):
            # function_motor4(repeat_times4)
            print("ashokarishta dispensed!")
        
            # Hide all frames
        for widget in self.root.winfo_children():
            widget.destroy()

        # Display the "Thank You" message on the whole screen
        thank_you_frame = ttk.Frame(self.root)
        thank_you_frame.pack(fill='both', expand=True)
        ttk.Label(thank_you_frame, text="Thank You!", font=("Arial", 20)).pack(expand=True)

        self.root.after(5000, self.restart_app)
        root.bind("<Escape>", lambda e:root.destroy())
        
        

if __name__ == "__main__":
    root = tk.Tk()
    app = QRScannerApp(root)
    while True:
        root.attributes('-fullscreen', True)
        root.bind("<Escape>", lambda e:root.destroy())
        root.mainloop()


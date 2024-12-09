
import customtkinter as ctk
import time
from tkinter import ttk

class InventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Finder")
        self.root.geometry("1020x600")

        self.rfid_code = '010101ff'  # This is a placeholder
        self.countdown_job = None  # Keep track of the countdown job
        self.localization_job = None  # Keep track of the localization countdown job
        self.starting_page()

    def starting_page(self):
        """Starting page with buttons to begin scan object or scan box flow."""
        self.clear_frame()

        # Title
        label = ctk.CTkLabel(self.root, text="Starting Page", font=ctk.CTkFont(size=24))
        label.pack(pady=20)

        # Buttons for Scan Object and Scan Box
        scan_object_btn = ctk.CTkButton(self.root, text="Scan Object", font=ctk.CTkFont(size=20), width=300, height=60, command=self.scanning_page)
        scan_object_btn.pack(pady=10)

        scan_box_btn = ctk.CTkButton(self.root, text="Scan Box", font=ctk.CTkFont(size=20), width=300, height=60, command=self.scan_box_page)
        scan_box_btn.pack(pady=10)

        new_object_btn = ctk.CTkButton(self.root, text="New Object", font=ctk.CTkFont(size=20), width=300, height=60)
        new_object_btn.pack(pady=10)

        change_location_btn = ctk.CTkButton(self.root, text="Change Box Location", font=ctk.CTkFont(size=20), width=300, height=60)
        change_location_btn.pack(pady=10)

    # ---- Scan Object Flow ----

    def scanning_page(self):
        """This method will handle the 'Scan Object' functionality."""
        self.clear_frame()

        # Display countdown for starting object scanning
        self.countdown_label = ctk.CTkLabel(self.root, text="Starting object scanning in 3, 2, 1...", font=ctk.CTkFont(size=24))
        self.countdown_label.pack(pady=20)

        # Start the countdown and transition to the next phase
        self.countdown(3)

        # Add bottom buttons (scan type = object)
        self.add_bottom_buttons(scan_type="object")

    def countdown(self, count):
        """Countdown for object scanning."""
        if count > 0 and self.countdown_label.winfo_exists():
            self.countdown_label.configure(text=f"Starting object scanning in {count}...")
            self.countdown_job = self.root.after(1000, self.countdown, count - 1)
        else:
            self.taking_pictures_page()

    def taking_pictures_page(self):
        """Simulate taking pictures."""
        self.clear_frame()

        # Progress bar for taking pictures
        label = ctk.CTkLabel(self.root, text="Taking pictures...", font=ctk.CTkFont(size=24))
        label.pack(pady=20)

        progress = ttk.Progressbar(self.root, orient='horizontal', mode='determinate', length=300)
        progress.pack(pady=10)

        self.update_progress(progress)

        # Add bottom buttons (scan type = object)
        self.add_bottom_buttons(scan_type="object")

    def update_progress(self, progress):
        """Simulate progress for taking pictures."""
        progress['value'] += 20
        if progress['value'] < 100:
            self.root.after(500, self.update_progress, progress)
        else:
            self.evaluating_pictures_page()

    def evaluating_pictures_page(self):
        """Evaluating pictures after taking them."""
        self.clear_frame()

        # Evaluating pictures with a loading icon
        label = ctk.CTkLabel(self.root, text="Evaluating pictures...", font=ctk.CTkFont(size=24))
        label.pack(pady=20)

        loading_label = ctk.CTkLabel(self.root, text="⌛", font=ctk.CTkFont(size=24))  # Simulated spinner/loading icon
        loading_label.pack(pady=10)

        self.root.after(2000, self.starting_page)  # Return to the starting page after a delay

        # Add bottom buttons (scan type = object)
        self.add_bottom_buttons(scan_type="object")

    # ---- Scan Box Flow ----

    def scan_box_page(self):
        """Hold box on the RFID Reader page for scan box path."""
        self.clear_frame()

        # Message to hold box on the RFID Reader
        label = ctk.CTkLabel(self.root, text="Hold box on the RFID Reader\n\nScanning...", font=ctk.CTkFont(size=24))
        label.pack(pady=20)

        # Simulate scanning delay before transitioning to searching
        self.root.after(2000, self.searching_for_box_page)

        # Add bottom buttons (scan type = box)
        self.add_bottom_buttons(scan_type="box")

    def searching_for_box_page(self):
        """Searching for box with loading spinner."""
        self.clear_frame()

        # Message to indicate searching
        label = ctk.CTkLabel(self.root, text="Searching for box...", font=ctk.CTkFont(size=24))
        label.pack(pady=20)

        # Add a spinning/loading icon (represented by "" here, you can customize this)
        loading_label = ctk.CTkLabel(self.root, text="", font=ctk.CTkFont(size=24))
        loading_label.pack(pady=10)

        # Simulate a short delay for the search process
        self.root.after(2000, self.box_found_page)

        # Add bottom buttons (scan type = box)
        self.add_bottom_buttons(scan_type="box")

    def box_found_page(self):
        """Box found page with localization countdown."""
        self.clear_frame()

        # Display that the box is found
        label = ctk.CTkLabel(self.root, text="Box Found!", font=ctk.CTkFont(size=24))
        label.pack(pady=10)

        # Simulate displaying a box image or label
        box_image = ctk.CTkLabel(self.root, text="[Box Image Placeholder]", font=ctk.CTkFont(size=24))
        box_image.pack(pady=10)

        box_name = ctk.CTkLabel(self.root, text="Box Name: Example Box", font=ctk.CTkFont(size=20))
        box_name.pack(pady=10)

        # Start localization countdown in 3 seconds
        localization_label = ctk.CTkLabel(self.root, text="Localization starting in 3, 2, 1...", font=ctk.CTkFont(size=20))
        localization_label.pack(pady=10)

        # Delay before starting localization process
        self.root.after(3000, self.localization_page)

        # Add bottom buttons (scan type = box)
        self.add_bottom_buttons(scan_type="box")

    def localization_page(self):
        """Localization process with countdown timer."""
        self.clear_frame()

        # Display localization message
        label = ctk.CTkLabel(self.root, text="Localization end in 60s", font=ctk.CTkFont(size=24))
        label.pack(pady=10)

        # Simulate a 60-second countdown timer for localization
        self.localization_countdown_label = ctk.CTkLabel(self.root, text="60", font=ctk.CTkFont(size=20))
        self.localization_countdown_label.pack(pady=10)

        self.localization_countdown(60)

        # Add bottom buttons (scan type = box, with or without Go Now button)
        self.add_bottom_buttons(scan_type="box", extra_button=True)

    def localization_countdown(self, count):
        """Count down for 60 seconds and update the label."""
        if count > 0 and self.localization_countdown_label.winfo_exists():
            self.localization_countdown_label.configure(text=str(count))
            self.localization_job = self.root.after(1000, self.localization_countdown, count - 1)
        else:
            self.starting_page()  # After the countdown, go back to the starting page.

    # ---- General Functions ----

    def add_bottom_buttons(self, scan_type="box", extra_button=False):
        """This method adds the bottom buttons for exit and scan."""
        button_frame = ctk.CTkFrame(self.root)
        button_frame.pack(side="bottom", fill="x", padx=20, pady=10)

        exit_button = ctk.CTkButton(button_frame, text="X", font=ctk.CTkFont(size=20), command=self.starting_page, width=80)
        exit_button.pack(side="left", padx=10)

        if scan_type == "object":
            scan_button = ctk.CTkButton(button_frame, text="Scan Object", font=ctk.CTkFont(size=20), command=self.scanning_page, width=200)
        else:
            scan_button = ctk.CTkButton(button_frame, text="Scan Box", font=ctk.CTkFont(size=20), command=self.scan_box_page, width=200)

        scan_button.pack(side="right", padx=10)

        if extra_button:
            # Add the "Go Now" button during localization
            go_now_button = ctk.CTkButton(button_frame, text="Go Now", font=ctk.CTkFont(size=20), command=self.starting_page, width=150)
            go_now_button.pack(side="right", padx=10)

    def clear_frame(self):
        """Clear all the widgets from the root window and cancel any pending jobs."""
        if self.countdown_job:
            self.root.after_cancel(self.countdown_job)
            self.countdown_job = None
        if self.localization_job:
            self.root.after_cancel(self.localization_job)
            self.localization_job = None

        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = ctk.CTk()
    app = InventoryApp(root)
    root.mainloop()
















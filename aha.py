import tkinter as tk
from tkinter import messagebox

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DELA CRUZ STORE INVENTORY MANAGEMENT SYSTEM")
        
        # Gawing Full Screen
        self.root.attributes("-fullscreen", True)
        
        # Kunin ang lapad at taas ng screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Main Canvas para sa Gradient Background
        self.canvas = tk.Canvas(self.root, width=screen_width, height=screen_height, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.draw_gradient(screen_width, screen_height)

        # Posisyon sa gitna ng screen
        cx, cy = screen_width // 2, screen_height // 2

        # Header Title & Cart Icon (Diretso nang naka-canvas para walang puting background box)
        self.canvas.create_text(
            cx - 260, 80, 
            text="🛒", 
            fill="white", 
            font=("Arial", 28)
        )
        self.canvas.create_text(
            cx + 40, 80, 
            text="DELA CRUZ STORE INVENTORY MANAGEMENT SYSTEM", 
            fill="white", 
            font=("Arial", 22, "bold")
        )

        # User Icon / Avatar Circle (Nasa itaas ng USER LOGIN)
        self.canvas.create_oval(cx - 25, cy - 155, cx + 25, cy - 105, outline="white", width=2)
        self.canvas.create_oval(cx - 10, cy - 145, cx + 10, cy - 125, outline="white", width=2) # ulo
        self.canvas.create_arc(cx - 20, cy - 125, cx + 20, cy - 95, start=0, extent=180, outline="white", width=2, style="arc") # katawan

        # USER LOGIN Title
        self.canvas.create_text(
            cx, cy - 175, 
            text="USER LOGIN", 
            fill="white", 
            font=("Arial", 14, "bold")
        )

        # Username Label & Entry
        self.canvas.create_text(
            cx - 100, cy - 65, 
            text="Username", 
            fill="white", 
            font=("Arial", 11, "bold"), 
            anchor="e"
        )
        self.username_entry = tk.Entry(self.root, font=("Arial", 11), width=20)
        self.canvas.create_window(cx + 30, cy - 65, window=self.username_entry)

        # Password Label & Entry
        self.canvas.create_text(
            cx - 100, cy - 25, 
            text="Password", 
            fill="white", 
            font=("Arial", 11, "bold"), 
            anchor="e"
        )
        self.password_entry = tk.Entry(self.root, font=("Arial", 11), width=20, show="*")
        self.canvas.create_window(cx + 30, cy - 25, window=self.password_entry)

        # Login Button (Nasa tabi ng Username at Password)
        self.login_btn = tk.Button(
            self.root, 
            text="LOGIN", 
            bg="#1b4f72", 
            fg="white", 
            font=("Arial", 10, "bold"), 
            width=8, 
            command=self.handle_login
        )
        self.canvas.create_window(cx + 165, cy - 45, window=self.login_btn)

        # Show Password Checkbox (Naka-center sa ilalim ng password field at may transparent/matching background)
        self.show_pass_var = tk.IntVar()
        self.show_pass_chk = tk.Checkbutton(
            self.root, 
            text="Show Password", 
            variable=self.show_pass_var, 
            bg="#2c8fd6", 
            fg="white", 
            selectcolor="#1b4f72", 
            activebackground="#2c8fd6", 
            activeforeground="white",
            font=("Arial", 9),
            command=self.toggle_password
        )
        self.canvas.create_window(cx + 30, cy + 15, window=self.show_pass_chk)

        # Bottom Buttons (Create Account & Forgot Password - magkatabi sa ibaba)
        self.create_acc_btn = tk.Button(
            self.root, 
            text="Create Account", 
            bg="#2980b9", 
            fg="white", 
            font=("Arial", 9, "bold"),
            command=self.create_account_action
        )
        self.canvas.create_window(cx - 100, cy + 110, window=self.create_acc_btn)

        self.forgot_pass_btn = tk.Button(
            self.root, 
            text="Forgot Password", 
            bg="#2980b9", 
            fg="white", 
            font=("Arial", 9, "bold"),
            command=self.forgot_password_action
        )
        self.canvas.create_window(cx + 100, cy + 110, window=self.forgot_pass_btn)

        # Pindutin ang 'Escape' key para lumabas sa Full Screen
        self.root.bind("<Escape>", self.exit_fullscreen)

    def draw_gradient(self, width, height):
        """Dynamic gradient para sa buong screen."""
        for i in range(height):
            r = int(0 + (77 - 0) * (i / height))
            g = int(86 + (166 - 86) * (i / height))
            b = int(179 + (255 - 179) * (i / height))
            hex_color = f"#{r:02x}{g:02x}{b:02x}"
            self.canvas.create_line(0, i, width, i, fill=hex_color)

    def toggle_password(self):
        if self.show_pass_var.get() == 1:
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="*")

    def handle_login(self):
        user = self.username_entry.get()
        pwd = self.password_entry.get()
        if not user or not pwd:
            messagebox.showwarning("Warning", "Please enter both username and password!")
        else:
            messagebox.showinfo("Success", f"Login attempted for user: {user}")

    def create_account_action(self):
        messagebox.showinfo("Navigation", "Redirecting to Create Account window...")

    def forgot_password_action(self):
        messagebox.showinfo("Navigation", "Redirecting to Forgot Password recovery...")

    def exit_fullscreen(self, event=None):
        self.root.attributes("-fullscreen", False)
        self.root.geometry("800x500")

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import sqlite3
import matplotlib.pyplot as plt
import pandas as pd

class BMICalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("BMI Calculator")
        self.root.geometry("800x900")
        self.root.config(bg="#A8DADC")

        # Create or connect to the SQLite database
        self.conn = sqlite3.connect('bmi_calculator.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS bmi_data (
            user_name TEXT,
            weight REAL,
            height REAL,
            bmi REAL,
            PRIMARY KEY (user_name, weight, height)
        )''')
        self.conn.commit()

        self.current_user = None

        # Header with title
        header = tk.Label(root, text="BMI Calculator", font=("Helvetica", 24, "bold"), fg="#1D3557", bg="#A8DADC")
        header.pack(pady=15)

        # Create a centered frame for input
        input_frame = tk.Frame(root, bg="#A8DADC", bd=2, relief=tk.RAISED)
        input_frame.pack(pady=10, padx=10, ipadx=10, ipady=10)

        # Labels and Entries in form style
        label_style = {"font": ("Arial", 12), "bg": "#A8DADC", "fg": "#1D3557"}
        tk.Label(input_frame, text="Weight (kg):", **label_style).grid(row=0, column=0, padx=10, pady=5, sticky="e")
        tk.Label(input_frame, text="Height (ft):", **label_style).grid(row=1, column=0, padx=10, pady=5, sticky="e")
        tk.Label(input_frame, text="Height (in):", **label_style).grid(row=2, column=0, padx=10, pady=5, sticky="e")
        tk.Label(input_frame, text="BMI:", **label_style).grid(row=3, column=0, padx=10, pady=5, sticky="e")

        self.weight_entry = tk.Entry(input_frame, font=("Arial", 12), width=15, bg="#F1FAEE")
        self.height_ft_entry = tk.Entry(input_frame, font=("Arial", 12), width=15, bg="#F1FAEE")
        self.height_in_entry = tk.Entry(input_frame, font=("Arial", 12), width=15, bg="#F1FAEE")
        self.bmi_label = tk.Label(input_frame, text="", font=("Arial", 12, "bold"), fg="#E63946", bg="#A8DADC")

        self.weight_entry.grid(row=0, column=1, pady=5, sticky="w")
        self.height_ft_entry.grid(row=1, column=1, pady=5, sticky="w")
        self.height_in_entry.grid(row=2, column=1, pady=5, sticky="w")
        self.bmi_label.grid(row=3, column=1, pady=5, sticky="w")

        # Create a frame for buttons
        button_frame = tk.Frame(root, bg="#A8DADC")
        button_frame.pack(pady=10)

        button_style = {
            "font": ("Arial", 10),
            "bg": "#457B9D",
            "fg": "white",
            "activebackground": "#1D3557",
            "activeforeground": "white",
            "padx": 10,
            "pady": 5,
            "width": 18
        }

        # Buttons with hover effects
        def hover(event):
            event.widget['bg'] = '#1D3557'
        
        def leave(event):
            event.widget['bg'] = '#457B9D'

        select_user_btn = tk.Button(button_frame, text="👤 Select User", command=self.select_user, **button_style)
        calculate_bmi_btn = tk.Button(button_frame, text="🧮 Calculate BMI", command=self.calculate_bmi, **button_style)
        save_data_btn = tk.Button(button_frame, text="💾 Save Data", command=self.save_data, **button_style)
        view_history_btn = tk.Button(button_frame, text="📜 View History", command=self.view_history, **button_style)
        visualize_data_btn = tk.Button(button_frame, text="📊 Visualize Data", command=self.visualize_data, **button_style)
        delete_data_btn = tk.Button(button_frame, text="🗑️ Delete Data", command=self.delete_data, **button_style)

        select_user_btn.grid(row=0, column=0, padx=10)
        calculate_bmi_btn.grid(row=0, column=1, padx=10)
        save_data_btn.grid(row=1, column=0, padx=10)
        view_history_btn.grid(row=1, column=1, padx=10)
        visualize_data_btn.grid(row=2, column=0, padx=10)
        delete_data_btn.grid(row=2, column=1, padx=10)

        for btn in [select_user_btn, calculate_bmi_btn, save_data_btn, view_history_btn, visualize_data_btn, delete_data_btn]:
            btn.bind("<Enter>", hover)
            btn.bind("<Leave>", leave)

        # Create a frame for the BMI classification scale
        scale_frame = tk.Frame(root, bg="#A8DADC", bd=2, relief=tk.RAISED)
        scale_frame.pack(pady=10, padx=10, fill=tk.X)

        scale_label = tk.Label(scale_frame, text="BMI Classification Scale", font=("Helvetica", 14, "bold"), fg="#1D3557", bg="#A8DADC")
        scale_label.pack(pady=5)

        scale_info = [
            ("Severe Thinness", "< 16"),
            ("Moderate Thinness", "16 - 17"),
            ("Mild Thinness", "17 - 18.5"),
            ("Normal", "18.5 - 25"),
            ("Overweight", "25 - 30"),
            ("Obese Class I", "30 - 35"),
            ("Obese Class II", "35 - 40"),
            ("Obese Class III", "> 40"),
        ]

        for classification, range_ in scale_info:
            tk.Label(scale_frame, text=f"{classification}: {range_}", font=("Arial", 10), bg="#A8DADC", fg="#1D3557").pack(anchor="center")

    def select_user(self):
        username = simpledialog.askstring("Input", "Enter your username:")
        if username:
            self.current_user = username
            messagebox.showinfo("User Selected", f"Current user set to: {self.current_user}")

    def calculate_bmi(self):
        try:
            weight = float(self.weight_entry.get())
            height_ft = float(self.height_ft_entry.get())
            height_in = float(self.height_in_entry.get())
            # Convert height to meters
            total_height = (height_ft * 12 + height_in) * 0.0254
            bmi = weight / (total_height ** 2)
            self.bmi_label.config(text=f"{bmi:.2f}")
            self.show_bmi_classification(bmi)
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers for weight and height.")

    def show_bmi_classification(self, bmi):
        if bmi < 16:
            classification = "Severe Thinness"
        elif bmi < 17:
            classification = "Moderate Thinness"
        elif bmi < 18.5:
            classification = "Mild Thinness"
        elif bmi < 25:
            classification = "Normal"
        elif bmi < 30:
            classification = "Overweight"
        elif bmi < 35:
            classification = "Obese Class I"
        elif bmi < 40:
            classification = "Obese Class II"
        else:
            classification = "Obese Class III"

        messagebox.showinfo("BMI Classification", f"Your BMI is {bmi:.2f}. Classification: {classification}")

    def save_data(self):
        if not self.current_user:
            messagebox.showwarning("No User", "Please select a user before saving data.")
            return
            
        try:
            weight = float(self.weight_entry.get())
            height = (float(self.height_ft_entry.get()) * 12 + float(self.height_in_entry.get())) * 0.0254
            bmi = float(self.bmi_label.cget("text"))
        except ValueError:
            messagebox.showwarning("No Data", "Please calculate the BMI before saving.")
            return
        
        try:
            self.cursor.execute('INSERT INTO bmi_data (user_name, weight, height, bmi) VALUES (?, ?, ?, ?)',
                                (self.current_user, weight, height, bmi))
            self.conn.commit()
            messagebox.showinfo("Data Saved", "BMI data saved successfully.")
        except sqlite3.IntegrityError:
            messagebox.showwarning("Data Exists", "This entry already exists for the user.")

    def delete_data(self):
        if not self.current_user:
            messagebox.showwarning("No User", "Please select a user before deleting data.")
            return
        
        confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete all data for this user?")
        if confirm:
            self.cursor.execute('DELETE FROM bmi_data WHERE user_name = ?', (self.current_user,))
            self.conn.commit()
            messagebox.showinfo("Data Deleted", "All BMI data for the user has been deleted.")

    def view_history(self):
        if not self.current_user:
            messagebox.showwarning("No User", "Please select a user before viewing history.")
            return
        
        self.cursor.execute('SELECT weight, height, bmi FROM bmi_data WHERE user_name = ?', (self.current_user,))
        data = self.cursor.fetchall()
        
        if not data:
            messagebox.showinfo("No Data", "No history found for this user.")
            return
        
        history_window = tk.Toplevel(self.root)
        history_window.title("BMI History")
        history_window.geometry("400x300")
        history_text = tk.Text(history_window, wrap="word")
        history_text.insert("end", f"BMI History for {self.current_user}\n\n")
        for idx, (weight, height, bmi) in enumerate(data, 1):
            history_text.insert("end", f"{idx}. Weight: {weight} kg, Height: {height:.2f} m, BMI: {bmi:.2f}\n")
        history_text.pack(fill="both", expand=True)

    def visualize_data(self):
        if not self.current_user:
            messagebox.showwarning("No User", "Please select a user before visualizing data.")
            return
        
        self.cursor.execute('SELECT weight, bmi FROM bmi_data WHERE user_name = ?', (self.current_user,))
        data = self.cursor.fetchall()
        
        if not data:
            messagebox.showinfo("No Data", "No data available to visualize.")
            return
        
        weights, bmis = zip(*data)
        df = pd.DataFrame({"Weight": weights, "BMI": bmis})
        
        plt.figure(figsize=(10, 6))
        plt.plot(df["Weight"], df["BMI"], marker="o", color="#E63946", linestyle="-", linewidth=2)
        plt.title(f"BMI Trend for {self.current_user}")
        plt.xlabel("Weight (kg)")
        plt.ylabel("BMI")
        plt.grid(True)
        plt.show()

if __name__ == "__main__":
    root = tk.Tk()
    app = BMICalculator(root)
    root.mainloop()

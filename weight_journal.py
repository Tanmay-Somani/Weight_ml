import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import matplotlib.pyplot as plt
import mplcursors
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime, timedelta
import os

__author__ = "Tanmay Somani"
__date__ = "06-10-24"
__description__ = "A very basic executable goal-based weight tracking Application"

class WeightDashboard:
    def __init__(self, master):
        self.master = master
        self.master.title("Weight Dashboard")
        self.master.geometry("1080x760")
        self.master.config(bg="#f0f0f0")

        self.weight = tk.DoubleVar()
        self.data = []
        self.log_file = "weight_log.txt"
        self.goal_weight = None
        self.goal_date = None

        self.load_data()
        self.create_widgets()
        self.create_menu()

        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_widgets(self):
        input_frame = ttk.Frame(self.master, padding="10")
        input_frame.grid(row=0, column=0, sticky="ew")
        input_frame.columnconfigure(1, weight=1)

        ttk.Label(input_frame, text="Weight (kg):").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        weight_entry = ttk.Entry(input_frame, textvariable=self.weight)
        weight_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.create_tooltip(weight_entry, "Enter your current weight in kilograms.")

        ttk.Button(input_frame, text="Add Data", command=self.add_data).grid(row=1, column=0, columnspan=2, pady=10)

        self.viz_frame = ttk.Frame(self.master)
        self.viz_frame.grid(row=1, column=0, sticky="nsew")

        self.update_dashboard()

    def create_menu(self):
        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)

        goal_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Goal", menu=goal_menu)
        goal_menu.add_command(label="Set Goal", command=self.set_goal)
        goal_menu.add_command(label="Remove Goal", command=self.remove_goal)
        goal_menu.add_separator()
        goal_menu.add_command(label="View Current Goal", command=self.view_goal)

        info_menu = tk.Menu(menubar, tearoff=1)
        menubar.add_cascade(label="Help", menu=info_menu)
        info_menu.add_command(label="About", command=self.show_about)

    def create_tooltip(self, widget, text):
        tooltip = tk.Toplevel(self.master)
        tooltip.wm_overrideredirect(True)
        tooltip.withdraw()

        label = ttk.Label(tooltip, text=text, background="lightyellow", relief="solid", borderwidth=1)
        label.pack()

        def show_tooltip(event):
            tooltip.wm_deiconify()
            tooltip.wm_geometry(f"+{event.x_root + 10}+{event.y_root + 10}")

        def hide_tooltip(event):
            tooltip.wm_withdraw()

        widget.bind("<Enter>", show_tooltip)
        widget.bind("<Leave>", hide_tooltip)

    def show_about(self):
        messagebox.showinfo("About", "Weight Dashboard Application\nAuthor: Tanmay Somani\nDate: 06-10-24")

    def view_goal(self):
        if self.goal_weight and self.goal_date:
            messagebox.showinfo("Current Goal", f"Goal Weight: {self.goal_weight} kg\nGoal Date: {self.goal_date.strftime('%Y-%m-%d')}")
        else:
            messagebox.showinfo("Current Goal", "No goal set.")

    def set_goal(self):
        goal_weight = simpledialog.askfloat("Set Goal", "Enter your goal weight (kg):", parent=self.master)
        if goal_weight is not None:
            weeks = simpledialog.askinteger("Set Goal", "Enter the number of weeks to achieve this goal:", parent=self.master)
            if weeks is not None and weeks > 0:
                self.goal_weight = goal_weight
                self.goal_date = datetime.now() + timedelta(weeks=weeks)
                messagebox.showinfo("Goal Set", f"Goal set: {self.goal_weight} kg by {self.goal_date.strftime('%Y-%m-%d')}")
                self.save_log()
                self.update_dashboard()
            else:
                messagebox.showerror("Invalid Input", "Please enter a positive number for weeks.")

    def remove_goal(self):
        self.goal_weight = None
        self.goal_date = None
        messagebox.showinfo("Goal Successfully Removed", "Time to Set a New Goal")
        self.save_log()
        self.update_dashboard()

    def add_data(self):
        try:
            weight = self.weight.get()
            if weight <= 0:
                raise ValueError("Weight must be a positive number.")
            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.data.append((date, weight))
            self.save_log()
            self.update_dashboard()
            self.weight.set("")
        except tk.TclError:
            messagebox.showerror("Invalid Input", "Please enter a valid number for weight.")
        except ValueError as ve:
            messagebox.showerror("Invalid Input", str(ve))

    def save_log(self):
        with open(self.log_file, "a") as f:
            if self.data:
                date, weight = self.data[-1]
                f.write(f"DATA,{date},{weight}\n")
            if self.goal_weight is not None and self.goal_date is not None:
                f.write(f"GOAL,{self.goal_weight},{self.goal_date.strftime('%Y-%m-%d %H:%M:%S')}\n")
            else:
                f.write("GOAL,None,None\n")

    def load_data(self):
        if os.path.exists(self.log_file):
            with open(self.log_file, "r") as f:
                for line in f:
                    parts = line.strip().split(",")
                    if parts[0] == "DATA":
                        try:
                            date, weight = parts[1], float(parts[2])
                            self.data.append((date, weight))
                        except (ValueError, IndexError):
                            continue
                    elif parts[0] == "GOAL":
                        if parts[1] != "None":
                            self.goal_weight = float(parts[1])
                            self.goal_date = datetime.strptime(parts[2], "%Y-%m-%d %H:%M:%S")
                        else:
                            self.goal_weight = None
                            self.goal_date = None

    def update_dashboard(self):
        for widget in self.viz_frame.winfo_children():
            widget.destroy()

        if not self.data:
            ttk.Label(self.viz_frame, text="No data available. Please add some data.").pack(expand=True)
            return

        fig, ax = plt.subplots(figsize=(10, 6))
        fig.suptitle("Weight Dashboard", fontsize=16)

        dates = [datetime.strptime(date, "%Y-%m-%d %H:%M:%S") for date, _ in self.data]
        weights = [weight for _, weight in self.data]

        scatter = ax.scatter(dates, weights, marker='o', color='blue', label="Actual Weight")

        ax.set_ylabel("Weight (kg)")
        ax.set_xlabel("Date")
        ax.set_title("Weight Over Time")

        if self.goal_weight and self.goal_date:
            ax.axhline(y=self.goal_weight, color='r', linestyle='--', label="Goal Weight")
            ax.axvline(x=self.goal_date, color='g', linestyle='--', label="Goal Date")
            ax.annotate(f"Goal: {self.goal_weight} kg", (self.goal_date, self.goal_weight),
                        xytext=(10, 10), textcoords='offset points')

        ax.legend()
        plt.tight_layout()

        mplcursors.cursor(scatter, hover=True).connect("add", lambda sel: sel.annotation.set_text(
            f"Date: {dates[sel.index].strftime('%Y-%m-%d')}\nWeight: {weights[sel.index]} kg"
        ))

        canvas = FigureCanvasTkAgg(fig, master=self.viz_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        canvas_widget.bind("<Configure>", lambda event: self.on_resize(event, fig, canvas))

    def on_resize(self, event, fig, canvas):
        fig.set_size_inches(event.width / 100, event.height / 100)
        canvas.draw()

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = WeightDashboard(root)
    root.mainloop()

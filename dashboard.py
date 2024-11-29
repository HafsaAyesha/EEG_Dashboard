import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np


class MindGuardDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("MindGuard Dashboard")
        self.root.geometry("400x800")  # Fixed size for the main window
        self.root.configure(bg="white")

        # Create a scrollable frame
        self.canvas = tk.Canvas(root, bg="white")
        self.scrollable_frame = tk.Frame(self.canvas, bg="white")
        self.scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Pack the canvas and scrollbar
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # Ensure dynamic resizing of the scrollable area
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Add content to the scrollable frame
        self.build_dashboard(self.scrollable_frame)

    def build_dashboard(self, parent):
        # Navigation bar
        nav_bar = tk.Frame(parent, bg="white", height=40)
        nav_bar.pack(fill="x", padx=20, pady=(10, 0))

        nav_buttons = ["Dashboard", "Alerts", "History"]
        for button_text in nav_buttons:
            button = tk.Button(nav_bar, text=button_text, font=("Helvetica", 12), bg="white", bd=0, fg="black", relief="flat")
            button.pack(side="left", padx=15)

        # Title: Dashboard
        title_label = tk.Label(parent, text="Dashboard", font=("Helvetica", 20, "bold"), bg="white", anchor="w")
        title_label.pack(fill="x", padx=20, pady=(10, 0))

        # Subtitle: Real-Time Emotional State
        subtitle_label = tk.Label(parent, text="Real-Time Emotional State", font=("Helvetica", 14), bg="white", anchor="w")
        subtitle_label.pack(fill="x", padx=20, pady=(5, 0))

        # Mood Fluctuations
        mood_label = tk.Label(parent, text="Mood Fluctuations", font=("Helvetica", 12), bg="white", anchor="w")
        mood_label.pack(fill="x", padx=20, pady=(10, 0))

        # Last 24 Hours
        time_label = tk.Label(parent, text="Last 24 Hours", font=("Helvetica", 10), bg="white", anchor="w")
        time_label.pack(fill="x", padx=20, pady=(0, 10))

        # Donut Chart
        donut_frame = tk.Frame(parent, bg="white")
        donut_frame.pack(fill="both", expand=True, padx=20, pady=10)
        self.plot_donut_chart(donut_frame)
        self.create_legend(["Calm", "Happy", "Sad"], ["#4CAF50", "#2196F3", "#F44336"], donut_frame)

        # Line Chart
        line_frame = tk.Frame(parent, bg="white")
        line_frame.pack(fill="both", expand=True, padx=20, pady=10)
        self.plot_line_chart(line_frame)
        self.create_legend(["Joy", "Anger", "Surprise"], ["green", "red", "blue"], line_frame)

        # Footer
        self.create_footer(parent)

    def plot_donut_chart(self, frame):
        # Data for the donut chart
        sizes = [40, 35, 25]
        colors = ["#4CAF50", "#2196F3", "#F44336"]

        fig, ax = plt.subplots(figsize=(3.5, 3.5), dpi=100)
        ax.pie(
            sizes,
            autopct=None,
            startangle=90,
            colors=colors,
            wedgeprops=dict(width=0.4, edgecolor="white"),
        )

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.get_tk_widget().pack(pady=10)
        canvas.draw()

    def plot_line_chart(self, frame):
        # Data for the line chart
        time = np.linspace(0, 24, 100)
        joy = np.sin(time) + 2
        anger = np.cos(time) + 2
        surprise = np.sin(time / 2) + 2

        fig, ax = plt.subplots(figsize=(4, 2.5), dpi=100)
        ax.plot(time, joy, label="Joy", color="green", linewidth=2)
        ax.plot(time, anger, label="Anger", color="red", linewidth=2)
        ax.plot(time, surprise, label="Surprise", color="blue", linewidth=2)
        ax.set_title("Emotion Distribution\nLast 24 Hours", fontsize=12)
        ax.set_xlabel("Time (Hours)", fontsize=10)
        ax.set_ylabel("Emotion Level", fontsize=10)
        ax.grid(alpha=0.3)

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.get_tk_widget().pack(pady=10)
        canvas.draw()

    def create_legend(self, labels, colors, frame):
        legend_frame = tk.Frame(frame, bg="white")
        legend_frame.pack(pady=5)

        for label, color in zip(labels, colors):
            item_frame = tk.Frame(legend_frame, bg="white")
            item_frame.pack(side="left", padx=10)

            color_sphere = tk.Label(item_frame, bg=color, width=2, height=1, relief="solid", borderwidth=1)
            color_sphere.pack(side="left", padx=5)

            label_text = tk.Label(item_frame, text=label, font=("Helvetica", 10), bg="white")
            label_text.pack(side="left")

    def create_footer(self, parent):
        footer_frame = tk.Frame(parent, bg="white", height=50)
        footer_frame.pack(side="bottom", fill="x", pady=5)

        icons = ["🏠", "📊", "⚙️", "👤"]
        labels = ["Dashboard", "Insights", "Settings", "Profile"]

        for i in range(len(icons)):
            frame = tk.Frame(footer_frame, bg="white")
            frame.pack(side="left", expand=True, padx=10)

            icon_label = tk.Label(
                frame,
                text=icons[i],
                font=("Helvetica", 20),
                bg="white",
                fg="black",
                cursor="hand2",
            )
            icon_label.pack()
            icon_label.bind("<Enter>", lambda e, lbl=icon_label: lbl.config(fg="blue"))
            icon_label.bind("<Leave>", lambda e, lbl=icon_label: lbl.config(fg="black"))

            text_label = tk.Label(frame, text=labels[i], font=("Helvetica", 10), bg="white")
            text_label.pack()


# Main application
root = tk.Tk()
dashboard = MindGuardDashboard(root)
root.mainloop()

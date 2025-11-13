"""
Smart Study Tracker - Main Application
A comprehensive study tracking application with GUI, data visualization, and progress monitoring.
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime, timedelta
import json
import os
from typing import List, Dict
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import random


class StudyTracker:
    """Main application class for the Smart Study Tracker"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Study Tracker")
        self.root.geometry("900x700")
        self.root.configure(bg="#f0f0f0")
        
        # Data file path
        self.data_file = "study_data.json"
        
        # Motivational messages
        self.motivational_messages = [
            "Great job! Keep up the excellent work!",
            "You're making amazing progress!",
            "Consistency is key - you're doing fantastic!",
            "Every study session brings you closer to your goals!",
            "Your dedication is impressive! Keep it up!",
            "Learning is a journey, and you're on the right path!",
            "Proud of your commitment to learning!",
            "Small steps lead to big achievements!"
        ]
        
        # Create the GUI
        self.create_widgets()
        
        # Load existing data
        self.load_data()
        
    def create_widgets(self):
        """Create all GUI widgets"""
        
        # Title
        title_frame = tk.Frame(self.root, bg="#4a90e2", height=60)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame, 
            text="Smart Study Tracker", 
            font=("Arial", 24, "bold"),
            bg="#4a90e2",
            fg="white"
        )
        title_label.pack(pady=10)
        
        # Main container
        main_container = tk.Frame(self.root, bg="#f0f0f0")
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Left side - Input form
        left_frame = tk.Frame(main_container, bg="white", relief=tk.RAISED, borderwidth=2)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Form title
        form_title = tk.Label(
            left_frame,
            text="Log Study Session",
            font=("Arial", 16, "bold"),
            bg="white",
            fg="#333"
        )
        form_title.pack(pady=15)
        
        # Subject
        subject_frame = tk.Frame(left_frame, bg="white")
        subject_frame.pack(pady=10, padx=20, fill=tk.X)
        
        tk.Label(subject_frame, text="Subject:", font=("Arial", 11), bg="white").pack(anchor=tk.W)
        self.subject_entry = ttk.Entry(subject_frame, font=("Arial", 11))
        self.subject_entry.pack(fill=tk.X, pady=5)
        
        # Duration
        duration_frame = tk.Frame(left_frame, bg="white")
        duration_frame.pack(pady=10, padx=20, fill=tk.X)
        
        tk.Label(duration_frame, text="Duration (minutes):", font=("Arial", 11), bg="white").pack(anchor=tk.W)
        self.duration_entry = ttk.Entry(duration_frame, font=("Arial", 11))
        self.duration_entry.pack(fill=tk.X, pady=5)
        
        # Productivity Score
        productivity_frame = tk.Frame(left_frame, bg="white")
        productivity_frame.pack(pady=10, padx=20, fill=tk.X)
        
        tk.Label(productivity_frame, text="Productivity Level (1-5):", font=("Arial", 11), bg="white").pack(anchor=tk.W)
        self.productivity_var = tk.IntVar(value=3)
        
        productivity_scale = ttk.Scale(
            productivity_frame,
            from_=1,
            to=5,
            orient=tk.HORIZONTAL,
            variable=self.productivity_var,
            command=self.update_productivity_label
        )
        productivity_scale.pack(fill=tk.X, pady=5)
        
        self.productivity_label = tk.Label(
            productivity_frame,
            text="3 - Good",
            font=("Arial", 10),
            bg="white",
            fg="#4a90e2"
        )
        self.productivity_label.pack()
        
        # Notes
        notes_frame = tk.Frame(left_frame, bg="white")
        notes_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        tk.Label(notes_frame, text="Notes (optional):", font=("Arial", 11), bg="white").pack(anchor=tk.W)
        self.notes_text = scrolledtext.ScrolledText(notes_frame, height=5, font=("Arial", 10))
        self.notes_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Buttons
        button_frame = tk.Frame(left_frame, bg="white")
        button_frame.pack(pady=20, padx=20, fill=tk.X)
        
        save_button = tk.Button(
            button_frame,
            text="Save Study Session",
            command=self.save_session,
            bg="#4a90e2",
            fg="white",
            font=("Arial", 12, "bold"),
            cursor="hand2",
            relief=tk.RAISED,
            borderwidth=2
        )
        save_button.pack(fill=tk.X, pady=5)
        
        clear_button = tk.Button(
            button_frame,
            text="Clear Form",
            command=self.clear_form,
            bg="#e74c3c",
            fg="white",
            font=("Arial", 10),
            cursor="hand2"
        )
        clear_button.pack(fill=tk.X, pady=5)
        
        # Right side - Actions and info
        right_frame = tk.Frame(main_container, bg="white", relief=tk.RAISED, borderwidth=2)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Actions title
        actions_title = tk.Label(
            right_frame,
            text="View Progress",
            font=("Arial", 16, "bold"),
            bg="white",
            fg="#333"
        )
        actions_title.pack(pady=15)
        
        # Action buttons
        actions_container = tk.Frame(right_frame, bg="white")
        actions_container.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        
        tk.Button(
            actions_container,
            text="View Subject Distribution",
            command=self.show_subject_distribution,
            bg="#27ae60",
            fg="white",
            font=("Arial", 11, "bold"),
            cursor="hand2",
            height=2
        ).pack(fill=tk.X, pady=10)
        
        tk.Button(
            actions_container,
            text="View Time Spent Chart",
            command=self.show_time_chart,
            bg="#8e44ad",
            fg="white",
            font=("Arial", 11, "bold"),
            cursor="hand2",
            height=2
        ).pack(fill=tk.X, pady=10)
        
        tk.Button(
            actions_container,
            text="Weekly Summary",
            command=self.show_weekly_summary,
            bg="#e67e22",
            fg="white",
            font=("Arial", 11, "bold"),
            cursor="hand2",
            height=2
        ).pack(fill=tk.X, pady=10)
        
        tk.Button(
            actions_container,
            text="View All Sessions",
            command=self.show_all_sessions,
            bg="#3498db",
            fg="white",
            font=("Arial", 11, "bold"),
            cursor="hand2",
            height=2
        ).pack(fill=tk.X, pady=10)
        
        tk.Button(
            actions_container,
            text="Clear All Data",
            command=self.clear_all_data,
            bg="#c0392b",
            fg="white",
            font=("Arial", 11, "bold"),
            cursor="hand2",
            height=2
        ).pack(fill=tk.X, pady=10)
        
        # Stats display
        self.stats_frame = tk.Frame(right_frame, bg="#ecf0f1", relief=tk.SUNKEN, borderwidth=2)
        self.stats_frame.pack(pady=10, padx=20, fill=tk.X)
        
        self.stats_label = tk.Label(
            self.stats_frame,
            text="Total Sessions: 0\nTotal Time: 0 min",
            font=("Arial", 10),
            bg="#ecf0f1",
            fg="#2c3e50",
            justify=tk.LEFT
        )
        self.stats_label.pack(pady=10)
        
    def update_productivity_label(self, value):
        """Update the productivity level label"""
        value = int(float(value))
        labels = {
            1: "1 - Very Low",
            2: "2 - Low",
            3: "3 - Good",
            4: "4 - High",
            5: "5 - Excellent"
        }
        self.productivity_label.config(text=labels.get(value, "3 - Good"))
        
    def load_data(self) -> List[Dict]:
        """Load study data from JSON file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    self.update_stats()
                    return data
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load data: {str(e)}")
                return []
        return []
    
    def save_data(self, data: List[Dict]):
        """Save study data to JSON file"""
        try:
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save data: {str(e)}")
    
    def save_session(self):
        """Save a new study session"""
        # Validate inputs
        subject = self.subject_entry.get().strip()
        duration_str = self.duration_entry.get().strip()
        
        if not subject:
            messagebox.showwarning("Missing Information", "Please enter a subject.")
            return
        
        if not duration_str:
            messagebox.showwarning("Missing Information", "Please enter duration.")
            return
        
        try:
            duration = int(duration_str)
            if duration <= 0:
                raise ValueError("Duration must be positive")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid positive number for duration.")
            return
        
        # Create session object
        session = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "subject": subject,
            "duration": duration,
            "productivity": self.productivity_var.get(),
            "notes": self.notes_text.get("1.0", tk.END).strip()
        }
        
        # Load existing data and append
        data = self.load_data()
        data.append(session)
        self.save_data(data)
        
        # Show motivational message
        message = random.choice(self.motivational_messages)
        messagebox.showinfo(
            "Session Saved!",
            f"Successfully logged {duration} minutes of {subject}!\n\n{message}"
        )
        
        # Clear form and update stats
        self.clear_form()
        self.update_stats()
    
    def clear_form(self):
        """Clear all input fields"""
        self.subject_entry.delete(0, tk.END)
        self.duration_entry.delete(0, tk.END)
        self.productivity_var.set(3)
        self.notes_text.delete("1.0", tk.END)
        self.update_productivity_label(3)
    
    def update_stats(self):
        """Update statistics display"""
        data = self.load_data()
        total_sessions = len(data)
        total_time = sum(session['duration'] for session in data)
        
        hours = total_time // 60
        minutes = total_time % 60
        
        time_str = f"{hours}h {minutes}min" if hours > 0 else f"{minutes} min"
        
        self.stats_label.config(
            text=f"Total Sessions: {total_sessions}\nTotal Time: {time_str}"
        )
    
    def show_subject_distribution(self):
        """Show pie chart of time distribution by subject"""
        data = self.load_data()
        
        if not data:
            messagebox.showinfo("No Data", "No study sessions recorded yet!")
            return
        
        # Calculate time per subject
        subject_time = {}
        for session in data:
            subject = session['subject']
            duration = session['duration']
            subject_time[subject] = subject_time.get(subject, 0) + duration
        
        # Create new window
        chart_window = tk.Toplevel(self.root)
        chart_window.title("Subject Distribution")
        chart_window.geometry("800x600")
        
        # Create pie chart
        fig = Figure(figsize=(8, 6))
        ax = fig.add_subplot(111)
        
        subjects = list(subject_time.keys())
        times = list(subject_time.values())
        
        colors = plt.cm.Set3(range(len(subjects)))
        
        wedges, texts, autotexts = ax.pie(
            times,
            labels=subjects,
            autopct='%1.1f%%',
            startangle=90,
            colors=colors
        )
        
        # Make percentage text more readable
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(10)
            autotext.set_weight('bold')
        
        ax.set_title("Study Time Distribution by Subject", fontsize=14, fontweight='bold')
        
        # Add canvas to window
        canvas = FigureCanvasTkAgg(fig, chart_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def show_time_chart(self):
        """Show bar chart of total time spent on each subject"""
        data = self.load_data()
        
        if not data:
            messagebox.showinfo("No Data", "No study sessions recorded yet!")
            return
        
        # Calculate time per subject
        subject_time = {}
        for session in data:
            subject = session['subject']
            duration = session['duration']
            subject_time[subject] = subject_time.get(subject, 0) + duration
        
        # Sort by time
        sorted_subjects = sorted(subject_time.items(), key=lambda x: x[1], reverse=True)
        subjects = [s[0] for s in sorted_subjects]
        times = [s[1] for s in sorted_subjects]
        
        # Create new window
        chart_window = tk.Toplevel(self.root)
        chart_window.title("Time Spent by Subject")
        chart_window.geometry("800x600")
        
        # Create bar chart
        fig = Figure(figsize=(8, 6))
        ax = fig.add_subplot(111)
        
        bars = ax.bar(subjects, times, color='#4a90e2', alpha=0.8)
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width()/2.,
                height,
                f'{int(height)} min',
                ha='center',
                va='bottom',
                fontweight='bold'
            )
        
        ax.set_xlabel("Subject", fontsize=12, fontweight='bold')
        ax.set_ylabel("Time (minutes)", fontsize=12, fontweight='bold')
        ax.set_title("Total Study Time by Subject", fontsize=14, fontweight='bold')
        
        # Rotate x-axis labels if needed
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        fig.tight_layout()
        
        # Add canvas to window
        canvas = FigureCanvasTkAgg(fig, chart_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def show_weekly_summary(self):
        """Show weekly study summary"""
        data = self.load_data()
        
        if not data:
            messagebox.showinfo("No Data", "No study sessions recorded yet!")
            return
        
        # Calculate date 7 days ago
        week_ago = datetime.now() - timedelta(days=7)
        
        # Filter sessions from last 7 days
        weekly_sessions = []
        for session in data:
            session_date = datetime.strptime(session['timestamp'], "%Y-%m-%d %H:%M:%S")
            if session_date >= week_ago:
                weekly_sessions.append(session)
        
        if not weekly_sessions:
            messagebox.showinfo("Weekly Summary", "No study sessions in the past 7 days!")
            return
        
        # Calculate statistics
        total_sessions = len(weekly_sessions)
        total_time = sum(s['duration'] for s in weekly_sessions)
        avg_productivity = sum(s['productivity'] for s in weekly_sessions) / total_sessions
        
        # Time per subject
        subject_time = {}
        for session in weekly_sessions:
            subject = session['subject']
            duration = session['duration']
            subject_time[subject] = subject_time.get(subject, 0) + duration
        
        # Most studied subject
        most_studied = max(subject_time.items(), key=lambda x: x[1])
        
        # Create summary window
        summary_window = tk.Toplevel(self.root)
        summary_window.title("Weekly Summary")
        summary_window.geometry("600x500")
        summary_window.configure(bg="white")
        
        # Title
        title = tk.Label(
            summary_window,
            text="Weekly Study Summary",
            font=("Arial", 18, "bold"),
            bg="white",
            fg="#4a90e2"
        )
        title.pack(pady=20)
        
        # Summary text
        summary_frame = tk.Frame(summary_window, bg="#ecf0f1", relief=tk.RAISED, borderwidth=2)
        summary_frame.pack(padx=30, pady=10, fill=tk.BOTH, expand=True)
        
        hours = total_time // 60
        minutes = total_time % 60
        
        summary_text = f"""
        Summary for Last 7 Days
        
        Total Study Sessions: {total_sessions}
        
        Total Time Studied: {hours}h {minutes}min
        
        Average Productivity: {avg_productivity:.1f}/5
        
        Most Studied Subject: {most_studied[0]} ({most_studied[1]} min)
        
        Subjects Covered: {len(subject_time)}
        """
        
        summary_label = tk.Label(
            summary_frame,
            text=summary_text,
            font=("Arial", 12),
            bg="#ecf0f1",
            fg="#2c3e50",
            justify=tk.LEFT
        )
        summary_label.pack(pady=20, padx=20)
        
        # Motivational message
        motivation = random.choice(self.motivational_messages)
        motivation_label = tk.Label(
            summary_window,
            text=motivation,
            font=("Arial", 11, "italic"),
            bg="white",
            fg="#27ae60",
            wraplength=500
        )
        motivation_label.pack(pady=20)
    
    def show_all_sessions(self):
        """Display all study sessions in a new window"""
        data = self.load_data()
        
        if not data:
            messagebox.showinfo("No Data", "No study sessions recorded yet!")
            return
        
        # Create new window
        sessions_window = tk.Toplevel(self.root)
        sessions_window.title("All Study Sessions")
        sessions_window.geometry("900x600")
        
        # Title
        title = tk.Label(
            sessions_window,
            text="All Study Sessions",
            font=("Arial", 16, "bold"),
            bg="#4a90e2",
            fg="white"
        )
        title.pack(fill=tk.X, pady=10)
        
        # Create treeview
        tree_frame = tk.Frame(sessions_window)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient="vertical")
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal")
        
        # Treeview
        tree = ttk.Treeview(
            tree_frame,
            columns=("timestamp", "subject", "duration", "productivity", "notes"),
            show="headings",
            yscrollcommand=vsb.set,
            xscrollcommand=hsb.set
        )
        
        vsb.config(command=tree.yview)
        hsb.config(command=tree.xview)
        
        # Column headings
        tree.heading("timestamp", text="Date & Time")
        tree.heading("subject", text="Subject")
        tree.heading("duration", text="Duration (min)")
        tree.heading("productivity", text="Productivity")
        tree.heading("notes", text="Notes")
        
        # Column widths
        tree.column("timestamp", width=150)
        tree.column("subject", width=150)
        tree.column("duration", width=100)
        tree.column("productivity", width=100)
        tree.column("notes", width=300)
        
        # Add data (reverse order to show newest first)
        for session in reversed(data):
            tree.insert("", tk.END, values=(
                session['timestamp'],
                session['subject'],
                session['duration'],
                f"{session['productivity']}/5",
                session['notes'][:50] + "..." if len(session['notes']) > 50 else session['notes']
            ))
        
        # Pack tree and scrollbars
        tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
    
    def clear_all_data(self):
        """Clear all study session data"""
        result = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete all study sessions?\n\nThis action cannot be undone!"
        )
        
        if result:
            try:
                if os.path.exists(self.data_file):
                    os.remove(self.data_file)
                messagebox.showinfo("Success", "All data has been cleared.")
                self.update_stats()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to clear data: {str(e)}")


def main():
    """Main function to run the application"""
    root = tk.Tk()
    app = StudyTracker(root)
    root.mainloop()


if __name__ == "__main__":
    main()

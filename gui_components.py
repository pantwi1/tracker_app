"""
GUI Components Module
Contains all GUI-related components and windows for the study tracker.
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from typing import Callable, Optional
from utils import Constants, MessageGenerator, TimeFormatter, Validator


class StudyInputForm:
    """Input form for logging study sessions"""
    
    def __init__(self, parent: tk.Frame, on_save: Callable, on_clear: Callable):
        """
        Initialize the study input form.
        
        Args:
            parent: Parent tkinter frame
            on_save: Callback function for save button
            on_clear: Callback function for clear button
        """
        self.parent = parent
        self.on_save = on_save
        self.on_clear = on_clear
        
        self.subject_entry = None
        self.duration_entry = None
        self.productivity_var = None
        self.productivity_label = None
        self.notes_text = None
        
        self._create_form()
    
    def _create_form(self):
        """Create the form widgets"""
        
        # Form title
        form_title = tk.Label(
            self.parent,
            text="Log Study Session",
            font=Constants.HEADING_FONT,
            bg=Constants.WHITE,
            fg=Constants.TEXT_COLOR
        )
        form_title.pack(pady=15)
        
        # Subject
        subject_frame = tk.Frame(self.parent, bg=Constants.WHITE)
        subject_frame.pack(pady=10, padx=20, fill=tk.X)
        
        tk.Label(subject_frame, text="Subject:", font=Constants.NORMAL_FONT, 
                bg=Constants.WHITE).pack(anchor=tk.W)
        self.subject_entry = ttk.Entry(subject_frame, font=Constants.NORMAL_FONT)
        self.subject_entry.pack(fill=tk.X, pady=5)
        
        # Duration
        duration_frame = tk.Frame(self.parent, bg=Constants.WHITE)
        duration_frame.pack(pady=10, padx=20, fill=tk.X)
        
        tk.Label(duration_frame, text="Duration (minutes):", font=Constants.NORMAL_FONT, 
                bg=Constants.WHITE).pack(anchor=tk.W)
        self.duration_entry = ttk.Entry(duration_frame, font=Constants.NORMAL_FONT)
        self.duration_entry.pack(fill=tk.X, pady=5)
        
        # Productivity Score
        productivity_frame = tk.Frame(self.parent, bg=Constants.WHITE)
        productivity_frame.pack(pady=10, padx=20, fill=tk.X)
        
        tk.Label(productivity_frame, text="Productivity Level (1-5):", 
                font=Constants.NORMAL_FONT, bg=Constants.WHITE).pack(anchor=tk.W)
        self.productivity_var = tk.IntVar(value=3)
        
        productivity_scale = ttk.Scale(
            productivity_frame,
            from_=1,
            to=5,
            orient=tk.HORIZONTAL,
            variable=self.productivity_var,
            command=self._update_productivity_label
        )
        productivity_scale.pack(fill=tk.X, pady=5)
        
        self.productivity_label = tk.Label(
            productivity_frame,
            text="3 - Good",
            font=Constants.SMALL_FONT,
            bg=Constants.WHITE,
            fg=Constants.PRIMARY_COLOR
        )
        self.productivity_label.pack()
        
        # Notes
        notes_frame = tk.Frame(self.parent, bg=Constants.WHITE)
        notes_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        tk.Label(notes_frame, text="Notes (optional):", font=Constants.NORMAL_FONT, 
                bg=Constants.WHITE).pack(anchor=tk.W)
        self.notes_text = scrolledtext.ScrolledText(notes_frame, height=5, 
                                                     font=Constants.SMALL_FONT)
        self.notes_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Buttons
        button_frame = tk.Frame(self.parent, bg=Constants.WHITE)
        button_frame.pack(pady=20, padx=20, fill=tk.X)
        
        save_button = tk.Button(
            button_frame,
            text="Save Study Session",
            command=self.on_save,
            bg=Constants.PRIMARY_COLOR,
            fg=Constants.WHITE,
            font=Constants.BUTTON_FONT,
            cursor="hand2",
            relief=tk.RAISED,
            borderwidth=2
        )
        save_button.pack(fill=tk.X, pady=5)
        
        clear_button = tk.Button(
            button_frame,
            text="Clear Form",
            command=self.on_clear,
            bg=Constants.DANGER_COLOR,
            fg=Constants.WHITE,
            font=Constants.SMALL_FONT,
            cursor="hand2"
        )
        clear_button.pack(fill=tk.X, pady=5)
    
    def _update_productivity_label(self, value):
        """Update the productivity level label"""
        value = int(float(value))
        self.productivity_label.config(text=MessageGenerator.get_productivity_label(value))
    
    def get_values(self) -> dict:
        """Get form values"""
        return {
            'subject': self.subject_entry.get().strip(),
            'duration': self.duration_entry.get().strip(),
            'productivity': self.productivity_var.get(),
            'notes': self.notes_text.get("1.0", tk.END).strip()
        }
    
    def clear(self):
        """Clear all form fields"""
        self.subject_entry.delete(0, tk.END)
        self.duration_entry.delete(0, tk.END)
        self.productivity_var.set(3)
        self.notes_text.delete("1.0", tk.END)
        self._update_productivity_label(3)


class ActionPanel:
    """Panel with action buttons for viewing progress"""
    
    def __init__(self, parent: tk.Frame, callbacks: dict):
        """
        Initialize the action panel.
        
        Args:
            parent: Parent tkinter frame
            callbacks: Dictionary of callback functions for each action
        """
        self.parent = parent
        self.callbacks = callbacks
        self.stats_label = None
        
        self._create_panel()
    
    def _create_panel(self):
        """Create the action panel widgets"""
        
        # Actions title
        actions_title = tk.Label(
            self.parent,
            text="View Progress",
            font=Constants.HEADING_FONT,
            bg=Constants.WHITE,
            fg=Constants.TEXT_COLOR
        )
        actions_title.pack(pady=15)
        
        # Action buttons
        actions_container = tk.Frame(self.parent, bg=Constants.WHITE)
        actions_container.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        
        buttons_config = [
            ("View Subject Distribution", "subject_distribution", Constants.SECONDARY_COLOR),
            ("View Time Spent Chart", "time_chart", Constants.PURPLE_COLOR),
            ("Weekly Summary", "weekly_summary", Constants.WARNING_COLOR),
            ("View All Sessions", "all_sessions", "#3498db"),
            ("Export CSV", "export_csv", "#16a085"),
            ("Clear All Data", "clear_data", Constants.BUTTON_RED)
        ]
        
        for text, callback_key, color in buttons_config:
            tk.Button(
                actions_container,
                text=text,
                command=self.callbacks.get(callback_key),
                bg=color,
                fg=Constants.WHITE,
                font=Constants.NORMAL_FONT + ("bold",),
                cursor="hand2",
                height=2
            ).pack(fill=tk.X, pady=10)
        
        # Stats display
        stats_frame = tk.Frame(self.parent, bg=Constants.LIGHT_GRAY, 
                              relief=tk.SUNKEN, borderwidth=2)
        stats_frame.pack(pady=10, padx=20, fill=tk.X)
        
        self.stats_label = tk.Label(
            stats_frame,
            text="Total Sessions: 0\nTotal Time: 0 min",
            font=Constants.SMALL_FONT,
            bg=Constants.LIGHT_GRAY,
            fg=Constants.DARK_GRAY,
            justify=tk.LEFT
        )
        self.stats_label.pack(pady=10)
    
    def update_stats(self, session_count: int, total_time: int):
        """Update statistics display"""
        time_str = TimeFormatter.format_minutes(total_time)
        self.stats_label.config(
            text=f"Total Sessions: {session_count}\nTotal Time: {time_str}"
        )


class SessionsTable:
    """Table view for displaying all study sessions"""
    
    @staticmethod
    def create_window(sessions: list, parent: tk.Tk):
        """
        Create a window displaying all sessions in a table.
        
        Args:
            sessions: List of study sessions
            parent: Parent tkinter window
        """
        # Create new window
        sessions_window = tk.Toplevel(parent)
        sessions_window.title("All Study Sessions")
        sessions_window.geometry("900x600")
        
        # Title
        title = tk.Label(
            sessions_window,
            text="All Study Sessions",
            font=Constants.HEADING_FONT,
            bg=Constants.PRIMARY_COLOR,
            fg=Constants.WHITE
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
        for session in reversed(sessions):
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


class WeeklySummaryWindow:
    """Window displaying weekly study summary"""
    
    @staticmethod
    def create_window(sessions: list, stats: dict, parent: tk.Tk):
        """
        Create a window displaying weekly summary.
        
        Args:
            sessions: List of weekly sessions
            stats: Dictionary containing calculated statistics
            parent: Parent tkinter window
        """
        # Create summary window
        summary_window = tk.Toplevel(parent)
        summary_window.title("Weekly Summary")
        summary_window.geometry("600x500")
        summary_window.configure(bg=Constants.WHITE)
        
        # Title
        title = tk.Label(
            summary_window,
            text="Weekly Study Summary",
            font=("Arial", 18, "bold"),
            bg=Constants.WHITE,
            fg=Constants.PRIMARY_COLOR
        )
        title.pack(pady=20)
        
        # Summary text
        summary_frame = tk.Frame(summary_window, bg=Constants.LIGHT_GRAY, 
                                relief=tk.RAISED, borderwidth=2)
        summary_frame.pack(padx=30, pady=10, fill=tk.BOTH, expand=True)
        
        hours, minutes = TimeFormatter.format_time_detailed(stats['total_time'])
        
        summary_text = f"""
        Summary for Last 7 Days
        
        Total Study Sessions: {stats['session_count']}
        
        Total Time Studied: {hours}h {minutes}min
        
        Average Productivity: {stats['avg_productivity']:.1f}/5
        
        Most Studied Subject: {stats['most_studied'][0]} ({stats['most_studied'][1]} min)
        
        Subjects Covered: {stats['subject_count']}
        """
        
        summary_label = tk.Label(
            summary_frame,
            text=summary_text,
            font=("Arial", 12),
            bg=Constants.LIGHT_GRAY,
            fg=Constants.DARK_GRAY,
            justify=tk.LEFT
        )
        summary_label.pack(pady=20, padx=20)
        
        # Motivational message
        motivation = MessageGenerator.get_random_motivation()
        motivation_label = tk.Label(
            summary_window,
            text=f"{motivation}",
            font=("Arial", 11, "italic"),
            bg=Constants.WHITE,
            fg=Constants.SECONDARY_COLOR,
            wraplength=500
        )
        motivation_label.pack(pady=20)

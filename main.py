"""
Smart Study Tracker 
A comprehensive study tracking application with GUI, data visualization, and progress monitoring.
"""


import tkinter as tk
from tkinter import messagebox

from data_manager import DataManager
from visualizer import Visualizer
from gui_components import StudyInputForm, ActionPanel, SessionsTable, WeeklySummaryWindow
from utils import Constants, MessageGenerator, Validator


class StudyTrackerApp:
    """Main application class for the Smart Study Tracker"""
    
    def __init__(self, root: tk.Tk):
        """
        Initialize the Study Tracker application.
        
        Args:
            root: The main tkinter window
        """
        self.root = root
        self.root.title("Smart Study Tracker")
        self.root.geometry("900x700")
        self.root.configure(bg=Constants.BACKGROUND_COLOR)
        
        # Initialize components
        self.data_manager = DataManager()
        self.visualizer = Visualizer()
        
        # GUI components
        self.input_form = None
        self.action_panel = None
        
        # Create the GUI
        self._create_gui()
        
        # Load and display initial stats
        self._update_stats()
    
    def _create_gui(self):
        """Create all GUI components"""
        
        # Title bar
        self._create_title_bar()
        
        # Main container
        main_container = tk.Frame(self.root, bg=Constants.BACKGROUND_COLOR)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Left side - Input form
        left_frame = tk.Frame(main_container, bg=Constants.WHITE, 
                             relief=tk.RAISED, borderwidth=2)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        self.input_form = StudyInputForm(
            left_frame,
            on_save=self._save_session,
            on_clear=self._clear_form
        )
        
        # Right side - Actions and info
        right_frame = tk.Frame(main_container, bg=Constants.WHITE, 
                              relief=tk.RAISED, borderwidth=2)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        action_callbacks = {
            'subject_distribution': self._show_subject_distribution,
            'time_chart': self._show_time_chart,
            'weekly_summary': self._show_weekly_summary,
            'all_sessions': self._show_all_sessions,
            'export_csv': self._export_csv,
            'clear_data': self._clear_all_data
        }
        
        self.action_panel = ActionPanel(right_frame, action_callbacks)
    
    def _create_title_bar(self):
        """Create the application title bar"""
        title_frame = tk.Frame(self.root, bg=Constants.PRIMARY_COLOR, height=60)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame,
            text="Smart Study Tracker",
            font=Constants.TITLE_FONT,
            bg=Constants.PRIMARY_COLOR,
            fg=Constants.WHITE
        )
        title_label.pack(pady=10)
    
    def _save_session(self):
        """Handle saving a new study session"""
        # Get form values
        values = self.input_form.get_values()
        
        # Validate subject
        is_valid, error_msg = Validator.validate_subject(values['subject'])
        if not is_valid:
            messagebox.showwarning("Missing Information", error_msg)
            return
        
        # Validate duration
        is_valid, error_msg, duration = Validator.validate_duration(values['duration'])
        if not is_valid:
            messagebox.showerror("Invalid Input", error_msg)
            return
        
        # Validate productivity
        is_valid, error_msg = Validator.validate_productivity(values['productivity'])
        if not is_valid:
            messagebox.showerror("Invalid Input", error_msg)
            return
        
        # Save the session
        success = self.data_manager.add_session(
            subject=values['subject'],
            duration=duration,
            productivity=values['productivity'],
            notes=values['notes']
        )
        
        if success:
            # Show success message
            message = MessageGenerator.get_session_saved_message(
                duration, values['subject']
            )
            messagebox.showinfo("Session Saved!", message)
            
            # Clear form and update stats
            self._clear_form()
            self._update_stats()
        else:
            messagebox.showerror("Error", "Failed to save session. Please try again.")
    
    def _clear_form(self):
        """Clear the input form"""
        self.input_form.clear()
    
    def _update_stats(self):
        """Update statistics display"""
        session_count = self.data_manager.get_session_count()
        total_time = self.data_manager.get_total_time()
        self.action_panel.update_stats(session_count, total_time)
    
    def _show_subject_distribution(self):
        """Show pie chart of time distribution by subject"""
        sessions = self.data_manager.get_all_sessions()
        
        if not sessions:
            messagebox.showinfo("No Data", "No study sessions recorded yet!")
            return
        
        subject_time = self.data_manager.get_subject_time()
        
        # Create new window
        chart_window = tk.Toplevel(self.root)
        chart_window.title("Subject Distribution")
        chart_window.geometry("800x600")
        
        self.visualizer.create_pie_chart(subject_time, chart_window)
    
    def _show_time_chart(self):
        """Show bar chart of total time spent on each subject"""
        sessions = self.data_manager.get_all_sessions()
        
        if not sessions:
            messagebox.showinfo("No Data", "No study sessions recorded yet!")
            return
        
        subject_time = self.data_manager.get_subject_time()
        
        # Create new window
        chart_window = tk.Toplevel(self.root)
        chart_window.title("Time Spent by Subject")
        chart_window.geometry("800x600")
        
        self.visualizer.create_bar_chart(subject_time, chart_window)
    
    def _show_weekly_summary(self):
        """Show weekly study summary"""
        weekly_sessions = self.data_manager.get_weekly_sessions()
        
        if not weekly_sessions:
            messagebox.showinfo("Weekly Summary", "No study sessions in the past 7 days!")
            return
        
        # Calculate statistics
        stats = {
            'session_count': len(weekly_sessions),
            'total_time': self.data_manager.get_total_time(weekly_sessions),
            'avg_productivity': self.data_manager.get_average_productivity(weekly_sessions),
            'most_studied': self.data_manager.get_most_studied_subject(weekly_sessions),
            'subject_count': len(self.data_manager.get_subject_time(weekly_sessions))
        }
        
        WeeklySummaryWindow.create_window(weekly_sessions, stats, self.root)
    
    def _show_all_sessions(self):
        """Display all study sessions"""
        sessions = self.data_manager.get_all_sessions()
        
        if not sessions:
            messagebox.showinfo("No Data", "No study sessions recorded yet!")
            return
        
        SessionsTable.create_window(sessions, self.root)
    
    def _clear_all_data(self):
        """Clear all study session data"""
        result = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete all study sessions?\n\nThis action cannot be undone!"
        )
        
        if result:
            success = self.data_manager.clear_all_data()
            if success:
                messagebox.showinfo("Success", "All data has been cleared.")
                self._update_stats()
            else:
                messagebox.showerror("Error", "Failed to clear data.")

    def _export_csv(self):
        """Export all sessions to a CSV file using DataManager."""
        sessions = self.data_manager.get_all_sessions()
        if not sessions:
            messagebox.showinfo("No Data", "No study sessions to export.")
            return

        csv_path = self.data_manager.export_to_csv()
        if csv_path:
            messagebox.showinfo("Export Complete", f"CSV exported to:\n{csv_path}")
        else:
            messagebox.showerror("Export Failed", "Failed to export sessions to CSV.")


def main():
    """Main function to run the application"""
    root = tk.Tk()
    app = StudyTrackerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

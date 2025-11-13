"""
Data Manager Module
Handles all data storage, retrieval, and manipulation operations for study sessions.
"""

import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional


class DataManager:
    """Manages study session data storage and retrieval"""
    
    def __init__(self, data_file: Optional[str] = None):
        """
        Initialize the data manager.

        If no path is provided, the data file will be created at
        <package_dir>/data/study_data.json. The data directory is created
        automatically if it does not exist.

        Args:
            data_file: Optional path to the JSON file for storing data
        """
        if data_file is None:
            base_dir = os.path.dirname(__file__)
            data_dir = os.path.join(base_dir, "data")
            os.makedirs(data_dir, exist_ok=True)
            self.data_file = os.path.join(data_dir, "study_data.json")
        else:
            # Use provided path and ensure parent directory exists
            parent = os.path.dirname(data_file)
            if parent:
                os.makedirs(parent, exist_ok=True)
            self.data_file = data_file
    
    def load_data(self) -> List[Dict]:
        """
        Load study data from JSON file.
        
        Returns:
            List of study session dictionaries
        """
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading data: {e}")
                return []
        return []
    
    def save_data(self, data: List[Dict]) -> bool:
        """
        Save study data to JSON file.
        
        Args:
            data: List of study session dictionaries
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Ensure parent directory exists (defensive)
            parent = os.path.dirname(self.data_file)
            if parent:
                os.makedirs(parent, exist_ok=True)

            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=4)
            return True
        except IOError as e:
            print(f"Error saving data: {e}")
            return False
    
    def add_session(self, subject: str, duration: int, productivity: int, notes: str = "") -> bool:
        """
        Add a new study session.
        
        Args:
            subject: Subject name
            duration: Duration in minutes
            productivity: Productivity level (1-5)
            notes: Optional notes
            
        Returns:
            True if successful, False otherwise
        """
        session = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "subject": subject,
            "duration": duration,
            "productivity": productivity,
            "notes": notes
        }
        
        data = self.load_data()
        data.append(session)
        return self.save_data(data)
    
    def get_all_sessions(self) -> List[Dict]:
        """
        Get all study sessions.
        
        Returns:
            List of all study sessions
        """
        return self.load_data()
    
    def get_weekly_sessions(self, days: int = 7) -> List[Dict]:
        """
        Get study sessions from the last N days.
        
        Args:
            days: Number of days to look back
            
        Returns:
            List of study sessions from the specified time period
        """
        data = self.load_data()
        cutoff_date = datetime.now() - timedelta(days=days)
        
        weekly_sessions = []
        for session in data:
            try:
                session_date = datetime.strptime(session['timestamp'], "%Y-%m-%d %H:%M:%S")
                if session_date >= cutoff_date:
                    weekly_sessions.append(session)
            except ValueError:
                continue
        
        return weekly_sessions
    
    def get_subject_time(self, sessions: Optional[List[Dict]] = None) -> Dict[str, int]:
        """
        Calculate total time spent per subject.
        
        Args:
            sessions: List of sessions to analyze (if None, uses all sessions)
            
        Returns:
            Dictionary mapping subject names to total minutes
        """
        if sessions is None:
            sessions = self.load_data()
        
        subject_time = {}
        for session in sessions:
            subject = session['subject']
            duration = session['duration']
            subject_time[subject] = subject_time.get(subject, 0) + duration
        
        return subject_time
    
    def get_total_time(self, sessions: Optional[List[Dict]] = None) -> int:
        """
        Calculate total study time.
        
        Args:
            sessions: List of sessions to analyze (if None, uses all sessions)
            
        Returns:
            Total minutes studied
        """
        if sessions is None:
            sessions = self.load_data()
        
        return sum(session['duration'] for session in sessions)
    
    def get_average_productivity(self, sessions: Optional[List[Dict]] = None) -> float:
        """
        Calculate average productivity score.
        
        Args:
            sessions: List of sessions to analyze (if None, uses all sessions)
            
        Returns:
            Average productivity score (0 if no sessions)
        """
        if sessions is None:
            sessions = self.load_data()
        
        if not sessions:
            return 0.0
        
        return sum(s['productivity'] for s in sessions) / len(sessions)
    
    def get_most_studied_subject(self, sessions: Optional[List[Dict]] = None) -> Optional[tuple]:
        """
        Get the most studied subject.
        
        Args:
            sessions: List of sessions to analyze (if None, uses all sessions)
            
        Returns:
            Tuple of (subject_name, total_minutes) or None if no sessions
        """
        subject_time = self.get_subject_time(sessions)
        
        if not subject_time:
            return None
        
        return max(subject_time.items(), key=lambda x: x[1])
    
    def clear_all_data(self) -> bool:
        """
        Delete all study session data.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            if os.path.exists(self.data_file):
                os.remove(self.data_file)
            return True
        except OSError as e:
            print(f"Error clearing data: {e}")
            return False
    
    def get_session_count(self, sessions: Optional[List[Dict]] = None) -> int:
        """
        Get the number of study sessions.
        
        Args:
            sessions: List of sessions to count (if None, uses all sessions)
            
        Returns:
            Number of sessions
        """
        if sessions is None:
            sessions = self.load_data()
        
        return len(sessions)

    def export_to_csv(self, csv_file: Optional[str] = None) -> Optional[str]:
        """
        Export stored sessions to a CSV file.

        If csv_file is None the default path <data_dir>/study_data.csv is used.

        Returns the path to the written CSV on success, or None on failure.
        """
        import csv

        sessions = self.get_all_sessions()
        if not sessions:
            return None

        if csv_file is None:
            base_dir = os.path.dirname(__file__)
            data_dir = os.path.join(base_dir, "data")
            os.makedirs(data_dir, exist_ok=True)
            csv_file = os.path.join(data_dir, "study_data.csv")
        else:
            parent = os.path.dirname(csv_file)
            if parent:
                os.makedirs(parent, exist_ok=True)

        try:
            with open(csv_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["timestamp", "subject", "duration", "productivity", "notes"])
                for s in sessions:
                    writer.writerow([
                        s.get('timestamp', ''),
                        s.get('subject', ''),
                        s.get('duration', ''),
                        s.get('productivity', ''),
                        s.get('notes', '')
                    ])
            return os.path.abspath(csv_file)
        except Exception as e:
            print(f"Error exporting CSV: {e}")
            return None

"""
Utilities Module
Contains helper functions and constants for the study tracker application.
"""

import random
from typing import Tuple


class Constants:
    """Application constants"""
    
    # Color scheme
    PRIMARY_COLOR = "#4a90e2"
    SECONDARY_COLOR = "#27ae60"
    DANGER_COLOR = "#e74c3c"
    WARNING_COLOR = "#e67e22"
    PURPLE_COLOR = "#8e44ad"
    BACKGROUND_COLOR = "#f0f0f0"
    WHITE = "white"
    LIGHT_GRAY = "#ecf0f1"
    DARK_GRAY = "#2c3e50"
    TEXT_COLOR = "#333"
    BUTTON_RED = "#c0392b"
    
    # Font settings
    TITLE_FONT = ("Arial", 24, "bold")
    HEADING_FONT = ("Arial", 16, "bold")
    SUBHEADING_FONT = ("Arial", 14, "bold")
    BUTTON_FONT = ("Arial", 12, "bold")
    NORMAL_FONT = ("Arial", 11)
    SMALL_FONT = ("Arial", 10)
    
    # Productivity level labels
    PRODUCTIVITY_LABELS = {
        1: "1 - Very Low",
        2: "2 - Low",
        3: "3 - Good",
        4: "4 - High",
        5: "5 - Excellent"
    }
    
    # Motivational messages
    MOTIVATIONAL_MESSAGES = [
        "Great job! Keep up the excellent work!",
        "You're making amazing progress!",
        "Consistency is key - you're doing fantastic!",
        "Every study session brings you closer to your goals!",
        "Your dedication is impressive! Keep it up!",
        "Learning is a journey, and you're on the right path!",
        "Proud of your commitment to learning!",
        "Small steps lead to big achievements!",
        "Your hard work will pay off!",
        "Stay focused, stay motivated!",
        "You're building great study habits!",
        "Knowledge is power, and you're gaining it!"
    ]


class MessageGenerator:
    """Generates motivational and feedback messages"""
    
    @staticmethod
    def get_random_motivation() -> str:
        """
        Get a random motivational message.
        
        Returns:
            Random motivational message
        """
        return random.choice(Constants.MOTIVATIONAL_MESSAGES)
    
    @staticmethod
    def get_session_saved_message(duration: int, subject: str) -> str:
        """
        Generate a message for when a session is saved.
        
        Args:
            duration: Study duration in minutes
            subject: Subject name
            
        Returns:
            Formatted success message
        """
        motivation = MessageGenerator.get_random_motivation()
        return f"Successfully logged {duration} minutes of {subject}!\n\n{motivation}"
    
    @staticmethod
    def get_productivity_label(score: int) -> str:
        """
        Get the label for a productivity score.
        
        Args:
            score: Productivity score (1-5)
            
        Returns:
            Descriptive label
        """
        return Constants.PRODUCTIVITY_LABELS.get(score, "1 - Very Low")


class TimeFormatter:
    """Formats time values for display"""
    
    @staticmethod
    def format_minutes(total_minutes: int) -> str:
        """
        Format minutes into hours and minutes string.
        
        Args:
            total_minutes: Total minutes
            
        Returns:
            Formatted string like "2h 30min" or "45 min"
        """
        hours = total_minutes // 60
        minutes = total_minutes % 60
        
        if hours > 0:
            return f"{hours}h {minutes}min"
        return f"{minutes} min"
    
    @staticmethod
    def format_time_detailed(total_minutes: int) -> Tuple[int, int]:
        """
        Convert total minutes to hours and minutes.
        
        Args:
            total_minutes: Total minutes
            
        Returns:
            Tuple of (hours, minutes)
        """
        hours = total_minutes // 60
        minutes = total_minutes % 60
        return hours, minutes


class Validator:
    """Input validation utilities"""
    
    @staticmethod
    def validate_subject(subject: str) -> Tuple[bool, str]:
        """
        Validate subject input.
        
        Args:
            subject: Subject name
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        subject = subject.strip()
        if not subject:
            return False, "Please enter a subject."
        if len(subject) > 100:
            return False, "Subject name is too long (max 100 characters)."
        return True, ""
    
    @staticmethod
    def validate_duration(duration_str: str) -> Tuple[bool, str, int]:
        """
        Validate duration input.
        
        Args:
            duration_str: Duration as string
            
        Returns:
            Tuple of (is_valid, error_message, duration_value)
        """
        if not duration_str.strip():
            return False, "Please enter duration.", 0
        
        try:
            duration = int(duration_str)
            if duration <= 0:
                return False, "Duration must be positive.", 0
            if duration > 1440:  # 24 hours
                return False, "Duration seems too long (max 1440 minutes).", 0
            return True, "", duration
        except ValueError:
            return False, "Please enter a valid number for duration.", 0
    
    @staticmethod
    def validate_productivity(score: int) -> Tuple[bool, str]:
        """
        Validate productivity score.
        
        Args:
            score: Productivity score
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not 1 <= score <= 5:
            return False, "Productivity must be between 1 and 5."
        return True, ""


class StatsCalculator:
    """Calculate various statistics from study data"""
    
    @staticmethod
    def calculate_study_streak(sessions: list) -> int:
        """
        Calculate the current study streak (consecutive days).
        
        Args:
            sessions: List of study sessions
            
        Returns:
            Number of consecutive days studied
        """
        from datetime import datetime, timedelta
        
        if not sessions:
            return 0
        
        # Get unique dates
        dates = set()
        for session in sessions:
            try:
                date = datetime.strptime(session['timestamp'], "%Y-%m-%d %H:%M:%S").date()
                dates.add(date)
            except ValueError:
                continue
        
        if not dates:
            return 0
        
        # Sort dates
        sorted_dates = sorted(dates, reverse=True)
        
        # Check for consecutive days
        streak = 1
        today = datetime.now().date()
        
        # If no study today, check if studied yesterday
        if sorted_dates[0] != today:
            if sorted_dates[0] != today - timedelta(days=1):
                return 0
        
        for i in range(len(sorted_dates) - 1):
            if sorted_dates[i] - sorted_dates[i + 1] == timedelta(days=1):
                streak += 1
            else:
                break
        
        return streak
    
    @staticmethod
    def get_best_productivity_subject(sessions: list) -> Tuple[str, float]:
        """
        Find the subject with highest average productivity.
        
        Args:
            sessions: List of study sessions
            
        Returns:
            Tuple of (subject_name, average_productivity)
        """
        if not sessions:
            return "", 0.0
        
        subject_productivity = {}
        subject_count = {}
        
        for session in sessions:
            subject = session['subject']
            productivity = session['productivity']
            
            subject_productivity[subject] = subject_productivity.get(subject, 0) + productivity
            subject_count[subject] = subject_count.get(subject, 0) + 1
        
        # Calculate averages
        subject_avg = {
            subject: subject_productivity[subject] / subject_count[subject]
            for subject in subject_productivity
        }
        
        if not subject_avg:
            return "", 0.0
        
        best = max(subject_avg.items(), key=lambda x: x[1])
        return best[0], best[1]

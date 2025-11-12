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


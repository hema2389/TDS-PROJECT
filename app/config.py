import os

SECRET = os.getenv("STUDENT_SECRET", "CHANGE_THIS")
EMAIL = os.getenv("STUDENT_EMAIL", "your-email@example.com")

TIME_LIMIT_SECONDS = 170  # must finish before 3 minutes

"""CAPAI application configuration and constants."""

from pathlib import Path

BASE_DIR = Path(__file__).parent
ASSETS_DIR = BASE_DIR / "assets"
DB_PATH = BASE_DIR / "data" / "capai.db"
FAVICON_PATH = ASSETS_DIR / "favicon.png"


def get_logo_path() -> Path:
    """Prefer uploaded logo assets; fall back to bundled SVG."""
    for name in ("logo.png", "logo.jpg", "logo.jpeg", "logo.webp", "logo.svg"):
        candidate = ASSETS_DIR / name
        if candidate.exists():
            return candidate
    return ASSETS_DIR / "logo.svg"


LOGO_PATH = get_logo_path()

COLORS = {
    "primary": "#0A66FF",
    "secondary": "#00B4FF",
    "accent": "#4F46E5",
    "background": "#F5FAFF",
    "text": "#1E293B",
    "success": "#10B981",
    "warning": "#F59E0B",
    "danger": "#EF4444",
}

REGIONS = [
    "North Region",
    "South Region",
    "East Region",
    "West Region",
    "Central Region",
    "Capital District",
]

AGE_GROUPS = ["18-24", "25-34", "35-44", "45-54", "55-64", "65+"]

GENDERS = ["Male", "Female", "Non-binary", "Prefer not to say"]

URBAN_RURAL = ["Urban", "Rural", "Suburban"]

ACCESSIBILITY_OPTIONS = [
    "Wheelchair Access",
    "Senior Citizen Support",
    "Signage Visibility",
    "Language Assistance",
    "Parking Availability",
]

EXPERIENCE_METRICS = [
    "polling_station_accessibility",
    "staff_helpfulness",
    "waiting_time_satisfaction",
    "security_confidence",
    "voting_process_clarity",
    "facility_cleanliness",
    "technology_effectiveness",
    "overall_voting_experience",
]

EXPERIENCE_LABELS = {
    "polling_station_accessibility": "Polling Station Accessibility",
    "staff_helpfulness": "Staff Helpfulness",
    "waiting_time_satisfaction": "Waiting Time Satisfaction",
    "security_confidence": "Security Confidence",
    "voting_process_clarity": "Voting Process Clarity",
    "facility_cleanliness": "Facility Cleanliness",
    "technology_effectiveness": "Technology Effectiveness",
    "overall_voting_experience": "Overall Voting Experience",
}

SECURITY_METRICS = [
    "safety_at_polling_station",
    "trust_in_election_process",
    "confidence_in_vote_security",
]

SECURITY_LABELS = {
    "safety_at_polling_station": "Safety at Polling Station",
    "trust_in_election_process": "Trust in Election Process",
    "confidence_in_vote_security": "Confidence in Vote Security",
}

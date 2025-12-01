# Purpose: Load environment variables and define global settings (API keys, DB path, color scheme).
import os

class Settings:
    def __init__(self):
        self.LUCID_API_KEY = os.getenv("LUCID_API_KEY", "")  # keep empty in code; set via environment
        self.DB_PATH = os.getenv("EB5_DB_PATH", "eb5.db")    # default SQLite path

        # Color scheme for flowchart nodes. Unknown categories default to white ("no color").
        self.COLORS = {
            "employment_income": "#4CAF50",  # green
            "business_income": "#4CAF50",    # green
            "loan": "#FFC107",               # yellow/orange
            "gift": "#9C27B0",               # purple
            "combined": "#FFFFFF"            # white/no fill (escrow/combined)
        }

    def get_color(self, category: str) -> str:
        """Return color for known categories, else 'no color' (white)."""
        return self.COLORS.get(category, "#FFFFFF")

settings = Settings()
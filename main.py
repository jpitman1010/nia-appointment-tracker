from server import app
from your_module.staff_api import staff_bp
from dotenv import load_dotenv
import os

load_dotenv()  # Loads environment variables from .env automatically

# Example usage
DB_URI = os.getenv("DATABASE_URL")  # or whatever variable you have set

app.register_blueprint(staff_bp)
app.register_blueprint(questionnaire_bp)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)

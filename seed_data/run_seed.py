from seeders.question_seeder import seed_all_questionnaires
from models.models import connect_to_db
from server import app  

connect_to_db(app)

if __name__ == "__main__":
    seed_all_questionnaires()

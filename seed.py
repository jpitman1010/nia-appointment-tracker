from models.models import db, Staff, Questionnaire, Question 
from werkzeug.security import generate_password_hash


def create_admin_user():
    admin_email = "admin@example.com"
    admin_password = "admin1234!"  # Remember to use environment variables in production!

    existing_admin = Staff.query.filter_by(email=admin_email).first()
    if existing_admin:
        print("Admin user already exists.")
        return

    hashed_password = generate_password_hash(admin_password)
    admin = Staff(
        fname="Admin",
        lname="User",
        email=admin_email,
        password=hashed_password,
        role="admin",
        enabled=True,
        created_by="system",
        updated_by="system"
    )
    db.session.add(admin)
    db.session.commit()
    print("Admin user created.")

def seed_ess_questions():
    # Find or create ESS questionnaire record
    ess = Questionnaire.query.filter_by(name='ESS').first()
    if not ess:
        ess = Questionnaire(name='ESS', version='1.0', language='en')
        db.session.add(ess)
        db.session.commit()
    
    # Delete existing questions for ESS
    Question.query.filter_by(questionnaire_id=ess.id).delete()
    db.session.commit()

    # Insert new questions
    for q in ess_questions:
        question = Question(
            questionnaire_id=ess.id,
            question_code=q['question_code'],
            display_text=q['display_text'],
            order=q['order']
        )
        db.session.add(question)

    db.session.commit()
    print("ESS questions seeded successfully.")

if __name__ == "__main__":
    from server import app  # Or wherever your Flask app is
    with app.app_context():
        create_admin_user()

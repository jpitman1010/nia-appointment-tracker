from models.models import db, Role
from server import app
from werkzeug.security import generate_password_hash



# Store hashed_password in the database, NOT plain-text password
hashed_password = generate_password_hash('plain-text-password')

def seed_roles():
    with app.app_context():
        roles = [
            Role(
                name='physician',
                description='Can prescribe medications and place orders',
                can_prescribe=True,
                can_order_tests=True,
                can_manage_users=False,
                can_view_billing=True,
                can_view_research_data=False,
                can_schedule_appointments=True
            ),
            Role(
                name='clinician',
                description='Can place orders, view billing, schedule appointments',
                can_prescribe=False,
                can_order_tests=True,
                can_manage_users=False,
                can_view_billing=True,
                can_view_research_data=False,
                can_schedule_appointments=True
            ),
            Role(
                name='admin',
                description='Full access including user management',
                can_prescribe=False,
                can_order_tests=False,
                can_manage_users=True,
                can_view_billing=True,
                can_view_research_data=True,
                can_schedule_appointments=True
            ),
            Role(
                name='administration',
                description='Front desk / scheduler limited access',
                can_prescribe=False,
                can_order_tests=False,
                can_manage_users=False,
                can_view_billing=False,
                can_view_research_data=False,
                can_schedule_appointments=True
            ),
            Role(
                name='research_coordinator',
                description='Access to all research data',
                can_prescribe=False,
                can_order_tests=False,
                can_manage_users=False,
                can_view_billing=False,
                can_view_research_data=True,
                can_schedule_appointments=False
            ),
        ]

        for role in roles:
            existing = Role.query.filter_by(name=role.name).first()
            if not existing:
                db.session.add(role)

        db.session.commit()
        print("Default roles seeded.")

if __name__ == "__main__":
    seed_roles()

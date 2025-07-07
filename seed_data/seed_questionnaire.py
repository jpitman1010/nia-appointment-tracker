import json
from models.models import db, Questionnaire, Question
from sqlalchemy.exc import IntegrityError

def seed_questionnaire_from_json(json_filepath):
    with open(json_filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    existing = Questionnaire.query.filter_by(name=data['name'], version=data['version'], language=data['language']).first()
    if existing:
        for q in existing.questions:
            # Delete options first
            for opt in q.options:
                db.session.delete(opt)
            db.session.delete(q)
        db.session.delete(existing)
        db.session.commit()

    questionnaire = Questionnaire(
        name=data['name'],
        version=data['version'],
        language=data['language']
    )
    db.session.add(questionnaire)
    db.session.commit()

    for order_idx, q in enumerate(data['questions'], start=1):
        question = Question(
            questionnaire_id=questionnaire.id,
            question_code=q['question_code'],
            display_text=q['text'],
            order=order_idx
        )
        db.session.add(question)
        db.session.flush()  # to get question.id before commit

        # Insert options if any
        options = q.get('options', [])
        for opt_order, opt in enumerate(options, start=1):
            option = QuestionOption(
                question_id=question.id,
                option_text=opt.get('text'),
                option_value=opt.get('value', opt.get('text')),
                order=opt_order
            )
            db.session.add(option)

    db.session.commit()
    print(f"Seeded questionnaire '{data['name']}' with {len(data['questions'])} questions and options.")

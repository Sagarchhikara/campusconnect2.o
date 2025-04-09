# reset_alembic.py
from app import db
from sqlalchemy import text

# Make sure to import/create your Flask app here if needed:
from app import app

with app.app_context():
    with db.engine.connect() as conn:
        conn.execute(text("DELETE FROM alembic_version"))
        conn.commit()

print("✅ alembic_version table cleared. You're good to go!")

from sqlalchemy import text
from database import engine

# Add the deadline column to the boards table
with engine.connect() as conn:
    try:
        conn.execute(text("ALTER TABLE boards ADD COLUMN deadline VARCHAR(100)"))
        conn.commit()
        print("✓ Deadline column added successfully!")
    except Exception as e:
        print(f"Column might already exist or error: {str(e)}")
        conn.rollback()

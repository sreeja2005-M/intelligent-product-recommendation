from sqlalchemy import text
from backend.database import engine

try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        print("✅ MySQL connected successfully!")
        print("Test result:", result.scalar())

except Exception as e:
    print("❌ Database connection failed!")
    print("Error:", e)
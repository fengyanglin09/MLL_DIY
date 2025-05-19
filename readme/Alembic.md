**Basic steps:**
1. Install Alembic:  
   ```
   pip install alembic
   ```
2. Initialize Alembic in your project:  
   ```
   alembic init alembic
   ```
3. Configure `alembic.ini` and `env.py` to use your database and models.
4. Generate a migration after schema changes:  
   ```
   alembic revision --autogenerate -m "Describe your change"
   ```
5. Apply the migration:  
   ```
   alembic upgrade head
   ```

This workflow keeps your database schema up to date with your code changes.
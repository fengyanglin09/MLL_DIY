**Basic steps:**
1. Install Alembic:  
   ```shell
   pip install alembic
   ```
2. Initialize Alembic in your project:  
```shell
   alembic init alembic
```
3. Configure `alembic.ini` and `env.py` to use your database and models.

4. Generate a migration after schema changes:  
```shell
  alembic revision --autogenerate -m "Describe your change"
```
5. Apply the migration:  
```shell
  alembic upgrade head
```

This workflow keeps your database schema up to date with your code changes.
### Overall Stacks

Pydantic / Python Equivalents:
✅ 1. SQLModel
Built on top of Pydantic and SQLAlchemy

Designed for defining models that are both Pydantic models and SQLAlchemy ORM models

Great for FastAPI projects

📦 pip install sqlmodel


✅ 2. SQLAcodegen – DB to model code generator
Reverse-engineers your DB and generates SQLAlchemy ORM classes.

You can use those models with Pydantic via SQLModel or manually wrap them.

📦 pip install sqlacodegen


✅ 3. Alembic + Autogenerate (for migrations)
Analogous to Flyway/Liquibase

Automatically generates migration scripts by inspecting model changes

Usually used alongside SQLAlchemy/SQLModel


✅ 4. VS Code or PyCharm + Pydantic Plugin
PyCharm has a Pydantic plugin (JetBrains Marketplace) with model completion and hints

VS Code has extensions for FastAPI/Pydantic as well



### Alembic
✅ 1. Install Alembic
```shell
pip install alembic
```

✅ 2. Initialize Alembic in your project
```shell
alembic init alembic
```

This creates:
```markdown
        alembic/
          env.py
          script.py.mako
          versions/
        alembic.ini
```

✅ 3. Edit alembic.ini — set your database URL
```yaml
sqlalchemy.url = sqlite:///./test.db
# or
# sqlalchemy.url = postgresql://user:pass@localhost/mydb

```

✅ 4. Tell Alembic where your models are (in alembic/env.py)
Find the section that looks like this:

```python
# add your model's MetaData object here for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
```

Change it to point to your model’s metadata. Example with SQLModel:

```python
from sqlmodel import SQLModel
target_metadata = SQLModel.metadata
```

If your models are in a different file, you might need to import them as well so Alembic can "see" them.
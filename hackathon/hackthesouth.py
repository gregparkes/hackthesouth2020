from app import app, db
from app.models import User, Post

# set DATABASE_URL=postgresql://postgres:password@localhost:5432/hackthesouth
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}

# https://guicommits.com/how-sql-injection-attack-works-with-examples/
# Date: N/A

DB_FILENAME = os.path.realpath("data/test.db")
def _get_connection() -> sqlite3.Connection:
    ...

@contextlib.contextmanager
def connection_context():
    ...

def get_challenges_for_candidate(cpf: str) -> List[Any]:
    query = f"""
        SELECT title, score FROM challenges c
        JOIN users u
        ON u.id = c.user_id
        WHERE u.cpf='{cpf}';
    """
    ...

    with connection_context() as cur:
        cur.execute(query)
        results = cur.fetchall()

        return results
    
from db_commands import start_database
from flask_app import app

if __name__ == "__main__":
    start_database()
    app.run()
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "data" / "warehouse.db"
SQL_PATH = BASE_DIR / "sql" / "analytics_queries.sql"

def split_sql_statements(sql_text: str):
    """
    Parser function to break down a single large .sql text script file 
    into individual execute-ready SQL commands, stripping comments and empty lines.
    """
    statements = []
    buff = []
    for line in sql_text.splitlines():
        stripped = line.strip()
        if stripped.startswith("--") or stripped == "":
            continue
        buff.append(line)
        if stripped.endswith(";"):
            statements.append("\n".join(buff))
            buff = []
    if buff:
        statements.append("\n".join(buff))
    return statements

def main():
    # Read raw query string commands from the analytics file
    sql_text = SQL_PATH.read_text(encoding="utf-8")
    statements = split_sql_statements(sql_text)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Iterate through and execute each isolated analytical SQL statement in sequence
    for i, stmt in enumerate(statements, start=1):
        print(f"\n--- Query {i} ---")
        print(stmt)
        cur.execute(stmt)
        rows = cur.fetchall()

        # Limit output visualization to the top 20 rows to keep logging concise
        for r in rows[:20]:
            print(r)

    conn.close()

if __name__ == "__main__":
    main()
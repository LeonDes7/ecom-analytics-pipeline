import duckdb
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "ecom_warehouse.duckdb"
SQL_PATH = BASE_DIR / "sql" / "analytics_queries.sql"

def split_sql_statements(sql_text: str):
    """
    Parser to break a .sql script into individual executable statements,
    stripping comments and empty lines.
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
    sql_text = SQL_PATH.read_text(encoding="utf-8")
    statements = split_sql_statements(sql_text)

    conn = duckdb.connect(str(DB_PATH))

    for i, stmt in enumerate(statements, start=1):
        print(f"\n--- Query {i} ---")
        print(stmt)
        rows = conn.execute(stmt).fetchmany(20)
        for r in rows:
            print(r)

    conn.close()

if __name__ == "__main__":
    main()

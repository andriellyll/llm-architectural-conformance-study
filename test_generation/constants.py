import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

_pg_user = os.getenv("POSTGRES_USER", "postgres")
_pg_password = os.getenv("POSTGRES_PASSWORD", "mysecretpassword")
_pg_host = os.getenv("POSTGRES_HOST", "localhost")
_pg_port = os.getenv("POSTGRES_PORT", "5432")

connection_string = f"postgresql://{_pg_user}:{_pg_password}@{_pg_host}:{_pg_port}"
db_name = os.getenv("POSTGRES_DB", "archunit_docs")
table_name = "docs"
contents_dir = BASE_DIR / "archunit-docs" / "archunit"
embed_dim = 1024

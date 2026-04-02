
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

connection_string = "postgresql://postgres:mysecretpassword@localhost:5432"
db_name = "archunit_docs"
table_name="docs"
contents_dir=BASE_DIR / "archunit-docs" / "archunit"
embed_dim=1024
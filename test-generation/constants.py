connection_string = "postgresql://postgres:mysecretpassword@localhost:5432"
db_name = "archunit_docs"
table_name="docs"
contents_dir="./data/archunit"
embed_dim=1024

# docker run --name pgvector-db \
#   -e POSTGRES_PASSWORD=mysecretpassword \
#   -e POSTGRES_USER=postgres \
#   -e POSTGRES_DB=archunit_docs \
#   -p 5432:5432 \
#   -d pgvector/pgvector:pg16
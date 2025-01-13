import reflex as rx

db_host = "localhost"
db_port = 5432


config = rx.Config(
    app_name="front_end",
    db_url=f"postgresql+psycopg2://postgres:postgres@{db_host}:{db_port}/postgres",
    # deploy_url="http://159.75.120.46:13000",
    # api_url="http://159.75.120.46:18000",
)

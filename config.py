SQL_SERVER = 'localhost'
SQL_DATABASE = 'AutoRepair'
SQL_USERNAME = 'your_user'
SQL_PASSWORD = 'your_password'

SQLALCHEMY_DATABASE_URI = (
    f'mssql+pyodbc://{SQL_USERNAME}:{SQL_PASSWORD}@{SQL_SERVER}/{SQL_DATABASE}'
    '?driver=ODBC+Driver+17+for+SQL+Server'
)
SQLALCHEMY_TRACK_MODIFICATIONS = False
from sqlalchemy import create_engine

class RdsUploader:
    def __init__(self):
        DATABASE_TYPE = 'postgresql'
        DBAPI = 'psycopg2'
        ENDPOINT =  # 
        USER = 'postgres'
        PASSWORD = # 
        PORT = 5432
        DATABASE = 'postgres'
        self.engine = create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{ENDPOINT}:{PORT}/{DATABASE}")
        self.engine.connect()
    def add_row(self, table, columns: list, values: list):
        self.engine.execute(f'''
                            INSERT INTO {table} ({*columns})
                            VALUES ({*values});
                            '''

    def delete_row(self, table, columns: list, values: list):
        self.engine.execute(f'''
                            INSERT INTO {table} ({*columns})
                            VALUES ({*values});
                            '''
    def update_row(self, table, columns: list, values: list):
        self.engine.execute(f'''
                            INSERT INTO {table} ({*columns})
                            VALUES ({*values});
                            '''
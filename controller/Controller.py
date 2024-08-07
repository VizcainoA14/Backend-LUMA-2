from sqlalchemy import create_engine, text
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from controller.Setup import set_up


class Controller:

    def __init__(self):
        self.config = set_up()

        DBNAME = self.config['POSTGRES_DATABASE']
        USER = self.config['POSTGRES_USER']
        PASSWORD = self.config['POSTGRES_PASSWORD']
        HOST = self.config['POSTGRES_HOST']
        PORT = "5432"

        #self.engine = create_engine(f'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}')
        self.engine = create_engine('sqlite:///C://Users//adria//Desktop//Backend LUMA//DATA.db')
        self.conn = self.engine.connect()



    def get_data(self, startdate: str, enddate: str):
            session = self.conn

            try:
                tables = ['eit171', 'eit195', 'eit284', 'eit304', 'hmiigr', 'hmimag']
                namerow = ['data171', 'data195', 'data284', 'data304', 'datahmiigr', 'datahmimag']
                data = {}

                for table, name in zip(tables, namerow):
                    query = text(f"SELECT * FROM {table} WHERE date BETWEEN '{startdate}' AND '{enddate}'")
                    result = session.execute(query).fetchall()
                    data[name] = {"rows": [dict(row._mapping) for row in result]}

            except SQLAlchemyError as error:
                return JSONResponse(content={"error": str(error)}, status_code=500)
            finally:
                session.close()

            return JSONResponse(content=data)
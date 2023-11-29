import os
from sqlalchemy.orm.mapper import Mapper
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine
from dotenv import load_dotenv
from sqlalchemy.inspection import inspect


class Base:

    def __init__(self):
        load_dotenv()
        self.tables = {}
        user = os.environ.get("USER")
        database = os.environ.get("DATABASE")
        url = os.environ.get("URL")
        password = os.environ.get("PASSWORD")
        port = os.environ.get("PORT")
        self.engine = create_engine(
            f"postgresql+psycopg2://{user}:{password}@{url}:{port}/{database}",
            isolation_level="SERIALIZABLE")
        self.__map_tables()

    def __map_tables(self):
        BaseAutoMap = automap_base()
        BaseAutoMap.prepare(autoload_with=self.engine)
        for i in BaseAutoMap.classes:
            try:
                self.tables[str(i.__table__)] = i
            except (TypeError):
                continue

    def get_tables(self):
        return list(self.tables.keys())

    def check_instance(self, rel):
        if isinstance(rel[1].__dict__['argument'], Mapper):
            child_name = str(
                rel[1].__dict__['argument'].__dict__['class_']
                .__table__)
        else:
            child_name = str(rel[1].__dict__['argument'].__table__)

        return child_name

    def connections(self, table):
        children = []
        relations = inspect(self.tables[table]).relationships.items()
        for rel in relations:
            children.append(self.check_instance(rel))

        return children

    def wr_dependence(self, start_table, end_table):
        relations = inspect(self.tables[start_table]).relationships.items()
        for rel in relations:
            child_name = self.check_instance(rel)
            if child_name == end_table:
                table1 = str(rel[1].__dict__["synchronize_pairs"][0][0])
                table2 = str(rel[1].__dict__["synchronize_pairs"][0][1])
                query = f"{table1} = {table2}"

                return query

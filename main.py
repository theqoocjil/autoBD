from database.Base import Base
from graph.Graph import Graph


def create_SQL(db, path, column1, column2):
    path_len = len(path)
    selected_tables = ", ".join(path)
    sql_query = f"select {path[0]}.{column1}, {path[path_len-1]}{column2}" \
        f" from {selected_tables} where "
    for table in range(path_len - 1):
        _add = db.wr_dependence(path[table], path[table+1])
        sql_query += _add
        if table != path_len - 2:
            sql_query += " and "

    return sql_query


def main():
    db = Base()
    gh = Graph(db)
    path = (gh.bfs('person', 'case'))
    if path != 0:
        print(create_SQL(db, path, "name", "caseid"))
    else:
        print("Error")


if __name__ == "__main__":
    main()

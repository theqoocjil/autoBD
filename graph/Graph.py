class Graph:

    def __init__(self, db):
        self.graph = {f"{table}":
                      db.connections(table) for table in db.get_tables()}

    def tables_exit(self, tables):
        try:
            for i in tables:
                self.graph[i]
            return 200
        except KeyError:
            return 400

    def bfs(self, start, end):
        if self.tables_exit([start, end]) == 200:
            pass
        else:
            return 0
        queue = [[start]]

        while queue:
            path = queue.pop(0)
            node = path[-1]

            if node == end:
                return path
            else:
                for neighbor in self.graph[node]:
                    new_path = list(path)
                    new_path.append(neighbor)
                    queue.append(new_path)

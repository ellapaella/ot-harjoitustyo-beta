
class User:

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.graphs = []

    def add_graph(self, graph):
        self.graphs.append(graph)

    def __str__(self):
        return f"{self.username}, has saved {len(self.graphs)} graphs"

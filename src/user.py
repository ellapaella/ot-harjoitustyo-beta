
class User:
    def __init__(self, name: str, password: str):
        self.name = name
        self.password = password
        self.graphs_list = []

    def add_graph(self, graph):
        self.graphs_list.append(graph)

    def __str__(self):
        return f"{self.name}, has saved {len(self.graphs_list)} graphs"

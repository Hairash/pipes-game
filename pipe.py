class Pipe:
    def __init__(self, path):
        if len(path) < 3:
            raise Exception('Pipe with zero length')
        self.edges = [
            {'entry_point': path[0], 'pipe_edge': path[1]},
            {'entry_point': path[-1], 'pipe_edge': path[-2]}
        ]
        self.path = path

    def __str__(self):
        return f'Pipe {self.path}'

    def __del__(self):
        # erase pipe
        pass

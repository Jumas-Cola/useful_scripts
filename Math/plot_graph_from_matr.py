import networkx as nx
from networkx.drawing.nx_agraph import to_agraph

def plot_graph_from_matr(matr, path='multi.png'):
    x_size = len(matr)
    y_size = len(matr[0])

    if x_size != y_size:
        raise Exception(
            'Matrix shape is: {}x{}\nMatrx should be square.'.format(x_size, y_size))

    G = nx.MultiDiGraph()
    G.add_nodes_from(range(1, x_size + 1))

    for i, row in enumerate(matr):
        for j, col in enumerate(row):
            if col:
                G.add_edge(i + 1, j + 1)

    G.graph['edge'] = {'arrowsize': '0.6', 'splines': 'curved'}
    G.graph['graph'] = {'scale': '3'}

    A = to_agraph(G)
    A.layout('dot')
    A.draw(path)


plot_graph_from_matr([
    [0, 1, 0, 1],
    [0, 0, 2, 0],
    [1, 1, 1, 0],
    [1, 0, 1, 1],
])

import networkx as nx
from networkx.drawing.nx_agraph import to_agraph

def graph_from_adjacency_matrix(matr):
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
    return G

def graph_from_aincidence_matrix(matr):
    cols = [[row[i]for row in matr] for i in range(len(matr[0]))]

    G = nx.MultiDiGraph()
    G.add_nodes_from(range(1, len(matr) + 1))

    for n, col in enumerate(cols):
        if col.count(1) == col.count(-1) == 1 and col.count(0) == len(col) - 2:
            G.add_edge(col.index(1) + 1, col.index(-1) + 1)
        elif col.count(1) == 2 and col.count(0) == len(col) - 2:
            G.add_edge(col.index(1) + 1, len(col) - col[::-1].index(1) - 1)
            G.add_edge(len(col) - col[::-1].index(1) - 1, col.index(1) + 1)
        elif col.count(0) == len(col) - 1 and len([i for i in col if i not in (0, 1, -1)]) == 1:
            non_zero = [n for n,i in enumerate(col) if i != 0][0] + 1
            G.add_edge(non_zero, non_zero)
        else:
            raise Exception('Incorrect column: {}\nOn pos: {}'.format(col, n))
    return G


def plot_graph(G, path='multi.png'):
    G.graph['edge'] = {'arrowsize': '0.6', 'splines': 'curved'}
    G.graph['graph'] = {'scale': '3'}

    A = to_agraph(G)
    A.layout('dot')
    A.draw(path)



#G = graph_from_adjacency_matrix([
#    [0, 1, 0, 1],
#    [0, 0, 2, 0],
#    [1, 1, 1, 0],
#    [1, 0, 1, 1],
#])
#plot_graph(G)

#G = graph_from_aincidence_matrix([
#    [1, 2, 0, -1, 0,  1],
#    [-1,0, 0,  0, 0,  0],
#    [0, 0, 1,  1, 0,  0],
#    [0, 0,-1,  0, 2, -1],
#])
#plot_graph(G)


#G = nx.MultiDiGraph()
#G.add_nodes_from(range(1, 5))
#G.add_edges_from([(2, 3), (1, 4), (3, 1), (2, 4)])
#G.remove_node(1)
#plot_graph(G)




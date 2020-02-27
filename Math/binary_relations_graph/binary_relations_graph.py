
import matplotlib.pyplot as plt
import networkx as nx
import itertools

class Drawer(object):
    def __init__(self, file_name='graph.png'):
        self.graph = nx.Graph()
        self.file_name = file_name

    def draw(self):
        options = {
            'node_color': '#A0CBE2', # цвет узла
            'node_size': 1000, # размер узла
            'edge_color': '#C0C0C0', # цвет соединений
            'font_size': 17, # размер шрифта
            'with_labels': True, # печатать ли заголовки узлов
            'arrows': True
        }
        nx.draw(self.graph, pos=nx.spring_layout(self.graph), **options)
        # устанавливаем размер изображения в дюймах
        plt.gcf().set_size_inches(10, 10)
        plt.savefig(self.file_name)

# функция бинарного отношения
def T(x, y):
    if ((x+y)**(0.5))%1==0:
        return True
    else:
        return False




elems = [i for i in range(1,16)]# элементы
edges = [] #список групп
count = 2 #количество элементов в группе
# Пишем отношения в файл и список
f = open('edges.csv', 'a', encoding='utf-8')
for i in itertools.product(elems, repeat=count):
    # бинарное отношение
    if T(i[0],i[1]):
        print(i)
        edges.append(i)
        f.write(str(i)+'\n')
f.close()

G = nx.DiGraph() # создание объекта графа(с направлениями)
G.add_edges_from(edges) # добавление групп в граф

# отрисовка графа в .png изображение
Graph = Drawer()
Graph.graph = G
Graph.draw()
binary_relations_graph ![Python 3.6](https://pp.userapi.com/c846523/v846523407/b716d/N3RXKWFcPS0.jpg)
======
**binary_relations_graph** – скрипт на Python для построения графа бинарных отношений

Необходимо задать список элементов elem и бинарные отношения между ними (**T(x, y)**).

Пример решения задачи квадратных сумм
======
***Расположить числа от 1 до 15 так, чтобы сумма соседних была равна квадратному числу.***
```python
...
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
...

```

Пример графа
------------
![граф бинарных отношений](https://pp.userapi.com/c849216/v849216684/95ff4/Mkj-hgCgaY8.jpg)


import networkx as nx

edges = [(1, 2), (1, 6), (2, 3), (2, 4), (2, 6),
         (3, 4), (3, 5), (4, 8), (4, 9), (6, 7)]

G.add_edges_from(edges)
nx.draw_networkx(G, with_label=True)
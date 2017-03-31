#!/usr/bin/env python
#coding=utf-8
import matplotlib.pyplot as plt
from operator import itemgetter
import networkx as nx

def labels_color():

    G=nx.cubical_graph()
    pos=nx.spring_layout(G) # positions for all nodes

    # nodes
    nx.draw_networkx_nodes(G,pos,
                           nodelist=[0,1,2,3],
                           node_color='r',
                           node_size=500,
                       alpha=0.8)
    nx.draw_networkx_nodes(G,pos,
                           nodelist=[4,5,6,7],
                           node_color='b',
                           node_size=500,
                       alpha=0.8)

    # edges
    nx.draw_networkx_edges(G,pos,width=1.0,alpha=0.5)
    nx.draw_networkx_edges(G,pos,
                           edgelist=[(0,1),(1,2),(2,3),(3,0)],
                           width=8,alpha=0.5,edge_color='r')
    nx.draw_networkx_edges(G,pos,
                           edgelist=[(4,5),(5,6),(6,7),(7,4)],
                           width=8,alpha=0.5,edge_color='b')


    # some math labels
    labels={}
    labels[0]=r'$a$'
    labels[1]=r'$b$'
    labels[2]=r'$c$'
    labels[3]=r'$d$'
    labels[4]=r'$\alpha$'
    labels[5]=r'$\beta$'
    labels[6]=r'$\gamma$'
    labels[7]=r'$\delta$'
    nx.draw_networkx_labels(G,pos,labels,font_size=16)

    plt.axis('off')
    #plt.savefig("labels_and_colors.png") # save as png
    plt.show() # display

def random_graph():
    G=nx.random_geometric_graph(200,0.125)
    # position is stored as node attribute data for random_geometric_graph
    pos=nx.get_node_attributes(G,'pos')

    # find node near center (0.5,0.5)
    dmin=1
    ncenter=0
    for n in pos:
        x,y=pos[n]
        d=(x-0.5)**2+(y-0.5)**2
        if d<dmin:
            ncenter=n
            dmin=d

    # color by path length from node near center
    p=nx.single_source_shortest_path_length(G,ncenter)

    plt.figure(figsize=(8,8))
    nx.draw_networkx_edges(G,pos,nodelist=[ncenter],alpha=0.4)
    nx.draw_networkx_nodes(G,pos,nodelist=p.keys(),
                           node_size=80,
                           node_color=p.values(),
                           cmap=plt.cm.Reds_r)

    plt.xlim(-0.05,1.05)
    plt.ylim(-0.05,1.05)
    plt.axis('off')
    #plt.savefig('random_geometric_graph.png')
    plt.show()

def colormap():
    G=nx.star_graph(20)
    pos=nx.spring_layout(G)
    colors=range(20)
    nx.draw(G,pos,node_color='#A0CBE2',edge_color=colors,width=4,edge_cmap=plt.cm.Blues,with_labels=False)
    #plt.savefig("edge_colormap.png") # save as png
    plt.show() # display

def weighted_graph():

    G=nx.Graph()

    G.add_edge(u'历史',u'地理',weight=0.6)
    G.add_edge(u'历史',u'科学',weight=0.2)
    G.add_edge(u'科学',u'自然',weight=0.1)
    G.add_edge(u'科学',u'宗教',weight=0.7)
    G.add_edge(u'科学',u'娱乐',weight=0.9)
    G.add_edge(u'历史',u'社会',weight=0.3)

    elarge=[(u,v) for (u,v,d) in G.edges(data=True) if d['weight'] >0.5]
    esmall=[(u,v) for (u,v,d) in G.edges(data=True) if d['weight'] <=0.5]

    pos=nx.spring_layout(G) # positions for all nodes

    # nodes
    nx.draw_networkx_nodes(G,pos,node_size=700)

    # edges
    nx.draw_networkx_edges(G,pos,edgelist=elarge,
                        width=6)
    nx.draw_networkx_edges(G,pos,edgelist=esmall,
                        width=6,alpha=0.5,edge_color='b',style='dashed')

    # labels
    nx.draw_networkx_labels(G,pos,font_size=15,font_family='sans-serif')

    plt.axis('off')
    # plt.savefig("weighted_graph.png") # save as png
    plt.show() # display

def ego_graph():
    # Create a BA model graph
    n=1000
    m=2
    G=nx.generators.barabasi_albert_graph(n,m)
    # find node with largest degree
    node_and_degree=G.degree()
    (largest_hub,degree)=sorted(node_and_degree.items(),key=itemgetter(1))[-1]
    # Create ego graph of main hub
    hub_ego=nx.ego_graph(G,largest_hub)
    # Draw graph
    pos=nx.spring_layout(hub_ego)
    nx.draw(hub_ego,pos,node_color='b',node_size=50,with_labels=False)
    # Draw ego as large and red
    nx.draw_networkx_nodes(hub_ego,pos,nodelist=[largest_hub],node_size=300,node_color='r')
    plt.savefig('ego_graph.png')
    plt.show()

if __name__ == '__main__':
    weighted_graph()


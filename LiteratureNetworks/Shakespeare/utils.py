import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Polygon
import matplotlib
import random

# import community as community

def create_conn_random_graph(nodes,p):
    while  True:
        # G=nx.connected_watts_strogatz_graph(25, 2, 0.8, tries=100)
        G=nx.erdos_renyi_graph(nodes,p)
        if nx.is_connected(G):
            break
    G.remove_nodes_from(nx.isolates(G))
    sstt="Erdos-Renyi Random Graph with %i nodes and probability %.02f" %(nodes,p)
    return G, sstt


def draw_network(G,sstt,withLabels=True,labfs=10,valpha=0.4,ealpha=0.4):

    pos=nx.spring_layout(G,scale=50)
    plt.figure(figsize=(12,12))
    nx.draw_networkx_nodes(G,pos=pos,with_labels=withLabels,alpha=valpha)
    if withLabels:
        labe=nx.draw_networkx_labels(G,pos=pos,font_size=labfs)
    nx.draw_networkx_edges(G,pos=pos,edge_color='b',alpha=ealpha)
    plt.title(sstt,fontsize=20)
    kk=plt.axis('off')
    return pos


def draw_centralities(G,centr,pos,withLabels=True,labfs=10,valpha=0.4,ealpha=0.4):

    plt.figure(figsize=(12,12))
    if centr=='degree_centrality':
        cent=nx.degree_centrality(G)
        sstt='Degree Centralities'
        ssttt='degree centrality'
    elif centr=='closeness_centrality':
        cent=nx.closeness_centrality(G)
        sstt='Closeness Centralities'
        ssttt='closeness centrality'
    elif centr=='betweenness_centrality':
        cent=nx.betweenness_centrality(G)
        sstt='Betweenness Centralities'
        ssttt='betweenness centrality'
    elif centr=='eigenvector_centrality':
        cent=nx.eigenvector_centrality(G,max_iter=1000)
        sstt='Eigenvector Centralities'
        ssttt='eigenvector centrality'
    elif centr=='page_rank':
        cent=nx.pagerank(G)
        sstt='PageRank'
        ssttt='pagerank'
    cs={}
    for k,v in cent.items():
        if v not in cs:
            cs[v]=[k]
        else:
            cs[v].append(k)
    for k in sorted(cs,reverse=True):
        for v in cs[k]:
            print 'Node %s has %s = %.4f' %(v,ssttt,k)

    if withLabels:
        labe=nx.draw_networkx_labels(G,pos=pos,font_size=labfs)
    nx.draw_networkx_nodes(G,pos=pos,nodelist=cent.keys(), #with_labels=withLabels,
                           node_size = [d*4000 for d in cent.values()],node_color=cent.values(),
                           cmap=plt.cm.Reds,alpha=valpha)
    
    nx.draw_networkx_edges(G,pos=pos,edge_color='b', alpha=ealpha)
    plt.title(sstt,fontsize=20)
    kk=plt.axis('off')

def draw_centralities_subplots(G,pos,withLabels=True,labfs=10,valpha=0.4,ealpha=0.4):
    centList=['degree_centrality','closeness_centrality','betweenness_centrality',
    'eigenvector_centrality','page_rank']
    cenLen=len(centList)
    plt.figure(figsize=(12,12))
    for uu,centr in enumerate(centList):
        if centr=='degree_centrality':
            cent=nx.degree_centrality(G)
            sstt='Degree Centralities'
            ssttt='degree centrality'
        elif centr=='closeness_centrality':
            cent=nx.closeness_centrality(G)
            sstt='Closeness Centralities'
            ssttt='closeness centrality'
        elif centr=='betweenness_centrality':
            cent=nx.betweenness_centrality(G)
            sstt='Betweenness Centralities'
            ssttt='betweenness centrality'
        elif centr=='eigenvector_centrality':
            cent=nx.eigenvector_centrality(G,max_iter=1000)
            sstt='Eigenvector Centralities'
            ssttt='eigenvector centrality'
        elif centr=='page_rank':
            cent=nx.pagerank(G)
            sstt='PageRank'
            ssttt='pagerank'
        cs={}
        for k,v in cent.items():
            if v not in cs:
                cs[v]=[k]
            else:
                cs[v].append(k)
        nodrank=[]
        uui=0
        for k in sorted(cs,reverse=True):
            for v in cs[k]:

                if uui<5:
                    nodrank.append(v)
                    uui+=1

        #         print 'Node %s has %s = %.4f' %(v,ssttt,k)
        nodeclo=[]
        for k,v in cent.items():
            if k in  nodrank :
                nodeclo.append(v)
            else:
                nodeclo.append(0.)
        plt.subplot(1+cenLen/2.,2,uu+1).set_title(sstt)
        if withLabels:
            labe=nx.draw_networkx_labels(G,pos=pos,font_size=labfs)
        
        # print uu,sstt
        nx.draw_networkx_nodes(G,pos=pos,nodelist=cent.keys(), #with_labels=withLabels,
                               # node_size = [d*4000 for d in cent.values()],
                               node_color=nodeclo,
                               cmap=plt.cm.Reds,alpha=valpha)
        
        nx.draw_networkx_edges(G,pos=pos,edge_color='b', alpha=ealpha)
        plt.title(sstt,fontsize=20)
        kk=plt.axis('off')
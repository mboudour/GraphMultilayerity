__author__ = "Moses A. Boudourides & Sergios T. Lenis"
__copyright__ = "Copyright (C) 2015 Moses A. Boudourides & Sergios T. Lenis"
__license__ = "Public Domain"
__version__ = "1.0"

'''
This script implements the construction of a 3-layer graph in the 2-path topology
by bridging 3 random graphs through 3 random bipartite graphs.
'''

import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms import bipartite
from matplotlib.patches import Ellipse, Polygon

def synthetic_three_level(n1,n2,n3,p1,p2,p3,q1,q2,q3,no_isolates=True):#,isolate_up=True,isolate_down=True):
    
    k=n1

    J=nx.erdos_renyi_graph(n1,p1) #The first layer graph
    Jis = nx.isolates(J)
    F=nx.erdos_renyi_graph(n2,p2) #The second layer graph
    Fis = nx.isolates(F)
    D=nx.erdos_renyi_graph(n3,p3) #The third layer graph
    Dis = nx.isolates(D)

    H1=nx.bipartite_gnmk_random_graph(n1,n2,int(n1*n2*q1)) #The bipartite graph that bridges layers 1 and 2
    H2=nx.bipartite_gnmk_random_graph(n2,n3,int(n2*n3*q2)) #The bipartite graph that bridges layers 2 and 3
    H3=nx.bipartite_gnmk_random_graph(n3,n1,int(n1*n3*q3)) #The bipartite graph that bridges layers 1 and 3
    
    G=nx.Graph()  #The synthetic two-layer graph
    
    # Relabing nodes maps

    mappingF={}
    for i in range(n3+n2):
        mappingF[i]=n1+i
    HH2=nx.relabel_nodes(H2,mappingF,copy=True)
    FF=nx.relabel_nodes(F,mappingF,copy=True)
    
    mappingD={}
    for i in range(n1+n3):
        if i >n3-1:
            mappingD[i]=i-n3
        else:
            mappingD[i]=n1+n2+i

    HH3=nx.relabel_nodes(H3,mappingD,copy=True)
    DD=nx.relabel_nodes(D,mappingD,copy=True)

    # Removing isolates

    if  no_isolates:
        J.remove_nodes_from(Jis) 
        H1.remove_nodes_from(Jis)
        HH3.remove_nodes_from(Jis)
        Fis = [mappingF[i] for i in Fis]
        FF.remove_nodes_from(Fis) 
        H1.remove_nodes_from(Fis)
        HH2.remove_nodes_from(Fis)
        Dis = [mappingD[i] for i in Dis]
        DD.remove_nodes_from(Dis) 
        HH2.remove_nodes_from(Dis)
        HH3.remove_nodes_from(Dis)

    G.add_edges_from(J.edges())
    G.add_edges_from(H1.edges())
    G.add_edges_from(DD.edges())
    G.add_edges_from(HH2.edges())
    G.add_edges_from(HH3.edges())
    G.add_edges_from(FF.edges())

    edgeList = []
    for e in H1.edges():
        edgeList.append(e)
    for e in HH2.edges():
        edgeList.append(e)
    for e in HH3.edges():
        edgeList.append(e)

    return G, J, FF, DD, edgeList

def plot_graph(G,J,FF,DD,n1,n2,n3,d1=0.8,d2=5.0,nodesize=1000,withlabels=True,edgelist=[],layout=True,b_alpha=0.5):
    '''
    Plotting the synthetic graph after increasing the distance among layers by a parameter d1
    and dilating each layer by a parameter d2 
    '''
    if layout:
        pos=nx.spring_layout(G)
    else:
        pos=nx.random_layout(G)

    top_set=set()
    bottom_set=set()
    middle_set=set()
    middle=[]
    level2=[]
    level1=[]
    for i in pos:

        npos=pos[i]
        if i < n1:
            pos[i]=[d2*(npos[0]),d2*(npos[1])] 
            top_set.add(i)
            level2.append(pos[i])
        elif i>=n1+n2:
            pos[i]=[d2*(npos[0]),d2*(npos[1]+d1)] 
            bottom_set.add(i)
            level1.append(pos[i])
        else:
            pos[i]=[d2*npos[0],d2*(npos[1]-d1)] 
            middle_set.add(i)
            middle.append(pos[i])
    
    xlevel1=[i[0] for i in level1]
    ylevel1=[i[1] for i in level1]

    alevel1 = [min(xlevel1)-d1/2.-0.7,max(ylevel1)+d1/2.]
    blevel1 = [max(xlevel1)+d1/2.-0.7,max(ylevel1)+d1/2.]
    clevel1 = [max(xlevel1)+d1/2.,min(ylevel1)-d1/2.]
    dlevel1 = [min(xlevel1)-d1/2.,min(ylevel1)-d1/2.]

    xlevel2=[i[0] for i in level2]
    ylevel2=[i[1] for i in level2]

    alevel2 = [min(xlevel2)-d1/2.-0.7,max(ylevel2)+d1/2.]
    blevel2 = [max(xlevel2)+d1/2.-0.7,max(ylevel2)+d1/2.]
    clevel2 = [max(xlevel2)+d1/2.,min(ylevel2)-d1/2.]
    dlevel2 = [min(xlevel2)-d1/2.,min(ylevel2)-d1/2.]

    xmiddle=[i[0] for i in middle]
    ymiddle=[i[1] for i in middle]

    amiddle = [min(xmiddle)-d1/2.-0.7,max(ymiddle)+d1/2.]
    bmiddle = [max(xmiddle)+d1/2.-0.7,max(ymiddle)+d1/2.]
    cmiddle = [max(xmiddle)+d1/2.,min(ymiddle)-d1/2.]
    dmiddle = [min(xmiddle)-d1/2.,min(ymiddle)-d1/2.]

    fig=plt.figure(figsize=(20,20))
    ax=fig.add_subplot(111)

    ax.add_patch(Polygon([alevel1,blevel1,clevel1,dlevel1],color='b',alpha=0.1)) #closed=True,fill=False))
    plt.plot([alevel1[0],blevel1[0],clevel1[0],dlevel1[0],alevel1[0]],[alevel1[1],blevel1[1],clevel1[1],dlevel1[1],alevel1[1]],'-b')

    ax.add_patch(Polygon([alevel2,blevel2,clevel2,dlevel2],color='r',alpha=0.1)) #closed=True,fill=False))
    plt.plot([alevel2[0],blevel2[0],clevel2[0],dlevel2[0],alevel2[0]],[alevel2[1],blevel2[1],clevel2[1],dlevel2[1],alevel2[1]],'-r')

    ax.add_patch(Polygon([amiddle,bmiddle,cmiddle,dmiddle],color='g',alpha=0.1)) #closed=True,fill=False))
    plt.plot([amiddle[0],bmiddle[0],cmiddle[0],dmiddle[0],amiddle[0]],[amiddle[1],bmiddle[1],cmiddle[1],dmiddle[1],amiddle[1]],'-g')

    nx.draw(J,pos, with_labels=withlabels,nodelist=list(top_set),node_color='r',node_size=nodesize,edge_color='r',alpha=0.2)
    nx.draw(FF,pos, with_labels=withlabels,nodelist=list(middle_set),node_color='g',node_size=nodesize,edge_color='g',alpha=0.2)
    nx.draw(DD,pos, with_labels=withlabels,nodelist=list(bottom_set),node_color='b',node_size=nodesize,edge_color='b',alpha=0.2)

    nx.draw_networkx_edges(G,pos,edgelist=edgelist,edge_color='k',alpha=b_alpha)

    plt.show()
    return pos

# q1=q2=q3=.1
# p1=p2=p3=.1
# n1=4
# n2=5
# n3=6
# G=synthetic_three_level(q1,q2,q3,p1,p2,p3,n1,n2,n3,J_isolates=False,F_isolates= False, D_isolates= False)
# # print G.nodes()
# # print nx.isolates(G)
# plot_graph(G,n1,n2,n3)
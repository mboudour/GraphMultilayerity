__author__ = "Moses A. Boudourides & Sergios T. Lenis"
__copyright__ = "Copyright (C) 2015 Moses A. Boudourides & Sergios T. Lenis"
__license__ = "Public Domain"
__version__ = "1.0"

'''
This script implements the construction of a 3-layer graph in the triangular topology
by bridging 3 random graphs through 3 random bipartite graphs.
'''

import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms import bipartite
from matplotlib.patches import Ellipse, Polygon

def synthetic_three_level(n1,n2,n3,p1,p2,p3,q1,q2,q3,no_isolates=True):

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

def plot_graph(G,J,FF,DD,n1,n2,n3,d1=0.8,d2=3.,d3=0.8,nodesize=1000,withlabels=True,edgelist=[],layout=True,b_alpha=0.5):
    '''
    Plotting the synthetic graph after increasing the distance among layers by a parameter d1
    and dilating each layer by a parameter d2 
    '''

    if layout:
        pos=nx.spring_layout(G)
    else:
        pos=nx.random_layout(G)
        # pos =nx.circular_layout(G)
    
    top_set=set()
    bottom_set=set()
    middle_set=set()
    down=[]
    right=[]
    left=[]
    for i in pos:
        npos=pos[i]
        if i < n1:
            pos[i]=[d2*(npos[0]-d1),d2*(npos[1]+d1)] 
            top_set.add(i)
            left.append(pos[i])
        elif i>=n1+n2:
            pos[i]=[d2*(npos[0]+d1),d2*(npos[1]+d1)] 
            bottom_set.add(i)
            right.append(pos[i])
        else:
            pos[i]=[d2*npos[0],d2*(npos[1]-d1)] 
            middle_set.add(i)
            down.append(pos[i])
    
    xleft=[i[0] for i in left]
    yleft=[i[1] for i in left]

    aleft = [min(xleft)-d1/2.,max(yleft)+d1/2.+d3]
    bleft = [max(xleft)+d1/2.,max(yleft)+d1/2.+3*d3]
    cleft = [max(xleft)+d1/2.,min(yleft)-d1/2.-3*d3]
    dleft = [min(xleft)-d1/2.,min(yleft)-d1/2.-d3]

    xright=[i[0] for i in right]
    yright=[i[1] for i in right]

    aright = [min(xright)-d1/2.,max(yright)+d1/2.+d3]
    bright = [max(xright)+d1/2.,max(yright)+d1/2.+3*d3]
    cright = [max(xright)+d1/2.,min(yright)-d1/2.-3*d3]
    dright = [min(xright)-d1/2.,min(yright)-d1/2.-d3]

    xdown=[i[0] for i in down]
    ydown=[i[1] for i in down]

    adown = [min(xdown)-d1/2.,max(ydown)+d1/2.+d3]
    bdown = [max(xdown)+d1/2.,max(ydown)+d1/2.+3*d3]
    cdown = [max(xdown)+d1/2.,min(ydown)-d1/2.-3*d3]
    ddown = [min(xdown)-d1/2.,min(ydown)-d1/2.-d3]

    fig=plt.figure(figsize=(20,20))
    ax=fig.add_subplot(111)

    ax.add_patch(Polygon([aleft,bleft,cleft,dleft],color='r',alpha=0.1)) 
    plt.plot([aleft[0],bleft[0],cleft[0],dleft[0],aleft[0]],[aleft[1],bleft[1],cleft[1],dleft[1],aleft[1]],'-r')

    ax.add_patch(Polygon([aright,bright,cright,dright],color='b',alpha=0.1)) 
    plt.plot([aright[0],bright[0],cright[0],dright[0],aright[0]],[aright[1],bright[1],cright[1],dright[1],aright[1]],'-b')

    ax.add_patch(Polygon([adown,bdown,cdown,ddown],color='g',alpha=0.1)) 
    plt.plot([adown[0],bdown[0],cdown[0],ddown[0],adown[0]],[adown[1],bdown[1],cdown[1],ddown[1],adown[1]],'-g')

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
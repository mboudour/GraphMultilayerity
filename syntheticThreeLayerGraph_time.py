__author__ = "Moses A. Boudourides & Sergios T. Lenis"
__copyright__ = "Copyright (C) 2015 Moses A. Boudourides & Sergios T. Lenis"
__license__ = "Public Domain"
__version__ = "1.0"

'''
This script constructs a temporal random graph with 3 time slices.
'''

import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms import bipartite
from matplotlib.patches import Ellipse, Polygon

def synthetic_three_level(n,p1,p2,p3,J_isolates=False,F_isolates=False,D_isolates=False):#,isolate_up=True,isolate_down=True):
    
    k=n

    J=nx.erdos_renyi_graph(n,p1) #The first layer graph
    Jis = nx.isolates(J)
    F=nx.erdos_renyi_graph(n,p2) #The second layer graph
    Fis = nx.isolates(F)
    D=nx.erdos_renyi_graph(n,p3) #The third layer graph
    Dis = nx.isolates(D)

    def translation_graph(J,F,D):
        H1=nx.Graph()
        H2=nx.Graph()
        for i in range(n):
            H1.add_edges_from([(J.nodes()[i],F.nodes()[i])])
            H2.add_edges_from([(F.nodes()[i],D.nodes()[i])])
        return H1, H2

    Jed = set(J.edges())
    Fed = set(F.edges())
    Ded = set(D.edges())
    l=[Jed,Fed,Ded]
    lu = list(set.union(*l))
    JFD=nx.Graph()
    JFD.add_edges_from(lu)

    G=nx.Graph()  #The synthetic two-layer graph
    
    # Relabing nodes maps
    
    mappingF={}
    for i in range(2*n):
        mappingF[i]=n+i
    FF=nx.relabel_nodes(F,mappingF,copy=True)
    
    mappingD={}
    for i in range(2*n):
        if i >n-1:
            mappingD[i]=i-n
        else:
            mappingD[i]=2*n+i
    DD=nx.relabel_nodes(D,mappingD,copy=True)
    
    H1, HH2 = translation_graph(J,FF,DD)
    
    G.add_edges_from(J.edges())
    G.add_edges_from(H1.edges())
    G.add_edges_from(DD.edges())
    G.add_edges_from(HH2.edges())
    G.add_edges_from(FF.edges())

    edgeList = []
    for e in H1.edges():
        edgeList.append(e)
    for e in HH2.edges():
        edgeList.append(e)
    
    return G, J, FF, DD, JFD, edgeList  


def plot_graph(n,G,J,FF,DD,JFD,d1=0.8,d2=5.0,nodesize=1000,withlabels=True,edgelist=[],layout=True,b_alpha=0.5):  
    
    if layout:
        pos=nx.spring_layout(JFD)
    else:
        pos=nx.random_layout(JFD)
        # pos =nx.circular_layout(JFD)

    minPos=min(pos.keys())
    
    top_set=set()
    bottom_set=set()
    middle_set=set()
    level1=[]
    level2=[]
    level3=[]
    created_pos={}
    for j in range(3):
        for i in range(len(pos)):
            npos=pos[pos.keys()[i]]
            if j==0:
                ij=i
                created_pos[ij]=[d2*npos[0],d2*(npos[1]-d1)] 
                bottom_set.add(i)
                level3.append(created_pos[i])
            elif j==1:
                ij=i+n
                created_pos[ij]=[d2*(npos[0]),d2*(npos[1])] 
                middle_set.add(ij)
                level1.append(created_pos[ij])
            else:
                ij=i+2*n                
                created_pos[ij]=[d2*(npos[0]),d2*(npos[1]+d1)] 
                top_set.add(ij)
                level2.append(created_pos[ij])
    
    xlevel2=[i[0] for i in level2]
    ylevel2=[i[1] for i in level2]
    
    alevel2 = [min(xlevel2)-d1/2.-0.7,max(ylevel2)+d1/2.]
    blevel2 = [max(xlevel2)+d1/2.-0.7,max(ylevel2)+d1/2.]
    clevel2 = [max(xlevel2)+d1/2.,min(ylevel2)-d1/2.]
    dlevel2 = [min(xlevel2)-d1/2.,min(ylevel2)-d1/2.]

    xlevel3=[i[0] for i in level3]
    ylevel3=[i[1] for i in level3]

    alevel3 = [min(xlevel3)-d1/2.-0.7,max(ylevel3)+d1/2.]
    blevel3 = [max(xlevel3)+d1/2.-0.7,max(ylevel3)+d1/2.]
    clevel3 = [max(xlevel3)+d1/2.,min(ylevel3)-d1/2.]
    dlevel3 = [min(xlevel3)-d1/2.,min(ylevel3)-d1/2.]

    xlevel1=[i[0] for i in level1]
    ylevel1=[i[1] for i in level1]

    alevel1 = [min(xlevel1)-d1/2.-0.7,max(ylevel1)+d1/2.]
    blevel1 = [max(xlevel1)+d1/2.-0.7,max(ylevel1)+d1/2.]
    clevel1 = [max(xlevel1)+d1/2.,min(ylevel1)-d1/2.]
    dlevel1 = [min(xlevel1)-d1/2.,min(ylevel1)-d1/2.]

    fig=plt.figure(figsize=(20,20))
    ax=fig.add_subplot(111)

    ax.add_patch(Polygon([alevel2,blevel2,clevel2,dlevel2],color='b',alpha=0.1)) 
    plt.plot([alevel2[0],blevel2[0],clevel2[0],dlevel2[0],alevel2[0]],[alevel2[1],blevel2[1],clevel2[1],dlevel2[1],alevel2[1]],'-b')

    ax.add_patch(Polygon([alevel3,blevel3,clevel3,dlevel3],color='r',alpha=0.1)) 
    plt.plot([alevel3[0],blevel3[0],clevel3[0],dlevel3[0],alevel3[0]],[alevel3[1],blevel3[1],clevel3[1],dlevel3[1],alevel3[1]],'-r')

    ax.add_patch(Polygon([alevel1,blevel1,clevel1,dlevel1],color='g',alpha=0.1)) 
    plt.plot([alevel1[0],blevel1[0],clevel1[0],dlevel1[0],alevel1[0]],[alevel1[1],blevel1[1],clevel1[1],dlevel1[1],alevel1[1]],'-g')

    nx.draw(J,created_pos, with_labels=withlabels,nodelist=list(bottom_set),node_color='r',node_size=nodesize,edge_color='r',alpha=0.2)
    nx.draw(FF,created_pos, with_labels=withlabels,nodelist=list(middle_set),node_color='g',node_size=nodesize,edge_color='g',alpha=0.2)
    nx.draw(DD,created_pos, with_labels=withlabels,nodelist=list(top_set),node_color='b',node_size=nodesize,edge_color='b',alpha=0.2)
    nx.draw_networkx_edges(G,created_pos,edgelist=edgelist,edge_color='k',alpha=0.2)

    plt.show()

    return created_pos

# p1=p2=p3=0.1
# n=500
# G,J,FF,DD,JFD,edgeList = synthetic_three_level(n,p1,p2,p3,J_isolates=False,F_isolates= False, D_isolates= False)
# # print JFD.nodes()
# # print JFD.edges()
# # print F.nodes()
# # print F.edges()
# # print G.nodes()
# # print edgeList
# # print aaaa
# # print nx.isolates(G)
# # plot_graph(n,G,J,FF,DD,F,d1=2.,d2=3.,nodesize=100,withlabels=False,edgelist=edgeList,layout=True,b_alpha=0.5)
# plot_graph(n,G,J,FF,DD,JFD,d1=2.,d2=3.,nodesize=50,withlabels=False,edgelist=edgeList,layout=False,b_alpha=0.15)
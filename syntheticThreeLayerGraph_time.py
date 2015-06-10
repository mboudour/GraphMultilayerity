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
import matplotlib

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
def synthetic_multi_level(k,n,p=[],No_isolates=True):#,p2=[],p3=[],J_isolates=False,F_isolates=False,D_isolates=False):#,isolate_up=True,isolate_down=True):
    # print k,n,p
    # k=ng
    list_of_Graphs=[]
    list_of_isolates=[]
    list_of_Graphs_final=[]
    for ij in range(k):
        list_of_Graphs.append(nx.erdos_renyi_graph(n,p[ij]))
        list_of_isolates.append(nx.isolates(list_of_Graphs[ij]))
    # J=nx.erdos_renyi_graph(n,p1) #The first layer graph
    # Jis = nx.isolates(J)
    # F=nx.erdos_renyi_graph(n,p2) #The second layer graph
    # Fis = nx.isolates(F)
    # D=nx.erdos_renyi_graph(n,p3) #The third layer graph
    # Dis = nx.isolates(D)
    
    # def translation_graph(J,F,D):
    #     H1=nx.Graph()
    #     H2=nx.Graph()
    #     for i in range(n):
    #         H1.add_edges_from([(J.nodes()[i],F.nodes()[i])])
    #         H2.add_edges_from([(F.nodes()[i],D.nodes()[i])])
    #     return H1, H2
    # lu=set()
    Gagr=nx.Graph()
    for i in list_of_Graphs:
        Gagr.add_edges_from(i.edges())
        Gagr.add_nodes_from(i.nodes())
    # for i in range(n):

        # lu=lu.union(set(i.edges()))
    # lu=list(lu)
    #     Jed = set(J.edges())
    # Fed = set(F.edges())
    # Ded = set(D.edges())
    # l=[Jed,Fed,Ded]
    # lu = list(set.union(*l))
    # Gagr=nx.Graph()
    # Gagr.add_edges_from(lu)

    G=nx.Graph()  #The synthetic two-layer graph
    
    # Relabing nodes maps
    
    
    for i in range(k):
        # print i
        # ngn=nx.Graph()
        mapping={}
        # mapping[i]=
        for ij in range(n):
            mapping[ij]=ij+i*n
        #     print i,ij, mapping
        # print i,mapping,'kkk'
        # for ed in list_of_Graphs[i].edges():
        #     ngn.add_edge(mapping[ed[0]],mapping[ed[1]])
        # for nd in list_of_Graphs[i].nodes():
        #     ngn.add_node(mapping[nd])
        # print list_of_Graphs[i].nodes()
        # print list_of_Graphs[i].edges()
        list_of_Graphs_final.append(nx.relabel_nodes(list_of_Graphs[i],mapping,copy=True))
    #     list_of_Graphs_final.append(ngn)
    #     print list_of_Graphs_final[i].nodes()
    #     print list_of_Graphs_final[i].edges()
    #     print 'kkkkkkkkkkkkkk'
    # print aaaa
    # print mapping
    # for kk in list_of_Graphs_final:
    #     print kk.nodes()
    # print aaaaaa
    # list_of_Graphs_final=[nx.relabel_nodes(i,mapping,copy=True) for i in list_of_Graphs]
    # for i in range(k):
    #     print list_of_Graphs_final[i].nodes()
    list_of_translation_graphs=[]
    for ij in range(k-1):
        H1=nx.Graph()
        # H2=nx.Graph()
        for ji in range(n):
            # print ij,ji,ij+1
            # print list_of_Graphs_final[ij].nodes()[ji],list_of_Graphs_final[ij+1].nodes()[ji]
            # print ij,ji
            # print [list_of_Graphs_final[ij].nodes(),list_of_Graphs_final[ij+1].nodes()]
            # print [list_of_Graphs_final[ij].nodes()[ji],list_of_Graphs_final[ij+1].nodes()[ji]]
            H1.add_edge(list_of_Graphs_final[ij].nodes()[ji],list_of_Graphs_final[ij+1].nodes()[ji])
        list_of_translation_graphs.append(H1)
    # print aaaaa
    luf=set()
    for i in list_of_Graphs_final:
        luf=luf.union(set(i.edges()))
    luf=list(luf)
    G.add_edges_from(luf)
    luf=set()
    for i in list_of_translation_graphs:
        luf=luf.union(set(i.edges()))
    edgeList=list(luf)
    G.add_edges_from(luf)
    # for i in range(2*n):
    #     mappingF[i]=n+i
    # FF=nx.relabel_nodes(F,mappingF,copy=True)
    
    # mappingD={}
    # for i in range(2*n):
    #     if i >n-1:
    #         mappingD[i]=i-n
    #     else:
    #         mappingD[i]=2*n+i
    # DD=nx.relabel_nodes(D,mappingD,copy=True)
    
    # H1, HH2 = translation_graph(J,FF,DD)
    
    # if  J_isolates:
    #     J.remove_nodes_from(Jis) 
    #     H1.remove_nodes_from(Jis)
    # if  F_isolates:
    #     Fis = [mappingF[i] for i in Fis]
    #     FF.remove_nodes_from(Fis) 
    #     H1.remove_nodes_from(Fis)
    #     HH2.remove_nodes_from(Fis)
    # if  D_isolates:
    #     Dis = [mappingD[i] for i in Dis]
    #     DD.remove_nodes_from(Dis) 
    #     HH2.remove_nodes_from(Dis)

    # G.add_edges_from(J.edges())
    # G.add_edges_from(H1.edges())
    # G.add_edges_from(DD.edges())
    # G.add_edges_from(HH2.edges())
    # G.add_edges_from(FF.edges())

    # edgeList = []
    # for e in H1.edges():
    #     edgeList.append(e)
    # for e in HH2.edges():
    #     edgeList.append(e)
    
    return G, list_of_Graphs_final, Gagr, edgeList  #F


# k,n,G, list_of_Graphs_final, Gagr, luf
def plot_graph_k(k,n,G,list_of_Graphs_final, Gagr,d1=0.8,d2=5.0,nodesize=1000,withlabels=True,edgelist=[],layout=True,b_alpha=0.5):  
    '''
    Plotting the synthetic graph after increasing the distance among layers by a parameter d1
    and dilating each layer by a parameter d1 
    '''
    # print k,n,'st'
    if layout:
        pos=nx.spring_layout(Gagr)
    else:
        pos=nx.random_layout(Gagr)
        # pos =nx.circular_layout(Gagr)

    minPos=min(pos.keys())
    # print pos
    top_set=set()
    bottom_set=set()
    middle_set=set()
    levels=dict()
    # level1=[]
    # level2=[]
    # level3=[]
    created_pos={}
    colors=[name for name,hex in matplotlib.colors.cnames.iteritems()]
    for j in range(k):
        # created_pos={}
        sset=set()
        pos_lis=[]
        for i in range(n):
            ij=i+j*n
            # print i,j,ij
            npos=pos[i]
            # print npos
    # print aaa

        #     # if j not in levels:
        #     #     levels[j]=[set(),[],None]
        #     # if j==0:
        #         # ij=i
            # print d2*(npos[1]+j*n*d1),j*n*d1,j,n,d1,npos[1]
            created_pos[ij]=[d2*npos[0],d2*(npos[1]+j*n*d1)] 
            sset.add(ij)
            pos_lis.append(created_pos[ij])
            col_li=colors[j]
            # print created_pos[ij]
            # print aaa
        levels[j]=(sset,pos_lis,col_li)
            # bottom_set.add(i)
            # level3.append(created_pos[i])
            # elif j==1:
            #     ij=i+n
            #     created_pos[ij]=[d2*(npos[0]),d2*(npos[1])] 
            #     middle_set.add(ij)
            #     level1.append(created_pos[ij])
            # else:
            #     ij=i+2*n                
            #     created_pos[ij]=[d2*(npos[0]),d2*(npos[1]+d1)] 
            #     top_set.add(ij)
            #     level2.append(created_pos[ij])
    xylevels={}
    # for i in levels[1][1]:
    #     print i
    # print aaaa
    # print levels[1][1]
    # print len(levels[1][1])
    # print levels[0][1]
    # print aaaaa
    for i in range(k):
        # if i not in xylevels:
            # xylevels=
        # ssle=[ij for ij in levels[i]]
        # print ssle
        # print levels[i]
        # print levels[i]
        xlevel2=[ij[0] for ij in levels[i][1]]
        # print xlevel2
        # print levels[i][1]
        # print levels[i][2]

        # for ij in levels[i]:
        #     print ij
        #     print ij[1]
        #     for kij in ij:
        #         print ij,'ddddddd'
        # print aaa
        # ssle=[ij[1][1] for ij in levels[i]]
        # print ssle
        ylevel2=[ij[1] for ij in levels[i][1]]
        # print ylevel2
        # print aaaa
        alevel2 = [min(xlevel2)-d1/2.-0.7,max(ylevel2)+d1/2.]
        blevel2 = [max(xlevel2)+d1/2.-0.7,max(ylevel2)+d1/2.]
        clevel2 = [max(xlevel2)+d1/2.,min(ylevel2)-d1/2.]
        dlevel2 = [min(xlevel2)-d1/2.,min(ylevel2)-d1/2.]
        xylevels[i]=[alevel2,blevel2,clevel2,dlevel2]

    # xlevel3=[i[0] for i in level3]
    # ylevel3=[i[1] for i in level3]

    # alevel3 = [min(xlevel3)-d1/2.-0.7,max(ylevel3)+d1/2.]
    # blevel3 = [max(xlevel3)+d1/2.-0.7,max(ylevel3)+d1/2.]
    # clevel3 = [max(xlevel3)+d1/2.,min(ylevel3)-d1/2.]
    # dlevel3 = [min(xlevel3)-d1/2.,min(ylevel3)-d1/2.]

    # xlevel1=[i[0] for i in level1]
    # ylevel1=[i[1] for i in level1]

    # alevel1 = [min(xlevel1)-d1/2.-0.7,max(ylevel1)+d1/2.]
    # blevel1 = [max(xlevel1)+d1/2.-0.7,max(ylevel1)+d1/2.]
    # clevel1 = [max(xlevel1)+d1/2.,min(ylevel1)-d1/2.]
    # dlevel1 = [min(xlevel1)-d1/2.,min(ylevel1)-d1/2.]

    fig=plt.figure()#figsize=(20,20))
    ax=fig.add_subplot(111)
    for i in range(k):
        # print xylevels[i]
        # print xylevels[i][0][0], type(xylevels[i][0][0])

        # print aaa
        ax.add_patch(Polygon(xylevels[i],color=levels[i][2],alpha=0.1))

        xa=[j[0] for j in xylevels[i]]
        # print xa
        # print xylevels[i][0][0]#, type(xylevels[i][0][0])
        xa.append(xylevels[i][0][0])
        ya=[j[1] for j in xylevels[i]]
        ya.append(xylevels[i][0][1])
        plt.plot(xa,ya,'-',color=levels[i][2])

    # ax.add_patch(Polygon([alevel2,blevel2,clevel2,dlevel2],color='b',alpha=0.1)) 
    # plt.plot([alevel2[0],blevel2[0],clevel2[0],dlevel2[0],alevel2[0]],[alevel2[1],blevel2[1],clevel2[1],dlevel2[1],alevel2[1]],'-b')

    # ax.add_patch(Polygon([alevel3,blevel3,clevel3,dlevel3],color='r',alpha=0.1)) 
    # plt.plot([alevel3[0],blevel3[0],clevel3[0],dlevel3[0],alevel3[0]],[alevel3[1],blevel3[1],clevel3[1],dlevel3[1],alevel3[1]],'-r')

    # ax.add_patch(Polygon([alevel1,blevel1,clevel1,dlevel1],color='g',alpha=0.1)) 
    # plt.plot([alevel1[0],blevel1[0],clevel1[0],dlevel1[0],alevel1[0]],[alevel1[1],blevel1[1],clevel1[1],dlevel1[1],alevel1[1]],'-g')
        nx.draw(list_of_Graphs_final[i],created_pos,with_labels=withlabels,nodelist=list(levels[i][0]),node_color=levels[i][2],node_size=nodesize,edge_color=levels[i][2],alpha=0.2)
    # nx.draw(J,created_pos, with_labels=withlabels,nodelist=list(bottom_set),node_color='r',node_size=nodesize,edge_color='r',alpha=0.2)
    # nx.draw(FF,created_pos, with_labels=withlabels,nodelist=list(middle_set),node_color='g',node_size=nodesize,edge_color='g',alpha=0.2)
    # nx.draw(DD,created_pos, with_labels=withlabels,nodelist=list(top_set),node_color='b',node_size=nodesize,edge_color='b',alpha=0.2)
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
# k=5
# n=10
# pp=[0.1,.1,.1,.1,.4]
# G, list_of_Graphs_final, Gagr, edgeList=synthetic_multi_level(k,n,p=pp,No_isolates=True)
# plot_graph_k(k,n,G, list_of_Graphs_final, Gagr, edgelist=edgeList)
#             # k,n,G,list_of_Graphs_final, Gagr,d1
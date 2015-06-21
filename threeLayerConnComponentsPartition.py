__author__ = "Moses A. Boudourides & Sergios T. Lenis"
__copyright__ = "Copyright (C) 2015 Moses A. Boudourides & Sergios T. Lenis"
__license__ = "Public Domain"
__version__ = "1.0"

'''
This script finds the connected components of a 3-layer graph.
'''

import community as cm
import networkx as nx
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Polygon
import random
from collections import Counter
import numpy as np
np.seterr(divide='ignore', invalid='ignore')

def analyticThreeLayerGraph(n,p,r1,r2,r3,G_isolates=True):

    G=nx.erdos_renyi_graph(n,p)

    if  G_isolates:
        G.remove_nodes_from(nx.isolates(G))

    layer1 = random.sample(G.nodes(),int(len(G.nodes())*r1))
    layer2 = random.sample(set(G.nodes())-set(layer1),int(len(G.nodes())*r2))
    layer3 = list(set(G.nodes())-set(layer1)-set(layer2))

    edgeList =[]
    for e in G.edges():
        if (e[0] in layer1 and e[1] in layer2) or (e[0] in layer2 and e[1] in layer1):
            edgeList.append(e)
        if (e[0] in layer2 and e[1] in layer3) or (e[0] in layer3 and e[1] in layer2):
            edgeList.append(e)
        if (e[0] in layer3 and e[1] in layer1) or (e[0] in layer1 and e[1] in layer3):
            edgeList.append(e)

    return G, layer1, layer2, layer3, edgeList


def create_node_conncomp_graph(G,layer1,layer2,layer3):
    
    npartition = list(nx.connected_components(G))
    layers={'layer1':layer1,'layer2':layer2,'layer3':layer3}
    broken_partition={}
    for i,v in enumerate(npartition):
        vs=set(v)
        for ii,vv in layers.items():
            papa=vs.intersection(set(vv))
            if len(papa)==len(v):
                broken_partition['a_%i_%s_s' %(i,ii)]=v
            elif len(papa)>0:
                broken_partition['b_%i_%s' %(i,ii)]=list(papa)
                vs=vs-set(vv)
    broken_graph=nx.Graph()
    rbroken_partition=dict()
    colors=[name for name,hex in matplotlib.colors.cnames.iteritems()]
    colors=list(set(colors)-set(['red','blue','green']))
    cl=dict()
    for i,v in broken_partition.items():
        name=i.split('_')
        for ii in v:
            rbroken_partition[ii]=i
        if name[-1]=='s':
            cl[name[1]]=colors.pop()
        elif name[0]=='b' and not cl.has_key(name[1]):
            cl[name[1]]=colors.pop()
    for i,v in rbroken_partition.items():
        name=v.split('_')
        broken_graph.add_node(v,color=cl[name[1]])
        edg=G[i]
        for j in edg:
            if j not in broken_partition[v]:
                if not broken_graph.has_edge(v,rbroken_partition[j]):
                    broken_graph.add_edge(v,rbroken_partition[j])
    
    return broken_graph,broken_partition,npartition


def plot_graph_stack(G,broken_graph,broken_partition,npartition,layer1,layer2,layer3,d1=1.5,d2=5.,d3=0,d4=.8,nodesize=1000,withlabels=True,edgelist=[],layout=True,alpha=0.5):
    
    if layout:
        pos=nx.spring_layout(G)
    else:
        pos=nx.random_layout(G)

    top_set=set()
    bottom_set=set()
    middle_set=set()
    down=[]
    right=[]
    left=[]

    mlayer_part={}
    for i in broken_partition:
        ii=i.split('_')
        if ii[1] not in mlayer_part:
            mlayer_part[ii[1]]=set([ii[2]])
        else:
            mlayer_part[ii[1]].add(ii[2])
    layers_m=Counter()
    for k,v in mlayer_part.items():
        if len(v)==1:
            layers_m[1]+=1
        elif len(v)==2:
            layers_m[2]+=1
        elif len(v)==3:
            layers_m[3]+=1
        else:
            print k,v

    broken_pos={}
    mlayer_part={}
    for i in broken_partition:
        # print i.split('_')
        ii=i.split('_')
        if ii[1] not in mlayer_part:
            mlayer_part[ii[1]]=set([ii[2]])
        else:
            mlayer_part[ii[1]].add(ii[2])

    layers_m=Counter()
    for k,v in mlayer_part.items():
        if len(v)==1:
            layers_m[1]+=1
        elif len(v)==2:
            layers_m[2]+=1
        elif len(v)==3:
            layers_m[3]+=1
        else:
            print k,v
    singles=0
    for i,v in broken_partition.items():       
        name=i.split('_')
        if name[-1]=='s':
            singles+=1
        ndnd=random.choice(v)
        npos=pos[ndnd]
        if ndnd in layer1:
            broken_pos[i]=[d2*(npos[0]),d2*(npos[1]+d1)] 
            top_set.add(i)
            left.append(broken_pos[i])
        elif ndnd in layer2:
            broken_pos[i]=[d2*(npos[0]),d2*(npos[1]-d1)] 
            bottom_set.add(i)
            right.append(broken_pos[i])
        else:
            broken_pos[i]=[d2*npos[0],d2*(npos[1])] 
            middle_set.add(i)
            down.append(broken_pos[i])
    
    xleft=[i[0] for i in left]
    yleft=[i[1] for i in left]

    aleft = [min(xleft)-d1/2.,max(yleft)+d1/2.-d3]
    bleft = [max(xleft)+d1/2.,max(yleft)+d1/2.+d3]
    cleft = [max(xleft)+d1/2.-d4,min(yleft)-d1/2.+d3]
    dleft = [min(xleft)-d1/2.-d4,min(yleft)-d1/2.-d3]

    xright=[i[0] for i in right]
    yright=[i[1] for i in right]

    aright = [min(xright)-d1/2.,max(yright)+d1/2.-d3]
    bright = [max(xright)+d1/2.,max(yright)+d1/2.+d3]
    cright = [max(xright)+d1/2.-d4,min(yright)-d1/2.+d3]
    dright = [min(xright)-d1/2.-d4,min(yright)-d1/2.-d3]

    xdown=[i[0] for i in down]
    ydown=[i[1] for i in down]

    adown = [min(xdown)-d1/2.,max(ydown)+d1/2.-d3]
    bdown = [max(xdown)+d1/2.,max(ydown)+d1/2.+d3]
    cdown = [max(xdown)+d1/2.-d4,min(ydown)-d1/2.+d3]
    ddown = [min(xdown)-d1/2.-d4,min(ydown)-d1/2.-d3]

    fig=plt.figure(figsize=(20,20))
    ax=fig.add_subplot(111)

    ax.add_patch(Polygon([aleft,bleft,cleft,dleft],color='r',alpha=0.1)) 
    plt.plot([aleft[0],bleft[0],cleft[0],dleft[0],aleft[0]],[aleft[1],bleft[1],cleft[1],dleft[1],aleft[1]],'-r')

    ax.add_patch(Polygon([aright,bright,cright,dright],color='b',alpha=0.1)) 
    plt.plot([aright[0],bright[0],cright[0],dright[0],aright[0]],[aright[1],bright[1],cright[1],dright[1],aright[1]],'-b')

    ax.add_patch(Polygon([adown,bdown,cdown,ddown],color='g',alpha=0.1)) 
    plt.plot([adown[0],bdown[0],cdown[0],ddown[0],adown[0]],[adown[1],bdown[1],cdown[1],ddown[1],adown[1]],'-g')
   
    nodeSize=[nodesize*len(broken_partition[i]) for i in list(top_set)]
    nodeColor=[broken_graph.node[i]['color'] for i in list(top_set) ]
    
    nx.draw_networkx_nodes(broken_graph,broken_pos, nodelist=list(top_set),node_shape='s',node_color=nodeColor,alpha=1,node_size=nodeSize)
    nodeSize=[nodesize*len(broken_partition[i]) for i in list(middle_set)]
    nodeColor=[broken_graph.node[i]['color'] for i in list(middle_set) ]
    
    nx.draw_networkx_nodes(broken_graph,broken_pos, nodelist=list(middle_set),node_shape='s',node_color=nodeColor,alpha=1,node_size=nodeSize)
    nodeSize=[nodesize*len(broken_partition[i]) for i in list(bottom_set)]
    nodeColor=[broken_graph.node[i]['color'] for i in list(bottom_set) ]

    nx.draw_networkx_nodes(broken_graph,broken_pos,nodelist=list(bottom_set),node_shape='s',node_color=nodeColor,alpha=1,node_size=nodeSize)
    
    if withlabels:
        nx.draw_networkx_labels(G,pos)

    lay1_edges=[ed for ed in G.edges() if ed[0] in layer1 and ed[1] in layer1]
    lay2_edges=[ed for ed in G.edges() if ed[0] in layer2 and ed[1] in layer2]
    lay3_edges=[ed for ed in G.edges() if ed[0] in layer3 and ed[1] in layer3]
    
    nx.draw_networkx_edges(broken_graph,broken_pos,alpha=0.3)
    for i,v in broken_partition.items():
        for nd in v:
            atrr=G.node[nd]
            G.add_node(nd,attr_dict=atrr,asso=i)
    # print G.nodes(data=True)
    rr=nx.attribute_assortativity_coefficient(G,'asso')
    # print 'Attribute assortativity coefficient wrt layer partition (old)= %f' %orr
    title_s='%i connected components (%i 3-layered, %i 2-layered, %i 1-layered)\n Discrete assortativity coefficient of the joint partition for connected_components and 3 layers = %f ' %(len(npartition),layers_m[3],layers_m[2],layers_m[1],rr)

    # title_s='%i connected components (%i 3-layered, %i 2-layered, %i 1-layered)' %(len(npartition),layers_m[3],layers_m[2],layers_m[1])  #  %(len(npartition),len(npartition)-singles,singles)
    plt.title(title_s,{'size': '20'})
    
    plt.axis('off')
    plt.show()
    

def plot_graph(G,broken_graph,broken_partition,npartition,layer1,layer2,layer3,d1=1.5,d2=5.,d3=0,d4=.8,nodesize=1000,withlabels=True,edgelist=[],layout=True,alpha=0.5):
    
    if layout:
        pos=nx.spring_layout(G)
    else:
        pos=nx.random_layout(G)

    top_set=set()
    bottom_set=set()
    middle_set=set()
    down=[]
    right=[]
    left=[]

    mlayer_part={}
    for i in broken_partition:
        ii=i.split('_')
        if ii[1] not in mlayer_part:
            mlayer_part[ii[1]]=set([ii[2]])
        else:
            mlayer_part[ii[1]].add(ii[2])

    layers_m=Counter()
    for k,v in mlayer_part.items():
        if len(v)==1:
            layers_m[1]+=1
        elif len(v)==2:
            layers_m[2]+=1
        elif len(v)==3:
            layers_m[3]+=1
        else:
            print k,v

    broken_pos={}
    singles=0
    for i,v in broken_partition.items():       
        name=i.split('_')
        if name[-1]=='s':
            singles+=1
        ndnd=random.choice(v)
        npos=pos[ndnd]
        if ndnd in layer1:
            broken_pos[i]=[d2*(npos[0]-d1),d2*(npos[1]+d1)] 
            top_set.add(i)
            left.append(broken_pos[i])
        elif ndnd in layer2:
            broken_pos[i]=[d2*(npos[0]+d1),d2*(npos[1]+d1)] 
            bottom_set.add(i)
            right.append(broken_pos[i])
        else:
            broken_pos[i]=[d2*npos[0],d2*(npos[1]-d1)] 
            middle_set.add(i)
            down.append(broken_pos[i])
       
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

    nodeSize=[nodesize*len(broken_partition[i]) for i in list(top_set)]
    nodeColor=[broken_graph.node[i]['color'] for i in list(top_set) ]
    
    nx.draw_networkx_nodes(broken_graph,broken_pos, nodelist=list(top_set),node_shape='s',node_color=nodeColor,alpha=1,node_size=nodeSize)
    nodeSize=[nodesize*len(broken_partition[i]) for i in list(middle_set)]
    nodeColor=[broken_graph.node[i]['color'] for i in list(middle_set) ]
    
    nx.draw_networkx_nodes(broken_graph,broken_pos, nodelist=list(middle_set),node_shape='s',node_color=nodeColor,alpha=1,node_size=nodeSize)
    nodeSize=[nodesize*len(broken_partition[i]) for i in list(bottom_set)]
    nodeColor=[broken_graph.node[i]['color'] for i in list(bottom_set) ]

    nx.draw_networkx_nodes(broken_graph,broken_pos,nodelist=list(bottom_set),node_shape='s',node_color=nodeColor,alpha=1,node_size=nodeSize)
    
    if withlabels:
        nx.draw_networkx_labels(G,pos)
    
    lay1_edges=[ed for ed in G.edges() if ed[0] in layer1 and ed[1] in layer1]
    lay2_edges=[ed for ed in G.edges() if ed[0] in layer2 and ed[1] in layer2]
    lay3_edges=[ed for ed in G.edges() if ed[0] in layer3 and ed[1] in layer3]
    

    nx.draw_networkx_edges(broken_graph,broken_pos,alpha=0.3) #0.15
    # orr=nx.attribute_assortativity_coefficient(broken_graph,'color')
    for i,v in broken_partition.items():
        for nd in v:
            atrr=G.node[nd]
            G.add_node(nd,attr_dict=atrr,asso=i)
    rr=nx.attribute_assortativity_coefficient(G,'asso')
    # print 'Attribute assortativity coefficient wrt layer partition (old) = %f' %orr
    title_s='%i connected components (%i 3-layered, %i 2-layered, %i 1-layered)\n  Discrete assortativity coefficient of the joint partition for connected_components and 3 layers = %f ' %(len(npartition),layers_m[3],layers_m[2],layers_m[1],rr)
    plt.title(title_s,{'size': '20'})
    
    plt.axis('off')
    
    plt.show()




# n = 50
# p = 0.05
# r1 = 0.333
# r2 = 0.333
# r3 = 0.333
# G, layer1, layer2, layer3, edgeList = analyticThreeLayerGraph(n,p,r1,r2,r3,G_isolates=False)
# # # print G.nodes()
# # # print layer1
# # # print layer2
# # # print layer3
# broken_graph,broken_partition,npartition=create_node_conncomp_graph(G,layer1,layer2,layer3)
# # # print broken_partition
# print broken_graph.nodes(data=True)
# plot_graph(G,broken_graph,broken_partition,npartition,layer1,layer2,layer3,withlabels=False,nodesize=10,layout=False)
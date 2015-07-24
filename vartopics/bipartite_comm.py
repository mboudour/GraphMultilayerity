import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms import bipartite
from matplotlib.patches import Ellipse, Polygon
import matplotlib
import community as comm
from collections import Counter
import random
fig=plt.figure(num=1,figsize=(16,12))
def create_3comms_bipartite(n,m,p,No_isolates=True):
    
    # import community as comm

    # from networkx.algorithms import bipartite as bip
    u=0
    while  True:
        G=nx.bipartite_random_graph(n,m,p)
        list_of_isolates=nx.isolates(G)
        if No_isolates:
            G.remove_nodes_from(nx.isolates(G))
        partition=comm.best_partition(G)
        sel=max(partition.values())
        if sel==2 and nx.is_connected(G):
            break
        u+=1
        # print u,sel
    ndlss=bipartite.sets(G)
    print 'n = %i' %len(ndlss[0])
    print 'm = %i' %len(ndlss[1])
    print 'Number of edges = %i' %len(G.edges())
    ndls=[list(i) for i in ndlss]
    slayer1=ndls[0]
    slayer2=ndls[1]
    layer1=[i for i,v in partition.items() if v==0]
    layer2=[i for i,v in partition.items() if v==1]
    layer3=[i for i,v in partition.items() if v==2]
    print 'Community1 = ', layer1
    print 'Community2 = ' ,layer2
    print 'Community3 = ' ,layer3

    edgeList=[]
    for e in G.edges():
        if (e[0] in slayer1 and e[1] in slayer2) or (e[0] in slayer2 and e[1] in slayer1):
            edgeList.append(e)
    return G,layer1,layer2,layer3,slayer1,slayer2,edgeList,partition

def plot_initial_graph(G):
    fig=plt.figure(num=1,figsize=(16,12))
    
    sets=bipartite.sets(G)
    pos=nx.spring_layout(G)
    nx.draw_networkx_nodes(G,pos=pos,nodelist=list(sets[0]),node_color='grey',alpha=0.3)
    nx.draw_networkx_nodes(G,pos=pos,nodelist=list(sets[1]),node_color='gold')
    nx.draw_networkx_labels(G,pos=pos)
    nx.draw_networkx_edges(G,pos=pos,alpha=0.2)
    plt.axis("off")
    plt.show()
    
def plot_initial_bgraph(G,subp=121):
    fig=plt.figure(num=1,figsize=(16,12))
    fig.add_subplot(subp)
    sets=bipartite.sets(G)
    pos={}
    for i,v in enumerate(sets[0]):
        pos[v]= (0.,i)
    for i,v in enumerate(sets[1]):
        pos[v]= (1, i)

    rr=nx.attribute_assortativity_coefficient(G,'bipartite')
    s_title='Bipartite Graph\nAssortativity_coef(bipartition) = %.2f' %rr
    plt.title(s_title)#,{'size': '20'})
    nx.draw_networkx_nodes(G,pos=pos,nodelist=list(sets[0]),node_color='grey',alpha=0.3)
    nx.draw_networkx_nodes(G,pos=pos,nodelist=list(sets[1]),node_color='gold')
    nx.draw_networkx_labels(G,pos=pos)
    nx.draw_networkx_edges(G,pos=pos,alpha=0.2)
    plt.axis("off")
    # plt.show()  
    return pos,fig

def create_colors_per_comm(G,layer1,layer2,layer3,slayer1,slayer2,pos,fig,subp=(122)):
    for i in layer1:
        G.add_node(i,color='r',attr_dict=G.node[i],best_partition_comm='1')
    for i in layer2:
        G.add_node(i,color='g',attr_dict=G.node[i],best_partition_comm='2')
    for i in layer3:
        G.add_node(i,color='b',attr_dict=G.node[i],best_partition_comm='3')    
    fig.add_subplot(subp)
    # for i in G.nodes(data=True):
    #     print i
    # rr=nx.attribute_assortativity_coefficient(G,'color')
    rra=nx.attribute_assortativity_coefficient(G,'best_partition_comm')
    s_title='Community Partition\nAssortativity_coef(3_communities) = %.2f ' %(rra)
    plt.title(s_title)#,{'size': '20'})
    nodecolor=[i[1]['color'] for i in G.nodes(data=True)]
    nx.draw_networkx_nodes(G,pos=pos,node_color=nodecolor,alpha=0.3)
    # nx.draw_networkx_nodes(G,pos=pos,nodelist=list(sets[1]),node_color='gold')
    nx.draw_networkx_labels(G,pos=pos)
    nx.draw_networkx_edges(G,pos=pos,alpha=0.2)


    plt.axis("off")

def create_2colors_per_comm(G,layer1,layer2,layer3,slayer1,slayer2,pos,fig,subp=122):
    sl11=random.sample(slayer1,len(slayer1)/2)
    sl12=list(set(slayer1)-set(sl11))
    # print G.nodes(data=True)
    for i in sl11:
        G.add_node(i,color='y',attr_dict=G.node[i],fattr='1')
    for i in sl12:
        G.add_node(i,color='grey',attr_dict=G.node[i],fattr='2')
    sl21=random.sample(slayer2,len(slayer2)/2)
    sl22=list(set(slayer2)-set(sl21))
    for i in sl21:
        G.add_node(i,color='m',attr_dict=G.node[i],fattr='3')
    for i in sl22:
        G.add_node(i,color='c',attr_dict=G.node[i],fattr='4')
    fig.add_subplot(subp)
    # for i in G.nodes():
    #     if i in la
    # for i in G.nodes(data=True):
    #     print i
    rr= nx.attribute_assortativity_coefficient(G,'fattr')
    s_title='Discrete vertex attributes\nAssortativity_coef(4_attibutes) = %.2f' %rr
    plt.title(s_title)#,{'size': '20'})
    nodecolor=[i[1]['color'] for i in G.nodes(data=True)]
    nx.draw_networkx_nodes(G,pos=pos,node_color=nodecolor,alpha=0.3)
    # nx.draw_networkx_nodes(G,pos=pos,nodelist=list(sets[1]),node_color='gold')
    nx.draw_networkx_labels(G,pos=pos)
    nx.draw_networkx_edges(G,pos=pos,alpha=0.2)


    plt.axis("off")

def create_node_6attri_graph(G,layer1,layer2,layer3,slayer1,slayer2):
    '''G is a 3-layer graph 
    '''
    fig=plt.figure(figsize=(17,12))
    npart={}
    for i in G.nodes(data=True):
        if i[1]['color'] not in npart:
            npart[i[1]['color']]=[i[0]]
        else:
            npart[i[1]['color']].append(i[0])

    npartition=npart.values()#[slayer1,slayer2]
    # print npartition

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
    
    # colors=[name for name,hex in matplotlib.colors.cnames.iteritems()]
    colors=[name[1]['color'] for name in G.nodes(data=True)]
    colors=list(set(colors)-set(['red','blue','g']))
   
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
    
    return broken_graph,broken_partition,npartition,fig




def create_node_3attri_graph(G,layer1,layer2,layer3,slayer1,slayer2):
    '''G is a 3-layer graph 
    '''
   
    # layerattri1 = random.sample(G.nodes(),int(len(G.nodes())*attri1))
    # layerattri2 = random.sample(set(G.nodes())-set(layerattri1),int(len(G.nodes())*attri2))
    # layerattri3 = list(set(G.nodes())-set(layerattri1)-set(layerattri2))
    # npartition=[layerattri1,layerattri2,layerattri3]
    fig=plt.figure(figsize=(17,12))
    npartition=[slayer1,slayer2]

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
    
    return broken_graph,broken_partition,npartition,fig
def plot_graph_bip_3comms_2set(G,broken_graph,broken_partition,npartition,layer1,layer2,layer3,fig,asso=True,d1=1.5,d2=5.,d3=0,d4=.8,nodesize=1000,withlabels=True,edgelist=[],layout=True,alpha=0.5):
    
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

    # fig=plt.figure(figsize=(20,20))
    # plt.subplot(1,2,1)
    if asso:
        ax=fig.add_subplot(121)
    else:
        ax=fig.add_subplot(111)

    ax.add_patch(Polygon([aleft,bleft,cleft,dleft],color='r',alpha=0.1)) 
    plt.plot([aleft[0],bleft[0],cleft[0],dleft[0],aleft[0]],[aleft[1],bleft[1],cleft[1],dleft[1],aleft[1]],'-r')

    ax.add_patch(Polygon([aright,bright,cright,dright],color='b',alpha=0.1)) 
    plt.plot([aright[0],bright[0],cright[0],dright[0],aright[0]],[aright[1],bright[1],cright[1],dright[1],aright[1]],'-b')

    ax.add_patch(Polygon([adown,bdown,cdown,ddown],color='g',alpha=0.1)) 
    plt.plot([adown[0],bdown[0],cdown[0],ddown[0],adown[0]],[adown[1],bdown[1],cdown[1],ddown[1],adown[1]],'-g')

    nodeSize=[nodesize*len(broken_partition[i]) for i in list(top_set)]
    nodeColor=[broken_graph.node[i]['color'] for i in list(top_set) ]
    
    nx.draw_networkx_nodes(broken_graph,broken_pos, nodelist=list(top_set),node_shape='s',node_color=nodeColor,alpha=.9,node_size=nodeSize)
    nodeSize=[nodesize*len(broken_partition[i]) for i in list(middle_set)]
    nodeColor=[broken_graph.node[i]['color'] for i in list(middle_set) ]
    
    nx.draw_networkx_nodes(broken_graph,broken_pos, nodelist=list(middle_set),node_shape='s',node_color=nodeColor,alpha=.9,node_size=nodeSize)
    nodeSize=[nodesize*len(broken_partition[i]) for i in list(bottom_set)]
    nodeColor=[broken_graph.node[i]['color'] for i in list(bottom_set) ]

    nx.draw_networkx_nodes(broken_graph,broken_pos,nodelist=list(bottom_set),node_shape='s',node_color=nodeColor,alpha=.9,node_size=nodeSize)
    
    if withlabels:
        nx.draw_networkx_labels(G,pos)
    
    lay1_edges=[ed for ed in G.edges() if ed[0] in layer1 and ed[1] in layer1]
    lay2_edges=[ed for ed in G.edges() if ed[0] in layer2 and ed[1] in layer2]
    lay3_edges=[ed for ed in G.edges() if ed[0] in layer3 and ed[1] in layer3]

    
    nx.draw_networkx_edges(broken_graph,broken_pos,alpha=0.3) #0.15
    orr=nx.attribute_assortativity_coefficient(broken_graph,'color')
    for i,v in broken_partition.items():
        for nd in v:
            atrr=G.node[nd]
            G.add_node(nd,attr_dict=atrr,asso=i)
    # print G.nodes(data=True)
    # print len(set(broken_partition))
    crr=nx.attribute_assortativity_coefficient(G,'color')
    rr=nx.attribute_assortativity_coefficient(G,'asso')
    if asso:
        # rr=nx.attribute_assortativity_coefficient(broken_graph,'color')
        # print 'Bipartition attribute assortativity coefficient wrt community partition(old) = %f' %orr
        title_s='Bipartite graph with 3 communities as 3-layers (%i 3-layered, %i 2-layered, %i 1-layered)\n Joint_Assortativity_coef(3_communities,bipartition) = %.2f' %(layers_m[3],layers_m[2],layers_m[1],rr)  
    else:
        # rr=nx.attribute_assortativity_coefficient(broken_graph,'color')
        # print 'Discrete attribute assortativity coefficient wrt community partition = %f' %orr
        title_s='Bipartite graph with 3 communities as 3-layers (%i 3-layered, %i 2-layered, %i 1-layered)\n Joint_Assortativity_coef(3_communities,%i_attributes) = %.2f' %(layers_m[3],layers_m[2],layers_m[1],len(set(broken_partition)),rr)  
        # title_s='Bipartite graph with 3 communities as 3-layers (%i 3-layered, %i 2-layered, %i 1-layered)\n Discrete assortativity coefficient of the joint partition for communities and %i attributes = %f' %(layers_m[3],layers_m[2],layers_m[1],len(set(broken_partition)),rr)  
            
    # title_s='%i Three vertex attributes (%i 3-layered, %i 2-layered, %i 1-layered)' %(len(npartition),layers_m[3],layers_m[2],layers_m[1])
    plt.title(title_s,{'size': '12'})
    plt.axis('off')
    # plt.show()

def create_node_2attri_graph(G,layer1,layer2,layer3,slayer1,slayer2,asso=True):
    '''G is a 3-layer graph 
    '''
   
    # layerattri1 = random.sample(G.nodes(),int(len(G.nodes())*attri1))
    # layerattri2 = random.sample(set(G.nodes())-set(layerattri1),int(len(G.nodes())*attri2))
    # layerattri3 = list(set(G.nodes())-set(layerattri1)-set(layerattri2))
    # npartition=[layerattri1,layerattri2,layerattri3]
    npartition=[layer1,layer2,layer3]

    layers={'layer1':slayer1,'layer2':slayer2}#,'layer3':layer3}
   
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
    # print colors[:2]
    # colors=list(set(colors)-set(['red','blue','green']))
    if asso:
        colors=['r','b','g']
    else:
        colors=[i[1]['color'] for i in G.nodes(data=True)]
   
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
    # print broken_partition,npartition,layers
    return broken_graph,broken_partition,npartition
def plot_graph_bip_2set_3comms(G,broken_graph,broken_partition,npartition,layer1,layer2,layer3,fig,d1=1.5,d2=5.,d3=0,d4=.8,nodesize=1000,withlabels=True,edgelist=[],layout=True,alpha=0.5):
    
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
        # else:
        #     broken_pos[i]=[d2*npos[0],d2*(npos[1]-d1)] 
        #     middle_set.add(i)
        #     down.append(broken_pos[i])
    # print top_set
    # print bottom_set 
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

    # xdown=[i[0] for i in down]
    # ydown=[i[1] for i in down]

    # adown = [min(xdown)-d1/2.,max(ydown)+d1/2.+d3]
    # bdown = [max(xdown)+d1/2.,max(ydown)+d1/2.+3*d3]
    # cdown = [max(xdown)+d1/2.,min(ydown)-d1/2.-3*d3]
    # ddown = [min(xdown)-d1/2.,min(ydown)-d1/2.-d3]

    # fig=plt.figure(figsize=(20,20))
        # plt.subplot(1,2,1)

    ax=fig.add_subplot(122)

    ax.add_patch(Polygon([aleft,bleft,cleft,dleft],color='grey',alpha=0.1)) 
    plt.plot([aleft[0],bleft[0],cleft[0],dleft[0],aleft[0]],[aleft[1],bleft[1],cleft[1],dleft[1],aleft[1]],'-',color='grey')

    ax.add_patch(Polygon([aright,bright,cright,dright],color='gold',alpha=0.1)) 
    plt.plot([aright[0],bright[0],cright[0],dright[0],aright[0]],[aright[1],bright[1],cright[1],dright[1],aright[1]],'-',color='gold')

    # ax.add_patch(Polygon([adown,bdown,cdown,ddown],color='g',alpha=0.1)) 
    # plt.plot([adown[0],bdown[0],cdown[0],ddown[0],adown[0]],[adown[1],bdown[1],cdown[1],ddown[1],adown[1]],'-g')

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
    # print G.nodes()
    # print npartition
    for i,v in enumerate(npartition):
        for nd in v:
            G.add_node(nd,part=i)


 #    print 'bbbbbb'
    # print G.nodes(data=True)
 #      print 'aaaaa'
    rrd=nx.attribute_assortativity_coefficient(G,'part')
    nx.draw_networkx_edges(broken_graph,broken_pos,alpha=0.3) #0.15
    orr=nx.attribute_assortativity_coefficient(broken_graph,'color')
    for i,v in broken_partition.items():
        for nd in v:
            atrr=G.node[nd]
            G.add_node(nd,attr_dict=atrr,asso=i)
    # print G.nodes(data=True)
    rr=nx.attribute_assortativity_coefficient(G,'asso')
    # print 'Community partition attribute assortativity coefficient wrt bipartition = %f' %orr
    # title_s='Bipartite graph with bipartition as 2-layers (%i 2-layered, %i 1-layered)\n Discrete assortativity coefficient of the joint partition of communities and bipartition = %f\n(Community partition attribute assortativity coefficient = %f)' %(layers_m[2],layers_m[1],rr,rrd)  
    title_s='Bipartite graph with bipartition as 2-layers (%i 2-layered, %i 1-layered)\n Joint_Assortativity_coef(bipartition,3_communities) = %.2f' %(layers_m[2],layers_m[1],rr)  

    # title_s='%i Three vertex attributes (%i 3-layered, %i 2-layered, %i 1-layered)' %(len(npartition),layers_m[3],layers_m[2],layers_m[1])
    plt.title(title_s,{'size': '12'})
    plt.axis('off')
    plt.show()


# n=7
# m=6
# p=0.19
# G,layer1,layer2,layer3,slayer1,slayer2,edgeList,partition=create_3comms_bipartite(n,m,p)
# broken_graph,broken_partition,npartition = create_node_3attri_graph(G,layer1,layer2,layer3,slayer1,slayer2)
# fig=plt.figure(num=1,figsize=(12,12))

# plot_graph_bip_3comms_2set(G,broken_graph,broken_partition,npartition,layer1,layer2,layer3,fig,d1=1.4,d2=5.,d3=0.8,withlabels=False,nodesize=100,layout=False)
# # print G,layer1,layer2
# broken_graph,broken_partition,npartition=create_node_2attri_graph(G,layer1,layer2,layer3,slayer1,slayer2)
# plot_graph_bip_2set_3comms(G,broken_graph,broken_partition,npartition,slayer1,slayer2,layer3,fig,d1=1.4,d2=5.,d3=0.8,withlabels=False,nodesize=100,layout=False)

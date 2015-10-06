__author__ = "Moses A. Boudourides & Sergios T. Lenis"
__copyright__ = "Copyright (C) 2015 Moses A. Boudourides & Sergios T. Lenis"
__license__ = "Public Domain"
__version__ = "1.0"

'''
This script computes and plots dominating sets and communities.
'''

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
    return G

def create_conn_random_graph_chrom(nodes,p,x):
    while  True:
        # G=nx.connected_watts_strogatz_graph(25, 2, 0.8, tries=100)
        G=nx.erdos_renyi_graph(nodes,p)
        if nx.is_connected(G):
            g=Graph(G)
            cn=vertex_coloring(g, value_only=True)
            if cn==x:
                break
    G.remove_nodes_from(nx.isolates(G))
    return G

# def draw_doms(G,dom,idom,doml,nodoml,d,dd):
#     pos=nx.spring_layout(G)
    
#     col=[]
#     for nd in G.nodes():
#         if nd in dom:
#             col.append('r')
#         elif nd in doml:
#             col.append('m')
#         elif nd in nodoml:
#             col.append('c')
#         else:
#             col.append('b')

#     for i in pos:
#         npos=pos[i]
#         if i in dom:
#             pos[i]=[dd*npos[0],npos[1]+d]
#         elif i in doml:
#             pos[i]=[dd*npos[0],npos[1]-d]
#         else:
#             pos[i]=[dd*npos[0],npos[1]-d]

#     fig = plt.figure(figsize=(17,8))

#     sstt="Minimum Dominating Set" 
#     plt.subplot(1,2,1).set_title(sstt)
#     nx.draw_networkx_nodes(G,pos=pos, node_color=col) 
#     nx.draw_networkx_labels(G,pos,font_color='w')
#     nx.draw_networkx_edges(G,pos,edge_color='k',alpha=0.5)
#     plt.axis('equal')
#     plt.axis('off')

    
#     pos=nx.spring_layout(G)

#     col=[]
#     for nd in G.nodes():
#         if nd in idom:
#             col.append('g')
#         elif nd in doml:
#             col.append('m')
#         elif nd in nodoml:
#             col.append('c')
#         else:
#             col.append('b')

#     for i in pos:
#         npos=pos[i]
#         if i in idom:
#             pos[i]=[dd*npos[0],npos[1]+d]
#         elif i in doml:
#             pos[i]=[dd*npos[0],npos[1]-d]
#         else:
#             pos[i]=[dd*npos[0],npos[1]-d]

#     sstt="Independent Dominating Set" 
#     plt.subplot(1,2,2).set_title(sstt)
#     nx.draw_networkx_nodes(G,pos=pos, node_color=col)  
#     nx.draw_networkx_labels(G,pos,font_color='w')
#     nx.draw_networkx_edges(G,pos,edge_color='k',alpha=0.5)
#     plt.axis('equal')
#     plt.axis('off')
#     plt.show()



def draw_domcomms(G,dom,idom,doml,nodoml ,par,cpar,d,dd,c,cc,alpha,ealpha):
    import community 
    from matplotlib.patches import Ellipse
    
    import matplotlib
    
    # par= community.best_partition(G)
    invpar={}

    for i,v in par.items():
        if v not in invpar:
            invpar[v]=[i]
        else:
            invpar[v].append(i)
    ninvpar={}
    for i,v in invpar.items():
        if i not in ninvpar:
            ninvpar[i]=nx.spring_layout(G.subgraph(v))
    pos=nx.spring_layout(G)
    
    
        
    ells=[]
    ellc=[]
    colors=[name for name,hex in matplotlib.colors.cnames.iteritems()]
    colors=list(set(colors)-set(['red','blue','green','m','c']))
    col_dic={}
    for i,v in ninvpar.items():
        xp=[xx[0] for x,xx in v.items()]
        yp=[yy[1] for y,yy in v.items()]

        ells.append(Ellipse(xy=(((-1)**i)*dd+max(xp)/2.,d*i+max(yp)/2.),width=cc*max(xp)/dd,height=c*max(yp)/d))
        colll=random.choice(colors)
        ellc.append(colll)
        colors.remove(colll)
        col_dic[i]=colll
        for j in v:
            npos=v[j]
            pos[j]=[((-1)**par[j])*dd+npos[0],npos[1]+d*par[j]]

    col=[]
    if dom==G.nodes():
        for nd in G.nodes():
            col.append(col_dic[par[nd]])
    else:
        for nd in G.nodes():
            if nd in dom:
                col.append('r')
            elif nd in doml:
                col.append('m')
            elif nd in nodoml:
                col.append('c')
            else:
                col.append('b')


    fig = plt.figure(figsize=(16,8))
    ncomm=max(par.values())+1
    sstt="Chromatic Partition in %s Groups" %ncomm
    plt.subplot(121).set_title(sstt)
    ax = fig.add_subplot(121)
    ax.set_title(sstt)
    for i,e in enumerate(ells):
        ax.add_artist(e)
        e.set_clip_box(ax.bbox)
        e.set_alpha(alpha)
        e.set_facecolor(ellc[i])
    nx.draw_networkx_nodes(G,pos=pos, node_color=col) 
    nx.draw_networkx_labels(G,pos,font_color='k')
    nx.draw_networkx_edges(G,pos,edge_color='k',alpha=ealpha)
    plt.axis('equal')
    plt.axis('off')

    # pos=nx.spring_layout(G)

    # col=[]
    # for nd in G.nodes():
    #     if nd in idom:
    #         col.append('g')
    #     elif nd in doml:
    #         col.append('m')
    #     elif nd in nodoml:
    #         col.append('c')
    #     else:
    #         col.append('b')
    cinvpar={}

    for i,v in cpar.items():
        if v not in cinvpar:
            cinvpar[v]=[i]
        else:
            cinvpar[v].append(i)
    cninvpar={}
    for i,v in cinvpar.items():
        if i not in cninvpar:
            cninvpar[i]=nx.spring_layout(G.subgraph(v))
            # gg=Graph(G.subgraph(v))
            # print i,vertex_coloring(gg, value_only=False)
    ells=[]
    # colors=[name for name,hex in matplotlib.colors.cnames.iteritems()]
    # colors=list(set(colors)-set(['red','blue','green','m','c']))
    for i,v in cninvpar.items():
        xp=[xx[0] for x,xx in v.items()]
        yp=[yy[1] for y,yy in v.items()]

        ells.append(Ellipse(xy=(((-1)**i)*dd+max(xp)/2.,d*i+max(yp)/2.),width=cc*max(xp)/dd,height=c*max(yp)/d))
        colll=random.choice(colors)
        ellc.append(colll)
        colors.remove(colll)
        col_dic[i]=colll
        for j in v:
            npos=v[j]
            pos[j]=[((-1)**cpar[j])*dd+npos[0],npos[1]+d*cpar[j]]

    ncomm=max(cpar.values())+1
    sstt="Community Partition in %s Groups" %ncomm
    plt.subplot(1,2,2).set_title(sstt)
    ax = fig.add_subplot(1,2,2)

    ax.set_title(sstt)
    for i,e in enumerate(ells):
        ax.add_artist(e)
        e.set_clip_box(ax.bbox)
        e.set_alpha(alpha)
        e.set_facecolor(ellc[i])
    nx.draw_networkx_nodes(G,pos=pos, node_color=col)  
    nx.draw_networkx_labels(G,pos)#,font_color='w')
    nx.draw_networkx_edges(G,pos,edge_color='k',alpha=ealpha)
    plt.axis('equal')
    plt.axis('off')
    plt.show()



def draw_comms(G,dom,idom,doml,nodoml ,par,cpar,d,dd,c,cc,alpha,ealpha,nodper,sstt):
    import community 
    from matplotlib.patches import Ellipse
    
    import matplotlib
    
    # par= community.best_partition(G)
    invpar={}

    for i,v in par.items():
        if v not in invpar:
            invpar[v]=[i]
        else:
            invpar[v].append(i)
    ninvpar={}
    for i,v in invpar.items():
        if i not in ninvpar:
            ninvpar[i]=nx.spring_layout(G.subgraph(v))
    pos=nx.spring_layout(G)

    # pos=pos_dict[0]

    # print ninvpar
    
        
    ells=[]
    ellc=[]
    colors=[name for name,hex in matplotlib.colors.cnames.iteritems()]
    colors=list(set(colors)-set(['red','blue','green','m','c']))
    col_dic={}
    for i,v in ninvpar.items():
        xp=[xx[0] for x,xx in v.items()]
        yp=[yy[1] for y,yy in v.items()]

        # ells.append(Ellipse(xy=(((-1)**i)*dd+max(xp)/2.,d*i+max(yp)/2.),width=cc*max(xp)/dd,height=c*max(yp)/d))
        colll=random.choice(colors)
        ellc.append(colll)
        colors.remove(colll)
        col_dic[i]=colll
        # for j in v:
        #     npos=v[j]
        #     pos[j]=[((-1)**par[j])*dd+npos[0],npos[1]+d*par[j]]

    col=[]
    if dom==G.nodes():
        for nd in G.nodes():
            col.append(col_dic[par[nd]])
    else:
        for nd in G.nodes():
            if nd in dom:
                col.append('r')
            elif nd in doml:
                col.append('m')
            elif nd in nodoml:
                col.append('c')
            else:
                col.append('b')


    fig = plt.figure(figsize=(12,12))
    # plt.figure(figsize=(12,12))

    # ncomm=max(par.values())+1
    # sstt="Chromatic Partition in %s Groups" %ncomm
    # plt.subplot(121).set_title(sstt)
    # ax = fig.add_subplot(121)
    # ax.set_title(sstt)
    # for i,e in enumerate(ells):
    #     ax.add_artist(e)
    #     e.set_clip_box(ax.bbox)
    #     e.set_alpha(alpha)
    #     e.set_facecolor(ellc[i])
    # nx.draw_networkx_nodes(G,pos=pos, node_color=col) 
    # nx.draw_networkx_labels(G,pos,font_color='k')
    # nx.draw_networkx_edges(G,pos,edge_color='k',alpha=ealpha)
    # plt.axis('equal')
    # plt.axis('off')

    # # pos=nx.spring_layout(G)

    # # col=[]
    # # for nd in G.nodes():
    # #     if nd in idom:
    # #         col.append('g')
    # #     elif nd in doml:
    # #         col.append('m')
    # #     elif nd in nodoml:
    # #         col.append('c')
    # #     else:
    # #         col.append('b')
    # cinvpar={}

    # for i,v in cpar.items():
    #     if v not in cinvpar:
    #         cinvpar[v]=[i]
    #     else:
    #         cinvpar[v].append(i)
    # cninvpar={}
    # for i,v in cinvpar.items():
    #     if i not in cninvpar:
    #         cninvpar[i]=nx.spring_layout(G.subgraph(v))
    #         # gg=Graph(G.subgraph(v))
    #         # print i,vertex_coloring(gg, value_only=False)
    # ells=[]
    # # colors=[name for name,hex in matplotlib.colors.cnames.iteritems()]
    # # colors=list(set(colors)-set(['red','blue','green','m','c']))
    # for i,v in cninvpar.items():
    #     xp=[xx[0] for x,xx in v.items()]
    #     yp=[yy[1] for y,yy in v.items()]

    #     ells.append(Ellipse(xy=(((-1)**i)*dd+max(xp)/2.,d*i+max(yp)/2.),width=cc*max(xp)/dd,height=c*max(yp)/d))
    #     colll=random.choice(colors)
    #     ellc.append(colll)
    #     colors.remove(colll)
    #     col_dic[i]=colll
    #     for j in v:
    #         npos=v[j]
    #         pos[j]=[((-1)**cpar[j])*dd+npos[0],npos[1]+d*cpar[j]]

    ncomm=max(cpar.values())+1
    # sstt="The %s Communities of Hamlet Act I Network" %ncomm
    plt.figure(figsize=(12,12))
    
    plt.title(sstt,fontsize=20)
	# kk=plt.axis('off')

    # plt.subplot(1,1,1).set_title(sstt)
    # ax = fig.add_subplot(1,1,1)
    
    # print nodper,G.nodes()
    labelsn={v:i for v,i in nodper.items() if v in G.nodes()}
    # print labelsn
    # print pos
    edgewidth=[]
    for (u,v,d) in G.edges(data=True):
        edgewidth.append(d['weight'])
    
    # ax.set_title(sstt)
    
    for i,e in enumerate(ells):
        ax.add_artist(e)
        e.set_clip_box(ax.bbox)
        e.set_alpha(alpha)
        e.set_facecolor(ellc[i])
    nx.draw_networkx_nodes(G,pos=pos, node_color=col)  
    nx.draw_networkx_labels(G,pos,labels=labelsn,font_size=20)#,font_color='w')
    nx.draw_networkx_edges(G,pos,edge_color='k',width=edgewidth, alpha=ealpha)
    plt.axis('equal')
    plt.axis('off')
    plt.show()






def draw_domcomms_sr(G,layer1,layer2,dom,idom,doml,nodoml ,par,cpar,d,dd,c,cc,alpha,ealpha,labels=False,nodesize=10):
    import community 
    from matplotlib.patches import Ellipse
    import random

    
    # par= community.best_partition(G)
    invpar={}

    for i,v in par.items():
        if v not in invpar:
            invpar[v]=[i]
        else:
            invpar[v].append(i)
    ninvpar={}
    for i,v in invpar.items():
        if i not in ninvpar:
            ninvpar[i]=nx.spring_layout(G.subgraph(v))
    pos=nx.spring_layout(G)
    
    
        
    ells=[]
    ellc=[]
    colors=[name for name,hex in matplotlib.colors.cnames.iteritems()]
    colors=list(set(colors)-set(['red','blue','green','m','c']))
    col_dic={}
    for i,v in ninvpar.items():
        xp=[xx[0] for x,xx in v.items()]
        yp=[yy[1] for y,yy in v.items()]

        ells.append(Ellipse(xy=(((-1)**i)*dd+max(xp)/2.,d*i+max(yp)/2.),width=cc*max(xp)/dd,height=c*max(yp)/d))
        colll=random.choice(colors)
        ellc.append(colll)
        colors.remove(colll)
        col_dic[i]=colll
        for j in v:
            npos=v[j]
            pos[j]=[((-1)**par[j])*dd+npos[0],npos[1]+d*par[j]]

    col1=[]
    col2=[]
    if dom==G.nodes():
        for nd in G.nodes():
            if nd in layer1:
                col1.append(col_dic[par[nd]])
            if nd in layer2:
                col2.append(col_dic[par[nd]])
    else:
        for nd in G.nodes():
            if nd in dom:
                col.append('r')
            elif nd in doml:
                col.append('m')
            elif nd in nodoml:
                col.append('c')
            else:
                col.append('b')


    fig = plt.figure(figsize=(16,8))
    ncomm=max(par.values())+1
    sstt="Chromatic Partition in %s Groups" %ncomm
    plt.subplot(121).set_title(sstt)
    ax = fig.add_subplot(121)
    ax.set_title(sstt)
    for i,e in enumerate(ells):
        ax.add_artist(e)
        e.set_clip_box(ax.bbox)
        e.set_alpha(alpha)
        e.set_facecolor(ellc[i])
    nx.draw_networkx_nodes(G,pos=pos, node_color=col1,nodelist=layer1,node_size=nodesize) 
    nx.draw_networkx_nodes(G,pos=pos, node_color=col2,nodelist=layer2,node_shape='s',node_size=nodesize)  
    if labels:
        nx.draw_networkx_labels(G,pos,font_color='k')
    nx.draw_networkx_edges(G,pos,edge_color='k',alpha=ealpha)
    plt.axis('equal')
    plt.axis('off')

    # pos=nx.spring_layout(G)

    # col=[]
    # for nd in G.nodes():
    #     if nd in idom:
    #         col.append('g')
    #     elif nd in doml:
    #         col.append('m')
    #     elif nd in nodoml:
    #         col.append('c')
    #     else:
    #         col.append('b')
    cinvpar={}

    for i,v in cpar.items():
        if v not in cinvpar:
            cinvpar[v]=[i]
        else:
            cinvpar[v].append(i)
    cninvpar={}
    for i,v in cinvpar.items():
        if i not in cninvpar:
            cninvpar[i]=nx.spring_layout(G.subgraph(v))
            # gg=Graph(G.subgraph(v))
            # print i,vertex_coloring(gg, value_only=False)
    ells=[]
    # colors=[name for name,hex in matplotlib.colors.cnames.iteritems()]
    # colors=list(set(colors)-set(['red','blue','green','m','c']))
    for i,v in cninvpar.items():
        xp=[xx[0] for x,xx in v.items()]
        yp=[yy[1] for y,yy in v.items()]

        ells.append(Ellipse(xy=(((-1)**i)*dd+max(xp)/2.,d*i+max(yp)/2.),width=cc*max(xp)/dd,height=c*max(yp)/d))
        colll=random.choice(colors)
        ellc.append(colll)
        colors.remove(colll)
        col_dic[i]=colll
        for j in v:
            npos=v[j]
            pos[j]=[((-1)**cpar[j])*dd+npos[0],npos[1]+d*cpar[j]]

    ncomm=max(cpar.values())+1
    sstt="Community Partition in %s Groups" %ncomm
    plt.subplot(1,2,2).set_title(sstt)
    ax = fig.add_subplot(1,2,2)

    ax.set_title(sstt)
    for i,e in enumerate(ells):
        ax.add_artist(e)
        e.set_clip_box(ax.bbox)
        e.set_alpha(alpha)
        e.set_facecolor(ellc[i])
    nx.draw_networkx_nodes(G,pos=pos, node_color=col1,nodelist=layer1,node_size=nodesize) 
    nx.draw_networkx_nodes(G,pos=pos, node_color=col2,nodelist=layer2,node_shape='s',node_size=nodesize) 
    if labels:

        nx.draw_networkx_labels(G,pos)#,font_color='w')
    nx.draw_networkx_edges(G,pos,edge_color='k',alpha=ealpha)
    plt.axis('equal')
    plt.axis('off')
    plt.show()


def attribute_ac(M):
    
    try:
        import numpy
    except ImportError:
        raise ImportError(
          "attribute_assortativity requires NumPy: http://scipy.org/ ")
    if M.sum() != 1.0:
        M=M/float(M.sum())
    M=numpy.asmatrix(M)
    s=(M*M).sum()
    t=M.trace()
    r=(t-s)
    return float(r)

def modul_arity(G,attribute):
    from correlationss import attribute_mixing_matrix
    M = attribute_mixing_matrix(G,attribute)
    return attribute_ac(M)

def sim_for_ch(G,start,stop,iterations,k,x,chromAttrassor,commAttrassor,commNumber,stringTitle=''):
    import random
    # import matplotlib.cbook as cbook
    ll={}
    llm=[]
    lln=[]
    ppn=[]
    ppm=[]
    pp={}
    plt.figure(figsize=(12,8))  
    for i in range(start,stop):
        ll[i]=[]
        pp[i]=[]
        for j in range(iterations):
            while True:
                checki=set()
                for nd in G.nodes():
                    kk=range(i)
                    kkll=random.choice(kk)
                    checki.add(kkll)
                    G.add_node(nd,vertex_colors=kkll)
    #             print len(checki),i
                if len(checki)==i:
                    break
            mm=modul_arity(G,'vertex_colors')
            ll[i].append(mm)
            # plt.plot(i,mm,'.k')
            # for mm in ll[i]:
            #     plt.plot(i,mm,'.k')
    #         ll[i].append(nx.attribute_assortativity_coefficient(G,'vertex_colors'))
    #         pp[i].append(nx.attribute_assortativity_coefficient(G,'comm_coll'))
        llm.append(max(ll[i]))
        lln.append(min(ll[i]))
    #     ppm.append(max(pp[i]))
    #     ppn.append(min(pp[i]))
    
    plt.plot(range(start,stop),llm,'ro',label='Sim-Max Modularity')
    plt.plot(range(start,stop),lln,'b*',label='Sim-Min Modularity')
    for kk,vv in enumerate(llm):
        plt.plot([kk+1,kk+1],[llm[kk],lln[kk]],'--k')
    # plt.plot([start,stop-1],[0,0],'-k')

    plt.xlim(start-0.1, stop-1+0.1)
    # plt.plot(range(start,stop),ppm,'-ms')
    # plt.plot(range(start,stop),ppn,'-c^')
    # plt.plot([x,x],[-1.,1.],'-g',label='Chromatic Number')
    # # chromAttrassor=modul_arity(G,)

    # plt.plot([start,stop-1],[chromAttrassor,chromAttrassor],'-c',label='Chromatic Modularity')
    # plt.plot([start,stop-1],[commAttrassor,commAttrassor],'-m',label='Community Modularity')
    # plt.plot([commNumber,commNumber],[-1,1],'-y',label='Community Number')
    # plt.legend(numpoints=1)
    plt.legend(loc=1)
    plt.plot(x, chromAttrassor, 'bD', markersize=12)  # ,label='(Chromatic Number, Chrommatic Modularity)')
    plt.annotate('(Chromatic Number, Chrommatic Modularity)', xy=(x, chromAttrassor), xytext=(x-1, chromAttrassor-0.015))
    plt.plot(commNumber, commAttrassor, 'rs', markersize=12)  # ,label='(Community Number, Community Modularity)')
    plt.annotate('(Community Number, Community Modularity)', xy=(commNumber, commAttrassor), xytext=(commNumber-1, commAttrassor-0.015))
    plt.xlabel('Number of Colors (Partition Cardinality)')
    plt.ylabel('Modularity')
    stil='%s simulations of colored partitions of graph G for %s - %s colors\n %s' %(iterations,start,stop-1,stringTitle)
    plt.title(stil)
    plt.legend()
        
    pass
def sim_for_ch1(G,start,stop,iterations,k,x,chromAttrassor,commAttrassor,commNumber,stringTitle=''):
    import random
    # import matplotlib.cbook as cbook
    ll={}
    llm=[]
    lln=[]
    ppn=[]
    ppm=[]
    pp={}
    plt.figure(figsize=(12,8))  
    for i in range(start,stop):
        ll[i]=[]
        pp[i]=[]
        for j in range(iterations):
            while True:
                checki=set()
                for nd in G.nodes():
                    kk=range(i)
                    kkll=random.choice(kk)
                    checki.add(kkll)
                    G.add_node(nd,vertex_colors=kkll)
    #             print len(checki),i
                if len(checki)==i:
                    break
            mm=modul_arity(G,'vertex_colors')
            ll[i].append(mm)
            plt.plot(i,mm,'.k')
            # for mm in ll[i]:
            #     plt.plot(i,mm,'.k')
    #         ll[i].append(nx.attribute_assortativity_coefficient(G,'vertex_colors'))
    #         pp[i].append(nx.attribute_assortativity_coefficient(G,'comm_coll'))
        llm.append(max(ll[i]))
        lln.append(min(ll[i]))
    #     ppm.append(max(pp[i]))
    #     ppn.append(min(pp[i]))
    
    plt.plot(range(start,stop),llm,'ro',label='Sim-Max Modularity')
    plt.plot(range(start,stop),lln,'b*',label='Sim-Min Modularity')
    for kk,vv in enumerate(llm):
        plt.plot([kk+1,kk+1],[llm[kk],lln[kk]],'--k')
    # plt.plot([start,stop-1],[0,0],'-k')

    plt.xlim(start-0.1, stop-1+0.1)
    # plt.plot(range(start,stop),ppm,'-ms')
    # plt.plot(range(start,stop),ppn,'-c^')
    # plt.plot([x,x],[-1.,1.],'-g',label='Chromatic Number')
    # # chromAttrassor=modul_arity(G,)

    # plt.plot([start,stop-1],[chromAttrassor,chromAttrassor],'-c',label='Chromatic Modularity')
    # plt.plot([start,stop-1],[commAttrassor,commAttrassor],'-m',label='Community Modularity')
    # plt.plot([commNumber,commNumber],[-1,1],'-y',label='Community Number')
    # plt.legend(numpoints=1)
    plt.legend(loc=1)
    plt.plot(x, chromAttrassor, 'bD', markersize=12)  # ,label='(Chromatic Number, Chrommatic Modularity)')
    # plt.annotate('(Chromatic Number, Chrommatic Modularity)', xy=(x, chromAttrassor), xytext=(x-1, chromAttrassor-0.015))
    plt.plot(commNumber, commAttrassor, 'rs', markersize=12)  # ,label='(Community Number, Community Modularity)')
    # plt.annotate('(Community Number, Community Modularity)', xy=(commNumber, commAttrassor), xytext=(commNumber-1, commAttrassor-0.015))
    plt.xlabel('Number of Colors (Partition Cardinality)')
    plt.ylabel('Modularity')
    stil='%s simulations of colored partitions of graph G for %s - %s colors\n %s' %(iterations,start,stop-1,stringTitle)
    plt.title(stil)
    plt.legend()
        
    pass


# def twolevel_plot(G,layer1,layer2,layer3,d1=1.5,d2=5.,d3=0.8,nodesize=1000,withlabels=True,edgelist=[],layout=True,alpha=0.5):

def plot_paral(G,layer1,layer2,d1=1.5,d2=5.,d3=0.8,d4=0,d5=0,d6=0,nodesize=1000,withlabels=True,edgelist=[],layout=True,alpha=0.5):
    
    edgeList =[]
    for e in G.edges():
        if (e[0] in layer1 and e[1] in layer2) or (e[0] in layer2 and e[1] in layer1):
            edgeList.append(e)
            
    pos=nx.spring_layout(G)
    # pos=nx.graphviz_layout(G)
    # d1=0.6 #1.5
    # d2=15. # 5.
    # d3=0.3 #0.8
    nodesize=200
    withlabels=False
    edgelist=[]
    layout=True
    alpha=0.25

    top_set=set()
    bottom_set=set()
    top=[]
    down=[]

    for i in pos:
        npos=pos[i]
        if i in layer1:
            pos[i]=[d2*(npos[0]),d2*(npos[1]+d1)] 
    #         pos[i]=[d2*(npos[0]-d1),d2*(npos[1]+d1)] 
            top_set.add(i)
            top.append(pos[i])
        else:
            pos[i]=[d6*(npos[0]),d6*(npos[1]-d1)] 
    #         pos[i]=[d2*(npos[0]+d1),d2*(npos[1]+d1)] 
            bottom_set.add(i)
            down.append(pos[i])

    xtop=[i[0] for i in top]
    ytop=[i[1] for i in top]

    atop = [min(xtop)-d4/2.+d5,max(ytop)+d4/2.+d3]
    btop = [max(xtop)+d4/2.+d5,max(ytop)+d4/2.+d3]   
    ctop = [max(xtop)+d4/2.-d5,min(ytop)-d4/2.-d3]
    dtop = [min(xtop)-d4/2.-d5,min(ytop)-d4/2.-d3]

    xdown=[i[0] for i in down]
    ydown=[i[1] for i in down]

    adown = [min(xdown)-d4/2+d5,max(ydown)+d4/2.+d3]
    bdown = [max(xdown)+d4/2.+d5,max(ydown)+d4/2.+d3]
    cdown = [max(xdown)+d4/2.-d5,min(ydown)-d4/2.-d3]
    ddown = [min(xdown)-d4/2.-d5,min(ydown)-d4/2.-d3]

    fig=plt.figure(figsize=(20,20))
    ax=fig.add_subplot(111)
    ax.add_patch(Polygon([atop,btop,ctop,dtop],color='r',alpha=0.1)) 
    plt.plot([atop[0],btop[0],ctop[0],dtop[0],atop[0]],[atop[1],btop[1],ctop[1],dtop[1],atop[1]],'-r')
    ax.add_patch(Polygon([adown,bdown,cdown,ddown],color='b',alpha=0.1)) 
    plt.plot([adown[0],bdown[0],cdown[0],ddown[0],adown[0]],[adown[1],bdown[1],cdown[1],ddown[1],adown[1]],'-b')
    nx.draw_networkx_nodes(G,pos, nodelist=top_set,node_color='r',alpha=0.2,node_size=nodesize,node_shape='s')
    nx.draw_networkx_nodes(G,pos,nodelist=bottom_set,node_color='b',alpha=0.2,node_size=nodesize)
    if withlabels:
        nx.draw_networkx_labels(G,pos)
    lay1_edges=[ed for ed in G.edges() if ed[0] in layer1 and ed[1] in layer1]
    lay2_edges=[ed for ed in G.edges() if ed[0] in layer2 and ed[1] in layer2]
    nx.draw_networkx_edges(G,pos,edgelist=lay1_edges,edge_color='r',alpha=0.15)
    nx.draw_networkx_edges(G,pos,edgelist=lay2_edges,edge_color='b',alpha=0.15)
    nx.draw_networkx_edges(G,pos,edgelist=edgeList,edge_color='k',alpha=alpha)
    plt.axis('off')
    plt.show()

def plot_paral_chr_comm(G,layer1,layer2,ccv,par,d1=1.5,d2=5.,d3=0.8,d4=0,d5=0,d6=0,nodesize=1000,withlabels=True,edgelist=[],layout=True,nodal=1,alpha=0.5):
    
    edgeList =[]
    for e in G.edges():
        if (e[0] in layer1 and e[1] in layer2) or (e[0] in layer2 and e[1] in layer1):
            edgeList.append(e)
            
    pos=nx.spring_layout(G)
    # pos=nx.graphviz_layout(G)
    # d1=0.6 #1.5
    # d2=15. # 5.
    # d3=0.3 #0.8
    # nodesize=200
    # withlabels=False
    # edgelist=[]
    # layout=True
    # alpha=0.25

    top_set=set()
    bottom_set=set()
    top=[]
    down=[]

    for i in pos:
        npos=pos[i]
        if i in layer1:
            pos[i]=[d2*(npos[0]),d2*(npos[1]+d1)] 
    #         pos[i]=[d2*(npos[0]-d1),d2*(npos[1]+d1)] 
            top_set.add(i)
            top.append(pos[i])
        else:
            pos[i]=[d6*(npos[0]),d6*(npos[1]-d1)] 
    #         pos[i]=[d2*(npos[0]+d1),d2*(npos[1]+d1)] 
            bottom_set.add(i)
            down.append(pos[i])

    xtop=[i[0] for i in top]
    ytop=[i[1] for i in top]

    atop = [min(xtop)-d4/2.+d5,max(ytop)+d4/2.+d3]
    btop = [max(xtop)+d4/2.+d5,max(ytop)+d4/2.+d3]   
    ctop = [max(xtop)+d4/2.-d5,min(ytop)-d4/2.-d3]
    dtop = [min(xtop)-d4/2.-d5,min(ytop)-d4/2.-d3]

    xdown=[i[0] for i in down]
    ydown=[i[1] for i in down]

    adown = [min(xdown)-d4/2+d5,max(ydown)+d4/2.+d3]
    bdown = [max(xdown)+d4/2.+d5,max(ydown)+d4/2.+d3]
    cdown = [max(xdown)+d4/2.-d5,min(ydown)-d4/2.-d3]
    ddown = [min(xdown)-d4/2.-d5,min(ydown)-d4/2.-d3]

    fig=plt.figure(figsize=(20,20))
    ax=fig.add_subplot(121)

    colors=[name for name,hex in matplotlib.colors.cnames.iteritems()]
    colors=list(set(colors)-set(['red','blue','green','m','c']))
    ccpar={}
    # print ccv
    for i,v in enumerate(ccv):
        for vv in v:
            # print i,v 
            if i not in ccpar:
                ccpar[i]=[vv]
            else:
                ccpar[i].append(vv)
    # print ccpar
    rccv={}
    for i,v in ccpar.items():
        # print i,v
        for ii in v:
            # print i,v,ii
            rccv[ii]=i
    # print len(ccpar)
    # print len(ccpar.keys())
    # print rccv.keys()
    col_dic={}
    for i,v in ccpar.items():
        # print i,v
        # for nd in v:
        colll=random.choice(colors)
        # ellc.append(colll)
        colors.remove(colll)
        col_dic[i]=colll
    colors_a=[]
    colors_b=[]
    for nd in top_set:
        colors_a.append(col_dic[rccv[nd]])
    for nd in bottom_set:
        colors_b.append(col_dic[rccv[nd]])

    sst='Chromatic coloring in %i groups distributed over layers' %(len(ccpar.keys()))
    plt.title(sst)

    ax.add_patch(Polygon([atop,btop,ctop,dtop],color='r',alpha=0.1)) 
    plt.plot([atop[0],btop[0],ctop[0],dtop[0],atop[0]],[atop[1],btop[1],ctop[1],dtop[1],atop[1]],'-r')
    ax.add_patch(Polygon([adown,bdown,cdown,ddown],color='b',alpha=0.1)) 
    plt.plot([adown[0],bdown[0],cdown[0],ddown[0],adown[0]],[adown[1],bdown[1],cdown[1],ddown[1],adown[1]],'-b')
    nx.draw_networkx_nodes(G,pos, nodelist=top_set,node_color=colors_a,alpha=nodal,node_size=nodesize,node_shape='s')
    nx.draw_networkx_nodes(G,pos,nodelist=bottom_set,node_color=colors_b,alpha=nodal,node_size=nodesize)
    if withlabels:
        nx.draw_networkx_labels(G,pos)
    lay1_edges=[ed for ed in G.edges() if ed[0] in layer1 and ed[1] in layer1]
    lay2_edges=[ed for ed in G.edges() if ed[0] in layer2 and ed[1] in layer2]
    nx.draw_networkx_edges(G,pos,edgelist=lay1_edges,edge_color='r',alpha=0.15)
    nx.draw_networkx_edges(G,pos,edgelist=lay2_edges,edge_color='b',alpha=0.15)
    nx.draw_networkx_edges(G,pos,edgelist=edgeList,edge_color='k',alpha=alpha)
    plt.axis('off')

    ax=fig.add_subplot(122)
    # colors=[name for name,hex in matplotlib.colors.cnames.iteritems()]
    # colors=list(set(colors)-set(['red','blue','green','m','c']))
    ccpar={}

    for i,v in enumerate(par):
        for vv in v:
            # print i,v 
            if i not in ccpar:
                ccpar[i]=[vv]
            else:
                ccpar[i].append(vv)
    # print ccpar
    rccv={}
    for i,v in ccpar.items():
        # print i,v
        for ii in v:
            # print i,v,ii
            rccv[ii]=i
    # print len(ccpar)
    # print len(ccpar.keys())
    # print rccv.keys()
    col_dic={}
    for i,v in ccpar.items():
        # print i,v
        # for nd in v:
        colll=random.choice(colors)
        # ellc.append(colll)
        colors.remove(colll)
        col_dic[i]=colll

    # for i in par:
    #     for v in i:
    #         if v not in ccpar:
    #             ccpar[v]=[i]
    #         else:
    #             ccpar[v].append(i)
    # rccv={}
    # for i,v in ccpar.items():
    #     for ii in v:
    #         rccv[ii]=i

    # col_dic={}
    # for i,v in ccpar.items():
    #     # for nd in v:
    #     colll=random.choice(colors)
    #     # ellc.append(colll)
    #     colors.remove(colll)
    #     col_dic[i]=colll
    colors_a=[]
    colors_b=[]
    for nd in top_set:
        colors_a.append(col_dic[rccv[nd]])
    for nd in bottom_set:
        colors_b.append(col_dic[rccv[nd]])
    ax.add_patch(Polygon([atop,btop,ctop,dtop],color='r',alpha=0.1)) 
    plt.plot([atop[0],btop[0],ctop[0],dtop[0],atop[0]],[atop[1],btop[1],ctop[1],dtop[1],atop[1]],'-r')
    ax.add_patch(Polygon([adown,bdown,cdown,ddown],color='b',alpha=0.1)) 

    sst='Community coloring in %i groups distributed over layers' %(len(ccpar.keys()))
    plt.title(sst)
    plt.plot([adown[0],bdown[0],cdown[0],ddown[0],adown[0]],[adown[1],bdown[1],cdown[1],ddown[1],adown[1]],'-b')
    nx.draw_networkx_nodes(G,pos, nodelist=top_set,node_color=colors_a,alpha=nodal,node_size=nodesize,node_shape='s')
    nx.draw_networkx_nodes(G,pos,nodelist=bottom_set,node_color=colors_b,alpha=nodal,node_size=nodesize)
    if withlabels:
        nx.draw_networkx_labels(G,pos)
    lay1_edges=[ed for ed in G.edges() if ed[0] in layer1 and ed[1] in layer1]
    lay2_edges=[ed for ed in G.edges() if ed[0] in layer2 and ed[1] in layer2]
    nx.draw_networkx_edges(G,pos,edgelist=lay1_edges,edge_color='r',alpha=0.15)
    nx.draw_networkx_edges(G,pos,edgelist=lay2_edges,edge_color='b',alpha=0.15)
    nx.draw_networkx_edges(G,pos,edgelist=edgeList,edge_color='k',alpha=alpha)
    plt.axis('off')

    plt.show()


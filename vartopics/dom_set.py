__author__ = "Moses A. Boudourides & Sergios T. Lenis"
__copyright__ = "Copyright (C) 2015 Moses A. Boudourides & Sergios T. Lenis"
__license__ = "Public Domain"
__version__ = "1.0"

'''
This script computes and plots dominating sets and communities.
'''

import networkx as nx
import matplotlib.pyplot as plt
import community as community

def domination(nodes,p):
    while  True:
        # G=nx.connected_watts_strogatz_graph(25, 2, 0.8, tries=100)
        G=nx.erdos_renyi_graph(nodes,p)
        if nx.is_connected(G):
            break
    G.remove_nodes_from(nx.isolates(G))
    return G


def draw_doms(G,dom,idom,doml,nodoml,d,dd):
    pos=nx.spring_layout(G)
    
    col=[]
    for nd in G.nodes():
        if nd in dom:
            col.append('r')
        elif nd in doml:
            col.append('m')
        elif nd in nodoml:
            col.append('c')
        else:
            col.append('b')

    for i in pos:
        npos=pos[i]
        if i in dom:
            pos[i]=[dd*npos[0],npos[1]+d]
        elif i in doml:
            pos[i]=[dd*npos[0],npos[1]-d]
        else:
            pos[i]=[dd*npos[0],npos[1]-d]

    fig = plt.figure(figsize=(17,8))

    sstt="Minimum Dominating Set" 
    plt.subplot(1,2,1).set_title(sstt)
    nx.draw_networkx_nodes(G,pos=pos, node_color=col) 
    nx.draw_networkx_labels(G,pos,font_color='w')
    nx.draw_networkx_edges(G,pos,edge_color='k',alpha=0.5)
    plt.axis('equal')
    plt.axis('off')

    
    pos=nx.spring_layout(G)

    col=[]
    for nd in G.nodes():
        if nd in idom:
            col.append('g')
        elif nd in doml:
            col.append('m')
        elif nd in nodoml:
            col.append('c')
        else:
            col.append('b')

    for i in pos:
        npos=pos[i]
        if i in idom:
            pos[i]=[dd*npos[0],npos[1]+d]
        elif i in doml:
            pos[i]=[dd*npos[0],npos[1]-d]
        else:
            pos[i]=[dd*npos[0],npos[1]-d]

    sstt="Independent Dominating Set" 
    plt.subplot(1,2,2).set_title(sstt)
    nx.draw_networkx_nodes(G,pos=pos, node_color=col)  
    nx.draw_networkx_labels(G,pos,font_color='w')
    nx.draw_networkx_edges(G,pos,edge_color='k',alpha=0.5)
    plt.axis('equal')
    plt.axis('off')
    plt.show()



def draw_domcomms(G,dom,idom,doml,nodoml,d,dd,c,cc,alpha):
    import community 
    from matplotlib.patches import Ellipse
    import random
    import matplotlib
    
    par= community.best_partition(G)
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
    
    col=[]
    for nd in G.nodes():
        if nd in dom:
            col.append('r')
        elif nd in doml:
            col.append('m')
        elif nd in nodoml:
            col.append('c')
        else:
            col.append('b')
    
    ells=[]
    ellc=[]
    colors=[name for name,hex in matplotlib.colors.cnames.iteritems()]
    colors=list(set(colors)-set(['red','blue','green','m','c']))
    for i,v in ninvpar.items():
        xp=[xx[0] for x,xx in v.items()]
        yp=[yy[1] for y,yy in v.items()]

        ells.append(Ellipse(xy=(((-1)**i)*dd+max(xp)/2.,d*i+max(yp)/2.),width=cc*max(xp)/dd,height=c*max(yp)/d))
        colll=random.choice(colors)
        ellc.append(colll)
        colors.remove(colll)
        for j in v:
            npos=v[j]
            pos[j]=[((-1)**par[j])*dd+npos[0],npos[1]+d*par[j]]

    # for i in pos:
    #     npos=pos[i]
    #     pos[i]=[((-1)**par[i])*dd*par[i]+npos[0],npos[1]+d*par[i]]
        # if i in dom:
        #     pos[i]=[dd*npos[0],npos[1]+d]
        # elif i in doml:
        #     pos[i]=[dd*npos[0],npos[1]-d]
        # else:
        #     pos[i]=[dd*npos[0],npos[1]-d]

    fig = plt.figure(figsize=(17,8))
    ncomm=max(par.values())+1
    sstt="Minimum Dominating Set in %s Communities" %ncomm
    plt.subplot(1,2,1).set_title(sstt)
    ax = fig.add_subplot(1,2,1)
    ax.set_title(sstt)
    for i,e in enumerate(ells):
        ax.add_artist(e)
        e.set_clip_box(ax.bbox)
        e.set_alpha(alpha)
        e.set_facecolor(ellc[i])
    nx.draw_networkx_nodes(G,pos=pos, node_color=col) 
    nx.draw_networkx_labels(G,pos,font_color='w')
    nx.draw_networkx_edges(G,pos,edge_color='k',alpha=0.5)
    plt.axis('equal')
    plt.axis('off')

    pos=nx.spring_layout(G)

    col=[]
    for nd in G.nodes():
        if nd in idom:
            col.append('g')
        elif nd in doml:
            col.append('m')
        elif nd in nodoml:
            col.append('c')
        else:
            col.append('b')

    ells=[]
    colors=[name for name,hex in matplotlib.colors.cnames.iteritems()]
    colors=list(set(colors)-set(['red','blue','green','m','c']))
    for i,v in ninvpar.items():
        xp=[xx[0] for x,xx in v.items()]
        yp=[yy[1] for y,yy in v.items()]

        ells.append(Ellipse(xy=(((-1)**i)*dd+max(xp)/2.,d*i+max(yp)/2.),width=cc*max(xp)/dd,height=c*max(yp)/d))
        for j in v:
            npos=v[j]
            pos[j]=[((-1)**par[j])*dd+npos[0],npos[1]+d*par[j]]
    
    sstt="Independent Dominating Set in %s Communities" %ncomm
    plt.subplot(1,2,2).set_title(sstt)
    ax = fig.add_subplot(1,2,2)
    ax.set_title(sstt)
    for i,e in enumerate(ells):
        ax.add_artist(e)
        e.set_clip_box(ax.bbox)
        e.set_alpha(alpha)
        e.set_facecolor(ellc[i])
    nx.draw_networkx_nodes(G,pos=pos, node_color=col)  
    nx.draw_networkx_labels(G,pos,font_color='w')
    nx.draw_networkx_edges(G,pos,edge_color='k',alpha=0.5)
    plt.axis('equal')
    plt.axis('off')
    plt.show()


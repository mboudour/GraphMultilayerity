# import nltk
import re
import networkx as nx
def create_diction_of_actors(path):
    pers_l={}
    fifi=open(path)
    u=0
    while True:
        u+=1
        i=fifi.readline()
        if i=='':
            break
        else:
            i=i.strip()
        # ii=i.split()
        ii=re.split(r'[A-Z]+', i)
        print ii,len(ii)
        if len(ii)>0 and len(ii) <= 2 and i[-1]=='.':
            if i[:-1] not in pers_l:
                pers_l[i[:-1]]=[u]
            else:
                pers_l[i[:-1]].append(u)
    return pers_l

def create_dict_of_acts(path):
    fifi = open(path)
    # fifi = open('/home/sergios-len/Dropbox/Python Projects (1)/LiteratureNetworks/corpora/HamletShakespeare.txt')
    persons = False
    acting=False
    pers_l=[]
    pers_dict={}
    act_dict={}
    lact=[]
    checked=set()
    u=0
    while True:
        u+=1
        i=fifi.readline()
        if i=='':
            break
        else:
            i=i.strip()
        # print i ,u,i.strip(),persons,acting
        # if u>410:
        #     break
        if i=='PERSONS REPRESENTED':
            # print persons
            persons =True
            continue
        if i[:5] == 'ACT I':
            # print acting
            acting=True
            # continue
        if persons and acting :
            # print i,'hehe'
            spers_l=set(pers_l)
            # print i,'hehe',spers_l,checked
            # break
            if i[:3].lower()=='Act'.lower() and i[3] ==' ':

                ikl=i.split()[1][:-1]
                # print i,ikl , u
                if ikl not in act_dict:
                    act_dict[ikl]=u

                    if len(lact)==0:
                        pact=[ikl]
                        lact.append(u)
                    else:
                        pu=lact[-1]
                        ppu=pact[-1]
                        act_dict[ppu]=(pu,u-1)
                        pact.append(ikl)
                        lact.append(u)
                    
            if i[:5]=='Scene':
                continue
                # print i
                # act_dict[ikl][i.split()[1][:-1]]=u
                # lact.append(u)

            if len(i)>=4 :#and len(i)<=8:
                if i[0]!='[' and i[-1]=='.':
                    # print i,'aaaaaaaaaaaaaaaaaaaaaaa'
                    # if i not in pers_dict:
                        # print i
                    i=i[:-1]
                    if i in pers_l:
                        # print i,'bbbbbbbbbbbbb'
                        j=fifi.readline().strip()
                        u+=1
                        while j !='':
                            # j=j.strip()
                            if i not in pers_dict:
                        # for j in set(pers_l) - checked:
                            # print j,i,i[:-1]
                            # if j.find(i[:-1])==0 and j not in checked:
                                pers_dict[i]={u:j}
                                checked.add(j)
                            else:
                                pers_dict[i][u]=j
                            j=fifi.readline().strip()
                            u+=1
                   
        elif persons and len(i)>1 and not acting:
            # print i.split(', ')[0]
            pers_l.append(i.split(', ')[0])
            # spers_l=

        else:
            continue

    fifi.close()

    return act_dict,u,pers_l,pers_dict,pact,lact
# print act_dict
# print pact
# print lact
# print u
# print aaa
def create_per_nod_dict(pers_dict):
    pernode_dict={}
    nodper_dic={}
    for i,v in enumerate(pers_dict.keys()):
        pernode_dict[v]=i
        nodper_dic[i]=v
    return pernode_dict,nodper_dic
def create_graph_dict(act_dict,pers_l,pers_dict,u):
    ract_dic={}
    graph_dic={}
    pernode_dict,nodper_dic=create_per_nod_dict(pers_dict)
    # lact=sorted(lact)
    # print lact
    for k,v in act_dict.items():
        try:
            vv=int(v)
            va=(v,u)
        except:
            va=v
        ract_dic[va]=k
        G=nx.Graph()
        graph_dic[k]=G

    # print ract_dic
    # print graph_dic
    # print aaaa
    sractd=sorted(ract_dic.keys())
    # print sractd

    # G=nx.Graph()
    for k,v in pers_dict.items():
        for kk ,vv in v.items():
            for tok in set(re.split(r'\W+', vv)):
                if tok in pers_dict:
                    # print sractd
                    for act_interv in sractd:
                        # print kk,act_interv
                        if act_interv[0]<=kk and kk<act_interv[1]:
                            G=graph_dic[ract_dic[act_interv]]
                            # print type(G)
                            ed=pernode_dict[k]
                            de=pernode_dict[tok]
                            if G.has_edge(ed,de):
                                wei=G[ed][de]['weight']
                            else:
                                wei=0
                    # print k,'k'
                    # print v,'v'
                    # print kk,'kk'
                    # print vv,'vv'
                    # print tok
                            G.add_edge(ed,de,act=ract_dic[act_interv],weight=wei+1)

    for k,g in graph_dic.items():
        for nd in g.nodes():
            g.add_node(nd,label=nodper_dic[nd])
        g.name='Act %s' %k    
        graph_dic[k]=g


    return graph_dic,ract_dic,pernode_dict,nodper_dic,sractd
# def relabel_graph_nodes(graph_dic,ract_dic):
#     ngraph_dic={}
#     for kk

# act_dict,u,pers_l,pers_dict,pact,lact=create_dict_of_acts('/home/sergios-len/Dropbox/Python Projects (1)/LiteratureNetworks/corpora/HamletShakespeare.txt')

# graph_dic,ract_dic=create_graph_dict(act_dict,pers_l,pers_dict)
# for k,v in graph_dic.items():
    # print k,nx.info(v)
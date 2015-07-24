__author__ = "Moses A. Boudourides & Sergios T. Lenis"
__copyright__ = "Copyright (C) 2015 Moses A. Boudourides & Sergios T. Lenis"
__license__ = "Public Domain"
__version__ = "1.0"

import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms import bipartite
from matplotlib.patches import Ellipse, Polygon
import random
# print
def analyticThreeLayerGraph(n,p,r1,r2,r3,G_isolates=True,maxTries=1500):
	u=0
	while True:
		try:
			G=nx.erdos_renyi_graph(n,p)

			if  G_isolates:
				G.remove_nodes_from(nx.isolates(G))

			layer1 = random.sample(G.nodes(),int(len(G.nodes())*r1))
			nei_layer1=[]
			for i in layer1:
				for j in G.neighbors(i):
					nei_layer1.append(j)


			not_nei_layer1=[i for i in G.nodes() if i not in nei_layer1]
			# print layer1
			# print nei_layer1
			# print not_nei_layer1
			# print aaaa
			# non_nei= set(G.nodes())-s
			layer2 = random.sample(not_nei_layer1,int(len(G.nodes())*r2))

			# layer3 =
			layer3 = list(set(G.nodes())-set(layer1)-set(layer2))

			edgeList =[]#{'layer12':[],'layer23':[],'layer31':[]}


			for e in G.edges():
				# if (e[0] in layer1 and e[1] in layer2) or (e[0] in layer2 and e[1] in layer1):
				# 	edgeList.append(e)
				if (e[0] in layer2 and e[1] in layer3) or (e[0] in layer3 and e[1] in layer2):
					edgeList.append(e)
				if (e[0] in layer3 and e[1] in layer1) or (e[0] in layer1 and e[1] in layer3):
					edgeList.append(e)
			return G, layer1, layer2, layer3, edgeList
			break
		except:
			u+=1
			if u> maxTries:
				break



def plot_graph(G,layer1,layer2,layer3,d1=1.5,d2=5.,d3=0,d4=.8,nodesize=1000,withlabels=True,edgelist=[],layout=True,alpha=0.5):
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
	# print pos
# AYTA EINAI LATHOS. DIORTHWSE TA
	for i in pos:

		npos=pos[i]
		if i in layer1:
			pos[i]=[d2*(npos[0]),d2*(npos[1]+d1)] 
			top_set.add(i)
			left.append(pos[i])
		elif i in layer2:
			pos[i]=[d2*(npos[0]),d2*(npos[1]-d1)] 
			bottom_set.add(i)
			right.append(pos[i])
		else:
			pos[i]=[d2*npos[0],d2*(npos[1])] 
			middle_set.add(i)
			down.append(pos[i])

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

	nx.draw_networkx_nodes(G,pos, nodelist=list(top_set),node_color='r',alpha=0.2,node_size=nodesize)
	nx.draw_networkx_nodes(G,pos, nodelist=list(middle_set),node_color='g',alpha=0.2,node_size=nodesize)
	nx.draw_networkx_nodes(G,pos,nodelist=list(bottom_set),node_color='b',alpha=0.2,node_size=nodesize)
	if withlabels:
		nx.draw_networkx_labels(G,pos)


	# nx.draw(J,pos, with_labels=withlabels,nodelist=list(top_set),node_color='r',node_size=nodesize,edge_color='r',alpha=0.2)
	# nx.draw(FF,pos, with_labels=withlabels,nodelist=list(middle_set),node_color='g',node_size=nodesize,edge_color='g',alpha=0.2)
	# nx.draw(DD,pos, with_labels=withlabels,nodelist=list(bottom_set),node_color='b',node_size=nodesize,edge_color='b',alpha=0.2)
	# # ,alpha=0.2
	# print len(edgelist)
	# edges=list(set(G.edges())-set(edgelist))
	lay1_edges=[ed for ed in G.edges() if ed[0] in layer1 and ed[1] in layer1]
	lay2_edges=[ed for ed in G.edges() if ed[0] in layer2 and ed[1] in layer2]
	lay3_edges=[ed for ed in G.edges() if ed[0] in layer3 and ed[1] in layer3]
	# print lay1_edges
	# print lay2_edges
	# print lay3_edges

	nx.draw_networkx_edges(G,pos,edgelist=lay1_edges,edge_color='r',alpha=0.25)
	nx.draw_networkx_edges(G,pos,edgelist=lay2_edges,edge_color='b',alpha=0.25)
	nx.draw_networkx_edges(G,pos,edgelist=lay3_edges,edge_color='g',alpha=0.25)


	# if len(edgelist)!=0:
	# 	for lay in edgelist:
	
	nx.draw_networkx_edges(G,pos,edgelist=edgelist,edge_color='k',alpha=alpha)
		# nx.draw_networkx_edges(G,pos,edgelist=edgelist,edge_color='k',alpha=0.05)
		# nx.draw_networkx_edges(G,pos,edgelist=edgelist,edge_color='k',alpha=0.05)
	plt.axis('off')
	plt.show()
	# return pos


# n = 150
# p = 0.01
# r1 = 0.333
# r2 = 0.333
# r3 = 0.333
# G, layer1, layer2, layer3, edgeList = analyticThreeLayerGraph(n,p,r1,r2,r3,G_isolates=True)
# print G.nodes()
# print G.edges()
# print layer1
# print layer2
# print layer3
# print edgeList

# plot_graph(G,layer1,layer2,layer3,d1=3.5,d2=5.,nodesize=100,withlabels=False,edgelist=edgeList,alpha=0.1,layout=False)
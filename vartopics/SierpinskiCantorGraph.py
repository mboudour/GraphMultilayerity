__author__ = "Moses A. Boudourides & Sergios T. Lenis"
__copyright__ = "Copyright (C) 2015 Moses A. Boudourides & Sergios T. Lenis"
__license__ = "Public Domain"
__version__ = "1.0"

import networkx as nx
import numpy as np
import matplotlib.pylab as plt

def SierpinskiCantorGraph(a,b,c,k, depth):
	
	a1=a[0]
	a2=a[1]
	b1=b[0]
	b2=b[1]
	c1=c[0]
	c2=c[1]

	ab1 = ((k-1)*a1 + b1)/k                   # (a + b)/k
	ab2 = ((k-1)*a2 + b2)/k
	ba1 = (a1 + (k-1)*b1)/k                   # (a + b) * (k-1)/k
	ba2 = (a2 + (k-1)*b2)/k
	ac1 = ((k-1)*a1 + c1)/k                   # (a + c)/k
	ac2 = ((k-1)*a2 + c2)/k
	ca1 = (a1 + (k-1)*c1)/k                   # (a + c) * (k-1)/k
	ca2 = (a2 + (k-1)*c2)/k
	bc1 = ((k-1)*b1 + c1)/k                   # (k*a + (k-1)*b + c)/k  # (b + c)/k
	bc2 = ((k-1)*b2 + c2)/k
	cb1 = (b1 + (k-1)*c1)/k                   # (k*a + b + (k-1)*c)/k  # (b + c) * (k-1)/k
	cb2 = (b2 + (k-1)*c2)/k

	ab = np.array([ab1,ab2])
	ba = np.array([ba1,ba2])
	bc = np.array([bc1,bc2])
	cb = np.array([cb1,cb2])
	ca = np.array([ca1,ca2])
	ac = np.array([ac1,ac2])

	points = []
	# vertices = []
	# edges = []

	if depth == 0:
		points.extend([a,b,c])
		plt.plot([a[0], b[0], c[0], a[0]], [a[1], b[1], c[1], a[1]], '-o', color='k') 	
		# vertices.extend(range(len(points)))
		# vertices = vertices + range(len(points))	
	elif depth == 1:
		points.extend([a,ab,ba,b,bc,cb,c,ca,ac])
		# vertices.extend(range(len(points)))
		# vertices = range(len(points))
		plt.plot([a[0], ab[0], ac[0], a[0]], [a[1], ab[1], ac[1], a[1]], '-o', color='r',ms=10,lw=2)#ms=20
		plt.plot([b[0], bc[0], ba[0], b[0]], [b[1], bc[1], ba[1], b[1]], '-o', color='g',ms=10,lw=2)
		plt.plot([c[0], ca[0], cb[0], c[0]], [c[1], ca[1], cb[1], c[1]], '-o', color='b',ms=10,lw=2)
		plt.plot([ab[0],ba[0]], [ab[1],ba[1]], '-', color='k',lw=2) 
		plt.plot([bc[0],cb[0]], [bc[1],cb[1]], '-', color='k',lw=2)
		plt.plot([ac[0],ca[0]], [ac[1],ca[1]], '-', color='k',lw=2)		
	else:
		points.extend(SierpinskiCantorGraph(a,ab,ac,k, depth-1))
		points.extend(SierpinskiCantorGraph(b,bc,ba,k, depth-1))
		points.extend(SierpinskiCantorGraph(c,ca,cb,k, depth-1))
		# vertices.extend(range(len(points)))
		# vertices = vertices + range(3*len(points))
		plt.plot([ab[0],ba[0]], [ab[1],ba[1]], '-', color='k') 
		plt.plot([bc[0],cb[0]], [bc[1],cb[1]], '-', color='k')
		plt.plot([ac[0],ca[0]], [ac[1],ca[1]], '-', color='k')
	# print len(points)
	vertices = range(len(points))
	return points, vertices

a = np.array([0, 0])
b = np.array([1, 0])
h = np.sqrt(3)/2.
c = np.array([0.5, h])

k=2.5 #2.2
depth=4
fig, ax = plt.subplots(1,figsize=(20,20)) #40
# fig = plt.figure(figsize=(15,15))
plt.fill([-0.01,0.42,0.42,-0.01],[-0.01,-0.01,0.38,0.38],color='g',alpha=0.15)
plt.plot([-0.01,0.42],[-0.01,-0.01],color='g',lw=4)
plt.plot([0.42,0.42],[-0.01,0.38],color='g',lw=4)
plt.plot([0.42,-0.01],[0.38,0.38],color='g',lw=4)
plt.plot([-0.01,-0.01],[-0.01,0.38],color='g',lw=4)
plt.fill([0.58,1.01,1.01,0.58],[-0.01,-0.01,0.38,0.38],color='b',alpha=0.15)
plt.plot([0.58,1.01],[-0.01,-0.01],color='b',lw=4)
plt.plot([1.01,1.01],[-0.01,0.38],color='b',lw=4)
plt.plot([1.01,0.58],[0.38,0.38],color='b',lw=4)
plt.plot([0.58,0.58],[-0.01,0.38],color='b',lw=4)
plt.fill([0.28,0.72,0.72,0.28],[0.50,0.50,0.88,0.88],color='r',alpha=0.15)
plt.plot([0.28,0.72],[0.50,0.50],color='r',lw=4)
plt.plot([0.72,0.72],[0.50,0.88],color='r',lw=4)
plt.plot([0.72,0.28],[0.88,0.88],color='r',lw=4)
plt.plot([0.28,0.28],[0.88,0.50],color='r',lw=4)
points,vertices=SierpinskiCantorGraph(a,b,c,k,depth)
title_s='A Sierpinski (Cantor-type) Graph with k = %.1f and depth %i' %(k, depth)
plt.title(title_s,{'size': '50'})
# print points
# print len(points)

ax.set_xlim(-0.02,1.02) 
ax.set_ylim(-0.02,1)
# plt.axis('equal')
plt.axis('off')

G = nx.Graph()
G.add_nodes_from(vertices)
# print G.nodes()

plt.show()
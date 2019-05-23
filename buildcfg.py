from __future__ import print_function
import argparse
import sys
from pycparser import c_parser, c_ast, parse_file
from graphviz import Digraph


def main():
	read_dir = sys.argv[1]
	fr_dir = open(read_dir,'r')
	bb = fr_dir.readlines()
	position = []
	node_pos = []
	node_name = []
	node_content = []
	edges = []
	edge = ''
	t = 0
	namelist = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t']
	for i in range(0,len(bb)):
		if 'BB' in bb[i]:
			position.append(i)
	#print(position)
	dot = Digraph(comment='CFG')

	for i in range(0,len(position)-1):
		p1 = i
		p2 = i+1
		name = namelist[t]
		t = t + 1
		content = ''.join(bb[position[p1]+1:position[p2]])
		dot.node(name,content)
		node_pos.append(position[i])
		node_name.append(name)
		node_content.append(content)


	name = namelist[t]
	content = ''.join(bb[position[i+1]+1:])

	dot.node(name,content)
	node_pos.append(position[i])
	node_name.append(name)
	node_content.append(content)

	for i in range(0,len(node_name)-1):
		edges.append(node_name[i] + node_name[i+1])

	#node_pos.append(position[i])
	for i in range(0,len(node_name)):
		if 'goto l' in node_content[i]:
			#for k in range(1,len(node_content[i])):
			label_location = node_content[i].find('goto l')
			#print(node_content[i][label_location+6])
			label = node_content[i][label_location+6]				
			
			for j in range(0,len(node_name)):
				label_des = 'l' + str(label) + ':'
				if label_des in node_content[j]:
					edge = node_name[i] + node_name[j] 
					edges.append(edge)
		if 'goto  l' in node_content[i]:
			#for k in range(1,len(node_content[i])):
			label_location = node_content[i].find('goto  l')
			#print(node_content[i][label_location+6])
			label = node_content[i][label_location+7]				
			
			for j in range(0,len(node_name)):
				label_des = 'l' + str(label) + ':'
				if label_des in node_content[j]:
					edge = node_name[i] + node_name[j] 
					edges.append(edge)			

	print(edges)
	l2 = list(set(edges))
	l2.sort(key=edges.index)
	#print(node_name)
	dot.edges(l2)
	dot.render('output', view=False)	
	print(type(dot))
	#dot.dot()
    
					
	
	#print(dot)

if __name__ == '__main__':
	main()
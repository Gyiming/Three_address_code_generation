from __future__ import print_function
import argparse
import sys
from pycparser import c_parser, c_ast, parse_file
from graphviz import Digraph
import os

global dic
dic = {}

def part(src):
	global dic

	operands = {'+','-','*','/'}
	for k in operands:
		if k in src:
			src1 = src[0:src.find(k)]
			src2 = src[src.find(k)+1:len(src)]
			if 't' not in src:
				if src1 in dic.keys() or src2 in dic.keys():
					return 1
	return 0

def split(src):
	operands = {'+','-','*','/'}
	for k in operands:
		if k in src:
			src1 = src[0:src.find(k)]
			src2 = src[src.find(k)+1:len(src)]
			op = k
	return src1,src2,op


def main():
	global dic
	dir_input = sys.argv[1]
	dir_output = sys.argv[2]
	cmd = 'python gen3ac.py ' + sys.argv[1] + ' gen3ac.c'
	#print(cmd)
	os.system(cmd)
	cmd = 'python genbb.py gen3ac.c output.txt'
	os.system(cmd)
	fr_dir = open('output.txt','r')
	bb = fr_dir.readlines()
	position = []
	node_pos = []
	node_name = []
	node_content = []
	edges = []
	edge = ''
	t = 0
	namelist = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t']
	ops = ['!','<','>']
	number = ['1', '2','3','4','5','6','7','8','9','0']
	modified = []
	#dic = {}
	sig = 0
	operands = 1
	real1 = ''
	real2 = ''
	check = 0
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

	#print(node_content)
	#for each basic block
	for i in range(1,len(node_content)):
		basicblock = node_content[i].split('\n')
		for j in range(0,len(basicblock)):
			
			if '=' in basicblock[j]:
				for k in ops:
					if k in basicblock[j].replace('=',''):
						sig = 1
				if sig == 0:#if this is an equation								
					src = basicblock[j][basicblock[j].find('=')+1:len(basicblock[j])-1]
					dest = basicblock[j][0:basicblock[j].find('=')]

					if src in dic.keys() and 't' not in src:
						src = dic[src]
						dic[dest] = src
						basicblock[j] = dest + '=' + src + ';' + '\n'

					elif part(src) == 1:
						p1,p2,op = split(src)
						if p1 in dic.keys() and p2 in dic.keys():
							basicblock[j] = basicblock[j].replace(p1,dic[p1])
							basicblock[j] = basicblock[j].replace(p2,dic[p2]) + '\n'
						elif p1 in dic.keys() and p2 not in dic.keys():
							basicblock[j] = basicblock[j].replace(p1,dic[p1]) + '\n'
						elif p2 in dic.keys() and p1 not in dic.keys():
							basicblock[j] = basicblock[j].replace(p2,dic[p2]) + '\n'
					else:
						dic[dest] = src.replace(';','')
						basicblock[j] = basicblock[j] + '\n'
				else:
					basicblock[j] = basicblock[j] + '\n'
			else:
				basicblock[j] = basicblock[j] + '\n'


		node_content[i] = ''.join(basicblock)

	result = ''.join(node_content)
	#print(result)
	print(dic)
	fw_dir = open(sys.argv[2],'w')
	fw_dir.write(result)


if __name__ == '__main__':
	main()
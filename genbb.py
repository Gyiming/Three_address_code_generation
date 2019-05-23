from __future__ import print_function
import argparse
import sys
from pycparser import c_parser, c_ast, parse_file



def main():
	bb_position = []
	bbid = 1
	start_label = 3
	fr_dir = sys.argv[1]
	out_dir = sys.argv[2]
	fr_dir = open(fr_dir,'r')
	content = fr_dir.readlines()
	fw_dir = open('tempbb.c','w')
	fw_dir.write('BB000:\n')
	print('BB000:')
	#print(content)
	for i in range(3,len(content)-1):
		'''
		if 'goto' in content[i] : 
			start_label = i

		if ':' in content[i] and 'goto' not in content[i-1]:
			start_label = i


		if i == start_label:
			print('BB'+str(bbid).rjust(3,'0')+':' + '\n')
			fw_dir.write('BB'+str(bbid).rjust(3,'0')+':' + '\n')
			bbid = bbid + 1

		print(content[i])
		fw_dir.write(content[i])

		if 'goto' in content[i] and 'if' not in content[i]:
			print('BB'+str(bbid).rjust(3,'0')+':' + '\n')
			fw_dir.write('BB'+str(bbid).rjust(3,'0')+':' + '\n')
			bbid = bbid + 1		
		'''
		if i==3 and 'l' not in content[i+1]:
			print('BB'+str(bbid).rjust(3,'0')+':' + '\n')
			fw_dir.write('BB'+str(bbid).rjust(3,'0')+':' + '\n')
			bbid = bbid + 1			

		if 'l' in content[i] and ':' in content[i] and 'goto' not in content[i-1]:
			print('BB'+str(bbid).rjust(3,'0')+':' + '\n')
			fw_dir.write('BB'+str(bbid).rjust(3,'0')+':' + '\n')
			bbid = bbid + 1

		print(content[i])
		fw_dir.write(content[i])

		if 'goto' in content[i] and i!= len(content)-2:
			print('BB'+str(bbid).rjust(3,'0')+':' + '\n')
			fw_dir.write('BB'+str(bbid).rjust(3,'0')+':' + '\n')
			bbid = bbid + 1



	
	fw_dir.close()
	read_dir = open('tempbb.c','r')
	read_content = read_dir.readlines()
	#print(read_content)


	final_dir = open(out_dir,'w')
	result = ''.join(read_content)
	final_dir.write(result)
	
	


			
if __name__ == '__main__':
	main()


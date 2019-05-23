from __future__ import print_function
import argparse
import sys
from pycparser import c_parser, c_ast, parse_file

global t 
global l
global fw_dir
global break_
global continue_
t = 0
l = 0

def walk_AST(ast):
	for i in ast.ext:
		if type(i) is c_ast.Decl:
			parse_funcdecl(i)
		else:
			parse_funcdef(i.decl)
			print('{')
			fw_dir.write('{' + '\n')
			for j in i.body.block_items:
				#parse each item in the body
				parse_item(j)
			print('}')
			fw_dir.write('}' + '\n')

def parse_funcdecl(item):
	print(item.type.type.type.names, item.name)


def a3c_decl(item):
	print(item.type.type.names, item.name)
	if 'unsigned' in item.type.type.names:
		vartype = 'unsigned ' + item.type.type.names[1]
	else:
		vartype = ''.join(item.type.type.names)

	fw_dir.write(vartype + ' ' + item.name + ';' + '\n')

def a3c_binary(left,right,op):
	global t
	global fw_dir
	if type(left) == int:
		left = 't' + str(left) 
		t = t + 1
	#print(op)
	if type(right) is int:
		right = 't' + str(right)
	print('t' + str(t) + '=' + left + op + right + ';')
	fw_dir.write('t' + str(t) + '=' + left + op + right + ';' + '\n')
	t = t + 1
	
def a3c_unary(var,op):
	global t
	global fw_dir
	if type(var) is int:
		if (op == 'p++'):
			print('t' + str(var) + '=' + 't' + str(var-1) + '+1' + ';')
			fw_dir.write('t' + str(var) + '=' + 't' + str(var-1) + '+1' + ';' + '\n')
			t = t + 1
		elif (op == 'p--'):
			print('t' + str(var) + '=' + 't' + str(var-1) + '-1' + ';')
			fw_dir.write('t' + str(var) + '=' + 't' + str(var-1) + '-1' + ';' + '\n')
			t = t + 1
		elif (op == '++'):
			print('t' + str(var) + '=' + 't' + str(var-1) + '+1' + ';')
			fw_dir.write('t' + str(var) + '=' + 't' + str(var-1) + '+1' + ';' + '\n')
			t = t + 1
		elif (op == '--'):
			print('t' + str(var) + '=' + 't' + str(var-1) + '-1' + ';')		
			fw_dir.write('t' + str(var) + '=' + 't' + str(var-1) + '-1' + ';' + '\n')	
			t = t + 1
		elif (op == '&'):
			print('t' + str(var) + '=' + '&' + 't' + str(var-1) + ';')
			fw_dir.write('t' + str(var) + '=' + '&' + 't' + str(var-1) + ';' + '\n')
			t = t + 1

	else:
		if (op == 'p++'):
			print('t' + str(t) + '=' + var + '+1' + ';')
			fw_dir.write('t' + str(t) + '=' + var + '+1' + ';' + '\n')
			t = t + 1
		elif (op == 'p--'):
			print('t' + str(t) + '=' + var + '-1' + ';')	
			fw_dir.write('t' + str(t) + '=' + var + '-1' + ';' + '\n')		
			t = t + 1
		elif (op == '++'):
			print('t' + str(t) + '=' + var + '+1' + ';')
			fw_dir.write('t' + str(t) + '=' + var + '+1' + ';' + '\n')
			t = t + 1
		elif (op == '--'):
			print('t' + str(t) + '=' + var + '-1' + ';')
			fw_dir.write('t' + str(t) + '=' + var + '-1' + ';' + '\n')
			t = t + 1
		elif (op == '&'):
			print('t' + str(t) + '=' + '&' + var + ';')
			fw_dir.write('t' + str(t) + '=' + '&' + var + ';' + '\n')
			t = t + 1


def a3c_assign(left,right,op):
	global t
	global fw_dir
	if type(right) is int:
		print(left + '=' + 't' + str(right-1) + ';')
		fw_dir.write(left + '=' + 't' + str(right-1) + ';' + '\n')
		print('t' + str(t) + '='  + left + ';')
		fw_dir.write('t' + str(t) + '='  + left + ';' + '\n')
		t = t + 1
	else:
		print(left + '=' + right + ';')
		fw_dir.write(left + '=' + right + ';' + '\n')
		print('t' + str(t) + '='  + left + ';')
		fw_dir.write('t' + str(t) + '='  + left +  ';' + '\n')
		t = t + 1

def a3c_assignfuncall(left,right):
	global t
	global fw_dir
	args=[]
	func_name = str(right.name.name)

	if right.args is None:
		dest = parse_item(left)
		print(dest + '=' + func_name + '(' + ')' + ';')
		fw_dir.write(dest + '=' + func_name + '(' + ')' + ';' + '\n')
		return

	for i in right.args.exprs:
		if type(i) is c_ast.Constant:
			print('t' + str(t) + '=' + parse_item(i) + ';')
			fw_dir.write('t' + str(t) + '=' + parse_item(i) + ';' + '\n')
			args.append('t' + str(t))
			args.append(',')
			t = t + 1
		elif type(i) is c_ast.ID:
			a = parse_item(i)
			args.append('t' + str(a-1))
			args.append(',')
		else:
			a = parse_item(i)
			args.append('t' + str(a-1))
			args.append(',')
	#print(args)
	arg_str = ''.join(args[0:len(args)-1])
	dest = parse_item(left)
	print(dest + '=' + func_name + '(' + arg_str + ')' + ';')
	fw_dir.write(dest + '=' + func_name + '(' + arg_str + ')' + ';' + '\n')
	print('t' + str(t) + '=' + dest + ';')
	fw_dir.write('t' + str(t) + '=' + dest + ';' + '\n')
	t = t + 1



def parse_item(item):
	global t
	global l
	global fw_dir
	global continue_
	global break_

	# based on the type of the item, decide what to do.
	if type(item) is c_ast.Constant:
		return str(item.value)

	if type(item) is c_ast.ID:
		return item.name

	if type(item) is c_ast.Decl:
		a3c_decl(item)

	if type(item) is c_ast.Assignment:
		if type(item.rvalue) is c_ast.FuncCall:
			a3c_assignfuncall(item.lvalue,item.rvalue)
		else:
			left = parse_item(item.lvalue)
			right = parse_item(item.rvalue)
			a3c_assign(left,right,item.op)

	if type(item) is c_ast.BinaryOp:
		left = parse_item(item.left)
		right = parse_item(item.right)
		a3c_binary(left,right,item.op)
		return t

	if type(item) is c_ast.UnaryOp:
		var = parse_item(item.expr)
		a3c_unary(var, item.op)
		return t

	if type(item) is c_ast.ArrayRef:
		print('t' + str(t) + '=' + item.name.name + '[' + item.subscript.name + ']')
		t = t + 1
		return t

	if type(item) is c_ast.If:
		a = parse_item(item.cond)
		print('if (!t' + str(a-1) + ')' + ' goto l' + str(l) + ';')
		fw_dir.write('if (!t' + str(a-1) + ')' + ' goto l' + str(l) + ';' + '\n')
		false_label = l
		l = l + 1
		true_label = l
		l = l + 1

		if type(item.iftrue) is not c_ast.Continue and type(item.iftrue) is not c_ast.Break:
			if type(item.iftrue) is c_ast.Assignment:
				parse_item(item.iftrue)
			elif type(item.iftrue) is c_ast.FuncCall:
				parse_item(item.iftrue)
			else:
				for i in item.iftrue.block_items:
					parse_item(i)

		else:
			if type(item.iftrue) is c_ast.Continue:
				print('goto ' + 'l' + str(continue_) + ';')
				fw_dir.write('goto ' + 'l' + str(continue_) + ';' + '\n')
			elif type(item.iffalse) is c_ast.Break:
				print('goto ' + 'l' + str(break_) + ';')
				fw_dir.write('goto ' + 'l' + str(break_) + ';' + '\n')

		if item.iffalse is not None:

			print('goto l' + str(true_label) + ';')
			fw_dir.write('goto l' + str(true_label) + ';' + '\n')

		print('l' + str(false_label) + ':')
		fw_dir.write('l' + str(false_label) + ':' + '\n')

		if item.iffalse is None:
			return

		if type(item.iffalse) is c_ast.Continue or type(item.iffalse) is c_ast.Break:
			parse_item(item.iffalse)
		else:
			if type(item.iffalse) is c_ast.If:
				parse_item(item.iffalse)
			else:
				for i in item.iffalse.block_items:
					parse_item(i)

		print('l' + str(true_label) + ':')
		fw_dir.write('l' + str(true_label) + ':' + '\n')



	if type(item) is c_ast.While:
		continue_ = l
		l = l + 1
		break_ = l
		l = l + 1
		#two label, one at the beginning for continue, one at the end for break;
		print('l' + str(continue_) + ':')
		fw_dir.write('l' + str(continue_) + ':' + '\n')
		cond = parse_item(item.cond)
		if type(cond) is str:
			cond = int(cond)
		print('if (!t' + str(cond-1) + ')' +  'goto l' + str(break_) + ';')
		fw_dir.write('if (!t' + str(cond-1) + ')'+ 'goto' + ' l' + str(break_) + ';' + '\n')


		for i in item.stmt.block_items:
			parse_item(i)

		print('l' + str(break_) + ':')
		fw_dir.write('l' + str(break_) + ':' + '\n')


	if type(item) is c_ast.DoWhile:
		continue_ = l
		l = l + 1
		break_ = l
		l = l + 1
		print('l' + str(continue_) + ':')
		fw_dir.write('l' + str(continue_) + ':' + '\n')

		for i in item.stmt.block_items:
			parse_item(i)


		cond = parse_item(item.cond)
		print('if (!t' + str(cond-1) +')' + ' goto' + ' l' + str(break_) + ';')
		fw_dir.write('if (!t' + str(cond-1) +')' + ' goto' + ' l' + str(break_) + ';' + '\n')
		print('goto l' + str(continue_) + ';')
		fw_dir.write('goto l' + str(continue_) + ';' + '\n')


		print('l' + str(break_) + ':')
		fw_dir.write('l' + str(break_) + ':' + '\n')		


	if type(item) is c_ast.For:
		#print(item)
		continue_ = l
		l = l + 1
		break_ = l
		l = l + 1

		print('l' + str(continue_) + ':')
		fw_dir.write('l' + str(continue_) + ':' + '\n')

		parse_item(item.init)
		cond = parse_item(item.cond)

		print('if (!t' + str(cond-1) +')' + ' goto l' + str(break_) + ';')
		fw_dir.write('if (!t' + str(cond-1) + ')'+ ' goto l' + str(break_) + ';' + '\n')

		parse_item(item.next)
		for i in item.stmt.block_items:
			parse_item(i)

		print('l' + str(break_) + ':')
		fw_dir.write('l' + str(break_) + ':' + '\n')


	if type(item) is c_ast.Switch:
		parse_switch(item)

	if type(item) is c_ast.Break:
		print('goto ' + 'l' + str(break_) + ';')
		fw_dir.write('goto ' + 'l' + str(break_) + ';' + '\n')

	if type(item) is c_ast.Continue:
		print('goto ' + 'l' + str(continue_) + ';')
		fw_dir.write('goto ' + 'l' + str(continue_) + ';' + '\n')

	if type(item) is c_ast.FuncCall:
		#print(item)
		func_name = str(item.name.name)
		#print(func_name)
		args = []
		for i in item.args.exprs:
			if type(i) is c_ast.Constant:
				print('t' + str(t) + '=' + parse_item(i) + ';')
				fw_dir.write('t' + str(t) + '=' + parse_item(i) + ';' + '\n')
				args.append('t' + str(t))
				args.append(',')
				t = t + 1
			elif type(i) is c_ast.ID:
				a = parse_item(i)
				args.append(a)
				args.append(',')
			else:
				a = parse_item(i)
				args.append('t' + str(a-1))
				args.append(',')
		#print(args)
		arg_str = ''.join(args[0:len(args)-1])
		print(func_name + '(' + arg_str + ')' + ';')
		fw_dir.write(func_name + '(' + arg_str + ')' + ';' + '\n')
		#print(arg_str)


	if type(item) is c_ast.Return:
		print('return ' + item.expr.name + ';')
		fw_dir.write('return ' + item.expr.name + ';' + '\n')


	if type(item) is c_ast.FuncDecl:
		return

def parse_funcdef(item):
	#parse a function definition 
	global fw_dir
	

	args = []
	var = ''
	func_name = item.name
	func_type = item.type.type.type.names

	#print(func_type)
	if 'unsigned' in func_type:
		typef = 'unsigned ' + func_type[1]
	else:
		typef = ''.join(func_type) 
	


	for i in range(len(item.type.args.params)):
		var_name = item.type.args.params[i].name
		#print(type(item.type.args.params[i].type))
		if type(item.type.args.params[i].type) is c_ast.TypeDecl:
			var_type = item.type.args.params[i].type.type.names
		elif type(item.type.args.params[i].type) is c_ast.PtrDecl:
			var_type = item.type.args.params[i].type.type.type.names

		if 'unsigned' in var_type:
			vtype = 'unsigned ' + var_type[1]
		else:
			vtype = ''.join(var_type)	
		

		if vtype=='void':
			var = 'void '
		else:
			var = var + vtype + ' ' + var_name + ','
	
	print(typef + ' ' + func_name + '(' + var[:-1] + ')')
	fw_dir.write(typef + ' ' + func_name + '(' + var[:-1] + ')' + '\n')
		
	
		
def parse_switch(item):
	#parse a switch

	global fw_dir
	global t
	global l
	case_end = l
	condId = item.cond.name

	for i in item.stmt.block_items:
		if type(i) is c_ast.Case:
			comp = i.expr.value
			print('t' + str(t) + '=' + condId + '-' + comp)
			t = t + 1
			print('if (!t' + str(t-1) + ')' + ' goto l' + str(case_end) + ';')
			fw_dir.write('if (!t' + str(t-1) + ')' + ' goto l' + str(case_end) + ';' + '\n')
			for j in i.stmts:
				if type(j) is c_ast.Break:
					print('goto l' + str(case_end) + ';')
					fw_dir.write('goto l' + str(case_end) + ';' + '\n')
				else:
					parse_item(j)

		elif type(i) is c_ast.Default:
			for j in i.stmts:
				if type(j) is c_ast.Break:
					print('goto l' + str(case_end) + ';')
					fw_dir.write('goto l' + str(case_end) + ';' + '\n')
				else:
					parse_item(j)

	print('l'+str(case_end) + ':')
	fw_dir.write('l'+str(case_end) + ':'+'\n')


	

def main():

	global t
	global l
	global fw_dir


	input_dir = sys.argv[1]
	output_dir = sys.argv[2]
	ast = parse_file(input_dir, use_cpp=True)
	#clear the old file
	fw_dir = open('temp.c','w')
	fw_dir.write('')
	fw_dir.close()

	#write into new file

	fw_dir = open('temp.c','a')
	#walk throught the AST
	walk_AST(ast)
	
	fw_dir.close()

	read_dir = open('temp.c','r')
	content = read_dir.readlines()

	t_list=['int ']
	for i in range(0,t):
		t_list.append('t' + str(i) + ',')
	tp = ''.join(t_list)

	content.insert(2,tp[:-1]+';' + '\n')
	if 'l' in content[-2] and ':' in content[-2]:
		content.insert(-1,'return;\n')
	result = ''.join(content)
	write_to_ = open(output_dir,'w')
	write_to_.write(result)



if __name__ == '__main__':
	main()

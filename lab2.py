
import argparse
from optparse import OptionParser
import sys
from collections import defaultdict 


syntax_array = ["loadI", "load", "store", "add", "sub", "mult", "lshift", "rshift", "output", "nop", "," , "=>","r", "int", "EOF", "new_line", "error"]
#syntax_dict = ["load", "store", "loadI", "add", "sub", "mult", "lshift", "rshift", "output", "nop", "r", "," , "=>", "int", "EOF"]
errors_found = False

#Node class
class Node: 
	def __init__(self, data): 
		self.data = data 
		self.next = None
		self.prev = None

#Double Linked List class
class DoubleLinkedList: 

	def __init__(self): 
		self.head = None
		self.last = None
	
	def appendNode(self, new_data): 

		new_node = Node(new_data)  
		new_node.next = None
		if self.head is None: 
			new_node.prev = None
			self.head = new_node 
			return
		last = self.head 
		while(last.next is not None): 
			last = last.next

		last.next = new_node 
		new_node.prev = last 
		self.last = new_node

		return




	# Adding a node at the front of the list 
	def push(self, new_data): 
	  
		# 1 & 2: Allocate the Node & Put in the data 
		new_node = Node(data = new_data) 
	  
		# 3. Make next of new node as head and previous as NULL 
		new_node.next = self.head 
		new_node.prev = None
	  
		# 4. change prev of head node to new node  
		if self.head is not None: 
			self.head.prev = new_node 
	  
		# 5. move the head to point to the new node 
		self.head = new_node 
		return 
	def insertAfter(self, prev_node, new_data): 
  
		if prev_node is None: 
			print("This node doesn't exist in DLL") 
			return
  
		#2. allocate node  & 3. put in the data 
		new_node = Node(data = new_data) 
  
		# 4. Make next of new node as next of prev_node 
		new_node.next = prev_node.next
  
		# 5. Make the next of prev_node as new_node  
		prev_node.next = new_node 
  
		# 6. Make prev_node as previous of new_node 
		new_node.prev = prev_node 
  
		# 7. Change previous of new_node's next node */ 
		if new_node.next is not None: 
			new_node.next.prev = new_node 
		return

	def printListContents(self, node): 

		print "\n"
		while(node is not None): 
			print(node.data)
			last = node 
			node = node.next
		return


ir_list = DoubleLinkedList() 



def test_func():
  
	a_list = DoubleLinkedList() 
	a_list.appendNode(6) 
	a_list.pushNode(7) 
	llist.pushNode(1) 
	a_list.appendNode(4) 
	a_list.insertNode(llist.head.next, 8) 

	print "Created DLL is: ", 
	a_list.printListContents(llist.head) 
	return

def present_category(line_num, category, non_op_string=None):
	if category == 0:
		print('%d: < LOADI    , "%s" >' % (line_num, syntax_array[category]))
	elif category < 3:
		print('%d: < MEMOP    , "%s" >' % (line_num, syntax_array[category]))
	elif category < 8:
		print('%d: < ARITHOP  , "%s" >' % (line_num, syntax_array[category]))
	elif category == 8:
		print('%d: < OUTPUT   , "%s" >' % (line_num, syntax_array[category]))
	elif category == 9:
		print('%d: < NOP      , "%s" >' % (line_num, syntax_array[category]))
	elif category == 10:
		print('%d: < COMMA    , "%s" >' % (line_num, syntax_array[category]))
	elif category == 11:
		print('%d: < INTO     , "%s" >' % (line_num, syntax_array[category]))
	elif category == 12:
		print('%d: < REG      , "%s" >' % (line_num, non_op_string))
	elif category == 13:
		print('%d: < CONST    , "%s" >' % (line_num, non_op_string))
	else:
		print('%d: < ENDFILE  , "%s" >' % (line_num, ""))


def finish_loadi(line, line_num, opcode, ir=False):
	# index 1 = opcode
	# index 2 = constant
	#index  10= target register
	loadi_list = ["-"] * 14
	errors = True;
	loadi_list[0] = line_num
	loadi_list[1] = "loadI"

	found_lexemes = 0
	str_index = 0
	while(str_index < len(line)):
		#while("/n" not in line[str_index:str_index + 2] and "/r/n" not in line[str_index:str_index + 4]):
		#if line is commented skip line
		if line[str_index:str_index + 2] == "//":
			#print message about word part required that
			if found_lexemes == 0:
				sys.stderr.write("%d: Missing constant in loadI \n" % line_num) 
			elif found_lexemes == 1:
				sys.stderr.write("%d: Missing INTO symbol in loadI \n" % line_num) 
			elif found_lexemes == 2:
				sys.stderr.write("%d: Missing target register in loadI \n" % line_num)
			break

		#check for white space and skip to next character if so
		if line[str_index].isspace():
			str_index += 1
			if str_index == len(line):
				if found_lexemes == 0:
					sys.stderr.write("%d: Missing constant in loadI. \n" % line_num) 
				elif found_lexemes == 1:
					sys.stderr.write("%d: Missing INTO symbol in loadI. \n" % line_num) 
				elif found_lexemes == 2:
					sys.stderr.write("%d: Missing target register in loadI. \n" % line_num)
			continue
		#if not white space, detect category, iterate through higher indices of syntax_dict for matching lexeme
		else:
			lexeme, scan_index, token = scan_for_parser(line_num, line[str_index:], 10)
			str_index = str_index + scan_index 
			#ensure that next lexeme of line is acceptable for grammar
			#next lexeme must be a constant
			if found_lexemes == 0:
				if lexeme != 13:
					sys.stderr.write("%d: Missing constant in loadI \n" % line_num) 
					break
				#increment found_lexemes to include the newly found lexeme
				found_lexemes += 1
				loadi_list[2] = int(token)
				continue
			#next lexeme must be an into symbol
			elif found_lexemes == 1:
				if lexeme != 11:
					sys.stderr.write("%d: Missing INTO symbol in loadI \n" % line_num) 
					break
				found_lexemes += 1
				continue
			#next lexeme must be a register
			elif found_lexemes == 2:
				if lexeme != 12:
					sys.stderr.write("%d: Missing target register in loadI \n" % line_num)
					break
				found_lexemes += 1
				loadi_list[10] = int(token[1:])
				errors = False
				continue
			#if line ends early without completing the grammar
			elif lexeme == 15 and found_lexemes < 3:
				#print message about word part required that is missing
				if found_lexemes == 0:
					sys.stderr.write("%d: Missing constant in loadI. \n" % line_num) 
				elif found_lexemes == 1:
					sys.stderr.write("%d: Missing INTO symbol in loadI. \n" % line_num) 
				elif found_lexemes == 2:
					sys.stderr.write("%d: Missing target register in loadI. \n" % line_num)
				errors = True
			else:
				#any remaining lexemes must be either a new line character or the end of the file
				if lexeme < 14:
					sys.stderr.write("%d: Excessive lexemes in loadI \n" % line_num) 
					errors = True		

			break
	#print ir representation
	if ir and not errors:
		#print(" %s  [ val %d ], [ ], [ sr%d ]" % (loadi_list[1], loadi_list[2], loadi_list[10]))
		ir_list.appendNode(loadi_list)
	if ir and errors:
		print("Due to syntax errors, run terminates.")

	return

def finish_memop(line, line_num, opcode, ir=False):
	# index 1 = opcode
	# index 2 = source register
	#index  10= target register

	memop_list = ["-"] * 14
	errors = True;
	memop_list[0] = line_num
	memop_list[1] = opcode

	found_lexemes = 0
	str_index = 0
	while(str_index < len(line)):
		#while("/n" not in line[str_index:str_index + 2] and "/r/n" not in line[str_index:str_index + 4]):
		#if line is commented skip line
		if line[str_index:str_index + 2] == "//":
			#print message about word part required that
			if found_lexemes == 0:
				sys.stderr.write("%d: Missing source register in load or store. \n" % line_num) 
			elif found_lexemes == 1:
				sys.stderr.write("%d: Missing INTO symbol in load or store. \n" % line_num) 
			elif found_lexemes == 2:
				sys.stderr.write("%d: Missing target register in load or store. \n" % line_num)
			break

		#check for white space and skip to next character if so
		if line[str_index].isspace():
			str_index += 1
			if str_index == len(line):
				if found_lexemes == 0:
					sys.stderr.write("%d: Missing source register in load or store. \n" % line_num) 
				elif found_lexemes == 1:
					sys.stderr.write("%d: Missing INTO symbol in load or store. \n" % line_num) 
				elif found_lexemes == 2:
					sys.stderr.write("%d: Missing target register in load or store. \n" % line_num)
				
			continue

		#if not white space, detect category, iterate through higher indices of syntax_dict for matching lexeme
		else:
			lexeme, scan_index, token = scan_for_parser(line_num, line[str_index:], 10)
			str_index = str_index + scan_index 
			#ensure that next lexeme of line is acceptable for grammar
			#next lexeme must be a register
			if found_lexemes == 0:
				if lexeme != 12:
					sys.stderr.write("%d: Missing source register in load or store. \n" % line_num)
					break
				#increment found_lexemes to include the newly found lexeme
				found_lexemes += 1
				memop_list[2] = int(token[1:])
				continue
			#next lexeme must be an into symbol
			elif found_lexemes == 1:
				if lexeme != 11:
					sys.stderr.write("%d: Missing INTO symbol in load or store. \n" % line_num) 
					break
				found_lexemes += 1
				continue
			#next lexeme must be a register
			elif found_lexemes == 2:
				if lexeme != 12:
					sys.stderr.write("%d: Missing target register in load or store. \n" % line_num)
					break
				found_lexemes += 1
				memop_list[10] = int(token[1:])
				errors = False
				continue
			#if line ends early without completing the grammar
			elif lexeme == 15 and found_lexemes < 3:
				#print message about word part required that is missing
				if found_lexemes == 0:
					sys.stderr.write("%d: Missing source register in load or store. \n" % line_num) 
				elif found_lexemes == 1:
					sys.stderr.write("%d: Missing INTO symbol in load or store. \n" % line_num) 
				elif found_lexemes == 2:
					sys.stderr.write("%d: Missing target register in load or store. \n" % line_num)
				errors = True
			#any remaining lexemes must be either a new line character or the end of the file
			else:
				if lexeme < 14:
					sys.stderr.write("%d: Excessive lexemes in load or store. \n" % line_num) 
					errors = True

			break
	#print ir representation
	if ir and not errors:
		#print(" %s [ sr%d ], [ ], [ sr%d ]" % (memop_list[1], memop_list[2], memop_list[10]))
		ir_list.appendNode(memop_list)
	if ir and errors:
		print("Due to syntax errors, run terminates.")

	return

def finish_arithop(line, line_num, opcode, ir=False):
	# index 1 = opcode
	# index 2 = initial source register
	# index 6 = second source register
	#index  10= target register
	arithop_list = ["-"] * 14
	errors = True;
	arithop_list[0] = line_num
	arithop_list[1] = opcode

	found_lexemes = 0
	str_index = 0
	while(str_index < len(line)):
		#while("/n" not in line[str_index:str_index + 2] and "/r/n" not in line[str_index:str_index + 4]):
		#if line is commented skip line
		if line[str_index:str_index + 2] == "//":
			#print message about word part required that
			if found_lexemes == 0:
				sys.stderr.write("%d: Missing initial source register in arithop. \n" % line_num) 
			if found_lexemes == 1:
				sys.stderr.write("%d: Missing comma in arithop. \n" % line_num) 
			if found_lexemes == 2:
				sys.stderr.write("%d: Missing second source register in arithop. \n" % line_num) 
			elif found_lexemes == 3:
				sys.stderr.write("%d: Missing INTO symbol in arithop. \n" % line_num) 
			elif found_lexemes == 4:
				sys.stderr.write("%d: Missing target register in arithop. \n" % line_num)
			break

		#check for white space and skip to next character if so
		if line[str_index].isspace():
			str_index += 1
			if str_index == len(line):
				if found_lexemes == 0:
					sys.stderr.write("%d: Missing initial source register in arithop. \n" % line_num) 
				if found_lexemes == 1:
					sys.stderr.write("%d: Missing comma in arithop. \n" % line_num) 
				if found_lexemes == 2:
					sys.stderr.write("%d: Missing second source register in arithop. \n" % line_num) 
				elif found_lexemes == 3:
					sys.stderr.write("%d: Missing INTO symbol in arithop. \n" % line_num) 
				elif found_lexemes == 4:
					sys.stderr.write("%d: Missing target register in arithop. \n" % line_num)

			continue
		#if not white space, detect category, iterate through higher indices of syntax_dict for matching lexeme
		else:
			lexeme, scan_index, token = scan_for_parser(line_num, line[str_index:], 10)
			str_index = str_index + scan_index 
			#ensure that next lexeme of line is acceptable for grammar
			#next lexeme must be a register
			if found_lexemes == 0:
				if lexeme != 12:
					sys.stderr.write("%d: Missing initial source register in arithop. \n" % line_num)
					break
				#increment found_lexemes to include the newly found lexeme
				found_lexemes += 1
				arithop_list[2] = int(token[1:])
				continue
			elif found_lexemes == 1:
				if lexeme != 10:
					sys.stderr.write("%d: Missing comma in arithop. \n" % line_num)
					break
				#increment found_lexemes to include the newly found lexeme
				found_lexemes += 1
				continue
			#next lexeme must be a register
			elif found_lexemes == 2:
				if lexeme != 12:
					sys.stderr.write("%d: Missing second source register in arithop. \n" % line_num)
					break
				#increment found_lexemes to include the newly found lexeme
				found_lexemes += 1
				arithop_list[6] = int(token[1:])
				continue
			#next lexeme must be an into symbol
			elif found_lexemes == 3:
				if lexeme != 11:
					sys.stderr.write("%d: Missing INTO symbol in arithop. \n" % line_num) 
					break
				found_lexemes += 1
				continue
			#next lexeme must be a register
			elif found_lexemes == 4:
				if lexeme != 12:
					sys.stderr.write("%d: Missing target register in arithop. \n" % line_num)
					break
				found_lexemes += 1
				arithop_list[10] = int(token[1:])
				errors = False
				continue
			#if line ends early without completing the grammar
			elif lexeme == 15 and found_lexemes < 5:
				#print message about word part required that is missing
				if found_lexemes == 0:
					sys.stderr.write("%d: Missing initial source register in arithop. \n" % line_num) 
				if found_lexemes == 1:
					sys.stderr.write("%d: Missing comma in arithop. \n" % line_num) 
				if found_lexemes == 2:
					sys.stderr.write("%d: Missing second source register in arithop. \n" % line_num) 
				elif found_lexemes == 3:
					sys.stderr.write("%d: Missing INTO symbol in arithop. \n" % line_num) 
				elif found_lexemes == 4:
					sys.stderr.write("%d: Missing target register in arithop. \n" % line_num)
				errors = True
			#any remaining lexemes must be either a new line character or the end of the file
			else:
				if lexeme < 14:
					sys.stderr.write("%d: Excessive lexemes in arithop. \n" % line_num) 
					errors = True;

			break

	#print ir representation
	if ir and not errors:
		#print(" %s [ sr%d ], [ sr%d ], [ sr%d ]" % (arithop_list[1], arithop_list[2], arithop_list[6], arithop_list[10]))
		ir_list.appendNode(arithop_list)
	if ir and errors:
		print("Due to syntax errors, run terminates.")
	return

def finish_output(line, line_num, opcode, ir=False):
	# index 1 = opcode
	# index 2 = constant
	output_list = ["-"] * 14
	errors = True;
	output_list[0] = line_num
	output_list[1] = opcode



	found_lexemes = 0
	str_index = 0
	while(str_index < len(line)):
		#while("/n" not in line[str_index:str_index + 2] and "/r/n" not in line[str_index:str_index + 4]):
		#if line is commented skip line
		if line[str_index:str_index + 2] == "//":
			#print message about word part required that
			if found_lexemes == 0:
				sys.stderr.write("%d: Missing constant in output. \n" % line_num) 
			break

		#check for white space and skip to next character if so
		if line[str_index].isspace():
			str_index += 1
			if str_index == len(line):
				if found_lexemes == 0:
					sys.stderr.write("%d: Missing constant in output. \n" % line_num) 
			continue
		#if not white space, detect category, iterate through higher indices of syntax_dict for matching lexeme
		else:
			lexeme, scan_index, token = scan_for_parser(line_num, line[str_index:], 10)
			str_index = str_index + scan_index 
			#ensure that next lexeme of line is acceptable for grammar
			#next lexeme must be a constant
			if found_lexemes == 0:
				if lexeme != 13:
					sys.stderr.write("%d: Missing constant in output. \n" % line_num) 
					errors = True
					break
				#increment found_lexemes to include the newly found lexeme
				found_lexemes += 1
				output_list[2] = int(token)
				errors = False
				continue
			else:
				#any remaining lexemes must be either a new line character or the end of the file
				if lexeme < 14:
					sys.stderr.write("%d: Excessive lexemes in output. \n" % line_num) 
					errors = True

			break
	#print ir representation
	if ir and not errors:
		#print(" %s [ val %d ], [ ], [ ]" % (output_list[1], output_list[2]))
		ir_list.appendNode(output_list)

	if ir and errors:
		print("Due to syntax errors, run terminates.")
	return

def finish_nop(line, line_num, opcode, ir=False):
	# index 1 = opcode
	# index 2 = constant
	nop_list = ["-"] * 14
	errors = False;
	nop_list[0] = line_num
	nop_list[1] = opcode


	found_lexemes = 0
	str_index = 0
	while(str_index < len(line)):
		#while("/n" not in line[str_index:str_index + 2] and "/r/n" not in line[str_index:str_index + 4]):
		#if line is commented skip line
		if line[str_index:str_index + 2] == "//":
			break

		#check for white space and skip to next character if so
		if line[str_index].isspace():
			str_index += 1
			continue
		#if not white space, detect category, iterate through higher indices of syntax_dict for matching lexeme
		else:
			lexeme, scan_index, token = scan_for_parser(line_num, line[str_index:], 10)
			str_index = str_index + scan_index 
			if lexeme < 14:
				sys.stderr.write("%d: Excessive lexemes in nop. \n" % line_num) 
				errors = True
				break
	#print ir representation
	if ir and not errors:
		#print(" %s [ ], [ ], [ ]" % nop_list[1])
		ir_list.appendNode(nop_list)
	if ir and errors:
		print("Due to syntax errors, run terminates.")
	
	return

def parse_file(file):
	'''
	inputs: filename
	Effects:
	Prints out parsing details, including errors and line number for error if parsing is unsuccessful
	'''
	line_num = 1

	while 1: 
		
		# read from provided file line by line
		line = file.readline() 
		str_index = 0        
		if not line: 
			#if at end of file say so 
			#present_category(line_num - 1, 14) 
			break

		#if line is commented skip line
		if line[str_index:str_index + 2] == "//":
			line_num += 1
			continue
			#print("Line %d is commented out" % line_num)
		#if line not commented begin evaluation
		#then iterate until end of line

		else:      
			while(str_index < len(line)):
				#while("/n" not in line[str_index:str_index + 2] and "/r/n" not in line[str_index:str_index + 4]):
				#if line is commented skip line
				if line[str_index:str_index + 2] == "//":
					#print("Line %d is commented out" % line_num)
					break
				#let sar = syntax_array_index abbreviation
				sar = 0
				
				#check for white space
				if line[str_index].isspace():
					str_index += 1
					continue
				#if not white space, detect category, iterate through syntax_dict for matching lexeme
				else:
					lexeme, scan_index, token = scan_for_parser(line_num, line[str_index:], 0)
					str_index = str_index + scan_index 
					#ensure that beginning lexeme of line is acceptable for grammar
					#parse the rest of the line respective to first lexeme
					if lexeme < 10:
						if lexeme == 0:
							finish_loadi(line[str_index:], line_num, token)
						elif lexeme < 3:
							finish_memop(line[str_index:], line_num, token)
						elif lexeme < 8:
							finish_arithop(line[str_index:], line_num, token)
						elif lexeme == 8:
							finish_output(line[str_index:], line_num, token)
						elif lexeme == 9:
							finish_nop(line[str_index:], line_num, token)
						#exit and return error if the first lexeme is not appropriate for the grammar
						else:
							sys.stderr.write("%d: ILOC sentence must begin with a LOADI, MEMOP, ARITHOP, OUTPUT, or NOP lexeme. Operation starts with an invalid opcode. \n" % line_num)
					#evaluate the rest of the line in the appropriate subfunction
					break


					

			line_num += 1
					


	return
def create_ir(file):
	'''
	inputs: filename
	Effects:
	Prints out parsing details, including errors and line number for error if parsing is unsuccessful
	'''
	line_num = 1

	while 1: 
		
		# read from provided file line by line
		line = file.readline() 
		str_index = 0        
		if not line: 
			#if at end of file say so 
			#present_category(line_num - 1, 14) 
			break

		#if line is commented skip line
		if line[str_index:str_index + 2] == "//":
			line_num += 1
			continue
			#print("Line %d is commented out" % line_num)
		#if line not commented begin evaluation
		#then iterate until end of line

		else:      
			while(str_index < len(line)):
				#while("/n" not in line[str_index:str_index + 2] and "/r/n" not in line[str_index:str_index + 4]):
				#if line is commented skip line
				if line[str_index:str_index + 2] == "//":
					#print("Line %d is commented out" % line_num)
					break
				#let sar = syntax_array_index abbreviation
				sar = 0
				
				#check for white space
				if line[str_index].isspace():
					str_index += 1
					continue
				#if not white space, detect category, iterate through syntax_dict for matching lexeme
				else:
					lexeme, scan_index, token = scan_for_parser(line_num, line[str_index:], 0)
					str_index = str_index + scan_index 
					#ensure that beginning lexeme of line is acceptable for grammar
					#parse the rest of the line respective to first lexeme
					if lexeme < 10:
						if lexeme == 0:
							finish_loadi(line[str_index:], line_num, token, ir=True)
						elif lexeme < 3:
							finish_memop(line[str_index:], line_num, token, ir=True)
						elif lexeme < 8:
							finish_arithop(line[str_index:], line_num, token, ir=True)
						elif lexeme == 8:
							finish_output(line[str_index:], line_num, token, ir=True)
						elif lexeme == 9:
							finish_nop(line[str_index:], line_num, token, ir=True)
						#exit and return error if the first lexeme is not appropriate for the grammar
						else:
							sys.stderr.write("%d: ILOC sentence must begin with a LOADI, MEMOP, ARITHOP, OUTPUT, or NOP lexeme. Operation starts with an invalid opcode. \n" % line_num)
					#evaluate the rest of the line in the appropriate subfunction
					break


					

			line_num += 1
					
	#ir_list.printListContents(ir_list.head) 

	return
def def_value(): 
	return "-"

def rename_registers(file):
	'''
	Inputs: filename
	Effects:
	Prints out the original file with source registers reassigned to virtual registers
	'''
	#sr_to_vr dict
	create_ir(file)
	sr= defaultdict(def_value)
	lu = defaultdict(def_value)
	vr = 0
	live = 0
	max_live = 0


	curr = ir_list.last
	
	while (curr != None) :
		
		#skip this process for nops
		if curr.data[1] not in ["nop", "output"]:
			#print("line num is ", curr.data[0])

			#for last region of source registers
			if curr.data[1] not in []:



				#if source register use not previously defined, define it  
				if sr[curr.data[10]] == "-":		
					sr[curr.data[10]] = vr
					vr += 1
					#keep track of maxlive value
					live += 1
					if live > max_live:
						max_live = live
				#pair virtual register with sr in logs
				curr.data[11] = sr[curr.data[10]]
				#update next use logs
				curr.data[13] = lu[curr.data[10]] 
				#kill register
				if curr.data[1] != "store":
					lu[curr.data[10]] = "-"
					sr[curr.data[10]] = "-"
					#keep track of maxlive value
					live -= 1

			#for first region of source registers
			if curr.data[1] not in ["loadI"]:

				#if source register use not previously defined, define it  
				if sr[curr.data[2]] == "-":		
					sr[curr.data[2]] = vr
					vr += 1
					live += 1
					if live > max_live:
						max_live = live
				#update next use logs
				curr.data[5] = lu[curr.data[2]] 
				'''
				#update max live value
				if curr.data[5] == "-":
					live -= 1
				'''

				#pair virtual register with sr in logs
				curr.data[3] = sr[curr.data[2]]
				lu[curr.data[2]] = curr.data[0]
			#for second region of source registers
			if curr.data[1] not in ["load", "loadI", "store"]:
				#if source register use not previously defined, define it 
				if sr[curr.data[6]] == "-":		
					sr[curr.data[6]] = vr
					vr += 1
					live += 1
					if live > max_live:
						max_live = live
				#update next use logs
				curr.data[9] = lu[curr.data[6]]
				''' 
				#update max live value
				if curr.data[9] == "-":
					live -= 1
				'''
				#pair virtual register with sr in logs
				curr.data[7] = sr[curr.data[6]]
				lu[curr.data[6]] = curr.data[0]
		#print("live amount at end of op line %s is: %d ", (curr.data[0], curr.data[1], live))
		curr = curr.prev
	#print("max live was " , max_live)
	#ir_list.printListContents(ir_list.head);
	#print_renamed_registers()

	max_live = 0;
	return max_live, lu, sr


def allocate_easy(reg, file):

	reg_stack = []
	
	#just for testing purposes
	#print("reg " , reg)
	#max_live = int(reg) - 1
	#k = int(reg) - 1
	#dict of next uses for registers (perhaps redundant, could be more efficient) 
	#prnu = defaultdict(def_value)
	#spill_loc = defaultdict(def_value)

	#finishing testing purposes
	print("inside allocate easy")

	#vr should be initialized to be inverse of sr dict
	vr2 = defaultdict(def_value)
	#dict of vr to pr
	pr2 = defaultdict(def_value)
	#loc = 32768

	k = int(reg)
	
	max_live, lu, sr = rename_registers(file)
	print("max_live is " , max_live)
	#initialize physical register stack
	i = 0;
	while i < int(k) - 1 :
		reg_stack.append(i)
		i += 1


	#iterate through opcodes
	curr = ir_list.head
	while (curr != None) :
		#print("curr " + curr)
		#skip this process for nops
		if curr.data[1] not in ["nop", "output"]:
		

			#for first region of source registers
			if curr.data[1] not in ["loadI"]:
				vr = curr.data[3]
				#if pr already  assigned use it
				if vr2[vr] != "-":
					pr = vr2[vr]
					curr.data[4] = pr
				#get a pr and restore use value
				else:
					print("1: enough registers: shouldn't enter the condition where spilling needed ")
				
				#check whether use is last use instance
				'''
				if curr.data[5] == "-":
					#free physical register
					vr2[vr] = "-"
					pr2[pr] = "-"
					#add freed register to stack
					reg_stack.append(pr)
				'''
				#mark next use of physical register in mapping
				#prnu[pr] = curr.data[5] 
				for vra, pra in vr2.items():
					prb = vr2[vra]
					#if pr2[prb] != pra:
					'''
					if pr2[pra] != vra:
						print("3: vr2pr : %s, %s" % (vra, pra))
						print("3: pr2vr : %s, %s" % (pra, pr2[pra]))
						print("We have found a MISMATCHED dictionary at : " , curr.data)
					'''

			#for second region of source registers
			if curr.data[1] not in ["load", "loadI", "store"]:
				pr0 = pr
				vr = curr.data[7]
				#if pr already  assigned use it
				if vr2[vr] != "-":
					pr = vr2[vr]
					curr.data[8] = pr
				#get a pr and restore use value
				else:
					print("2: enough registers: shouldn't enter the condition where spilling needed ")
					#if pr2[prb] != pra:
					''''
					if pr2[pra] != vra:
						print("3: vr2pr : %s, %s" % (vra, pra))
						print("3: pr2vr : %s, %s" % (pra, pr2[pra]))
						print("We have found a MISMATCHED dictionary at : " , curr.data)
					'''
			#check whether uses were last uses in regions two and three
			
			if curr.data[5] == "-" and vr2[curr.data[3]]!= "-":
				#free physical register
				vr2[curr.data[3]] = "-"
				pr2[curr.data[4]] = "-"
				#add freed register to stack
				reg_stack.append(pr)
			if curr.data[9] == "-" and vr2[curr.data[7]]!= "-":
					#free physical register
					vr2[curr.data[7]] = "-"
					pr2[curr.data[8]] = "-"
					#add freed register to stack
					reg_stack.append(pr)
			
			#for last region of source registers
			if curr.data[1] not in []:
				vr = curr.data[11]
				#if pr already  assigned use it
				if vr2[vr] != "-":
					pr = vr2[vr]
					curr.data[12] = pr
					#sanity check
					if pr2[pr] != vr:
						print("equivalency fail 1")
				#get a pr and restore use value
				else:
					#if pr available use it
					if reg_stack:
						pr = reg_stack.pop()				
					#otherwise spill value to attain pr
					else:
						print("3: enough registers: shouldn't enter the condition where spilling needed ")

					curr.data[12] = pr
					#update prvr mappings
					#print("vr is: ", vr)
					vr2[vr] = pr
					pr2[pr] = vr
					#print("first Line check")
					#print("vr2 at 0 :", vr2[0])
					#print("pr2 at 2 :", pr2[2])
					#sanity check
					if pr2[pr] != vr:
						print("equivalency fail 2a")
					if vr2[vr] != pr:
						print("equivalency fail 2b")
				#check whether use is last use instance
				'''
				if curr.data[13] == "-":
					#free physical register
					vr2[vr] = "-"
					pr2[pr] = "-"
					#add freed register to stack
					reg_stack.append(pr)
				'''
				
		
		


		curr = curr.next
	#print("this is the final ir allowing for physical register placement")
	#ir_list.printListContents(ir_list.head)  
	print_reallocated_registers()      
	return 


def allocate_registers(reg, file):
	
	reg_stack = []
	
	#just for testing purposes
	#print("reg " , reg)
	#max_live = int(reg) - 1

	#k = int(reg) - 1
	#dict of next uses for registers (perhaps redundant, could be more efficient) 
	prnu = defaultdict(def_value)
	spill_loc = defaultdict(def_value)
	max_live, lu, sr = rename_registers(file)
	#finishing testing purposes
	#print("max_live start is  " , max_live)

	#vr should be initialized to be inverse of sr dict
	vr2 = defaultdict(def_value)
	#dict of vr to pr
	pr2 = defaultdict(def_value)
	loc = 32768

	k = int(reg) - 1
	'''
	k = int(reg)
	#reserve one register for spill locations
	if max_live > reg:
		k = int(reg) - 1
		#dict of next uses for registers (perhaps redundant, could be more efficient) 
		prnu = defaultdict(def_value)
		spill_loc = defaultdict(def_value)
	else:
		return allocate_easy(reg, file)
	'''
	#initialize physical register stack
	i = 0;
	while i < int(k) :
		reg_stack.append(i)
		i += 1
	#print("Length of reg stack is : ", len(reg_stack))


	#iterate through opcodes
	curr = ir_list.head
	while (curr != None) :
		#print("curr " + curr)
		#skip this process for nops
		if curr.data[1] not in ["nop", "output"]:
		

			#for first region of source registers
			if curr.data[1] not in ["loadI"]:
				vr = curr.data[3]
				#if pr already  assigned use it
				if vr2[vr] != "-":
					pr = vr2[vr]
					pr2[pr] = vr
					curr.data[4] = pr
					if pr2[pr] != vr:
						print("equivalency fail 1:1a")
					if vr2[vr] != pr:
						print("equivalency fail 1:1b")
				#get a pr and restore use value
				else:
					#if pr available use it
					if reg_stack:
						pr = reg_stack.pop()
								
					#otherwise spill value to attain pr
					else:
						#spill value, update ir
						print("spill region 1")
						pr = get_pr(curr, prnu, loc, k, None)
						#update vr to spillloc dict with previous vr
						spill_loc[pr2[pr]] = loc
						#######spill_loc[curr.data[3]] = loc
						#update loc value
						loc = loc + 4
					#restore use value
					#print("data is : ", curr.data)
					#print("SPILL location dictionary (use 1) is : ")
					#print("vr value is ", vr)
					#for key, value in spill_loc.items():
						#print("key, value : %s  %s" % (key, value))
					print("restoring at register 1")
					restore(curr, spill_loc[vr], k, pr)	
					curr.data[4] = pr
					#update prvr mappings
					#based on piazza post, commenting this out for a moment
					#vr2[vr] = pr
					#pr2[pr] = vr
					if pr2[pr] != vr:
						print("equivalency fail 1:2a")
					if vr2[vr] != pr:
						print("equivalency fail 1:2b")

				
				#check whether use is last use instance
				'''
				if curr.data[5] == "-":
					#free physical register
					vr2[vr] = "-"
					pr2[pr] = "-"
					#add freed register to stack
					reg_stack.append(pr)
				'''
				
				#mark next use of physical register in mapping
				prnu[pr] = curr.data[5] 
				for vra, pra in vr2.items():
					prb = vr2[vra]
					#if pr2[prb] != pra:
					'''
					if pr2[pra] != vra:
						print("3: vr2pr : %s, %s" % (vra, pra))
						print("3: pr2vr : %s, %s" % (pra, pr2[pra]))
						print("We have found a MISMATCHED dictionary at : " , curr.data)
					'''
			
			for vra, pra in vr2.items():
				prb = vr2[vra]
				if pra != prb:
					print("1: We have found a MISMATCHED dictionary at " )
					print("pr2vr: %s  %s"  % (pr, vr))
					print("vr2pr: %s  %s"  % (vr, pr))
			
			#for second region of source registers
			if curr.data[1] not in ["load", "loadI", "store"]:
				pr0 = pr
				vr = curr.data[7]
				#if pr already  assigned use it
				if vr2[vr] != "-":
					pr = vr2[vr]
					pr2[pr] = vr
					curr.data[8] = pr
				#get a pr and restore use value
				else:
					#if pr available use it
					if reg_stack:
						pr = reg_stack.pop()
								
					#otherwise spill value to attain pr
					else:
						#spill value, update ir
						print("spill region 2")
						pr = get_pr(curr, prnu, loc, k, pr0)
						#update vr to spillloc dict with previous vr
						spill_loc[pr2[pr]] = loc
						#######spill_loc[curr.data[3]] = loc
						#update loc value
						loc = loc + 4
					#restore use value
					#print("SPILL location dictionary (use 2) is : ")
					#print("vr value is ", vr)
					#for key, value in spill_loc.items():
						#print("key, value : %s  %s" % (key, value))
					print("restoring at register 2")
					restore(curr, spill_loc[vr], k, pr)	
					curr.data[8] = pr
					#update prvr mappings
					#based on piazza post, commenting this out for a moment
					#vr2[vr] = pr
					#pr2[pr] = vr
			
				#check whether use is last use instance
				'''
				if curr.data[9] == "-":
					#free physical register
					vr2[vr] = "-"
					pr2[pr] = "-"
					#add freed register to stack
					reg_stack.append(pr)
				'''
				
				#mark next use of physical register in mapping
				prnu[pr] = curr.data[9] 
				for vra, pra in vr2.items():
					prb = vr2[vra]
					#if pr2[prb] != pra:
					''''
					if pr2[pra] != vra:
						print("3: vr2pr : %s, %s" % (vra, pra))
						print("3: pr2vr : %s, %s" % (pra, pr2[pra]))
						print("We have found a MISMATCHED dictionary at : " , curr.data)
					'''
			
			for vra, pra in vr2.items():
				prb = vr2[vra]
				if pra != prb:
					print("2: We have found a MISMATCHED dictionary at " )
			
			#check whether uses were last uses in regions two and three
			
			if curr.data[5] == "-" and vr2[curr.data[3]]!= "-":
				#free physical register
				vr2[curr.data[3]] = "-"
				pr2[curr.data[4]] = "-"
				#add freed register to stack
				reg_stack.append(pr)
			if curr.data[9] == "-" and vr2[curr.data[7]]!= "-":
					#free physical register
					vr2[curr.data[7]] = "-"
					pr2[curr.data[8]] = "-"
					#add freed register to stack
					reg_stack.append(pr)
			
			#for last region of source registers
			if curr.data[1] not in []:
				vr = curr.data[11]
				#if pr already  assigned use it
				if vr2[vr] != "-":
					pr = vr2[vr]
					pr2[pr] = vr
					curr.data[12] = pr
					#sanity check
					if pr2[pr] != vr:
						print("equivalency fail 1")
						print("vr is: ", vr)
						print("pr is: ", pr)
						print("pr2 is: ", pr2[pr])
						print("vr2 is: ", vr2[vr])
						print("pr2vr: %s  %s"  % (pr, vr))
						print("vr2pr: %s  %s"  % (vr, pr))
				#get a pr and restore use value
				else:
					#if pr available use it
					if reg_stack:
						pr = reg_stack.pop()				
					#otherwise spill value to attain pr
					else:
						#spill value, update ir
						pr = get_pr(curr, prnu, loc, k, None)
						#update vr to spillloc dict with previous vr
						spill_loc[pr2[pr]] = loc
						#update loc value
						loc = loc + 4

					curr.data[12] = pr
					#update prvr mappings
					#print("vr is: ", vr)
					vr2[vr] = pr
					pr2[pr] = vr
					#print("first Line check")
					#print("vr2 at 0 :", vr2[0])
					#print("pr2 at 2 :", pr2[2])
					#sanity check
					if pr2[pr] != vr:
						print("equivalency fail 2a")
					if vr2[vr] != pr:
						print("equivalency fail 2b")
				#check whether use is last use instance
				'''
				if curr.data[13] == "-":
					#free physical register
					vr2[vr] = "-"
					pr2[pr] = "-"
					#add freed register to stack
					reg_stack.append(pr)
				'''
				#sanity check
				
				if pr2[pr] != vr:
					print("equivalency fail 3a")
					#print("pr2vr: %s  %s"  % (pr, vr))
				if vr2[vr] != pr:
					print("equivalency fail 3b")
					#print("vr2pr: %s  %s"  % (vr, pr))
				
				#mark next use of physical register in mapping
				prnu[pr] = curr.data[13] 
				for vra, pra in vr2.items():
					prb = vr2[vra]
					#if pr2[prb] != pra:
					'''
					if pr2[pra] != vra:
						print("3: vr2pr : %s, %s" % (vra, pra))
						print("3: pr2vr : %s, %s" % (pra, pr2[pra]))
						print("We have found a MISMATCHED dictionary at : " , curr.data)
					'''
		#add check for whether vr and pr dictionaries are equivalent
		
		for vra, pra in vr2.items():
			prb = vr2[vra]
			if pra != prb:
				print("3: We have found a MISMATCHED dictionary at " )
		
		


		curr = curr.next
	#print("this is the final ir allowing for physical register placement")
	#ir_list.printListContents(ir_list.head)  
	print_reallocated_registers()      
	return 

def restore(curr, loc, k, new_pr):
	'''
	Inputs:
	curr- the current data block in front of which operations will be added to IR
	loc- the location at which the restored information currently exists
	k- the kth pr in which restored information will be temporarily held
	new_pr- freed physical register in which the restored value will be loaded
	

	Effects:
	Restore the contents of a spilled register to a new physical register, updates intermediate representation
	'''
	#print("in restore ir is:" , ir_list.printListContents(ir_list.head) )


	#add loadi operation to IR
	loadI = ["-"] *  14
	loadI[0] = "restore"
	loadI[1] = "loadI"
	loadI[2] = loc
	loadI[12] = k
	loadI[13] = curr.data[0]
	if curr.prev == None:
		ir_list.push(loadI)
	else:
		ir_list.insertAfter(curr.prev, loadI)

	#print("restore loadI data array is: " , loadI)


	#add load operation to IR
	
	load = ["-"] *  14
	load[0] = "restore"
	load[1] = "load"
	load[4] = k
	load[12] = new_pr
	load[13] = curr.data[0]
	if curr.prev == None:
		ir_list.push(load)
	else:
		ir_list.insertAfter(curr.prev, load)

	return


def get_pr(curr, prnu, loc, free_pr, old_pr):
	'''
	Inputs:
	curr- the current data block in front of which operations will be added to IR
	prnu- dictionary mapping registers to their next use instance
	loc- the location at which the restored information currently exists
	free_pr-freed physical register in which the restored value will be loaded
	old_pr- the pr previously spilled in the same operation

	Effects:
	Returns the identifier of a physical register to whose data has been freed for reallocation
	'''
	#TODOOOOO, can be optimized for loadi operation

	nu_val = -1
	pr_val = "-"
	for pr, nu in prnu.items():
		if nu == "-":
			#print("pr for - nu val was ", pr)
			pr_val = pr
			nu_val = nu
			break

		if int(nu) > nu_val and pr != old_pr :
			pr_val = pr
			nu_val = nu
	#add loadi operation to IR
	loadI = ["-"] *  14
	loadI[0] = "spill"
	loadI[1] = "loadI"
	loadI[2] = loc
	loadI[12] = free_pr
	if curr.prev == None:
		ir_list.push(loadI)
	else:
		ir_list.insertAfter(curr.prev, loadI)

	#add store operation to IR
	store = ["-"] *  14
	store[0] = "spill"
	store[1] = "store"
	store[4] = pr_val
	store[12] = free_pr
	if curr.prev == None:
		ir_list.push(store)
	else:
		ir_list.insertAfter(curr.prev, store)




	return pr_val

def print_reallocated_registers():
	'''

	Effects:
	Prints to standard out a complete file with new virtual representation of the registers
	'''
	curr = ir_list.head
	while curr!= None:
		#print opname
		sys.stdout.write(" %s " % curr.data[1])

		#print first region
		if curr.data[1] != "nop":
			#if not a register print the constant at location
			if curr.data[1] in ["loadI", "output"]:
				sys.stdout.write(" %s " % curr.data[2])
				#if output, no further printing needed
				if curr.data[1] == "output":
					curr = curr.next
					sys.stdout.write("\n")
					continue


			#if a register print the register, potentially with a comma as well
			else:
				if curr.data[1] not in ["load", "store"]:
					sys.stdout.write(" r%s, " % curr.data[4])
				else:
					sys.stdout.write(" r%s " % curr.data[4])


		#if nop, no further printing needed
		else:
			curr = curr.next
			sys.stdout.write("\n")
			continue

		#print second region
		if curr.data[1] not in ["load", "loadI", "store"]:
			sys.stdout.write(" r%s " % curr.data[8])

		#print arrow
		sys.stdout.write(" => ") 
		#print third region
		sys.stdout.write(" r%s " % curr.data[12])

		#print the new linked list item
		#print("data is : " , curr.data)

		#advance pointer
		curr = curr.next
		#print new line
		sys.stdout.write("\n")

	return

def print_renamed_registers():
	'''

	Effects:
	Prints to standard out a complete file with new virtual representation of the registers
	'''
	curr = ir_list.head
	while curr!= None:
		#print opname
		sys.stdout.write(" %s " % curr.data[1])

		#print first region
		if curr.data[1] != "nop":
			#if not a register print the constant at location
			if curr.data[1] in ["loadI", "output"]:
				sys.stdout.write(" %s " % curr.data[2])
				#if output, no further printing needed
				if curr.data[1] == "output":
					curr = curr.next
					sys.stdout.write("\n")
					continue


			#if a register print the register, potentially with a comma as well
			else:
				if curr.data[1] not in ["load", "store"]:
					sys.stdout.write(" r%s, " % curr.data[3])
				else:
					sys.stdout.write(" r%s " % curr.data[3])


		#if nop, no further printing needed
		else:
			curr = curr.next
			sys.stdout.write("\n")
			continue

		#print second region
		if curr.data[1] not in ["load", "loadI", "store"]:
			sys.stdout.write(" r%s " % curr.data[7])

		#print arrow
		sys.stdout.write(" => ") 
		#print third region
		sys.stdout.write(" r%s " % curr.data[11])

		#advance pointer
		curr = curr.next
		#print new line
		sys.stdout.write("\n")

	return




def scan_for_parser(line_num, line, sar):
	'''
	inputs: line_number evaluating, line contents, sar (syntax array index at which to begin evaluation)
	Effects:
	Prints out a tag/lexeme pairs along with its line number from a given file
	Returns an identifier for the corresponding lexeme and the new string index
	'''

	lexeme_found = False
	str_index = 0
	while(sar < 12):

		#check lexeme against array of accepted lexemes
		
		if line[str_index: str_index + len(syntax_array[sar])] == syntax_array[sar]:
			#print("new string index is %d", str_index)
			#print("the word matches from syntax array",  line[str_index: str_index + len(syntax_array[sar])], syntax_array[sar])
			#print("the word matches -%s- " % line[str_index: str_index + len(syntax_array[sar])])
			str_index += len(syntax_array[sar])
			#present_category(line_num, sar)
			


			

			#make sure that there is at least one empty space following
			if sar < 9:
				if not line[str_index].isspace():
					#EXIT PROGRAMMMM HEREE
					sys.stderr.write("%d: An ILOC opcode must be followed by a blank space. \n" % line_num)
					return 16, str_index, line[str_index]
				str_index += 1
			lexeme_found = True
			return sar, str_index, syntax_array[sar]
			break
		else:
			sar += 1


	#only check further lexeme categories if lexeme match not yet found
	if lexeme_found == False:
		#check if lexeme is possible register identifier
		if line[str_index] == "r":
			strt_str_index = str_index
			str_index += 1
			#ensure r is followed by at least one digit
			if line[str_index] in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
				str_index += 1
				while (1):
					#print("still inside register while condition")
					if line[str_index] in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
						str_index += 1
					#time to break loop
					else:
						#present_category(line_num, 12, line[strt_str_index: str_index])
						return 12, str_index, line[strt_str_index: str_index]

						#print("this is a register, register -%s-" % line[strt_str_index: str_index])
						

						break
				
			


			else:
				#EXIT PROGRAMMMM HEREE
				sys.stderr.write("%d: ERROR: A register must be followed by a positive integer in order to be valid. \n" % line_num)
				return 16, str_index, line[str_index]



		#check if lexeme is positive integer
		elif line[str_index] in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
			strt_str_index = str_index
			str_index += 1
			while (1):
				if line[str_index] in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
					str_index += 1
					#time to break loop
				else:
					#present_category(line_num, 13, line[strt_str_index: str_index])
					

					#print("this is a constant, constant number is -%s-" % line[strt_str_index: str_index])
					#print("rest of line after constant is %s" % line[str_index:])
					return 13, str_index, line[strt_str_index: str_index] 
					break
		#check whether this is a newline or line break
		elif line[str_index].isspace():
			str_index += 1
			return 15, str_index, line[str_index]
			#present_category(line_num, 14)
		
		
		else:
			#print("rest of line prior to error is %s" % line[str_index:])
			#print("Line %d: ERROR: This is not a valid word." % line_num)
			#this is an error notification 
			return 16, str_index, line[str_index]



	return


def scan_file(file):
	'''
	inputs: filename
	Effects:
	Prints out a series of tag/lexeme pairs along with their line number from a given file

	'''
	line_num = 1

	while 1: 
		
		# read from provided file line by line
		line = file.readline()   
		str_index = 0        
		if not line: 
			#if at end of file say so 
			present_category(line_num - 1, 14) 
			break

		#if line is commented skip line
		if line[str_index:str_index + 2] == "//":
			line_num += 1
			continue
			#print("Line %d is commented out" % line_num)
		#if line not commented begin evaluation
		#then iterate until end of line

		else:      
			while(str_index < len(line)):
				#while("/n" not in line[str_index:str_index + 2] and "/r/n" not in line[str_index:str_index + 4]):
				#if line is commented skip line
				if line[str_index:str_index + 2] == "//":
					#print("Line %d is commented out" % line_num)
					break
				#let sar = syntax_array_index abbreviation
				sar = 0
				
				#check for white space
				if line[str_index].isspace():
					str_index += 1
					continue
				#if not white space, detect category, iterate through syntax_dict for matching lexeme
				else:
					lexeme_found = False
					while(sar < 12):
					
						#check lexeme against array of accepted lexemes
						
						if line[str_index: str_index + len(syntax_array[sar])] == syntax_array[sar]:
							#print("new string index is %d", str_index)
							#print("the word matches from syntax array",  line[str_index: str_index + len(syntax_array[sar])], syntax_array[sar])
							#print("the word matches -%s- " % line[str_index: str_index + len(syntax_array[sar])])
							str_index += len(syntax_array[sar])
							present_category(line_num, sar)


							

							#make sure that there is at least one empty space following
							if sar < 9:
								if not line[str_index].isspace():
									#EXIT PROGRAMMMM HEREE
									print("Line %d: ERROR: An ILOC opcode must be followed by a blank space." % line_num)
								str_index += 1
							lexeme_found = True
							break
						else:
							sar += 1

					#only check further lexeme categories if lexeme match not yet found among opcodes
					if lexeme_found == False:
						
						#check if lexeme is possible register identifier
						if line[str_index] == "r":
							strt_str_index = str_index
							str_index += 1
							#ensure r is followed by at least one digit
							if line[str_index] in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
								str_index += 1
								while (1):
									#print("still inside register while condition")
									if line[str_index] in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
										str_index += 1
									#time to break loop
									else:
										present_category(line_num, 12, line[strt_str_index: str_index])

										#print("this is a register, register -%s-" % line[strt_str_index: str_index])
										

										break

							else:
								#EXIT PROGRAMMMM HEREE
								print("Line %d: ERROR: An register must be followed by a positive integer in order to be valid." % line_num)




						#check if lexeme is positive integer
						elif line[str_index] in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
							strt_str_index = str_index
							str_index += 1
							while (1):
								if line[str_index] in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
									str_index += 1
									#time to break loop
								else:
									present_category(line_num, 13, line[strt_str_index: str_index])
									break
						#check whether this is a newline or line break
						elif line[str_index].isspace():
							str_index += 1		
						else:
							print("rest of line prior to error is -%s-" % line[str_index:])
							print("Line %d: ERROR: This is not an acceptable lexeme." % line_num)
							break
							
						
				




		
			#if string matches syntax dict...print corresponding category for index, otherwise or also in case of r, check int category 
		

			#error detection comes later... 
			  
		
			#print(line)


			#increment line indexing
			line_num += 1

	

	return



def main():
	
	#determine the flag by reading from command line
	
	parser = OptionParser()
	parser.add_option("-s", help="Prints out a series of tag/lexeme pairs along with their line number from a given file", action="store_true")
	parser.add_option("-r", help="Prints out parser's intermediate representation in a human readable format", action="store_true")
	parser.add_option("-p", help="Prints out parsing details, including errors and line number for error if parsing is unsuccessful", action="store_true")
	parser.add_option("-x", help="Renames source registers in provided file to corresponding virtual registers", action="store_true")
	parser.add_option("-k", help="Allocates registers", action="store_true")
	(options, args) = parser.parse_args()

	scan = options.s
	parse = options.p
	read = options.r
	rename = options.x
	allocate = options.k

	#determine the filename from command line
	filename = sys.argv[-1]
	
	registers = sys.argv[-2]

	


	#open file and execute appropriate command
	file = open(str(filename), 'r')
	if scan:
		scan_file(file)
	elif read:
		#print intermediate representation
		create_ir(file)
	elif rename:
		#print intermediate representation
		rename_registers(file)
	elif allocate:
		#print intermediate representation
		allocate_registers(registers, file)
	else:
		#parse_file(file)
		#test_func()
		allocate_registers(registers, file)

	#close file
	file.close() 



	return


if __name__ == "__main__":
	main()




	
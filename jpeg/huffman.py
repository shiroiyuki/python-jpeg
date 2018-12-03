from queue import PriorityQueue

class Node(Object):
    pass

# An internal node in a code tree. It has two nodes as children.
class InternalNode(Node):
	def __init__(self, left, right):
		if not isinstance(left, Node) or not isinstance(right, Node):
			raise TypeError()
		self.leftchild = left
		self.rightchild = right


# A leaf node in a code tree. It has a symbol value.
class Leaf(Node):
	def __init__(self, sym):
		if sym < 0:
			raise ValueError("Symbol value must be non-negative")
		self.symbol = sym


class HuffmanTree:
	
	# Constructs a code tree from the given tree of nodes and given symbol limit.
	# Each symbol in the tree must have value strictly less than the symbol limit.
	def __init__(self, root, symbollimit):
		# Recursive helper function
		def build_code_list(node, prefix):
			if isinstance(node, InternalNode):
				build_code_list(node.leftchild , prefix + (0,))
				build_code_list(node.rightchild, prefix + (1,))
			elif isinstance(node, Leaf):
				if node.symbol >= symbollimit:
					raise ValueError("Symbol exceeds symbol limit")
				if self.codes[node.symbol] is not None:
					raise ValueError("Symbol has more than one code")
				self.codes[node.symbol] = prefix
			else:
				raise AssertionError("Illegal node type")
		
		if symbollimit < 2:
			raise ValueError("At least 2 symbols needed")
		# The root node of this code tree
		self.root = root
		# Stores the code for each symbol, or None if the symbol has no code.
		# For example, if symbol 5 has code 10011, then codes[5] is the tuple (1,0,0,1,1).
		self.codes = [None] * symbollimit
		build_code_list(root, ())  # Fill 'codes' with appropriate data
		
	# Returns the Huffman code for the given symbol, which is a sequence of 0s and 1s.
	def get_code(self, symbol):
		if symbol < 0:
			raise ValueError("Illegal symbol")
		elif self.codes[symbol] is None:
			raise ValueError("No code for given symbol")
		else:
			return self.codes[symbol]
	
	# Returns a string representation of this code tree,
	# useful for debugging only, and the format is subject to change.
	def __str__(self):
		# Recursive helper function
		def to_str(prefix, node):
			if isinstance(node, InternalNode):
				return to_str(prefix + "0", node.leftchild) + to_str(prefix + "0", node.rightchild)
			elif isinstance(node, Leaf):
				return "Code {}: Symbol {}\n".format(prefix, node.symbol)
			else:
				raise AssertionError("Illegal node type")
		
		return to_str("", self.root)
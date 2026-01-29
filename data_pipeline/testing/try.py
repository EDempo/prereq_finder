import sys
import os

# Get the absolute path of the parent directory
parent_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))

# Append the parent directory to sys.path
sys.path.append(parent_dir)

# Now you can import the module from the parent directory
import tree

s = "ARAB201; or must hav appropriate World Language Placement (WLP) score."
node = tree.treeify(s)
if isinstance(node, tree.courseNode):
    tree.print_node(node)
else:
    print(node)

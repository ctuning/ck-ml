import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()
import argparse
from tensorflow.core.framework import graph_pb2
from tensorflow.python.platform import gfile
import copy
import os

def load_frozen_graph(model_file):
	graph_def = tf.compat.v1.GraphDef()
	with gfile.FastGFile(model_file, 'rb') as f:
		graph_def.ParseFromString(f.read())
	return graph_def

if __name__=='__main__':
	parser = argparse.ArgumentParser(
		description='Fix input shape for Tensorflow Models')
	parser.add_argument("--input_graph", "-i", 
		default='input.pb',
		required=False,
		type=str, help="file name of input frozen graph")
	parser.add_argument("--input_name", "-in", 
		default='input_tensor',
		required=False,
		type=str, help="input of tensorflow graph")
	parser.add_argument("--output_graph", "-o", 
		default='output.pb',
		required=False,
		type=str, help="file name of output frozen graph")
	parser.add_argument("-t", "--type", 
		required=True,
		dest='input_type',
		type=str, help="indicate input type. 't' for pbtxt, 'b' for pb")
	args = parser.parse_args()
	inputGraph = load_frozen_graph(args.input_graph)
	outputGraph = tf.compat.v1.GraphDef()

	new_input = tf.placeholder( dtype=tf.float32, shape = [1, 224, 224, 3], name=args.input_name)
	for node in inputGraph.node:
		if node.name == args.input_name:
			print("replacing ()".format(args.input_name))
			outputGraph.node.extend([new_input.op.node_def])
		else:
			outputGraph.node.extend([copy.deepcopy(node)])
	# Save the new graph.
	with tf.compat.v1.Session() as sess:
		sess.graph.as_default()
		tf.import_graph_def(outputGraph, name="")
		if(args.input_type == 'b'):
			tf.io.write_graph(sess.graph.as_graph_def(add_shapes=True), os.path.dirname(args.output_graph), os.path.basename(args.output_graph), as_text=False)
		if(args.input_type == 't'):
			tf.io.write_graph(sess.graph.as_graph_def(add_shapes=True), os.path.dirname(args.output_graph), os.path.basename(args.output_graph), as_text=True)
	print("The input shape has been fixed successfully.")

	# Cut the unwanted nodes.
	graph = tf.compat.v1.GraphDef()
	with tf.gfile.Open(args.output_graph, 'rb') as f:
		data = f.read()
		graph.ParseFromString(data)

	nodes = graph.node[2:]
	output_graph = graph_pb2.GraphDef()
	output_graph.node.extend(nodes)
	with tf.gfile.GFile(args.output_graph, 'w') as f:
		os.remove(args.output_graph)
		f.write(output_graph.SerializeToString())

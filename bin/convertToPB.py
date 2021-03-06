#!/usr/bin/env python


#script that takes model in .h5 format as input as spits out the graph format used in CMSSW

import imp
try:
    imp.find_module('setGPU')
    import setGPU
except ImportError:
    found = False
            
import tensorflow as tf

sess = tf.Session()
from keras.models import load_model
from argparse import ArgumentParser
from keras import backend as K
from Losses import * #needed!
import os

K.set_session(sess)

parser = ArgumentParser('')
parser.add_argument('inputModel')
parser.add_argument('outputDir')
args = parser.parse_args()

 
if os.path.isdir(args.outputDir):
    raise Exception('output directory must not exists yet')

model=load_model(args.inputModel, custom_objects=global_loss_list)

K.set_learning_phase(0)
outputs = [node.op.name for node in model.outputs]
print outputs
constant_graph = tf.graph_util.convert_variables_to_constants(sess, sess.graph.as_graph_def(), outputs)
tfoutpath=args.outputDir+'/tf'
import os
os.system('mkdir -p '+tfoutpath)
tf.train.write_graph(constant_graph, tfoutpath, "constant_graph.pb", as_text=False)



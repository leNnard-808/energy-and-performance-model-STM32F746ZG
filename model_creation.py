#!/usr/bin/env python3
# coding: utf-8

# In[179]:


import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import matplotlib.pyplot as plt
import pandas as pd




conv_macs = []
maxpool_macs = []
fc_macs = []




def function(order, Iy, Ix, Cin, neurons):
	
    order_format = order.replace(",", ".") # format to save it to the CSV as a string without the , to be annoying.

    
    order_list = list(order.split("/"))
    
    conv_amount = 0
    mpool_amount = 0
    
    model = keras.Sequential()
    
    model.add(keras.Input(shape=(Iy,Ix,Cin)))
    
    
    for x in range(len(order_list)):
        
        
        
        if order_list[x] == "conv":
            
            p = order_list[x+1].split(",")
            

            
            ksize, kpoolsize, kpoolsize = int(p[0]), int(p[1]), int(p[2])
            
            
            model.add(layers.Conv2D(ksize, kernel_size=(kpoolsize,kpoolsize), activation="relu"))
            
            #Calculate MACs: K * K * Cin * Hout * Wout * Cout
            param = list(model.layers[-1].output_shape)
            param.pop(0)
            Wout, Hout, Cout = param[0], param[1], param[2]
            cmacs = Wout * Hout * Cout * kpoolsize * kpoolsize * Cin
            conv_macs.append(cmacs)
            Cin = Cout
            
            conv_amount = conv_amount + 1
            
        elif order_list[x] == "maxpool":
            
            
            p = order_list[x+1].split(",")
            
            maxpoolsize, maxpoolsize = int(p[0]), int(p[1])
            
            model.add(layers.MaxPooling2D(pool_size=(maxpoolsize,maxpoolsize)))
            
            param = list(model.layers[-1].output_shape)
            param.pop(0)
            Wout, Hout, Cout = param[0], param[1], param[2]
            mmacs = Wout * Hout * Cout * maxpoolsize * maxpoolsize
            maxpool_macs.append(mmacs)
            
            mpool_amount = mpool_amount + 1
            
            
            
        elif order_list[x] == "FC": 
            model.add(layers.Flatten())
            
            
            param = list(model.layers[-1].output_shape)
            param.pop(0)
            O = param[0]
            FCmacs = O * neurons
            fc_macs.append(FCmacs)
            
            model.add(layers.Dropout(0.5))
            model.add(layers.Dense(neurons, activation="softmax"))
        
        else:
            None
            
    #model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])
    
    
    filename = "_".join(order_list) + ".h5"
    
    model.save(filename)
    
    
    return model, filename, order_format, conv_amount, mpool_amount
            
            
        


# In[174]:


def representative_data_gen():
        random_image = np.random.rand(1, 28, 28, 1).astype(np.float32)
        yield [random_image]
  
def convert_to_tflite(model, filename):
    
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    converter.representative_dataset = representative_data_gen
    converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
    converter.inference_input_type = tf.int8  # or tf.uint8
    converter.inference_output_type = tf.int8  # or tf.uint8
    tflite_quant_model = converter.convert()


    tflite_filename = filename.replace('.h5', '.tflite')
    with open(tflite_filename, 'wb') as f:
        f.write(tflite_quant_model)
        
    return tflite_filename


# In[175]:


import subprocess

def convert_to_c_header(tflite_filename):
    # Run the xxd command to generate the C header file
    c_header_filename = tflite_filename.replace('.tflite', '.h')
    subprocess.run(f'xxd -i {tflite_filename} > {c_header_filename}', shell=True)


# In[178]:


import argparse

# create argument parser object
parser = argparse.ArgumentParser(description='Process some arguments.')

# add arguments to parser
parser.add_argument('-C_in', type=int, help='Number of input channels')
parser.add_argument('-I_y', type=int, help='Input height')
parser.add_argument('-I_x', type=int, help='Input width')
parser.add_argument('-n', type=int, help='Number of classes')
parser.add_argument('-order', type=str, help='Layer order as a string')

# parse arguments from command line
args = parser.parse_args()


# In[161]:


model, filename, order_format, conv_amount, mpool_amount = function(args.order, args.I_x, args.I_y, args.C_in, args.n)
tflite_filename = convert_to_tflite(model, filename)
convert_to_c_header(tflite_filename)

model.summary()


# In[ ]:


# Compute the sum of each array
conv_macs_sum = sum(conv_macs)
mpool_macs_sum = sum(maxpool_macs)
FC_macs_sum = sum(fc_macs)

# Define the output file
import os

output_file = 'data.txt'

# Check if the output file exists and open it in append mode
if os.path.exists(output_file):
    with open(output_file, 'a') as f:
        # Write the sums and their names in a new line
        f.write(f'{conv_macs_sum}, {conv_amount}, {mpool_macs_sum}, {mpool_amount}, {FC_macs_sum}, {order_format}\n')
else:
    with open(output_file, 'w') as f:
        # Write the sums and their names in a new line
        f.write(f'{conv_macs_sum}, {conv_amount}, {mpool_macs_sum}, {mpool_amount}, {FC_macs_sum}, {order_format}\n') 


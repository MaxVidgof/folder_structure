import sys
import os
import folderstats
import pygraphviz as pgv
import numpy as np

#parameters
target_dir = str(sys.argv[1]) #1st argument (after the script name, of course)
name = target_dir+'_structure.svg' # output file
hidden = False #include hidden files/folders

#print folder structure
for (dirpath, dirnames, filenames) in os.walk(target_dir):
    for f in filenames:
        print('FILE :', os.path.join(dirpath, f))
    for d in dirnames:
        print('DIRECTORY :', os.path.join(dirpath, d))

#create dataframe of the folder structure
df = folderstats.folderstats(target_dir, ignore_hidden = not hidden)
print(df.head())

# Sort the index
df_sorted = df.sort_values(by='id')

#general graph parameters
G = pgv.AGraph(strict = False, directed = True, format = 'svg')
G.graph_attr['rankdir'] = 'TB'
#G.graph_attr['rankdir'] = 'LR'
G.node_attr['shape'] = 'box'

#root node
G.add_node("1", label=target_dir)

#all other nodes
for i, row in df_sorted.iterrows():
    if (row.parent and not np.isnan(row.num_files)):
        G.add_node(row.id, label=(row.path.split('/'))[-1])
        G.add_edge(row.parent, row.id)
#draw the graph and save it to file
G.draw(name, prog='dot')

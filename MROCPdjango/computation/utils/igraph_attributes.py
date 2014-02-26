#!/usr/bin/python

# igraph_attributes.py
# Created by Disa Mhembere on 2014-01-15.
# Email: disa@jhu.edu
# Copyright (c) 2014. All rights reserved.

import rpy2.robjects as robjects
import igraph

def r_igraph_get_attr(g, attr_name, which):
  """
  Get an igraph graph attribute in R.

  Positional arguments
  ====================
  g - the R igraph object
  attr_name - the name of the vetex attribute I want to get. Type: string
  which - "g"/"e"/"v" stand for graph, edge, vertex

  Returns
  ======
  The requested attribute

  """

  attr_dict = {"g":"graph", "e":"edge", "v":"vertex"}

  get = robjects.r("""
  require(igraph)
  fn <- function(g, attr_name){
  get.%s.attribute(g, attr_name)
  }
  """ %attr_dict.get(which, "graph")) # assume graph attr if not specified

  return get(g, attr_name)

def r_serial_save(g, fn):
  """
  Serialized save from R.

  Positional arguments
  ====================
  g - the graph to be saved
  fn - the file name it should have
  """
  save =  robjects.r("""
        fn <- function(g, fn){
        save(g, file=fn)
       } """)

  return save(g, fn)

def get_latent_pos(g):
  """
  Helper function to extract the latent position vectors (eigenvalues) from
  a graph.

  Positional arguments
  ====================
  g - the igraph graph

  Returns
  =======
  A numpy dense array (latent position matrix)
  """
  import numpy as np
  lp = g.vs.get_attribute_values("latent_pos")
  print "Initial lp's", lp , "\n"

  eigvals = None # Don't know its 2nd dimension yet

  for idx, item in enumerate(lp):
    converted = map(complex, item.split(","))

    if eigvals is None:
      eigvals = np.zeros((g.vcount(), len(converted)), dtype=complex)

    eigvals[idx,:] = converted

  return eigvals

def test():
  if len(sys.argv) > 1 and sys.argv[1] != "-h":
    g = igraph.read(sys.argv[1], format="graphml")
    print get_latent_pos(g)
  #else
  print "Provide command line arg 1"

if __name__ == "__main__":
  import sys
  test()
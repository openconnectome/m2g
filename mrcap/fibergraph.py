from scipy.sparse import lil_matrix, csc_matrix
from scipy.io import loadmat, savemat
from fiber import Fiber
import roi
import mask
import zindex
import math
import itertools
from cStringIO import StringIO

"""
  This routine uses two different sparse matrix representations.
  The calls need to be performed in the following order

     Create FiberGraph
     Add Edges (lil format)
     Complete -- this converts from dictionary of keys format to Column CSC
     Write or SVD (on csc format)


  Sparse matrix representation of a Fiber graph
"""

class FiberGraph:

  """
  Constructor: number of nodes in the graph
    convert it to a maximum element
  """
  def __init__(self, matrixdim, rois, mask ):

    # Regions of interest
    self.rois = rois

    # Brainmask
#    self.mask = mask

    # Round up to the nearest power of 2
    xdim = int(math.pow(2,math.ceil(math.log(matrixdim[0],2))))
    ydim = int(math.pow(2,math.ceil(math.log(matrixdim[1],2))))
    zdim = int(math.pow(2,math.ceil(math.log(matrixdim[2],2))))

    # Need the dimensions to be the same shape for zindex
    xdim = ydim = zdim = max ( xdim, ydim, zdim )

    # largest value is -1 in each dimension, then plus one because range(10) is 0..9
    self._maxval = zindex.XYZMorton ([xdim-1,ydim-1,zdim-1]) + 1

    # list of list matrix for one by one insertion
    self.spedgemat = lil_matrix ( (self._maxval, self._maxval), dtype=float )

    # empty CSC matrix
    self.spcscmat = csc_matrix ( (self._maxval, self._maxval), dtype=float )


  #
  # Destructor
  #
  def __del__(self):
    pass

  #
  # Add a fiber to the graph.
  #  This is not idempotent, i.e. if you add the same fiber twice you get a different result
  #  in terms of graph weigths.
  #
  def add ( self, fiber ):
    """Add a fiber to the graph"""

    # Get the set of voxels in the fiber
    allvoxels = fiber.getVoxels ()

    # Voxels for the big graph
    voxels = []

    for i in allvoxels:
      xyz = zindex.MortonXYZ(i)

      # Use only the important voxels
      roival = self.rois.get(xyz)
      # if it's an roi and in the brain
  #    if roival and self.mask.get (xyz):
      if roival:
        voxels.append ( i )

    # Add edges to the big graph
    for v1,v2 in itertools.combinations((voxels),2):
      if ( v1 < v2 ):
        self.spedgemat [ v1, v2 ] += 1.0
      else:
        self.spedgemat [ v2, v1 ] += 1.0

  #
  # Complete the graph.  Get it ready for analysis.
  #
  def complete ( self ):
    """Done adding fibers.  Prior to analysis"""

    self.spcscmat = csc_matrix ( self.spedgemat )
    del self.spedgemat

  #
  #  Write the sparse matrix out in a format that can be reingested.
  #  fout should be an open file handle
  #
  def saveToMatlab ( self, key, filename ):
    """Save the sparse array to disk in the specified file name"""

    if 0 == self.spcscmat.getnnz():
      print "Call complete after adding all edges"
      assert 0

    print "Saving key ", key, " to file ", filename
    savemat( filename , {key: self.spcscmat})

  #
  #  Write the sparse matrix out in a format that can be reingested.
  #  fout should be an open file handle
  #
  def loadFromMatlab ( self, key, filename ):
    """Load the sparse array from disk by file name"""

    print "Reading key ", key, " from file ", filename

    # first convert to csc
    t = loadmat ( filename  )
    self.spcscmat = t[key]

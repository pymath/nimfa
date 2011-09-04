
"""
    ##############################################
    Recommendations (``examples.recommendations``)
    ##############################################
    
    .. note:: MovieLens movies' rating data set used in this example is not included in the `datasets` and need to be
      downloaded. Download links are listed in the ``datasets``. Download compressed version of the MovieLens 100k. 
      To run the example, the extracted data set must be find in the ``MovieLens`` folder under ``datasets``. 
      
    .. note:: No additional knowledge in terms of ratings' timestamps, information about items and their
       genres or demographic information about users is used in this example. 
      
    To run the example simply type::
        
        python recommendations.py
        
    or call the module's function::
    
        import mf.examples
        mf.examples.recommendations.run()
        
    .. note:: This example uses matplotlib library for producing visual interpretation of the RMSE error measure. 
    
"""

import mf
import numpy as np
import scipy.sparse as sp
from os.path import dirname, abspath, sep

try:
    import matplotlib.pylab as plb
except ImportError, exc:
    raise SystemExit("Matplotlib must be installed to run this example.")

def run():
    """
    Run NMF - Divergence on the MovieLens data set.
    
    Factorization is run on `ua.base`, `ua.test` and `ub.base`, `ub.test` data set. This is MovieLens's data set split 
    of the data into training and test set. Both test data sets are disjoint and with exactly 10 ratings per user
    in the test set. 
    """
    for data_set in ['ua', 'ub']:
        # read ratings from MovieLens data set 
        V = read(data_set)
        # preprocess MovieLens data matrix
        V = preprocess(V)
        # run factorization
        W, H = factorize(V)
        # plot RMSE rate on MovieLens data set. 
        plot(W, H, data_set)
        exit()
        
def factorize(V):
    """
    Perform NMF - Divergence factorization on the sparse MovieLens data matrix. 
    
    Return basis and mixture matrices of the fitted factorization model. 
    
    :param V: The MovieLens data matrix. 
    :type V: `scipy.sparse.csr_matrix`
    """
    print "Performing NMF - Divergence factorization ..." 
    model = mf.mf(V, 
                  seed = "random_vcol", 
                  rank = 12, 
                  method = "nmf", 
                  max_iter = 15, 
                  initialize_only = True,
                  update = 'divergence',
                  objective = 'div')
    fit = mf.mf_run(model)
    print "... Finished"
    sparse_w, sparse_h = fit.fit.sparseness()
    print """Stats:
            - iterations: %d
            - KL Divergence: %5.3f
            - Euclidean distance: %5.3f
            - Sparseness basis: %5.3f, mixture: %5.3f""" % (fit.fit.n_iter, fit.distance(), fit.distance(metric = 'euclidean'), sparse_w, sparse_h)
    return fit.basis(), fit.coef()
    
def read(data_set):
    """
    Read movies' ratings data from MovieLens data set. 
    
    Construct a user-by-item matrix. This matrix is sparse, therefore ``scipy.sparse`` format is used. For construction
    LIL sparse format is used, which is an efficient structure for constructing sparse matrices incrementally. 
    
    Return the MovieLens sparse data matrix in LIL format. 
    
    :param data_set: Name of the split data set to be read. 
    :type data_set: `str`
    """
    print "Reading MovieLens ratings data set ..."
    dir = dirname(dirname(abspath(__file__))) + sep + 'datasets' + sep + 'MovieLens' + sep + data_set + '.base'
    V = sp.lil_matrix((943, 1682))
    for line in open(dir): 
        u, i, r, _ = map(int, line.split())
        V[u - 1, i - 1] = r
    return V 
    print "... Finished."
            
def preprocess(V):
    """
    Preprocess MovieLens data matrix. Normalize data.
    
    Return preprocessed target sparse data matrix in CSR format. Returned matrix's shape is 943 (users) x 1682 (movies). 
    The sparse data matrix is converted to CSR format for fast arithmetic and matrix vector operations. 
    
    :param V: The MovieLens data matrix. 
    :type V: `scipy.sparse.lil_matrix`
    """
    print "Preprocessing data matrix ..." 
    return V
    print "... Finished."    
            
def plot(W, H, data_set):
    """
    Plot the RMSE error rate on MovieLens data set. 
    
    :param W: Basis matrix of the fitted factorization model.
    :type W: `scipy.sparse.csr_matrix`
    :param H: Mixture matrix of the fitted factorization model.
    :type H: `scipy.sparse.csr_matrix`
    :param data_set: Name of the split data set to be read. 
    :type data_set: `str`
    """
    print "Plotting RMSE rates ..."
    print "... Finished."
    

if __name__ == "__main__":
    """Run the Recommendations example."""
    run()
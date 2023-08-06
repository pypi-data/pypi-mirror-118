import numpy as np
import scipy.linalg as la
import pandas as pd
from numpy.linalg import norm
from sklearn.cluster import KMeans

def HSC(y,r):
    '''
    High-order Spectral Clustering
    
    Input: 
    y: data
    r: vector representing number of clusters
    
    Output:
    z: initialization
    '''
    ranks = y.shape
    d = len(ranks)
    if len(r) != d:
        print("Different order in data and number of clusters. Please try again.\n")
        print("If certain orders are not to be clustered, use the function HSC_alt instead ")
        print("and set the corresponding number of clusters to be -1.")             
        return
    
    U_list = []
    for k in range(d):
        new_mat = np.moveaxis(y,k,0).reshape(ranks[k],-1)
        U_list.append(la.svd(new_mat,full_matrices=False)[0][:,:r[k]])
    
    U_hat_list = []
    for k in range(d):
        new_mat = y.copy()
        for i in range(d):
            if i == k:
                continue
            new_mat = np.moveaxis(np.tensordot(new_mat,U_list[i],axes=(i,0)),-1,i)
        new_mat = np.moveaxis(new_mat,k,0).reshape(ranks[k],-1)
        U_hat_list.append(la.svd(new_mat,full_matrices=False)[0][:,:r[k]])
    
    Y_hat_list = []
    for k in range(d):
        new_mat = y.copy()
        for i in range(d):
            if i == k:
                continue
            new_mat = np.moveaxis(np.tensordot(new_mat,U_hat_list[i],axes=(i,0)),-1,i)
        new_mat = np.moveaxis(new_mat,k,0).reshape(ranks[k],-1)
        Y_hat_list.append(U_hat_list[k] @ U_hat_list[k].T @ new_mat)
    
    z = []
    for k in range(d):
        kmeans = KMeans(n_clusters=r[k], random_state=0).fit(Y_hat_list[k])
        z.append(kmeans.labels_)
    
    return z

def HSC_alt(y,r):
    '''
    High-order Spectral Clustering if certain orders are not to be clustered
    
    Input: 
    y: data
    r: vector representing number of clusters
    
    Output:
    z: initialization
    '''
    ranks = y.shape
    if len(r) != len(ranks):
        print("Different order in data and number of clusters. Please try again.\n")
        print("If certain orders are not to be clustered, set the corresponding number of clusters to be -1.")             
        return
    
    d = [i for i in range(len(ranks)) if r[i] != -1]
    
    U_list = []
    for k in d:
        new_mat = np.moveaxis(y,k,0).reshape(ranks[k],-1)
        U_list.append(la.svd(new_mat,full_matrices=False)[0][:,:r[k]])
    
    U_hat_list = []
    for k in d:
        new_mat = y.copy()
        for ind,i in enumerate(d):
            if i == k:
                continue
            new_mat = np.moveaxis(np.tensordot(new_mat,U_list[ind],axes=(i,0)),-1,i)
        new_mat = np.moveaxis(new_mat,k,0).reshape(ranks[k],-1)
        U_hat_list.append(la.svd(new_mat,full_matrices=False)[0][:,:r[k]])
    
    Y_hat_list = []
    for indk,k in enumerate(d):
        new_mat = y.copy()
        for indi,i in enumerate(d):
            if i == k:
                continue
            new_mat = np.moveaxis(np.tensordot(new_mat,U_hat_list[indi],axes=(i,0)),-1,i)
        new_mat = np.moveaxis(new_mat,k,0).reshape(ranks[k],-1)
        Y_hat_list.append(U_hat_list[indk] @ U_hat_list[indk].T @ new_mat)
    
    z = []
    for indk,k in enumerate(d):
        kmeans = KMeans(n_clusters=r[k], random_state=0).fit(Y_hat_list[indk])
        z.append(kmeans.labels_)
    
    return z

def to_weight_matrix(z):
    '''
    Transform input (weight vector in each mode) to output (weight matrix in each mode)
    '''
    d = len(z)
    W = []
    for i in range(d):
        zi = z[i]
        pi = len(zi)
        ri = len(set(zi))
        Wi = np.zeros((ri, pi),dtype='float')
        for k in range(ri):
            zi_subset = np.where(zi==k)[0]
            Wi[k,zi_subset] = 1/len(zi_subset)
        W.append(Wi)
    return W

def HLloyd(y,z,T):
    """
    Implementation of HLloyd algorithm
    
    Input:
    y: data
    z: initialization
    T: number of iterations
    
    Output:
    z: estimated clustering labels
    """
    ranks = y.shape
    d = len(ranks)
    for t in range(T):
        W = to_weight_matrix(z)  # Transform weight vector to weight matrix in each mode
        S_hat = y.copy()
        for i in range(d):
            S_hat = np.moveaxis(np.tensordot(S_hat,W[i],axes=(i,1)),-1,i)
        S_ranks = S_hat.shape
        for i in range(d):
            S_hat_matrix = np.moveaxis(S_hat,i,0).reshape(S_ranks[i],-1)

            A_matrix = y.copy()
            for j in range(d):
                if j == i:
                    continue
                A_matrix = np.moveaxis(np.tensordot(A_matrix,W[j],axes=(j,1)),-1,j)
            A_matrix = np.moveaxis(A_matrix,i,0).reshape(ranks[i],-1)
        
            zi = np.fromiter(map(lambda j: np.argmin(norm(A_matrix[j] - S_hat_matrix, axis = 1)), 
                                 range(len(A_matrix))), dtype = 'int')
        
            z[i] = zi
    return z 

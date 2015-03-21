import numpy as np
import scipy.stats as stats

from sklearn.cross_validation import KFold, cross_val_score
from sklearn.linear_model import LassoCV

N=10
X_vec = stats.norm.rvs(size=N*N,loc=0,scale=1)
X_vec = X_vec.reshape(N,N)
Y_vec = stats.norm.rvs(size = N)

cv_outer = KFold(N,n_folds=3)

clf = LassoCV(eps=0.01, n_alphas=10,cv =3)

print cross_val_score(clf,X_vec,Y_vec,cv=cv_outer)




#print X_vec.shape
#print Y_vec.shape

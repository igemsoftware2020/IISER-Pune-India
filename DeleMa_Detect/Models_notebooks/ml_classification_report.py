import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import roc_curve, roc_auc_score

X ,Y = make_classification(n_samples=2000,n_classes=2,n_features=10,random_state=0)

random_state = np.random.RandomState(0)
n_samples,n_features = X.shape
X = np.c_[X,random_state.randn(n_samples,200*n_features)]

X_train,X_test,Y_train, Y_test = train_test_split(X,Y,test_size=0.2,random_state=0)


## Random Forest 

rf = RandomForestClassifier(max_features=1,n_estimators=500)
rf.fit(X_train,Y_train)


## Gaussian NB

nb = GaussianNB()
nb.fit(X_train,Y_train)

### Prediction probabilities :

r_probs = [0 for _ in range(len(Y_test))]
rf_probs = rf.predict_proba(X_test)
nb_probs = nb.predict_proba(X_test)


## probabilities for positive outcome is kept 

rf_probs = rf_probs[:,1]
nb_probs = nb_probs[:,1]


## Computing AUROC and ROC curve values

r_auc = roc_auc_score(Y_test,r_probs)
rf_auc = roc_auc_score(Y_test,rf_probs)
nb_auc = roc_auc_score(Y_test,nb_probs)

## Print AUROC scores

print("Random (chance) Prediction : AUROC = %.3f" %(r_auc))
print('Random Forest : AUROC = %.3f' %(rf_auc))
print('Naive Bayes : AUROC = %.3f' %(nb_auc))

## Calculate ROC curve

r_fpr, r_tpr , _ = roc_curve(Y_test, r_probs)
rf_fpr,rf_tpr, _ = roc_curve(Y_test, rf_probs)
nb_fpr, nb_tpr, _ = roc_curve(Y_test, nb_probs) 


### PLot the ROC curves

plt.plot(r_fpr,r_tpr, ls = '--', label='Random prediction (AUROC = %0.3f)' %(r_auc))
plt.plot(rf_fpr,rf_tpr, marker = ',', label='Random Forest (AUROC = %0.3f' %(rf_auc))
plt.plot(nb_fpr,nb_tpr, marker = '.', label='Naive Bayes (AUROC = %0.3f)' %(nb_auc))
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate') 

plt.legend()
plt.show()






































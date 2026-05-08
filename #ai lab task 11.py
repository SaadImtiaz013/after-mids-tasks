#ai lab task 11
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import BernoulliNB, GaussianNB, MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics
import matplotlib.pyplot as plt
data = pd.read_csv('data.csv', sep=None, engine='python', on_bad_lines='skip')
for col in data.columns:
    if data[col].isnull().any():
        data[col] = data[col].fillna(data[col].mode()[0])
cat_columns = data.select_dtypes(['object']).columns
data[cat_columns] = data[cat_columns].apply(lambda x: pd.factorize(x)[0])
x = data.iloc[:, 0:-1]
y = data.iloc[:, -1]
X_train, X_test, Y_train, Y_test = train_test_split(x, y, test_size=0.3, shuffle=False)
BernNB = BernoulliNB()
BernNB.fit(X_train, Y_train)
Y_bpred = BernNB.predict(X_test)
b_accuracy = metrics.accuracy_score(Y_test, Y_bpred)
print('Bernoulli Accuracy: %f' % b_accuracy)
RF = RandomForestClassifier()
RF.fit(X_train, Y_train)
Y_rpred = RF.predict(X_test)
r_accuracy = metrics.accuracy_score(Y_test, Y_rpred)
print('Random Forest Accuracy: %f' % r_accuracy)
GausNB = GaussianNB()
GausNB.fit(X_train, Y_train)
Y_gpred = GausNB.predict(X_test)
g_accuracy = metrics.accuracy_score(Y_test, Y_gpred)
print('Gaussian Accuracy: %f' % g_accuracy)
Dtree = DecisionTreeClassifier()
Dtree.fit(X_train, Y_train)
Y_dpred = Dtree.predict(X_test)
d_accuracy = metrics.accuracy_score(Y_test, Y_dpred)
print('Decision Tree Accuracy: %f' % d_accuracy)
MultiNB = MultinomialNB()
MultiNB.fit(X_train, Y_train)
Y_mpred = MultiNB.predict(X_test)
m_accuracy = metrics.accuracy_score(Y_test, Y_mpred)
print('Multinomial Accuracy: %f' % m_accuracy)
KNN = KNeighborsClassifier()
KNN.fit(X_train, Y_train)
Y_kpred = KNN.predict(X_test)
k_accuracy = metrics.accuracy_score(Y_test, Y_kpred)
print('KNN Accuracy: %f' % k_accuracy)
plt.figure(figsize=(10,6))
x1 = np.array(['Bernoulli', 'Random Forest', 'Gaussian', 'Decision Tree', 'Multinomial', 'KNeighbors'])
y1 = np.array([b_accuracy, r_accuracy, g_accuracy, d_accuracy, m_accuracy, k_accuracy])
plt.bar(x1, y1, color=['#08737f', '#00898a', '#089f8f', '#39b48e', '#64c987', '#92dc7e'])
plt.title("Scores of Applied Classifiers")
plt.xlabel('Classifiers')
plt.ylabel('Accuracy')
plt.show()
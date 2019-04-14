#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np


# In[2]:


data = pd.read_csv('./data.csv')

data = data.transpose()
data = data.assign(target_class='target')


for (i, row) in data.iterrows():
    row['target_class'] = row.name
    

data = data.reset_index(drop=True)

data.describe()


# In[3]:


#import sys

newDataset = []

for (i, row) in data.iterrows():
    for c in data:
        newDataset.append([str (row[c]), row['target_class']])


# In[4]:


newDf = pd.DataFrame(newDataset, columns = ['value', 'target_class'])

newDf.shape


# In[5]:


newDf.describe()


# In[6]:


# split into training set and test set

from sklearn.model_selection import train_test_split

newDf = newDf.sample(n=50000, random_state=1)

x=newDf['value'].values
y=newDf['target_class'].values

train_input, test_input, class_train, class_test = train_test_split(x, y, test_size=0.20, random_state=1000)


# In[7]:


from sklearn import feature_extraction
count_vect = feature_extraction.text.CountVectorizer(ngram_range=(1,2), analyzer="char")

count_vect.fit(train_input)
count_vect.fit(test_input)

X_train = count_vect.transform(train_input)
X_test = count_vect.transform(test_input) 

#b = count_vect.fit_transform(newDf.value)


# In[8]:


from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2


selector = SelectKBest(chi2, k=1000)
X_train = selector.fit_transform(X_train, class_train)

cols = selector.get_support(indices=True)
# Create new dataframe with only desired columns, or overwrite existing
colsDf = pd.DataFrame(cols)


# In[9]:


from sklearn.linear_model import LogisticRegression

classifier = LogisticRegression()

classifier.fit(X_train, class_train)

score = classifier.score(X_test, class_test)
score


# In[ ]:


# deep learning model
#import tensorflow as tf

#def train_input_fn(features, labels, batch_size):
#    """An input function for training"""
#    # Convert the inputs to a Dataset.
#    dataset = tf.data.Dataset.from_tensor_slices((dict(features), labels))
#
#    # Shuffle, repeat, and batch the examples.
#    return dataset.shuffle(1000).repeat().batch(batch_size)


#classifier = tf.estimator.DNNClassifier(
#    feature_columns=colsDf,
#    hidden_units=[10,10],
#    n_classes=34
#)

#classifier.train(
#    input_fn=lambda: train_input_fn(X_train, class_train, 10),
#    steps=100)


# In[ ]:


# from keras.models import Sequential
#from keras import layers
#from sklearn import preprocessing

#le = preprocessing.LabelEncoder()

#class_train = le.fit_transform(class_train)
#class_test = le.fit_transform(class_test)


#print(class_train[0:20])


# In[ ]:


#from scipy.sparse import csr_matrix


#csr_matrix.todense(X_train)


# In[ ]:


#X_train[1:10]
#X_test[1:10]


# In[ ]:


#from sklearn.naive_bayes import GaussianNB

#model = GaussianNB()


#model.fit(X_train,class_train)


#y_pred = model.predict(X_test)


# In[ ]:


#input_dim = X_train.shape[1]

#model = Sequential()

#model.add(layers.Dense(10, input_dim=input_dim, activation='relu'))
#model.add(layers.Dense(1, activation='sigmoid'))

#model.compile(loss='binary_crossentropy', 
#              optimizer='adam', 
#              metrics=['accuracy'])
#model.summary()


# In[ ]:


#history = model.fit(X_train, class_train,
#                    epochs=100,
#                    verbose=True,
#                    validation_data=(X_test, class_test),
#                    batch_size=10)


# In[ ]:


#loss, accuracy = model.evaluate(X_train, class_train, verbose=False)
#print("Training Accuracy: {:.4f}".format(accuracy))
#loss, accuracy = model.evaluate(X_test, class_test, verbose=False)
#print("Testing Accuracy:  {:.4f}".format(accuracy))


# In[ ]:


#X_train.shape


# In[ ]:





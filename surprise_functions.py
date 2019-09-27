#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error
from sklearn.impute import SimpleImputer
from surprise.prediction_algorithms.matrix_factorization import SVDpp, SVD
from surprise.prediction_algorithms.knns import KNNBasic
from surprise import Reader, Dataset
from surprise.model_selection import train_test_split


# In[2]:


#Initialize surprise dataset and split into training and test set

def load_surprise_data(df):
    """
    Parameters: 
    df:  Dataframe contaning user, book and ratings data
    
    Returns:
    
    rat_data: surprise full raw dataset
    train: full data prepared as surprise training set
    """
    reader = Reader()
    rat_data = Dataset.load_from_df(df[['uid', 'bid', 'rating']], reader)
    train = rat_data.build_full_trainset()
    return rat_data, train


# In[3]:


def build_model(train,method ='svd'):
    
    """Builds model and makes predictions for user-book rating.
    
    Args:
    train(surprise trainset): training set for the model to train on
    
    method (string): Method to use. Either 'knn' or 'svd'. Deafault is 'svd'. 
    
    Returns: list of Prediction objects.
    
    """
    
    if method == 'knn':
        surprise_sim_opt = {'name':'cosine','user_based':False}
        model = KNNBasic(k=100, min_k=20,sim_options = surprise_sim_opt)
    else:
        model = SVD(n_epochs=50)
        
    
    model.fit(train)
    
    
    test = train.build_anti_testset()
    pred = model.test(testset)
    
    return pred


# In[8]:


def get_top_n(predictions, n=5):
    '''Return the top-N recommendation for each user from a set of predictions.

    Args:
        predictions(list of Prediction objects): The list of predictions, as
            returned by the test method of an algorithm.
        n(int): The number of recommendation to output for each user. Default
            is 10.

    Returns: top_n (array): array of shape (num_users, n) with top n predictions for each user id.
    
    '''
    n_users = 1517
    n_books = 9501
    # Creates a matrix with shape (n_users, n_books).
    rat_pred = np.zeros((n_users,n_books))
    
    # Fills the matrix with the average rating for book weighted by a factor of 0.8 to ensure booksthat are personally matched with users gets returned first.
    for bid in range(rat_pred.shape[1]):
        rat_pred[:,bid] = users.loc[users['bid']==bid]['b_average_rating'].iloc[0]*0.8*div_m.iloc[int(bid)][1]

    #Fills in actual prediction for given user id, book id combination where the estimate is non-zero.
    for uid, bid, true_r, est, _ in predictions:
        if est > 0.6:
            rat_pred[int(uid)][int(bid)] = est*div_m.iloc[int(bid)][1]

    # Sorts the predictions for each user and retrieve the n highest ones.
    top_n = np.zeros((rat_pred.shape[0],n))
    
    for uid in range(rat_pred.shape[0]):
        top_n[uid] = rat_pred[uid].argsort()[::-1][:n]
            
    return top_n


# In[12]:


def id_from_title(df,title=''):
    
    gid = title_to_id[title]
    
    return user_df.loc[users['goodreads_book_id']==gid].bid.iloc[0]


# In[7]:


def titles_from_ids(df,bids=[1]):
    
    """Retrives title of the book from book id from the dataframe.
    Args: df: Pandas dataframe from which to retrieve the information.
    bids (list): list of book ids for which we need the titles. 
    
    Returns: titles(list): List of titles from provided book ids.
    """
    titles = []
    
    for bid in bids:
        titles.append(df.loc[df['bid']==bid]['title'].iloc[0])
    
    return titles


# In[5]:


def get_n_rec_user(user_id,model,testset):
    
    tst = []
    for (uid,bid,rat) in testset:
        if uid == user_id:
            tst.append((uid,bid,rat))
        continue
        
    pred = model.test(tst)
    
    topn = get_top_n(pred,n=5)
    
    return topn


# In[ ]:




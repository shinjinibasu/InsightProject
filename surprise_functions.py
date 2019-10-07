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
    
    return df.loc[users['goodreads_book_id']==gid].bid.iloc[0]


# In[7]:

def titles_authors_from_ids(df,bids=[1]):
    
    """Retrives title and authors of the book from book id from the dataframe.
    Args: df: Pandas dataframe from which to retrieve the information.
    bids (list): list of book ids for which we need the titles. 
    
    Returns: (list): List of titles from provided book ids.
    """
    titles = []
    authors = []
    
    for bid in bids:
        titles.append(df.loc[df['bid']==bid]['title'].iloc[0])
        authors.append(df.loc[df['bid']==bid]['author'].iloc[0])
    
    return [m + ' by ' +n for m,n in zip(titles,authors)]



# ln[ ]:


def get_n_rec_user(df,user_id,model,div_m,testset,n=5):
    
    """Return the top-N recommendation for an individual user given the model and a testset.

    Args:

        df: dataframe containing information about books and users
        user_id(int): user id
        model: model to use for prediction
        div_m: dataframe containing information if the books are diverse.
            has two columns: bid and is_div (0 or 1).
            used for masking non-diverse recs. 
        testset(list): list of tuples containing (user_id, book_id, <placeholder rating to be predicted>)

        n(int): The number of recommendation to output for each user. Default
            is 5.

    Returns: rec_n (list): list of length (n) with top n predictions for given user id.
    """
    n_books=9501
    tst = testset.loc[testset['0']==user_id].to_records(index=False).tolist()    
    pred = model.test(tst)
    
    # Creates a matrix with shape (n_books).
    rat_pred = np.zeros(n_books)
    # Finds user's favorite genre and the books in that genre.
    gen_u = df.loc[df.uid==user_id]['fav_genre'].iloc[0]
    blist = list(df.loc[df.genre == gen_u]['bid'].astype(int).unique())
    
    # Fills the matrix with the average rating for book weighted by a weight factor to ensure booksthat are personally matched with users gets returned first.
    for bid in range(len(rat_pred)):
        if bid in blist:
            rat_pred[bid] = df.loc[df['bid']==bid]['b_average_rating'].iloc[0]*div_m.iloc[int(bid)][1]*0.85

    #Fills in actual prediction for given user id, book id combination where the estimate is non-zero.
    for uid, bid, true_r, est, _ in pred:
        if est > 0.6:
            rat_pred[int(bid)] = est*div_m.iloc[int(bid)][1]

    # Sorts the predictions for each user and retrieve the n highest ones.
    top_n = rat_pred.argsort()[::-1][:n]
    
    rec_n = titles_authors_from_ids(df,bids=list(top_n))
    
    return rec_n


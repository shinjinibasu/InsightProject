from flask import render_template, request, redirect
from flaskexample import app
import os
import numpy as np
import pandas as pd
from surprise import dump
from surprise.prediction_algorithms.matrix_factorization import SVD
from surprise_functions import get_n_rec_user
import csv

@app.route('/')
@app.route('/getrec',methods=['POST','GET'])
def form_example():
   genres = ['sci-fi/fantasy', 'young-adult', 'contemporary',
             'adult-fiction','any']
   path = "C:/Users/shinj/Anaconda3/envs/insight/insight_project"
   
   with open(os.path.join(path,'name_id_map.csv'),mode='r') as infile:
      reader = csv.reader(infile)
      name_dict = {}
      for row in reader:
         k = row[0]
         if k in name_dict:
         # implement your duplicate row handling here
            pass
         name_dict[k] = int(row[1])


   if request.method == 'POST':  #this block is only entered when the form is submitted
      user_id = request.form.get('user_id')
      genre = request.form.get('genre')
      full_string = '<br>'.join(["Alanna: The First Adventure",
                                      "The Hunger Games","Pure",
                                    "Half of a Yellow Sun","Under the Udala Tree"])

      #### Model goes here 
      _,model = dump.load(os.path.join(path,'surprise_svd_dump_file'))      

      test = pd.read_csv(os.path.join(path,'testset.csv'))
      user_df = pd.read_csv(os.path.join(path,'goodreads2/user_w_uid_bavg_titles.csv'))
      div_m = pd.read_csv(os.path.join(path,'goodreads2/div_array.csv'))


      ###Model output goes here
      if user_id in name_dict.keys():
         u_id = name_dict[user_id]
         rec = get_n_rec_user(user_df,u_id,model,div_m,test)
         full_string = '<br>'.join(rec)
         full_string=full_string.replace('The New Jim Crow: Mass Incarceration in the Age of Colorblindness','The Hate U Give')
      
      template_dict = {
            'user_id' : user_id,
            'genre' : genre,
            'full_string': full_string
            }
      return render_template('bs_test_results.html',genres=genres,**template_dict)
    
   return render_template('bs_test.html', genres=genres)

@app.route('/index')
def index():
   user = { 'nickname': 'Ainsel' } # fake user
   return render_template("index.html", title = 'Home', user = user)




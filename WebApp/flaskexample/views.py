from flask import render_template, request, redirect
from flaskexample import app
import os
import numpy as np
import pandas as pd
from surprise import dump
from surprise.prediction_algorithms.matrix_factorization import SVD
from surprise_functions import get_n_rec_user

@app.route('/')
@app.route('/getrec',methods=['POST','GET'])
def form_example():
   genres = ['sci-fi/fantasy', 'young-adult', 'contemporary',
             'adult-fiction','any']
   path = "C:/Users/shinj/Anaconda3/envs/insight/insight_project"
   
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
      u_id=1200
      u_id=1200
      names = ['Brianne', 'John', 'Bennett','Brandon', 'Yaarit','Danila', 'Daliang',
          'Steven', 'Randolph', 'Alex', 'Gary', 'Julia', 'Ilia', 'Chang', 'Daniel', 'Kai',
          'Jason', 'Victoria', 'Antoine', 'Wenke', 'Avi', 'Jesse', 'Anna', 'Nina', 'Paul', 'Avery', 'Hugo', 'Charlie', 'Dewey', 'Jamel', 'Magdalena', 'Molly', 'Sherry', 'Curtis', 'Thad', 'Junior', 'Seymour', 'Betty', 'Otto', 'Elsie', 'May', 'Marcelino', 'Roger', 'Graciela', 'Ashley','Antony', 'Tameka', 'Andreas', 'Fermin',
          'Garland', 'Sol', 'Joshua', 'Gavin', 'Whitney', 'Shelby', 'Coy', 'Wm', 'Myra', 'Dalton', 'Williams', 'Danial', 'Sophia', 'Krista', 'Samuel',
          'Polly', 'Veronica', 'Winfred', 'Erwin', 'Tonya', 'Markus', 'Marisa', 'Houston', 'Numbers', 'Kris', 'Darcy', 'Kenny', 'Dwight', 'Ronda', 'Clarice', 'Wendell', 'Gerardo', 'Millard', 'Jeffry', 'Mitch', 'Haywood',
          'Dylan', 'Terrence', 'Jeanne', 'Leopoldo', 'Clifton', 'Cornelius', 'Linwood', 'Rolando', 'Alyson',
          'Darren', 'Maximo', 'Vance', 'Rocky', 'Robert', 'Darrin', 'Cole', 'Augusta', 'Gilberto', 'Eloy', 'Dino',
          'Malcolm', 'Bessie', 'Roseann', 'Norman', 'Allyson', 'Abe', 'Antwan', 'Stevie', 'Claudio', 'Blair', 'Keisha', 'Goldie',
          'Lucy', 'Byron', 'Reyes', 'Zachery', 'Stefan', 'Aron', 'Cecile', 'Brent', 'Adam', 'Emily', 'Allen',
          'Donald', 'Amanda', 'Kim', 'Jen', 'Jolene', 'Ethan', 'Dennis', 'Taissa', 'Ricardo', 'Alyssa']

      if user_id in names:
         u_id = 1445
      
      if user_id == 'Shinjini':
         #full_string = '<br>'.join(["The Fifth Season","Americanah",
                                      #"Poisonwood Bible",
                                      #"Alanna: The First Adventure",
                                      #"Bayou Moon"])
         
         u_id = 1500
         ### model output goes here      
      rec = get_n_rec_user(user_df,u_id,model,div_m,test)
      full_string = '<br>'.join(rec)

      template_dict = {
            'user_id' : user_id,
            'genre' : genre,
            'full_string': full_string
            }
      return render_template('bs_test.html',genres=genres,**template_dict)
    
   return render_template('bs_test.html', genres=genres)
    


@app.route('/index')
def index():
   user = { 'nickname': 'Ainsel' } # fake user
   return render_template("index.html", title = 'Home', user = user)




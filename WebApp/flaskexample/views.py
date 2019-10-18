from flask import render_template, request, redirect
from flaskexample import app
import os
import numpy as np
import pandas as pd
from surprise import dump
from surprise.prediction_algorithms.matrix_factorization import SVD
from surprise_functions import get_n_rec_user
import csv

@app.route('/',methods=['POST','GET'])
@app.route('/getrec',methods=['POST','GET'])
def form_example():
   genres = ['science-fiction','fantasy','young-adult','historical-fiction','graphic-novel','adult','mystery','any']
   path = "C:/Users/shinj/Anaconda3/envs/insight/insight_project"
   genre_dict = pickle.load(open(os.path.join(path,'goodreads2/genrelist.p'),'rb'))
   name_rec = pickle.load(open(os.path.join(path,'goodreads2/name_rec.p'),"rb"))
   
   if request.method == 'POST':  #this block is only entered when the form is submitted
      user_id = request.form.get('user_id')
      genre = request.form.get('genre')
      full_string = ''
      template_dict = {
            'user_id' : user_id,
            'genre' : genre,
            'full_string': full_string
             }
      ###Model output goes here
      if user_id in name_rec.keys():
         full_string = '<br>'.join(name_rec[user_id])
         template_dict = {
            'user_id' : user_id,
            'genre' : genre,
            'full_string': full_string
             }
      
         out_template = render_template('bs_test_results.html',genres=genres,**template_dict)

      else:
         df = genre_dict[genre]         
         if genre == 'any':
            df = df.sample(n=20).sort_values('Average Rating',ascending=False).reset_index(drop=True)
         tables = [df.to_html(classes='data')]
         titles = df.columns.values
         out_template = render_template('test_results.html',genres=genres,tables=tables,
            titles=titles,
           **template_dict)
         
      return out_template
   return render_template('bs_test.html', genres=genres)
   
@app.route('/index')
def index():
   user = { 'nickname': 'Ainsel' } # fake user
   return render_template("index.html", title = 'Home', user = user)




import pandas as pd

""" Расчет и вывод рейтинга для каждого фильма
       на основе оценок всех пользователей """

data = pd.read_csv('ratings.csv')
rating_of_movies = data.pivot_table(index = ['movieId', 'rating'],
    values = 'timestamp', aggfunc = 'count').reset_index()
rating_of_movies['sum'] = rating_of_movies.groupby('movieId').timestamp.transform(lambda x: sum(x))
rating_of_movies['mul'] = rating_of_movies['rating'] * rating_of_movies['timestamp']
rating_of_movies['sum_of_marks'] = rating_of_movies.groupby('movieId').mul.transform(lambda x: sum(x))
rating_of_movies['rating'] = rating_of_movies['sum_of_marks'] / rating_of_movies['sum']
del rating_of_movies['timestamp']
del rating_of_movies['sum']
del rating_of_movies['mul']
del rating_of_movies['sum_of_marks']
movies = pd.read_csv('movies.csv')
rating_of_movies['movie'] = movies['title']
rating_of_movies.drop_duplicates('movieId', inplace = True)
print (rating_of_movies.head(700).sort_values('rating', ascending = False))

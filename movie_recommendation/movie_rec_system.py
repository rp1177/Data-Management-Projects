# FILL IN ALL THE FUNCTIONS IN THIS TEMPLATE
# MAKE SURE YOU TEST YOUR FUNCTIONS WITH MULTIPLE TEST CASES
# ASIDE FROM THE SAMPLE FILES PROVIDED TO YOU, TEST ON YOUR OWN FILES

# WHEN DONE, SUBMIT THIS FILE TO CANVAS

from collections import defaultdict
from collections import Counter

# YOU MAY NOT CODE ANY OTHER IMPORTS

# ------ TASK 1: READING DATA  --------

# 1.1
def read_ratings_data(f):
    # parameter f: movie ratings file name f (e.g. "movieRatingSample.txt")
    # return: dictionary that maps movie to ratings
    # WRITE YOUR CODE BELOW

    rate_list = {} #create empty ratings dictionary

    for line in open(f):
        movie_and_year,rating,count= line.split('|')
        if movie_and_year in rate_list:
            rate_list[movie_and_year].append(rating) #add to the key if the movie already exists, makes a list like extension
        else:
            rate_list[movie_and_year] = [rating] #create a new key that will have the corresponding rating to it
        
    return rate_list

    

# 1.2
def read_movie_genre(f):
    # parameter f: movies genre file name f (e.g. "genreMovieSample.txt")
    # return: dictionary that maps movie to genre
    # WRITE YOUR CODE BELOW
    movie_genre = {} #create empty movie_genre dictionary

    for line in open(f):
        genre,count,movie= line.split('|')
        movie_genre[movie.strip()] = genre

    return movie_genre

# ------ TASK 2: PROCESSING DATA --------

# 2.1
def create_genre_dict(d):
    # parameter d: dictionary that maps movie to genre
    # return: dictionary that maps genre to movies
    # WRITE YOUR CODE BELOW

    genre_dict = {} #empty dictionary to sort out genres
    
    extract_values = []
    extract_keys = []
    
    counter_val = 0
    
    for item in d.values(): #populate extract_values list
        extract_values.append(item)
    
    for key in d:  #populate extract_keys list
        extract_keys.append(key)
        
    for val in extract_values:
        
        if val in genre_dict:
            genre_dict[val].append(extract_keys[counter_val])
        
        else:
            genre_dict[val] = [extract_keys[counter_val]]
            
        counter_val+=1


    return genre_dict

    
# 2.2
def calculate_average_rating(d):
    # parameter d: dictionary that maps movie to ratings
    # return: dictionary that maps movie to average rating
    # WRITE YOUR CODE BELOW
    average_rating = {} #create the dictionary we want to return 
    
    average_list = [] #get the averages of each value-list in the task 1.1 dictionary
    counter=0
    
    for values in d.values():
        values = [float(i) for i in values] #convert to int
        average_list.append(sum(values) / len(values))
        
    for key in d:
        average_rating[key] = average_list[counter]
        counter+=1
        
    return average_rating
    
# ------ TASK 3: RECOMMENDATION --------

# 3.1
def get_popular_movies(d, n=10):
    # parameter d: dictionary that maps movie to average rating
    # parameter n: integer (for top n), default value 10
    # return: dictionary that maps movie to average rating, 
    #         in ranked order from highest to lowest average rating
    # WRITE YOUR CODE BELOW
    
    if len(d) < n:
        final = sorted(d.items(), key=lambda x: x[1], reverse=True)
    else:
        final = sorted(d.items(), key=lambda x: x[1], reverse=True)[:n]
        
    return dict(final)

# 3.2
def filter_movies(d, thres_rating=3):
    # parameter d: dictionary that maps movie to average rating
    # parameter thres_rating: threshold rating, default value 3
    # return: dictionary that maps movie to average rating
    filter_dict = {}
    
    for i in d:
        if d[i] >= thres_rating:
            filter_dict[i] = d[i]
        
        
    return filter_dict
    
# 3.3
def get_popular_in_genre(genre, genre_to_movies, movie_to_average_rating, n=5):
    # parameter genre: genre name (e.g. "Comedy")
    # parameter genre_to_movies: dictionary that maps genre to movies
    # parameter movie_to_average_rating: dictionary  that maps movie to average rating
    # parameter n: integer (for top n), default value 5
    # return: dictionary that maps movie to average rating
    
    final_dict = {}
    
    if genre in genre_to_movies:
        for j in genre_to_movies[genre]: #traverse the movie values in each genre
            if j in movie_to_average_rating:
                final_dict[j] = movie_to_average_rating[j]
                
    if len(final_dict) < n:
        result = sorted(final_dict.items(), key=lambda x: x[1], reverse=True)
    else:
        result = sorted(final_dict.items(), key=lambda x: x[1], reverse=True)[:n]
        

    return dict(result)
    
    
# 3.4
def get_genre_rating(genre, genre_to_movies, movie_to_average_rating):
    # parameter genre: genre name (e.g. "Comedy")
    # parameter genre_to_movies: dictionary that maps genre to movies
    # parameter movie_to_average_rating: dictionary  that maps movie to average rating
    # return: average rating of movies in genre
    # WRITE YOUR CODE BELOW
    
    genre_average = 0
    movie_val = []
    if genre in genre_to_movies:
        for j in genre_to_movies[genre]: #traverse the movie values in each genre
            if j in movie_to_average_rating:
                movie_val.append(movie_to_average_rating[j])
    return sum(movie_val) / len(movie_val)
    

# 3.5
def genre_popularity(genre_to_movies, movie_to_average_rating, n=5):
    # parameter genre_to_movies: dictionary that maps genre to movies
    # parameter movie_to_average_rating: dictionary  that maps movie to average rating
    # parameter n: integer (for top n), default value 5
    # return: dictionary that maps genre to average rating
    
    final_dict = {}
    
    for i in genre_to_movies: #traverse the movie values in each genre
        final_dict[i] = get_genre_rating(i, genre_to_movies, movie_to_average_rating)
            
    if len(final_dict) < n:
        final_result = sorted(final_dict.items(), key=lambda x: x[1], reverse=True)
        return dict(final_result)
    else:
        final_result = sorted(final_dict.items(), key=lambda x: x[1], reverse=True)[:n]
        return dict(final_result)

# ------ TASK 4: USER FOCUSED  --------

# 4.1
def read_user_ratings(f):
    # parameter f: movie ratings file name (e.g. "movieRatingSample.txt")
    # return: dictionary that maps user to list of (movie,rating)
    # WRITE YOUR CODE BELOW
    final_dict = {}
    
    for line in open(f):
        movie,rating,user_id=line.strip().split('|')
        if user_id not in final_dict:
                final_dict[user_id] = []
        final_dict[user_id].append((movie, float(rating)))
            
    return final_dict
    
# 4.2
def get_user_genre(user_id, user_to_movies, movie_to_genre):
    # parameter user_id: user id
    # parameter user_to_movies: dictionary that maps user to movies and ratings
    # parameter movie_to_genre: dictionary that maps movie to genre
    # return: top genre that user likes
    # WRITE YOUR CODE BELOW
    def get_user_genre(user_id, user_to_movies, movie_to_genre):
    # parameter user_id: user id
    # parameter user_to_movies: dictionary that maps user to movies and ratings
    # parameter movie_to_genre: dictionary that maps movie to genre
    # return: top genre that user likes
        average= 0
        tracker = {}
    
        if user_id in user_to_movies:
            for counter in range(len(user_to_movies[user_id])):
                for movie in movie_to_genre:
                    if movie == user_to_movies[user_id][counter][0]:
                        if movie_to_genre[movie] not in tracker:
                            tracker[movie_to_genre[movie]] = []
                
                        tracker[movie_to_genre[movie]].append(user_to_movies[user_id][counter][1])
    
    
        average_max=0 #default
        for v in tracker:
            #print(tracker[v], v)
            average = ( sum(tracker[v]) / len(tracker[v]) )
        
            if average >= average_max:
                average_max = average
                topgenre = v
                
            average = 0 #reset
        
        return topgenre
    
# 4.3    
def recommend_movies(user_id, user_to_movies, movie_to_genre, movie_to_average_rating):
    # parameter user_id: user id
    # parameter user_to_movies: dictionary that maps user to movies and ratings
    # parameter movie_to_genre: dictionary that maps movie to genre
    # parameter movie_to_average_rating: dictionary that maps movie to average rating
    # return: dictionary that maps movie to average rating
    # WRITE YOUR CODE BELOW
    
    c = get_user_genre(user_id, user_to_movies, movie_to_genre) #get a user's top genre based on average
    movies_seen = [] #list of movies already rated by user and is top genre.
    final_dict = {}
    

    for m in movie_to_genre:
        for movie in user_to_movies[user_id]:
             if movie_to_genre[m] == c and m == movie[0]: #if genres are same and movies in user vers = to m in movie_to_genre
                movies_seen.append(m)                                    
         
    for movie in movie_to_genre:
        if movie not in movies_seen and movie_to_genre[movie] == c:
            if movie in movie_to_average_rating:
                final_dict[movie] = movie_to_average_rating[movie]

    
    if len(final_dict) == 0:
        print("Watched all recommended movies in list.")
        
    elif len(final_dict) < 3:
        result = sorted(final_dict.items(), key=lambda x: x[1], reverse=True)
        return dict(result)
    else:
        result = sorted(final_dict.items(), key=lambda x: x[1], reverse=True)[:3]
        return dict(result)

# -------- main function for your testing -----
def main():
    # write all your test code here
    # this function will be ignored by us when grading
    
    pass
    
# DO NOT write ANY CODE (including variable names) outside of any of the above functions
# In other words, ALL code your write (including variable names) MUST be inside one of
# the above functions
    
# program will start at the following main() function call
# when you execute hw1.py
main()

    
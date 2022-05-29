import streamlit as st
import pickle
import pandas as pd
import requests
from PIL import Image

# Bootstrap
st.markdown(
    """
<script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.10.2/dist/umd/popper.min.js" integrity="sha384-7+zCNj/IqJ95wo16oMtfsKbZ9ccEh31eOz1HGyDuCQ6wgnyJNSYdrPa03rtR1zdB" crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.min.js" integrity="sha384-QJHtvGhmr9XOIpI6YVutG+2QOK9T+ZnN4kzFN1RtK3zEFEIsxhlmWl5/YESvpZ13" crossorigin="anonymous"></script>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
""",
    unsafe_allow_html=True,
)

my_api_key = "8733b6301205356312386e556cc10249"


def fetch_poster(movie_id):
    response = requests.get(
        "https://api.themoviedb.org/3/movie/{}?api_key=8733b6301205356312386e556cc10249&language=en-US".format(
            movie_id, my_api_key
        )
    )
    data = response.json()
    if data["poster_path"] == None:
        poster_path = "https://picsum.photos/500/750"
    else:
        poster_path = "https://image.tmdb.org/t/p/w500/" + data["poster_path"]

    if data["overview"] == None:
        overview = "No Data"
    else:
        overview = data["overview"]

    if data["vote_average"] == None:
        vote_average = "No Data"
    else:
        vote_average = data["vote_average"]

    if data["imdb_id"] == None:
        imdb_id = "https://www.imdb.com/title/tt1762742"
    else:
        imdb_id = "https://www.imdb.com/title/" + data["imdb_id"]

    return poster_path, overview, vote_average, imdb_id


def recommend(movie_title):
    movie_index = movies[movies["title"] == movie_title].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[
                  1:13
                  ]

    top_recommended_movies = []
    top_recommended_movies_posters = []
    top_recommended_movies_overview = []
    top_recommended_movies_vote_average = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        # fetch poster from API
        poster_url, overview_text, vote_average, imdb_id = fetch_poster(movie_id)
        top_recommended_movies_posters.append(poster_url)
        top_recommended_movies_overview.append(overview_text)
        top_recommended_movies_vote_average.append(vote_average)
        top_recommended_movies.append(movies.iloc[i[0]].title)

    return (
        top_recommended_movies,
        top_recommended_movies_posters,
        top_recommended_movies_overview,
        top_recommended_movies_vote_average,
    )


movies_dict = pickle.load(open("movies_dict.pkl", "rb"))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open("similarity.pkl", "rb"))

heading = '<h1 style="color:black;">Movie Mania</h1>'
st.markdown(heading, unsafe_allow_html=True)
subheading = '<p style="color:grey; font-size: 20px;">Enter a movie name<span></span></p>'
st.markdown(subheading, unsafe_allow_html=True)

sec1, sec2 = st.columns(2)

with sec1:
    selected_movie_name = st.selectbox("", movies["title"].values)
with sec2:
    pass

rec_button = st.button("Recommend")

st.markdown(
    '<h3>Now Checking : <span style="color:red;">{}</span></h3>'.format(
        selected_movie_name
    ),
    unsafe_allow_html=True,
)
# Selected movie utils

selected_movie_index = movies[movies["title"] == selected_movie_name].index[0]
selected_movie_index = movies[movies["title"] == selected_movie_name]["movie_id"]
(
    selected_poster_path,
    selected_movie_overview,
    selected_vote_average,
    selected_movie_imdb_id,
) = fetch_poster(int(selected_movie_index))

st.markdown(
    """
<div class="card bg-black text-white">
  <img src="{}" class="card-img-top" />
  <div class="card-body">
    <h1 class="card-title">{}</h1>
    <h3 class="text-info">{}</h3>
    <h4 class="card-text">
      {}
    </h4>
     <a target="_blank" href={}>IMDB Page</a>
  </div>
</div>
<hr>
""".format(
        selected_poster_path,
        selected_movie_name,
        selected_vote_average,
        selected_movie_overview,
        selected_movie_imdb_id,
    ),
    unsafe_allow_html=True,
)

if rec_button:
    names, posters, overviews, vote_averages = recommend(selected_movie_name)
    num = 1
    row1 = st.columns(4)
    for i in range(4):
        if i >= len(names):
            break
        with row1[i]:
            st.markdown(
                "<h5>{}</h5>".format(str(num) + ". " + names[i]), unsafe_allow_html=True
            )
            review = '<h3 style="color:red;">{}</h3>'.format(str(vote_averages[i]))
            st.markdown(review, unsafe_allow_html=True)
            num += 1
            st.image(posters[i])
            st.markdown(
                """
                    <button type="button" class="btn btn-info" data-bs-toggle="tooltip" data-bs-placement="top" title="{}">
                         Know More
                    </button>
              """.format(
                    overviews[i].replace('"', "`")
                ),
                unsafe_allow_html=True,
            )

    st.markdown("<hr>", unsafe_allow_html=True)
    row2 = st.columns(4)
    for i in range(4, 8):
        if i >= len(names):
            break
        with row2[i - 4]:
            st.markdown(
                "<h5>{}</h5>".format(str(num) + ". " + names[i]), unsafe_allow_html=True
            )
            review = '<h3 style="color:red;">{}</h3>'.format(str(vote_averages[i]))
            st.markdown(review, unsafe_allow_html=True)
            num += 1
            st.image(posters[i])
            st.markdown(
                """
                    <button type="button" class="btn btn-info" data-bs-toggle="tooltip" data-bs-placement="top" title="{}">
                         Know More
                    </button>
              """.format(
                    overviews[i].replace('"', "`")
                ),
                unsafe_allow_html=True,
            )

    st.markdown("<hr>", unsafe_allow_html=True)
    row3 = st.columns(4)
    for i in range(8, 12):
        if i >= len(names):
            break
        with row3[i - 8]:
            st.markdown(
                "<h5>{}</h5>".format(str(num) + ". " + names[i]), unsafe_allow_html=True
            )
            review = '<h3 style="color:red;">{}</h3>'.format(str(vote_averages[i]))
            st.markdown(review, unsafe_allow_html=True)
            num += 1
            st.image(posters[i])
            st.markdown(
                """
                    <button type="button" class="btn btn-info" data-bs-toggle="tooltip" data-bs-placement="top" title="{}">
                         Know More
                    </button>
              """.format(
                    overviews[i].replace('"', "`")
                ),
                unsafe_allow_html=True,
            )

    st.markdown("<hr>", unsafe_allow_html=True)

hide_st_style = """
               <style>
               #MainMenu {visibility : hidden;}
               footer {visibility : hidden;}
               .css-e370rw {visibility : hidden;}
               .effi0qh0 {display:none;}
               .button-row {background-color:red;}


               .card {
                 flex-direction: row;
                 align-items: center;
               }
               .card-title {
                 font-weight: bold;
               }
               .card img {
                 width: 30%;
                 border-top-right-radius: 0;
                 border-bottom-left-radius: calc(0.25rem - 1px);
                 max-height : 500px;
               }

               .card-body{
                    display: flex;
                    flex-direction: column;
                    align-self: flex-start;
               }

               .title-text{
                    font-size : 2vw;
               }

               @media only screen and (max-width: 760px) {
                 a {
                   display: none;
                 }
                 .card-body {
                   padding: 0.5em 1.2em;
                 }

                 .card{
                    display : flex;
                    flex-direction : column;
                 }

                 .card-body .card-text {
                   margin: 0;
                 }

                 .card-body h4, .title-text {
                    font-size : 3.5vw;
                 }

                 .card img {
                   width: 50%;
                   max-height : 500px;
                 }
               }
               @media only screen and (max-width: 1200px) {
                 .card img {
                   width: 40%;
                   max-height : 500px;
                 }
               }


               </style>
               """
st.markdown(hide_st_style, unsafe_allow_html=True)
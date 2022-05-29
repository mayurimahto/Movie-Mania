# Movie-Mania
Content Based Movie Recommendation System using cosine similarity.

#### Submission for Microsoft Engage 2022

### About
This repository demonstrates content based movie recommendation system through similarities in genres, cast, directors etc.

Steps involved in making:
1. Manipulate the dataset using pandas in jupyter notebook and eliminating undesirable informations.
2. Using cosine similarity fetch the similar movies.
3. Develope it in pycharm using streamlit.
4. Through API key fetch the data related to movie.
5. Deploy it to heroku.

### Prerequisites

This is an example of how to list things you need to use the software and how to install them.

-   pip
    ```sh
    python -m pip install –upgrade pip
    ```
    
### Installation

_Below is an example of how you can instruct your audience on installing and setting up your app. This template doesn't rely on any external dependencies or services._

1. Get a free API Key at [developers.themoviedb.org/3/getting-started/authentication](https://developers.themoviedb.org/3/getting-started/authentication)
2. Clone the repo
    ```sh
    git clone https://github.com/mayurimahto/Movie-Mania
    ```
3. Install pip packages (It is recommended to this in a `venv`)
    ```sh
    pip install requirements.txt
    ```
4. Launch the Project by writing
    ```sh
    streamlit run app.py

### Built With

This project is made with :

-   [Bootstrap 5](https://getbootstrap.com)
-   [Streamlit](https://streamlit.io/)
-   [Pandas](https://pandas.pydata.org/)
-   [Numpy](https://numpy.org/)
-   [Pickle](https://docs.python.org/3/library/pickle.html)
-   [nltk](https://www.nltk.org/)

### Future Scope
- Adding IMDb links of each recommended movie.
- Displaying cast, genres.
- Adding short bios of the casts.

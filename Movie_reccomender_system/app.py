import pickle
import streamlit as st
import requests

# ------------------ Functions ------------------ #
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url).json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path 
    return full_path

def recommend(movie, num_recommendations=5):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:num_recommendations+1]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)
    return recommended_movie_names, recommended_movie_posters

# ------------------ Load Data ------------------ #
movies = pickle.load(open('movie_list.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))
movie_list = movies['title'].values

# ------------------ Page Config ------------------ #
st.set_page_config(page_title="Movie Recommender", layout="wide")

# ------------------ Light Purple Background ------------------ #
st.markdown(
    """
    <style>
    .stApp {
        background-color: #E6E6FA;  /* Light purple background */
        color: #000000;
    }
    h1 {
        color: #6A0DAD;  /* Dark purple heading */
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ------------------ Header ------------------ #
st.markdown("<h1>🎬 Movie Recommender</h1>", unsafe_allow_html=True)

# ------------------ Sidebar ------------------ #
st.sidebar.header("🎛 Customize Recommendations")
num_recommendations = st.sidebar.slider("Number of recommendations:", 1, 10, 5)
show_posters = st.sidebar.checkbox("Show Posters", value=True)
show_titles = st.sidebar.checkbox("Show Titles", value=True)

# ------------------ Movie Selection ------------------ #
selected_movie = st.selectbox("Type or select a movie from the dropdown", movie_list)
search_movie = st.text_input("Or type a movie name:")
if search_movie and search_movie in movie_list:
    selected_movie = search_movie

# ------------------ Show Recommendations ------------------ #
if st.button('Show Recommendation'):
    st.subheader(f"🎯 Recommendations for: {selected_movie}")
    with st.spinner('Fetching recommendations...'):
        recommended_movie_names, recommended_movie_posters = recommend(selected_movie, num_recommendations)
    
    # Dynamically create columns
    cols = st.columns(num_recommendations)
    for idx, col in enumerate(cols):
        with col:
            if show_posters:
                st.image(recommended_movie_posters[idx], use_container_width=True)
            if show_titles:
                st.markdown(f"**🎥 {recommended_movie_names[idx]}**")
            # Optional: show description if exists
            if 'description' in movies.columns:
                with st.expander("More info"):
                    st.write(movies.iloc[movies[movies['title']==recommended_movie_names[idx]].index[0]]['description'])

# ------------------ Recently Released Movies ------------------ #
st.markdown("---")
st.subheader("🎬 Recently Released")
recent_movies = movie_list[:12]  # pick first 12 movies as “recently released”
cols = st.columns(len(recent_movies))
for idx, col in enumerate(cols):
    with col:
        st.image(fetch_poster(movies.iloc[idx].movie_id), use_container_width=True)
        st.markdown(f"**{recent_movies[idx]}**")

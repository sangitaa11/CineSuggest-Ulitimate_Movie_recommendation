import streamlit as st
import pickle 
import requests
st.set_page_config(page_title="CineSuggest - Movie Guide", page_icon=":guardsman:", layout="wide")
movies=pickle.load(open("artificats\movie_list.pkl",'rb'))
similarity=pickle.load(open("artificats\similarity.pkl",'rb'))
movies_list=movies['title'].values
st.markdown("""
<style>
.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    color: white;
    background-color: #1E1E1E;
    text-align: center;
    padding: 10px;
    box-sizing: border-box;
}
.css-18rr30r {
    background-color: #1E1E1E;
}
</style>
""", unsafe_allow_html=True)

def fetch_poster(movie_id):
    url="https://api.themoviedb.org/3/movie/{}?api_key=71e22c8ba0aae47f0c3391d2892f6c4d&language=en-US".format(movie_id)
    data=requests.get(url)
    data=data.json()
    poster_path=data['poster_path']
    full_path="https://image.tmdb.org/t/p/w500/"+poster_path
    return full_path


st.title("CineSuggest - Movie Guide")
st.write("Discover movies similar to your favorite films!")

selected_movie=st.selectbox("Select a movie",movies_list)

import streamlit.components.v1 as components
def recommend(movie):
    index=movies[movies['title']== movie].index[0]
    distances=sorted(list(enumerate(similarity[index])),reverse=True,key=lambda x: x[1])
    recommended_movies_name=[]
    recommended_movies_poster=[]
    for i in distances[1:6]:
        movie_id=movies.iloc[i[0]].movie_id
        recommended_movies_poster.append(fetch_poster(movie_id))
        recommended_movies_name.append(movies.iloc[i[0]].title)
    return recommended_movies_name,recommended_movies_poster
   

if st.button("Recommend"):
    st.header("Recommended Movies")
    recommended_movies_name,recommended_movies_poster=recommend(selected_movie)
    col1,col2,col3,col4,col5=st.columns(5)
    with col1:
        st.text(recommended_movies_name[0])
        st.image(recommended_movies_poster[0])
    with col2:
        st.text(recommended_movies_name[1])
        st.image(recommended_movies_poster[1])
    with col3:
        st.text(recommended_movies_name[2])
        st.image(recommended_movies_poster[2])
    with col4:
        st.text(recommended_movies_name[3])
        st.image(recommended_movies_poster[3])
    with col5:
        st.text(recommended_movies_name[4])
        st.image(recommended_movies_poster[4])    
st.markdown("""
<div class="footer">
    Made with ❤️ in india
</div>
""", unsafe_allow_html=True)
import requests 
import yaml
from urllib.request import urlretrieve
import os 

url = "https://api.themoviedb.org/3"
with open("config.yml",'r',encoding="utf-8") as file : 
    config = yaml.safe_load(file)

Bearer = config['credentials']['header']
headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {Bearer}"
}
poster_dir = "poster"
horror_movies = []

for page in range(1,6) : 
    """_summary_
    genres = 27 => horror
    """
    query_url = f"{url}/discover/movie?with_genres=27&sort_by=popularity.des&vote_count.gte=500=fr-FR&page={page}"
    response = requests.get(query_url,headers=headers)
    if response.status_code != 200:
        print(f"Erreur lors de la requête page {page}")
        break

    data = response.json()

    for movie in data['results']:
        movie_id = movie['id']

        img_url = f"{url}/movie/{movie_id}/images?include_image_language=fr,en"
        img_res = requests.get(img_url, headers=headers).json()

        posters = img_res.get("posters",[])

        poster_fr = next((p['file_path'] for p in posters if p['iso_639_1'] == 'fr'),None)
        poster_en = next((p['file_path'] for p in posters if p['iso_639_1'] == 'en'),None)

        horror_movies.append({
            "titre": movie['title'],
            "rating": movie['vote_average'],
            "synopsis": movie["overview"],
            "affiche_fr": f"https://image.tmdb.org/t/p/w500{poster_fr}" if poster_fr else "Non disponible",
            "affiche_en": f"https://image.tmdb.org/t/p/w500{poster_en}" if poster_en else "Non disponible"
        })

if horror_movies:
    print(f"\nRécupération terminée ! {len(horror_movies)} films enregistrés.")
    print(f"Exemple : {horror_movies[0]['titre']}")
    print(f"Affiche FR : {horror_movies[0]['affiche_fr']}")
    print(f"Affiche EN : {horror_movies[0]['affiche_en']}")

for movie in range (len(horror_movies)):
        if horror_movies[movie]['affiche_fr'] != "Non disponible":
            fr_save = os.path.join(poster_dir,f"{horror_movies[movie]['titre']}_fr.jpg")
            urlretrieve(horror_movies[movie]['affiche_fr'],fr_save)

        if horror_movies[movie]['affiche_en'] != "Non disponible":
            en_save = os.path.join(poster_dir,f"{horror_movies[movie]['titre']}_en.jpg")    
            urlretrieve(horror_movies[movie]['affiche_en'],en_save)
        
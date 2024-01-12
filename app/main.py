from fastapi import FastAPI, Request, Form, HTTPException, Query

from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

# from sqlalchemy import create_engine, text
# from sqlalchemy.orm import sessionmaker

from elasticsearch import Elasticsearch
import requests

app = FastAPI()
es = Elasticsearch('http://elastic:9200') # Connect to Elasticsearch container
templates = Jinja2Templates(directory="templates")

# Utilisez la fonction app.mount() pour servir les fichiers statiques depuis le répertoire "styles"
app.mount("/styles", StaticFiles(directory="styles"), name="styles")

# Endpoint to test Elasticsearch container
@app.get('/test_elasticsearch')
async def test_elasticsearch(request: Request):
    try:
        # Check if the index "omdb" exists
        index_exists = es.indices.exists(index="omdb")

        return templates.TemplateResponse("test_elasticsearch.html", {"request": request, "index_exists": index_exists})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/')
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# @app.get('/add_movie')
# async def add_movie(request: Request):
#     return templates.TemplateResponse("add_movie.html", {"request": request})

# @app.post('/add_movie_db')
# async def add_movie_db(
#     customerid: str = Form(...),
#     companyname: str = Form(...),
#     contactname: str = Form(...)
# ):
#     try:
#         # Index the customer information in Elasticsearch
#         es.index(index="customers", doc_type="_doc", body={
#             "customerid": customerid,
#             "companyname": companyname,
#             "contactname": contactname
#         })
#         message = "Customer added successfully."
#     except Exception as e:
#         message = f"Error adding customer. Please check your customer information"

#     response_data = {"message": message}
#     return JSONResponse(content=response_data)


@app.get('/get_movie')
async def get_movie(request: Request):
    return templates.TemplateResponse("get_movie.html", {"request": request})

# Update the FastAPI endpoint to search for a movie by title
@app.get('/search_movies')
async def search_movies(request: Request, title: str = Query(..., description="Title of the movie")):
    try:
        # Use a match query to search for the movie by title
        es_query = {
            "query": {
                "match": {
                    "Title": title  # Assuming your movie documents have a "Title" field
                }
            }
        }
        es_response = es.search(index="omdb", body=es_query)

        print("Elasticsearch Response:", es_response)

        # Get all matching movies from the response
        matching_movies = [hit["_source"] for hit in es_response.get("hits", {}).get("hits", [])]

        print("Matching Movie:", matching_movies)

        if matching_movies:
            # If movies are found, return them as JSON
            return JSONResponse(content={"movies": matching_movies})
        else:
            # If no movies match the search, return an empty list
            return JSONResponse(content={"movies": []})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# New endpoint to retrieve all data from Elasticsearch
@app.get('/get_all_movies')
async def get_all_movies(request: Request):
    try:
        # Assuming es is your Elasticsearch instance
        es_response = es.search(index="omdb", body={"query": {"match_all": {}}}, size=20)
        movies = [hit["_source"] for hit in es_response["hits"]["hits"]]
        return templates.TemplateResponse("get_all_movies.html", {"request": request, "movies": movies})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


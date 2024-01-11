from fastapi import FastAPI, Request, Form, HTTPException

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
        # Documents to insert in the Elasticsearch index "cities"
        doc1 = {"city":"New Delhi", "country":"India"}
        doc2 = {"city":"London", "country":"England"}
        doc3 = {"city":"Los Angeles", "country":"USA"}

        #Inserting doc1 in id=1
        es.index(index="cities", id=1, body=doc1)

        #Inserting doc2 in id=2
        es.index(index="cities", id=2, body=doc2)

        #Inserting doc3 in id=3
        es.index(index="cities", id=3, body=doc3)

        # Retrieving data for id=1
        es_response_1 = es.get(index="cities", id=1)
        es_data_1 = es_response_1.get("_source", {})

        # Retrieving data for id=2
        es_response_2 = es.get(index="cities", id=2)
        es_data_2 = es_response_2.get("_source", {})

        # Retrieving data for id=3
        es_response_3 = es.get(index="cities", id=3)
        es_data_3 = es_response_3.get("_source", {})

        return templates.TemplateResponse("test_elasticsearch.html", {"request": request, "es_data_1": es_data_1, "es_data_2": es_data_2, "es_data_3": es_data_3})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/')
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get('/add_customer')
async def add_customer(request: Request):
    return templates.TemplateResponse("add_customer.html", {"request": request})

@app.post('/add_customer_db')
async def add_customer_db(
    customerid: str = Form(...),
    companyname: str = Form(...),
    contactname: str = Form(...)
):
    try:
        # Index the customer information in Elasticsearch
        es.index(index="customers", doc_type="_doc", body={
            "customerid": customerid,
            "companyname": companyname,
            "contactname": contactname
        })
        message = "Customer added successfully."
    except Exception as e:
        message = f"Error adding customer. Please check your customer information"

    response_data = {"message": message}
    return JSONResponse(content=response_data)


@app.get('/get_customer')
async def get_customer(request: Request):
    return templates.TemplateResponse("get_customer.html", {"request": request})

@app.get('/search_customer')
async def search_customer(request: Request, contact_name: str):
    try:
        # Search for customer in Elasticsearch
        result = es.search(index="customers", body={
            "query": {
                "match": {
                    "contactname": contact_name
                }
            }
        })
        customer = result['hits']['hits'][0]['_source']

        return JSONResponse(content=customer)
    except Exception as e:
        message = {"message": f"Customer {contact_name} not found"}
        return JSONResponse(content=message)

@app.get('/get_all_customer')
async def get_all_customer(request: Request):
    session = Session()
    result = session.execute(text('SELECT customer_id, company_name, contact_name FROM customers LIMIT 20'))
    customers = [dict(customerid=row[0], companyname=row[1], contactname=row[2]) for row in result]
    return templates.TemplateResponse("get_all_customer.html", {"request": request, "customers": customers})

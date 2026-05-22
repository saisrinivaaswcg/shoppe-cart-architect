import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.intent_parser import parse_intent
from backend.product_retriever import retrieve_products
from backend.cart_assembler import assemble_cart

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

class SituationRequest(BaseModel):
    situation: str

@app.post("/generate-cart")
def generate_cart(request: SituationRequest):
    intent = parse_intent(request.situation)
    products = retrieve_products(intent)
    cart = assemble_cart(intent, products)
    return cart

@app.get("/")
def root():
    return {"message": "Shopee Cart Architect API is running"}
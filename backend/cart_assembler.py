import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def assemble_cart(intent: dict, products: list) -> dict:
    
    product_list = json.dumps(products, indent=2)
    
    system_prompt = """
    You are a shopping cart planner for Shopee.
    Given a user's intent and a list of available products, build a coordinated cart.
    
    Rules:
    - Total cost must not exceed budget_total
    - Multiply unit price by group_size to get subtotal per item
    - Pick items that work well together for the occasion
    - Prefer higher rated items
    - Prefer faster shipping items
    - Aim to cover different categories (clothing, accessories, drinkware etc)
    
    Return ONLY valid JSON, nothing else:
    {
        "cart_name": "",
        "total_cost": 0,
        "cost_per_person": 0,
        "items": [
            {
                "product_id": "",
                "name": "",
                "quantity": 0,
                "unit_price": 0,
                "subtotal": 0,
                "reason": ""
            }
        ]
    }
    """
    
    user_message = f"""
    Intent: {json.dumps(intent, indent=2)}
    Available Products: {product_list}
    """
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
    )
    
    result = response.choices[0].message.content
    clean = result.replace("```json", "").replace("```", "").strip()
    return json.loads(clean)


if __name__ == "__main__":
    test_intent = {
        "occasion": "team bonding day",
        "group_size": 12,
        "budget_per_person": 30,
        "budget_total": 360,
        "aesthetic_constraints": ["red"],
        "excluded_themes": ["CNY"],
        "required_categories": [],
        "max_shipping_days": 7
    }
    
    test_products = [
        {"id": "001", "name": "Red Dry-Fit Sports T-Shirt (Pack of 12)", "category": "clothing", "price": 10.00, "rating": 4.8, "shipping_days": 2, "stock": 50, "tags": ["red", "sporty"]},
        {"id": "002", "name": "Matching Red Trucker Caps (Pack of 12)", "category": "accessories", "price": 5.00, "rating": 4.6, "shipping_days": 2, "stock": 30, "tags": ["red", "sporty"]},
        {"id": "003", "name": "Insulated Red Sports Water Bottles (12 Units)", "category": "drinkware", "price": 12.00, "rating": 4.7, "shipping_days": 3, "stock": 40, "tags": ["red", "sporty"]},
        {"id": "004", "name": "Red Foam Spirit Fingers (Pack of 12)", "category": "party", "price": 3.00, "rating": 4.5, "shipping_days": 1, "stock": 100, "tags": ["red", "party"]}
    ]
    
    cart = assemble_cart(test_intent, test_products)
    print(json.dumps(cart, indent=2))
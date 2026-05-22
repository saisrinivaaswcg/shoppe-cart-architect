import json
import os

def retrieve_products(intent: dict) -> list:
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(os.path.join(base_dir, "data/products.json")) as f:
        products = json.load(f)
    
    budget = intent["budget_per_person"]
    excluded = intent["excluded_themes"]
    max_shipping = intent["max_shipping_days"]
    aesthetic = intent["aesthetic_constraints"]
    
    filtered = [
        p for p in products
        if p["price"] <= budget
        and p["shipping_days"] <= max_shipping
        and not any(tag in excluded for tag in p["tags"])
        and p["stock"] >= intent["group_size"]
        and (not aesthetic or any(tag in aesthetic for tag in p["tags"]))
    ]

    return filtered


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
    
    results = retrieve_products(test_intent)
    print(f"Found {len(results)} products:")
    for p in results:
        print(f"- {p['name']} ${p['price']}")
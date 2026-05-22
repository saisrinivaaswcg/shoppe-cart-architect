import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def parse_intent(situation: str) -> dict:
    
    system_prompt = """
    You are an intent parser for a shopping assistant.
    Extract the following from the user's situation and return ONLY valid JSON, nothing else:
    {
        "occasion": "",
        "group_size": 0,
        "budget_per_person": 0,
        "budget_total": 0,
        "aesthetic_constraints": [],
        "excluded_themes": [],
        "required_categories": [],
        "max_shipping_days": 0
    }
    
    Rules:
    - If group size is mentioned, calculate budget_total = budget_per_person x group_size
    - If no shipping deadline mentioned, set max_shipping_days to 7
    - If no budget mentioned, set budget_per_person to 50
    - aesthetic_constraints should only contain visual/colour descriptors like "red", "blue", "minimalist", "sporty" — never phrases like "matching items"
    - excluded_themes should only contain theme names like "CNY", "halloween" — never words like "stuff"    
    - Return ONLY the JSON object, no explanation, no markdown
    """
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": situation}
        ]
    )
    
    result = response.choices[0].message.content
    return json.loads(result)


# Test it
if __name__ == "__main__":
    test = "Organising a team bonding day for 12 people, red team, budget $30/person, need matching items that aren't CNY stuff"
    result = parse_intent(test)
    print(json.dumps(result, indent=2))

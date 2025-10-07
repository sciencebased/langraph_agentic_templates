from langchain_core.tools import tool

@tool("get_products", description="Get the current products for a given store")
def get_products(store: str):
    print("Store", store)
    return [
        {"name": "Laptop", "price": 999.99, "stock": 10},
        {"name": "Smartphone", "price": 499.99, "stock": 25},
        {"name": "Tablet", "price": 299.99, "stock": 15},
        {"name": "Headphones", "price": 199.99, "stock": 50},
        {"name": "Smartwatch", "price": 199.99, "stock": 30},
        ]

@tool("get_weather", description="Get the current weather for a given city")
def get_weather(city: str):
    print("City", city)
    return [{"city": "New York", "temperature": 75, "condition": "Sunny"},]

tools = [get_products, get_weather] # For each tool

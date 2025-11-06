import os
from dotenv import load_dotenv
from google.adk.agents import Agent

# Load environment variables from .env file
load_dotenv('../.env')

from toolbox_core import ToolboxSyncClient

# Connect to the MCP Toolbox server (use port 7000 or whatever port you used)
toolbox = ToolboxSyncClient("http://127.0.0.1:7000")

# Load the tools from the toolset we defined in tools.yaml
tools = toolbox.load_toolset('products-toolset')

root_agent = Agent(
    model='gemini-2.5-pro',  # Use a powerful model for better SQL generation
    name='data_analyst_agent',
    description='Agent to answer questions about products in the database',
    instruction="""
    You are a data analyst. 
    Your goal is to help users understand data from a product database. 
    
    The database contains products records with the following rows: 
        - category: The category for the product such us: 'Electronics' and 'Home Goods'
        - name: The name of the product
        - price: The price of the product
        - stock: The number of units of the product in stock
    
    You have access to several predefined tools to query the database:
        - search-products-by-category: Search products by category (needs 'category' parameter)
        - get-products-sorted-by-price: Get products sorted by price (high to low)
        - get-low-stock-products: Get products with stock less than 200 units
        - get-average-price-by-category: Get average price for a category (needs 'category' parameter)


    Use the appropriate tool based on the user's question.
    If you don't know the answer, just say that you don't know.
    """,
    tools=tools,
)



import json
from cart import dao
import products
from products import Product


class Cart:
    def __init__(self, id: int, username: str, contents: list[Product], cost: float):
        self.id = id
        self.username = username
        self.contents = contents
        self.cost = cost

    @staticmethod
    def load(data):
        return Cart(data['id'], data['username'], data['contents'], data['cost'])


def get_cart(username: str) -> list:
    cart_details = dao.get_cart(username)
    if cart_details is None:
        return []
    
    # Assuming 'contents' is a JSON string or list-like object stored in the database
    items = []
    for cart_detail in cart_details:
        # Directly parse the contents if it's a string representing a list or dictionary
        contents = json.loads(cart_detail['contents']) if isinstance(cart_detail['contents'], str) else cart_detail['contents']
        items.extend(contents)
    
    # Batch retrieve all products in one go to reduce multiple DB calls
    product_ids = [item['id'] for item in items]  # Assuming item has 'id' key
    products_list = products.get_products_by_ids(product_ids)
    
    # Map the evaluated contents to product objects
    return [product for product in products_list if product.id in product_ids]


def add_to_cart(username: str, product_id: int):
    dao.add_to_cart(username, product_id)


def remove_from_cart(username: str, product_id: int):
    dao.remove_from_cart(username, product_id)


def delete_cart(username: str):
    dao.delete_cart(username)

from langchain_core.tools import tool
import os

products = [
    {
        "id": 1,
        "name": "ASUS Vivobook",
        "price": 15000000,
        "stock": 5
    },
    {
        "id": 2,
        "name": "Acer Aspire",
        "price": 18000000,
        "stock": 3
    },
    {
        "id": 3,
        "name": "MacBook Air",
        "price": 25000000,
        "stock": 2
    }
]

@tool
def search_products(max_price: int) -> list[dict]:
    """
    Tìm các sản phẩm có giá không vượt quá max_price.

    Args:
        max_price: Giá tối đa tính bằng VND.
    """
    result = []

    for product in products:
        if product["price"] <= max_price:
            result.append(product)

    return result


@tool
def check_stock(product_id: int) -> dict:
    """
    Kiểm tra số lượng tồn kho của sản phẩm theo ID.

    Args:
        product_id: ID của sản phẩm cần kiểm tra.
    """
    for product in products:
        if product["id"] == product_id:
            return {
                "name": product["name"],
                "stock": product["stock"]
            }

    return {"error": "Product not found"}


@tool
def calculate_total(product_id: int, quantity: int) -> dict:
    """
    Tính tổng tiền mua sản phẩm theo ID và số lượng.

    Args:
        product_id: ID của sản phẩm.
        quantity: Số lượng muốn mua.
    """

    if quantity < 1:
        return {"error": "Invalid quantity"}

    stock_info = check_stock.invoke({
        "product_id": product_id
    })

    if "error" in stock_info:
        return stock_info

    if quantity > stock_info["stock"]:
        return {"error": "Not enough stock"}

    for product in products:
        if product["id"] == product_id:
            return {
                "name": product["name"],
                "quantity": quantity,
                "total": quantity * product["price"]
            }

    return {"error": "Product not found"}

tools = [
    search_products,
    check_stock,
    calculate_total
]
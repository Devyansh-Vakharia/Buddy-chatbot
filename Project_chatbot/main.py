from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse
import json
from itertools import count
import generic_helper
import time
import random

app = FastAPI()

inprogress_orders = {}
order_list = []


@app.post("/")
async def handle_request(request: Request):
    payload = await request.json()

    intent = payload['queryResult']['intent']['displayName']
    parameters = payload['queryResult']['parameters']
    output_contexts = payload['queryResult']['outputContexts']
    session_id = generic_helper.extract_session_id(output_contexts[0]['name'])

    intent_handler = {
        'order.add - context: ongoing-order': add_to_order,
        'track.order - context: ongoing-order': track_order,
        'order.remove - context: ongoing-order': remove_to_order,
        'order.complete - context: ongoing-order': complete_to_order
    }

    return JSONResponse(
        content={
            "fulfillmentText": intent_handler[intent](parameters, session_id)
        })


def add_to_order(parameters: dict, session_id: str) -> str:

    food_items = parameters.get('food-item')
    quantities = parameters.get('number')

    if len(food_items) != len(quantities):
        fulfillment_text = "Sorry I didn't understand. Please specify food items and quantity"
    else:
        new_food_dict = dict(zip(food_items, quantities))
        if session_id in inprogress_orders:
            current_food_dict = inprogress_orders[session_id]
            current_food_dict.update(new_food_dict)
            inprogress_orders[session_id] = current_food_dict
        else:
            inprogress_orders[session_id] = new_food_dict
        print(inprogress_orders)
        order_str = generic_helper.get_str_from_food_dict(
            inprogress_orders[session_id])
        fulfillment_text = f"So far you have: {order_str}. Do you need anything else? "
    return fulfillment_text



def track_order(parameters: dict, session_id: str) -> str:
    order_id = generate_unique_order_id
    with open('order.json', 'r') as json_file:
        order_data = json.load(json_file)
        if order_id in order_data:
            fulfillment_text = "Your order will be delivered soon."
        else:
            fulfillment_text = "Invalid order ID! Please check your order ID and try again."
    return fulfillment_text






def complete_to_order(parameters: dict, session_id: str):
    if session_id not in inprogress_orders:
        fulfillment_text = "Sorry, can't find your order. Can you place a new order?"
    else:
        order = inprogress_orders[session_id]
        order_id = generate_unique_order_id()

        order_data = {
            "id":
            order_id,
            "items": [{
                "name": item,
                "quantity": quantity
            } for item, quantity in order.items()]
        }


        order_list[:] = [
            order_entry for order_entry in order_list
            if order_entry['id'] != session_id
        ]


        order_list.append(order_data)

        with open('order.json', 'w') as json_file:
            json.dump(order_list, json_file, indent=2)

        del inprogress_orders[session_id]
        fulfillment_text = f"Order completed. Your ID is #{order_id}. Thank you for your order!"
    return fulfillment_text

def generate_unique_order_id():
    current_timestamp = int(time.time() * 10)
    random_component = random.randint(1, 100)
    order_id = f"{current_timestamp}-{random_component}"
    return order_id

def remove_to_order(parameters: dict, session_id: str):
    if session_id not in inprogress_orders:
        return "Sorry, can't find your order. Can you place a new order?"
    current_order = inprogress_orders[session_id]
    food_items = parameters["food-item"]
    removed_items = []
    no_such_items = []

    for item in food_items:
        if item not in current_order:
            no_such_items.append(item)
        else:
            removed_items.append(item)
            del current_order[item]

    if len(removed_items) > 0:
        fulfillment_text = f"Removed {','.join(removed_items)} from your order!"
    else:
        fulfillment_text = ""

    if len(no_such_items) > 0:
        fulfillment_text += f"Your current order does not have {','.join(no_such_items)}"

    if len(current_order.keys()) == 0:
        fulfillment_text += "Your order is empty!"
    else:
        order_str = generic_helper.get_str_from_food_dict(current_order)
        fulfillment_text += f"Here is what's left in your order: {order_str}. Anything else?"

    return fulfillment_text

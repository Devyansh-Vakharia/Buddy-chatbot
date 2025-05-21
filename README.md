# 🍽️ Food Ordering Chatbot (FastAPI + Dialogflow CX)

An intelligent food ordering chatbot built with Python, FastAPI, and Dialogflow CX that enables users to add, remove, track, and complete food orders through natural language conversations.

## 🚀 Features

- **🔄 Contextual Order Management**: Handles ongoing sessions for each user using Dialogflow CX
- **🛒 Add/Remove Items**: Supports adding or removing food items with quantities in a single message
- **📦 Track & Complete Orders**: Generates a unique order ID and stores completed orders in a JSON file
- **💬 Natural Language Understanding**: Uses Dialogflow CX intents and parameters to drive dynamic responses

## 🛠️ Tech Stack

- **Python**
- **FastAPI** – Backend web framework
- **Dialogflow CX** – Natural language processing & conversation design
- **JSON** – Data storage for completed orders
- **Random & Time** – For generating unique order IDs

## 📁 Project Structure

```
.
├── main.py               # Main FastAPI server with intent handling
├── generic_helper.py     # Utility functions for session ID and food dict formatting
├── order.json            # Stores all completed orders
├── README.md             # Project documentation
```

## ⚙️ Setup Instructions

### Clone the repository

```bash
git clone https://github.com/yourusername/food-ordering-chatbot.git
cd food-ordering-chatbot
```

### Install dependencies

```bash
pip install fastapi uvicorn
```

### Run the server

```bash
uvicorn main:app --reload
```

### Integrate with Dialogflow CX

1. Create intents in Dialogflow CX:
   - `order.add` - context: ongoing-order
   - `order.remove` - context: ongoing-order
   - `track.order` - context: ongoing-order
   - `order.complete` - context: ongoing-order
2. Set webhook URL to your FastAPI server endpoint (`http://<your-domain>:/`)

## 📌 Example Flow

**User**: "Add 2 pizzas and 1 burger to my order"  
**Bot**: "So far you have: 2 pizzas, 1 burger. Do you need anything else?"

**User**: "Remove burger"  
**Bot**: "Removed burger from your order! Here is what's left: 2 pizzas. Anything else?"

**User**: "Complete my order"  
**Bot**: "Order completed. Your ID is #17099810389-43. Thank you for your order!"

## 📄 License

This project is licensed under the MIT License.

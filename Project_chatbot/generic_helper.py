import re

def extract_session_id(session_str: str):
    match = re.search(r"/sessions/(.*?)/contexts/",session_str)
    if match:
        extracted_string = match.group(1)
        return extracted_string
    return ""

def get_str_from_food_dict(food_dict: dict):
    return ", ".join([f"{int(value)} {key}" for key,value in food_dict.items()])

if __name__ == "__main__":
    
    print(extract_session_id("projects/buddy-tjky/agent/sessions/827359be-ab38-fdf0-666e-f74803a713b7/contexts/ongoing-order"))
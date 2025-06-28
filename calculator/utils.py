import base64
import json
import requests
from django.conf import settings

def encode_image(image_path):
    """Convert an image file to base64 encoding for API transmission"""
    try:
        with open(image_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
        return encoded_image
    except Exception as e:
        return None

def analyze_with_gemma(user_responses):
    """Send user activity data to Gemma 3 LLM for carbon footprint calculation"""
    prompt = f"""
    You are an expert in carbon footprint calculation. Based on the following user activities, calculate their daily carbon footprint in kg CO2e.
    Provide detailed breakdown by category and explain the calculation methodology.
    
    User's daily activities:
    {json.dumps(user_responses, indent=2)}
    
    Calculate the carbon footprint with these guidelines:
    1. Use region-specific emission factors where possible (assume global average if no region specified)
    2. Break down the calculation by categories (transportation, food, energy, etc.)
    3. Provide the total carbon footprint in kg CO2e
    4. Include specific recommendations for reducing their carbon footprint
    5. Compare their footprint to global average (which is about 4.5 tons CO2e per year or 12.3 kg CO2e per day)
    6. In the end provide some suggestions to the user on how they can reduce their carbon footprint.
    7. Present the generated response beautifully.

    IMPORTANT: Your response MUST include a structured summary section at the beginning with the following format:
    ```json
    {{
      "total": [TOTAL_FOOTPRINT_IN_KG],
      "transportation": [TRANSPORTATION_FOOTPRINT_IN_KG],
      "food": [FOOD_FOOTPRINT_IN_KG],
      "home_energy": [HOME_ENERGY_FOOTPRINT_IN_KG],
      "consumption": [CONSUMPTION_FOOTPRINT_IN_KG]
    }}
    ```
    
    Format the rest of your response in markdown with clear headings and sections.
    """
    
    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {settings.GEMMA_API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://carbon-calculator.app",
                "X-Title": "Carbon Footprint Calculator",
            },
            json={
                "model": "google/gemma-3n-e4b-it:free",
                "messages": [
                    {"role": "user", "content": prompt}
                ],
            },
            timeout=90
        )
        
        if response.status_code == 200:
            try:
                response_json = response.json()
                
                if 'choices' in response_json and len(response_json['choices']) > 0:
                    if 'message' in response_json['choices'][0] and 'content' in response_json['choices'][0]['message']:
                        return response_json['choices'][0]['message']['content']
                    elif 'text' in response_json['choices'][0]:
                        return response_json['choices'][0]['text']
                elif 'response' in response_json:
                    return response_json['response']
                elif 'result' in response_json:
                    return response_json['result']
                elif 'output' in response_json:
                    return response_json['output']
                elif 'text' in response_json:
                    return response_json['text']
                
                return json.dumps(response_json, indent=2)
            except json.JSONDecodeError:
                return response.text
        else:
            return f"Error {response.status_code}: The API request failed. Please try again later."
            
    except Exception as e:
        return f"An error occurred: {str(e)}"

def analyze_food_invoice(image_data):
    """Send a food receipt/invoice image to Gemma 3 for analysis"""
    prompt_instruction = """
    Analyze this food order receipt/invoice and provide:
    
    1. A list of all food items, classified as vegetarian or non-vegetarian
    2. An estimate of the carbon footprint for each item using standard emission factors
    3. The total carbon footprint of the order
    4. Suggestions to reduce the carbon footprint of future orders
    
    Use region-specific carbon emission factors when available.
    """
    
    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {settings.GEMMA_API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://carbon-calculator.app",
                "X-Title": "Food Carbon Footprint Analyzer",
            },
            json={
                "model": "google/gemma-3-4b-it:free",
                "messages": [
                    {"role": "user", "content": [
                        {"type": "text", "text": prompt_instruction},
                        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_data}"}}
                    ]}
                ],
            },
            timeout=90
        )
        
        if response.status_code == 200:
            try:
                response_json = response.json()
                
                if 'choices' in response_json and len(response_json['choices']) > 0:
                    if 'message' in response_json['choices'][0] and 'content' in response_json['choices'][0]['message']:
                        return response_json['choices'][0]['message']['content']
                    elif 'text' in response_json['choices'][0]:
                        return response_json['choices'][0]['text']
                elif 'response' in response_json:
                    return response_json['response']
                elif 'result' in response_json:
                    return response_json['result']
                elif 'output' in response_json:
                    return response_json['output']
                elif 'text' in response_json:
                    return response_json['text']
                
                return json.dumps(response_json, indent=2)
            except json.JSONDecodeError:
                return response.text
        else:
            return f"Error {response.status_code}: The API request failed. Please try again later."
            
    except Exception as e:
        return f"An error occurred: {str(e)}"

def extract_footprint_values(analysis_text):
    """Extract numerical values from the analysis text"""
    try:
        # Default values
        total = 0
        transportation = 0
        food = 0
        home_energy = 0
        consumption = 0
        
        # Look for JSON block in the response
        if "```json" in analysis_text and "}" in analysis_text:
            # Extract the JSON block
            start_index = analysis_text.find("```json") + 7
            end_index = analysis_text.find("```", start_index)
            if end_index == -1:  # If no closing code block, find the closing brace
                end_index = analysis_text.find("}", start_index) + 1
            
            json_str = analysis_text[start_index:end_index].strip()
            try:
                data = json.loads(json_str)
                
                # Handle array values with units (e.g., ["28.7 kg"])
                if 'total' in data:
                    if isinstance(data['total'], list) and len(data['total']) > 0:
                        # Extract number from string with units
                        value_str = data['total'][0]
                        total = float(''.join(c for c in value_str if c.isdigit() or c == '.'))
                    else:
                        total = float(data['total'])
                        
                if 'transportation' in data:
                    if isinstance(data['transportation'], list) and len(data['transportation']) > 0:
                        value_str = data['transportation'][0]
                        transportation = float(''.join(c for c in value_str if c.isdigit() or c == '.'))
                    else:
                        transportation = float(data['transportation'])
                        
                if 'food' in data:
                    if isinstance(data['food'], list) and len(data['food']) > 0:
                        value_str = data['food'][0]
                        food = float(''.join(c for c in value_str if c.isdigit() or c == '.'))
                    else:
                        food = float(data['food'])
                        
                if 'home_energy' in data:
                    if isinstance(data['home_energy'], list) and len(data['home_energy']) > 0:
                        value_str = data['home_energy'][0]
                        home_energy = float(''.join(c for c in value_str if c.isdigit() or c == '.'))
                    else:
                        home_energy = float(data['home_energy'])
                        
                if 'consumption' in data:
                    if isinstance(data['consumption'], list) and len(data['consumption']) > 0:
                        value_str = data['consumption'][0]
                        consumption = float(''.join(c for c in value_str if c.isdigit() or c == '.'))
                    else:
                        consumption = float(data['consumption'])
                        
            except (json.JSONDecodeError, ValueError) as e:
                print(f"Error parsing JSON: {e}")
                pass
        
        # If no JSON block found or parsing failed, try to find JSON at the beginning of the text
        if total == 0 and analysis_text.strip().startswith('{'):
            try:
                # Find the closing brace of the JSON object
                end_index = analysis_text.find('}')
                if end_index != -1:
                    json_str = analysis_text[:end_index+1].strip()
                    data = json.loads(json_str)
                    
                    # Process the same way as above
                    if 'total' in data:
                        if isinstance(data['total'], list) and len(data['total']) > 0:
                            value_str = data['total'][0]
                            total = float(''.join(c for c in value_str if c.isdigit() or c == '.'))
                        else:
                            total = float(data['total'])
                            
                    # Process other fields similarly...
                    # (Same code as above for other fields)
            except (json.JSONDecodeError, ValueError):
                pass
        
        # Fallback to text parsing if JSON parsing fails
        if total == 0:
            # Look for the total value
            if "total carbon footprint" in analysis_text.lower():
                lines = analysis_text.split('\n')
                for line in lines:
                    if "total carbon footprint" in line.lower() and "kg co2e" in line.lower():
                        # Extract the number before kg CO2e
                        parts = line.split('kg CO2e')
                        if parts and parts[0]:
                            number_text = ''.join(c for c in parts[0] if c.isdigit() or c == '.')
                            try:
                                total = float(number_text)
                            except ValueError:
                                pass
        
        return {
            'total': total,
            'transportation': transportation,
            'food': food,
            'home_energy': home_energy,
            'consumption': consumption
        }
    except Exception as e:
        print(f"Exception in extract_footprint_values: {e}")
        return {
            'total': 0,
            'transportation': 0,
            'food': 0,
            'home_energy': 0,
            'consumption': 0
        }
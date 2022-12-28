import requests

def translate(text, target_language, email):
    # MyMemory Translation API endpoint
    endpoint = "http://api.mymemory.translated.net/get"

    # Make a request to the API
    params = {
        "q": text,
        "langpair": f"en|{target_language}",
        "de": email,
    }
    response = requests.get(endpoint, params=params)

    # Parse the response
    data = response.json()
    translated_text = data["responseData"]["translatedText"]

    return translated_text

def translate_json(json_data, target_language, email, keys_processed=0, total_keys=None):
    if total_keys is None:
        # Calculate total number of keys in the JSON data
        total_keys = 0
        stack = [json_data]
        while stack:
            value = stack.pop()
            if isinstance(value, dict):
                total_keys += len(value)
                stack.extend(value.values())
            elif isinstance(value, list):
                total_keys += len(value)
                stack.extend(value)

    if isinstance(json_data, dict):
        for key, value in json_data.items():
            if isinstance(value, str) and len(value) > 1:
                # Check if the string contains only a single letter or symbol or only numbers
                if not value.strip() or len(value.strip()) == 1 or value.isdigit():
                    print(f"Skipping '{value}' because it contains only a single letter or symbol or only numbers.")
                else:
                    print(f"Translating '{value}'")
                    json_data[key] = translate(value, target_language, email)
            else:
                translate_json(value, target_language, email, keys_processed, total_keys)
            keys_processed += 1
            percentage_complete = keys_processed / total_keys * 100
            print(f"{percentage_complete:.2f}% complete\n")
    elif isinstance(json_data, list):
        for item in json_data:
            translate_json(item, target_language, email, keys_processed, total_keys)
            keys_processed += 1
            percentage_complete = keys_processed / total_keys * 100
            print(f"{percentage_complete:.2f}% complete\n")
    else:
        # Return immediately if the value is not a string, dict, or list
        print(f"Skipping '{json_data}' because it is not a string, dict, or list.")
        return

import base64
import os
import re

html_path = 'golf_club.html'
img_path = 'golf_background.png'

# Check if files exist
if not os.path.exists(html_path):
    print(f"Error: {html_path} not found")
    exit(1)
if not os.path.exists(img_path):
    print(f"Error: {img_path} not found")
    exit(1)

# Read image and convert to base64
try:
    with open(img_path, 'rb') as img_file:
        img_data = img_file.read()
        b64_data = base64.b64encode(img_data).decode('utf-8')
        mime_type = 'image/png' 
        # Construct the new URL string
        new_url = f"url('data:{mime_type};base64,{b64_data}')"
except Exception as e:
    print(f"Error processing image: {e}")
    exit(1)

# Read HTML
try:
    with open(html_path, 'r', encoding='utf-8') as html_file:
        content = html_file.read()

    # Regex to find the background property with linear-gradient and url
    # We match: background: linear-gradient(...), url('...')
    # Using non-greedy matching .*? inside the parentheses
    
    pattern = r"(background:\s*linear-gradient\(rgba\(.*?\),\s*rgba\(.*?\)\),\s*)url\('data:image/.*?Base64.*?'\)"
    # Note: The existing file has 'data:image/png;base64,...' so we match that structure. 
    # To be more robust, we can match url\('.*?'\) but we want to be specific to replace the right one if possible.
    # Actually, let's keep it simple and robust:
    # Match the specific background line structure we saw in the file.
    
    # Improved Pattern:
    # background: linear-gradient(rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.2)), url('...');
    
    # We will capture the gradient part and replace the url part.
    pattern = r"(background:\s*linear-gradient\(.*?\),\s*)url\('.*?'\)"
    
    replacement = f"\\1{new_url}"
    
    new_content, count = re.subn(pattern, replacement, content, flags=re.DOTALL)

    if count == 0:
        print("Warning: Could not find exact background pattern to replace.")
        # Fallback: Try to just find any background with a data URI if the specific gradient missing?
        # Or maybe the user edited it? 
        # Let's try searching for just the url('...') part if previous failed, but let's stick to the gradient one first as it's what we saw.
        print("Checking content for 'background:'...")
        if "background:" in content:
             print("Found 'background:' in content. Attempting simple replace if it's the only one.")
        else:
             print("'background:' keyword not found.")
        exit(1)
    
    # Write back
    with open(html_path, 'w', encoding='utf-8') as html_file:
        html_file.write(new_content)
        
    print(f"Successfully embedded {img_path} into {html_path}")

except Exception as e:
    print(f"Error processing HTML: {e}")
    exit(1)

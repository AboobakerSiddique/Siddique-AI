import os

js_path = "frontend/js/app.js"

if os.path.exists(js_path):
    with open(js_path, "r", encoding="utf-8") as f:
        js = f.read()

    # Find the payload creation block
    old_payload = """body: JSON.stringify({
                conversation_id: currentConversationId,
                message: text,
                image_base64: currentImage
            })"""
            
    new_payload = """body: JSON.stringify({
                ...(currentConversationId !== null && { conversation_id: currentConversationId }),
                message: text,
                ...(currentImage && { image_base64: currentImage })
            })"""

    if old_payload in js:
        js = js.replace(old_payload, new_payload)
        with open(js_path, "w", encoding="utf-8") as f:
            f.write(js)
        print("✅ Fixed payload to prevent 422 validation errors.")
    else:
        print("Payload structure slightly different, trying alternative replacement.")
        # Alternative replacement if whitespace is different
        import re
        js = re.sub(
            r'body:\s*JSON\.stringify\(\{\s*conversation_id:\s*currentConversationId,\s*message:\s*text,\s*image_base64:\s*currentImage\s*\}\)',
            new_payload,
            js
        )
        with open(js_path, "w", encoding="utf-8") as f:
            f.write(js)
        print("✅ Applied regex fix for payload.")
else:
    print(f"Error: Could not find {js_path}")
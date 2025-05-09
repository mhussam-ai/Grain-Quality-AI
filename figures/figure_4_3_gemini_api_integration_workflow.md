sequenceDiagram
    participant SL as Streamlit App (Python Backend)
    participant GenAI as Google Generative AI SDK
    participant Gemini as Gemini API Endpoint

    SL->>GenAI: 1. genai.configure(api_key)
    activate GenAI
    GenAI-->>SL: Configured
    deactivate GenAI

    SL->>SL: 2. User triggers analysis (image_bytes, grain_type)
    SL->>SL: 3. generate_prompt(grain_type) -> prompt_text
    SL->>GenAI: 4. model = genai.GenerativeModel(GEMINI_MODEL)
    activate GenAI
    GenAI-->>SL: Model object
    deactivate GenAI
    
    SL->>GenAI: 5. image_part = {"mime_type": "image/jpeg", "data": image_bytes}
    SL->>GenAI: 6. response = model.generate_content([prompt_text, image_part], request_options={'timeout': 60})
    activate GenAI
    GenAI->>Gemini: HTTPS Request (Prompt + Image Data)
    activate Gemini
    Gemini-->>GenAI: API Response (Text with JSON)
    deactivate Gemini
    GenAI-->>SL: Response object
    deactivate GenAI

    SL->>SL: 7. Check response.candidates
    alt No candidates or safety block
        SL->>SL: 8a. Handle error (e.g., Content Filter Block)
        SL-->>User: Display Error Message
    else Candidates exist
        SL->>SL: 8b. Extract text: response.candidates[0].content.parts[0].text
        SL->>SL: 9. Regex search for JSON block: re.search(r'\{.*\}', text, re.DOTALL)
        alt JSON found
            SL->>SL: 10a. json_str = match.group(0)
            SL->>SL: 11a. result = json.loads(json_str)
            SL->>SL: 12a. Check image_quality_assessment.suitable_for_analysis (Store warning if not suitable)
            SL->>SL: 13a. Check for Grain Mismatch (selected_grain vs result.grain_identity.detected_grain)
            alt Mismatch Detected
                SL->>SL: 14aa. Handle Grain Mismatch Error (Prepare specific error message)
                SL-->>User: Display Mismatch Error Message
            else No Mismatch
                SL->>SL: 14ab. Proceed with displaying analysis results
                SL-->>User: Display Analysis Results (potentially with image quality warnings)
            end
        else No JSON found
            SL->>SL: 10b. Handle error (Invalid Response Format)
            SL-->>User: Display Error Message
        end
    end

    Note right of SL: Error handling for API calls (timeout, network) and JSON parsing is also present.

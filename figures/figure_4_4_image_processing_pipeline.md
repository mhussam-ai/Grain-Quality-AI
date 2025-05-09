graph TD
    A[User Input: Uploaded File or Camera Capture] --> B{Streamlit Input Widget};
    B -- Bytes --> C[st.session_state.image_data (Raw Bytes)];
    
    subgraph AnalysisTrigger["On 'Analyze' Button Click"]
        C --> D{`process_image(image_bytes, ...)` Function Call};
        D --> E[Image Bytes (from session state)];
        E --> F{Gemini API Request Preparation};
        F --> F1[image_part = {"mime_type": "image/jpeg", "data": image_bytes}];
        F1 --> G[Send to Gemini API];
    end

    subgraph HistoryThumbnailCreation["For History Tab: `save_to_history(...)`"]
        C --> H{`save_to_history(..., image_data, ...)`};
        H --> I[image = PIL.Image.open(io.BytesIO(image_data))];
        I --> J[image.thumbnail((100, 100))];
        J --> K[buffered = io.BytesIO()];
        K --> L{Convert to RGB if RGBA};
        L -- image.mode == 'RGBA' --> M[image = image.convert('RGB')];
        M --> N;
        L -- else --> N;
        N[image.save(buffered, format="JPEG", quality=85)];
        N --> O[img_str = base64.b64encode(buffered.getvalue()).decode()];
        O --> P[Store `img_str` in session_state.analysis_history];
    end

    subgraph DisplayInUI["For Display in Analysis Tab"]
        C --> Q[st.image(st.session_state.image_data, ...)];
        Q --> R[Rendered Image in UI];
    end

    style A fill:#FFFACD,stroke:#333,stroke-width:1px
    style AnalysisTrigger fill:#E0FFFF,stroke:#333,stroke-width:1px,border-style:dashed
    style HistoryThumbnailCreation fill:#F0FFF0,stroke:#333,stroke-width:1px,border-style:dashed
    style DisplayInUI fill:#FFF0F5,stroke:#333,stroke-width:1px,border-style:dashed
    style G fill:#FFD700,stroke:#333,stroke-width:1px
    style P fill:#98FB98,stroke:#333,stroke-width:1px
    style R fill:#ADD8E6,stroke:#333,stroke-width:1px

    note right of F1 "Assumes JPEG for API, even if original is PNG etc.<br>Gemini likely handles various input formats internally."
    note right of L "Ensures JPEG compatibility for saving thumbnail."

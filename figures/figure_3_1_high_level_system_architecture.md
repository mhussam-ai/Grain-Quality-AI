graph TD
    subgraph UserDevice["User Device (Browser)"]
        UI[Streamlit UI]
    end

    subgraph ApplicationServer["Application Server (Python/Streamlit)"]
        CoreLogic["Core Application Logic"]
        PromptGen["Prompt Generation (`generate_prompt`)"]
        AI_Interaction["AI Interaction (`process_image`)"]
        ResponseParse["Response Parsing"]
        ResultRender["Result Rendering (`render_analysis_results`)"]
        HistoryMgmt["History Management (`save_to_history`)"]
        SessionState["Streamlit Session State"]
        EnvConfig[".env / Environment Variables"]
    end

    subgraph GoogleCloud["Google Cloud Platform"]
        GeminiAPI["Google Generative AI (Gemini API)"]
    end

    UI -- "Select Grain, Upload/Capture Image" --> CoreLogic
    CoreLogic -- "Selected Grain Type" --> PromptGen
    CoreLogic -- "Image Data, API Key" --> AI_Interaction
    PromptGen -- "Generated Prompt" --> AI_Interaction
    AI_Interaction -- "Image + Prompt" --> GeminiAPI
    GeminiAPI -- "JSON Response" --> AI_Interaction
    AI_Interaction -- "Raw Response" --> ResponseParse
    ResponseParse -- "Parsed Analysis (Dict)" --> CoreLogic
    CoreLogic -- "Analysis Data" --> ResultRender
    CoreLogic -- "Analysis Data, Thumbnail" --> HistoryMgmt
    ResultRender -- "Display Results" --> UI
    HistoryMgmt -- "Store/Retrieve History" --> SessionState
    CoreLogic -- "Access/Update" --> SessionState
    CoreLogic -- "Load API Key" --> EnvConfig

    style UserDevice fill:#f9f,stroke:#333,stroke-width:2px
    style ApplicationServer fill:#ccf,stroke:#333,stroke-width:2px
    style GoogleCloud fill:#cfc,stroke:#333,stroke-width:2px

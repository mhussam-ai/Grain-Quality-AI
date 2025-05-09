graph LR
    A[User: Selects Grain Type & Uploads Image] --> B(Streamlit UI: Receives Input);
    B --> C{GrainSight Backend: Input Validation};
    C -- Valid --> D[Generate Prompt for AI];
    D --> E[Prepare Image Data];
    E --> F{Call Gemini API};
    C -- Invalid --> G[Display Error to User];
    F -- Image + Prompt --> H[Gemini AI Model];
    H -- JSON Response --> I{Parse AI Response};
    I -- Parsing Error --> G;
    I -- Successfully Parsed --> M{Check for Grain Mismatch};
    M -- Mismatch Detected --> N[Display Mismatch Error to User];
    M -- No Mismatch --> J[Store in Session State];
    J --> K[Render Analysis Results];
    K --> L(Streamlit UI: Displays Results & Visualizations);
    F -- API Error --> G;

    subgraph UserInteraction["User Interaction"]
        direction LR
        A
        L
        G
        N
    end

    subgraph ApplicationLogic["GrainSight Application Logic"]
        direction TB
        B
        C
        D
        E
        F
        I
        M # New Mismatch Check
        J
        K
    end

    subgraph ExternalService["External AI Service"]
        direction LR
        H
    end

    style UserInteraction fill:#E6E6FA,stroke:#333,stroke-width:2px
    style ApplicationLogic fill:#ADD8E6,stroke:#333,stroke-width:2px
    style ExternalService fill:#90EE90,stroke:#333,stroke-width:2px

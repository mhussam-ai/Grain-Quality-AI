graph LR
    A[User: Selects Grain Type & Uploads Image] --> B(Streamlit UI: Receives Input);
    B --> C{GrainSight Backend: Input Validation};
    C -- Valid --> D[Generate Prompt for AI];
    D --> E[Prepare Image Data];
    E --> F{Call Gemini API};
    C -- Invalid --> G[Display Error to User];
    F -- Image + Prompt --> H[Gemini AI Model];
    H -- JSON Response --> I{Parse AI Response};
    I -- Parsed Data --> J[Store in Session State];
    J --> K[Render Analysis Results];
    K --> L(Streamlit UI: Displays Results & Visualizations);
    I -- Parsing Error --> G;
    F -- API Error --> G;

    subgraph UserInteraction["User Interaction"]
        A
        L
        G
    end

    subgraph ApplicationLogic["GrainSight Application Logic"]
        B
        C
        D
        E
        F
        I
        J
        K
    end

    subgraph ExternalService["External AI Service"]
        H
    end

    style UserInteraction fill:#E6E6FA,stroke:#333,stroke-width:2px
    style ApplicationLogic fill:#ADD8E6,stroke:#333,stroke-width:2px
    style ExternalService fill:#90EE90,stroke:#333,stroke-width:2px

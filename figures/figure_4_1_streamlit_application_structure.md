graph TD
    A[GrainSight.py] --> B{Streamlit App Initialization};
    B --> C[Page Config (Title, Icon, Layout)];
    B --> D[Load Environment Variables (.env)];
    D --> E[API Key (GOOGLE_API_KEY)];
    B --> F[Custom CSS Injection];
    B --> G[Session State Initialization];
    G --> G1[image_data: None];
    G --> G2[analysis_history: []];
    G --> G3[current_analysis: None];
    G --> G4[selected_grain: None];
    G --> G5[history_limit: HISTORY_LIMIT];
    G --> Gx[...other states];

    B --> H{Main UI Rendering};
    H --> I[App Title & Subheader];
    H --> J[API Key Check (Error if missing)];
    H --> K[Sidebar (Instructions, Tips)];
    
    H --> L{Tabs Creation};
    L -- "🔬 Analysis" --> M[Analysis Tab Logic];
    L -- "📊 History" --> N[History Tab Logic];
    L -- "⚙️ Settings" --> O[Settings Tab Logic];

    subgraph AnalysisTab["Analysis Tab (Tab 1)"]
        M --> M1[Grain Selection Dropdown];
        M1 --> M2[Conditional UI (Uploader/Camera)];
        M2 --> M3[Image Preview];
        M3 --> M4[Analysis Button];
        M4 -- On Click --> M5{Image Processing & AI Call};
        M5 --> M6[Update Session State (current_analysis, history)];
        M6 --> M7[Render Analysis Results];
    end

    subgraph HistoryTab["History Tab (Tab 2)"]
        N --> N1[Display History Items from Session State];
        N1 --> N2[View Details Button (Loads to Main Tab)];
        N --> N3[Clear History Button];
    end

    subgraph SettingsTab["Settings Tab (Tab 3)"]
        O --> O1[History Limit Slider];
        O --> O2[About Section];
        O --> O3[Reset Application State Button];
    end

    H --> P[Footer];

    subgraph HelperFunctions["Helper Functions"]
        HF1[get_color_from_score()]
        HF2[get_color_from_grade()]
        HF3[render_progress_circle()]
        HF4[generate_prompt()]
        HF5[process_image()]
        HF6[save_to_history()]
        HF7[render_analysis_results()]
    end
    
    M5 --> HF4;
    M5 --> HF5;
    M6 --> HF6;
    M7 --> HF1;
    M7 --> HF2;
    M7 --> HF3;
    M7 --> HF7;


    style A fill:#FFF,stroke:#333,stroke-width:2px
    style HelperFunctions fill:#FFFFE0,stroke:#333,stroke-width:1px,border-style:dashed
    style AnalysisTab fill:#E0FFFF,stroke:#333,stroke-width:1px
    style HistoryTab fill:#FFF0F5,stroke:#333,stroke-width:1px
    style SettingsTab fill:#F5F5DC,stroke:#333,stroke-width:1px

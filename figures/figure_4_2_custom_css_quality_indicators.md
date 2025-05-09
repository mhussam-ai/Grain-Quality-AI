graph TD
    A["Python: st.markdown() for CSS injection"] --> B{Embedded CSS Block};

    B --> C[CSS Rules for Quality Indicators];
    C --> C1[".quality-excellent { color: #27ae60; ... } /* Green */"];
    C --> C2[".quality-good { color: #2ecc71; ... } /* L. Green */"];
    C --> C3[".quality-fair { color: #f39c12; ... } /* Orange */"];
    C --> C4[".quality-poor { color: #e74c3c; ... } /* Red */"];
    C --> C5[".quality-na { color: #7f8c8d; ... } /* Grey */"];

    B --> D[Other CSS Rules (e.g., headers, cards, buttons)];

    subgraph PythonHelperFunctions["Python Helper Functions"]
        E["get_color_from_score(score)"] --> F{Determine Class based on Score};
        F -- Score >= 90 --> G1[Returns "excellent"];
        F -- Score >= 75 --> G2[Returns "good"];
        F -- Score >= 60 --> G3[Returns "fair"];
        F -- Else --> G4[Returns "poor"];
        F -- Invalid Score --> G5[Returns "na"];

        H["get_color_from_grade(grade_str)"] --> I{Determine Class based on Grade String};
        I -- "excellent" --> J1[Returns "excellent"];
        I -- "good" --> J2[Returns "good"];
        I -- "fair" --> J3[Returns "fair"];
        I -- "poor" --> J4[Returns "poor"];
        I -- Else/Invalid --> J5[Returns "na"];
    end
    
    subgraph ResultRendering["Result Rendering Logic (Python)"]
        K["Example: render_analysis_results()"] --> L{Construct HTML with Dynamic Class};
        L -- Uses helper function output --> M["HTML: <span class='quality-[dynamic_class]'>...</span>"];
    end

    G1 --> C1;
    G2 --> C2;
    G3 --> C3;
    G4 --> C4;
    G5 --> C5;
    J1 --> C1;
    J2 --> C2;
    J3 --> C3;
    J4 --> C4;
    J5 --> C5;
    
    M --> N[Styled Output in Streamlit UI];

    style A fill:#FFFACD,stroke:#333,stroke-width:1px
    style B fill:#ADD8E6,stroke:#333,stroke-width:1px
    style C fill:#E0FFFF,stroke:#333,stroke-width:1px,border-style:dashed
    style PythonHelperFunctions fill:#FFFFE0,stroke:#333,stroke-width:1px,border-style:dotted
    style ResultRendering fill:#F0FFF0,stroke:#333,stroke-width:1px,border-style:dotted
    style N fill:#98FB98,stroke:#333,stroke-width:2px

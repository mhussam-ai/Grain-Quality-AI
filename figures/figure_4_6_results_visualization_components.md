graph TD
    A[Parsed AI Analysis (Dictionary `analysis`)] --> B{`render_analysis_results(analysis)` Function};

    B --> C{Handle Top-Level Errors};
    C -- Error in `analysis` --> C1[Display `st.error()` with error message];
    C -- No Error --> D{Extract Data Sections};
    D --> D_ID["identity = analysis.get('grain_identity', {})"];
    D --> D_QL["quality = analysis.get('quality_assessment', {})"];
    D --> D_DF["defects = analysis.get('defects', {})"];
    D --> D_GR["grade_info = analysis.get('overall_grade', {})"];
    D --> D_RC["recommendations = analysis.get('usage_recommendations', {})"];
    D --> D_IQ["img_quality_notes = analysis.get('image_quality_assessment', {})"];

    
    B --> Header1["`st.markdown('<h2 class=\"section-header\">Analysis Summary</h2>', ...)`"];
    
    subgraph Row1["Row 1: Overall Grade & Detected Type (Columns)"]
        Col1_1["`render_progress_circle(grade_score, 'Overall: grade_text', grade_color)`"] --> ProgCirc1["Circular Progress Bar (Overall Grade)"];
        Col1_2["Metric Card: Detected Grain Identity, Variety, Characteristics"];
    end
    ProgCirc1 --> Helper_RPC1["Uses `render_progress_circle()` helper"];
    Helper_RPC1 --> Helper_GCS1["Uses `get_color_from_grade()` for color"];


    B --> Header2["`st.markdown('<h3 class=\"section-header\">Quality Metrics</h3>', ...)`"];
    subgraph Row2["Row 2: Key Quality Metrics (4 Columns)"]
        Col2_1["`render_progress_circle(integrity_pct, 'Integrity', integrity_color)`"] --> ProgCirc2["Circular Progress (Integrity)"];
        Col2_2["`render_progress_circle(uniformity_score, 'Uniformity', uniformity_color)`"] --> ProgCirc3["Circular Progress (Uniformity)"];
        Col2_3["`render_progress_circle(maturity_score, 'Maturity', maturity_color)`"] --> ProgCirc4["Circular Progress (Maturity)"];
        Col2_4["`render_progress_circle(defect_quality, 'Defect Level', defect_color)`"] --> ProgCirc5["Circular Progress (Defect Level)"];
    end
    ProgCirc2 --> Helper_RPC2["Uses `render_progress_circle()`"]; Helper_RPC2 --> Helper_GCS2["Uses `get_color_from_score()`"];
    ProgCirc3 --> Helper_RPC3["Uses `render_progress_circle()`"]; Helper_RPC3 --> Helper_GCS3["Uses `get_color_from_score()`"];
    ProgCirc4 --> Helper_RPC4["Uses `render_progress_circle()`"]; Helper_RPC4 --> Helper_GCS4["Uses `get_color_from_score()`"];
    ProgCirc5 --> Helper_RPC5["Uses `render_progress_circle()`"]; Helper_RPC5 --> Helper_GCS5["Uses `get_color_from_score()`"];


    B --> Header3["`st.markdown('<h3 class=\"section-header\">Detailed Analysis</h3>', ...)`"];
    subgraph Expanders["Detailed Sections (st.expander)"]
        Exp1["Detailed Quality Assessment (Integrity, Uniformity, Maturity, Foreign Matter, Soundness descriptions)"];
        Exp2["Defect Analysis (Iterates `defects` dict, displays severity, description)"];
        Exp3["Usage Recommendations (Primary Uses, Cooking/Processing, Storage Tips)"];
        Exp4["Additional Notes from AI (if `analysis.additional_notes` exists)"];
        Exp5["AI Image Quality Assessment (if `img_quality_notes.suitable_for_analysis` is false)"];
    end

    B --> RawJsonExpander["`st.expander('Show Raw AI Response (JSON)')` --> `st.json(analysis)`"];

    subgraph HelperFunctionsUsed["Helper Functions Used Directly by `render_progress_circle` or `render_analysis_results`"]
        HF_GCS["`get_color_from_score()`"]
        HF_GCG["`get_color_from_grade()`"]
        HF_RPC["`render_progress_circle()` - This itself is a visualization component using HTML/CSS"]
    end
    
    Helper_RPC1 --> HF_RPC; Helper_RPC2 --> HF_RPC; Helper_RPC3 --> HF_RPC; Helper_RPC4 --> HF_RPC; Helper_RPC5 --> HF_RPC;
    Helper_GCS1 --> HF_GCG; Helper_GCS2 --> HF_GCS; Helper_GCS3 --> HF_GCS; Helper_GCS4 --> HF_GCS; Helper_GCS5 --> HF_GCS;

    style A fill:#FFFACD,stroke:#333,stroke-width:1px
    style B fill:#ADD8E6,stroke:#333,stroke-width:1px
    style Row1 fill:#E0FFFF,stroke:#ccc,stroke-width:1px,border-style:dashed
    style Row2 fill:#E0FFFF,stroke:#ccc,stroke-width:1px,border-style:dashed
    style Expanders fill:#F0FFF0,stroke:#ccc,stroke-width:1px,border-style:dashed
    style HelperFunctionsUsed fill:#FFFFE0,stroke:#333,stroke-width:1px,border-style:dotted
    style ProgCirc1 fill:#98FB98; style ProgCirc2 fill:#98FB98; style ProgCirc3 fill:#98FB98; style ProgCirc4 fill:#98FB98; style ProgCirc5 fill:#98FB98;

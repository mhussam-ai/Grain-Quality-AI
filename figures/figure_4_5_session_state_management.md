graph TD
    A[Streamlit App Starts / Reruns] --> B{Session State Initialization (if key not exists)};
    B --> S1["`st.session_state.image_data = None` (Bytes of current image)"];
    B --> S2["`st.session_state.image_source = None` ('upload' or 'camera')"];
    B --> S3["`st.session_state.analysis_history = []` (List of history items)"];
    B --> S4["`st.session_state.current_analysis = None` (Dict of last analysis result/error)"];
    B --> S5["`st.session_state.selected_grain = None` (String, e.g., 'Rice')"];
    B --> S6["`st.session_state.last_analysis_grain = None` (String, grain type AI detected/analyzed)"];
    B --> S7["`st.session_state.history_limit = HISTORY_LIMIT` (Int)"];
    B --> S8["`st.session_state.show_uploader = False` (Bool)"];
    B --> S9["`st.session_state.show_camera = False` (Bool)"];

    subgraph UserActionsUpdatingState["User Actions & Callbacks Updating State"]
        direction LR
        UA1[Grain Selection Dropdown] -- Changes value --> S5;
        UA1 -- Also clears --> S1;
        UA1 -- Also clears --> S4;
        UA1 -- Also clears --> S2;
        UA1 -- Also clears --> S6;
        UA1 -- Also resets --> S8;
        UA1 -- Also resets --> S9;

        UA2[Upload/Camera Button Click] -- Sets True --> S8_OR_S9["S8 or S9"];
        UA2 -- Clears other if switching --> S1_S4_IfSwitch["S1, S4 (if switching input)"];
        
        UA3[File Uploader / Camera Input] -- New image data --> S1;
        UA3 -- Sets source --> S2;
        UA3 -- Clears --> S4;

        UA4["'Analyze' Button Click"] -- After `process_image` --> S4;
        UA4 -- After `process_image` --> S6;
        UA4 -- Calls `save_to_history` --> S3;
        
        UA5["'View Details' (History)"] -- Loads item --> S4;
        UA5 -- Loads item --> S5;
        UA5 -- Loads item --> S6;

        UA6["'Clear History' Button"] -- Clears list --> S3;
        UA7["History Limit Slider (Settings)"] -- Changes value --> S7;
        UA7 -- Trims list --> S3;
        UA8["'Reset Application' Button"] -- Deletes all keys --> AllStates["All Session State Keys"];
        AllStates -- Re-initializes --> S7_Default["S7 (default)"];
    end

    subgraph ReadingStateForUIRendering["UI Components Reading from Session State"]
        direction LR
        R1[Image Preview] <-- Reads --- S1;
        R2[Analysis Results Display] <-- Reads --- S4;
        R2[Analysis Results Display] <-- Reads --- S6;
        R2[Analysis Results Display] <-- Reads --- S5;
        R3[History Tab List] <-- Reads --- S3;
        R4[Grain Dropdown Pre-selection] <-- Reads --- S5;
        R5[Conditional Uploader/Camera Display] <-- Reads --- S8;
        R5[Conditional Uploader/Camera Display] <-- Reads --- S9;
        R6[History Limit Info/Slider Value] <-- Reads --- S7;
    end
    
    S1; S2; S3; S4; S5; S6; S7; S8; S9;

    style B fill:#ADD8E6,stroke:#333,stroke-width:1px
    style UserActionsUpdatingState fill:#FFFFE0,stroke:#333,stroke-width:1px,border-style:dashed
    style ReadingStateForUIRendering fill:#F0FFF0,stroke:#333,stroke-width:1px,border-style:dashed
    style S1 fill:#FFFACD; style S2 fill:#FFFACD; style S3 fill:#FFFACD; style S4 fill:#FFFACD; style S5 fill:#FFFACD; style S6 fill:#FFFACD; style S7 fill:#FFFACD; style S8 fill:#FFFACD; style S9 fill:#FFFACD;

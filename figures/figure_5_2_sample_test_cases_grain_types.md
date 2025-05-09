graph TD
    A[Test Objective: Verify correct analysis and differentiation for various grain types and image conditions] --> B{Test Case Categories};

    B --> TC_Rice["Rice Test Cases"];
    B --> TC_Wheat["Wheat Test Cases"];
    B --> TC_Corn["Corn Test Cases"];
    B --> TC_General["General/Cross-Cutting Test Cases"];

    subgraph RiceTestCases["Rice Test Cases"]
        R1["ID: TC_R_001 | Desc: Good quality Basmati rice image | Expected: Correct identification, high scores, relevant defects (e.g., low chalkiness)"];
        R2["ID: TC_R_002 | Desc: Poor quality short-grain rice (broken, discolored) | Expected: Correct identification, low scores, high defect report"];
        R3["ID: TC_R_003 | Desc: Image with mixed rice varieties | Expected: AI identifies 'Multiple Types' or primary type, comments on mix"];
        R4["ID: TC_R_004 | Desc: Rice image with significant foreign matter (stones, husks) | Expected: Foreign matter detected, impacts grade"];
        R5["ID: TC_R_005 | Desc: User selects 'Wheat', uploads Rice image | Expected: 'Grain Type Mismatch' error displayed (e.g., 'You selected Wheat, AI detected Rice...'), no analysis results shown on main tab."];
    end

    subgraph WheatTestCases["Wheat Test Cases"]
        W1["ID: TC_W_001 | Desc: Good quality Hard Red Winter wheat | Expected: Correct ID, high scores, wheat-specific characteristics"];
        W2["ID: TC_W_002 | Desc: Wheat with signs of sprouting/mold | Expected: Sprouting/mold detected, low grade, storage warnings"];
        W3["ID: TC_W_003 | Desc: Durum wheat image | Expected: Correct ID as Durum or general Wheat, appropriate usage (pasta)"];
        W4["ID: TC_W_004 | Desc: User selects 'Corn', uploads Wheat image | Expected: 'Grain Type Mismatch' error displayed (e.g., 'You selected Corn, AI detected Wheat...'), no analysis results shown on main tab."];
    end

    subgraph CornTestCases["Corn Test Cases"]
        C1["ID: TC_C_001 | Desc: Good quality Yellow Dent corn | Expected: Correct ID, high scores, corn-specific characteristics"];
        C2["ID: TC_C_002 | Desc: Corn with broken kernels and insect damage | Expected: Damage detected, low grade, relevant defects"];
        C3["ID: TC_C_003 | Desc: Popcorn kernels image | Expected: ID as Popcorn or Corn, notes on suitability"];
        C4["ID: TC_C_004 | Desc: User selects 'Rice', uploads Corn image | Expected: 'Grain Type Mismatch' error displayed (e.g., 'You selected Rice, AI detected Corn...'), no analysis results shown on main tab."];
    end
    
    subgraph GeneralTestCases["General/Cross-Cutting Test Cases"]
        G1["ID: TC_GEN_001 | Desc: Blurry/unsuitable image for any grain | Expected: `image_quality_assessment.suitable_for_analysis = false`, minimal analysis"];
        G2["ID: TC_GEN_002 | Desc: Image of non-grain material (e.g., pebbles) | Expected: AI identifies as 'Non-grain material' or 'Unknown', low confidence"];
        G3["ID: TC_GEN_003 | Desc: No grain selected by user, attempt to analyze | Expected: Error message, no API call"];
        G4["ID: TC_GEN_004 | Desc: API Key missing/invalid | Expected: Error message before API call attempt"];
        G5["ID: TC_GEN_005 | Desc: AI returns malformed JSON | Expected: Graceful error handling, 'Invalid JSON Response' message"];
        G6["ID: TC_GEN_006 | Desc: AI response blocked by content filter | Expected: 'Content Filter Block' error message"];
    end

    TC_Rice --> R1; TC_Rice --> R2; TC_Rice --> R3; TC_Rice --> R4; TC_Rice --> R5;
    TC_Wheat --> W1; TC_Wheat --> W2; TC_Wheat --> W3; TC_Wheat --> W4;
    TC_Corn --> C1; TC_Corn --> C2; TC_Corn --> C3; TC_Corn --> C4;
    TC_General --> G1; TC_General --> G2; TC_General --> G3; TC_General --> G4; TC_General --> G5; TC_General --> G6;

    note right of A "Each test case implies: Action (User input, image), Expected UI Output, Expected AI JSON (partial), Expected Session State changes."

    style RiceTestCases fill:#E0FFFF,stroke:#333,stroke-width:1px
    style WheatTestCases fill:#F0FFF0,stroke:#333,stroke-width:1px
    style CornTestCases fill:#FFFACD,stroke:#333,stroke-width:1px
    style GeneralTestCases fill:#FFE4E1,stroke:#333,stroke-width:1px

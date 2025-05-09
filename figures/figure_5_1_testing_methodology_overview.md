graph TD
    A[Testing Goal: Ensure Reliability, Accuracy, and Usability of GrainSight AI] --> B{Testing Levels};
    B --> B1[Unit Testing];
    B --> B2[Integration Testing];
    B --> B3[System/End-to-End Testing];
    B --> B4[User Acceptance Testing (UAT)];

    subgraph UnitTesting["Unit Testing (Python `unittest` or `pytest`)"]
        UT1["Test Helper Functions (e.g., `get_color_from_score`, `generate_prompt`)"];
        UT2["Test Individual UI Component Logic (where separable)"];
        UT3["Mock External Dependencies (e.g., Gemini API calls in `process_image`)"];
    end
    
    subgraph IntegrationTesting["Integration Testing"]
        IT1["Test UI Interactions with Backend Logic (e.g., button click -> state change -> UI update)"];
        IT2["Test `process_image` with Mocked AI Response (successful and error JSONs)"];
        IT3["Test Session State interactions between components/tabs"];
        IT4["Test `save_to_history` and history display logic"];
    end

    subgraph SystemTesting["System/End-to-End Testing (Manual & Potentially Automated with Selenium/Playwright)"]
        ST1["Full User Workflows:"];
        ST1_1["Select Grain -> Upload Image -> Analyze -> View Results -> View History"];
        ST1_2["Select Grain -> Take Photo -> Analyze -> View Results -> Change Settings"];
        ST2["Test with Various Image Qualities (Good, Poor, Unsuitable)"];
        ST3["Test with Different Grain Types"];
        ST4["Test Edge Cases (e.g., no grain selected, API key missing, network errors - simulated)"];
        ST5["Test UI Responsiveness and CSS Styling"];
        ST6["Verify Error Handling and Messaging"];
    end

    subgraph UAT["User Acceptance Testing (Real Users or Stakeholders)"]
        UAT1["Gather Feedback on Usability and User Experience"];
        UAT2["Verify if AI analysis aligns with expert expectations (qualitative)"];
        UAT3["Test on Different Devices/Browsers (if feasible)"];
    end

    C{Test Focus Areas};
    C --> F1[Functionality: Does it work as expected?];
    C --> F2[Accuracy: How well does AI perform (qualitative, comparison with known samples)?];
    C --> F3[Robustness: How does it handle errors and invalid inputs?];
    C --> F4[Usability: Is it easy to use and understand?];
    C --> F5[Performance: Is it reasonably fast (especially AI analysis step)?];

    D{Test Environment};
    D1["Local Development Environment"];
    D2["Staging Environment (if available)"];

    E{Test Data};
    E1["Sample Grain Images (Various types, qualities, defects)"];
    E2["Mock AI JSON Responses (for controlled testing of parsing and display)"];

    B1 --> UT1; B1 --> UT2; B1 --> UT3;
    B2 --> IT1; B2 --> IT2; B2 --> IT3; B2 --> IT4;
    B3 --> ST1; B3 --> ST2; B3 --> ST3; B3 --> ST4; B3 --> ST5; B3 --> ST6;
    B4 --> UAT1; B4 --> UAT2; B4 --> UAT3;

    A --> C; A --> D; A --> E;
    
    style UnitTesting fill:#E0FFFF,stroke:#333,stroke-width:1px
    style IntegrationTesting fill:#F0FFF0,stroke:#333,stroke-width:1px
    style SystemTesting fill:#FFFACD,stroke:#333,stroke-width:1px
    style UAT fill:#FFE4E1,stroke:#333,stroke-width:1px
    style C fill:#ADD8E6,stroke:#333,stroke-width:1px
    style D fill:#FAFAD2,stroke:#333,stroke-width:1px
    style E fill:#F5F5DC,stroke:#333,stroke-width:1px

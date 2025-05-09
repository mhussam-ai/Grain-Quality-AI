graph TD
    A[Goal: Systematically Collect, Analyze, and Act on User Feedback] --> B{Feedback Collection Methods};
    B --> BM_Surveys["Surveys (Post-UAT or In-App Pop-ups)"];
    B --> BM_Interviews["User Interviews (Targeted Users)"];
    B --> BM_Direct["Direct Feedback Channel (Email, Forum, In-App Form)"];
    B --> BM_Analytics["Usage Analytics (Indirect Feedback - e.g., drop-off points, feature usage)"];

    C{Feedback Categories for Analysis};
    C --> FC_Usability["Usability & UX (Ease of use, intuitiveness, clarity)"];
    C --> FC_Accuracy["Perceived AI Accuracy & Reliability"];
    C --> FC_Features["Feature Requests & Missing Functionality"];
    C --> FC_Bugs["Bug Reports & Technical Issues"];
    C --> FC_Performance["Perceived Speed & Responsiveness"];
    C --> FC_Overall["Overall Satisfaction"];

    D{Feedback Analysis Process};
    D1[Collection & Aggregation] --> D2[Categorization & Tagging (by theme, severity, etc.)];
    D2 --> D3[Prioritization (Impact vs. Effort)];
    D3 --> D4[Identify Trends & Patterns];
    D4 --> D5[Generate Actionable Insights & Recommendations];
    D5 --> D6[Share Findings with Development Team];

    E{Acting on Feedback};
    E1[Bug Fixing (Prioritize critical issues)];
    E2[Feature Enhancements (Based on popular requests & strategic goals)];
    E3[UX Improvements (Address pain points, improve clarity)];
    E4[Documentation Updates (Clarify confusing aspects)];
    E5[Communicate Changes to Users (Release notes, updates)];

    F{Feedback Loop};
    A --> B;
    B --> D1;
    D6 --> E;
    E --> G[Improved GrainSight AI Version];
    G --> B_NewFeedback["New Round of Feedback Collection"];
    B_NewFeedback --> D1;

    subgraph SampleSurveyQuestions["Sample Survey Questions (Conceptual)"]
        Q1["On a scale of 1-5, how easy was it to analyze a grain sample?"];
        Q2["How would you rate the accuracy of the AI's grain identification?"];
        Q3["Were the analysis results clear and understandable?"];
        Q4["What features would you like to see added?"];
        Q5["Did you encounter any technical issues?"];
    end

    BM_Surveys --> SampleSurveyQuestions;

    note right of A "This diagram outlines a structured approach to user feedback."

    style B fill:#E0FFFF,stroke:#333,stroke-width:1px
    style C fill:#F0FFF0,stroke:#333,stroke-width:1px
    style D fill:#FFFACD,stroke:#333,stroke-width:1px
    style E fill:#FFE4E1,stroke:#333,stroke-width:1px
    style F fill:#ADD8E6,stroke:#333,stroke-width:1px,border-style:dashed
    style SampleSurveyQuestions fill:#F5F5DC,stroke:#ccc,stroke-width:1px,border-style:dotted

graph TD
    A[Performance Testing Goal: Evaluate and Compare Key Metrics] --> B{Metrics Categories};

    B --> M_ResponseTime["Response Time"];
    B --> M_ResourceUsage["Resource Usage (Conceptual)"];
    B --> M_AccuracyConsistency["Accuracy/Consistency (Qualitative)"];

    subgraph ResponseTimeMetrics["Response Time Metrics"]
        RT1["End-to-End Analysis Time (User Click to Results Display)"];
        RT2["AI API Call Latency (`model.generate_content` duration)"];
        RT3["Image Upload/Processing Time (Client-side + Server-side before API call)"];
        RT4["UI Rendering Time (After receiving AI response)"];
    end
    
    subgraph ResourceUsageMetrics["Resource Usage (Conceptual - Requires Profiling Tools)"]
        RU1["Server-Side CPU/Memory (During image processing & AI call handling)"];
        RU2["Client-Side Browser Memory/CPU (For UI rendering, large images)"];
        RU3["Network Bandwidth (Image upload, API request/response size)"];
    end

    subgraph AccuracyConsistencyMetrics["Accuracy & Consistency (Qualitative & Comparative)"]
        AC1["Consistency of AI Output for Similar Images"];
        AC2["Impact of Image Size/Resolution on Analysis Time & Quality"];
        AC3["Comparison of AI Grades vs. Manual/Expert Grades (Sample Set)"];
    end

    C{Comparison Scenarios (Conceptual Examples)};
    C --> S1["Scenario 1: Small Image (e.g., <500KB) vs. Large Image (e.g., >5MB)"];
    S1 --> S1_RT["Expected: Longer upload, potentially longer API for large image"];
    S1 --> S1_RU["Expected: Higher bandwidth, potentially higher memory for large image"];
    
    C --> S2["Scenario 2: Clear, Well-lit Image vs. Blurry, Poorly-lit Image"];
    S2 --> S2_AC["Expected: Higher accuracy/confidence for clear image"];
    S2 --> S2_RT["Expected: API time might vary if AI struggles with poor image"];

    C --> S3["Scenario 3: Different Grain Types (e.g., Rice vs. Corn - assuming similar image quality)"];
    S3 --> S3_RT["Expected: API time might vary slightly based on complexity of features for each grain type"];

    D{Tools & Techniques for Measurement};
    D1["Browser Developer Tools (Network tab, Performance tab) for client-side times"];
    D2["Python `time` module or `cProfile` for server-side function timing"];
    D3["Logging API call durations"];
    D4["Manual observation and qualitative assessment for accuracy"];

    A --> C;
    A --> D;

    M_ResponseTime --> RT1; M_ResponseTime --> RT2; M_ResponseTime --> RT3; M_ResponseTime --> RT4;
    M_ResourceUsage --> RU1; M_ResourceUsage --> RU2; M_ResourceUsage --> RU3;
    M_AccuracyConsistency --> AC1; M_AccuracyConsistency --> AC2; M_AccuracyConsistency --> AC3;

    note right of A "This diagram outlines metrics and comparisons for performance evaluation.<br>Actual data would be gathered through testing."
    
    style ResponseTimeMetrics fill:#E0FFFF,stroke:#333,stroke-width:1px
    style ResourceUsageMetrics fill:#F0FFF0,stroke:#333,stroke-width:1px
    style AccuracyConsistencyMetrics fill:#FFFACD,stroke:#333,stroke-width:1px
    style C fill:#ADD8E6,stroke:#333,stroke-width:1px
    style D fill:#FAFAD2,stroke:#333,stroke-width:1px

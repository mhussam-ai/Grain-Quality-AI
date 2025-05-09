graph TD
    subgraph HistoryTab["History Tab"]
        direction TB
        Header["App Header: GrainSight AI 🔬"]
        TabHeader["Analysis History Header"]
        
        InfoMessage["Message: 'Displaying last X analyses (max Y).' OR 'No history yet.'"]
        
        subgraph HistoryList["Scrollable List of History Items"]
            direction TB
            subgraph HistoryItem1["History Item 1 (Card-like)"]
                direction LR
                Thumb1["Image Thumbnail (80x80)"]
                Details1["Analysis Title (e.g., Mismatch: Selected Rice (Detected Wheat))<br>Result: Grade (Score%)<br>Analyzed: Timestamp"]
                ViewButton1["View Details Button"]
            end
            Divider1["--- Divider ---"]
            subgraph HistoryItem2["History Item 2 (Card-like)"]
                direction LR
                Thumb2["Image Thumbnail"]
                Details2["Analysis Title (e.g., Analyzed: Corn)<br>Result: Grade (Score%)<br>Analyzed: Timestamp"]
                ViewButton2["View Details Button"]
            end
            Ellipsis["... more items ..."]
        end
        
        ClearHistoryButton["Clear Analysis History Button (Full Width)"]
        Footer["App Footer: Copyright, Disclaimers"]

        ViewButton1 -- "Loads analysis to Main Tab & Reruns" --> MainAnalysisTabRef("Ref: Main Analysis Tab")
        ViewButton2 -- "Loads analysis to Main Tab & Reruns" --> MainAnalysisTabRef
        ClearHistoryButton -- "Clears session_state.analysis_history & Reruns" --> HistoryList
    end

    style HistoryTab fill:#fff0f5,stroke:#333,stroke-width:2px
    style HistoryList fill:#f5f5f5,stroke:#ccc,stroke-width:1px,border-style:dashed
    style HistoryItem1 fill:#ffffff,stroke:#ddd,stroke-width:1px,border-radius:5px
    style HistoryItem2 fill:#ffffff,stroke:#ddd,stroke-width:1px,border-radius:5px
    style MainAnalysisTabRef fill:#add8e6,stroke:#333,stroke-width:1px,border-style:dotted

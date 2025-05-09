graph TD
    subgraph MainAnalysisTab["Main Analysis Tab"]
        direction LR
        Header["App Header: GrainSight AI 🔬"]
        SubHeader["Upload an image for detailed visual grain quality analysis."]
        
        subgraph InputSection["Input Section"]
            direction TB
            GrainSelect["1. Select Grain Type (Dropdown: Rice, Wheat, etc.)"]
            InstructionText["Instruction Text (Dynamic based on selected grain)"]
            InputButtons["Input Method Buttons"]
            UploadButton["📁 Upload [Grain] Image"]
            CameraButton["📷 Take Photo of [Grain]"]
            
            subgraph ConditionalInputArea["Conditional Input Area (Uploader or Camera)"]
                direction TB
                FileUploader["File Uploader (if Upload selected)"]
                CameraInput["Camera Input (if Take Photo selected)"]
            end
        end

        subgraph DisplaySection["Display & Analysis Section (Visible if image loaded)"]
            direction TB
            ImagePreviewHeader["Original Image Header"]
            ImageDisplay["Uploaded/Captured Image Preview"]
            AnalysisResultsHeader["Analysis Results Header"]
            
            subgraph ResultsArea["Results Area"]
                direction TB
                PlaceholderText["Initial State: '📊 Ready to analyze...' (Before analysis attempt)"]
                
                subgraph PostAnalysisDisplay["Post-Analysis Display (One of the following)"]
                    direction TB
                    style PostAnalysisDisplay fill:#f5fffa,stroke:#aaa,stroke-width:1px,border-style:dotted
                    SuccessState["✅ Successful Analysis Displayed (Metrics, Grade, Defects, etc.)"]
                    ErrorStateGeneric["🔴 Generic Error Displayed (e.g., API Failure, with details)"]
                    ErrorStateMismatch["🟠 Grain Mismatch Error Displayed ('You selected X, AI detected Y. Analysis for X cannot be shown.', with details)"]
                end
                
                PlaceholderText --> AnalyzeButtonBottom # User clicks Analyze
                AnalyzeButtonBottom -- Analysis Triggered --> PostAnalysisDisplay # Analysis leads to one of these states
            end
        end
        
        Footer["App Footer: Copyright, Disclaimers"]

        GrainSelect --> InstructionText
        GrainSelect --> UploadButton
        GrainSelect --> CameraButton
        UploadButton --> ConditionalInputArea
        CameraButton --> ConditionalInputArea
        ConditionalInputArea --> ImageDisplay
        ImageDisplay --> AnalyzeButtonBottom
    end

    style MainAnalysisTab fill:#f0f8ff,stroke:#333,stroke-width:2px
    style InputSection fill:#e6e6fa,stroke:#333,stroke-width:1px,border-style:dashed
    style DisplaySection fill:#fafad2,stroke:#333,stroke-width:1px,border-style:dashed
    style ConditionalInputArea fill:#fffacd,stroke:#ccc,stroke-width:1px,border-style:dotted
    style ResultsArea fill:#f0fff0,stroke:#333,stroke-width:1px,border-style:dashed

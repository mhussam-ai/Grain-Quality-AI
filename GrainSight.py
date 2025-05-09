import streamlit as st
import PIL.Image
import os
import tempfile
import json
import io
import google.generativeai as genai
from dotenv import load_dotenv
import re
import datetime
import base64

# Branding & Configuration
APP_TITLE = "GrainSight AI"
APP_ICON = "🔬"
FOOTER_TEXT = f"{APP_TITLE} © {datetime.datetime.now().year} | Advanced Grain Quality Analysis"
SUPPORTED_IMAGE_TYPES = ["jpg", "jpeg", "png"]
GRAIN_OPTIONS = ["Rice", "Wheat", "Barley", "Corn", "Oats", "Sorghum"]
GEMINI_MODEL = "gemini-2.0-flash" # Model used by the backend
HISTORY_LIMIT = 10 # Configurable number of history items

# Load API Key
load_dotenv()
api_key = os.environ.get("GOOGLE_API_KEY")

# Set Page Config
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide" # Use wide layout like RiceQual
)

# Custom CSS (Copied and adapted from RiceQual)
st.markdown("""
<style>
    /* Main styling */
    .main-header {
        font-size: 2.5rem; /* Adjusted size */
        color: #2c3e50; /* Slightly different color */
        margin-bottom: 0.5rem;
        font-weight: 700;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #576574;
        margin-bottom: 2rem;
        font-weight: 400;
    }
    .section-header {
        font-size: 1.5rem;
        color: #2c3e50;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        font-weight: 600;
        border-bottom: 2px solid #e0e0e0;
        padding-bottom: 0.3rem;
    }

    /* Instruction panel */
    .instruction-text {
        background-color: #eaf4ff; /* Light blue */
        padding: 1.2rem;
        border-radius: 8px;
        margin-bottom: 1.5rem;
        border-left: 4px solid #5fa8d3; /* Different blue */
        color: #1a1a1a;
        font-size: 1.05rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }

    /* Quality indicators */
    .quality-excellent { color: #27ae60; font-weight: bold; } /* Green */
    .quality-good { color: #2ecc71; font-weight: bold; } /* Lighter Green */
    .quality-fair { color: #f39c12; font-weight: bold; } /* Orange */
    .quality-poor { color: #e74c3c; font-weight: bold; } /* Red */
    .quality-na { color: #7f8c8d; font-weight: bold; } /* Grey */


    /* Image container */
    .stImage img {
        max-height: 350px !important;
        width: auto !important;
        margin: 0 auto !important;
        display: block !important;
        border-radius: 8px !important;
        border: 1px solid #ddd;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05) !important;
    }

    /* Metric cards */
    .metric-card {
        background-color: #ffffff;
        border-radius: 8px;
        padding: 1.2rem;
        margin-bottom: 1rem;
        border: 1px solid #e0e0e0;
        transition: box-shadow 0.3s ease;
        color: #333;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .metric-card:hover {
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    .metric-card h4 { margin-top: 0; color: #5fa8d3; } /* Blue header */


    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 4px 4px 0 0;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
        font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        background-color: rgba(95, 168, 211, 0.1); /* Light blue */
        border-bottom: 3px solid #5fa8d3; /* Blue border */
        color: #2c3e50;
    }

    /* General Button enhancements */
    div.stButton > button:first-child {
        background-color: #ffffff;
        border: 1px solid #cccccc;
        padding: 0.6rem 1.2rem;
        font-weight: 500;
        border-radius: 8px;
        transition: all 0.3s ease;
        color: #333;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
        font-size: 0.95rem;
    }
    div.stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 3px 6px rgba(0, 0, 0, 0.1);
        border-color: #5fa8d3;
        background-color: #f8f9fa;
    }

     /* Custom styling for primary buttons */
    button[data-testid="baseButton-primary"] {
        background-color: #5fa8d3 !important; /* Main blue */
        color: white !important;
        border: none !important;
        box-shadow: 0 4px 6px rgba(95, 168, 211, 0.2) !important;
        border-radius: 8px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
    }
    button[data-testid="baseButton-primary"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 12px rgba(95, 168, 211, 0.3) !important;
        background-color: #4a90b5 !important; /* Darker blue */
    }

    /* Special Analyze button */
    .analyze-button > div > button { /* Target the inner button */
        background-color: #27ae60 !important; /* Green for analyze */
        color: white !important;
        font-weight: 600 !important;
        padding: 0.8rem 1.8rem !important;
        font-size: 1.1rem !important;
        width: 100% !important;
        box-shadow: 0 4px 6px rgba(39, 174, 96, 0.2) !important;
    }
    .analyze-button > div > button:hover {
        background-color: #229954 !important; /* Darker green */
        box-shadow: 0 6px 12px rgba(39, 174, 96, 0.3) !important;
    }

    /* History table styling (if we use a table) */
    .history-table { width: 100%; border-collapse: collapse; }
    .history-table th, .history-table td { padding: 10px; text-align: left; border-bottom: 1px solid #ddd; color: #333; }
    .history-table tr:hover { background-color: #f5f5f5; }

    /* Loader animation */
    @keyframes pulse { 0% { opacity: 0.6; } 50% { opacity: 1; } 100% { opacity: 0.6; } }
    .loading-pulse { animation: pulse 1.5s infinite; }

    /* Circular progress bars */
    .progress-circle { position: relative; width: 100px; height: 100px; border-radius: 50%; margin: 0 auto; text-align: center; }
    .progress-circle-bg { width: 100%; height: 100%; border-radius: 50%; background-color: #e0e0e0; position: absolute; }
    .progress-circle-fill-wrapper { position: absolute; width: 100%; height: 100%; clip: rect(0px, 100px, 100px, 50px); }
    .progress-circle-fill { position: absolute; width: 100%; height: 100%; border-radius: 50%; clip: rect(0px, 50px, 100px, 0px); background-color: #5fa8d3; /* Default color */ }
    .progress-circle-value { position: absolute; width: 80%; height: 80%; border-radius: 50%; background-color: white; top: 10%; left: 10%; display: flex; align-items: center; justify-content: center; font-size: 1.5rem; font-weight: bold; color: #333; flex-direction: column; line-height: 1.1; }
    .progress-label { font-size: 0.7rem; color: #555; margin-top: 3px; }

    /* Responsive design */
    @media (max-width: 768px) {
        .main-header { font-size: 2rem; }
        .sub-header { font-size: 1rem; }
        .section-header { font-size: 1.2rem; }
        .metric-card { padding: 0.8rem; }
        .progress-circle { width: 80px; height: 80px; }
        .progress-circle-fill-wrapper { clip: rect(0px, 80px, 80px, 40px); }
        .progress-circle-fill { clip: rect(0px, 40px, 80px, 0px); }
        .progress-circle-value { font-size: 1.2rem; }
        .stTabs [data-baseweb="tab"] { padding-left: 8px; padding-right: 8px; height: 45px; }
    }
    .stAlert { border-radius: 8px; } /* Style alerts */
    
    .analyze-button-bottom > div > button { /* Target the inner button */
        background-color: #27ae60 !important; /* Green */
        color: white !important;
        font-weight: 600 !important;
        padding: 0.9rem 2rem !important; /* Make it taller */
        font-size: 1.2rem !important; /* Larger font */
        width: 100% !important;
        border-radius: 8px !important;
        border: none !important;
        box-shadow: 0 4px 8px rgba(39, 174, 96, 0.25) !important;
        margin-top: 1.5rem !important; /* Add space above */
        transition: all 0.3s ease !important;
    }
    .analyze-button-bottom > div > button:hover {
        background-color: #229954 !important; /* Darker green */
        box-shadow: 0 6px 12px rgba(39, 174, 96, 0.35) !important;
        transform: translateY(-2px) !important;
    }
    .image-preview-column {
        display: flex;
        flex-direction: column;
        justify-content: center; /* Vertically center content */
        align-items: center; /* Horizontally center content */
        height: 350px; /* Match max image height from other CSS */
        background-color: #f8f9fa; /* Light background for placeholder */
        border-radius: 8px;
        border: 1px dashed #ccc;
        padding: 1rem;
        text-align: center;
    }
}


</style>
""", unsafe_allow_html=True)

# Initialize Session State
if 'image_data' not in st.session_state:
    st.session_state.image_data = None
if 'image_source' not in st.session_state: # Track if it came from upload or camera
    st.session_state.image_source = None
if 'analysis_history' not in st.session_state:
    st.session_state.analysis_history = []
if 'current_analysis' not in st.session_state:
    st.session_state.current_analysis = None
if 'selected_grain' not in st.session_state:
    st.session_state.selected_grain = None
if 'last_analysis_grain' not in st.session_state: # Track grain type of the current analysis result
    st.session_state.last_analysis_grain = None
if 'history_limit' not in st.session_state:
    st.session_state.history_limit = HISTORY_LIMIT
if 'show_uploader' not in st.session_state:
    st.session_state.show_uploader = False
if 'show_camera' not in st.session_state:
    st.session_state.show_camera = False




# Helper Functions

def get_color_from_score(score):
    """Returns a color class based on a 0-100 score."""
    if score is None or not isinstance(score, (int, float)): return "na"
    if score >= 90: return "excellent"
    if score >= 75: return "good"
    if score >= 60: return "fair"
    return "poor"

def get_color_from_grade(grade):
    """Returns a color class based on grade string."""
    if not grade or not isinstance(grade, str): return "na"
    grade_lower = grade.lower()
    if grade_lower == "excellent": return "excellent"
    if grade_lower == "good": return "good"
    if grade_lower == "fair": return "fair"
    if grade_lower == "poor": return "poor"
    return "na"

def render_progress_circle(value, label, color_class="blue"):
    """Renders a circular progress bar with CSS."""
    # Map quality classes to hex colors
    color_map = {
        "excellent": "#27ae60", "good": "#2ecc71",
        "fair": "#f39c12", "poor": "#e74c3c",
        "blue": "#5fa8d3", "na": "#bdc3c7" # Grey for N/A
    }
    fill_color = color_map.get(color_class, "#bdc3c7") # Default to grey if class unknown

    # Normalize value for display (handle N/A)
    display_value = "N/A"
    progress_value = 0
    if value is not None and isinstance(value, (int, float)):
        display_value = f"{int(value)}%"
        progress_value = max(0, min(100, value)) # Clamp between 0 and 100

    # Calculate rotation for the progress bar fill
    # Rotation logic might need adjustment based on exact CSS implementation
    rotation = (progress_value / 100) * 360

    fill_style = f"transform: rotate({rotation}deg);" if rotation <= 180 else ""
    wrapper_style = f"transform: rotate(180deg);" if rotation > 180 else ""
    fill_bg_color = f"background-color: {fill_color};"


    html = f"""
    <div class="progress-circle">
        <div class="progress-circle-bg"></div>
        <div class="progress-circle-fill-wrapper" style="{wrapper_style}">
            <div class="progress-circle-fill" style="{fill_style} {fill_bg_color}"></div>
        </div>
        <div class="progress-circle-value">
            <div>{display_value}</div>
            <div class="progress-label">{label}</div>
        </div>
    </div>
    """
    return html

def generate_prompt(grain_type):
    """Generates the Gemini API prompt based on the selected grain type. (FROM ORIGINAL MULTIGRAIN)"""
    if not grain_type:
        return None
    # Using the EXACT JSON structure from the original MultiGrain code
    json_structure_string = """
        {
            "grain_identity": {
                "detected_grain": "string",
                "variety_or_class": "string",
                "characteristics": "string"
            },
            "quality_assessment": {
                "integrity": { "whole_percentage": number, "description": "string" },
                "uniformity": { "score": number, "description": "string" },
                "maturity": { "percentage_immature": number, "description": "string" },
                "foreign_matter": { "detected": boolean, "description": "string" },
                "storage_soundness": { "detected_issues": boolean, "description": "string" }
            },
            "defects": {
                "discoloration": { "severity": "string", "description": "string" },
                "physical_damage": { "severity": "string", "description": "string" },
                "disease_or_mold": { "detected": boolean, "description": "string" },
                "sprouting": { "detected": boolean, "description": "string" },
                "specific_defects": { "type": "string", "severity": "string", "description": "string" }
            },
            "overall_grade": { "grade": "string", "score": number, "explanation": "string" },
            "usage_recommendations": { "primary_uses": ["string"], "cooking_or_processing": "string", "storage_tips": "string" },
            "image_quality_assessment": { "suitable_for_analysis": boolean, "comments": "string" },
            "additional_notes": "string"
        }
    }"""
    grain_examples = {
        "Rice": "Basmati, Jasmine, Arborio, Long/Medium/Short grain", "Wheat": "Hard Red Winter, Soft White, Durum",
        "Barley": "Two-Row, Six-Row, Hulled, Hulless", "Corn": "Yellow Dent, White Corn, Popcorn",
        "Oats": "Rolled, Steel-cut, Whole groats", "Sorghum": "Grain Sorghum, White, Red"
    }
    example_text = grain_examples.get(grain_type, "Specific type")

    # Modified Prompt for Clarity and Branding
    prompt = f"""
You are GrainSight AI, an expert system for visual grain quality analysis. Analyze the provided image assumed to contain {grain_type} grains.

**Task:** Provide a comprehensive quality assessment of the grain sample in the image.

**Analysis Steps:**

1.  **Image & Grain Verification (CRITICAL):**
    *   Identify the primary grain type visible in the image. Report this *accurately* in `grain_identity.detected_grain`.
    *   Assess image quality (clarity, lighting) for analysis suitability. Report in `image_quality_assessment`.
    *   **If the image is unsuitable OR if the detected grain is CLEARLY NOT {grain_type}, state this directly in `grain_identity.detected_grain` and `image_quality_assessment.comments`, and provide minimal details in other fields.**

2.  **{grain_type}-Specific Analysis (ONLY if image is suitable AND detected grain matches {grain_type}):**
    *   **Grain Identity:** Confirm grain type ({grain_type}), attempt to identify variety/class (e.g., {example_text}) and note visual characteristics.
    *   **Quality Assessment:** Evaluate grain integrity (% whole grains), uniformity (visual consistency, score 0-100), maturity (% visually immature/shriveled), presence of foreign matter, and any visual signs of poor storage (mold, insects, off-color).
    *   **Defect Detection:** Identify and describe discoloration, physical damage (broken, cracked), disease/mold signs, sprouting, and any {grain_type}-specific defects (like chalkiness in Rice, ergot in Wheat/Barley). Note severity where applicable (e.g., None, Low, Moderate, High). If a defect category isn't applicable, note that.
    *   **Overall Grading:** Assign an overall quality grade (Excellent, Good, Fair, Poor) and a numerical score (0-100). Explain the key visual factors influencing this grade.
    *   **Usage Recommendations:** Suggest potential primary uses (e.g., Food, Feed, Milling, Seed) based on visual quality and provide general storage tips.

**Output Format:**
Return **ONLY** a valid JSON object precisely matching this structure. Ensure all keys are present. Use `null` or appropriate defaults (e.g., empty strings, `false`, `0`) if a value cannot be determined from the image. Do not include markdown formatting (like ```json) or any other text outside the JSON object itself.

```json
{json_structure_string}
```

**Important:** Base your analysis strictly on visual information. Acknowledge limitations clearly. Your primary function is accurate visual assessment. Avoid making assumptions beyond what's visible.
"""
    return prompt

def process_image(image_bytes, api_key, grain_type):
    """Processes the image using the AI backend. (FROM ORIGINAL MULTIGRAIN, slight modification for clarity)"""
    # --- Input Validation ---
    if not api_key:
        return {"error": "API Key Missing", "raw_text": "API key not configured."}, False
    if not grain_type:
        return {"error": "Grain Type Missing", "raw_text": "No grain type was selected."}, False
    if not image_bytes:
        return {"error": "Image Data Missing", "raw_text": "No image data provided."}, False

    # Prepare for API Call
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name=GEMINI_MODEL)
        image_part = {"mime_type": "image/jpeg", "data": image_bytes} # Assume JPEG for API
        prompt_text = generate_prompt(grain_type)
        if not prompt_text:
             return {"error": "Prompt Generation Failed", "raw_text": "Could not create analysis prompt."}, False

    except Exception as e:
         st.error(f"Error during AI setup: {e}")
         return {"error": "AI Client Configuration Error", "raw_text": str(e)}, False

    # Make API Call
    try:
        # Use a timeout for the request (e.g., 60 seconds)
        response = model.generate_content([prompt_text, image_part], request_options={'timeout': 60})

    except Exception as e:
        # Catch potential API call errors (network, timeout, auth, etc.)
        st.error(f"AI API Call Error: {e}")
        # Provide more specific feedback if possible (check error type)
        if "DeadlineExceeded" in str(e):
            return {"error": "Analysis Timeout", "raw_text": "The analysis took too long to complete. Try reducing image size or check network."}, False
        return {"error": f"AI API Call Failed", "raw_text": str(e)}, False

    # Parse API Response
    try:
        # 1. Check for safety blocks or empty response
        if not response.candidates:
            block_reason = "Unknown"
            finish_reason = "Unknown"
            try: # Safely access feedback attributes
                 if response.prompt_feedback:
                      block_reason = response.prompt_feedback.block_reason or block_reason
                 # Check candidate finish reason if available (though candidates list is empty)
                 # This part might be less reliable if candidates is empty
                 # finish_reason = response.candidates[0].finish_reason or finish_reason
            except Exception:
                 pass # Ignore errors accessing feedback details
            # Customize error message based on reason if needed
            error_msg = f"Analysis blocked by content filters ({block_reason})." if block_reason != "Unknown" else "Analysis failed (Empty Response)."
            return {"error": "Content Filter Block or Empty Response", "raw_text": f"Reason: {block_reason}. Full Response: {str(response)}"}, False

        # 2. Extract text content
        full_response_text = response.candidates[0].content.parts[0].text

        # 3. Find JSON block (more robust)
        json_match = re.search(r'\{.*\}', full_response_text, re.DOTALL) # Find first '{' to last '}'
        if json_match:
            json_str = json_match.group(0)
        else:
            # If no curly braces found, it's definitely not JSON
            return {"error": "Invalid Response Format", "raw_text": f"AI response did not contain a JSON structure.\nResponse:\n{full_response_text}"}, False

        # 4. Parse JSON
        result = json.loads(json_str)

        # 5. Basic check for image suitability note from AI
        img_quality = result.get("image_quality_assessment", {})
        if not img_quality.get("suitable_for_analysis", True):
             st.warning(f"AI Note on Image Quality: {img_quality.get('comments', 'Analysis may be affected.')}")

        return result, True # Success

    except json.JSONDecodeError as e:
        st.error(f"AI Response Parsing Error: Could not decode JSON.")
        # Try to show the problematic text
        return {"error": "Invalid JSON Response", "raw_text": f"JSON Parse Error: {e}\nAttempted to parse:\n{json_str}"}, False
    except IndexError:
        return {"error": "Invalid Response Structure", "raw_text": f"Could not access expected parts in AI response.\nResponse:\n{str(response)}"}, False
    except Exception as e: # Catch other unexpected errors during response handling
        st.error(f"Error processing AI response: {e}")
        return {"error": "Response Processing Error", "raw_text": str(response)}, False


def save_to_history(analysis, image_data, selected_grain):
    """Saves analysis result and thumbnail to session state history."""
    if not analysis or not image_data or not selected_grain:
        return

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Create thumbnail
    try:
        image = PIL.Image.open(io.BytesIO(image_data))
        image.thumbnail((100, 100))
        buffered = io.BytesIO()
        # Ensure saving as JPEG for consistency, handle potential RGBA issues
        if image.mode == 'RGBA':
            image = image.convert('RGB')
        image.save(buffered, format="JPEG", quality=85)
        img_str = base64.b64encode(buffered.getvalue()).decode()
    except Exception as e:
        st.warning(f"Could not create thumbnail for history: {e}")
        img_str = None # Store None if thumbnail fails

    history_item = {
        "timestamp": timestamp,
        "selected_grain": selected_grain, # Store which grain was *selected* for context
        "analysis": analysis, # Can be success or error dict
        "image_thumbnail": img_str
    }

    st.session_state.analysis_history.insert(0, history_item) # Add to beginning

    # Limit history size
    limit = st.session_state.get('history_limit', HISTORY_LIMIT)
    st.session_state.analysis_history = st.session_state.analysis_history[:limit]


def render_analysis_results(analysis):
    """Displays the structured analysis results visually (Adapted from RiceQual)."""
    if not analysis or not isinstance(analysis, dict):
        st.error("No valid analysis data to display.")
        return

    # Handle Top-Level Errors First
    if 'error' in analysis:
        st.error(f"🔴 Analysis Failed: {analysis.get('error', 'Unknown error')}")
        if 'raw_text' in analysis and analysis['raw_text']:
            with st.expander("Error Details"):
                st.text(analysis['raw_text'])
        return

    # Extract Data Safely
    identity = analysis.get('grain_identity', {})
    quality = analysis.get('quality_assessment', {})
    defects = analysis.get('defects', {})
    grade_info = analysis.get('overall_grade', {})
    recommendations = analysis.get('usage_recommendations', {})
    img_quality_notes = analysis.get('image_quality_assessment', {})

    detected_grain = identity.get('detected_grain', 'N/A')
    selected_grain = st.session_state.get('selected_grain', 'N/A') # Get user's selection

    # The specific mismatch warning here is removed, as it's handled by the main error display now.

    st.markdown('<h2 class="section-header">Analysis Summary</h2>', unsafe_allow_html=True)

    # Row 1: Overall Grade & Detected Type
    col1, col2 = st.columns([1, 2])
    with col1:
        grade_score = grade_info.get('score')
        grade_text = grade_info.get('grade', 'N/A')
        grade_color = get_color_from_grade(grade_text) # Get color from grade text

        st.markdown(
             render_progress_circle(grade_score, f"Overall: {grade_text}", grade_color),
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h4>Detected Grain Identity</h4>
            <p style="font-size: 1.3rem; font-weight: 600;">{identity.get('detected_grain', 'N/A')}</p>
            <p><strong>Variety/Class:</strong> {identity.get('variety_or_class', 'N/A')}</p>
            <p><strong>Characteristics:</strong> {identity.get('characteristics', 'N/A')}</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<h3 class="section-header">Quality Metrics</h3>', unsafe_allow_html=True)

    # Row 2: Key Quality Metrics (Integrity, Uniformity, Maturity, Defects)
    cols = st.columns(4)
    # Integrity
    integrity_pct = quality.get('integrity', {}).get('whole_percentage')
    integrity_color = get_color_from_score(integrity_pct)
    with cols[0]:
        st.markdown(render_progress_circle(integrity_pct, "Integrity", integrity_color), unsafe_allow_html=True)

    # Uniformity
    uniformity_score = quality.get('uniformity', {}).get('score')
    uniformity_color = get_color_from_score(uniformity_score)
    with cols[1]:
        st.markdown(render_progress_circle(uniformity_score, "Uniformity", uniformity_color), unsafe_allow_html=True)

    # Maturity (Lower % immature is better, so score is 100 - % immature)
    immature_pct = quality.get('maturity', {}).get('percentage_immature')
    maturity_score = (100 - immature_pct) if isinstance(immature_pct, (int, float)) else None
    maturity_color = get_color_from_score(maturity_score)
    with cols[2]:
        st.markdown(render_progress_circle(maturity_score, "Maturity", maturity_color), unsafe_allow_html=True)

    # Defect Score (Lower defect presence/severity is better)
    defect_score = 0
    defect_count = 0
    severity_map = {"none": 0, "low": 30, "moderate": 70, "high": 100, None: 0} # Map severity strings

    for defect_key, defect_info in defects.items():
        if isinstance(defect_info, dict):
            if 'severity' in defect_info:
                severity = str(defect_info.get('severity', 'none')).lower()
                defect_score += severity_map.get(severity, 50) # Add 50 for unknown severity
                defect_count += 1
            elif 'detected' in defect_info and defect_info.get('detected'):
                defect_score += 100 # High penalty for detected boolean defects
                defect_count += 1

    # Calculate overall defect quality (0-100, higher is better)
    defect_quality = (100 - (defect_score / defect_count)) if defect_count > 0 else 100
    defect_color = get_color_from_score(defect_quality)
    with cols[3]:
        st.markdown(render_progress_circle(defect_quality, "Defect Level", defect_color), unsafe_allow_html=True)


    # Expanders for Detailed Sections
    st.markdown('<h3 class="section-header">Detailed Analysis</h3>', unsafe_allow_html=True)

    with st.expander("Detailed Quality Assessment"):
        q_int = quality.get('integrity', {})
        q_uni = quality.get('uniformity', {})
        q_mat = quality.get('maturity', {})
        q_fm = quality.get('foreign_matter', {})
        q_ss = quality.get('storage_soundness', {})

        st.markdown(f"**Grain Integrity:** {q_int.get('whole_percentage', 'N/A')}% whole. {q_int.get('description', '')}")
        st.markdown(f"**Color & Size Uniformity:** Score {q_uni.get('score', 'N/A')}/100. {q_uni.get('description', '')}")
        st.markdown(f"**Grain Maturity:** {q_mat.get('percentage_immature', 'N/A')}% immature/shriveled. {q_mat.get('description', '')}")
        st.markdown(f"**Foreign Matter:** {'Detected' if q_fm.get('detected') else 'Not detected'}. {q_fm.get('description', '')}")
        st.markdown(f"**Storage Soundness:** Issues {'Detected' if q_ss.get('detected_issues') else 'Not detected'}. {q_ss.get('description', '')}")

    with st.expander("Defect Analysis"):
        if not defects:
            st.info("No specific defect data provided.")
        else:
            for key, info in defects.items():
                display_key = key.replace('_', ' ').title()
                desc = info.get('description', 'N/A')
                details = []
                if 'severity' in info: details.append(f"Severity: {info.get('severity', 'N/A')}")
                if 'detected' in info: details.append(f"Detected: {'Yes' if info.get('detected') else 'No'}")
                if 'type' in info and info.get('type'): details.append(f"Type: {info.get('type')}")
                st.markdown(f"**{display_key}:** {' | '.join(details)} - *{desc}*")

    with st.expander("Usage Recommendations"):
        st.markdown(f"**Primary Uses:** {', '.join(recommendations.get('primary_uses', ['N/A']))}")
        st.markdown(f"**Cooking/Processing Notes:** {recommendations.get('cooking_or_processing', 'N/A')}")
        st.markdown(f"**Storage Tips:** {recommendations.get('storage_tips', 'N/A')}")

    # Optional Sections
    add_notes = analysis.get('additional_notes')
    if add_notes:
        with st.expander("Additional Notes from AI"):
            st.write(add_notes)

    # Image Quality Assessment Notes from AI
    if not img_quality_notes.get("suitable_for_analysis", True):
        with st.expander("AI Image Quality Assessment"):
            st.warning(f"Image suitability comment: {img_quality_notes.get('comments', 'N/A')}")

    # Raw JSON for debugging
    with st.expander("Show Raw AI Response (JSON)"):
        st.json(analysis)


# Main App UI (Using Tabs)
st.markdown(f'<h1 class="main-header">{APP_ICON} {APP_TITLE}</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Upload an image for detailed visual grain quality analysis.</p>', unsafe_allow_html=True)

# API Key Check
if not api_key:
    st.error("🔴 AI Engine API key not found.")
    st.warning("Please ensure the `GOOGLE_API_KEY` environment variable is set correctly.")
    st.stop() # Stop execution if no key

# Sidebar
with st.sidebar:
    st.image("https://www.gstatic.com/mobilesdk/160503_mobilesdk/logo/2x/firebase_28dp.png", width=50) # Placeholder logo
    st.header("How It Works")
    st.markdown("""
    1.  **Select** the expected grain type.
    2.  **Upload** a clear image or **take a photo** of the grain sample.
    3.  Click **Analyze**.
    4.  The AI engine assesses **identity, quality, defects,** and provides **recommendations**.
    """)
    st.markdown("---")
    st.header("Tips for Best Results")
    st.markdown("""
    *   Use **bright, even lighting**.
    *   Place grains on a **plain, contrasting background**.
    *   **Spread grains** thinly, avoiding overlap.
    *   Ensure the image is **in focus**.
    """)
    st.markdown("---")
    st.info(f"History Limit: {st.session_state.history_limit} items")


# Create Tabs
tab1, tab2, tab3 = st.tabs(["🔬 Analysis", "📊 History", "⚙️ Settings"])

# Tab 1: Analysis
# --- Tab 1: Analysis ---
with tab1:
    st.markdown('<h2 class="section-header">Grain Sample Analysis</h2>', unsafe_allow_html=True)

    # Step 1: Grain Selection
    selected_grain_option = st.selectbox(
        "**1. Select the expected grain type:**",
        options=[None] + GRAIN_OPTIONS, # Add None for placeholder
        index=0 if st.session_state.selected_grain is None else GRAIN_OPTIONS.index(st.session_state.selected_grain) + 1, # Maintain selection across reruns
        format_func=lambda x: "Select grain..." if x is None else x,
        key="grain_select_widget_main" # Use a consistent key
    )

    # Update session state only if selection *changes*
    if selected_grain_option != st.session_state.get('selected_grain'):
        st.session_state.selected_grain = selected_grain_option
        # Clear image, analysis, and UI flags when grain type changes
        st.session_state.image_data = None
        st.session_state.current_analysis = None
        st.session_state.image_source = None
        st.session_state.last_analysis_grain = None
        st.session_state.show_uploader = False # Reset UI flags
        st.session_state.show_camera = False

    # Proceed only if a grain is selected
    if st.session_state.selected_grain:
        grain_name = st.session_state.selected_grain # Use the selected grain name

        # Instructions
        st.markdown(f"""
        <div class="instruction-text">
            <strong>Instructions:</strong> Upload a clear image of your <strong>{grain_name}</strong> sample or take a photo.
            For best results, ensure good lighting and place grains on a contrasting background.
            <br>
            <br>
            Based on visual assessment only. Further laboratory analysis would be needed for a comprehensive quality report.
        </div>
        """, unsafe_allow_html=True)

        # Step 2: Input Method Selection Buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button(f"📁 Upload {grain_name} Image", use_container_width=True):
                st.session_state.show_uploader = True
                st.session_state.show_camera = False
                # Clear any existing image data if switching input methods
                if st.session_state.image_source == "camera":
                    st.session_state.image_data = None
                    st.session_state.current_analysis = None
                st.rerun()

        with col2:
            if st.button(f"📷 Take Photo of {grain_name}", use_container_width=True):
                st.session_state.show_camera = True
                st.session_state.show_uploader = False
                # Clear any existing image data if switching input methods
                if st.session_state.image_source == "upload":
                    st.session_state.image_data = None
                    st.session_state.current_analysis = None
                st.rerun()

        # Step 3: Display Input Widget Conditionally
        if st.session_state.show_uploader:
            uploaded_file = st.file_uploader(
                f"Upload {grain_name} image file",
                type=SUPPORTED_IMAGE_TYPES,
                key=f"upload_widget_{grain_name}", # Key changes with grain to reset
                label_visibility="collapsed"
            )
            if uploaded_file:
                new_image_data = uploaded_file.getvalue()
                # Update only if image data is different to prevent unnecessary reruns
                if new_image_data != st.session_state.get('image_data'):
                    st.session_state.image_data = new_image_data
                    st.session_state.image_source = "upload"
                    st.session_state.current_analysis = None # Clear old analysis on new image
                    st.rerun() # Rerun to display the image preview

        if st.session_state.show_camera:
            camera_image = st.camera_input(
                f"Take photo of {grain_name} sample",
                key=f"camera_widget_{grain_name}", # Key changes with grain to reset
                label_visibility="collapsed"
            )
            if camera_image:
                new_image_data = camera_image.getvalue()
                # Update only if image data is different
                if new_image_data != st.session_state.get('image_data'):
                    st.session_state.image_data = new_image_data
                    st.session_state.image_source = "camera"
                    st.session_state.current_analysis = None # Clear old analysis on new image
                    st.rerun() # Rerun to display the image preview


        # Step 4: Display Image Preview and Analysis Area (if image data exists)
        if st.session_state.image_data:

            st.markdown("---") # Separator

            st.markdown('<h3 class="section-header">Original Image</h3>', unsafe_allow_html=True)
            st.image(st.session_state.image_data, caption=f"Image for '{grain_name}' analysis", use_container_width=True)

            st.markdown('<h3 class="section-header">Analysis Results</h3>', unsafe_allow_html=True)
            # Check if analysis results exist and are relevant
            analysis_to_render = None
            should_display = False
            if st.session_state.current_analysis:
                current_result = st.session_state.current_analysis
                grain_context = st.session_state.last_analysis_grain # What the analysis is actually about

                if 'error' in current_result and current_result['error'] == "Grain Type Mismatch":
                    should_display = True
                    analysis_to_render = current_result # Pass the full error object to render_analysis_results
                elif 'error' in current_result:
                    # Only display error if it corresponds to the *selected* grain attempt
                    if st.session_state.last_analysis_grain == grain_name:
                        should_display = True
                        analysis_to_render = current_result
                elif grain_context and grain_context.lower() == grain_name.lower():
                    # Display successful analysis if detected/analyzed grain matches selected grain
                    should_display = True
                    analysis_to_render = current_result

            if should_display and analysis_to_render:
                render_analysis_results(analysis_to_render) # Call the existing display function
            else:
                # Show placeholder if no analysis or analysis is for different grain
                st.markdown("""
                <div class="image-preview-column">
                    <p>📊 Ready to analyze your sample.</p>
                    <p style="font-size: 0.9em; color: #666;">Click the 'Analyze' button below.</p>
                </div>
                """, unsafe_allow_html=True)


            # Step 5: Show Large Analyze Button AT THE BOTTOM (only if image exists)
            st.markdown('<div class="analyze-button-bottom">', unsafe_allow_html=True)
            analyze_button = st.button(f"Analyze {grain_name} Sample", type="primary", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

            if analyze_button:
                with st.spinner(f"🧠 Analyzing '{grain_name}' sample... Please wait."):
                    # --- (Analysis Logic - Copied from previous version, NO CHANGES NEEDED HERE) ---
                    analysis_result, success = process_image(
                            st.session_state.image_data,
                            api_key,
                            grain_name # Pass the currently selected grain name
                        )
                    if success:
                        detected_grain = analysis_result.get('grain_identity', {}).get('detected_grain')
                        if detected_grain and isinstance(detected_grain, str) and \
                           detected_grain.lower() != grain_name.lower() and \
                           detected_grain.lower() not in ["unknown", "n/a", "multiple types", "non-grain material"]:
                            success = False
                            mismatch_error = {
                                 "error": "Grain Type Mismatch",
                                 "raw_text": f"Image Mismatch: You selected '{grain_name}', but the AI detected '{detected_grain}'. Analysis for '{grain_name}' cannot be shown. Please select '{detected_grain}' if you wish to analyze this image, or upload an image of '{grain_name}'.",
                                 "analysis_data_for_detected_grain": analysis_result # Kept for history/debug
                            }
                            st.session_state.current_analysis = mismatch_error # Store the full error object
                            st.session_state.last_analysis_grain = detected_grain
                            save_to_history(mismatch_error, st.session_state.image_data, grain_name)
                        else:
                            st.session_state.current_analysis = analysis_result
                            st.session_state.last_analysis_grain = detected_grain or grain_name
                            save_to_history(analysis_result, st.session_state.image_data, grain_name)
                    else:
                         st.session_state.current_analysis = analysis_result
                         st.session_state.last_analysis_grain = grain_name
                         save_to_history(analysis_result, st.session_state.image_data, grain_name)
                    # --- (End of Analysis Logic) ---
                st.rerun() # Rerun to display results immediately

    # Message if no grain is selected yet
    elif st.session_state.selected_grain is None:
        st.info("☝️ Select a grain type above to begin the analysis process.")



# Tab 2: History
with tab2:
    st.markdown('<h2 class="section-header">Analysis History</h2>', unsafe_allow_html=True)

    if not st.session_state.analysis_history:
        st.info("No analysis history yet. Analyze some samples!")
    else:
        st.markdown(f"Displaying last **{len(st.session_state.analysis_history)}** analyses (max {st.session_state.history_limit}).")
        st.markdown("---")

        # Display history items
        for i, item in enumerate(st.session_state.analysis_history):
            ts = item['timestamp']
            selected_g = item['selected_grain']
            analysis = item['analysis']
            thumb_str = item['image_thumbnail']

            # Determine display details based on analysis content
            display_title = f"Analysis for {selected_g}"
            grade_text = "N/A"
            score_text = ""
            is_error = 'error' in analysis
            is_mismatch = is_error and analysis.get('error') == "Grain Type Mismatch"
            detected_grain_in_analysis = None # For display

            if is_mismatch:
                 display_title = f"Mismatch: Selected {selected_g}"
                 # Get data from nested dict if available
                 nested_analysis = analysis.get("analysis_data_for_detected_grain", {})
                 detected_grain_in_analysis = nested_analysis.get('grain_identity', {}).get('detected_grain', 'Unknown')
                 grade_info = nested_analysis.get('overall_grade', {})
                 grade_text = grade_info.get('grade', 'N/A')
                 score_val = grade_info.get('score')
                 score_text = f"({score_val}%)" if isinstance(score_val, (int, float)) else ""
                 display_title += f" (Detected {detected_grain_in_analysis})"
            elif is_error:
                 display_title = f"Failed Analysis ({selected_g})"
                 grade_text = f"Error: {analysis.get('error', 'Failed')}"
            else: # Successful analysis
                 detected_grain_in_analysis = analysis.get('grain_identity', {}).get('detected_grain', selected_g) # Use detected, fallback to selected
                 grade_info = analysis.get('overall_grade', {})
                 grade_text = grade_info.get('grade', 'N/A')
                 score_val = grade_info.get('score')
                 score_text = f"({score_val}%)" if isinstance(score_val, (int, float)) else ""
                 display_title = f"Analyzed: {detected_grain_in_analysis}" # Show what was actually identified


            # Layout for history item
            hist_cols = st.columns([1, 3, 1]) # Thumbnail, Info, Button
            with hist_cols[0]:
                if thumb_str:
                    st.image(f"data:image/jpeg;base64,{thumb_str}", width=80)
                else:
                    st.caption("No thumb")

            with hist_cols[1]:
                 grade_color_class = f"quality-{get_color_from_grade(grade_text).lower()}" if not is_error else "quality-poor"
                 st.markdown(f"""
                 <div class='metric-card' style='margin-bottom: 0.5rem; padding: 0.8rem;'>
                     <h5 style='margin-bottom: 0.2rem; color: #333;'>{display_title}</h5>
                     <p style='font-size: 0.9rem; margin-bottom: 0.1rem;'>
                         Result: <span class='{grade_color_class}'>{grade_text} {score_text}</span>
                     </p>
                     <p style='font-size: 0.8rem; color: #666; margin-bottom: 0;'>Analyzed: {ts}</p>
                 </div>
                 """, unsafe_allow_html=True)


            with hist_cols[2]:
                if st.button("View Details", key=f"view_{i}", use_container_width=True):
                    # Load this analysis into the main view
                    st.session_state.current_analysis = item['analysis']
                    st.session_state.selected_grain = item['selected_grain'] # Set context for display
                    st.session_state.last_analysis_grain = detected_grain_in_analysis or item['selected_grain'] # Store what was analyzed
                    # Switch to Analysis tab - Streamlit doesn't directly support switching tabs via code,
                    # but we can use experimental_rerun and potentially manage active tab state if needed.
                    # For now, just load the data. User needs to click the tab.
                    st.info(f"Loaded analysis from {ts}. View details in the 'Analysis' tab.")
                    st.rerun() # Rerun to reflect the loaded state if user navigates back

            st.markdown("---", unsafe_allow_html=True) # Divider between items


        # Clear History Button
        st.markdown("---")
        if st.button("Clear Analysis History", use_container_width=True):
            st.session_state.analysis_history = []
            st.success("History cleared.")
            st.rerun()


# Tab 3: Settings
with tab3:
    st.markdown('<h2 class="section-header">Application Settings</h2>', unsafe_allow_html=True)

    st.markdown('<h3 class="section-header">History Settings</h3>', unsafe_allow_html=True)
    new_limit = st.slider(
        "Max History Items:",
        min_value=5,
        max_value=50,
        value=st.session_state.history_limit,
        key="history_limit_slider"
    )
    if new_limit != st.session_state.history_limit:
         st.session_state.history_limit = new_limit
         # Trim history if needed
         st.session_state.analysis_history = st.session_state.analysis_history[:new_limit]
         st.success(f"History limit updated to {new_limit}.")
         st.rerun()


    st.markdown('<h3 class="section-header">About GrainSight AI</h3>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="metric-card">
        <h4>Application Information</h4>
        <p><strong>Version:</strong> 1.1.0</p>
        <p><strong>Function:</strong> Visual Grain Quality Analysis</p>
        <p>Utilizes advanced AI for image assessment.</p>
        <p>{FOOTER_TEXT}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<h3 class="section-header">Reset</h3>', unsafe_allow_html=True)
    if st.button("⚠️ Reset Application State", use_container_width=True):
        # Keep API key if loaded from env
        api_key_backup = os.environ.get("GOOGLE_API_KEY")

        # Clear all session state keys
        keys_to_clear = list(st.session_state.keys())
        for key in keys_to_clear:
            del st.session_state[key]

        # Re-initialize necessary defaults
        st.session_state.history_limit = HISTORY_LIMIT
        # Optionally reload API key if it was cleared
        if api_key_backup: os.environ["GOOGLE_API_KEY"] = api_key_backup

        st.success("Application state has been reset.")
        st.rerun()


# Footer
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; margin-top: 1rem; padding: 1rem; border-top: 1px solid #eee; color: #777; font-size: 0.9rem;">
    {FOOTER_TEXT} | AI analysis engine may have limitations. Verify critical results.
</div>
""", unsafe_allow_html=True)

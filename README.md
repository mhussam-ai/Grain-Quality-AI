# GrainSight AI 🔬

**GrainSight AI** is a web application built with Streamlit for performing visual grain quality analysis using Google's Gemini AI model. Users can upload an image or take a photo of a grain sample (Rice, Wheat, Barley, Corn, Oats, Sorghum), and the application provides a detailed analysis including grain identification, quality assessment, defect detection, overall grading, and usage recommendations.

---

## Features

*   **Multiple Grain Types:** Supports analysis for Rice, Wheat, Barley, Corn, Oats, and Sorghum.
*   **Flexible Input:** Upload grain images (JPG, JPEG, PNG) or capture photos directly using the device camera.
*   **AI-Powered Analysis:** Leverages the Google Gemini model (`gemini-2.0-flash`) for detailed visual assessment.
*   **Structured Results:** Presents analysis in a clear, structured format including:
    *   Grain Identity (Detected type, variety, characteristics)
    *   Quality Metrics (Integrity, Uniformity, Maturity, Foreign Matter, Storage Soundness) with visual progress circles.
    *   Defect Detection (Discoloration, Damage, Disease/Mold, Sprouting, Specific Defects)
    *   Overall Grade & Score (Excellent, Good, Fair, Poor)
    *   Usage Recommendations & Storage Tips
*   **Visual Feedback:** Uses custom CSS for an enhanced user interface, including color-coded quality indicators and metric cards.
*   **Analysis History:** Stores recent analyses (configurable limit) with thumbnails for easy review and comparison.
*   **Settings:** Allows users to adjust the history limit and reset the application state.
*   **Error Handling:** Includes checks for API key presence, handles AI API errors, content filtering blocks, and potential grain type mismatches between user selection and AI detection.

---

## How it Works

1.  **Select Grain Type:** Choose the expected type of grain from the dropdown menu.
2.  **Provide Image:** Either upload an image file or use the camera option to take a photo of the grain sample.
3.  **Analyze:** Click the "Analyze [Grain Name] Sample" button.
4.  **View Results:** The application sends the image and selected grain type to the Gemini AI model. The AI analyzes the image based on a specific prompt and returns a structured JSON response. This response is then parsed and displayed visually in the "Analysis" tab.
5.  **Review History:** Past analyses are stored and can be viewed in the "History" tab.

---

## Technology Stack

*   **Frontend:** Streamlit
*   **AI Model:** Google Gemini (`gemini-2.0-flash` via `google-generativeai` SDK)
*   **Image Processing:** Pillow (PIL)
*   **Environment Variables:** `python-dotenv`
*   **Language:** Python 3

---

## Setup and Installation

1.  **Prerequisites:**
    *   Python 3.8 or higher
    *   Git (optional, for cloning)
    *   Access to Google AI Studio or Google Cloud Platform to obtain a Gemini API key.

2.  **Clone the Repository:**
    ```bash
    git clone <https://github.com/mhussam-ai/Grain-Quality-AI>
    cd <Grain-Quality-AI>
    ```

3.  **Create a Virtual Environment (Recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

4.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Set up API Key:**
    *   Obtain your API key from [Google AI Studio](https://aistudio.google.com/app/apikey) or your Google Cloud project.
    *   Create a file named `.env` in the root project directory.
    *   Add your API key to the `.env` file like this:
        ```
        GOOGLE_API_KEY="YOUR_API_KEY_HERE"
        ```
    *   Replace `"YOUR_API_KEY_HERE"` with your actual Gemini API key. **Do not commit the `.env` file to version control if your project is public.**

---

## Running the Application

1.  Make sure your virtual environment is activated.
2.  Navigate to the project directory in your terminal.
3.  Run the Streamlit application (assuming your script is named `app.py`):
    ```bash
    streamlit run app.py
    ```
4.  The application should automatically open in your web browser.

---

## Configuration

*   **API Key:** Must be set via the `GOOGLE_API_KEY` environment variable (loaded from the `.env` file).
*   **Gemini Model:** The specific model used is defined by the `GEMINI_MODEL` constant in the script (currently `gemini-2.0-flash`).
*   **History Limit:** The maximum number of history items is set by `HISTORY_LIMIT` constant and can be adjusted in the "Settings" tab of the running application.
*   **Supported Grains:** The list of supported grains is defined in the `GRAIN_OPTIONS` list.
*   **Supported Image Types:** Defined in `SUPPORTED_IMAGE_TYPES`.

---

## Code Overview

*   **`app.py` (Main Script):** Contains the Streamlit UI layout, state management, helper functions, and logic flow.
*   **Branding & Configuration:** Constants at the top define app title, icons, model names, etc.
*   **Custom CSS:** Injected using `st.markdown` for custom styling of elements.
*   **Session State:** Used extensively (`st.session_state`) to manage the current image, analysis results, history, selected grain, and UI flags across reruns.
*   **Helper Functions:**
    *   `get_color_from_score`, `get_color_from_grade`: Determine CSS classes for quality levels.
    *   `render_progress_circle`: Generates HTML/CSS for the circular progress indicators.
    *   `generate_prompt`: Creates the detailed JSON-structured prompt for the Gemini API.
    *   `process_image`: Handles interaction with the Gemini API, including sending the image/prompt and parsing the response (JSON extraction and error handling).
    *   `save_to_history`: Adds analysis results and image thumbnails to the session history.
    *   `render_analysis_results`: Displays the parsed analysis results in a user-friendly format.
*   **UI Tabs:** The application is organized into "Analysis", "History", and "Settings" tabs using `st.tabs`.

---

## Known Limitations & Disclaimers

*   **Visual Analysis Only:** The analysis is based solely on the visual information present in the image. It cannot detect internal defects, moisture content, chemical composition, or other non-visual properties.
*   **AI Model Limitations:** The accuracy and detail of the analysis depend on the capabilities of the underlying Gemini AI model. The model might misidentify grains, hallucinate details, or provide inaccurate assessments, especially with poor-quality images or unusual samples.
*   **Image Quality Dependency:** Analysis results are highly dependent on the quality of the input image (lighting, focus, background, grain spread). Follow the "Tips for Best Results" in the sidebar for optimal performance.
*   **Not a Substitute for Lab Testing:** This tool is intended for preliminary visual assessment and should not replace professional laboratory testing for critical quality control or grading purposes.
*   **Content Filtering:** The AI service includes safety filters. Analysis might be blocked if the image content triggers these filters.

---

*(Optional Sections)*

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs, feature requests, or improvements.

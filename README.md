# Automated Code Review Workflow with LangGraph and Groq
<img width="1213" alt="image" src="https://github.com/user-attachments/assets/02448e15-b046-438e-b8d3-bd90c6bbabd2" />


## Overview
This solution provides an automated code review system using LangGraph for workflow management and Groq's LLM for code analysis. The application features a Streamlit interface for easy interaction and presents reviews in a three-column layout.

## Architecture

### Core Components
1. **LangGraph Workflow Engine**
   - Manages the sequential flow of code review steps
   - Handles state management between steps
   - Provides traceability through LangSmith

2. **Groq LLM Integration**
   - Uses llama-3.3-70b-versatile model
   - Configured with max_tokens=2000 and temperature=0.0 for consistent output
   - Processes code analysis through chain operations

3. **Streamlit Interface**
   - Provides a user-friendly web interface
   - Features side-by-side display of review components
   - Implements light mode theme with DaisyUI styling

## Workflow Steps

### 1. Code Review (`@traceable(name="review_code")`)
- **Input**: Raw code from user
- **Process**: 
  - Analyzes code for:
    - Code quality
    - Potential bugs
    - Security issues
    - Performance concerns
    - Best practices
- **Output**: Detailed review comments

### 2. Severity Assessment (`@traceable(name="assess_severity")`)
- **Input**: Review comments from step 1
- **Process**: Categorizes issues into severity levels:
  - Critical: Must be fixed immediately
  - High: Should be fixed before merge
  - Medium: Should be addressed soon
  - Low: Nice to have improvements
- **Output**: Severity assessment for each issue

### 3. Summary Creation (`@traceable(name="create_summary")`)
- **Input**: Review comments and severity levels
- **Process**: Generates a comprehensive summary including:
  - Overall code quality
  - Key issues to address
  - Positive aspects
  - Next steps
- **Output**: Concise summary limited to 500 words

## State Management
- Uses `CodeReviewState` TypedDict for maintaining state
- Tracks:
  - Original code
  - Review comments
  - Severity levels
  - Final summary
  - Current step

## Monitoring and Debugging
- **LangSmith Integration**
  - Traces all LLM operations
  - Provides debugging capabilities
  - Tracks performance metrics
  - Project-specific tracking with unique IDs

## User Interface
- **Input Section**
  - Code input textarea
  - Review trigger button

- **Results Display**
  - Three equal columns showing:
    1. Review Comments
    2. Severity Assessment
    3. Final Summary
  - Each section features:
    - Scrollable content
    - Consistent styling
    - Clear headers
    - Fixed height for uniformity

## Setup and Configuration

### Environment Variables Required
- `LANGSMITH_API_KEY`: API key for LangSmith
- `GROQ_API_KEY`: API key for Groq

### Installation
1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Create a `.env` file in the root directory with the following variables:
```bash
LANGSMITH_API_KEY=your_langsmith_api_key
GROQ_API_KEY=your_groq_api_key
```
4. Run the Streamlit app:
```bash
streamlit run streamlit_app.py
```

## Contributing
Contributions are welcome! Please open an issue or submit a pull request.

## License
This project is licensed under the MIT License. See the LICENSE file for details.



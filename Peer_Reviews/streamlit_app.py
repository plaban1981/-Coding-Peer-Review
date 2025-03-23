import streamlit as st
from code_review_app import create_workflow, CodeReviewState
import streamlit.components.v1 as components
from typing import Dict
import json

# Configure Streamlit page
st.set_page_config(
    page_title="Code Review Assistant",
    page_icon="🔍",
    layout="wide"
)

# Custom CSS with DaisyUI light theme
def inject_custom_css():
    st.markdown("""
        <link href="https://cdn.jsdelivr.net/npm/daisyui@3.9.4/dist/full.css" rel="stylesheet" type="text/css" />
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            /* Light theme styles */
            :root {
                --primary-color: #570DF8;
                --background-color: #F2F2F2;
                --text-color: #1F2937;
                --card-bg: #FFFFFF;
            }
            
            .stApp {
                background-color: var(--background-color);
                color: var(--text-color);
            }
            
            .stTextInput > div > div > input {
                background-color: var(--card-bg);
                color: var(--text-color);
                border: 1px solid #E5E7EB;
            }
            
            .stTextArea > div > div > textarea {
                background-color: var(--card-bg);
                color: var(--text-color);
                border: 1px solid #E5E7EB;
            }
            
            .review-card {
                background-color: var(--card-bg);
                border: 1px solid #E5E7EB;
                border-radius: 8px;
                padding: 1rem;
                margin: 1rem 0;
                box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            }
            
            .severity-badge {
                padding: 0.25rem 0.5rem;
                border-radius: 4px;
                margin-right: 0.5rem;
                font-weight: 500;
            }
            
            .critical { background-color: #DC2626; color: white; }
            .high { background-color: #F87171; color: white; }
            .medium { background-color: #F59E0B; color: white; }
            .low { background-color: #10B981; color: white; }

            /* Tab styling */
            .stTabs [data-baseweb="tab-list"] {
                gap: 2px;
                background-color: var(--card-bg);
                border-radius: 8px;
                padding: 0.5rem;
            }

            .stTabs [data-baseweb="tab"] {
                height: 40px;
                background-color: transparent;
                border: 1px solid #E5E7EB;
                border-radius: 4px;
                color: var(--text-color);
                font-weight: 500;
            }

            .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
                background-color: var(--primary-color);
                color: white;
                border-color: var(--primary-color);
            }

            /* Button styling */
            .stButton > button {
                background-color: var(--primary-color);
                color: white;
                border: none;
                border-radius: 4px;
                padding: 0.5rem 1rem;
                font-weight: 500;
            }

            .stButton > button:hover {
                background-color: #4506CB;
            }

            /* Expander styling */
            .streamlit-expanderHeader {
                background-color: var(--card-bg);
                border: 1px solid #E5E7EB;
                border-radius: 4px;
            }

            .streamlit-expanderContent {
                background-color: var(--card-bg);
                border: 1px solid #E5E7EB;
                border-radius: 0 0 4px 4px;
            }

            /* Code block styling */
            .stCodeBlock {
                background-color: #F8F9FA;
                border: 1px solid #E5E7EB;
                border-radius: 4px;
            }

            .review-section {
                background-color: var(--card-bg);
                border: 1px solid #E5E7EB;
                border-radius: 8px;
                padding: 1rem;
                height: 500px;
                overflow-y: auto;
                box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            }
            
            .section-title {
                font-size: 1.2rem;
                font-weight: 600;
                margin-bottom: 1rem;
                padding-bottom: 0.5rem;
                border-bottom: 2px solid var(--primary-color);
            }
        </style>
    """, unsafe_allow_html=True)

def create_review_card(title: str, content: str, severity: str = None):
    severity_class = severity.lower() if severity else ""
    return f"""
    <div class="review-card">
        <div class="flex items-center mb-2">
            <h3 class="text-lg font-semibold">{title}</h3>
            {f'<span class="severity-badge {severity_class}">{severity}</span>' if severity else ''}
        </div>
        <p class="text-sm">{content}</p>
    </div>
    """

def main():
    inject_custom_css()
    
    st.title("🔍 Code Review Assistant")
    
    # Initialize workflow
    workflow = create_workflow()
    
    # Code input section
    st.header("📝 Submit Code for Review")
    code_input = st.text_area(
        "Enter your code here:",
        height=200,
        placeholder="Paste your code here..."
    )
    
    if st.button("Start Review", type="primary"):
        if code_input:
            with st.spinner("Analyzing code..."):
                # Initialize state
                initial_state = CodeReviewState(
                    code=code_input,
                    review_comments=[],
                    severity_levels=[],
                    final_summary="",
                    current_step="start"
                )
                
                # Run workflow
                try:
                    result = workflow.invoke(initial_state)
                    
                    # Create three columns for side-by-side display
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.markdown('<div class="review-section">'
                                  '<div class="section-title">📋 Review Comments</div>'
                                  f'{result["review_comments"]}</div>', 
                                  unsafe_allow_html=True)
                    
                    with col2:
                        st.markdown('<div class="review-section">'
                                  '<div class="section-title">🎯 Severity Assessment</div>'
                                  f'{result["severity_levels"]}</div>', 
                                  unsafe_allow_html=True)
                    
                    with col3:
                        st.markdown('<div class="review-section">'
                                  '<div class="section-title">📊 Final Summary</div>'
                                  f'{result["final_summary"]}</div>', 
                                  unsafe_allow_html=True)
                    
                    # Save review history in session state
                    if 'review_history' not in st.session_state:
                        st.session_state.review_history = []
                    
                    st.session_state.review_history.append({
                        'code': code_input,
                        'results': result
                    })
                    
                except Exception as e:
                    st.error(f"An error occurred during the review: {str(e)}")
        else:
            st.warning("Please enter some code to review.")
    
    # Review history section
    # if 'review_history' in st.session_state and st.session_state.review_history:
    #     st.header("📜 Review History")
    #     for i, review in enumerate(reversed(st.session_state.review_history)):
    #         with st.expander(f"Review #{len(st.session_state.review_history) - i}"):
    #             st.code(review['code'], language='python')
    #             st.markdown("#### Results")
    #             st.markdown(review['results']['final_summary'])

if __name__ == "__main__":
    main() 
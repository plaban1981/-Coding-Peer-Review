from typing import TypedDict, Annotated, Sequence,Any
from langgraph.graph import Graph, StateGraph
#from langgraph.prebuilt.tools import ToolExecutor
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.tools import Tool
from uuid import uuid4
import os
from langsmith import Client
from langsmith.run_helpers import traceable
from pydantic import BaseModel, Field
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()



# Initialize LangSmith
unique_id = uuid4().hex[0:8]
os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_PROJECT"] = f"Code_Review - {unique_id}"
os.environ["LANGSMITH_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGSMITH_API_KEY")
client = Client()

# Initialize Groq
llm = ChatGroq(model_name="llama-3.3-70b-versatile",max_tokens=2000,temperature=0.0)

class CodeReviewState(TypedDict):
    code: str
    review_comments: Any
    severity_levels: Any
    final_summary: Any
    current_step: Any

@traceable(name="review_code")
def review_code(state:CodeReviewState):
    # Initial code analysis prompt
    print(f"code:{state['code']}")
    code = state["code"]
    code_review_prompt = ChatPromptTemplate.from_messages([
        SystemMessage(content="""You are an expert code reviewer. Analyze the code for:
        1. Code quality
        2. Potential bugs
        3. Security issues
        4. Performance concerns
        5. Best practices
        Provide specific, actionable feedback based on the above points.Do not provide any other extra information or reasoning."""),
        HumanMessage(content=code )
    ])
    review_chain = code_review_prompt | llm | StrOutputParser()
    review_comments = review_chain.invoke({"code": code})

    state["review_comments"] = review_comments
    return {"review_comments":review_comments}

@traceable(name="assess_severity")
def assess_severity(state:CodeReviewState):
    print(f"REVIEW COMMENT :{state}")
    # Severity assessment prompt
    comments = state['review_comments']
    severity_prompt = ChatPromptTemplate.from_messages([
        SystemMessage(content="""Assess the severity of each issue found in the code review:
        - Critical: Must be fixed immediately
        - High: Should be fixed before merge
        - Medium: Should be addressed soon
        - Low: Nice to have improvements"""),
        HumanMessage(content=comments)
    ])
    asssesment_chain = severity_prompt | llm | StrOutputParser()
    severity_levels = asssesment_chain.invoke({"review_comments": state["review_comments"]})
    #state["severity_levels"] = severity_levels.content
    return {"severity_levels":severity_levels}

@traceable(name="create_summary")
def create_summary(state:CodeReviewState):
    # Final summary prompt
    
    review = state["review_comments"]
    severity = state["severity_levels"]
    print(f"review:{review}")
    print(f"severity:{severity}")
    summary_prompt = ChatPromptTemplate.from_messages([
        SystemMessage(content="""Create a concise ,clear and meaningful summary of the code review including:
        1. Overall code quality
        2. Key issues to address
        3. Positive aspects
        4. Next steps
        Stick to the above points and do not provide any other extra information or reasoning.Be more technical when providing the summary"""),
        HumanMessage(content="Review: {review}\nSeverity: {severity}.Please provide the summary in no more than 500 words.")
    ])
    summary_chain = summary_prompt | llm | StrOutputParser()
    final_summary = summary_chain.invoke({
        "review": review,
        "severity": severity
    })
    return {"final_summary": final_summary}

def create_workflow():
    workflow = StateGraph(CodeReviewState)

    # Add nodes to the workflow
    workflow.add_node("review_code", review_code)
    workflow.add_node("assess_severity", assess_severity)
    workflow.add_node("create_summary", create_summary)

    # Define the edges
    workflow.set_entry_point("review_code")
    workflow.add_edge("review_code", "assess_severity")
    workflow.add_edge("assess_severity", "create_summary")

    # Compile the workflow
    app = workflow.compile()
    return app



if __name__ == "__main__":
    # Example usage
    code_to_review = """
    def calculate_total(items):
        total = 0
        for item in items:
            total += item.price
        return total
    """

    initial_state = {
        "code": code_to_review,
        "review_comments": [],
        "severity_levels": [],
        "final_summary": "",
        "current_step": "start"
    }

    app = create_workflow()
    result = app.invoke(initial_state)
    print("Final Review Summary:", result["final_summary"]) 
    print("Final Review Summary:", result["final_summary"]) 
    print("Final Review Summary:", result["final_summary"]) 
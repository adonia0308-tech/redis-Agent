from datetime import datetime
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_groq import ChatGroq
from langchain.agents import create_agent
load_dotenv()
students={
    "101": {
        "name": "Arun",
        "department": "CSE",
        "attendance": 82
    },
    "102": {
        "name": "Priya",
        "department": "AI",
        "attendance": 91
    },
}
@tool
def calculate(expression: str)->str:
    """Calculate a mathematical expression, e.g.'12 *(4+1)',"""
    try:
        return str(eval(expression,{"__builtins__": {}}))
    except Exception as e:
        return f"Error: {e}"
@tool
def get_student_info(student_name: str) -> str:
    """Get a student's name and department."""

    for student in students.values():
        if student["name"].lower() == student_name.lower():
            return f"{student['name']} is from {student['department']}."

    return f"{student_name} was not found in the student database."
@tool
def get_attendance(student_name: str) -> str:
    """Get a student's attendance percentage."""

    for student in students.values():
        if student["name"].lower() == student_name.lower():
            return f"{student['name']}'s attendance is {student['attendance']}%."

    return f"{student_name} was not found in the student database."
tools=[calculate,get_student_info,get_attendance]
llm=ChatGroq(model="openai/gpt-oss-20b")
agent_executor=create_agent(
    llm,tools,system_prompt="You are helpfull Assistant that uses tools when needed,"
)
def student_agent(user_message, history):
    history.append(("user", user_message))

    response = agent_executor.invoke({
        "messages": history
    })

    history = response["messages"]

    return response["messages"][-1].content, history
if __name__=="__main__":
    history=[]
    while True:
        user_input=input("User:")
        if user_input.lower() in ("exit","quit","q"):
            print("bye")
            break
        reply, history=student_agent(user_input,history)
        print("Agent:",reply)
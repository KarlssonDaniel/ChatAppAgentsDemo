import time

from langchain_community.tools import DuckDuckGoSearchResults
from langchain_community.chat_models import ChatOllama

from typing_extensions import TypedDict

from langgraph.graph import StateGraph

from langchain_core.prompts import PromptTemplate

llm = ChatOllama(model = "llama3", base_url="http://ollama:11434")

class State(TypedDict):
    question: str
    enhancedQuestions: list[str]
    webSearch: str
    generation: str
    nPoints: int
    nQuestions: int
    graded: str
    iter: int
    maxIters: int

# Summarizer node
prompt = """You are an expert in creating search queries for web searching. Create {nQuestions} questions to retrieve information regarding the following question {question}.
Reply in the same anguage as the original question. Reply only with the generated questions separated by line breaks and no preamble."""

promptTemplate = PromptTemplate.from_template(prompt)

questionEnhancer = promptTemplate | llm

def enhance(state: State):
    print("-----------Enhancing question-----------")
    questions = questionEnhancer.invoke({"nQuestions": str(state["nQuestions"]), "question": state["question"]}).content
    questions = [x for x in questions.split("\n") if x !=""]
    return {"enhancedQuestions": questions, "iter": state["iter"] + 1} 

# search node
webSearch = DuckDuckGoSearchResults(max_results=2,)

def getInfo(state: State):
    print("-----------Searching-----------")
    questions = [state["question"]] + state["enhancedQuestions"]
    result = ""
    for question in questions:
        result += question + ":\n\n" + webSearch.invoke(input=question)
        time.sleep(0.5)
    return {"webSearch": result}

# Summarizer node
prompt = """You are an expert in summarizing text. Summarize the following text in {nPoints} bulletpoints,

{text}.

Reply in the same language as the text.
Reply only with the {nPoints} bullets and no preamble."""

promptTemplate = PromptTemplate.from_template(prompt)

summarizer = promptTemplate | llm

def summarize(state: State):
    print("-----------Summarizing-----------")
    result = summarizer.invoke({"nPoints": str(state["nPoints"]), "text": state["webSearch"]}).content
    return {"generation": result}

prompt = """You are an expert grader. Determine if the following bulletpoints,

{bullets}

answers the following question {question}.

Reply only "Sufficient" if the bulletpoints answer the question and "insufficient" if the question is not answered. Do not give any preamble."""

promptTemplate = PromptTemplate.from_template(prompt)

grader = promptTemplate | llm

def grade(state: State):
    print("-----------Grading answer-----------")
    result = grader.invoke({"bullets": str(state["generation"]), "question": state["question"]}).content
    return {"graded": result}

def gradeRouter(state: State):
    grade = state["graded"]
    print("-------------Routing---------------")
    if grade == "Sufficient" or state["iter"] >= state["maxIters"]:
        return "__end__"
    else:
        return "enhancer"
    
def getWebSearchGraph():
    graphBuilder = StateGraph(State)

    graphBuilder.add_node("generator", summarize)
    graphBuilder.add_node("search", getInfo)
    graphBuilder.add_node("grader", grade)
    graphBuilder.add_node("enhancer", enhance)

    graphBuilder.add_edge("enhancer", "search")
    graphBuilder.add_edge("search", "generator")
    graphBuilder.add_edge("generator","grader")

    graphBuilder.add_conditional_edges("grader", gradeRouter,
                                    {"__end__": "__end__", "enhancer": "enhancer"})

    graphBuilder.set_entry_point("enhancer")
    return graphBuilder.compile()

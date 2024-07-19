import panel as pn
import pandas as pd
import functools

from langchain_community.llms import Ollama
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain_core.prompts import PromptTemplate

def getPrompt():
    return """You are a helpful assistant named Sara. 
    
    You answer questions succinctly and if you do not know the answer to a
    question you communicate that \n\nCurrent conversation:
    \n{history}\nHuman: {input}\nAI:"""

def commonChatConversation():
    """Instantiate conversation with LLM, memory and prompt."""
    llm = Ollama(
        base_url='http://ollama:11434',
        model="llama3")

    commonChatMemory = ConversationBufferMemory()

    commonChatPrompt = getPrompt()
    commonChatPromptTemplate = PromptTemplate.from_template(commonChatPrompt)

    return ConversationChain(llm=llm,
                             verbose=True,
                             memory=commonChatMemory,
                             prompt = commonChatPromptTemplate)

MAXROWS = 20

def responseCallback(inputMessage: str, input_user: str,
                     instance: pn.chat.ChatInterface,
                     conversation):
    # if .csv file is imported extract only MAXROWS
    if type(inputMessage) == pd.core.frame.DataFrame:
        if len(inputMessage) > MAXROWS:
            inputMessage = inputMessage.iloc[:MAXROWS,:]

        header = inputMessage.columns.values.tolist()
        data = inputMessage.values.tolist()
        data.insert(0, header)
        inputMessage = str(data)

    # Currently yielding complete answer without streaming
    response_message = conversation.predict(input = inputMessage)
    yield  response_message

# Prepare chat callback to have the conversation already set.
commonChatCallback = functools.partial(responseCallback,
                                conversation=commonChatConversation())
    
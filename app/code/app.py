import panel as pn
import hvplot.pandas
import pandas as pd
import functools as ft

from langchain_community.llms import Ollama
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain_core.prompts import PromptTemplate

import common_chat.common_chat as commonChat


# llm
llm = Ollama(
    base_url='http://ollama:11434',
    model="llama3",
)

# Common chat conversation
commonChatMemory = ConversationBufferMemory()

commonChatPrompt = commonChat.getPrompt()
commonChatPromptTemplate = PromptTemplate.from_template(commonChatPrompt)

commonChatConversation = ConversationChain(llm=llm,
                                 verbose=True,
                                 memory=commonChatMemory,
                                 prompt = commonChatPromptTemplate)



# Dashboard
template = pn.template.BootstrapTemplate(title="Chat App")

commonChatCallback = ft.partial(commonChat.responseCallback,
                                conversation=commonChatConversation)
commonChatTab = commonChat.regularChat(commonChatCallback)

pythonAgentTab = pn.Row(pn.pane.Markdown("# TBD"))

ragAppTab = pn.Row(pn.pane.Markdown("# TBD"))

settingsTab = pn.Row(pn.pane.Markdown("# TBD"))

tabs = pn.Tabs(("Common chat", commonChatTab), 
               ("Python agent", pythonAgentTab), 
               ("Rag chat", ragAppTab),
               ("Settings", settingsTab))

template.main.append(tabs)

template.servable()
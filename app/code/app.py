import panel as pn

from common_chat import commonChatTab
from web_search import webSearchTab

template = pn.template.BootstrapTemplate(title="Chat Apps")

commonChatTab = commonChatTab.regularChat()

webSearchTab = webSearchTab.webSearch()

pythonAgentTab = pn.Row(pn.pane.Markdown("# TBD"))

ragAppTab = pn.Row(pn.pane.Markdown("# TBD"))

settingsTab = pn.Row(pn.pane.Markdown("# TBD"))

tabs = pn.Tabs(("Common chat", commonChatTab), 
               ("Web search Summary", webSearchTab),
               ("Python agent", pythonAgentTab), 
               ("Rag chat", ragAppTab),
               ("Settings", settingsTab))

template.main.append(tabs)

template.servable()
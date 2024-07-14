import panel as pn
import pandas as pd

MAXROWS = 50

def responseCallback(inputMessage: str, input_user: str,
                     instance: pn.chat.ChatInterface, conversation):
    # choose your favorite LLM API to respond to the input_message
    if type(inputMessage) == pd.core.frame.DataFrame:
        if len(inputMessage) > MAXROWS:
            inputMessage = inputMessage.iloc[:MAXROWS,:]

        header = inputMessage.columns.values.tolist()
        data = inputMessage.values.tolist()
        data.insert(0, header)
        inputMessage = str(data)

    response_message = conversation.predict(input = inputMessage)
   # callback_handler = pn.chat.langchain.PanelCallbackHandler(instance)
   # response_message = llm.predict(inputMessage)
    yield  response_message

def regularChat(response_callback=responseCallback):
    widgets=[pn.chat.ChatAreaInput(name="Chat", rows=5, cols=3),
             pn.widgets.FileInput(name="Upload file", accept=".csv")]
    return pn.Row(pn.chat.ChatInterface(widgets=widgets,
                                        show_button_name=False,
                                        callback=response_callback, 
                                        callback_exception='verbose', 
                                        sizing_mode='stretch_height'))


def getPrompt():
    return """You are a helpful assistant named Sara. 
    
    You answer questions succinctly and if you do not know the answer to a
    question you communicate that \n\nCurrent conversation:
    \n{history}\nHuman: {input}\nAI:"""
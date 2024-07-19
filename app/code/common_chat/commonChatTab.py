import panel as pn

from common_chat import commonChatLlm

def regularChat():
    """Chat interface using panel built in UI.
    
    The interface accepts uploading of .csv files."""
    callback = commonChatLlm.commonChatCallback
    widgets=[pn.chat.ChatAreaInput(name="Chat", rows=5, cols=3),
             pn.widgets.FileInput(name="Upload file", accept=".csv")]
    return pn.Row(pn.chat.ChatInterface(widgets=widgets,
                                        show_button_name=False,
                                        callback=callback, 
                                        callback_exception='verbose', 
                                        sizing_mode='stretch_height'))




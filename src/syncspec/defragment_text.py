from syncspec.context import Context
from syncspec.text import Text

def make_defragment_text(context: Context):
    state = {'path': None, 'text': "", 'last': False}

    def defragment_text(text: Text) -> Text:
        if state['path'] is not None and text.path != state['path']:
            state['path'].write_text(state['text'])
            state['path'] = text.path
            state['text'] = text.text
        elif state['path'] is None:
            state['path'] = text.path
            state['text'] = text.text
        else:
            state['text'] += text.text

        if state['last']:
            state['path'].write_text(state['text'])
            state['text'] = ""


        return text

    return defragment_text
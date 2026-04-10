from syncspec.context import Context
from syncspec.fragment import Fragment
from syncspec.indexedfragment import IndexedFragment

def make_index_fragments(context: Context):
    state = {'index': 0, 'path': None}
    def index_fragments(fragment: Fragment) -> IndexedFragment:
        if state["path"] != fragment.path:
            state["index"] = 0
            state["path"] = fragment.path

        indexed = IndexedFragment(
            path=fragment.path,
            text=fragment.text,
            line_number=fragment.line_number,
            index=state["index"]
        )
        state["index"] += 1
        return indexed
    return index_fragments
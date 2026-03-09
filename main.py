from src.syncspec.validate_text_context import ValidateTextContext
from src.syncspec.fragment_text_context import FragmentTextContext
from src.syncspec.create_blocks_context import CreateBlocksContext
from src.syncspec.text import Text
from src.syncspec.stop import Stop
from src.syncspec.validate_text import make_validate_text
from src.syncspec.fragment_text import make_fragment_text
from src.syncspec.create_blocks import make_create_blocks
from src.syncspec.production import build_rules, production
import pprint


def main():
    vtc = ValidateTextContext(
        name="test",
        open_delimiter="{{",
        close_delimiter="}}",
        line_number=1
    )
    ftc = FragmentTextContext(
        name="test",
        open_delimiter="{{",
        close_delimiter="}}",
        line_number=1
    )
    cbc = CreateBlocksContext(
        index=0,
        top_directive="",
        text="",
        line_number=1
    )


    # 2. Create Unary Function bound to context
    validate_text = make_validate_text(vtc)
    fragment_text = make_fragment_text(ftc)
    create_blocks = make_create_blocks(cbc)

    facts = [Text("""A{{B}}C{{D}}E{{F}}G{{H}}I""")]

    # 3. Build Rules
    rules = build_rules([validate_text,fragment_text,create_blocks])

    # 4. Run Production (no context passed)
    result = production(facts, rules, Stop)
    pprint.pp(result)


if __name__ == "__main__":
    main()
from syncspec.context import Context
from syncspec.production import production, build_rules
from syncspec.dummy import Dummy

from syncspec.validate_context import make_validate_context
from syncspec.traverse_path import make_traverse_path
from syncspec.fragment_text import make_fragment_text
from syncspec.index_fragments import make_index_fragments
from syncspec.create_blocks import make_create_blocks
from syncspec.create_directives import make_create_directives
from syncspec.export_directive import make_export_directive
from syncspec.import_directive import make_import_directive
from syncspec.source_directive import make_source_directive
from syncspec.include_directive import make_include_directive
from syncspec.reassemble_text import make_reassemble_text
from syncspec.defragment_text import make_defragment_text
from syncspec.write_keyfile import make_write_keyfile


def machine(context: Context) -> None:

    validate_context = make_validate_context(context)
    traverse_path = make_traverse_path(context)
    fragment_text = make_fragment_text(context)
    index_fragments = make_index_fragments(context)
    create_blocks = make_create_blocks(context)
    create_directives = make_create_directives(context)
    export_directive = make_export_directive(context)
    import_directive = make_import_directive(context)
    source_directive = make_source_directive(context)
    include_directive = make_include_directive(context)
    reassemble_text = make_reassemble_text(context)
    defragment_text = make_defragment_text(context)
    write_keyfile = make_write_keyfile(context)


    rules = build_rules([
        validate_context,
        traverse_path,
        fragment_text,
        index_fragments,
        create_blocks,
        create_directives,
        export_directive,
        import_directive,
        source_directive,
        include_directive,
        reassemble_text,
        defragment_text,
        write_keyfile,
    ])

    initial_facts = [Dummy()]
    production(initial_facts, rules)

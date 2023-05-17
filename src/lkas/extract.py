TAB = '  '
DELIM_LINE = '\n\n'


def generic(x, func_child, child_key, level):
    return DELIM_LINE.join(
        x['textlines']
        + [TAB * level + func_child(x) for x in x.get(child_key + 's', [])]
    )


def sub_paragraph(x) -> str:
    return '\n'.join(x['textlines'])


def paragraph(x) -> str:
    return generic(x, sub_paragraph, 'sub_paragraph', 3)


def subsection(x) -> str:
    return generic(x, paragraph, 'paragraph', 2)


def section(x) -> str:
    return generic(x, subsection, 'subsection', 1)


def part(x) -> str:
    return generic(x, section, 'section', 0)

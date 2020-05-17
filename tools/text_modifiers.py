"""
Module of tools, that modify text
"""

import re
import configs

__all__ = \
    [
        'article_text_modifier',
        'element_modifier'
    ]


def element_modifier(element: str) -> str:
    """ Function for modifying element """
    matched_element = re.search(configs.REGEX_PATTERN, element)

    if matched_element:
        element = ''.join(
            [element[:matched_element.end()], configs.SYMBOL_TO_APPEND, element[matched_element.end():]]
        )
    return element


def article_text_modifier(targets: list) -> None:
    """ Function for modifying the text according to configs """

    for node in targets:
        str_repr = str(node)
        split_out_notes = str_repr.split()

        if len(split_out_notes) > 1:
            new_str_repr = ''
            for element in split_out_notes:
                modified_element = element_modifier(element)
                new_str_repr = f'{new_str_repr} {modified_element}'

        else:
            new_str_repr = element_modifier(split_out_notes[0])

        node.replace_with(node.replace(str_repr, new_str_repr))

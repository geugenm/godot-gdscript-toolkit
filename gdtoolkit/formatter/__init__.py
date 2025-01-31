from types import MappingProxyType
from typing import Optional

from lark import Tree

from ..parser import parser
from .formatter import format_code  # noqa: F401
from .safety_checks import LoosenTreeTransformer  # noqa: F401
from .safety_checks import (
    check_comment_persistence,
    check_formatting_stability,
    check_tree_invariant,
)

DEFAULT_CONFIG = MappingProxyType(
    {
        "excluded_directories": {".git"},
        "safety_checks": True,
        "use_spaces": 4,
        "line_length": 80,
    }
)


# pylint: disable-next=too-many-arguments
# pylint: disable=too-many-positional-arguments
# pylint: disable=too-many-arguments
def check_formatting_safety(
    given_code: str,
    formatted_code: str,
    max_line_length: int,
    given_code_parse_tree: Optional[Tree] = None,
    given_code_comment_parse_tree: Optional[Tree] = None,
    spaces_for_indent: Optional[int] = None,
) -> None:
    if given_code == formatted_code:
        return
    formatted_code_parse_tree = parser.parse(formatted_code, gather_metadata=True)
    formatted_code_comment_parse_tree = parser.parse_comments(formatted_code)
    check_comment_persistence(
        given_code,
        formatted_code,
        given_code_comment_parse_tree=given_code_comment_parse_tree,
        formatted_code_comment_parse_tree=formatted_code_comment_parse_tree,
    )
    check_tree_invariant(
        given_code,
        formatted_code,
        given_code_parse_tree=given_code_parse_tree,
        formatted_code_parse_tree=formatted_code_parse_tree,
    )
    check_formatting_stability(
        formatted_code,
        max_line_length,
        parse_tree=formatted_code_parse_tree,
        comment_parse_tree=formatted_code_comment_parse_tree,
        spaces_for_indent=spaces_for_indent,
    )

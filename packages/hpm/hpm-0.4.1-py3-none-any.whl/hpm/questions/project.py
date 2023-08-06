import re
from ..namespaces import get_namespace_id
from .._typing import ProjectQuestion

QUESTIONS = [
    ProjectQuestion(
        message="💡 Project name",
        name="name",
        default="",
        help="The name cannot contains space",
        validate=lambda v: bool(re.search(r"^[\w\d\-\s]*$", v) and len(v) > 0),
    ),
    ProjectQuestion(
        message="📁 Project path (use empty value to skip)",
        name="path",
        default="",
        help="The name cannot contains space",
        validate=lambda v: bool(re.search(r"^[\w\d\-]*$", v)),
    ),
    ProjectQuestion(
        message="📄 Project description (use empty value to skip)",
        name="description",
        default="",
        help="The length cannot pass 255",
        validate=lambda v: bool(len(v) <= 255),
    ),
    ProjectQuestion(
        message="📖 Initialize project with a README (y, n)",
        name="initialize_with_readme",
        default="n",
        help="Choose between y, and n",
        validate=lambda v: bool(v in ["y", "n"]),
        transform=lambda v: True if v == "y" else False,
    ),
    ProjectQuestion(
        message="👀 Project visibility",
        name="visibility",
        default="public",
        help="Choose between public, internal, or private",
        validate=lambda v: bool(v in ["public", "internal", "private"]),
    ),
    ProjectQuestion(
        message="🗃️ Project namespace (<group>\[/<subgroup>, ...], use empty value to skip)",
        name="namespace_id",
        default="",
        help="",
        validate=lambda v: bool(re.search(r"(^$|^[\w\d.-\/]*$|)", v)),
        transform=lambda v: get_namespace_id(v) if v != "" else None,
    ),
    ProjectQuestion(
        message="🕹️ Remote for repo (ssh, https)",
        name="remote_type",
        default="ssh",
        help="Choose between ssh, and https",
        validate=lambda v: bool(v in ["ssh", "https"]),
        non_api=True
    )
]

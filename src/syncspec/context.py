from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class Context:
    open_delimiter: str
    close_delimiter: str
    keyvalue_file: str
    keyvalue: dict
    input_path: str
    import_path_prefix: str
    export_path_prefix: str
    output_path_prefix: str
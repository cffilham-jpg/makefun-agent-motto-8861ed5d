"""Write the chosen docs-first motto as exact UTF-8 bytes.
Its compact, conversational profile voice made it the strongest candidate.
"""

import hashlib
import os
import tempfile
from pathlib import Path

LINE = "I read the docs so you don't have to."
CHAR_LIMIT = 200


def _resolve_output_dir() -> Path:
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir:
        path = Path(env_dir)
        path.mkdir(parents=True, exist_ok=True)
        return path
    try:
        out = Path("out")
        out.mkdir(parents=True, exist_ok=True)
        return out
    except OSError:
        return Path(tempfile.mkdtemp(prefix="makefun-agent-motto-8861ed5d-"))


def validate(path: Path) -> None:
    data = path.read_bytes()
    text = data.decode("utf-8")
    if text != LINE:
        raise ValueError("entry.txt content does not match LINE")
    if not 1 <= len(text) <= CHAR_LIMIT:
        raise ValueError("entry must contain between 1 and 200 characters")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must contain exactly one line")
    if text.endswith("\n"):
        raise ValueError("entry must not end with a newline")
    if text != text.strip():
        raise ValueError("entry must not have leading or trailing whitespace")


def main() -> None:
    out_dir = _resolve_output_dir()
    entry = out_dir / "entry.txt"
    entry.write_bytes(LINE.encode("utf-8"))
    validate(entry)
    print(hashlib.sha256(LINE.encode("utf-8")).hexdigest())


if __name__ == "__main__":
    main()

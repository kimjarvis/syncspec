from pathlib import Path
def format_log_message(message: str, path: Path, line_number: int) -> str:
    return (
        f"{message}\n"
        f"        Line: {line_number}\n"
        f"        File: {path}\n\n"
    )


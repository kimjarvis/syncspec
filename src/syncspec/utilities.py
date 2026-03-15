def format_error(message: str, name: str, line_number: int) -> str:
    return (
        f"{message}\n"
        f"        Line: {line_number}\n"
        f"        File: {name}\n\n"
    )

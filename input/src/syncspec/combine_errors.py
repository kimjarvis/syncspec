from src.syncspec.error import Error
from src.syncspec.combine_errors_context import CombineErrorsContext

def make_combine_errors(context: CombineErrorsContext):
    def combine_errors(error: Error) -> None:
        msg = (
            f"Error: {error.message}\n"
            f"Line: {error.line_number}\n"
            f"File: {error.name}\n\n"
        )
        context.text += msg
    return combine_errors
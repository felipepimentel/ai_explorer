from pydantic import BaseModel, ValidationError
from typing import List, Dict, Any

class InputData(BaseModel):
    documents: List[str]
    timestamps: List[str]

def validate_input(data: Dict[str, Any]) -> InputData:
    try:
        return InputData(**data)
    except ValidationError as e:
        raise ValueError(f"Invalid input data: {e}")

# Uso:
# try:
#     validated_data = validate_input({"documents": ["doc1", "doc2"], "timestamps": ["2023-01-01", "2023-01-02"]})
# except ValueError as e:
#     print(f"Error: {e}")
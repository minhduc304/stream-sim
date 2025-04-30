import csv
import io
from typing import Dict, Any

def format_csv(record: Dict[str, Any]) -> str:
    """
    Format a record as CSV.
    """
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Get all field names
    field_names = list(record.keys())
    
    # Get values in the same order
    values = [record.get(field, "") for field in field_names]
    
    # Write the values
    writer.writerow(values)
    
    # Return the CSV string without trailing newline
    return output.getvalue().rstrip()
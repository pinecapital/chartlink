import json
from datetime import date

class CustomJSONEncoder(json.JSONEncoder):
    """Custom JSON Encoder that converts dates to strings."""
    def default(self, obj):
        if isinstance(obj, date):
            return obj.isoformat()  # Convert date objects to their ISO format (YYYY-MM-DD)
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)
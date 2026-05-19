import re
from django.core.exceptions import ValidationError

def validate_strong_password(value):
    pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*]).+$'
    if not re.match(pattern, value):
        raise ValidationError(
            "Password must include at least one uppercase letter, one lowercase letter, one number, and one special character (!@#$%^&*)."
        )
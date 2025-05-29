import re

def validate_password(password):
    if len(password) < 8:
        return False
    if not re.search(r'[A-Za-z]', password):
        return False
    if not re.search(r'\d', password):
        return False
    if not re.search(r'[!@#$%^&*()":;<>,.?/]', password):
        return False
    return True

# Test avec un mot de passe
print(validate_password("Test123!"))  # Doit retourner True
print(validate_password("avar>123"))  # Doit retourner False

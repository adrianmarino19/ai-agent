"""
Python Import Explanation - Visual Examples
============================================

This file demonstrates different ways to import and why some work and others don't.
"""

# ✅ CORRECT WAYS:

# Method 1: Import the whole module, then access things inside it
import google.genai.types
# Usage: google.genai.types.GenerateContentResponse

# Method 2: Import specific things from a module
from google.genai.types import GenerateContentResponse
# Usage: GenerateContentResponse (directly)

# Method 3: Import the genai package, then access its submodules
from google import genai
# Usage: genai.Client(...), genai.types.GenerateContentResponse

# Method 4: Import multiple things from the same module
from google.genai.types import (
    GenerateContentResponse,
    GenerateContentResponseUsageMetadata,
)
# Usage: Both classes available directly

# Method 5: Import with an alias
from google.genai.types import GenerateContentResponse as Response
# Usage: Response (instead of GenerateContentResponse)


# ❌ INCORRECT WAYS (these won't work):

# WRONG 1: Can't mix package and module-level imports like this
# from google import genai, types.GenerateContentResponse
# Error: 'types' is not directly under 'google', it's under 'google.genai'

# WRONG 2: Can't use dot notation in the import list like this
# from google import genai.types.GenerateContentResponse
# Error: Python doesn't parse nested paths in the 'from X import Y' format this way

# WRONG 3: Can't import a class from a package without specifying the module
# from google.genai import GenerateContentResponse
# Error: GenerateContentResponse is not directly in the genai package,
#        it's inside the types.py module file


"""
KEY TAKEAWAYS:
==============

1. Dots represent folder/file structure:
   google.genai.types = google/genai/types.py

2. 'from X import Y' means:
   - X must be a complete path to a module/package
   - Y must be something that exists directly in X

3. You can't skip levels:
   - If GenerateContentResponse is in google.genai.types
   - You can't import it from google or google.genai
   - You must import from google.genai.types

4. Each import statement handles ONE level:
   - 'from google import genai' imports the genai package
   - 'from google.genai.types import GenerateContentResponse' imports the class
   - These are separate operations, so they need separate import statements
"""

#!/usr/bin/python3
import re

# Example text
text = "Hello, world! Hello, everyone!"

# Pattern to match
pattern = r"Hello"

# Replacement string
replacement = "Hi"

# Using re.sub to replace occurrences of the pattern
result = re.sub(pattern, replacement, text)

print(result) 
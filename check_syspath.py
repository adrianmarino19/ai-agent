import sys

print("=== Running from project root ===")
print(f"sys.path[0]: {sys.path[0]}")
print(f"\nPython will look for imports in:")
for i, path in enumerate(sys.path[:3]):
    print(f"  {i}. {path}")

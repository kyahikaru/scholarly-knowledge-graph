import importlib
import sys

REQUIRED_MODULES = [
    "neo4j",
    "yaml",
    "pdfplumber",
    "torch",
    "numpy",
    "pandas",
    "sklearn",
    "tqdm",
    "spacy",
    "nltk",
    "transformers",
    "datasets",
    "networkx",
    "scipy",
]


def check_module(name: str) -> bool:
    try:
        importlib.import_module(name)
        print(f"[OK] {name}")
        return True
    except Exception as e:
        print(f"[FAIL] {name} -> {e}")
        return False


def main():
    print("Checking Python environment...\n")

    failures = 0
    for module in REQUIRED_MODULES:
        if not check_module(module):
            failures += 1

    if failures == 0:
        print("\nEnvironment check passed.")
        sys.exit(0)
    else:
        print(f"\nEnvironment check failed: {failures} modules missing.")
        sys.exit(1)


if __name__ == "__main__":
    main()



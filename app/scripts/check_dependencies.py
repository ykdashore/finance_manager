import sys
import subprocess


REQUIRED_PACKAGES = {
    "fastapi": "FastAPI web framework",
    "uvicorn": "ASGI server",
    "pydantic": "Data validation",
    "sqlalchemy": "ORM library",
    "langchain-core": "LangChain core",
    "langchain-google-genai": "Google Gemini integration",
    "langgraph": "Graph-based workflows",
    "google-genai": "Google Generative AI",
    "python-dotenv": "Environment variables",
    "pandas": "Data analysis",
}


def check_package(package_name):
    """Check if a package is installed."""
    try:
        __import__(package_name.replace("-", "_"))
        return True
    except ImportError:
        return False


def main():
    print("\n" + "="*60)
    print("DEPENDENCY VERIFICATION")
    print("="*60 + "\n")
    
    missing = []
    found = []
    
    for package, description in REQUIRED_PACKAGES.items():
        if check_package(package):
            found.append(package)
            print(f"{package:25} {description}")
        else:
            missing.append(package)
            print(f"{package:25} {description}")
    
    print("\n" + "="*60)
    
    if missing:
        print(f"\nMissing {len(missing)} package(s):\n")
        for pkg in missing:
            print(f"   - {pkg}")
        
        print("\nInstall missing packages:\n")
        print(f"   pip install {' '.join(missing)}\n")
        return 1
    else:
        print(f"All {len(found)} required packages are installed!\n")
        return 0


if __name__ == "__main__":
    sys.exit(main())

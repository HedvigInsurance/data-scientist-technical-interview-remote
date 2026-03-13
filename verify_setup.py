#!/usr/bin/env python3
import sys
import os
from pathlib import Path


def print_status(check_name: str, passed: bool, message: str = ""):
    status = "✓" if passed else "✗"
    color = "\033[92m" if passed else "\033[91m"
    reset = "\033[0m"
    print(f"{color}{status}{reset} {check_name}")
    if message:
        print(f"  → {message}")


def check_python_version():
    version = sys.version_info
    passed = version.major == 3 and version.minor >= 10
    version_str = f"{version.major}.{version.minor}.{version.micro}"

    if passed:
        print_status(f"Python version ({version_str})", True)
    else:
        print_status(
            f"Python version ({version_str})",
            False,
            "Required: Python 3.10 or higher"
        )
    return passed


def check_package_imports():
    try:
        from packaging import version as version_parser
        has_version_check = True
    except ImportError:
        version_parser = None
        has_version_check = False

    required_packages = {
        'fastapi': ('fastapi', '0.115.0'),
        'uvicorn': ('uvicorn', '0.30.0'),
        'pydantic': ('pydantic', '2.0.0'),
        'openai': ('openai', '1.0.0'),
        'chromadb': ('chromadb', '0.4.0'),
        'dotenv': ('python-dotenv', '1.0.0')
    }

    all_passed = True
    for module_name, (package_name, min_version) in required_packages.items():
        try:
            module = __import__(module_name)
            installed_version = getattr(module, '__version__', 'unknown')

            if installed_version == 'unknown':
                print_status(
                    f"Package: {package_name}",
                    True,
                    f"version unknown (requires >={min_version})"
                )
            elif has_version_check:
                if version_parser.parse(installed_version) >= version_parser.parse(min_version):
                    print_status(
                        f"Package: {package_name}",
                        True,
                        f"v{installed_version}"
                    )
                else:
                    print_status(
                        f"Package: {package_name}",
                        False,
                        f"v{installed_version} installed, requires >={min_version}"
                    )
                    all_passed = False
            else:
                # Fallback: just show version without validation
                print_status(
                    f"Package: {package_name}",
                    True,
                    f"v{installed_version} (install 'packaging' for version check)"
                )
        except ImportError:
            print_status(
                f"Package: {package_name}",
                False,
                f"Not installed. Run: pip install {package_name}>={min_version}"
            )
            all_passed = False

    return all_passed


def check_environment_variables():
    from dotenv import load_dotenv

    # Load .env file
    env_file = Path(".env")
    if not env_file.exists():
        print_status(
            "Environment file (.env)",
            False,
            "Create a .env file with required variables"
        )
        return False

    load_dotenv()

    required_vars = {
        'OPENAI_API_KEY': 'OpenAI API key for LLM calls',
        'CHROMA_DB_PATH': 'Path to ChromaDB storage',
        'EXPORT_DB': 'Path to export database'
    }

    all_passed = True
    for var_name, description in required_vars.items():
        value = os.getenv(var_name)
        if value:
            if 'KEY' in var_name:
                display_value = f"{value[:10]}...{value[-4:]}"
            else:
                display_value = value
            print_status(f"ENV: {var_name}", True, display_value)
        else:
            print_status(
                f"ENV: {var_name}",
                False,
                f"Required: {description}"
            )
            all_passed = False

    return all_passed


def main():
    print("\n" + "=" * 60)
    print("Claims Handler Environment Verification")
    print("=" * 60 + "\n")

    checks = [
        ("Python Version", check_python_version),
        ("Package Imports", check_package_imports),
        ("Environment Variables", check_environment_variables),
    ]

    results = {}
    for check_name, check_func in checks:
        print(f"\n{check_name}:")
        print("-" * 60)
        try:
            results[check_name] = check_func()
        except Exception as e:
            print_status(check_name, False, f"Unexpected error: {str(e)}")
            results[check_name] = False

    # Summary
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)

    passed = sum(1 for v in results.values() if v)
    total = len(results)

    print(f"\nPassed: {passed}/{total} checks")

    if all(results.values()):
        print("\n✓ Environment is ready!")
        print("\n")
        return 0
    else:
        print("\n✗ Please fix the issues above before proceeding.")
        print("\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())

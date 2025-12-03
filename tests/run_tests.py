# tests/run_tests.py
import pytest
import sys
import os

# Add project root to path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, PROJECT_ROOT)

if __name__ == "__main__":
    print("\nBazar Kori - Full Test Suite")
    print("Project Root:", PROJECT_ROOT)
    print("=" * 70)

    exit_code = pytest.main([
        "tests/",
        "-vv",
        "--tb=short",
        "--color=yes",
        "--durations=5"
    ])

    print("\n" + "=" * 70)
    if exit_code == 0:
        print("ALL TESTS PASSED SUCCESSFULLY!")
    else:
        print(f"TESTS FAILED: {exit_code}")
    sys.exit(exit_code)
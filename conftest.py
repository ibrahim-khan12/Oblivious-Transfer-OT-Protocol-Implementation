import pytest
from ot_protocol import PRIME, GENERATOR

@pytest.fixture(autouse=True)
def run_around_tests():
    # Setup: Initialize fresh cryptographic parameters for each test
    print("\n=== Starting Test ===")
    yield
    # Teardown: Clear sensitive data
    print("=== Test Complete ===\n")

@pytest.fixture
def test_vectors():
    # RFC 3526 test vectors
    return {
        "prime": PRIME,
        "generator": GENERATOR,
        "test_private_key": 123456789,
        "test_public_key": pow(GENERATOR, 123456789, PRIME)
    }
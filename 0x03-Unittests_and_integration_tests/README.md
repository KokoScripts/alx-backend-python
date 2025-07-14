# ALX Backend Python - Unittests and Integration Tests

This project covers how to write **unit tests** and **integration tests** for Python code, focusing on client classes that interact with external APIs (like GitHub). You’ll practice mocking, patching, parameterizing tests, and using fixtures for integration tests.

## Directory Structure

```
0x03-Unittests_and_integration_tests/
├── test_utils.py
├── test_client.py
└── README.md
```

## Files

- **client.py**: Contains the `GithubOrgClient` class, which interacts with the GitHub API.
- **fixtures.py**: Provides sample data for integration testing.
- **test_client.py**: Contains unit and integration tests for `GithubOrgClient`.
- **README.md**: Project documentation.

## Main Concepts

- **Unit Testing**: Test individual methods and functions in isolation using mocking.
- **Integration Testing**: Test how components work together, using fixtures to simulate API responses.
- **Mocking and Patching**: Use `unittest.mock` to replace parts of your system under test.
- **Parameterization**: Use the `parameterized` library to run tests with different inputs.
- **PyCodeStyle Compliance**: All code adheres to Python style guidelines.

## How to Run the Tests

Make sure you have `pytest` and `parameterized` installed:

```bash
pip install pytest parameterized
```

Then, run the tests:

```bash
pytest test_client.py
```

## Example: GithubOrgClient

The `GithubOrgClient` class fetches organization data and repositories from the GitHub API.

### Example usage:

```python
from client import GithubOrgClient

client = GithubOrgClient("google")
repos = client.public_repos()
print(repos)
```

## Key Test Features

- **Mocking properties and methods**
- **Testing with various payloads**
- **Checking for correct API usage**
- **Integration tests using fixtures**

## Author

KokoScripts

## License

This project is intended for educational purposes as part of the ALX curriculum.


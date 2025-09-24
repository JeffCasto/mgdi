# Contributing to MGDI

We welcome contributions from the community! If you would like to contribute to the project, please follow these guidelines.

## Getting Started

1.  Fork the repository and create a new branch for your feature or bug fix.
2.  Make your changes and ensure that all tests pass.
3.  Submit a pull request with a clear description of your changes.

## Linting

To ensure code quality, we use `flake8` to lint the Python code and `eslint` and `prettier` to lint the TypeScript code.

### Python

To run the Python linter, use the following command:

```sh
flake8 backend/app
```

**Note:** There are currently a number of "line too long" errors in the codebase. These errors are not critical and will be addressed in a future refactoring.

### TypeScript

To run the TypeScript linter, use the following commands:

```sh
cd frontend
npm install
npm run lint
```

To run the linter, use the `npm run lint` command in the `frontend` directory.

## Contact

If you have any questions, please open an issue or contact the project maintainers.

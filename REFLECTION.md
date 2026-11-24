# Module 12 Reflection

In Module 12, I connected my User and Calculation models to FastAPI routes for registration, login, and calculation BREAD operations. Using Pydantic schemas helped validate inputs and hide password hashes in responses.

Testing the routes in /docs and writing integration tests in pytest helped me catch bugs early. At first, pytest failed because of a mismatched password hash function name in my test imports and checking for status code 200 instead of 201 on POST requests. Fixing the import name, updating the status codes, and validating PUT updates with CalculationFactory solved these issues.

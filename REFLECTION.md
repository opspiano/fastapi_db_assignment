# Module 12 Reflection

In Module 12, I connected my User and Calculation models to FastAPI routes for registration, login, and calculation BREAD operations. Using Pydantic schemas helped validate inputs and hide password hashes in responses.

Testing the routes in /docs and writing integration tests in pytest helped me catch bugs early. At first, my tests failed because I checked for status code 200 instead of 201 on POST requests, and I also had to make sure the PUT route recalculated results while blocking division by zero. Fixing the status codes and validating updates with CalculationFactory solved these issues.

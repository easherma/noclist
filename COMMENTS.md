# How to Run
Note: The project was built with Python 3.8 and poetry. However a requirements.txt file has been provided but not tested.

1. Clone the repo and navigate to the project directory.
2. In the directory, run ```poetry install```
3. To run the program, run ``` poetry run python noclist.py ```

# How to test

Follow the install instrucitons above, then run ``` poetry run pytest ```

# Notes
Time spent: ~ 5 hours
Many of the functions are trivial and the use case is pretty artifical, but I kept things seperated to simulate how I might design something that was a bit more real world and complex. 

# What I'd do next/better

* Better, more standard logging using Python's logger as opposed to print statements

* More specific exception handiling. In a real world case, this would involve more integration tests and consulting with clients/users around how we want to handle instabilities

* I was quickler trying to implement the simplest solutions with the lowest common denominator functionality. It might make sense to refactor these functions into related objects, though I avoided this since the spec did not involve any significant plans for reuse and I thought it would be better to compose functionality than rely on any inheritance. 

* Test coverage could easily be refactored to use fixtures and reduce boilerplate. I would also write tests for the retry wrapper itself to verify that it handles cases with the current number of attempts.

* Move more parsing and returning functionality out of main() and into other functions

* Ideally the auth token function itself would return the token, while still being able to be wrapped in the retry decorator 
* I also noticed an edge case where the server seemingly does not always invalidate the auth token just by calling get `/auth`. This may be an error on my end; however it isn't preventing correct output at this time. 
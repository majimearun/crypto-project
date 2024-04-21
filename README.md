# Crypto Project: Decentralized Grade Storage

## Group 1

- Arunachala Amuda Murugan (2021A7PS0205H)
- Dharanikanth Reddy Yerasi (2021A7PS0264H)
- Divyateja Pasupuleti (2021A7PS0075H)
- Pranav Dinesh Sharma (2021A7PS2818H)

## Instructions to run the project

1. Download [poetry](https://python-poetry.org/docs/#installation).
2. Clone the repository (or) download the zip file and extract it.
3. Open the terminal and navigate to the project directory.
4. Run the following command to install the dependencies:
    ```bash
    poetry shell # creates a virtual environment
    poetry install # installs the dependencies
    ```
5. run `main.py` from this virtual environment to run the project.

## Files 

1. `authenticator.py` - Contains class and function for challenge response authentication.
2. `blockchain.py` - Contains class and all the required functions for blockchain (block mining, validitating blockchin, verification of transactions and viewing transactions and other util functions as well).
3. `company.py`, `university.py`, `student.py` - Contains classes for company, university and student respectively (users).
4. `main.py` - Contains the main function to run the project.
5. `seed.py` - Contains seed data for the project.
6. `get_response.py` - Contains a script which generates the required CRA + HMAC response.

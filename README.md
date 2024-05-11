**Robust Intelligent Query Processing System using Generative AI and FAST APIs**

**Introduction**

This project is a language model chat application that allows users to interact with a conversational AI using different file formats. The application supports PDF, DOCX, XLS, and CSV file formats for input. It uses a PostgreSQL database to manage user sessions and chat history.



**Project Structure**

Your project is a FastAPI application that provides a variety of functionalities, including creating users, managing sessions, and processing files. This README file contains instructions on how to set up and run the project, as well as how to test its functionalities

**Requirements**

-Python 3.8 or higher
-FastAPI
-Uvicorn
-SQLAlchemy
-Pydantic
-Other required packages are listed in requirements.txt


**Installation**

1) Clone the repository:

   git clone https://github.com/yourusername/yourproject.git

2) Create a virtual environment and activate it:

  python -m venv venv
  source venv/bin/activate (on Linux/macOS)
  venv\Scripts\activate (on Windows)

3) Install the required packages:

  pip install -r requirements.txt

4) Set up the database:

  createdb yourproject
  psql yourproject < db_setup.sql

5) Run the application:

  uvicorn main:app --reload

**Testing**'

project includes a variety of test cases that cover all the functionalities of the system. To run the tests, use the following command:
$ pytest

Here is an example of a test case for the /create-users/ endpoint:

def test_create_user():
    response = client.post("/create-users/", json={"username": "testuser", "email": "testuser@example.com"})
    assert response.status_code == 200
    assert response.json() == {"id": 1, "username": "testuser"}

**File Structure**

 - app
  - __init__.py
  - main.py
  - models
    - __init__.py
    - models.py
    - pydantic_models.py
  - parse_file.py
  - splits_into_chunks.py
  - embeddings
    - __init__.py
    - embeddings.py
  - tools_and_agents
    - __init__.py
    - agents.py
- tests
  - __init__.py
  - test_main.py
- db_setup.sql
- requirements.txt
- README.md

**Environment Variables**

The following environment variables are required:

POSTGRES_USER: The PostgreSQL user name.
POSTGRES_PASSWORD: The PostgreSQL user password.
POSTGRES_SERVER: The PostgreSQL server address.
POSTGRES_PORT: The PostgreSQL server port.
POSTGRES_DB: The PostgreSQL database name.
GROQ_API_KEY: The GROQ API key.
SERPAPI_API_KEY: The SerpAPI API key.
Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

**License**
This project is licensed under the MIT License.
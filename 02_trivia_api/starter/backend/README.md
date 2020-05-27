# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

run these commands for virtual environment:
python3 -m venv venv;&&
. venv/bin/activate

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
cd 02_trivia_api/starter/backend/&&
export FLASK_APP=flaskr&&
export FLASK_ENV=development&&
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

REVIEW_COMMENT
```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code. 

Endpoints
GET '/categories'
POST '/categories'
GET '/questions'
DELETE '/questions/<int:question_id>'
POST '/questions'
POST '/searchQuestions'
GET '/categories/<int:category_id>/questions'
POST '/quizzes'

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}


POST '/categories'
- Sends to the database a new category by sending an object type Category and defining only the type of the category only.
- Request Arguments: None
- Returns: the status of the operation, a dictionary of category and the number of current categories.
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

GET '/questions'
- Fetches a list of questions ordered by id and then they are paginated and then it fetches the categories and order them by id.
- Request Arguments: None
- Returns: the status of the operation , a dictionary of questions , the categories and the number of the questions.
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports", 
    "7": "Cool"
  }, 
  "questions": [
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?", 
      "rating": null
    }, 
    "success": true, 
  "totalQuestions": 23
}


DELETE '/questions/<int:question_id>'
- Deletes a selected questions by calling the method delete() in models.py from the database.
- Request Arguments: Questions.id.
- Returns: the status of the operation, the id of the deleted question, a dictionary of Questions, the total number of Questions.
{
  "deleted": 12,
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?",
      "rating": null
    },
    "success": true,
  "totalQuestions": 22
}

POST '/questions'
- Sends a new questions to database from the frontend by filling out the attributes of Question and inserting it by using insert() in models.py.
- Request Arguments: None
- Returns: the status of the insertion, the id of the new posted question, a dictionary of the Questions, the total number of Questions.


POST '/searchQuestions'
- Sends a string to be matched with the other Question.question in the database using ilike.
- Request Arguments: None.
- Returns: the status of the search, the questions that matched it as a dictionary, the total number of questions that matched the string.
{
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?",
      "rating": null
    }
  ],
  "success": true,
  "totalQuestions": 1
}

GET '/categories/<int:category_id>/questions'
- Sends an id number matching an id number of Category.id and sends that Questions.Category.id back only.
- Request Arguments: Category.id.
- Returns: the status of the operation, a dictionary of questions mathcing the condition, the total number of questions that match it.
{
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?",
      "rating": null
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?",
      "rating": null
    },
    {
      "answer": "Scarab",
      "category": 4,
      "difficulty": 4,
      "id": 23,
      "question": "Which dung beetle was worshipped by the ancient Egyptians?",
      "rating": null
    }
  ],
  "success": true,
  "totalQuestions": 3
}


POST '/quizzes'
- Recieves a category id for the Question.Categoty and then it stores the displayed questions in an array so they won't be displayed later, if you answer correctly it will increase your point if you answer wrong the questions will be terminated and it will display the current score.
- Request Arguments: None.
- Returns: the status of the operation and a question.

```

## Testing
To run the tests, run
```
testing is done in the virtual environment instructions are above


cd 02_trivia_api/starter/backend/&&
dropdb trivia_test&&
createdb trivia_test&&
psql trivia_test < trivia.psql&&
python test_flaskr.py
```
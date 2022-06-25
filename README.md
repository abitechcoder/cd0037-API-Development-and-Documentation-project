# API Development and Documentation Final Project

## Trivia App

This project is a trivia game for Udacity students and its employees. Team members are able to display all questions at once or by category, delete questions, add new question with its answer, search for questions based on a text query string and play the quiz game randomizing either all questions or within a specific category.

All backend code follows [PEP8 style guidelines](https://www.python.org/dev/peps/pep-0008/).

## Getting Started

### Pre-requisites and Local Development

Developers using this project should already have Python3, pip and node installed on their local machines.

#### Backend

From the backend folder run `pip install requirements.txt`. All required packages are included in the requirements file.

To run the application run the following commands:

```
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

These commands put the application in development and directs our application to use the `__init__.py` file in our flaskr folder. Working in development mode shows an interactive debugger in the console and restarts the server whenever changes are made. If running locally on Windows, look for the commands in the [Flask documentation](http://flask.pocoo.org/docs/1.0/tutorial/factory/).

The application is run on `http://127.0.0.1:5000/` by default and is a proxy in the frontend configuration.

#### Frontend

From the frontend folder, run the following commands to start the client:

```
npm install // only once to install dependencies
npm start
```

By default, the frontend will run on localhost:3000.

## API REFERENCE

### Getting Started

- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration.
- Authentication: This version of the application does not require authentication or API keys.

### Error Handling

Errors are returned as JSON objects in the following format:

```
{
    "success": False,
    "error": 400,
    "message": "bad request"
}
```

The API will return three error types when requests fail:

- 400: Bad Request
- 404: Resource Not Found
- 422: Not Processable
- 500: Internal Server Error

### API ENDPOINTS

`GET '/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, `categories`, that contains an object of `id: category_string` key: value pairs.

#### Sample

- `curl http://127.0.0.1:5000/categories`

#### Returns:

```json
{
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
}
```

`GET '/questions?page=${integer}'`

- Fetches a paginated set of questions, a total number of questions, all categories and current category string.
- Request Arguments: `page` - Integer
- Returns: An object with 10 paginated questions, total questions, object including all categories, and current category string

#### Sample

- `curl http://127.0.0.1:5000/questions?page=1`

#### Returns:

```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": "History",
  "questions": [
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    },
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    },
    {
      "answer": "Escher",
      "category": 2,
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    }
  ],
  "total_questions": 20
}
```

`GET '/categories/${category_id}/questions'`

- Fetches questions for a cateogry specified by id request argument
- Request Arguments: `category_id` - integer
- Returns: An object with questions for the specified category, total questions, and current category string

#### Sample

- `curl http://127.0.0.1:5000/categories/1/questions`

#### Returns:

```json
{
  "current_category": "Science",
  "questions": [
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "Blood",
      "category": 1,
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    }
  ],
  "total_questions": 3
}
```

`DELETE '/questions/${question_id}'`

- Deletes a specified question using the id of the question
- Request Arguments: `id` - integer
- Returns: Does not need to return anything besides the appropriate HTTP status code. Optionally can return the id of the question. If you are able to modify the frontend, you can have it remove the question using the id instead of refetching the questions.

#### Sample

- `curl -X DELETE http://127.0.0.1:5000/questions/9`

#### Returns:

```json
{
  "deleted": 9,
  "success": true
}
```

`POST '/quizzes'`

- Sends a post request in order to get the next question
- Request Body:

```json
{
  "previous_questions": [],
  "quiz_category": { "type": "Science", "id": "1" }
}
```

#### Sample

- `curl -X POST http://127.0.0.1:5000/quizzes -d '{"previous_questions":[4, 14, 31], "quiz_category": {"type": "Science", "id": "1"}}' -H "Content-Type:application/json"`

#### Returns:

```json
{
  "question": {
    "answer": "Alexander Fleming",
    "category": 1,
    "difficulty": 3,
    "id": 21,
    "question": "Who discovered penicillin?"
  }
}
```

`POST '/questions'`

- Sends a post request in order to add a new question
- Request Body:

```json
{
  "question": "Heres a new question string",
  "answer": "Heres a new answer string",
  "difficulty": 1,
  "category": 3
}
```

#### Sample

- `curl -X POST http://127.0.0.1:5000/questions -d '{"question":"What is Abiola Adeosun brother's name?","answer":"Mayowa Adeosun","difficulty":"3","category":"4"}' -H "Content-Type:application/json"`

#### Returns:

```json
{
  "created": 35,
  "success": true
}
```

`POST '/questions'`

- Sends a post request in order to search for a specific question by search term
- Request Body:

```json
{
  "searchTerm": "this is the term the user is looking for"
}
```

#### Sample

- `curl -X POST http://127.0.0.1:5000/questions -d '{"searchTerm":"author"}' -H "Content-Type:application/json"`

#### Returns:

```json
{
  "current_category": "Entertainment",
  "questions": [
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }
  ],
  "total_questions": 1
}
```

### Tests

In order to run tests navigate to the backend folder and run the following commands:

```
dropdb bookshelf_test
createdb bookshelf_test
psql bookshelf_test < books.psql
python test_flaskr.py
```

The first time you run the tests, omit the dropdb command.

All tests are kept in that file and should be maintained as updates are made to app functionality.

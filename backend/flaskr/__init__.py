import os
from flask import Flask, request, abort, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

# Get a list of paginated questions
def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    questions = [question.format() for question in selection]
    current_questions = questions[start:end]
    return current_questions

# Generate and return a random number
def get_random_number(num_list):
    rand_num = random.choice(num_list)
    return rand_num

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app, origins="*")

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    #CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization,true")
        response.headers.add("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS")
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route("/categories", methods=['GET'])
    def get_categories():
        try:
            selection = Category.query.all()
            categories_list = [category.format() for category in selection]
            if len(categories_list) == 0:
                abort(404)
            categories = {}
            for category in categories_list:
                categories.update({category.get("id"): category.get("type")})
            return jsonify({
                'categories': categories
            })
        except:
            abort(500)
        

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/questions', methods=['GET'])
    def get_questions():
        try:
            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, selection)
            if len(current_questions) == 0:
                abort(404)
            categories_list = [category.format() for category in Category.query.all()]
            categories = {}
            for category in categories_list:
                categories.update({category.get("id"): category.get("type")})
            
            return jsonify({
                'questions': current_questions,
                'total_questions': len(selection),
                'categories': categories,
                'current_category': 'History'
            })
        except:
            abort(500)

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:id>', methods=['DELETE'])
    def delete_question(id):
        try:
            print("Id to delete", id)
            question = Question.query.filter(Question.id == id).one_or_none()
            if question is None:
                abort(404)
            question.delete()
            return jsonify({
                'success': True,
                'deleted': id
            })
        except:
            abort(422)
    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """ 

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    @app.route('/questions', methods=['POST'])
    def create_and_search_question():
        body = request.get_json()
        new_question = body.get("question", None)
        new_answer = body.get("answer", None)
        new_difficulty = body.get("difficulty", None)
        new_category = body.get("category", None)
        search_term = body.get("searchTerm", None)
        try:
            if search_term:
                selection = Question.query.filter(Question.question.ilike('%{}%'.format(search_term))).order_by(Question.id).all()
                found_questions = paginate_questions(request, selection)
                return jsonify({
                    'questions': found_questions,
                    'total_questions': len(selection),
                    'current_category': 'Entertainment'
                })         
            elif new_question and new_answer:
                question = Question(question=new_question, answer=new_answer, difficulty=new_difficulty, category=new_category)
                question.insert()

                return jsonify({
                    'success': True,
                    'created': question.id
                })
            else:
                return redirect(url_for('get_questions'))
        except:
            abort(400)

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_by_categories(category_id):
        try:
            category = Category.query.filter(Category.id == category_id).one_or_none()
            if category is None:
                abort(404)
            selection = Question.query.filter(Question.category == category_id).all()
            questions = paginate_questions(request, selection)
            
            return jsonify({
                'questions': questions,
                'total_questions': len(selection),
                'current_category': category.type
            })
        except:
            abort(404)
    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        body = request.get_json()
        previous_questions = body.get("previous_questions", None)
        quiz_category = body.get("quiz_category", None)
        question_list = []
        questions = Question.query.order_by(Question.id).all()
        selected = []
        try:

            # format all questions from the model Question
            formatted_questions = [question.format() for question in questions]
            # Checks if the value of quiz_category id is equal to 0
            if quiz_category.get("id") == 0:
                selected = formatted_questions
            # select question by the category
            else: 
                selected = [question for question in formatted_questions if question["category"] == int(quiz_category.get("id"))]
            question_id_list = [q.get("id") for q in selected]

            # Get random number from the function get_random_number
            random_number = get_random_number(question_id_list)
            # Check if the random number is in the previous_questions list
            if random_number in previous_questions:
                random_number = get_random_number(question_id_list)
            else:
                # Get the question that it's id is equal to the random number
                question_list = [question for question in formatted_questions if question["id"] == random_number]
            return jsonify({
                'question': question_list[0],
            })
        except:
            abort(500)
            
    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'Bad request supplied'
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'resource not found'
        }), 404
    
    @app.errorhandler(422)
    def unprocessed(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'request unprocessable'
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'internal server error'
        }), 500

    return app


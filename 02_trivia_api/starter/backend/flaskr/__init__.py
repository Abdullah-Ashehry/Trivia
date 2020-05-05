import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)

  @app.after_request
  def handle_response(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    return response
        
  @app.route('/categories')
  def retrieve_categories():
    # categories = list(map(Category.format, Category.query.order_by(Category.id).all()))
    categories = [cat.format() for cat in Category.query.all()]


    if len(categories) == 0:
      abort(404)

    return jsonify({
      "success": True,
      "categories": categories,
      'total_categories': len(Category.query.all())
    })


  def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start =  (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions
  
  @app.route('/questions')
  def retrieve_questions():
    # selection = list((Question.query.order_by(Question.id).all()))
    selection = [ques.format() for ques in Question.query.order_by(Question.id).all()]
    categories = [cat.format() for cat in Category.query.all()]
    current_quesions = paginate_questions(request,selection)
    
    if (len(current_quesions) == 0):
      abort(404)

    return jsonify({
      'success': True,
      'questions': current_quesions,
      "categories": categories,
      'totalQuestions': len(Question.query.all())
    })

  
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    try:
      question = Question.query.filter(Question.id == question_id).one_or_none()

      if question is None:
        abort(404)

      question.delete()
      selection = Question.query.order_by(Question.id).all()
      current_questions = paginate_questions(request, selection)

      return jsonify({
        'success': True,
        'deleted': question_id,
        'questions': current_questions,
        'totalQuestions': len(Question.query.all())
      })

    except:
      abort(422)      

  @app.route('/questions', methods=['POST'])
  def post_question():
    body = request.get_json()

    new_question = body.get('question',None)
    new_answer = body.get('answer', None)
    new_category = body.get('category', None)
    new_difficulty = body.get('difficulty', None)
    
    try:
      question = Question(question = new_question, answer = new_answer, category = new_category, difficulty = new_difficulty)
      question.insert()

      selection = Question.query.order_by(Question.id).all()
      current_questions = paginate_questions(request, selection)

      return jsonify({
        'success': True,
        'created': question.id,
        'questions': current_questions,
        'totalQuestions': len(Question.query.all())
      })

    except:
      abort(422)

  @app.route('/searchQuestions',  methods=['POST'])
  def search_questions():
      try:
        body = request.get_json()
        search_term = request.form.get('searchTerm', '')
       

        selection = Question.query.filter(Question.question.ilike('%{}%'.format('searchTerm'))).all()
        # paginate = paginate_questions(request,selection)
        questions = [que.format() for que in selection]
        

        if(len(questions) == 0): 
              abort(400)
        
        result = {
          "success": True,
          "questions": questions,
          "totalQuestions": len(questions)
        }
        return jsonify(result)
      except:
        abort(404)

  @app.route('/categories/<int:category_id>/questions')
  def questions_by_category(category_id):
        questions = Question.query.filter(Question.category == category_id).all()
        
        if(len(questions) == 0):
          abort(404)
        
        selection = paginate_questions(request,questions)

        return jsonify({
          'success':True,
          'questions':selection,
          'totalQuestions':len(questions)
        })
    

  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  # @app.route('/quizzes')
  # def quizzes_questions():
  #   body = request.get_json()   
  #   question_category = body.get('category', None)
  #   selection = list(Question.query.filter(Question.category == question_category).all())

  @app.route('/quizzes', methods=["POST"]) 
  def post_quizzes():
    '''
    Returns a single question from the database
    Filters the questions already sent to the client
    '''
    try:
      data = request.get_json()
      # check given category
      category_id = int(data["quiz_category"]["id"])
      category = Category.query.get(category_id)
      previous_questions = data["previous_questions"]
      if not category == None:  
        if "previous_questions" in data and len(previous_questions) > 0:
          questions = Question.query.filter(
            Question.id.notin_(previous_questions),
            Question.category == category.id
            ).all()  
        else:
          questions = Question.query.filter(Question.category == category.id).all()
      else:
        if "previous_questions" in data and len(previous_questions) > 0:
          questions = Question.query.filter(Question.id.notin_(previous_questions)).all()  
        else:
          questions = Question.query.all()
      max = len(questions) - 1
      if max > 0:
        question = questions[random.randint(0, max)].format()
      else:
        question = False
      return jsonify({
        "success": True,
        "question": question
      })
    except:
      abort(500, "An error occured while trying to load the next question")


  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False, 
      "error": 404,
      "message": "Resource Not Found"
      }), 404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success": False, 
      "error": 422,
      "message": "Unprocessable"
      }), 422

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success": False, 
      "error": 400,
      "message": "Bad Request"
      }), 400

  @app.errorhandler(500)
  def bad_request(error):
    return jsonify({
      "success": False, 
      "error": 500,
      "message": "Intrenal Server Error"
      }), 500
  
  return app

    
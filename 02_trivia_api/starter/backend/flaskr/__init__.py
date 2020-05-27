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
  def add_cors_headers(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, PUT, POST, PATCH, DELETE, OPTIONS')
        return response
        
  @app.route('/categories')
  def retrieve_categories():
    
    categories = Category.query.all()
    catgs = {cat.id:cat.type for cat in categories}

    if len(categories) == 0:
      abort(404)

    return jsonify({
      "success": True,
      "categories": catgs,
      'total_categories': len(Category.query.all())
    })
  
  @app.route('/categories', methods=['POST'])
  def post_category():
    body = request.get_json()
    new_type = str(body.get('type',None))
    categories = Category.query.all()
    catgs = {cat.id:cat.type for cat in categories}
        
    try:  
        new_category = Category(type = new_type)
        new_category.insert()
        categories = Category.query.all()
        catgs = {cat.id:cat.type for cat in categories}
        
        return jsonify({
        'success': True,
        'categories': catgs,
        'totalCategories': len(Category.query.all())
      })
    except:
        abort(422)
          


  def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start =  (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions
  
  @app.route('/questions')
  def retrieve_questions():
   
    selection = list(Question.query.order_by(Question.id).all())
    current_quesions = paginate_questions(request,selection)
    categories = Category.query.all()
    catgs = {cat.id:cat.type for cat in categories}

    if (len(current_quesions) == 0):
      abort(404)

    return jsonify({
      'success': True,
      'questions': current_quesions,
      'categories' : catgs,
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
        'deleted': question.id,
        'questions': current_questions,
        'totalQuestions': len(Question.query.all())
      })

    except:
       abort(422)      

  @app.route('/questions', methods=['POST'])
  def post_question():
    body = request.get_json()
 
    new_question = body.get('question', None)
    new_answer = body.get('answer', None)
    new_category = body.get('category', None)
    new_difficulty = body.get('difficulty', None)
    new_rating = body.get('rating', None)
    
    try:
      question = Question(question = new_question, answer = new_answer, category = new_category, difficulty = new_difficulty, rating = new_rating)
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
   
        body = request.get_json()
        search_term = body.get('searchTerm', '')
        search_term = search_term.strip()
       
        selection = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()
        questions = [que.format() for que in selection]
         

        if(len(questions) == 0): 
              result = {
                "success": True,
                "questions": "No Results",
                "totalQuestions": 0
              }
              
        else:
          result = {
          "success": True,
          "questions": questions,
          "totalQuestions": len(questions)
          }
        return jsonify(result)
   
  @app.route('/categories/<int:category_id>/questions', methods=['GET'])
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
    
  
  @app.route('/quizzes', methods=["POST"]) 
  def post_quizzes():
    try:
      data = request.get_json()
    
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

    
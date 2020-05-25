import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question = {
            'question': 'What is the longest TV Show i watched ? ',
            'answer' : 'Grey Anatomy',
            'category' : '3',
            'difficulty' : '4'
        }
        
        self.questions_category = {
            'id' : '4'
        }
        
        self.quiz_category = {
            'previous_questions': [5, 9],
            'quiz_category': {
                'type': 'History',
                'id': 4
            }}
    
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_categories']) 
        self.assertTrue(len(data['categories']))    

    def test_get_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['totalQuestions'])
        self.assertTrue(len(data['questions']))

    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_404_if_question_does_not_exist(self):
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')
        

    def test_get_question_search_with_results(self):
        res = self.client().post('/searchQuestions', json={'searchTerm': 'Oscar'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['totalQuestions'])
        self.assertEqual(len(data['questions']), 1)

    def test_get_question_search_without_results(self):
        res = self.client().post('/searchQuestions', json={'searchTerm': 'dude'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['totalQuestions'], 0)
        

    def test_delete_question(self):
        res = self.client().delete('/questions/4')
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == 4).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 1)
        self.assertTrue(data['totalQuestions'])
        self.assertTrue(len(data['questions']))
        self.assertEqual(Question, None)
        
    
    def test_post_new_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)
        pass
    
    def test_422_if_question_creation_fails(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)
        pass

    def test_questions_by_category(self):
        res = self.client().post('categories', json=self.questions_category)
        data = json.loads(res.data)
        pass
    
    def test_quiz_random_question(self):
        response = self.client().post('/quizzes', 
                json=self.quiz_category)
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        # self.assertTrue(data['question']) 



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
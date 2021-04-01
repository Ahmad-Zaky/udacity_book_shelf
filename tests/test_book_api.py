import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from bookshelf import create_app
from models import setup_db

class BookTestCase(unittest.TestCase):
  # This Class represents the book shelf test case

  def setUp(self):
    # Define Test Variables and init. app

    self.app = create_app()
    self.client = self.app.test_client
    self.database_name = "bookshelf_test"
    self.database_path = "postgresql://{}:{}@{}/{}".format("postgres", "posgtres_me", "localhost:5432", self.database_name)
    setup_db(self.app, self.database_path)

    self.new_book = {
      "title":"test title",
      "author":"test author",
      "rating":5
    }

    def tearDown(self):
      # Execute afte each test
      pass

    def test_get_paginated_books(self):
      res = self.client.get('/books')
      data = json.loads(res.data)

      self.assertEqual(res.status_code, 200)
      self.assertEqual(data['success'], True)
      self.assertEqual(data['total_books'])
      self.assertEqual(len(data['books']))

    def test_404_requesting_beyond_valid_page():
      res = self.client.get('/books?page=1000', json={'rating': 1})
      data = json.loads(res.data)
      self.assertEqual(res.status_code, 404)
      self.assertEqual(data['success'], False)
      self.assertEqual(data['message'], 'resource not found')

    # def test_update_book_rating():
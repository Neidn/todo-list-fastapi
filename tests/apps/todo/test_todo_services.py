######################################################################
#  T O D O   S E R V I C E S   T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods
import unittest
from unittest import mock

from src.apps.todo.services import *
from .todo_factories import TodoItemFactory, TodoCreateRequestFactory, TodoUpdateRequestFactory


class TestTodoServices(unittest.TestCase):
    """Test Cases for TodoServices"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        cls.n = 10
        pass

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""
        pass

    def setUp(self):
        """This runs before each test"""
        self.db = {}
        pass

    def tearDown(self):
        """This runs after each test"""
        pass

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################
    def test_get_new_todo_id(self):
        """Test get_new_todo_id"""
        # test get_new_todo_id
        todo_id = get_new_todo_id()

        # assert
        self.assertIsNotNone(todo_id)
        self.assertTrue(len(todo_id) > 0)

    def test_create_todo(self):
        """Test create TodoItem"""
        # create fake TodoCreateRequestFactory
        todo_create_request = TodoCreateRequestFactory()

        # test create_todo
        new_todo = create_todo(self.db, todo_create_request)

        # assert
        self.assertEqual(new_todo.title, todo_create_request.title)
        self.assertEqual(new_todo.content, todo_create_request.content)
        self.assertEqual(new_todo.is_done, todo_create_request.is_done)

    def test_get_todo(self):
        """Test get TodoItem"""
        # create fake TodoItem
        todo = TodoItemFactory()
        self.db[todo.id] = todo

        # test get_todo
        todo = get_todo(self.db, todo.id)

        # assert
        self.assertIsNotNone(todo)
        self.assertEqual(todo.id, todo.id)
        self.assertEqual(todo.title, todo.title)
        self.assertEqual(todo.content, todo.content)
        self.assertEqual(todo.is_done, todo.is_done)
        self.assertEqual(todo.created_at, todo.created_at)
        self.assertEqual(todo.updated_at, todo.updated_at)

    def test_get_all(self):
        """Test get all TodoItems"""
        # create fake TodoItem
        for _ in range(self.n):
            todo = TodoItemFactory()
            self.db[todo.id] = todo

        # test get_all
        todos = get_all()

        # assert
        self.assertEqual(len(todos), self.n)

    def test_update_todo(self):
        """Test update TodoItem"""
        # create fake TodoItem
        todo = TodoItemFactory()
        self.db[todo.id] = todo

        # create fake TodoUpdateRequest
        todo_update_request = TodoUpdateRequestFactory()

        # assert
        # set time.sleep to 1 second
        # assert updated_at is not equal to previous updated_at
        with mock.patch('time.sleep', return_value=1):
            # test update_todo
            updated_todo = update_todo(self.db, todo.id, todo, todo_update_request)
            self.assertEqual(updated_todo.title, todo_update_request.title)
            self.assertEqual(updated_todo.content, todo_update_request.content)
            self.assertEqual(updated_todo.is_done, todo_update_request.is_done)
            self.assertEqual(updated_todo.created_at, todo.created_at)

    def test_delete_todo(self):
        """Test delete TodoItem"""
        # create fake TodoItem
        todo = TodoItemFactory()
        self.db[todo.id] = todo

        # test delete_todo
        delete_todo(self.db, todo.id)

        # assert
        self.assertEqual(len(self.db), 0)

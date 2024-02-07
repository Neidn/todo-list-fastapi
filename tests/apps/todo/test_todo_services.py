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
        self.db = mock.MagicMock()
        self.db.add.return_value = None
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
        new_todo = create_todo(
            db=self.db,
            todo=todo_create_request,
        )

        # assert
        self.assertEqual(new_todo.title, todo_create_request.title)
        self.assertEqual(new_todo.content, todo_create_request.content)
        self.assertEqual(new_todo.is_done, todo_create_request.is_done)

    def test_get_todo(self):
        """Test get TodoItem"""
        # create fake TodoItem
        todo = TodoItemFactory()

        new_todo = create_todo(
            db=self.db,
            todo=todo,
        )

        self.db.query.return_value.filter_by.return_value.first.return_value = new_todo

        # test get_todo
        todo = get_todo(
            db=self.db,
            todo_id=todo.id
        )

        # assert
        self.assertIsNotNone(todo)
        self.assertEqual(todo.title, new_todo.title)
        self.assertEqual(todo.content, new_todo.content)
        self.assertEqual(todo.is_done, new_todo.is_done)

    def test_get_all(self):
        """Test get all TodoItems"""
        # create fake TodoItem
        n = 10

        tmp = []

        for _ in range(n):
            # create fake TodoItem
            todo = TodoItemFactory()
            # test create_todo
            todo = create_todo(
                db=self.db,
                todo=todo,
            )
            tmp.append(todo)

        self.db.query.return_value.all.return_value = tmp

        # test get_all
        todos = get_all(
            db=self.db
        )

        # assert
        self.assertEqual(len(todos), n)

    def test_update_todo(self):
        """Test update TodoItem"""
        self.db.query.return_value.filter_by.return_value.update.return_value = 1

        # create fake TodoItem
        todo = TodoItemFactory()
        # test create_todo
        todo = create_todo(
            db=self.db,
            todo=todo,
        )

        # create fake TodoUpdateRequest
        todo_update_request = TodoUpdateRequestFactory()

        # assert
        # set time.sleep to 1 second
        # assert updated_at is not equal to previous updated_at
        with mock.patch('time.sleep', return_value=1):
            # test update_todo
            result = update_todo(
                db=self.db,
                todo_id=todo.id,
                todo_update_request=todo_update_request,
            )
            self.assertEqual(result, 1)

    def test_delete_todo(self):
        """Test delete TodoItem"""
        # create fake TodoItem
        todo = TodoItemFactory()

        # test create_todo
        todo = create_todo(
            db=self.db,
            todo=todo,
        )

        # test delete_todo
        delete_todo(
            db=self.db,
            todo_id=todo.id
        )

        # get all
        todos = get_all(
            db=self.db
        )

        # assert
        self.assertEqual(len(todos), 0)

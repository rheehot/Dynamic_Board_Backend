from django.test import TestCase
from django.db import IntegrityError
from boards.models import Board
from users.models import User
from common.models import Permission


class BoardModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Run only once when running BoardModelTest

        User Fields :
            id       : 1
            username : test_user_1

        Board Fields :
            name        : test
            path        : test
            create_user : test_user_1
        """
        user = User.objects.create_user(username="test_user_1")
        Board.objects.create(name="test", path="test", create_user=user)

    def setUp(self):
        """Run every test function

        User Fields :
            id         : 2
            username   : test_user_2

        Board Fields :
            name        : test2
            path        : test2
            create_user : test_user_2
        """
        user = User.objects.create_user(username="test_user_2")
        Board.objects.create(
            name="test2",
            path="test2",
            write_permission=Permission.STAFF,
            create_user=user,
        )

    def test_board_create_success(self):
        """Board model creation success test
        Check board's fields and instance's class name
        """
        board = Board.objects.get(name="test2")

        self.assertEqual("test2", board.name)
        self.assertEqual("test2", board.path)
        self.assertEqual(Permission.STAFF, board.write_permission)
        self.assertEqual("Board", board.__class__.__name__)

    def test_board_create_fail(self):
        """Board model creation failure test
        Duplicate path with IntegrityError exception
        """
        with self.assertRaises(IntegrityError):
            user = User.objects.get(id=1)
            Board.objects.create(name="test", path="test", create_user=user)

    def test_board_primary_key(self):
        """Board model primary key test
        Check board object's primary key is path
        """
        board = Board.objects.get(name="test2")
        self.assertEqual(board.pk, board.path)

    def test_board_write_permission_default(self):
        """Board model write_permission field default test
        Check test's write_permission is Permission.NORMAL
        """
        board = Board.objects.get(name="test")
        self.assertEqual(Permission.NORMAL, board.write_permission)

    def test_user_permission_set(self):
        """Board model write_permission field set test
        Check test2's write_permission is Permission.STAFF
        """
        board = Board.objects.get(name="test2")
        self.assertEqual(Permission.STAFF, board.write_permission)

    def test_board_str_method(self):
        """Board model __str__ method test
        Check str method return board's name
        """
        board = Board.objects.get(name="test")
        self.assertEqual(board.name, str(board))

    def test_board_save_method(self):
        """Board model save method test
        Check save method remove special character in path
        """
        board = Board.objects.get(name="test")

        board.path = "/test--?!'/"
        board.save()

        self.assertEqual(board.path, "test")

    def test_create_user_related_name(self):
        """Board model create_user field related_name test
        Check user access board objects using related_name
        """
        board = Board.objects.get(name="test")

        user = User.objects.get(id=1)
        user_board = user.boards.get(name="test")

        self.assertEqual(board, user_board)

    def test_create_user_on_delete(self):
        """Board model create_user field on_delete test
        Check remove cascade when user removed
        """
        user = User.objects.get(id=2)
        user.delete()

        with self.assertRaises(Board.DoesNotExist):
            Board.objects.get(name="test2")

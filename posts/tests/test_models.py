from django.test import TestCase
from django.db import IntegrityError
from common.models import Permission
from users.models import User
from boards.models import Board
from posts.models import Post, VotedPost


class PostModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Run only once when running PostModelTest

        User Fields :
            id       : 1
            username : test_user_1

        Board Fields :
            name        : test
            path        : test
            create_user : test_user_1

        Post Fields :
            create_user : test_user_1
            board       : test
            title       : test title
            content     : test content
        """
        user = User.objects.create_user(username="test_user_1")
        board = Board.objects.create(name="test", path="test", create_user=user)
        Post.objects.create(
            create_user=user, board=board, title="test title", content="test content"
        )

    def test_post_create_success(self):
        """Post model creation success test
        Check post's fields and instance's class name
        """
        post = Post.objects.get(title="test title")
        user = User.objects.get(username="test_user_1")
        board = Board.objects.get(name="test")

        self.assertEqual("test title", post.title)
        self.assertEqual("test content", post.content)
        self.assertEqual(user, post.create_user)
        self.assertEqual(board, post.board)
        self.assertEqual("Post", post.__class__.__name__)

    def test_post_upvote_default(self):
        """Post model upvote field default test
        Check post's upvote field is zero
        """
        post = Post.objects.get(title="test title")
        self.assertEqual(0, post.upvote)

    def test_post_downvote_default(self):
        """Post model downvote field default test
        Check post's downvote field is zero
        """
        post = Post.objects.get(title="test title")
        self.assertEqual(0, post.downvote)

    def test_post_str_method(self):
        """Post model downvote __str__ method test
        Check post's str method return post's title
        """
        post = Post.objects.get(title="test title")
        self.assertEqual(str(post), post.title)

    def test_post_voted_post(self):
        """Post model voted_post field test
        Check post's voted_post field's length is zero
        """
        post = Post.objects.get(title="test title")
        self.assertEqual(0, len(post.voted_post.all()))


class VotedPostModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Run only once when running VotedPostModelTest

        User Fields :
            id       : 1
            username : test_user_1

        Board Fields :
            name        : test
            path        : test
            create_user : test_user_1

        Post Fields :
            create_user : test_user_1
            board       : test
            title       : test title
            content     : test content

        VotedPost Fields :
            user       : test_user_1
            post       : test
            is_upvoted : true
        """
        user = User.objects.create_user(username="test_user_1")
        board = Board.objects.create(name="test", path="test", create_user=user)
        post = Post.objects.create(
            create_user=user, board=board, title="test title", content="test content"
        )
        VotedPost.objects.create(user=user, post=post)

    def test_voted_post_create_success(self):
        """VotedPost model creation success test
        Check voted post's fields and instance's class name
        """
        post = Post.objects.get(title="test title")
        user = User.objects.get(username="test_user_1")
        voted_post = VotedPost.objects.get(post=post, user=user)

        self.assertEqual(user, voted_post.user)
        self.assertEqual(post, voted_post.post)
        self.assertTrue(voted_post.is_upvoted)
        self.assertEqual("VotedPost", voted_post.__class__.__name__)

    def test_voted_post_create_fail(self):
        """VotedPost model creation fail test
        Duplicate post and user with IntegrityError exception
        """
        with self.assertRaises(IntegrityError):
            post = Post.objects.get(title="test title")
            user = User.objects.get(username="test_user_1")
            VotedPost.objects.create(post=post, user=user)

    def test_voted_post_str_method(self):
        """VotedPost model __str__ method test
        Check VotedPost model's str method equal to expected_value
        """
        post = Post.objects.get(title="test title")
        user = User.objects.get(username="test_user_1")
        voted_post = VotedPost.objects.get(post=post, user=user)
        expected_value = "USER(test_user_1) / POST(test title) / BOARD(test) -> upvoted"
        self.assertEqual(str(voted_post), expected_value)

    def test_voted_post_save_method(self):
        """VotedPost model save method test
        Check increase Post object's upvote or downvote field
        """
        user = User.objects.create_user(username="test_user_2")
        post = Post.objects.get(title="test title")

        VotedPost.objects.create(user=user, post=post, is_upvoted=False)

        self.assertEqual(1, post.downvote)

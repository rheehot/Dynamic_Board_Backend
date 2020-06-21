from django.test import TestCase
from django.db import IntegrityError
from common.models import Permission
from users.models import User
from boards.models import Board
from posts.models import Post, PostVotedUser


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

    def test_post_post_voted_user(self):
        """Post model post_voted_user field test
        Check post's post_voted_user field's length is zero
        """
        post = Post.objects.get(title="test title")
        self.assertEqual(0, len(post.post_voted_user.all()))


class PostVotedUserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Run only once when running PostVotedUserModelTest

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

        PostVotedUser Fields :
            user       : test_user_1
            post       : test
            is_upvoted : true
        """
        user = User.objects.create_user(username="test_user_1")
        board = Board.objects.create(name="test", path="test", create_user=user)
        post = Post.objects.create(
            create_user=user, board=board, title="test title", content="test content"
        )
        PostVotedUser.objects.create(user=user, post=post)

    def test_post_voted_user_create_success(self):
        """PostVotedUser model creation success test
        Check voted post's fields and instance's class name
        """
        post = Post.objects.get(title="test title")
        user = User.objects.get(username="test_user_1")
        post_voted_user = PostVotedUser.objects.get(post=post, user=user)

        self.assertEqual(user, post_voted_user.user)
        self.assertEqual(post, post_voted_user.post)
        self.assertTrue(post_voted_user.is_upvoted)
        self.assertEqual("PostVotedUser", post_voted_user.__class__.__name__)

    def test_post_voted_user_create_fail(self):
        """PostVotedUser model creation fail test
        Duplicate post and user with IntegrityError exception
        """
        with self.assertRaises(IntegrityError):
            post = Post.objects.get(title="test title")
            user = User.objects.get(username="test_user_1")
            PostVotedUser.objects.create(post=post, user=user)

    def test_post_voted_user_str_method(self):
        """PostVotedUser model __str__ method test
        Check PostVotedUser model's str method equal to expected_value
        """
        post = Post.objects.get(title="test title")
        user = User.objects.get(username="test_user_1")
        post_voted_user = PostVotedUser.objects.get(post=post, user=user)
        expected_value = "USER(test_user_1) / POST(test title) / BOARD(test) -> upvoted"
        self.assertEqual(str(post_voted_user), expected_value)

    def test_post_voted_user_save_method(self):
        """PostVotedUser model save method test
        Check increase Post object's upvote or downvote field
        """
        user = User.objects.create_user(username="test_user_2")
        post = Post.objects.get(title="test title")

        PostVotedUser.objects.create(user=user, post=post, is_upvoted=False)

        self.assertEqual(1, post.downvote)

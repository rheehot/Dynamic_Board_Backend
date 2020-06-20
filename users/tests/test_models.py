from django.test import TestCase
from django.db import IntegrityError
from users.models import User
from tempfile import NamedTemporaryFile


class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Run only once when running UserModelTest
        Only set username field

        Fields :
            id       : 1
            username : test_user_1
        """
        User.objects.create_user(username="test_user_1")

    def setUp(self):
        """Run every test function
        Setting all fields except avatar field

        Fields :
            id         : 2
            username   : test_user_2
            bio        : test bio
            permission : User.STAFF
        """
        User.objects.create_user(
            username="test_user_2", bio="test bio", permission=User.STAFF
        )

    def test_user_create_success(self):
        """User model creation success test
        Check username field and instance's class name
        """
        user = User.objects.get(username="test_user_2")
        self.assertEqual("test_user_2", user.username)
        self.assertEqual("User", user.__class__.__name__)

    def test_user_create_fail(self):
        """User model creation failure test
        Duplicate username with IntegrityError exception
        """
        with self.assertRaises(IntegrityError):
            User.objects.create_user("test_user_1")

    def test_user_permission_default(self):
        """User model permission field default test
        Check test_user_1's permission is NORMAL
        """
        user = User.objects.get(username="test_user_1")
        self.assertEqual(User.NORMAL, user.permission)

    def test_user_permission_set(self):
        user = User.objects.get(username="test_user_2")
        self.assertEqual(User.STAFF, user.permission)

    def test_user_bio_default(self):
        """User model bio field default value test
        Check test_user_1's bio is ""
        """
        user = User.objects.get(username="test_user_1")
        self.assertEqual("", user.bio)

    def test_user_bio_set(self):
        """User model bio field set value test
        Check test_user_2's bio is "test bio"
        """
        user = User.objects.get(username="test_user_2")
        self.assertEqual("test bio", user.bio)

    def test_user_avatar_default(self):
        """User model avatar field default test
        Check test_user_1's avatar set default image
        """
        user = User.objects.get(username="test_user_1")
        self.assertEqual(user.avatar.url, "/media/default_avatar.png")

    def test_user_avatar_set(self):
        """User model avatar field set file test
        Check test_user_2's avatar equal test_image_file
        test_image_file is a temporary file with the jpg extension
        """
        user = User.objects.get(username="test_user_2")

        test_image_file = NamedTemporaryFile(suffix=".jpg").name
        user.avatar = test_image_file
        user.save()

        self.assertEqual(user.avatar, test_image_file)

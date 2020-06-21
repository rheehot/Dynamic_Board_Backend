from django.db import models
from common.models import AbstractTimeStamp


class Post(AbstractTimeStamp):
    """Post Model
    Inherit:
        AbstractTimeStamp
    Fields:
        create_user : User model (1:N)
        board       : Board model (1:N)
        voted_post  : VotedPost model (M:N)
        title       : CharField
        content     : TextField
        upvote      : PositiveIntegerField
        downvote    : PositiveIntegerField
    Methods:
        __str__     : Return post's title
    Meta :
        db_table    : posts
    """

    create_user = models.ForeignKey(
        "users.User", related_name="users", on_delete=models.CASCADE
    )
    board = models.ForeignKey(
        "boards.Board", related_name="posts", on_delete=models.CASCADE
    )
    post_voted_user = models.ManyToManyField("users.User", through="PostVotedUser")
    title = models.CharField(max_length=100)
    content = models.TextField()
    upvote = models.PositiveIntegerField(default=0)
    downvote = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "posts"


class PostVotedUser(AbstractTimeStamp):
    """User Voted Post Model
    Inherit:
        AbstractTimeStamp
    Fields:
        user            : User model (1:N)
        post            : Post model (1:N)
        is_upvoted      : BooleanField
    Methods:
        __str__         : Return voted post's info
        save            : Update post object according to is_upvoted
    Meta:
        unique_together : user, post
        db_table        : voted_posts
    """

    user = models.ForeignKey(
        "users.User", related_name="vote_users", on_delete=models.CASCADE
    )
    post = models.ForeignKey(
        "posts.Post", related_name="vote_posts", on_delete=models.CASCADE
    )
    is_upvoted = models.BooleanField(default=True)

    def __str__(self):
        user = f"USER({self.user})"
        post = f"POST({self.post})"
        board = f"BOARD({self.post.board})"
        stat = f"{'up' if self.is_upvoted else 'down'}voted"

        return f"{user} / {post} / {board} -> {stat}"

    def save(self, *args, **kwargs):
        if self.is_upvoted:
            self.post.upvote = models.F("upvote") + 1
        else:
            self.post.downvote = models.F("downvote") + 1

        self.post.save()
        super().save(*args, **kwargs)

    class Meta:
        unique_together = (("user", "post"),)
        db_table = "voted_posts"

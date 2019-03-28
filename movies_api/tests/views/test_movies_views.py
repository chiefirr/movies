from rest_framework.test import APITestCase


class CommentTest(APITestCase):

    def setUp(self):

        self.comment_text = "Some test text."

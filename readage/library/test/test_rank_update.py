from library.models import Rank
from django.test import TestCase

class SimpleTest(TestCase):

    def test_rank_update(self):
       Rank.update()

import unittest

from tasks.tasks import add


class TestCelery(unittest.TestCase):
    def test_celery(self):
        add.delay(1, 2)

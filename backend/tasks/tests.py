from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from datetime import date, timedelta
from tasks.scoring import balanced_score

class ScoringTests(TestCase):

    def test_importance_matters(self):
        t1 = {"title": "A", "importance": 10}
        t2 = {"title": "B", "importance": 1}

        s1, _ = balanced_score(t1, [])
        s2, _ = balanced_score(t2, [])

        self.assertTrue(s1 > s2)

    def test_overdue_is_high_priority(self):
        past = date.today() - timedelta(days=2)
        task = {"title": "A", "importance": 5, "due_date": past}
        score, _ = balanced_score(task, [])
        self.assertTrue(score > 30)

    def test_low_effort_bonus(self):
        t1 = {"title": "A", "importance": 5, "estimated_hours": 1}
        t2 = {"title": "B", "importance": 5, "estimated_hours": 10}

        s1, _ = balanced_score(t1, [])
        s2, _ = balanced_score(t2, [])

        self.assertTrue(s1 > s2)
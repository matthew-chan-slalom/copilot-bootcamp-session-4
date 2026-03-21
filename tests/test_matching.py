import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from app import get_recommendations  # noqa: E402


class TeamMatchingTests(unittest.TestCase):
    def test_returns_ranked_recommendations(self):
        recommendations = get_recommendations("Cloud Architecture", top_n=5)

        self.assertGreaterEqual(len(recommendations), 1)
        scores = [item["score"] for item in recommendations]
        self.assertEqual(scores, sorted(scores, reverse=True))

    def test_excludes_already_registered_consultants(self):
        recommendations = get_recommendations("Cloud Architecture", top_n=20)
        existing_team = {"alice.smith@slalom.com", "bob.johnson@slalom.com"}

        for item in recommendations:
            self.assertNotIn(item["email"], existing_team)

    def test_limits_number_of_results(self):
        recommendations = get_recommendations("Data Analytics", top_n=3)
        self.assertEqual(len(recommendations), 3)

    def test_explainability_fields_present(self):
        recommendation = get_recommendations("DevOps Engineering", top_n=1)[0]
        explainability = recommendation["explainability"]

        self.assertIn("skill_level", explainability)
        self.assertIn("certifications", explainability)
        self.assertIn("availability", explainability)
        self.assertIn("practice_area", explainability)
        self.assertIn("industry_overlap", explainability)


if __name__ == "__main__":
    unittest.main()

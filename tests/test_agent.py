import unittest

from agent import analyze, extract_skills, format_report


class AgentTests(unittest.TestCase):
    def test_extracts_aliases_and_common_terms(self):
        self.assertEqual(
            extract_skills("Built software with Python, FastAPI, React.js, and PostgreSQL"),
            {"python", "fastapi", "react", "postgresql"},
        )

    def test_weighted_score_and_required_priority(self):
        resume = "I use Python and SQL for data analysis."
        job = "Required: Python and SQL. Preferred: AWS."
        report = analyze(resume, job)
        self.assertEqual(report.score, 80)
        self.assertEqual(report.required_count, 2)
        self.assertEqual(report.required_matched_count, 2)
        self.assertIn("aws", report.missing_skills)

    def test_evidence_is_attached_to_each_detected_match(self):
        report = analyze("Built data analysis dashboards with Python.", "Required Python and data analysis.")
        self.assertTrue(report.evidence["python"])
        self.assertTrue(report.evidence["data analysis"])
        self.assertIn("Built data analysis dashboards with Python.", report.evidence["python"])

    def test_unknown_job_skills_do_not_create_fake_score(self):
        report = analyze("I work with Python.", "Need experience with quantum widgets and interplanetary logistics.")
        self.assertEqual(report.score, 0)
        self.assertEqual(report.job_skill_count, 0)
        self.assertTrue(any("No skills" in item for item in report.recommendations))

    def test_requires_both_inputs(self):
        with self.assertRaises(ValueError):
            analyze("", "Need Python")

    def test_report_has_explicit_limitations(self):
        report = analyze("Python developer with FastAPI experience.", "Required Python, FastAPI.")
        rendered = format_report(report)
        self.assertIn("not an ATS score", rendered)
        self.assertIn("Python", rendered)


if __name__ == "__main__":
    unittest.main()

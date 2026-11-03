import unittest

from analyze_github import _validate_repository_page


class RepositoryPayloadValidationTests(unittest.TestCase):
    def test_accepts_valid_repository_records(self):
        records = [
            {"stargazers_count": 12, "fork": False, "language": "Python"},
            {"stargazers_count": 0, "fork": True, "language": None},
        ]
        self.assertEqual(_validate_repository_page(records, 1), records)

    def test_rejects_non_array_page_payloads(self):
        with self.assertRaisesRegex(ValueError, "JSON array"):
            _validate_repository_page({"name": "repo"}, 2)

    def test_rejects_non_object_repository_records(self):
        with self.assertRaisesRegex(ValueError, "JSON object"):
            _validate_repository_page([None], 1)

    def test_rejects_invalid_star_counts(self):
        for stars in (-1, "4", True, 1.5):
            with self.subTest(stars=stars):
                with self.assertRaisesRegex(ValueError, "stargazers_count"):
                    _validate_repository_page([{"stargazers_count": stars}], 1)

    def test_rejects_invalid_fork_and_language_fields(self):
        with self.assertRaisesRegex(ValueError, "fork flag"):
            _validate_repository_page([{"fork": "false"}], 1)
        with self.assertRaisesRegex(ValueError, "language"):
            _validate_repository_page([{"language": 123}], 1)


if __name__ == "__main__":
    unittest.main()

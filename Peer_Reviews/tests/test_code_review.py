import unittest
from code_review_app import create_workflow
from utils.code_parser import CodeParser

class TestCodeReview(unittest.TestCase):
    def setUp(self):
        self.app = create_workflow()
        self.test_code = """
        def add_numbers(a, b):
            return a + b  # No type hints or input validation
        
        def process_data(data):
            result = []
            for item in data:
                result.append(item * 2)
            return result  # No error handling
        """

    def test_code_review_workflow(self):
        initial_state = {
            "code": self.test_code,
            "review_comments": [],
            "severity_levels": [],
            "final_summary": "",
            "current_step": "start"
        }
        
        result = self.app.invoke(initial_state)
        
        # Assert that all steps were completed
        self.assertIsNotNone(result["review_comments"])
        self.assertIsNotNone(result["severity_levels"])
        self.assertIsNotNone(result["final_summary"])
        self.assertEqual(result["current_step"], "summary")

    def test_code_parser(self):
        parser = CodeParser()
        tree = parser.parse_python_code(self.test_code)
        functions = parser.extract_functions(tree)
        
        self.assertEqual(len(functions), 2)
        self.assertIn("add_numbers", [f["name"] for f in functions])
        self.assertIn("process_data", [f["name"] for f in functions])

if __name__ == "__main__":
    unittest.main() 
import ast
from typing import List, Dict

class CodeParser:
    @staticmethod
    def parse_python_code(code: str) -> ast.AST:
        try:
            return ast.parse(code)
        except SyntaxError as e:
            raise ValueError(f"Invalid Python code: {str(e)}")

    @staticmethod
    def extract_functions(tree: ast.AST) -> List[Dict]:
        functions = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                functions.append({
                    "name": node.name,
                    "lineno": node.lineno,
                    "code": ast.unparse(node)
                })
        return functions

    @staticmethod
    def analyze_complexity(tree: ast.AST) -> Dict:
        complexity = {
            "num_functions": 0,
            "num_classes": 0,
            "num_imports": 0
        }
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                complexity["num_functions"] += 1
            elif isinstance(node, ast.ClassDef):
                complexity["num_classes"] += 1
            elif isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
                complexity["num_imports"] += 1
                
        return complexity 
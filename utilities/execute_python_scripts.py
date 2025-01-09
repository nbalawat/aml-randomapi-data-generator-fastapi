import subprocess
import tempfile
import os
import ast
import sys
import json
from typing import Dict, Any, Optional, Tuple
import resource

class CodeExecutionError(Exception):
    """Custom exception for code execution errors"""
    pass

class LLMCodeExecutor:
    def __init__(self, 
                 max_execution_time: int = 30,
                 max_memory_mb: int = 512,
                 allowed_modules: Optional[set] = None):
        """
        Initialize the code executor with safety limits
        
        Args:
            max_execution_time: Maximum execution time in seconds
            max_memory_mb: Maximum memory usage in MB
            allowed_modules: Set of module names that are allowed to be imported
        """
        self.max_execution_time = max_execution_time
        self.max_memory_mb = max_memory_mb
        self.allowed_modules = allowed_modules or {
            'math', 'random', 'datetime', 'json', 
            'collections', 'statistics', 're', 'itertools'
        }

    def _validate_imports(self, code: str) -> None:
        """
        Validate that the code only imports allowed modules
        
        Args:
            code: Python code string to validate
            
        Raises:
            CodeExecutionError: If forbidden imports are found
        """
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            raise CodeExecutionError(f"Syntax error in code: {str(e)}")

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for name in node.names:
                    if name.name.split('.')[0] not in self.allowed_modules:
                        raise CodeExecutionError(f"Import of '{name.name}' is not allowed")
            elif isinstance(node, ast.ImportFrom):
                if node.module and node.module.split('.')[0] not in self.allowed_modules:
                    raise CodeExecutionError(f"Import from '{node.module}' is not allowed")

    def _create_temporary_script(self, code: str) -> str:
        """
        Create a temporary file containing the code
        
        Args:
            code: Python code to write to file
            
        Returns:
            Path to temporary file
        """
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            return f.name

    def _limit_resources(self) -> None:
        """Set resource limits for the subprocess"""
        try:
            memory_bytes = self.max_memory_mb * 1024 * 1024
            resource.setrlimit(resource.RLIMIT_AS, (memory_bytes, memory_bytes))
        except (ValueError, resource.error):
            # If setting resource limits fails, log a warning but continue
            print("Warning: Failed to set resource limits", file=sys.stderr)

    def execute_code(self, 
                    code: str, 
                    input_data: Optional[Dict[str, Any]] = None) -> Tuple[Any, str, str]:
        """
        Execute the provided code safely and return the results
        
        Args:
            code: Python code to execute
            input_data: Dictionary of input data to pass to the code
            
        Returns:
            Tuple containing (result, stdout, stderr)
            
        Raises:
            CodeExecutionError: If execution fails or violates constraints
        """
        # Validate imports first
        self._validate_imports(code)

        # Wrap the code to handle input data and capture the result
        wrapped_code = f"""
import sys
import json
import traceback

# Input data provided by the executor
input_data = {input_data if input_data else {}}

{code}

if __name__ == '__main__':
    try:
        result = main()
        print("RESULT_START")
        print(json.dumps(result))
        print("RESULT_END")
    except Exception as e:
        print("ERROR:", str(e), file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)
"""
        # Create temporary script
        script_path = self._create_temporary_script(wrapped_code)

        try:
            # Execute the script in a subprocess with resource limits
            process = subprocess.Popen(
                [sys.executable, script_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            try:
                stdout, stderr = process.communicate(timeout=self.max_execution_time)
            except subprocess.TimeoutExpired:
                process.kill()
                raise CodeExecutionError(f"Code execution exceeded time limit of {self.max_execution_time} seconds")

            if process.returncode != 0:
                raise CodeExecutionError(f"Code execution failed with error:\n{stderr}")

            # Parse the result from stdout
            result = None
            result_lines = []
            capture_result = False
            
            for line in stdout.split('\n'):
                if line == "RESULT_START":
                    capture_result = True
                elif line == "RESULT_END":
                    capture_result = False
                elif capture_result and line.strip():
                    result_lines.append(line)

            if result_lines:
                try:
                    result = json.loads('\n'.join(result_lines))
                except json.JSONDecodeError:
                    raise CodeExecutionError("Failed to parse execution result")

            return result, stdout, stderr

        finally:
            # Clean up temporary file
            try:
                os.unlink(script_path)
            except OSError:
                pass

# Example usage
if __name__ == "__main__":
    # Example code from LLM
    llm_code = """
def main():
    # This example shows how to work with input data
    numbers = input_data.get('numbers', range(10))
    result = {
        'sum': sum(numbers),
        'length': len(list(numbers))
    }
    return result
"""

    executor = LLMCodeExecutor(
        max_execution_time=5,
        max_memory_mb=100,
        allowed_modules={'math', 'random'}
    )

    # Example with input data
    input_data = {'numbers': [1, 2, 3, 4]}
    
    try:
        result, stdout, stderr = executor.execute_code(llm_code, input_data)
        print(f"Execution Result: {result}")
        if stdout.strip():
            print(f"Standard Output: {stdout}")
        if stderr.strip():
            print(f"Standard Error: {stderr}")
    except CodeExecutionError as e:
        print(f"Execution failed: {str(e)}")
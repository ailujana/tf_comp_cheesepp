import sys
import os
import traceback
import time
from typing import List, Dict, Any, Optional, Callable, Tuple
from dataclasses import dataclass
from enum import Enum
from io import StringIO
from contextlib import contextmanager

# Import compiler components
from .parser import parse
from .runtime import Runtime
from .ast import *
from .errors import CheeseError, ParseError, RuntimeError as CheeseRuntimeError


class TestResult(Enum):
    """Enumeration of test results"""
    PASSED = "PASSED"
    FAILED = "FAILED"
    ERROR = "ERROR"
    SKIPPED = "SKIPPED"


@dataclass
class TestCase:
    """Represents a single test case"""
    name: str
    description: str
    input_code: str
    expected_output: Optional[str] = None
    expected_error: Optional[str] = None
    should_fail: bool = False
    timeout: float = 5.0
    
    def __post_init__(self):
        if self.expected_output is None and self.expected_error is None and not self.should_fail:
            raise ValueError("Test case must have expected output, expected error, or should_fail=True")


@dataclass
class TestResult:
    """Represents the result of a test case execution"""
    test_case: TestCase
    result: TestResult
    actual_output: str
    actual_error: Optional[str]
    execution_time: float
    message: str
    
    def __str__(self):
        status_symbol = {
            TestResult.PASSED: "✓",
            TestResult.FAILED: "✗",
            TestResult.ERROR: "!",
            TestResult.SKIPPED: "-"
        }
        
        symbol = status_symbol.get(self.result, "?")
        return f"{symbol} {self.test_case.name}: {self.message} ({self.execution_time:.3f}s)"


class TestRunner:
    """
    Main test runner for Cheese++ compiler tests.
    
    Provides functionality to run individual tests, test suites, and generate reports.
    """
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.results: List[TestResult] = []
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
        self.error_tests = 0
        self.skipped_tests = 0
    
    def run_test(self, test_case: TestCase) -> TestResult:
        """Run a single test case"""
        start_time = time.time()
        
        try:
            # Capture output
            with self._capture_output() as output:
                if test_case.should_fail:
                    # Test should fail - expect an exception
                    try:
                        self._execute_code(test_case.input_code)
                        # If we get here, test failed (should have thrown exception)
                        result = TestResult(
                            test_case=test_case,
                            result=TestResult.FAILED,
                            actual_output=output.getvalue(),
                            actual_error=None,
                            execution_time=time.time() - start_time,
                            message="Expected failure but code executed successfully"
                        )
                    except Exception as e:
                        # Expected failure occurred
                        if test_case.expected_error and test_case.expected_error in str(e):
                            result = TestResult(
                                test_case=test_case,
                                result=TestResult.PASSED,
                                actual_output=output.getvalue(),
                                actual_error=str(e),
                                execution_time=time.time() - start_time,
                                message="Expected failure occurred"
                            )
                        else:
                            result = TestResult(
                                test_case=test_case,
                                result=TestResult.FAILED,
                                actual_output=output.getvalue(),
                                actual_error=str(e),
                                execution_time=time.time() - start_time,
                                message=f"Wrong error type: {str(e)}"
                            )
                else:
                    # Normal test execution
                    try:
                        self._execute_code(test_case.input_code)
                        actual_output = output.getvalue().strip()
                        
                        if test_case.expected_output is not None:
                            if actual_output == test_case.expected_output.strip():
                                result = TestResult(
                                    test_case=test_case,
                                    result=TestResult.PASSED,
                                    actual_output=actual_output,
                                    actual_error=None,
                                    execution_time=time.time() - start_time,
                                    message="Output matches expected"
                                )
                            else:
                                result = TestResult(
                                    test_case=test_case,
                                    result=TestResult.FAILED,
                                    actual_output=actual_output,
                                    actual_error=None,
                                    execution_time=time.time() - start_time,
                                    message=f"Expected '{test_case.expected_output}', got '{actual_output}'"
                                )
                        else:
                            result = TestResult(
                                test_case=test_case,
                                result=TestResult.PASSED,
                                actual_output=actual_output,
                                actual_error=None,
                                execution_time=time.time() - start_time,
                                message="Executed without error"
                            )
                    
                    except Exception as e:
                        if test_case.expected_error and test_case.expected_error in str(e):
                            result = TestResult(
                                test_case=test_case,
                                result=TestResult.PASSED,
                                actual_output=output.getvalue(),
                                actual_error=str(e),
                                execution_time=time.time() - start_time,
                                message="Expected error occurred"
                            )
                        else:
                            result = TestResult(
                                test_case=test_case,
                                result=TestResult.ERROR,
                                actual_output=output.getvalue(),
                                actual_error=str(e),
                                execution_time=time.time() - start_time,
                                message=f"Unexpected error: {str(e)}"
                            )
        
        except Exception as e:
            # Unexpected error in test framework itself
            result = TestResult(
                test_case=test_case,
                result=TestResult.ERROR,
                actual_output="",
                actual_error=str(e),
                execution_time=time.time() - start_time,
                message=f"Test framework error: {str(e)}"
            )
        
        self.results.append(result)
        self._update_counters(result)
        
        if self.verbose:
            print(result)
        
        return result
    
    def run_tests(self, test_cases: List[TestCase]) -> List[TestResult]:
        """Run multiple test cases"""
        self.total_tests = len(test_cases)
        results = []
        
        print(f"Running {self.total_tests} tests...")
        print("-" * 50)
        
        for i, test_case in enumerate(test_cases, 1):
            if self.verbose:
                print(f"[{i}/{self.total_tests}] Running {test_case.name}...")
            
            result = self.run_test(test_case)
            results.append(result)
        
        self._print_summary()
        return results
    
    def _execute_code(self, code: str) -> None:
        """Execute Cheese++ code"""
        try:
            # Parse the code
            ast = parse(code)
            
            # Create runtime and execute
            runtime = Runtime()
            runtime.run(ast, code)
            
        except Exception as e:
            raise e
    
    @contextmanager
    def _capture_output(self):
        """Context manager to capture stdout"""
        old_stdout = sys.stdout
        sys.stdout = captured_output = StringIO()
        try:
            yield captured_output
        finally:
            sys.stdout = old_stdout
    
    def _update_counters(self, result: TestResult):
        """Update test counters"""
        if result.result == TestResult.PASSED:
            self.passed_tests += 1
        elif result.result == TestResult.FAILED:
            self.failed_tests += 1
        elif result.result == TestResult.ERROR:
            self.error_tests += 1
        elif result.result == TestResult.SKIPPED:
            self.skipped_tests += 1
    
    def _print_summary(self):
        """Print test summary"""
        print("-" * 50)
        print(f"Tests run: {self.total_tests}")
        print(f"Passed: {self.passed_tests}")
        print(f"Failed: {self.failed_tests}")
        print(f"Errors: {self.error_tests}")
        print(f"Skipped: {self.skipped_tests}")
        
        if self.failed_tests == 0 and self.error_tests == 0:
            print("✓ All tests passed!")
        else:
            print("✗ Some tests failed!")
            print("\nFailures and Errors:")
            for result in self.results:
                if result.result in [TestResult.FAILED, TestResult.ERROR]:
                    print(f"  - {result.test_case.name}: {result.message}")
                    if result.actual_error:
                        print(f"    Error: {result.actual_error}")


class TestBuilder:
    """
    Utility class for building test cases.
    
    Provides factory methods for creating common test patterns.
    """
    
    @staticmethod
    def create_output_test(name: str, code: str, expected_output: str, 
                          description: str = "") -> TestCase:
        """Create a test that checks output"""
        return TestCase(
            name=name,
            description=description,
            input_code=code,
            expected_output=expected_output
        )
    
    @staticmethod
    def create_error_test(name: str, code: str, expected_error: str,
                         description: str = "") -> TestCase:
        """Create a test that expects an error"""
        return TestCase(
            name=name,
            description=description,
            input_code=code,
            expected_error=expected_error,
            should_fail=True
        )
    
    @staticmethod
    def create_execution_test(name: str, code: str, description: str = "") -> TestCase:
        """Create a test that just checks if code executes without error"""
        return TestCase(
            name=name,
            description=description,
            input_code=code
        )


class IntegrationTestSuite:
    """
    Integration test suite for the Cheese++ compiler.
    
    Contains predefined test cases for various language features.
    """
    
    @staticmethod
    def basic_tests() -> List[TestCase]:
        """Basic functionality tests"""
        return [
            TestBuilder.create_output_test(
                "hello_world",
                """Cheese
                   Wensleydale(SwissHello WorldSwiss) Brie
                   NoCheese""",
                "Hello World",
                "Basic hello world test"
            ),
            
            TestBuilder.create_output_test(
                "simple_assignment",
                """Cheese
                   Glyn(x) = 42;
                   Wensleydale(Glyn(x)) Brie
                   NoCheese""",
                "42",
                "Simple variable assignment"
            ),
            
            TestBuilder.create_output_test(
                "arithmetic",
                """Cheese
                   Glyn(a) = 10;
                   Glyn(b) = 20;
                   Glyn(c) = a plus b;
                   Wensleydale(Glyn(c)) Brie
                   NoCheese""",
                "30",
                "Arithmetic operations"
            )
        ]
    
    @staticmethod
    def control_flow_tests() -> List[TestCase]:
        """Control flow tests"""
        return [
            TestBuilder.create_output_test(
                "conditional_true",
                """Cheese
                   Glyn(x) = 10;
                   Stilton Glyn(x) greater 5 Blue
                       Wensleydale(SwissGreater than 5Swiss) Brie
                   White
                       Wensleydale(SwissNot greater than 5Swiss) Brie
                   NoCheese""",
                "Greater than 5",
                "Conditional statement - true branch"
            ),
            
            TestBuilder.create_output_test(
                "loop_basic",
                """Cheese
                   Glyn(i) = 0;
                   Cheddar
                       Wensleydale(Glyn(i)) Brie
                       Glyn(i) = i plus 1;
                   Coleraine i minor 3
                   NoCheese""",
                "0\n1\n2",
                "Basic loop test"
            )
        ]
    
    @staticmethod
    def error_tests() -> List[TestCase]:
        """Error handling tests"""
        return [
            TestBuilder.create_error_test(
                "undefined_variable",
                """Cheese
                   Wensleydale(Glyn(undefined_var)) Brie
                   NoCheese""",
                "undefined",
                "Undefined variable error"
            ),
            
            TestBuilder.create_error_test(
                "syntax_error",
                """Cheese
                   Glyn(x) = 
                   NoCheese""",
                "syntax",
                "Syntax error test"
            )
        ]
    
    @staticmethod
    def all_tests() -> List[TestCase]:
        """All predefined tests"""
        return (IntegrationTestSuite.basic_tests() + 
                IntegrationTestSuite.control_flow_tests() +
                IntegrationTestSuite.error_tests())


class PerformanceTestSuite:
    """
    Performance test suite for the Cheese++ compiler.
    
    Tests performance characteristics of the compiler.
    """
    
    @staticmethod
    def create_performance_test(name: str, code: str, max_time: float) -> TestCase:
        """Create a performance test case"""
        test_case = TestCase(
            name=name,
            description=f"Performance test - should complete in under {max_time}s",
            input_code=code,
            timeout=max_time
        )
        return test_case
    
    @staticmethod
    def parsing_performance_tests() -> List[TestCase]:
        """Tests for parsing performance"""
        large_program = """Cheese
        """ + "\n".join([f"Glyn(var{i}) = {i};" for i in range(1000)]) + """
        NoCheese"""
        
        return [
            PerformanceTestSuite.create_performance_test(
                "large_program_parsing",
                large_program,
                1.0
            )
        ]


def run_integration_tests(verbose: bool = False) -> bool:
    """Run all integration tests"""
    runner = TestRunner(verbose=verbose)
    test_cases = IntegrationTestSuite.all_tests()
    results = runner.run_tests(test_cases)
    
    return runner.failed_tests == 0 and runner.error_tests == 0


def run_performance_tests(verbose: bool = False) -> bool:
    """Run performance tests"""
    runner = TestRunner(verbose=verbose)
    test_cases = PerformanceTestSuite.parsing_performance_tests()
    results = runner.run_tests(test_cases)
    
    return runner.failed_tests == 0 and runner.error_tests == 0


def run_all_tests(verbose: bool = False) -> bool:
    """Run all tests"""
    print("=" * 60)
    print("CHEESE++ COMPILER TEST SUITE")
    print("=" * 60)
    
    integration_passed = run_integration_tests(verbose)
    performance_passed = run_performance_tests(verbose)
    
    print("=" * 60)
    if integration_passed and performance_passed:
        print("✓ ALL TESTS PASSED!")
        return True
    else:
        print("✗ SOME TESTS FAILED!")
        return False


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Run Cheese++ compiler tests")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    parser.add_argument("-t", "--type", choices=["integration", "performance", "all"], 
                       default="all", help="Type of tests to run")
    
    args = parser.parse_args()
    
    if args.type == "integration":
        success = run_integration_tests(args.verbose)
    elif args.type == "performance":
        success = run_performance_tests(args.verbose)
    else:
        success = run_all_tests(args.verbose)
    
    sys.exit(0 if success else 1)

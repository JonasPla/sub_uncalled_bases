import sys
import io
from contextlib import redirect_stdout
import substitute_uncalled_bases


def test_script(args):
    sys.argv = args
    f_stdout = io.StringIO()

    try:
        with redirect_stdout(f_stdout):
            substitute_uncalled_bases.main()
    except SystemExit:
        # Catch SystemExit to prevent the test script from exiting
        pass

    return f_stdout.getvalue()

def run_tests():
    print("Running 1 Test\n")
    stdout = test_script(
        [
            "substitute_uncalled_bases.py",
            "-a",
            "test.aln",
            "-s",
            "few_n",
            "-d",
            "many_n",
        ]
    )
    expected_output = ">many_n\nAGCTANCTACGT"
    print(f"Expected output:\n{expected_output}\n\nActual output:\n{stdout}\n")

    if expected_output == stdout:
        print("Test passed!")
    else:
        print("Test failed")


if __name__ == "__main__":
    run_tests()

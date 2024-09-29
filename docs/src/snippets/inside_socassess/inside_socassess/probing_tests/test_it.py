from pathlib import Path


def test_and_provide_context_1(artifacts: Path):
    f = (artifacts / 'test_case_context.txt').open('a')
    f.write("test_and_provide_context_1: log line #1\n")
    f.write("test_and_provide_context_1: log line #2\n")
    f.write("test_and_provide_context_1: log line #3\n")
    f.write("test_and_provide_context_1: log line ...\n")
    assert True


def test_and_provide_context_2(artifacts: Path):
    f = (artifacts / 'test_case_context.txt').open('a')
    f.write("test_and_provide_context_2: log line #1\n")
    f.write("test_and_provide_context_2: log line #2\n")
    f.write("test_and_provide_context_2: log line #3\n")
    f.write("test_and_provide_context_2: log line ...\n")
    assert True

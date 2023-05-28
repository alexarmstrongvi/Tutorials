from mypkg import utils
import pathlib
import pytest

# Test statements
def test_assert():
    assert True

# Test function return value
def func(a, b):
    return a + b

def test_func():
    assert func(1,2) == 3

# Test raise condition
def test_raise():
    with pytest.raises(SystemExit):
        raise SystemExit

################################################################################
# Grouping tests into a class
################################################################################
# Why would you use this?
class TestClass():
    def test_assert(self):
        assert True

################################################################################
# Fixtures - recognized arg names that retreive helpful objects (i.e. fixtures)
################################################################################
# Test in temporary directory
def test_tmpdir(tmp_path):
    # tmpdir was used before pathlib
    assert isinstance(tmp_path, pathlib.Path)

    file_path = tmp_path / 'my_file.txt' 
    file_path.write_text('Hello')
    assert len(list(tmp_path.iterdir())) == 1
    assert file_path.read_text() == 'Hello'

# Permanent fixtures
# @pytest.fixture(autouse=True)

# Custom fixtures
# @pytest.fixture

################################################################################
# Monkeypatching/Mocking
################################################################################
#def test_monkeypatch(monkeypatch):

# Overwrite module/class method for test
# monkeypatch.setattr(obj, name, value, raising=True)
# monkeypatch.delattr(obj, name, raising=True)

# Overwite dictionary item
# monkeypatch.setitem(mapping, name, value)
# monkeypatch.delitem(obj, name, raising=True)

# Overwrite environment variable
# monkeypatch.setenv(name, value, prepend=False)
# monkeypatch.delenv(name, raising=True)

# Change the current working directory
# monkeypatch.chdir(path)

# Modify sys.path
# monkeypatch.syspath_prepend(path)

# Only apply monkeypatching within a context manager
# with monkeypatch.context() as m:


#! python3  # noqa E265

"""
    Usage from the repo root folder:

    .. code-block:: bash
        # for whole tests
        python -m unittest tests.test_utils_check_path
        # for specific test
        python -m unittest tests.test_utils_check_path.TestUtilsCheckPath.test_check_path_as_str_ok
"""


# standard library
import stat
import unittest
from os import chmod, getenv
from pathlib import Path

# project
from qgis_deployment_toolbelt.utils.check_path import (
    check_path,
    check_path_exists,
    check_path_is_readable,
    check_path_is_writable,
    check_var_can_be_path,
)

# ############################################################################
# ########## Classes #############
# ################################


class TestUtilsCheckPath(unittest.TestCase):
    """Test package metadata."""

    def test_check_path_as_str_ok(self):
        """Test filepath as str is converted into Path."""
        self.assertTrue(
            check_var_can_be_path(input_var="/this/is/an/imaginary/file.imaginary")
        )

    def test_check_path_as_str_ko(self):
        """Test filepath from int can't be converted into Path."""
        with self.assertRaises(TypeError):
            check_var_can_be_path(input_var=1000)
        # no exception but False
        self.assertFalse(check_var_can_be_path(input_var=1000, raise_error=False))

    def test_check_path_exists_ok(self):
        """Test path exists."""
        # a valid Path instance pointing to an existing file
        self.assertTrue(check_path_exists(input_path=Path("setup.py")))
        # str is valid and point to an existing file
        self.assertTrue(check_path_exists(input_path="setup.py"))

    def test_check_path_exists_ko(self):
        """Test path exists fail cases."""
        # str is not valid
        with self.assertRaises(TypeError):
            check_path_exists(input_path=1000)
        self.assertFalse(check_path_exists(input_path=1000, raise_error=False))
        # str is valid but not an existing file
        with self.assertRaises(FileExistsError):
            check_path_exists(input_path="/this/is/an/imaginary/file.imaginary")
        # no exception but False
        self.assertFalse(
            check_path_exists(
                input_path="/this/is/an/imaginary/file.imaginary", raise_error=False
            )
        )

    def test_check_path_readable_ok(self):
        """Test path is readable."""
        # a valid Path instance pointing to an existing file which is readable
        self.assertTrue(check_path_is_readable(input_path=Path("setup.py")))
        # str is valid and point to an existing file which is readable
        self.assertTrue(check_path_is_readable(input_path="setup.py"))

    def test_check_path_readable_ko(self):
        """Test path is readable fail cases."""
        # str is not valid
        with self.assertRaises(TypeError):
            check_path_is_readable(input_path=1000)
        self.assertFalse(check_path_is_readable(input_path=1000, raise_error=False))

    @unittest.skipIf(
        getenv("CI"), "Creating file on CI with specific rights is not working."
    )
    def test_check_path_readable_ko_specific(self):
        """Test path is readable fail cases."""
        # temporary fixture
        new_file = Path("tests/tmp_file_no_readable.txt")
        new_file.touch(mode=0o333, exist_ok=True)

        # str not valid, an existing file but not readable
        with self.assertRaises(IOError):
            check_path_is_readable(input_path=new_file)

        # no exception but False
        self.assertFalse(check_path_is_readable(input_path=new_file, raise_error=False))

        # temporary fixture
        new_file.unlink(missing_ok=True)

    def test_check_path_writable_ok(self):
        """Test path is writable."""
        # a valid Path instance pointing to an existing file which is writable
        self.assertTrue(check_path_is_writable(input_path=Path("setup.py")))
        # str is valid and point to an existing file which is writable
        self.assertTrue(check_path_is_writable(input_path="setup.py"))

    def test_check_path_writable_ko(self):
        """Test path is writable fail cases."""
        # str is not valid
        with self.assertRaises(TypeError):
            check_path_exists(input_path=1000)
        self.assertFalse(check_path_is_writable(input_path=1000, raise_error=False))

    @unittest.skipIf(
        getenv("CI"), "Creating file on CI with specific rights is not working."
    )
    def test_check_path_writable_ko_specific(self):
        """Test path is writable fail cases (specific)."""
        # temporary fixture
        not_writable_file = Path("tests/tmp_file_no_writable.txt")
        not_writable_file.touch(mode=0o400, exist_ok=True)

        # str not valid, an existing file but not writable
        with self.assertRaises(IOError):
            check_path_is_writable(input_path=not_writable_file)

        # no exception but False
        self.assertFalse(
            check_path_is_writable(input_path=not_writable_file, raise_error=False)
        )

        not_writable_file.unlink()

    def test_check_path_meta_ok(self):
        """Test meta check path."""
        # an existing file
        check_path(
            input_path="requirements.txt",
            must_be_a_file=True,
            must_be_a_folder=False,
        )
        check_path(
            input_path=Path("requirements.txt"),
            must_be_a_file=True,
            must_be_a_folder=False,
        )

        # an existing folder
        check_path(
            input_path=Path(__file__).parent,
            must_be_a_file=False,
            must_be_a_folder=True,
        )

    def test_check_path_meta_ko(self):
        """Test meta check path fail cases."""
        # invalid path
        with self.assertRaises(TypeError):
            check_path(
                input_path=1000,
            )
        self.assertFalse(check_path(input_path=1000, raise_error=False))

        # mutual exclusive options
        with self.assertRaises(ValueError):
            check_path(
                input_path="requirements.txt",
                must_be_a_file=True,
                must_be_a_folder=True,
            )

        # must exist
        self.assertFalse(
            check_path(
                input_path="imaginary/path", raise_error=False, must_exists=False
            )
        )
        self.assertFalse(
            check_path(input_path="imaginary/path", raise_error=False, must_exists=True)
        )
        with self.assertRaises(FileExistsError):
            check_path(input_path="imaginary/path", must_exists=True)

        # must be readable
        self.assertTrue(
            check_path(
                input_path="imaginary/path",
                raise_error=False,
                must_exists=False,
                must_be_readable=False,
            )
        )
        self.assertTrue(
            check_path(
                input_path="setup.py",
                raise_error=False,
                must_exists=False,
                must_be_readable=True,
            )
        )

        # must be writable
        self.assertFalse(
            check_path(
                input_path="imaginary/path",
                raise_error=False,
                must_exists=False,
                must_be_readable=False,
                must_be_writable=True,
            )
        )
        self.assertTrue(
            check_path(
                input_path=f"tests/{Path(__file__).name}",
                raise_error=True,
                must_exists=False,
                must_be_readable=False,
                must_be_writable=True,
            )
        )

        # must be a file
        self.assertFalse(
            check_path(
                input_path=Path(__file__).parent,
                raise_error=False,
                must_exists=True,
                must_be_a_file=True,
            )
        )
        with self.assertRaises(FileNotFoundError):
            check_path(
                input_path=Path(__file__).parent,
                raise_error=True,
                must_exists=True,
                must_be_a_file=True,
            )

        # must be a folder
        self.assertFalse(
            check_path(
                input_path=Path(__file__),
                raise_error=False,
                must_exists=True,
                must_be_a_folder=True,
            )
        )
        with self.assertRaises(NotADirectoryError):
            check_path(
                input_path=Path(__file__),
                raise_error=True,
                must_exists=True,
                must_be_a_folder=True,
            )

    @unittest.skipIf(
        getenv("CI"), "Creating file on CI with specific rights is not working."
    )
    def test_check_path_meta_ko_specific(self):
        """Test meta check path is readbale / writable fail cases (specific)."""
        # temporary fixture
        not_writable_file = Path("tests/tmp_file_no_writable.txt")
        not_writable_file.touch()
        chmod(not_writable_file, stat.S_IREAD | stat.S_IROTH)

        # str not valid, an existing file but not writable
        with self.assertRaises(IOError):
            check_path(
                input_path=not_writable_file, must_be_a_file=True, must_be_writable=True
            )

        # no exception but False
        self.assertFalse(
            check_path(
                input_path=not_writable_file,
                must_be_a_file=True,
                must_be_writable=True,
                raise_error=False,
            )
        )

        not_writable_file.unlink()


# ############################################################################
# ####### Stand-alone run ########
# ################################
if __name__ == "__main__":
    unittest.main()

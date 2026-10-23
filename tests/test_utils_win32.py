#! python3  # noqa E265

"""
Usage from the repo root folder:

.. code-block:: bash
    # for whole tests
    python -m unittest tests.test_utils
    # for specific test
    python -m unittest tests.test_utils.TestUtilsWin32.test_win32_getenv
"""

# standard library
import subprocess
import sys
import unittest
from sys import platform as opersys

# project
from qgis_deployment_toolbelt.utils.os_utils_router import get_environment_variable
from qgis_deployment_toolbelt.utils.win32utils import hold_com_apartment


# Python code printing the COM apartment type of the main thread after a sequence
# of COM calls, run in a fresh interpreter: pywin32 tracks the main thread COM
# initialization in a global state which other tests may already have altered.
COM_STATE_SCRIPT = """
import ctypes
import pathlib
import tempfile

import pythoncom  # initializes COM on the main thread
from send2trash import send2trash

from qgis_deployment_toolbelt.utils.win32utils import hold_com_apartment

if {hold}:
    hold_com_apartment()

# checked after each run: once torn down, a later pythoncom.CoInitialize() creates
# a new apartment, which would hide that objects of the first one were orphaned
for _ in range(3):
    {operation}
    apartment_type, qualifier = ctypes.c_int(-1), ctypes.c_int(0)
    hresult = ctypes.windll.ole32.CoGetApartmentType(
        ctypes.byref(apartment_type), ctypes.byref(qualifier)
    )
    print(hresult & 0xFFFFFFFF, apartment_type.value)
"""

# what send2trash.win.modern does around IFileOperation
UNBALANCED_PAIR = "pythoncom.CoInitialize(); pythoncom.CoUninitialize()"
SEND2TRASH = (
    "f = pathlib.Path(tempfile.mkdtemp(prefix='QDT_test_com_')) / 'trash_me.txt'; "
    "f.write_text('QDT'); send2trash(f); assert not f.exists()"
)


def main_thread_has_sta(operation: str, hold: bool = True) -> bool:
    """Run a COM operation in a fresh interpreter and tell if its main thread still
    belongs to a single-threaded apartment afterwards.

    Args:
        operation (str): Python statement to run 3 times after the COM initialization
        hold (bool, optional): call hold_com_apartment first. Defaults to True.

    Returns:
        bool: True if the main thread stayed in a (main) single-threaded apartment
            after each run. An implicit multi-threaded apartment, kept for a while by
            the threads of the shell after send2trash, does not count.
    """
    completed = subprocess.run(
        [sys.executable, "-c", COM_STATE_SCRIPT.format(hold=hold, operation=operation)],
        capture_output=True,
        check=True,
        text=True,
    )
    states = [tuple(map(int, line.split())) for line in completed.stdout.splitlines()]
    # S_OK and APTTYPE_STA (0) or APTTYPE_MAINSTA (3)
    return len(states) == 3 and all(
        hresult == 0 and apartment_type in (0, 3) for hresult, apartment_type in states
    )


# ############################################################################
# ########## Classes #############
# ################################


class TestUtilsWin32(unittest.TestCase):
    """Test package utilities."""

    @unittest.skipIf(opersys != "win32", "Test specific to Windows.")
    def test_win32_getenv(self):
        """Test specific Windows environment variable getter."""
        # OK
        self.assertIsInstance(get_environment_variable("TEMP"), str)

        # KO
        self.assertIsNone(get_environment_variable("YOUPI"))

    @unittest.skipIf(opersys != "win32", "Test specific to Windows.")
    def test_hold_com_apartment(self):
        """Test that COM is initialized on the calling thread."""
        self.assertTrue(hold_com_apartment())

    @unittest.skipIf(opersys != "win32", "Test specific to Windows.")
    def test_hold_com_apartment_survives_unbalanced_uninitialize(self):
        """Test that the pythoncom.CoInitialize/CoUninitialize pair made by send2trash
        does not tear down COM on the main thread, which pywin32 initialized at import.
        """
        self.assertTrue(main_thread_has_sta(UNBALANCED_PAIR))

    @unittest.skipIf(opersys != "win32", "Test specific to Windows.")
    def test_hold_com_apartment_survives_send2trash(self):
        """Test that the main thread still has its COM apartment after send2trash."""
        self.assertTrue(main_thread_has_sta(SEND2TRASH))


# ############################################################################
# ####### Stand-alone run ########
# ################################
if __name__ == "__main__":
    unittest.main()

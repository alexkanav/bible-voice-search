import tkinter as tk

import pytest


@pytest.fixture(scope="module")
def tk_root():
    """
    Provides a hidden Tkinter root for GUI tests.
    """
    root = tk.Tk()
    root.withdraw()
    yield root
    root.destroy()

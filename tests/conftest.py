from __future__ import annotations

import string

import pytest


@pytest.fixture
def string_compare(s1, s2) -> bool:
    remove = string.punctuation + string.whitespace
    return s1.translate(None, remove) == s2.translate(None, remove)

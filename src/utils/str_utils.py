from __future__ import annotations


def clean_string(in_str):
    return in_str.lower().strip().replace(" ", "_")

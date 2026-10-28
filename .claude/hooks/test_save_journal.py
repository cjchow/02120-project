"""Tests for the journal redaction. Run: python .claude/hooks/test_save_journal.py"""

import json

from save_journal import redact, redact_line


def test_redact():
    out = redact(r"C:\Users\alice\proj, mail a.b@uni.edu from 10.2.33.4, Alice", "alice")
    assert out == r"C:\Users\[user]\proj, mail [email] from [ip], [user]"
    # Dots written as "\." inside a search pattern are caught too.
    assert redact(r"grep 'a.b@uni\.edu|10\.2\.33\.4'", "alice") == "grep '[email]|[ip]'"
    # An IP at the end of a sentence (followed by a period) is caught.
    assert redact("from IP address 10.2.33.4.", "alice") == "from IP address [ip]."
    # Ordinary text, decimals, and version numbers with 4+ parts are left alone.
    assert redact("tau = 2.5, years 3.0, v1.2.3.4.5", "alice") == "tau = 2.5, years 3.0, v1.2.3.4.5"


def test_redact_line_stays_valid_json():
    # A newline right before the email and IP: raw-text redaction used to break here.
    line = json.dumps({"text": "such\nalice@uni.edu\n10.2.33.4: 0", "path": "C:\\Users\\alice"}) + "\n"
    record = json.loads(redact_line(line, "alice"))
    assert record == {"text": "such\n[email]\n[ip]: 0", "path": "C:\\Users\\[user]"}


if __name__ == "__main__":
    test_redact()
    test_redact_line_stays_valid_json()
    print("all journal redaction tests: PASS")

import json

import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.normpath(os.path.join(SCRIPT_DIR, "..", "data", "sample_base.json"))

print(DATA_PATH)

EMAILS = None


def _load_emails() -> None:
    """Loads the list of emails from the path"""
    with open(DATA_PATH, "r") as f:
        data = json.loads(f.read())
        global EMAILS
        EMAILS = data["emails"]


def _get_emails() -> list[dict]:
    """Reads and return the full list of emails available"""
    if EMAILS is None:
        _load_emails()
    return EMAILS


def _search_email(id: str) -> dict:
    """Search the available emails and return a single email"""
    if EMAILS is None:
        _load_emails()

    email = [x for x in EMAILS if x["id"] == id]
    if email:
        return {"result": email}
    else:
        return {"result": "email id not found"}


def _send_email(to: str, subject: str, body: str) -> dict:
    """Mock sending an email with given parameters"""
    print(f"Sending email to: {to}")
    print(f"Subject: {subject}")
    print(f"Body: {body}")
    return {"result": f"Email sent successfully to {to}"}


if __name__ == "__main__":
    print("=" * 20)
    print(
        json.dumps(
            _get_emails(),
            indent=2,
            ensure_ascii=False,
        )
    )
    print("=" * 20)
    print(
        json.dumps(
            _search_email("email002"),
            indent=2,
            ensure_ascii=False,
        )
    )
    print("=" * 20)
    print(
        json.dumps(
            _search_email("email005"),
            indent=2,
            ensure_ascii=False,
        )
    )
    print("=" * 20)
    print(
        _send_email(
            to="recipient@example.com",
            subject="Meeting Reminder",
            body="Don't forget our meeting at 10 AM tomorrow.",
        )
    )

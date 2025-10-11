import json

EMAILS = None
DATA_PATH = "../data/sample_base.json"


def load_emails() -> None:
    """Loads the list of emails from the path"""
    with open(DATA_PATH, "r") as f:
        data = json.loads(f.read())
        global EMAILS
        EMAILS = data


def get_emails() -> list[dict]:
    """Reads and return the full list of emails available"""
    if EMAILS is None:
        load_emails()
    return EMAILS


def search_email(id: str) -> dict:
    """Search the available emails and return a single email"""
    email = [x for x in EMAILS if x["id"] == id]
    return email


if __name__ == "__main__":
    print("=" * 20)
    print(
        json.dumps(
            get_emails(),
            indent=2,
            ensure_ascii=False,
        )
    )
    print("=" * 20)
    print(
        json.dumps(
            search_email("email002"),
            indent=2,
            ensure_ascii=False,
        )
    )
    print("=" * 20)
    print(
        json.dumps(
            search_email("email005"),
            indent=2,
            ensure_ascii=False,
        )
    )

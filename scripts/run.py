#!/usr/bin/env python3
import argparse
import json
import sys


INTENTS = [
    {
        "intent": "email",
        "keywords": ["email"],
        "pattern": r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$",
        "notes": "Basic email matcher for most application validation needs.",
    },
    {
        "intent": "date-mmddyyyy",
        "keywords": ["date", "mm/dd/yyyy"],
        "pattern": r"^(0[1-9]|1[0-2])/(0[1-9]|[12][0-9]|3[01])/\d{4}$",
        "notes": "Matches calendar dates in MM/DD/YYYY format.",
    },
    {
        "intent": "ipv4",
        "keywords": ["ipv4"],
        "pattern": r"^((25[0-5]|2[0-4]\d|1?\d?\d)\.){3}(25[0-5]|2[0-4]\d|1?\d?\d)$",
        "notes": "Matches dotted IPv4 addresses from 0.0.0.0 to 255.255.255.255.",
    },
    {
        "intent": "us-phone",
        "keywords": ["phone", "us"],
        "pattern": r"^(?:\+1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}$",
        "notes": "Matches common US phone number formats.",
    },
    {
        "intent": "url",
        "keywords": ["url"],
        "pattern": r"^https?://[^\s/$.?#].[^\s]*$",
        "notes": "Matches basic HTTP/HTTPS URLs.",
    },
]


def detect_intent(text: str):
    request = text.lower()
    for rule in INTENTS:
        if all(keyword in request for keyword in rule["keywords"]):
            return rule
    return None


def main():
    parser = argparse.ArgumentParser(
        description="Generate regex patterns from plain-English matching requests."
    )
    parser.add_argument("request", nargs="?", help="Plain-English request to convert to regex.")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    args = parser.parse_args()

    request = args.request
    if request is None:
        request = sys.stdin.read()
    request = request.strip()
    if not request:
        print("ERROR: provide a request argument or stdin text.", file=sys.stderr)
        return 2

    match = detect_intent(request)
    if match is None:
        print(
            "ERROR: no supported pattern detected. Try email, date MM/DD/YYYY, IPv4, US phone, or URL.",
            file=sys.stderr,
        )
        return 1

    if args.format == "json":
        payload = {
            "intent": match["intent"],
            "pattern": match["pattern"],
            "notes": match["notes"],
        }
        print(json.dumps(payload, indent=2))
    else:
        print(f"intent: {match['intent']}")
        print(f"pattern: {match['pattern']}")
        print(f"notes: {match['notes']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

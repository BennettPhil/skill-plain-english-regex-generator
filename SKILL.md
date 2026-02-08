---
name: plain-english-regex-generator
description: Convert short plain-English matching requests into practical regex patterns.
version: 0.1.0
license: Apache-2.0
---

# Plain English Regex Generator

## Purpose

This skill turns a short plain-English description of what to match into a ready-to-use regular expression. It is useful when you know the data shape you need to match but do not want to handcraft regex syntax from scratch.

## Instructions

1. Collect a plain-English description from arguments or stdin, such as "match an email address".
2. Normalize the text to lowercase and trim whitespace before intent detection.
3. Match the request against supported intents in `scripts/run.py`:
4. `email`
5. `date-mmddyyyy`
6. `ipv4`
7. `us-phone`
8. `url`
9. If no supported intent matches, return an error with guidance and exit non-zero.
10. Print the selected regex pattern in text mode by default.
11. If `--format json` is supplied, print a JSON object with `intent`, `pattern`, and `notes`.
12. Preserve deterministic output so repeated runs with the same input return the same pattern.

## Inputs

- Primary input: plain-English description via positional argument or stdin.
- Optional input: `--format text|json` (default `text`).

## Outputs

- Text mode: three lines (`intent`, `pattern`, `notes`) to stdout.
- JSON mode: structured JSON on stdout.
- Exit `0` on success.
- Exit `1` when no supported intent is detected.
- Exit `2` for usage errors.

## Constraints

- This skill is pattern-template based, not an LLM.
- Only the predefined intents are supported.
- Generated regexes prioritize readability and common cases over full RFC-level strictness.

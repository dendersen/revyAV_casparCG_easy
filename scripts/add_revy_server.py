#!/usr/bin/env python3
"""Add the Revy CasparCG server to an existing client database."""

import argparse
import sqlite3
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Add the Revy server (127.0.0.1:5250) to the client database."
    )
    parser.add_argument("database", type=Path, help="path to the client's Database.s3db")
    database_path = parser.parse_args().database.expanduser()

    if not database_path.is_file():
        parser.error(f"database file does not exist: {database_path}")

    try:
        with sqlite3.connect(database_path) as connection:
            connection.execute("BEGIN IMMEDIATE")
            columns = {
                row[1]
                for row in connection.execute('PRAGMA table_info("Device")')
            }
            required_columns = {"Name", "Address", "Port"}
            if not required_columns.issubset(columns):
                missing = ", ".join(sorted(required_columns - columns))
                raise RuntimeError(f"Device table is missing required columns: {missing}")

            existing = connection.execute(
                'SELECT 1 FROM "Device" WHERE "Name" = ?', ("revy",)
            ).fetchone()
            if existing:
                raise RuntimeError("a server named 'revy' already exists; no changes made")

            connection.execute(
                'INSERT INTO "Device" ("Name", "Address", "Port") VALUES (?, ?, ?)',
                ("revy", "127.0.0.1", 5250),
            )
    except sqlite3.Error as error:
        raise SystemExit(f"Could not update client database {database_path}: {error}") from error
    except RuntimeError as error:
        raise SystemExit(str(error)) from error

    print("Added server 'revy' at 127.0.0.1:5250.")


if __name__ == "__main__":
    main()

import json
from datetime import datetime
import constants as c
import logging

# Setup logging
logging.basicConfig(level=logging.DEBUG, format="%(levelname)s: %(message)s")

# ---------- Load Notes ----------
try:
    with open(c.filename, "r") as file:
        note = json.load(file)
except (FileNotFoundError, json.JSONDecodeError):
    logging.warning("Could not load JSON, initializing empty note list.")
    note = []


# ---------- Functions ----------
def insert_note(text: str):
    """Add a new note with timestamp and auto-incremented ID."""
    logging.debug(f"Raw input: {text}")

    if not text.strip():
        logging.warning("Empty note not saved.")
        return

    new_note = {
        "id": len(note) + 1,
        "time": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "text": text.strip(),
    }

    note.append(new_note)
    _save_notes()
    logging.info("Note saved.")


def read_note():
    """Print all note texts to the console (for debug/testing)."""
    for dic in note:
        logging.debug(f"Note: {dic}")
        print(dic["text"])


def delete_note(del_id: int):
    """Delete a note by ID and re-number the rest."""

    global note
    original_len = len(note)
    note = [n for n in note if n.get("id") != del_id]

    if len(note) == original_len:
        logging.error(f"No note found with ID {del_id}.")
        return

    # Reassign IDs
    for i, n in enumerate(note, start=1):
        n["id"] = i

    _save_notes()
    logging.info(f"Deleted note with ID {del_id} and reindexed remaining.")


def _save_notes():
    """Helper function to save current notes to the JSON file."""
    try:
        with open(c.filename, "w") as file:
            json.dump(note, file, indent=4)
        logging.debug("Notes successfully written to file.")
    except Exception as e:
        logging.error(f"Failed to write notes to file: {e}")

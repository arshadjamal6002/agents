# utils/memory.py
import json
import os

MEMORY_FILE = "memory.json" # The file where memory will be stored

class Memory:
    """A simple key-value store that persists to a JSON file."""
    def __init__(self):
        self._mem = {}
        self._load() # Load from file on initialization
        print(f"[Memory] Initialized. Loaded {len(self._mem)} items from {MEMORY_FILE}")

    def _load(self):
        if os.path.exists(MEMORY_FILE):
            with open(MEMORY_FILE, "r") as f:
                try:
                    self._mem = json.load(f)
                except json.JSONDecodeError:
                    # If the file is empty or corrupt, start with an empty memory
                    self._mem = {}

    def _save(self):
        """Saves the current memory state to the file."""
        with open(MEMORY_FILE, "w") as f:
            json.dump(self._mem, f, indent=2)

    def store(self, key: str, value):
        print(f"[Memory] Storing '{key}'...")
        self._mem[key] = value
        self._save() # <-- Save after every change

    def get(self, key: str):
        return self._mem.get(key)

    def all(self):
        return self._mem.copy()

    def clear(self):
        print("[Memory] Clearing all values.")
        self._mem = {}
        self._save() # <-- Save after clearing

# This shared instance will now automatically load and save to memory.json
shared_memory = Memory()
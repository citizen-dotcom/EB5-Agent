# Purpose: Simple in-memory store for case facts (addresses, names, prompts).
class MemoryBank:
    def __init__(self):
        self._store = {}

    def get_case(self, case_id: str) -> dict:
        """Return all remembered facts for a case."""
        return self._store.get(case_id, {})

    def upsert_case_fact(self, case_id: str, key: str, value):
        """Add or update a fact for a case."""
        case = self._store.get(case_id, {})
        case[key] = value
        self._store[case_id] = case

memory = MemoryBank()
"""
Perfilación de la memoria UNICAMENTE de la carga de datos
"""

from pathlib import Path
from ll import LinkedList
from memory_profiler import profile

@profile
def main() -> None:
    base_path = Path(__file__).parent
    json_path = base_path / "songs.json"

    playlist = LinkedList.from_json_file(json_path)

    print(f"Loaded {len(playlist)} tracks")


if __name__ == "__main__":
    main()


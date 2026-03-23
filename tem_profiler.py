from ll import LinkedList
from pathlib import Path
import cProfile


def main() -> None:
    base_path = Path(__file__).parent
    json_path = base_path / "songs.json"

    playlist = LinkedList.from_json_file(json_path)

    print(f"Loaded {len(playlist)} tracks")


if __name__ == "__main__":
    cProfile.run("main()")
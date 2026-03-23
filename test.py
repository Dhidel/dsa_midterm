from ll import LinkedList
from pathlib import Path

# def run_demo() -> None:
#     playlist = LinkedList.from_json_file("songs.json")

#     print("--- PLAYLIST LOADED FROM JSON ---")
#     print(f"Total tracks loaded: {len(playlist)}")

#     if playlist.start is not None and playlist.end is not None:
#         print(f"\nFirst Track: {playlist.start.data['name']}")
#         print(f"Last Track: {playlist.end.data['name']}")

#     target_song = "Quemarás"
#     node = playlist.search(target_song)

#     if node is not None:
#         print(f"\nReproduciendo: {node.data['name']} [{node.data['album']}]")
#         if node.prev is not None:
#             print(f"  << Anterior: {node.prev.data['name']}")
#         if node.next is not None:
#             print(f"  >> Siguiente: {node.next.data['name']}")

#     print("\nVisualización de la Lista Doble:")
#     print(playlist)


# if __name__ == "__main__":
#     run_demo()


def print_track(prefix: str, node) -> None:
    if node is None:
        print(f"{prefix}: None")
        return

    print(
        f"{prefix}: {node.data['name']} "
        f"[{node.data['artist']} | {node.data['album']}]"
    )


def run_demo() -> None:
    base_path = Path(__file__).parent
    json_path = base_path / "songs.json"

    playlist = LinkedList.from_json_file(json_path)

    print("--- PLAYLIST TEST ---")
    print(f"Tracks loaded: {len(playlist)}")
    print(f"Shuffle enabled? {playlist.shuffle_enabled}")
    print()

    print_track("Now playing", playlist.now_playing())
    print_track("Next track", playlist.next_track())
    print_track("Next track", playlist.next_track())
    print_track("Previous track", playlist.previous_track())
    print()

    print("--- ENABLING SHUFFLE ---")
    playlist.enable_shuffle()
    print(f"Shuffle enabled? {playlist.shuffle_enabled}")
    print_track("Now playing", playlist.now_playing())
    print_track("Next track", playlist.next_track())
    print_track("Next track", playlist.next_track())
    print_track("Previous track", playlist.previous_track())
    print()

    print("--- DISABLING SHUFFLE ---")
    playlist.disable_shuffle()
    print(f"Shuffle enabled? {playlist.shuffle_enabled}")
    print_track("Now playing", playlist.now_playing())
    print_track("Next track", playlist.next_track())
    print_track("Next track", playlist.next_track())
    print_track("Previous track", playlist.previous_track())
    print()

    print("--- SEARCH TEST ---")
    target_song = "Quemarás"
    node = playlist.search(target_song)

    if node is None:
        print(f"Song not found: {target_song}")
    else:
        print_track("Found", node)
        print_track("Previous", node.prev)
        print_track("Next", node.next)


if __name__ == "__main__":
    run_demo()

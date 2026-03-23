from ll import LinkedList

def run_demo() -> None:
    playlist = LinkedList.from_json_file("songs.json")

    print("--- PLAYLIST LOADED FROM JSON ---")
    print(f"Total tracks loaded: {len(playlist)}")

    if playlist.start is not None and playlist.end is not None:
        print(f"\nFirst Track: {playlist.start.data['name']}")
        print(f"Last Track: {playlist.end.data['name']}")

    target_song = "Quemarás"
    node = playlist.search(target_song)

    if node is not None:
        print(f"\nReproduciendo: {node.data['name']} [{node.data['album']}]")
        if node.prev is not None:
            print(f"  << Anterior: {node.prev.data['name']}")
        if node.next is not None:
            print(f"  >> Siguiente: {node.next.data['name']}")

    print("\nVisualización de la Lista Doble:")
    print(playlist)


if __name__ == "__main__":
    run_demo()
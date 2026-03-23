from __future__ import annotations

from collections.abc import Iterable, Iterator


class Node:
    def __init__(self, name: str, artist: str, album: str) -> None:
        self.data: dict[str, str] = {
            "name": name,
            "artist": artist,
            "album": album,
        }
        self.next: Node | None = None
        self.prev: Node | None = None

    def __repr__(self) -> str:
        return f"Node({self.data['name']!r}, {self.data['artist']!r})"


class LinkedList:
    def __init__(self) -> None:
        self.start: Node | None = None
        self.end: Node | None = None

    def __iter__(self) -> Iterator[Node]:
        current = self.start
        while current is not None:
            yield current
            current = current.next

    def __len__(self) -> int:
        return sum(1 for _ in self)

    def __repr__(self) -> str:
        parts: list[str] = ["START"]
        for node in self:
            parts.append(f"[{node.data['name']}]")
        parts.append("NIL")
        return " <-> ".join(parts)

    def insert_at_beginning(self, name: str, artist: str, album: str) -> None:
        new_node = Node(name, artist, album)

        if self.start is None:
            self.start = new_node
            self.end = new_node
            return

        new_node.next = self.start
        self.start.prev = new_node
        self.start = new_node

    def insert_at_end(self, name: str, artist: str, album: str) -> None:
        new_node = Node(name, artist, album)

        if self.end is None:
            self.start = new_node
            self.end = new_node
            return

        new_node.prev = self.end
        self.end.next = new_node
        self.end = new_node

    def delete_node(self, song_name: str) -> bool:
        current = self.start

        while current is not None:
            if current.data["name"] == song_name:
                if current.prev is not None:
                    current.prev.next = current.next
                else:
                    self.start = current.next

                if current.next is not None:
                    current.next.prev = current.prev
                else:
                    self.end = current.prev

                current.next = None
                current.prev = None
                return True

            current = current.next

        return False

    def search(self, song_name: str) -> Node | None:
        for node in self:
            if node.data["name"] == song_name:
                return node
        return None

    @classmethod
    def from_iterable(cls, songs: Iterable[dict[str, str]]) -> LinkedList:
        linked_list = cls()

        for song in songs:
            linked_list.insert_at_end(
                song["name"],
                song["artist"],
                song["album"],
            )

        return linked_list
from __future__ import annotations

import json
import random
from collections.abc import Iterable, Iterator
from pathlib import Path


class Node:
    def __init__(self, name: str, artist: str, album: str) -> None:
        self.data: dict[str, str] = {
            "name": name,
            "artist": artist,
            "album": album,
        }
        self.next: Node | None = None
        self.prev: Node | None = None
        self.play_next: Node | None = None
        self.play_prev: Node | None = None

    def __repr__(self) -> str:
        return f"Node({self.data['name']!r}, {self.data['artist']!r})"


class LinkedList:
    def __init__(self) -> None:
        self.start: Node | None = None
        self.end: Node | None = None
        self.current: Node | None = None
        self.shuffle_enabled: bool = False

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

    def _rebuild_playback_links(self) -> None:
        nodes = list(self)

        if not nodes:
            self.current = None
            return

        if self.shuffle_enabled and len(nodes) > 1:
            if self.current is not None and self.current in nodes:
                current_node = self.current
                remaining = nodes.copy()
                remaining.remove(current_node)
                random.shuffle(remaining)
                order = [current_node, *remaining]
            else:
                order = nodes.copy()
                random.shuffle(order)
        else:
            order = nodes

        for index, node in enumerate(order):
            node.play_prev = order[index - 1] if index > 0 else None
            node.play_next = order[index + 1] if index < len(order) - 1 else None

        if self.current is None or self.current not in order:
            self.current = order[0]

    def enable_shuffle(self) -> None:
        self.shuffle_enabled = True
        self._rebuild_playback_links()

    def disable_shuffle(self) -> None:
        self.shuffle_enabled = False
        self._rebuild_playback_links()

    def toggle_shuffle(self) -> None:
        self.shuffle_enabled = not self.shuffle_enabled
        self._rebuild_playback_links()

    def now_playing(self) -> Node | None:
        return self.current

    def next_track(self) -> Node | None:
        if self.current is None:
            self._rebuild_playback_links()
            return self.current

        if self.current.play_next is not None:
            self.current = self.current.play_next

        return self.current

    def previous_track(self) -> Node | None:
        if self.current is None:
            self._rebuild_playback_links()
            return self.current

        if self.current.play_prev is not None:
            self.current = self.current.play_prev

        return self.current

    def insert_at_beginning(self, name: str, artist: str, album: str) -> None:
        new_node = Node(name, artist, album)

        if self.start is None:
            self.start = new_node
            self.end = new_node
        else:
            new_node.next = self.start
            self.start.prev = new_node
            self.start = new_node

        self._rebuild_playback_links()

    def insert_at_end(self, name: str, artist: str, album: str) -> None:
        new_node = Node(name, artist, album)

        if self.end is None:
            self.start = new_node
            self.end = new_node
        else:
            new_node.prev = self.end
            self.end.next = new_node
            self.end = new_node

        self._rebuild_playback_links()

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
                current.play_next = None
                current.play_prev = None

                self._rebuild_playback_links()
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
            new_node = Node(
                song["name"],
                song["artist"],
                song["album"],
            )

            if linked_list.start is None:
                linked_list.start = new_node
                linked_list.end = new_node
            else:
                assert linked_list.end is not None
                new_node.prev = linked_list.end
                linked_list.end.next = new_node
                linked_list.end = new_node

        linked_list._rebuild_playback_links()
        return linked_list

    @classmethod
    def from_json_file(cls, file_path: str | Path) -> LinkedList:
        with open(file_path, "r", encoding="utf-8") as file:
            songs: list[dict[str, str]] = json.load(file)

        return cls.from_iterable(songs)
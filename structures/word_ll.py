from __future__ import annotations
from typing import Optional


class WordNode:
    def __init__(
            self,
            val: str,
            translation: Optional[str],
            count: int,
            next: Optional[WordNode] = None
            ) -> None:
        self.val = val
        self.translation = translation
        self.count = count
        self.next = next

    def __str__(self) -> str:
        return f'{self.val} - {self.translation}'

    def __repr__(self) -> str:
        return f'{self.val} shows {self.count} in the text.'


class WordStorage:
    def __init__(self) -> None:
        self.head = None

    def __str__(self) -> str:
        return f'Word list with {self.head.val} as a head.'

    def __repr__(self) -> str:
        return f'Storage includes {self.size()} words.'

    def __iter__(self) -> Optional[WordNode]:
        if not self.head:
            return None
        current = self.head
        while current:
            yield current
            current = current.next

    def __len__(self) -> int:
        return self.size()

    def append(self, word, count, translation) -> None:
        new_node = WordNode(
            val=word,
            translation=translation,
            count=count
        )
        if not self.head:
            self.head = new_node
        else:
            last_node = self.get_last()
            last_node.next = new_node

    def get_last(self) -> Optional[WordNode]:
        if not self.head:
            return None
        current = self.head
        while current.next:
            current = current.next
        return current

    def size(self) -> int:
        counter = 0
        current = self.head
        while current:
            counter += 1
            current = current.next
        return counter

    def in_list(self, word) -> bool:
        if not self.head:
            return False
        current = self.head
        while current:
            if word == current.val:
                return True
            current = current.next
        return False

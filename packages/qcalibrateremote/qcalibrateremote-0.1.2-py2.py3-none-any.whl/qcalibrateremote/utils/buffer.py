import logging
from queue import Queue
from typing import Callable, Generator, Generic, TypeVar

from icecream import ic

TItem = TypeVar('TItem')


class QueueBuffer(Generic[TItem]):
    def __init__(
        self,
        is_end: Callable[[TItem], bool],
        timeout: float = None
    ) -> None:
        """[summary]

        Parameters
        ----------
        is_end : Callable[[TItem], bool]
            check if an item is terminal message
        timeout : float, optional
            Timeout in seconds to wait for a remote reply, by default None - wait forever
        """
        self._queue = Queue()
        self._timeout = timeout
        self._finished = False
        self._is_end = is_end

    def put(self, request: TItem) -> None:
        ic("QueueBuffer.put", request)
        if not self._finished:
            if not request or self._is_end(request):
                self._finished = True
            self._queue.put(request)
        else:
            logging.warn("Send after end %s", request)

    def get(self) -> Generator[TItem, None, None]:
        run = True
        while run:
            next: TItem = self._queue.get(timeout=self._timeout)
            if next:
                ic("QueueBuffer.__next__", next)
                yield next
                if self._is_end(next):
                    run = False
            else:
                run = False

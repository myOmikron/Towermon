from dataclasses import field, dataclass
from typing import Union, Tuple

import numpy as np

from . import JitCmp

number = Union[int, float]


@dataclass()
class Vector2:
    _data: np.array = field(init=False, default_factory=lambda: np.zeros([0, 0]))

    def __init__(self, data: Union[Tuple[number, number], np.ndarray]):
        if isinstance(data, Tuple):
            self._data = np.array([data[0], data[1]]).astype(np.float32)
        elif isinstance(data, np.ndarray):
            self._data = data.astype(np.float32)
        else:
            raise NotImplementedError(f"Cant instantiate Vector2 from {data}")

    @property
    def x(self):
        return self._data[0]

    @property
    def y(self):
        return self._data[1]

    def distance(self, other) -> float:
        """
        Calculates the Euclidian distance between self and the other Vector2
        :param other: Vector2
        :return: float
        """
        if isinstance(other, Vector2):
            # print(f"Distance Type: {self._data, other._data}")
            return JitCmp.distance(self._data, other._data)
        raise TypeError(f"other is not from type Vector2: {type(other)}")

    def _length(self) -> float:
        return JitCmp.length(self._data)

    def _add(self, other):
        if isinstance(other, Vector2):
            # print(f"Add Type: {self._data, other._data}")
            return Vector2(JitCmp.add(self._data, other._data))
        raise TypeError(f"other is not from type Vector2: {type(other)}")

    def _sub(self, other):
        if isinstance(other, Vector2):
            # print(f"Sub Type: {self._data, other._data}")
            return Vector2(JitCmp.sub(self._data, other._data))
        raise TypeError(f"other is not from type Vector2: {type(other)}")

    def _hash(self):
        return hash((self.x, self.y))

    def _equals(self, other):
        if isinstance(other, Vector2):
            # print(f"Equals Type: {self._data, other._data}")
            return JitCmp.equals(self._data, other._data)
        raise TypeError(f"other is not from type Vector2: {type(other)}")

    def uniform(self):
        """
        returns a new uniformed Vector2
        :return: Vector2
        """
        return JitCmp.uniform(self._data)

    def direction(self, other):
        """
        Calculates the direction Vector from 2 Vector2
        :param other: Vector2
        :return: Vector2
        """
        # print(f"Direction Type: {self._data, other._data}")
        if isinstance(other, Vector2):
            return Vector2(JitCmp.direction(self._data, other._data))
        raise TypeError(f"other is not from type Vector2: {type(other)}")

    def angle_from_direction(self) -> float:
        """
        calculate the current angle in degrees from the direction vector
        :return: the angle in degrees, if y is 0 it always returns 0
        """
        if self.y > 0:
            return JitCmp.angle(self._data)
        return 0

    def update(self, direction, speed: float, delta_time: float) -> None:
        """
        Update the current Vector 2 by given speed and delta-time
        :param direction: Vector2
        :param speed: float
        :param delta_time: float
        :return: None
        """
        self._data = JitCmp.update(self._data, direction._data, speed, delta_time)

    def copy(self):
        """
        Copy a Vector2
        :return: new Vector2
        """
        return Vector2(self._data.copy())

    def __copy__(self):
        return self.copy()

    def __len__(self):
        return self._length()

    def __add__(self, other):
        return self._add(other)

    def __sub__(self, other):
        return self._sub(other)

    def __hash__(self):
        return self._hash()

    def __eq__(self, other):
        return self._equals(other)

    def __repr__(self):
        return f"{self.x, self.y}"

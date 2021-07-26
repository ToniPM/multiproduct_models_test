from typing import Iterable
import numpy as np

from xp import xp
from ProductMove import ProductMove
from State import State


class ForgetfulState(State):
    def __init__(self):
        self.targets = xp.zeros((0, 0))

    @classmethod
    def from_target_matrix(cls, target_matrix):
        self = cls()
        self.targets = target_matrix
        return self

    @classmethod
    def from_targets(cls, targets):
        self = cls()
        qt_targets = len(targets)
        max_index = max((max(item) for item in targets))
        self.targets = xp.zeros((max_index+1, qt_targets), dtype=bool)
        for i, target in enumerate(targets):
            for j in target:
                self.targets[j, i] = True
        return self

    def remove_empty_indices(self):
        is_nonzero = xp.max(self.targets, axis=1)
        nonzero_indices = xp.where(is_nonzero)
        self.targets = self.targets[nonzero_indices]

    @property
    def max_index(self):
        return self.targets.shape[0]-1

    @property
    def qt_targets(self):
        return self.targets.shape[1]

    def available_moves(self) -> Iterable[ProductMove]:
        pairs = xp.sum(self.targets[xp.newaxis, :, :] * self.targets[:, xp.newaxis, :], axis=2)
        for i,j in zip(*np.triu_indices(self.max_index+1, k=1)):
            if pairs[i,j]:
                yield ProductMove(i,j)

    def is_finished(self) -> bool:
        return xp.all(xp.sum(self.targets, axis=0) == 1).astype(bool)

    def qt_finished(self) -> bool:
        return xp.sum(xp.sum(self.targets, axis=0) == 1).astype(int)

    def move(self, move: ProductMove) -> State:
        position = xp.all(self.targets[[move.i1, move.i2],:], axis=0)
        new_targets = xp.concatenate((self.targets, position[xp.newaxis, :]), axis=0)
        new_targets[move.i1] ^= position
        new_targets[move.i2] ^= position
        return ForgetfulState.from_target_matrix(new_targets)


# var_index x item_index
# (jesus christ this is inefficient)
class OvercomplicatedState:
    def __init__(self, max_index):
        self.known = xp.identity(max_index+1, dtype=bool)
        self.targets = xp.zeros((0, 0), dtype=bool)

    @classmethod
    def from_target_matrix(cls, target_matrix):
        max_index, qt_targets = target_matrix.shape
        max_index -= 1
        self = cls(max_index)
        self.targets = target_matrix
        return self

    @classmethod
    def from_targets(cls, targets):
        qt_targets = len(targets)
        max_index = max((max(item) for item in targets))
        self = cls(max_index)
        self.targets = xp.zeros((max_index+1, qt_targets), dtype=bool)
        for i, target in enumerate(targets):
            for j in target:
                self.targets[j, i] = True
        return self

    @property
    def max_index(self):
        return self.targets.shape[0]-1

    @property
    def qt_targets(self):
        return self.targets.shape[1]

    @property
    def qt_known(self):
        return self.known.shape[1]

    def available_moves(self) -> Iterable[ProductMove]:
        pairs = np.max(self.known[:,np.newaxis,:]*self.known[:,:,np.newaxis],axis=0)
        already_computed = np.any(np.all(self.known[:,np.newaxis,np.newaxis,:]==(self.known[:,np.newaxis,:] ^ self.known[:,:,np.newaxis])[...,np.newaxis], axis=0), axis=-1)
        for i, j in zip(*np.triu_indices(self.qt_known, k=1)):
            if not pairs[i, j] and not already_computed[i, j]:
                yield ProductMove(i,j)

    def is_finished(self) -> bool:
        return xp.all(xp.any(xp.all(self.targets[:,:,np.newaxis] == self.known[:,np.newaxis,:], axis=0), axis=1), axis=0).astype(bool)

    def move(self, move: ProductMove) -> State:
        computed = self.known[:, move.i1] ^ self.known[:,move.i2]
        new_state = OvercomplicatedState.from_target_matrix(self.targets)
        new_state.known = xp.concatenate((self.known, computed[:,np.newaxis]), axis=1)
        return new_state


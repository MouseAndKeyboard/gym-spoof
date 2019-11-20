from gym.spaces import Space
import numpy as np

class Categorical(Space):

    def __init__(self, n):
        assert n >= 1
        self.n = n
        super(Categorical, self).__init__((), np.int64)

    def sample(self):
        """Randomly sample an element of this space. Can be 
        uniform or non-uniform sampling based on boundedness of space."""
        index = self.np_random.randint(low=0, high=self.n, )
        arr = np.eye(self.n)[index]
        return arr

    def contains(self, x):
        """ If x is a valid index of the type then will return True
        """
        
        if isinstance(x, int):
            as_int = x
        elif isinstance(x, (np.generic, np.ndarray)) and (x.dtype.kind in np.typecodes['AllInteger'] and x.shape == ()):
            as_int = int(x)
        else:
            return False

        return as_int >= 0 and as_int < self.n

    def __repr__(self):
        return "Categorical({})".format(self.n)

    def __eq__(self, other):
        return isinstance(other, Categorical) and self.n == other.n
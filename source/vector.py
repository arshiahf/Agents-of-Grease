import math


def polar_to_vector2(radians: float, hypotenuse: float) -> "Vector2":
    x_pos = math.cos(radians) * hypotenuse
    y_pos = math.sin(radians) * hypotenuse
    polar_vector = Vector2(x_pos, y_pos)
    return polar_vector


def dot(vector1: "Vector", vector2: "Vector") -> float:

    if not issubclass(vector1.__class__, Vector) or not issubclass(vector2.__class__, Vector):

        raise TypeError("Both items given must be vectors")
        return None

    elif len(vector1) != len(vector2):

        raise ValueError("Both vectors must be of same dimension (length)")
        return None

    dot_product = 0.0
    vector1_math = vector1.copy()
    vector2_math = vector2.copy()

    for dimension in range(len(vector1_math)):
        dot_product += vector1_math[dimension] * vector2_math[dimension]

    return dot_product


def cross(vector1: "Vector3", vector2: "Vector3") -> "Vector3":

    if not issubclass(vector1.__class__, Vector3) or not issubclass(vector2.__class__, Vector3):

        raise TypeError("Both items given must be 3 dimensional vectors")
        return None

    cross_product = Vector3(0, 0, 0)
    vector1_math = vector1.copy()
    vector2_math = vector2.copy()

    cross_product[0] = vector1_math[1] * \
        vector2_math[2] - vector1_math[2] * vector2_math[1]
    cross_product[1] = -1 * (vector1_math[0] *
                             vector2_math[2] - vector1_math[2] * vector2_math[0])
    cross_product[2] = vector1_math[0] * \
        vector2_math[1] - vector1_math[1] * vector2_math[0]

    return cross_product


class Vector:

    def __init__(self, *args):
        self.mData = []
        for arg in args:
            arg = float(arg)
            self.mData.append(arg)
        self.mDim = len(self.mData)
        if self.mDim == 2:
            self.__class__ = Vector2
        elif self.mDim == 3:
            self.__class__ = Vector3

    def __str__(self):
        vector_string = "<Vector" + str(self.mDim) + ": "
        for i in range(self.mDim):
            vector_string += str(self.mData[i])
            if i < self.mDim - 1:
                vector_string += ", "
        vector_string += ">"
        return vector_string

    def __len__(self):
        return self.mDim

    def __getitem__(self, index: int):
        return self.mData[index]

    def __setitem__(self, index: int, new_value):
        self.mData[index] = float(new_value)

    def __add__(self, add_vector: "Vector"):
        return_vector = self.copy()
        for i in range(self.mDim):
            return_vector[i] += add_vector[i]
        return return_vector

    def __sub__(self, sub_vector: "Vector"):
        return_vector = self.copy()
        for i in range(self.mDim):
            return_vector[i] -= sub_vector[i]
        return return_vector

    def __mul__(self, scalar: float):
        return_vector = self.copy()
        for i in range(self.mDim):
            return_vector[i] *= scalar
        return return_vector

    def __rmul__(self, scalar: float):
        return_vector = self.copy()
        for i in range(self.mDim):
            return_vector[i] *= scalar
        return return_vector

    def __truediv__(self, scalar: float):
        return_vector = self.copy()
        for i in range(self.mDim):
            return_vector[i] /= scalar
        return return_vector

    def __neg__(self):
        return_vector = self.copy()
        for i in range(self.mDim):
            return_vector[i] = -return_vector[i]
        return return_vector

    def __eq__(self, other_vector):
        if not issubclass(other_vector.__class__, self.__class__):
            return False
        for i in range(self.mDim):
            if self.mData[i] != other_vector[i]:
                return False
        return True

    def copy(self):
        new_vector = Vector(*self.mData)
        return new_vector

    @property
    def i(self):
        temp_ints = [*self.mData]
        for i in range(len(temp_ints)):
            temp_ints[i] = int(temp_ints[i])
        return tuple(temp_ints)

    @property
    def magnitude(self):
        total_magnitude = 0.0
        for i in range(self.mDim):
            total_magnitude += self.mData[i] ** 2
        total_magnitude = total_magnitude ** (1/2)
        return total_magnitude

    @property
    def magnitude_squared(self):
        total_magnitude = 0.0
        for i in range(self.mDim):
            total_magnitude += self.mData[i] ** 2
        return total_magnitude

    @property
    def normalized(self):
        temp_vector = self.copy()
        true_magnitude = self.magnitude
        if true_magnitude == 0.0:
            return temp_vector
        for i in range(self.mDim):
            temp_vector[i] /= true_magnitude
        return temp_vector

    @property
    def is_zero(self):
        for mData in self.mData:
            if mData != 0:
                return False
        return True


class Vector2(Vector):

    def __init__(self, x: float, y: float):
        super().__init__(x, y)

    @property
    def x(self):
        return self.mData[0]

    @x.setter
    def x(self, new_value: float):
        self.mData[0] = float(new_value)

    @property
    def y(self):
        return self.mData[1]

    @y.setter
    def y(self, new_value: float):
        self.mData[1] = float(new_value)

    @property
    def degrees(self):
        return math.atan2(self.mData[1], self.mData[0]) * 180/math.pi

    @property
    def radians(self):
        return math.atan2(self.mData[1], self.mData[0])

    def copy(self):
        new_vector = Vector2(*self.mData)
        return new_vector


class Vector3(Vector):

    def __init__(self, x: float, y: float, z: float):
        super().__init__(x, y, z)

    @property
    def x(self):
        return self.mData[0]

    @x.setter
    def x(self, new_value: float):
        self.mData[0] = float(new_value)

    @property
    def y(self):
        return self.mData[1]

    @y.setter
    def y(self, new_value: float):
        self.mData[1] = float(new_value)

    @property
    def z(self):
        return self.mData[2]

    @z.setter
    def z(self, new_value: float):
        self.mData[2] = float(new_value)

    def copy(self):
        new_vector = Vector3(*self.mData)
        return new_vector

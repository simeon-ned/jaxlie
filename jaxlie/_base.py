import abc
from typing import TypeVar, overload

from ._types import Matrix, TangentVector, Vector

T = TypeVar("T", bound="MatrixLieGroup")


class MatrixLieGroup(abc.ABC):

    # Class properties
    # > These will be set in `_utils.register_lie_group()`

    matrix_dim: int
    parameters_dim: int
    tangent_dim: int

    # Shared implementations

    @overload
    def __matmul__(self: T, other: T) -> T:
        ...

    @overload
    def __matmul__(self: T, other: Vector) -> Vector:
        ...

    def __matmul__(self, other):
        """Operator overload, for composing transformations and/or applying them to
        points.
        """
        if type(self) is type(other):
            return self.product(other=other)
        elif isinstance(other, Vector):
            return self.apply(target=other)
        else:
            assert False, "Invalid argument"

    # Factory

    @staticmethod
    @abc.abstractmethod
    def identity() -> "MatrixLieGroup":
        """Returns identity element.

        Returns:
            Matrix: Identity.
        """

    @staticmethod
    @abc.abstractmethod
    def from_matrix(matrix: Matrix) -> "MatrixLieGroup":
        """Get group member from matrix representation.

        Args:
            matrix (jnp.ndarray): Matrix representaiton.

        Returns:
            T: Group member.
        """

    # Accessors

    @abc.abstractmethod
    def as_matrix(self) -> Matrix:
        """Get value as a matrix."""

    @property
    @abc.abstractmethod
    def parameters(self) -> Vector:
        """Get underlying representation."""

    # Operations

    @abc.abstractmethod
    def apply(self: T, target: Vector) -> Vector:
        """Applies transformation to a vector.

        Args:
            target (Vector): Vector to transform.

        Returns:
            Vector: Transformed vector.
        """

    @abc.abstractmethod
    def product(self: T, other: T) -> T:
        """Left-multiplies this transformations with another.

        Args:
            other (T): other

        Returns:
            T: self @ other
        """

    @staticmethod
    @abc.abstractmethod
    def exp(tangent: TangentVector) -> "MatrixLieGroup":
        """Computes `expm(wedge(tangent))`.

        Args:
            tangent (TangentVector): Input.

        Returns:
            Matrix: Output.
        """

    @abc.abstractmethod
    def log(self: T) -> TangentVector:
        """Computes `vee(logm(transformation matrix))`.

        Args:
            x (Matrix): Input.

        Returns:
            TangentVector: Output.
        """

    @abc.abstractmethod
    def inverse(self: T) -> T:
        """Computes the inverse of x.

        Args:
            x (Matrix): Input.

        Returns:
            Matrix: Output.
        """

    @abc.abstractmethod
    def normalize(self: T) -> T:
        """Normalize/projects values and returns.

        Returns:
            T: Normalized group member.
        """

from functools import reduce
import operator


class Expr:
    """Base class for all other expressions."""

    def eval(self, rec):
        """return True if condition is satisfied on a given record, False otherwise."""
        raise NotImplementedError("Each subclass must implement `eval` method.")


class NAryExpr(Expr):
    """Implementation of the n-ary operation (OR, AND).

    These expressions can have multiple operands, and are evaluated to a single bool.
    """

    def __init__(self, op_str, operands):
        self._op_str = op_str
        self._operands = operands

    @property
    def op(self):
        return {"OR": operator.or_, "AND": operator.and_}[self._op_str]

    def eval(self, rec):
        """return True if condition is satisfied on a given record, False otherwise."""
        return reduce(self.op, [n.eval(rec) for n in self._operands])


class BinaryExpr(Expr):
    """Implementation of the binary op (<, >, <=, >=, =)."""

    def __init__(self, op_str, field, val):
        self._op_str = op_str
        self._field = field
        self._val = val

    @property
    def op(self):
        """operator from python operator module, based on operation name (str).

        This operator will be used for expression evaluation.
        """
        return {
            "<": operator.lt,
            "<=": operator.le,
            ">": operator.gt,
            ">=": operator.ge,
            "=": operator.eq,
            "LIKE": operator.contains,
        }[self._op_str]

    def eval(self, rec):
        """return True if condition is satisfied on a given record, False otherwise."""
        return self.op(self._field_val(rec), self.val)

    @property
    def val(self):
        """int value of right-hand side expression, if convertible, str otherwise."""
        try:
            return int(self._val)
        except ValueError:
            return self._val

    def _field_val(self, rec):
        """return dictionary entry from the input table record, based on field name."""
        return rec[self._field]


class LiteralExpr(Expr):
    """Implementation of single value literals like True and False.

    The class serves to enable generic evaluation of the expressions with `eval`.
    """

    def __init__(self, val):
        self._val = val

    def eval(self, rec):
        return bool(self._val)

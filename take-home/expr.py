from functools import reduce
import operator


class Expr:
    def eval(self, rec):
        raise ValueError("Must subclass")


class NAryExpr(Expr):
    def __init__(self, op, nodes):
        self._op = op
        self._nodes = nodes

    @property
    def op(self):
        return {"OR": operator.or_, "AND": operator.and_}[self._op]

    def eval(self, rec):
        return reduce(self.op, [n.eval(rec) for n in self._nodes])


class BinaryExpr(Expr):
    def __init__(self, op, field, val):
        self._op = op
        self._field = field
        self._val = val

    @property
    def op(self):
        return {
            "<": operator.lt,
            "<=": operator.le,
            ">": operator.gt,
            ">=": operator.ge,
            "=": operator.eq,
            "LIKE": operator.contains,
        }[self._op]

    def eval(self, rec):
        return self.op(self._field_val(rec), self.val)

    @property
    def val(self):
        try:
            return int(self._val)
        except ValueError:
            return self._val

    def _field_val(self, rec):
        return rec[self._field]


class LiteralExpr(Expr):
    def __init__(self, val):
        self._val = val

    def eval(self, rec):
        return bool(self._val)

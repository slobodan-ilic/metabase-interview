from expr import NAryExpr, BinaryExpr, LiteralExpr


class Parser:
    def __init__(self, expr):
        self._expr = expr

    @property
    def expr(self):
        return self._parse_expr(self._expr)

    def _parse_expr(self, expression):
        expr = expression.strip()
        or_tokens = expr.split("OR")
        and_tokens = expr.split("AND")
        if len(or_tokens) > 1:
            return NAryExpr("OR", [self._parse_expr(e) for e in or_tokens])
        elif len(and_tokens) > 1:
            return NAryExpr("AND", [self._parse_expr(e) for e in and_tokens])

        tokens = expr.split(" ")
        if len(tokens) == 1:
            return LiteralExpr(expr)

        field, op, val = tokens
        return BinaryExpr(op, field, val)


class Filter:
    def __init__(self, table, expr):
        self._table = table
        self._expr = expr

    @property
    def table(self):
        return [rec for rec in self._table if self.expr.eval(rec)]

    @property
    def expr(self):
        return Parser(self._expr).expr


class Query:
    def __init__(self, db, query):
        self._db = db
        self._query = query

    @property
    def _table_name(self):
        return self._query.split("FROM")[-1].strip().split(" ")[0]

    @property
    def _filter_expr(self):
        tokens = self._query.split("WHERE")
        if len(tokens) == 1:
            return None
        return self._query.split("WHERE")[-1].strip()

    @property
    def _table(self):
        return self._db[self._table_name]

    @property
    def _filtered_table(self):
        if self._filter_expr is None:
            return self._table
        return Filter(self._table, self._filter_expr).table

    @property
    def _field_names(self):
        return [
            fn.strip()
            for fn in self._query.split("SELECT")[1].strip().split("FROM")[0].split(",")
        ]

    @property
    def result(self):
        if self._field_names == ["*"]:
            return self._filtered_table
        return [
            {fn: rec[fn] for fn in self._field_names} for rec in self._filtered_table
        ]

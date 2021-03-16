import pytest
from expr import BinaryExpr, NAryExpr
from query import Filter, Parser, Query


class TestExpr:
    def test_apply_simple_binary_expr_false(self):
        expr = BinaryExpr("<", "id", "3")
        assert expr.eval({"id": 4}) is False

    def test_apply_simple_binary_expr_true(self):
        expr = BinaryExpr("<", "id", "5")
        assert expr.eval({"id": 3}) is True

    def test_apply_simple_nary_expr_true(self):
        be1 = BinaryExpr("<", "id", "5")
        be2 = BinaryExpr(">", "id", "2")
        expr = NAryExpr("AND", [be1, be2])
        assert expr.eval({"id": 3}) is True

    def test_apply_simple_nary_expr_false(self):
        be1 = BinaryExpr("<", "id", "5")
        be2 = BinaryExpr(">", "id", "2")
        expr = NAryExpr("AND", [be1, be2])
        assert expr.eval({"id": 1}) is False

    def test_apply_complex_expr(self):
        be1 = BinaryExpr("<", "id", "5")
        be2 = BinaryExpr(">", "id", "2")
        be3 = BinaryExpr("=", "owner_id", "1")
        expr = NAryExpr("OR", [NAryExpr("AND", [be1, be2]), be3])
        assert expr.eval({"id": 1, "owner_id": 1}) is True
        assert expr.eval({"id": 1, "owner_id": 2}) is False
        assert expr.eval({"id": 3, "owner_id": 2}) is True


class TestParser:
    def test_simple_binary_expr(self):
        expr = Parser("ID < 3").expr

        assert expr._op_str == "<"
        assert expr._field == "ID"
        assert expr._val == "3"

    def test_simple_nary_expr_or(self):
        expr = Parser("True OR False OR True").expr

        assert expr._op_str == "OR"
        assert [n._val for n in expr._operands] == ["True", "False", "True"]


class TestFilter:
    def test_simple_filtering(self, table_):
        filter_ = Filter(table_, "id > 1 AND owner_id = 1")
        assert filter_.table == [
            {"id": 2, "owner_id": 1, "name": "dog"},
            {"id": 3, "owner_id": 1, "name": "cat"},
        ]

    def test_double_logical_filtering(self, table_):
        filter_ = Filter(table_, "id = 3 OR owner_id = 2")
        assert filter_.table == [
            {"id": 1, "owner_id": 2, "name": "parrot"},
            {"id": 3, "owner_id": 1, "name": "cat"},
        ]

    def test_string_comparison(self, table_):
        filter_ = Filter(table_, "name = parrot")
        assert filter_.table == [
            {"id": 1, "owner_id": 2, "name": "parrot"},
        ]

    def test_string_contains(self, table_):
        filter_ = Filter(table_, "name LIKE par")
        assert filter_.table == [
            {"id": 1, "owner_id": 2, "name": "parrot"},
        ]

    @pytest.fixture
    def table_(self):
        return [
            {"id": 1, "owner_id": 2, "name": "parrot"},
            {"id": 2, "owner_id": 1, "name": "dog"},
            {"id": 3, "owner_id": 1, "name": "cat"},
        ]


class TestQuery:
    def test_simple_table_name(self):
        query = Query(None, "SELECT * FROM persons")
        assert query._table_name == "persons"

    def test_simple_table_name_with_fields(self):
        query = Query(None, "SELECT id, name FROM persons")
        assert query._table_name == "persons"

    def test_simple_table_name_with_fields_and_filter(self):
        query = Query(None, "SELECT id, name FROM persons WHERE id > 3")
        assert query._table_name == "persons"

    def test_filtered_table_all_fields(self, db_):
        query = Query(db_, "SELECT * FROM people WHERE id > 1")
        assert query._filtered_table == [{"id": 2, "name": "Jill"}]

    def test_result_selected_fields(self, db_):
        query = Query(db_, "SELECT name FROM people WHERE id = 1")
        assert query.result == [{"name": "Jake"}]
        query = Query(db_, "SELECT id FROM people WHERE id = 1")
        assert query.result == [{"id": 1}]
        query = Query(db_, "SELECT id, name FROM people WHERE id = 1")
        assert query.result == [{"id": 1, "name": "Jake"}]
        query = Query(db_, "SELECT * FROM people WHERE id = 1")
        assert query.result == [{"id": 1, "name": "Jake"}]

    @pytest.fixture
    def db_(self):
        return {
            "people": [
                {"id": 1, "name": "Jake"},
                {"id": 2, "name": "Jill"},
            ],
            "pets": [
                {"id": 1, "owner_id": 2, "name": "parrot"},
                {"id": 2, "owner_id": 1, "name": "dog"},
                {"id": 3, "owner_id": 1, "name": "cat"},
            ],
        }

import pytest
from query import Query


class TestQuery:
    def test_case_1_simple_example_select_all(self, db_):
        query = Query(db_, "SELECT * FROM people")
        assert query.result == [
            {"id": 1, "name": "Cam Saul"},
            {"id": 2, "name": "Cam Era"},
        ]

    def test_case_2_simple_example_where_with_equals(self, db_):
        query = Query(db_, "SELECT * FROM people WHERE id = 2")
        assert query.result == [
            {"id": 2, "name": "Cam Era"},
        ]

    def test_case_3_simple_example_where_with_greater_then(self, db_):
        query = Query(db_, "SELECT * FROM birds WHERE id > 4")
        assert query.result == [
            {"id": 5, "name": "Lucky Pigeon", "owner_id": 1},
            {"id": 6, "name": "Rasta Toucan", "owner_id": 1},
        ]

    def test_case_4_simple_example_single_field(self, db_):
        query = Query(db_, "SELECT name FROM people")
        assert query.result == [
            {"name": "Cam Saul"},
            {"name": "Cam Era"},
        ]

    def test_case_5_simple_example_multiple_fields(self, db_):
        query = Query(db_, "SELECT id, name FROM people")
        assert query.result == [
            {"id": 1, "name": "Cam Saul"},
            {"id": 2, "name": "Cam Era"},
        ]

    def test_case_6_bonus_compound_where(self, db_):
        query = Query(db_, "SELECT * FROM birds WHERE owner_id = 1 AND id > 2")
        assert query.result == [
            {"id": 3, "name": "Lime Parakeet", "owner_id": 1},
            {"id": 4, "name": "Katie Parakeet", "owner_id": 1},
            {"id": 5, "name": "Lucky Pigeon", "owner_id": 1},
            {"id": 6, "name": "Rasta Toucan", "owner_id": 1},
        ]

    def test_extra_logical_conditions(self, db_):
        query = Query(db_, "SELECT id, name FROM birds WHERE name LIKE Lucky OR id = 2")
        assert query.result == [
            {"id": 2, "name": "Lemon Parakeet"},
            {"id": 5, "name": "Lucky Pigeon"},
        ]

    @pytest.fixture
    def db_(self):
        return {
            "people": [
                {"id": 1, "name": "Cam Saul"},
                {"id": 2, "name": "Cam Era"},
            ],
            "birds": [
                {"id": 1, "name": "Parroty Parakeet", "owner_id": 1},
                {"id": 2, "name": "Lemon Parakeet", "owner_id": 1},
                {"id": 3, "name": "Lime Parakeet", "owner_id": 1},
                {"id": 4, "name": "Katie Parakeet", "owner_id": 1},
                {"id": 5, "name": "Lucky Pigeon", "owner_id": 1},
                {"id": 6, "name": "Rasta Toucan", "owner_id": 1},
            ],
        }

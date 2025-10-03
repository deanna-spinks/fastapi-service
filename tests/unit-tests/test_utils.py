import pytest

from src.utils.id_generator import get_next_id


@pytest.mark.unit
class TestIdGenerator:
    """Test ID generator utility"""

    def test_get_next_id_increments(self):
        """Test that get_next_id returns incrementing integer values"""
        id1 = get_next_id()
        id2 = get_next_id()
        id3 = get_next_id()

        assert id2 == id1 + 1
        assert id3 == id2 + 1

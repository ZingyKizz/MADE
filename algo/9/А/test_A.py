import pytest
import random
from stuff_for_tests import FakeCartesianTree
from A import CartesianTree

OPERATIONS = ["insert", "delete", "exists", "prev", "next"]
SMALL_CASES = 10
LARGE_CASES = 100
RANDOM_TESTS_COUNT = 10000


@pytest.fixture()
def bst():
    return CartesianTree()


def test_can_insert(bst):
    bst.insert(1)


def test_can_exists(bst):
    assert bst.exists(1) == "false"


def test_can_exists_after_insert(bst):
    bst.insert(1)
    assert bst.exists(1) == "true"


def test_can_delete(bst):
    bst.delete(1)


def test_can_exists_after_delete(bst):
    bst.insert(1)
    bst.delete(1)
    assert bst.exists(1) == "false"


def test_can_prev(bst):
    assert bst.prev(1) == "none"


def test_can_prev_after_insert(bst):
    bst.insert(2)
    bst.insert(1)
    assert bst.prev(2) == 1
    assert bst.prev(1) == "none"
    bst.insert(8)
    bst.insert(9)
    bst.insert(10)
    assert bst.prev(10) == 9
    assert bst.prev(11) == 10
    assert bst.prev(0) == "none"
    assert bst.prev(9) == 8
    assert bst.prev(8) == 2
    bst.insert(-8)
    assert bst.prev(0) == -8
    assert bst.prev(1) == -8
    assert bst.prev(100) == 10
    bst.insert(101)
    assert bst.prev(101) == 10
    assert bst.prev(120) == 101
    assert bst.prev(-323) == "none"


def test_can_next(bst):
    assert bst.next(1) == "none"


def test_can_next_after_insert(bst):
    bst.insert(1)
    bst.insert(2)
    assert bst.next(2) == "none"
    assert bst.next(1) == 2


def test_simple_operations_case(bst):
    bst.insert(3)
    assert bst.exists(3) == "true"
    assert bst.exists(4) == "false"
    bst.insert(4)
    assert bst.next(4) == "none"
    assert bst.prev(3) == "none"
    assert bst.next(3) == 4
    assert bst.prev(4) == 3
    bst.delete(2)
    bst.delete(3)
    assert bst.prev(4) == "none"
    assert bst.next(3) == 4


def test_codeforces_case(bst):
    bst.insert(2)
    bst.insert(5)
    bst.insert(3)
    assert bst.exists(2) == "true"
    assert bst.exists(4) == "false"
    assert bst.next(4) == 5
    assert bst.prev(4) == 3
    bst.delete(5)
    assert bst.next(4) == "none"
    assert bst.prev(4) == 3


def _test_random_helper(operations, *, n_oprs, excluded=None):
    bst = CartesianTree()
    fbst = FakeCartesianTree()
    if excluded is not None:
        operations = [o for o in operations if o not in excluded]
    oprs = random.choices(operations, k=n_oprs)
    values = [random.randint(-10, 10) for _ in range(n_oprs)]

    script = "bst = CartesianTree()\n" \
             "fbst = FakeCartesianTree()\n"
    for opr, val in zip(oprs, values):
        script += f"bst.{opr}({val})\n"\
                  f"fbst.{opr}({val})\n"
        if opr == "insert":
            bst.insert(val)
            fbst.insert(val)
        elif opr == "delete":
            bst.delete(val)
            fbst.delete(val)
        elif opr == "exists":
            assert bst.exists(val) == fbst.exists(val), (
                script
            )
        elif opr == "prev":
            assert bst.prev(val) == fbst.prev(val), (
                script
            )
        elif opr == "next":
            assert bst.next(val) == fbst.next(val), (
                script
            )


def test_random_exclude_delete_prev_next_small_cases():
    for _ in range(RANDOM_TESTS_COUNT):
        _test_random_helper(OPERATIONS, n_oprs=SMALL_CASES, excluded=["delete", "next", "prev"])


def test_random_exclude_delete_prev_next_large_cases():
    for _ in range(RANDOM_TESTS_COUNT):
        _test_random_helper(OPERATIONS, n_oprs=LARGE_CASES, excluded=["delete", "next", "prev"])


def test_random_exclude_delete_next_small_cases():
    for _ in range(RANDOM_TESTS_COUNT):
        _test_random_helper(OPERATIONS, n_oprs=SMALL_CASES, excluded=["delete", "next"])


def test_random_exclude_delete_next_large_cases():
    for _ in range(RANDOM_TESTS_COUNT):
        _test_random_helper(OPERATIONS, n_oprs=LARGE_CASES, excluded=["delete", "next"])


def test_random_exclude_prev_next_small_cases():
    for _ in range(RANDOM_TESTS_COUNT):
        _test_random_helper(OPERATIONS, n_oprs=SMALL_CASES, excluded=["prev", "next"])


def test_random_exclude_prev_next_large_cases():
    for _ in range(RANDOM_TESTS_COUNT):
        _test_random_helper(OPERATIONS, n_oprs=LARGE_CASES, excluded=["prev", "next"])


def test_random_exclude_delete_prev_small_cases():
    for _ in range(RANDOM_TESTS_COUNT):
        _test_random_helper(OPERATIONS, n_oprs=SMALL_CASES, excluded=["delete", "prev"])


def test_random_exclude_delete_prev_large_cases():
    for _ in range(RANDOM_TESTS_COUNT):
        _test_random_helper(OPERATIONS, n_oprs=LARGE_CASES, excluded=["delete", "prev"])


def test_random_exclude_prev_small_cases():
    for _ in range(RANDOM_TESTS_COUNT):
        _test_random_helper(OPERATIONS, n_oprs=SMALL_CASES, excluded=["prev"])


def test_random_exclude_prev_large_cases():
    for _ in range(RANDOM_TESTS_COUNT):
        _test_random_helper(OPERATIONS, n_oprs=LARGE_CASES, excluded=["prev"])


def test_random_exclude_next_small_cases():
    for _ in range(RANDOM_TESTS_COUNT):
        _test_random_helper(OPERATIONS, n_oprs=SMALL_CASES, excluded=["next"])


def test_random_exclude_next_large_cases():
    for _ in range(RANDOM_TESTS_COUNT):
        _test_random_helper(OPERATIONS, n_oprs=LARGE_CASES, excluded=["next"])


def test_random_small_cases():
    for _ in range(RANDOM_TESTS_COUNT):
        _test_random_helper(OPERATIONS, n_oprs=SMALL_CASES)


def test_random_large_cases():
    for _ in range(RANDOM_TESTS_COUNT):
        _test_random_helper(OPERATIONS, n_oprs=LARGE_CASES)

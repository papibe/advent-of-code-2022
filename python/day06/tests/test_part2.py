import pytest

from part1 import solve


@pytest.mark.parametrize(
    "datastream,packet_size,expected",
    [
        ("mjqjpqmgbljsphdztnvjfqwrcgsmlb", 14, 19),
        ("bvwbjplbgvbhsrlpgdmjqwftvncz", 14, 23),
        ("nppdvjthqldpwncqszvftbrmjlhg", 14, 23),
        ("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 14, 29),
        ("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 14, 26),
    ],
    ids=[
        "mjqjpqmgbljsphdztnvjfqwrcgsmlb_shoud_be_7",
        "bvwbjplbgvbhsrlpgdmjqwftvncz_shoud_be_5",
        "nppdvjthqldpwncqszvftbrmjlhg_shoud_be_6",
        "nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg_shoud_be_10",
        "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw_shoud_be_11",
    ],
)
def test_part1_solve(datastream: str, packet_size: int, expected: int) -> None:
    result: int = solve(datastream, packet_size)
    assert result == expected, f"got {result}, needs {expected}"

from pl_extension.utilities import rand


def test_time_string():
    rand_str = rand.time_string()
    assert rand_str

import instadataeng as de


def test_key_not_found():
    ss = de.get_secret("xxyyz")
    assert ss is None

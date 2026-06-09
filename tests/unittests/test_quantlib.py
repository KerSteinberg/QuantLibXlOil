from quantlib_xloil import qlHexVersion, qlVersion


def test_qlVersion():

    version = qlVersion()
    assert isinstance(version, str)
    assert len(version) > 0


def test_qlHexVersion():
    hex_version = qlHexVersion()
    assert isinstance(hex_version, int)
    assert hex_version > 0

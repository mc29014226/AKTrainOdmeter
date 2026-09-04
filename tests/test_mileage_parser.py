from parsers.mileage_parser import MileageParser


def test_parse_latest_mileage():
    text = """
2026-09-04 00:03:34.137 INFO  [avlmanager.cpp      :462 ] VCU odometry update w/ meters 141499926, decimeters 7 and speed 1 km/h
2026-09-04 00:03:39.390 INFO  [avlmanager.cpp      :462 ] VCU odometry update w/ meters 141499928, decimeters 4 and speed 1 km/h
"""
    result = MileageParser().parse_latest(206, text)

    assert result.status == "ok"
    assert result.train_no == 206
    assert result.meters == 141499928
    assert result.decimeters == 4
    assert result.mileage_km == 141499.9284
    assert result.speed_kmh == 1
    assert result.timestamp == "2026-09-04 00:03:39.390"

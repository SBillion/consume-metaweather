from weather import get_city_woeid


def test_get_city_woeid_success():
    assert get_city_woeid("Paris") == 615702

def test_not_found_city_woeid():
    assert not get_city_woeid("Fdfsdfdsfsdf")


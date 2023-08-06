from moosetools.connect import AppConnect


def test_appconnect():
    cnt = AppConnect('https://server.com', username='user', password='pass')

    assert cnt.server == "https://server.com"
    assert cnt.username == "user"
    assert cnt.password == "pass"

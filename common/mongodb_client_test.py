import mongodb_client as client 

def test_basic():
    db = client.get_db("test")
    db.test.drop()
    assert db.test.count() == 0
    db.test.insert({"test": 1})
    assert db.test.count() == 1
    db.test.drop()
    assert db.test.count() == 0

    print('db basically works well')

if __name__ == '__main__':
    test_basic()


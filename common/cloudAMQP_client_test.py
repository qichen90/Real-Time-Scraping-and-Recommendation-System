from cloudAMQP_client import CloudAMQPClient

CLOUDAMQP_URL = 'amqp://zyxttdzy:CgfaZUfBCryGa5xfxdmJEfXSpVQZ-CN8@llama.rmq.cloudamqp.com/zyxttdzy'
QUEUE_NAME = 'test'

def test_basic():
    client = CloudAMQPClient(CLOUDAMQP_URL, QUEUE_NAME)

    sentMsg = {'test': 'test'}
    client.sendMessage(sentMsg)

    receivedMsg = client.getMessage()
    assert sentMsg == receivedMsg

    print('MQ basically works well')

if __name__ == '__main__':
    test_basic()


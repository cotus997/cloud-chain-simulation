import json

HTTP_URI = 'http://127.0.0.1:8545'
WEB_SOCKET_URI = 'ws://127.0.0.1:8546'

COMPILED_FACTORY_PATH = '../build/contracts/Factory.json'
COMPILED_ORACLE_PATH = '../build/contracts/FileDigestOracle.json'
COMPILED_CLOUD_SLA_PATH = '../build/contracts/CloudSLA.json'

RESULTS_CSV_DIR = 'results'

QUORUM_FACTORY_ADDRESS = '0xed78Cb21Ce10A086a7973fB44e96d34F31D45cF1'
QUORUM_ORACLE_ADDRESS = '0x4D2D24899c0B115a1fce8637FCa610Fe02f1909e'

POLYGON_FACTORY_ADDRESS = '0xD8DFE4694079eC670A70A5D06Bb33dA623169FB3'
POLYGON_ORACLE_ADDRESS = '0xb2f073b8b6C266785B1D6F9Bd8612B6E8C647A73'

# Preloaded accounts
quorum_accounts = [
    '0xFE3B557E8Fb62b89F4916B721be55cEb828dBd73',
    '0x627306090abaB3A6e1400e9345bC60c78a8BEf57',
    '0xf17f52151EbEF6C7334FAD080c5704D77216b732'
]
quorum_private_keys = [
    '0x8f2a55949038a9610f50fb23b5883af3b4ecb3c3bb792cbcefbd1542c692be63',
    '0xc87509a1c067bbde78beb793e6fa76530b6382a4c0241e5e4a9ec0a0f44dc0d3',
    '0xae6ae8e5ccbfb04590405997ee2d52d2b330726137b875053c36d94e974d162f'
]

with open('../polygon/src/address.json') as file:
    polygon_accounts = json.loads(file.read())['address']

with open('../polygon/src/private_keys.json') as file:
    polygon_private_keys = json.loads(file.read())['privatekey']

DEBUG = True
MIN_TIME = 1
MAX_TIME = 7200

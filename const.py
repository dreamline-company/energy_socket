PACKET_START_CHARACTER = '<'.encode()
PACKET_END_CHARACTER = str('>').encode()

DATA_START_CHARACTER = str('{').encode()
DATA_END_CHARACTER = str('}').encode()

REGISTER_NUM_VALUE_DELIMITER = str(':').encode()
REGISTER_DELIMITER = str(';').encode()
DATA_DELIMITER = str(',').encode()

REGULAR_PACKET_TYPE = str(1).encode()
EMERGENCY_PACKET_TYPE = str(2).encode()

SERVER_SEND_STATE = (2).to_bytes(1, "little")
REGULAR_PACKET_STATE = (1).to_bytes(1, "little")
EMERGENCY_PACKET_STATE = (0).to_bytes(1, "little")
OBJECT_ID = str(2).encode()
THREE = (3).to_bytes(1, "little")


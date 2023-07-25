PACKET_START_CHARACTER = ord('<').to_bytes(1, "little")
PACKET_END_CHARACTER = ord('>').to_bytes(1, "little")

DATA_START_CHARACTER = ord('{').to_bytes(1, "little")
DATA_END_CHARACTER = ord('}').to_bytes(1, "little")

REGISTER_NUM_VALUE_DELIMITER = ord(':').to_bytes(1, "little")
REGISTER_DELIMITER = ord(',').to_bytes(1, "little")
DATA_DELIMITER = ord(',').to_bytes(1, "little")

REGULAR_PACKET_TYPE = (1).to_bytes(1, "little")
EMERGENCY_PACKET_TYPE = (2).to_bytes(1, "little")

SERVER_SEND_STATE = (2).to_bytes(1, "little")
REGULAR_PACKET_STATE = (1).to_bytes(1, "little")
EMERGENCY_PACKET_STATE = (0).to_bytes(1, "little")
OBJECT_ID = (2).to_bytes(2, "little")

THREE = (3).to_bytes(1, "little")


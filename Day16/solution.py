
from typing import Tuple

class PacketParser:

    def __init__(self, message: str) -> None:
        self.message = message

    def get_packet_versions(self) -> list:
        
        message = self.message

        def get_packet_versions_inside(index: int) -> Tuple[list, int]:

            print(message[index:])

            version = int(message[index: index + 3], 2)
            index += 3

            type_id = int(message[index: index + 3], 2)
            index += 3

            if version == 6:

                while message[index] == "1":
                    # num = message[packet_index + 1: packet_index + 5]
                    index += 5
                
                # num = message[packet_index + 1: packet_index + 5]
                index += 5

                return [version], index
            
            else:

                subpackets_versions = list()

                length_type_id = int(message[index], 2)
                index += 1

                if length_type_id:
                    number_of_subpackets = int(message[index: index + 11], 2)
                    index += 11

                    for _ in range(number_of_subpackets):
                        subpacket_versions, subpacket_end_index = get_packet_versions_inside(index)
                        subpackets_versions += subpacket_versions
                        index = subpacket_end_index

                else:
                    subpackets_length = int(message[index: index + 15], 2)
                    index += 15

                    end_subpackets_index = index + subpackets_length

                    while index < end_subpackets_index:
                        subpacket_versions, subpacket_end_index = get_packet_versions_inside(index)
                        subpackets_versions += subpacket_versions
                        index = subpacket_end_index

                return [version] + subpackets_versions, index


        return get_packet_versions_inside(0)[0]



def task1(message: str) -> None:
    packet_parser = PacketParser(message)
    print(packet_parser.get_packet_versions())


def task2(message: str) -> None:
    pass


def main() -> None:
    with open("sample_input.txt", "r") as f:
        message = bin(int(f.read().strip(), 16))[2:]

        remainder = len(message) % 4

        if remainder != 0:
            message = "0" * (4 - remainder) + message

    task1(message)
    task2(message)


if __name__ == '__main__':
    main()

import can
import csv
import sys
from bitstring import BitArray


class Canedge1Analyzer():
    def __init__(self, mf4_file_path, clear_files=False) -> None:
        self.mf4_file_path = mf4_file_path
        self.init_files = clear_files
        self.options = {
            '0x1000001': self.can_0x01000001,  # system flags -> bool, uint
            '0x1000002': self.can_0x01000002,  # iqRef -> float
            '0x1000003': self.can_0x01000003,  # test_result -> float
            '0x1000004': self.can_0x01000004,  # piiq_ref -> float
        }
        if self.init_files:
            self.can_0x01000001('0', BitArray(hex='0x00000000'))
            self.can_0x01000002('0', BitArray(hex='0x00000000'))
            self.can_0x01000003('0', BitArray(hex='0x00000000'))
            self.can_0x01000004('0', BitArray(hex='0x00000000'))
            self.init_files = False  # turn off the initialize mode

    def processor(self) -> None:
        failure_canid = []
        # Open log file
        with can.LogReader(file_path) as reader:
            # Read messages
            for msg in reader:
                print(f"{msg.timestamp:.6f} {
                    msg.arbitration_id:X} {msg.data.hex()}")
                data = BitArray(hex=msg.data.hex())
                data.byteswap()
                canid = hex(msg.arbitration_id)

                try:
                    self.options.get(canid, lambda: print(
                        'invail option'))(msg.timestamp, data)
                except:
                    failure_canid.append(
                        canid) if canid not in failure_canid else ''

                    print(f'{canid} failure, this CAN ID process may not exist.')

        failure_canid.sort()
        print(f'No match process in these CAN-IDs.\n{failure_canid}') if len(
            failure_canid) > 0 else ''

    def can_0x01000001(self, timestamp: str, system_flags: BitArray) -> None:
        """
        System flag.

        Args:
            timestamp: unix time
            system_flags: system flags

        Returns:
            None
        """
        fieldnames = ['timestamp', 'flagEnableSystem', 'isOverSpeed',
                      'manualOverSpeed', 'M1_IFB_U_PPB2', 'tripFaultValue',
                      'clutch_status', 'loading_e', 'err']

        if self.init_files == False:
            data = {
                'timestamp': timestamp,
                'flagEnableSystem': BitArray((system_flags)[-1:]).uint,
                'isOverSpeed': BitArray((system_flags >> 1)[-1:]).uint,
                'manualOverSpeed': BitArray((system_flags >> 2)[-1:]).uint,
                'M1_IFB_U_PPB2': BitArray((system_flags >> 6)[-10:]).uint,
                'tripFaultValue': BitArray((system_flags >> 16)[-16:]).uint,
                'clutch_status': BitArray((system_flags >> 32)[-3:]).uint,
                'loading_e': BitArray((system_flags >> 40)[-3:]).uint,
                'err':  BitArray((system_flags >> 48)[-8:]).uint,
            }

        mode = 'w' if self.init_files else 'a'
        filename = f'{sys._getframe().f_code.co_name}.csv'

        with open(file=filename, mode=mode, newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if self.init_files:
                writer.writeheader()
            else:
                writer.writerow(data)

    def can_0x01000002(self, timestamp: str, iqRef: BitArray) -> None:  # iqRef, _iq, float
        """
        Motor of iqRef.

        Args:
            timestamp: unix time
            iqRef: motor iq

        Returns:
            None
        """
        fieldnames = ['timestamp', 'iqRef']
        data = {
            'timestamp': timestamp,
            'iqRef': iqRef.float,
        }
        mode = 'w' if self.init_files else 'a'
        filename = f'{sys._getframe().f_code.co_name}.csv'

        with open(file=filename, mode=mode, newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if self.init_files:
                writer.writeheader()
            else:
                writer.writerow(data)

    def can_0x01000003(self, timestamp: str, user_output: BitArray) -> None:
        """
        User output iq.

        Args:
            timestamp: unix time
            user_output: user output iq

        Returns:
            None
        """
        fieldnames = ['timestamp', 'user_output']
        data = {
            'timestamp': timestamp,
            'user_output': user_output.float,
        }
        mode = 'w' if self.init_files else 'a'
        filename = f'{sys._getframe().f_code.co_name}.csv'

        with open(file=filename, mode=mode, newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if self.init_files:
                writer.writeheader()
            else:
                writer.writerow(data)

    def can_0x01000004(self, timestamp: str, piiq_ref: BitArray) -> None:
        """
        PID iq_ref.

        Args:
            timestamp: unix time
            piiq_ref: PID iq_ref

        Returns:
            None
        """
        fieldnames = ['timestamp', 'piiq_ref']
        data = {
            'timestamp': timestamp,
            'piiq_ref': piiq_ref.float,
        }
        mode = 'w' if self.init_files else 'a'
        filename = f'{sys._getframe().f_code.co_name}.csv'

        with open(file=filename, mode=mode, newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if self.init_files:
                writer.writeheader()
            else:
                writer.writerow(data)

    def test_can_0x1000001(self) -> None:
        x = '0x1000001'
        timestamp = '1735009906.316400'
        data = BitArray(hex='0x0135000000000000')
        data.byteswap()
        self.options.get(x, lambda: print('invail option'))(timestamp, data)

    def test_can_0x1000002(self) -> None:
        x = '0x1000002'
        timestamp = '1735009906.316400'
        data = BitArray(hex='0x3d4ccccd')
        data.byteswap()
        self.options.get(x, lambda: print('invail option'))(timestamp, data)

    def test_can_0x1000003(self) -> None:
        x = '0x1000003'
        timestamp = '1735009906.316400'
        data = BitArray(hex='0x3ca3d70a')
        data.byteswap()
        self.options.get(x, lambda: print('invail option'))(timestamp, data)

    def test_can_0x1000004(self) -> None:
        x = '0x1000004'
        timestamp = '1735009906.316400'
        data = BitArray(hex='0x3d4ccccd')
        data.byteswap()
        self.options.get(x, lambda: print('invail option'))(timestamp, data)


if __name__ == '__main__':
    file_path = sys.argv[1]
    ret = Canedge1Analyzer(file_path, clear_files=True)
    # ret.test_can_0x1000001()
    ret.processor()

from time import time
import typing
import serial
import serial.serialutil


from siriuspy.bsmp.serial import IOInterface as _IOInterface


class TCPInterface(_IOInterface):
    pass


class SerialInterface(_IOInterface):
    def __init__(self, path: str, baudrate: int):
        super().__init__()
        self._port: str = path
        self._baudrate: int = baudrate
        self._serial: typing.Optional[serial.serialutil.SerialBase] = None
        self._encoding: str = "utf-8"

        self.open()

    def open(self) -> None:
        """Open the serial connection"""
        if not self._serial:
            self._serial = serial.Serial(port=self._port, baudrate=self._baudrate)

    def close(self) -> None:
        """Close the serial connection"""
        if self._serial:
            self._serial.close()
            self._serial = None

    def UART_read(self) -> typing.List[str]:
        # @todo: Usar a especificação do bsmp para ler o número correto de bytes
        if not self._serial:
            raise Exception("Serial not defined")

        _response = self._serial.read_all()
        _decoded = _response.decode(self._encoding)
        return [s for s in _decoded]

    def UART_write(
        self, stream: typing.List[str], timeout: float
    ) -> typing.Optional[typing.Any]:
        if not self._serial:
            raise Exception("Serial not defined")

        self._serial.write(stream)

    def UART_request(
        self, stream: typing.List[str], timeout: float
    ) -> typing.Optional[typing.List[str]]:
        """Read and Write OP"""
        self.UART_write(stream, timeout=timeout)
        return self.UART_read()

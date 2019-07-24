import serial
import struct
import time

arduino = serial.Serial('COM11', 115200, timeout=None)

arduino.flushInput()
arduino.write(b'a' * 6750)
arduino.flushOutput()

account1 = 0
account2 = 0

for j in range(3):
    print('Готовность 3 секунды!')
    for i in range(1, 4):
        print(i)
        time.sleep(1)
    print('Давай!')

    power1 = 0
    power2 = 0
    x1 = time.clock()
    while time.clock() - x1 < 10.0:
        a, b = struct.unpack('BB', arduino.read(2))
        if a > b:
            power1 += 1
        else:
            power2 += 1

    if power1 > power2:
        k = 1
        account1 += 1
    else:
        k = 2
        account2 += 1
    print('{} раунд закончен. Наш победитель игрок под номером {}'.format(j + 1, k))

print('{} : {}'.format(account1, account2))

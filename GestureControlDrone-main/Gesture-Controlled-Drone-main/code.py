# imports
import time
import board
import adafruit_bno055

from djitellopy import Tello
import cv2, math, time

# intialize sensor
i2c = board.I2C()
sensor = adafruit_bno055.BNO055_I2C(i2c)

# If you are going to use UART uncomment these lines
# uart = board.UART()
# sensor = adafruit_bno055.BNO055_UART(uart)

last_val = 0xFFFF

def temperature():
    global last_val  # pylint: disable=global-statement
    result = sensor.temperature
    if abs(result - last_val) == 128:
        result = sensor.temperature
        if abs(result - last_val) == 128:
            return 0b00111111 & result
    last_val = result
    return result

# initialize drone
tello = Tello()
tello.connect()

print('Battery level: ' +   str(tello.get_battery()))

#tello.streamon()
#frame_read = tello.get_frame_read()

tello.takeoff()

time.sleep(10)

# main loop
while True:

    print()
    # print sensor status
    print("Temperature: {} degrees C".format(sensor.temperature))
    """
    print(
        "Temperature: {} degrees C".format(temperature())
    )  # Uncomment if using a Raspberry Pi
    """
    print("Accelerometer (m/s^2): {}".format(sensor.acceleration))
    print("Magnetometer (microteslas): {}".format(sensor.magnetic))
    print("Gyroscope (rad/sec): {}".format(sensor.gyro))
    print("Euler angle: {}".format(sensor.euler))
    print("Quaternion: {}".format(sensor.quaternion))
    print("Linear acceleration (m/s^2): {}".format(sensor.linear_acceleration))
    print("Gravity (m/s^2): {}".format(sensor.gravity))
   
    # img = frame_read.frame
    # cv2.imshow("drone", img)

    key = cv2.waitKey(1) & 0xff
    if key == 27: # ESC
        break
    elif sensor.acceleration[0] > 1:
        print('forward')
        tello.move_forward(30)
    elif sensor.acceleration[0] < -1:
        print('back')
        tello.move_back(30)
    elif sensor.acceleration[1] > 1:
        print('left')
        tello.move_left(30)
    elif sensor.acceleration[1] < -1:
        print('right')
        tello.move_right(30)
    elif sensor.euler[0] > 45 and sensor.euler[0] < 135:
        print('rotate clockwise')
        tello.rotate_clockwise(30)
    elif sensor.euler[0] > 225 and sensor.euler[0] < 315:
        print('rotate counter clockwise')
        tello.rotate_counter_clockwise(30)
    #elif key == ord('r'):
        #tello.move_up(30)
    #elif key == ord('f'):
        #tello.move_down(30)
    else:
        print('flat')

    time.sleep(10)

tello.land()

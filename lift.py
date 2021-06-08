
import serial
from sql.sql_config import *
import time

class Crane:
    def __init__(self):
        self.ser = serial.Serial(
            port='/dev/ttyUSB0',
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS
    )

    def move_arm(self, msg):
        # msg = "#" + str(servo_num) + "P" + str(location)+"S" + str(speed)+ "\r"
        print("moving arm msg {}\n".format(msg))
        msg = bytes(bytearray(msg.encode()))
        self.ser.write(msg)
        self.ser.flush()


if __name__ == '__main__':
    ## initiate a new SQL table for the lift. load specimen of commands
    conn, cursor = connect_to_db()
    init_database(cursor, conn)
    init_sql_table(cursor, conn, "lift", d_lift, False)
   
    update_sql(cursor, conn, "lift", ("0"), False, d_lift)
    update_sql(cursor, conn, "driver", ("0"), False, d_lift) #should be lift 

    print_sql_row(cursor, "lift")

    ## forever awate commands to the lift and execute them
    cr = Crane()

    ID = 0
    conn, cursor = connect_to_db()
    while True:
        while int(ID) >= int(get_last_table_elem(cursor, "ID", "lift")):
            continue
        ID = get_last_table_elem(cursor, "ID", "lift")
        msg = get_last_table_elem(cursor, "command", "lift")
        msg += '\r'
        cr.move_arm(msg)






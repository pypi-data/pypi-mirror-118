import time

class timer:
    def __init__(self):
        self.max_time = int(0)
        self.occasion = ""

    def timer_settings(self):
        timer_time = input("how much time do you want to wait for countdown? ")
        self.max_time += int(timer_time)
        if timer_time:
            occasion = input("Any occasion? (y/n): ")
            if occasion == "y":
                o_name = input("occasion name: ")
                self.occasion = o_name
                print("countdown is starting...")
                time.sleep(2)
                for i in range(int(self.max_time)):
                    print(str(self.max_time))
                    self.max_time -= 1
                    time.sleep(1)
                    if self.max_time == 0:
                        print("YAY!!! its " + self.occasion)
            elif occasion == "n":
                print("countdown is starting...")
                for i in range(self.max_time):
                    print(str(self.max_time))
                    self.max_time -= 1
                    time.sleep(1)
                    if self.max_time == 0:
                        print("ALERT! it's time!")




if __name__ == '__main__':
    timer1 = timer()
    timer1.timer_settings()
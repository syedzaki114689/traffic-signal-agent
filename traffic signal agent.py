import random
import time
import os


from random import randint


class trafficlight:
    def __init__(self, state):
        self.state = state


class pedestrian:
    def __init__(self, state):
        self.state = state


class intersection:
    # tarffic light(red,yellow,green,left turn arrow)

    def __init__(self):
        self.east_to_west = trafficlight([1, 0, 0, 0])
        self.West_to_east = trafficlight([1, 0, 0, 0])
        self.north_to_south = trafficlight([1, 0, 0, 0])
        self.south_to_north = trafficlight([1, 0, 0, 0])
        self.east_p = pedestrian([1, 0])
        self.west_p = pedestrian([1, 0])
        self.north_p = pedestrian([1, 0])
        self.south_p = pedestrian([1, 0])

    def open_east_to_west_left(self):
        self.east_to_west.state = [0, 0, 1, 1]
        self.West_to_east.state = [0, 0, 1, 1]

    def open_east_to_west(self):
        self.east_to_west.state = [0, 0, 1, 0]
        self.West_to_east.state = [0, 0, 1, 0]
        self.north_p.state = [0, 1]
        self.south_p.state = [0, 1]

    def open_north_to_south_left(self):
        self.south_to_north.state = [0, 0, 1, 1]
        self.north_to_south.state = [0, 0, 1, 1]

    def open_north_to_south(self):
        self.south_to_north.state = [0, 0, 1, 0]
        self.north_to_south.state = [0, 0, 1, 0]
        self.east_p.state = [0, 1]
        self.west_p.state = [0, 1]

    def close_all(self):
        self.east_to_west.state = [1, 0, 0, 0]
        self.West_to_east.state = [1, 0, 0, 0]
        self.north_to_south.state = [1, 0, 0, 0]
        self.south_to_north.state = [1, 0, 0, 0]
        self.east_p.state = [1, 0]
        self.west_p.state = [1, 0]
        self.north_p.state = [1, 0]
        self.south_p.state = [1, 0]

    def findlight(self,l):
        if(l == [1, 0, 0, 0]):
            return "red"

        elif(l == [0, 0, 1, 0]):
            return "green and left turn red"

        elif(l == [0, 0, 1, 1]):
            return "green and left turn green"

        elif(l == [1, 0]):
            return "pedestrian dont cross"

        elif(l == [0, 1]):
            return "pedestrian cross"

        else:
            return 'error'

    def print_state(self):

        print("north facing trafficlight = ",self.findlight(self.north_to_south.state))
        print("south facing trafficlight = ",self.findlight(self.north_to_south.state))
        print("east facing trafficlight = ", self.findlight(self.east_to_west.state))
        print("west facing trafficlight = ", self.findlight(self.east_to_west.state))
        print("west crosswalk = ", self.findlight(self.west_p.state))
        print("east crosswalk = ", self.findlight(self.east_p.state))
        print("north crosswalk = ", self.findlight(self.north_p.state))
        print("south crosswalk = ", self.findlight(self.south_p.state))


class agent:
    

    def __init__(self):
        self.intersection_a = intersection()

    def sensors(self):
        return randint(0, 1)

    def printcount(self,a,b,c,d):
        print("\ntraffic east = ", a)
        print("traffic west = ", b)
        print("traffic north = ", c)
        print("traffic south = ", d)
        print()

    def cross(self, count):
        traffic_cross_per2sec = 3
        trafficcount_east = 0
        trafficcount_west = 0
        trafficcount_north = 0
        trafficcount_south = 0

        pedestrian_button_pressed_east = False
        pedestrian_button_pressed_west = False
        pedestrian_button_pressed_north = False
        pedestrian_button_pressed_south = False
        

        i = 0
        c = 0
        while (True):
            
            trafficcount_north = trafficcount_north+(self.sensors())
            trafficcount_south = trafficcount_south+(self.sensors())
            trafficcount_east = trafficcount_east+(self.sensors())
            trafficcount_west = trafficcount_west+(self.sensors())
            self.intersection_a.print_state()
            self.printcount(trafficcount_east,trafficcount_west,trafficcount_north,trafficcount_south)
            if(c == 10):
                c = 0
                pedestrian_button_pressed_east = bool(self.sensors)
                pedestrian_button_pressed_west = bool(self.sensors)
                pedestrian_button_pressed_north = bool(self.sensors)
                pedestrian_button_pressed_south = bool(self.sensors)
            else:
                c += 1

            if(((trafficcount_north + trafficcount_east + trafficcount_south + trafficcount_west)/4) > 5):

                if(trafficcount_east > trafficcount_north and trafficcount_east > trafficcount_south and trafficcount_east > trafficcount_west):

                    self.intersection_a.close_all()

                    if(pedestrian_button_pressed_east):
                        self.intersection_a.open_east_to_west()
                    else:
                        self.intersection_a.open_east_to_west_left()
                    trafficcount_east-=traffic_cross_per2sec
                    time.sleep(2)

                else:
                    if(trafficcount_north > trafficcount_west and trafficcount_north > trafficcount_south):
                        self.intersection_a.close_all()

                        if(pedestrian_button_pressed_north):
                            self.intersection_a.open_north_to_south()
                        else:
                            self.intersection_a.open_north_to_south_left()
                        trafficcount_north-=traffic_cross_per2sec
                        time.sleep(2)

                    else:
                        if(trafficcount_south > trafficcount_west):
                            self.intersection_a.close_all()

                            if(pedestrian_button_pressed_south):
                                self.intersection_a.open_north_to_south()
                            else:
                                self.intersection_a.open_north_to_south_left()
                            trafficcount_south-=traffic_cross_per2sec
                            time.sleep(2)

                        else:
                            self.intersection_a.close_all()

                            if(pedestrian_button_pressed_west):
                                self.intersection_a.open_east_to_west()
                            else:
                                self.intersection_a.open_east_to_west_left()
                            trafficcount_west-=traffic_cross_per2sec
                            time.sleep(2)

            else:
                time.sleep(2)

            i += 1
            os.system('cls||clear')
            if(i >= count):
                break


if __name__ == "__main__":
    m = agent()
    m.cross(100)
class Ship :
    def __init__(self, name, callname, departure, destination, speed = 0, direction = 0, eta = '미정', lat = 35.1037, long = 129.0408) :
        self.name = name
        self.callname = callname
        self.departure = departure
        self.destination = destination
        self.speed = speed
        self.direction = direction
        self.eta = eta
        self.status = 'report'
        self.long = long
        self.lat = lat

    def report(self) :
        inform_dict = {'name' : self.name, 'callname' : self.callname, 'departure' : self.departure, 'destination' : self.destination,
                        'speed' : self.speed, 'direction' : self.direction, 'eta' : self.eta, 'lat' : self.lat, 'long' : self.long}
        return inform_dict

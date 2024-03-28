class JsonPacket:
    # ...

    @staticmethod
    def REMOVEPacket(count):
        return JsonPacket(type=REMOVE, msg=count).getPacket()
# src/models/room.py
class Room:
    def __init__(self, name, capacity, is_lab=False):
        self.name = name
        self.capacity = capacity
        self.is_lab = is_lab
        self.schedule = {}  # Will hold time slot allocations
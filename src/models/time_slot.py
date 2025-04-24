# src/models/time_slot.py
# src/models/time_slot.py (ensure accurate overlap check)
class TimeSlot:
    def __init__(self, day, start_time, end_time):
        self.day = day
        self.start_time = start_time
        self.end_time = end_time
        
    def duration_minutes(self):
        return (self.end_time.hour - self.start_time.hour) * 60 + \
               (self.end_time.minute - self.start_time.minute)
    
    def overlaps(self, other_slot):
        if self.day != other_slot.day:
            return False
        return not (self.end_time <= other_slot.start_time or 
                    self.start_time >= other_slot.end_time)
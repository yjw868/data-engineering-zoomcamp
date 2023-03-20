from datetime import datetime
from typing import Dict, List


class FhvRideRecord:

    def __init__(self, arr: List[str]):
        self.dispatching_base_num = str(arr[0])
        self.pickup_datetime = datetime.strptime(arr[1], "%Y-%m-%d %H:%M:%S")
        self.drop_off_datetime = datetime.strptime(arr[2], "%Y-%m-%d %H:%M:%S")
        self.pickup_location_id = str(arr[3])
        self.drop_off_location_id = str(arr[4])
        self.sr_flag= str(arr[5])
        self.affiliated_base_number = str(arr[6])

    @classmethod
    def from_dict(cls, d: Dict):
        # print(f'd is {d}')
        try:
            return cls(arr=[
                d['dispatching_base_num'],
                d['pickup_datetime'],
                d['drop_off_datetime'],
                d['pickup_location_id'],
                d['drop_off_location_id'],
                d['sr_flag'],
                d['affiliated_base_number'],
            ]
            )
        except:
            return cls(arr=[
                d['dispatching_base_num'],
                d['pickup_datetime'].strftime("%Y-%m-%d %H:%M:%S"),
                d['drop_off_datetime'].strftime("%Y-%m-%d %H:%M:%S"),
                d['pickup_location_id'],
                d['drop_off_location_id'],
                d['sr_flag'],
                d['affiliated_base_number'],
            ]
            )

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.__dict__}'


def dict_to_ride_record(obj, ctx):
    if obj is None:
        return None

    return FhvRideRecord.from_dict(obj)


def ride_record_to_dict(ride_record:FhvRideRecord, ctx):
    return ride_record.__dict__
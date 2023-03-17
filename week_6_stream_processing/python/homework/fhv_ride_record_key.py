from typing import Dict


class FhvRideRecordKey:
    def __init__(self, affiliated_base_number):
        self.affiliated_base_number = affiliated_base_number

    @classmethod
    def from_dict(cls, d: Dict):
        return cls(affiliated_base_number=d['affiliated_base_number'])

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.__dict__}'


def dict_to_ride_record_key(obj, ctx):
    if obj is None:
        return None

    return FhvRideRecordKey.from_dict(obj)


def ride_record_key_to_dict(ride_record_key: FhvRideRecordKey, ctx):
    return ride_record_key.__dict__
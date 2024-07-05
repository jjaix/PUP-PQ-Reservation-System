from dataclasses import dataclass


# MODEL CLASS:: OOP
@dataclass
class ReservationRequests:
    id: int
    item: str
    name: str
    program_year_section: str
    contact_number: float
    email: str
    date: str
    time: str
    prof: str
    updated: str

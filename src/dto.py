from dataclasses import dataclass, fields

@dataclass
class Book:
    title: str | None
    price: tuple[float, str] | None
    tax: tuple[float, str] | None
    availability: int | None
    upc: str | None

    def is_valid(self):
        return all(getattr(self, f.name) is not None for f in fields(self))
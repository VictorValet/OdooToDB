
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(255), unique=True)
    password_hash: Mapped[str]
    def __repr__(self) -> str:
        return f"User(id={self.id!r}, username={self.username!r})"

class Contact(Base):
    __tablename__ = "contacts"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255))
    phone: Mapped[str] = mapped_column(String(255))
    mobile: Mapped[str] = mapped_column(String(255))
    contact_address: Mapped[str]
    is_company: Mapped[bool]
    def __repr__(self) -> str:
        return f"Contact(id={self.id!r}, name={self.name!r})"

class Invoice(Base):
    __tablename__ = "invoices"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    user_id: Mapped[int]
    partner_id: Mapped[int]
    date: Mapped[str] = mapped_column(String(255))
    invoice_date_due: Mapped[str] = mapped_column(String(255))
    amount_total: Mapped[float] = mapped_column(String(255))
    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, name={self.name!r})"


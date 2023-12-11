from sqlmodel import Session, select


from hotel.database.models import Customer
from hotel.operations.models import (
    CustomerCreateData,
    CustomerResult,
    CustomerUpdateData,
)
from hotel.operations.utils.delete_message import get_delete_message
from hotel.operations.utils.get_or_404 import get_or_404
from hotel.operations.utils.get_session import with_session
from hotel.operations.utils.to_dict import to_dict


@with_session
def get_customers(session: Session):
    statement = select(Customer)
    return session.exec(statement).all()


@with_session
def get_customer(session: Session, customer_id: int) -> CustomerResult | str:
    return get_or_404(session, Customer, customer_id)


@with_session
def create_customer(session: Session, customer: CustomerCreateData):
    customer = Customer(**customer.dict())
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer


@with_session
def update_customer(
    session: Session, customer_id: int, updated_customer: CustomerUpdateData
) -> CustomerResult | str:
    customer = get_or_404(session, Customer, customer_id)

    for key, value in updated_customer.dict(exclude_unset=True).items():
        setattr(customer, key, value)

    session.commit()
    session.refresh(customer)
    return CustomerResult(**to_dict(updated_customer))


@with_session
def delete_customer(session: Session, customer_id: int) -> dict:
    customer = get_or_404(session, Customer, customer_id)
    session.delete(customer)
    session.commit()
    return get_delete_message(Customer)

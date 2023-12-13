from hotel.operations.interface import DataInterface, DataObject
from hotel.operations.models import (
    CustomerCreateData,
    CustomerUpdateData,
)


def get_customers(customer_interface: DataInterface) -> list[DataObject]:
    return customer_interface.read_all()


def get_customer(
    customer_id: int, customer_interface: DataInterface
) -> DataObject | str:
    return customer_interface.read_by_id(customer_id)


def create_customer(
    customer: CustomerCreateData, customer_interface: DataInterface
) -> DataObject:
    return customer_interface.create(customer.dict())


def update_customer(
    customer_id: int,
    updated_customer: CustomerUpdateData,
    customer_interface: DataInterface,
) -> DataObject | str:
    return customer_interface.update(customer_id, updated_customer.dict())


def delete_customer(customer_id: int, customer_interface: DataInterface) -> dict:
    return customer_interface.delete(customer_id)

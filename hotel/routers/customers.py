from typing import List
from fastapi import APIRouter

from hotel.database.database_interface import DatabaseInterface
from hotel.database.models import Customer
from hotel.operations.customers import (
    get_customers,
    get_customer,
    create_customer,
    update_customer,
    delete_customer,
)
from hotel.operations.models import (
    CustomerCreateData,
    CustomerUpdateData,
    CustomerResult,
)

router = APIRouter()


@router.get("/customers", response_model=List[Customer])
def api_get_customers():
    customer_interface = DatabaseInterface(Customer)
    return get_customers(customer_interface)


@router.get("/customers/{customer_id}", response_model=Customer | str)
def api_get_customer(customer_id: int):
    customer_interface = DatabaseInterface(Customer)
    return get_customer(customer_id, customer_interface)


@router.post("/customers", response_model=CustomerCreateData, status_code=201)
def api_create_customer(customer: CustomerCreateData) -> CustomerResult:
    customer_interface = DatabaseInterface(Customer)
    return create_customer(customer, customer_interface)


@router.put("/customers/{customer_id}", response_model=CustomerUpdateData | str)
def api_update_customer(
    customer_id: int, customer: CustomerUpdateData
) -> CustomerResult | str:
    customer_interface = DatabaseInterface(Customer)
    return update_customer(customer_id, customer, customer_interface)


@router.delete("/customers/{customer_id}", response_model=dict)
def api_delete_customer(customer_id: int) -> dict:
    customer_interface = DatabaseInterface(Customer)
    return delete_customer(customer_id, customer_interface)

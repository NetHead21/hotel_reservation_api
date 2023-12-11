from typing import List
from fastapi import APIRouter
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
    return get_customers()


@router.get("/customers/{customer_id}", response_model=Customer | str)
def api_get_customer(customer_id: int):
    return get_customer(customer_id)


@router.post("/customers", response_model=CustomerCreateData, status_code=201)
def api_create_customer(customer: CustomerCreateData) -> CustomerResult:
    return create_customer(customer)


@router.put("/customers/{customer_id}", response_model=CustomerUpdateData | str)
def api_update_customer(
    customer_id: int, customer: CustomerUpdateData
) -> CustomerResult | str:
    return update_customer(customer_id, customer)


@router.delete("/customers/{customer_id}", response_model=dict)
def api_delete_customer(customer_id: int) -> dict:
    return delete_customer(customer_id)

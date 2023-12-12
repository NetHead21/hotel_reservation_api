def get_delete_message(model: object) -> dict:
    return {"detail": f"{model.__name__} deleted successfully."}

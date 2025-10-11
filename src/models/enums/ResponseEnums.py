from enum import Enum


class ResponseStatus(Enum):

    USER_ADDED_SUCCESS = "User added successfully"
    USER_EMAIL_EXISTS = "User with this email already exists"
    CATEGORY_NOT_FOUND = "category not found"
    CATEGORY_UPDATED_SUCCESSFULLY= "category updated successfully"
    CATEGORY_ALLREADY_EXISTS= "category with this name already exists"
    CATEGORY_ADDED_SUCCESS = "category added successfully"
    ERROR = "error"
    ADDED_INVOICE_SUCCESSFULLY = "invoice added successfully"
    INVOICE_NOT_FOUND = "invoice not found"
    GET_INVOICES_FOR_USER_SUCCESS = "invoices for user retrieved successfully"
    GET_INVOICES_FOR_USER_SUCCESS_IN_RANGE_DATE = "invoices for user in range date retrieved successfully"
    GET_ALL_CATEGORIES_SUCCESS = "all categories retrieved successfully"
    INVOICE_CANNOT_BE_ADDED = "invoice cannot be added"
    INVOICE_ADDED_SUCCESSFULLY = "invoice added successfully"
    FAILED_ADDED_NEW_INCOME = "failed while adding new income"
    ADDED_NEW_INCOME_SUCCESSFULLY = "added the new income successfully"
    FAILED_TO_ADD_NEW_INCOME_CATEGORY = "failed to add new income category"
    ADDED_NEW_INCOME_CATEGORY_SUCCESSFULLY = "added new income category successfully"
    CAN_NOT_DELETED_THE_INCOME = "can not deleted this income"
    DELETED_INCOME_SUCCESSFULLY = "deleted income successfully"
    INCOME_ID_DOES_NOT_EXISTS = "income_id does not exists"
    UPDATED_INCOME_SUCCESSFULLY = "updated income successfully"
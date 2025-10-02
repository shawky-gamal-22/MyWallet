from .BaseDataModel import BaseDataModel
from .db_schemes import Invoice
from sqlalchemy.future import select
from datetime import datetime
from sqlalchemy import func
from sqlalchemy.future import select
from datetime import timedelta, timezone


class InvoiceModel(BaseDataModel):
    """
    InvoiceModel class for interacting with the invoices table in the database.
    Inherits from BaseDataModel to utilize common database functionalities.
    """
    def __init__(self, db_client: object):
        super().__init__(db_client)
        self.db_client = db_client

    @classmethod
    async def create_instance(cls, db_client: object):
        """
        Asynchronous factory method to create an instance of InvoiceModel.

        :param db_client: The database client/session maker.
        :return: An instance of UserModel.
        """
        return cls(db_client)

    
    async def create_invoice(self,
                             user_id: int,
                             category_id: int,
                             invoice_name: str,
                             total_price: float,
                             description: str = None,
                             img_path: str = None) -> Invoice:
        
        """
        Create a new invoice record in the database.
        :param user_id: ID of the user associated with the invoice.
        :param category_id: ID of the
        :param totoal_price: Total price of the invoice.
        :param description: Optional description of the invoice.
        :param img_path: Optional image path associated with the invoice.
        :return: The created Invoice object.
        """
        async with self.db_client() as session:
            async with session.begin():
                new_invoice = Invoice(
                    user_id=user_id,
                    category_id=category_id,
                    invoice_name=invoice_name,
                    total_price=total_price,
                    description=description,
                    img_path=img_path
                )
                session.add(new_invoice)  # No await here
            await session.refresh(new_invoice)
            return new_invoice
        
    async def get_invoice_by_id(self, invoice_id: int) -> Invoice:
        """
        Retrieve an invoice by its ID.
        :param invoice_id: The ID of the invoice to retrieve.
        :return: The Invoice object if found, else None.
        """
        async with self.db_client() as session:
            stmt = select(Invoice).where(Invoice.id == invoice_id)
            result = await session.execute(stmt)
            invoice = result.scalars().first()
            return invoice
        
    async def get_all_invoices_by_user(self, user_id: int, limit: int = 10, skip: int=0) -> list[Invoice]:
        """
        Retrieve all invoices associated with a specific user.
        :param user_id: The ID of the user whose invoices to retrieve.
        :param limit: Maximum number of invoices to retrieve.
        :return: A list of Invoice objects.
        """
        async with self.db_client() as session:
            stmt = select(Invoice).where(Invoice.user_id == user_id).offset(skip).limit(limit)
            result = await session.execute(stmt)
            invoices = result.scalars().all()
            return invoices
    
    async def update_invoice(self, 
                             invoice_id: int, 
                             total_price: int = None, 
                             description: str = None, 
                             category_id: int = None, 
                             img_path: str = None) -> Invoice:
        
        async with self.db_client() as session:
            async with session.begin():
                stmt = select(Invoice).where(Invoice.id == invoice_id)
                result = await session.execute(stmt)
                invoice = result.scalars().first()
                
                if not invoice:
                    return None
                
                if total_price is not None:
                    invoice.total_price = total_price
                if description is not None:
                    invoice.description = description
                if category_id is not None:
                    invoice.category_id = category_id
                if img_path is not None:
                    invoice.img_path = img_path
                
                session.add(invoice)
            
            await session.refresh(invoice)
            return invoice
        
    async def delete_invoice(self, invoice_id: int) -> bool:
        """
        Delete an invoice by its ID.

        :param invoice_id: The ID of the invoice to delete.
        :return: True if deletion was successful, else False.
        """
        async with self.db_client() as session:
            async with session.begin():
                stmt = select(Invoice).where(Invoice.id == invoice_id)
                result = await session.execute(stmt)
                invoice = result.scalars().first()
                if invoice:
                    await session.delete(invoice)
                    return True
            return False
        
    async def get_invoice_by_date_range(self, user_id: int, start_date: datetime, end_date: datetime) -> list[Invoice]:
        """
        Retrieve invoices for a user within a specific date range.

        :param user_id: The ID of the user whose invoices to retrieve.
        :param start_date: The start date of the range.
        :param end_date: The end date of the range.
        :return: A list of Invoice objects within the date range.
        """
        end_at = end_date + timedelta(days=1)
        async with self.db_client() as session:
            stmt = select(Invoice).where(
                Invoice.user_id == user_id,
                Invoice.created_at >= start_date,
                Invoice.created_at < end_at  # less than next day
            )
            result = await session.execute(stmt)
            invoices = result.scalars().all()
            return invoices
        
    async def get_total_spent_by_date_range(self, user_id: int, start_date: datetime, end_date: datetime) -> float:
        """
        Calculate the total amount spent by a user within a specific date range.

        :param user_id: The ID of the user.
        :param start_date: The start date of the range.
        :param end_date: The end date of the range.
        :return: The total amount spent as a float.
        """
        end_at = end_date + timedelta(days=1)
        async with self.db_client() as session:
            stmt = select(func.sum(Invoice.total_price)).where(
                Invoice.user_id == user_id,
                Invoice.created_at >= start_date,
                Invoice.created_at < end_at
            )
            result = await session.execute(stmt)
            total_spent = result.scalar() or 0.0
            return total_spent
    
    async def get_invoices_by_category(self, user_id: int, category_id: int) -> list[Invoice]:
        """
        Retrieve all invoices for a user within a specific category.

        :param user_id: The ID of the user.
        :param category_id: The ID of the category.
        :return: A list of Invoice objects within the specified category.
        """
        async with self.db_client() as session:
            stmt = select(Invoice).where(
                Invoice.user_id == user_id,
                Invoice.category_id == category_id
            )
            result = await session.execute(stmt)
            invoices = result.scalars().all()
            return invoices

    

    
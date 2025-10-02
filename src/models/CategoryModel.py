from .BaseDataModel import BaseDataModel
from .db_schemes import Category
from sqlalchemy.future import select
from .enums import ResponseStatus
from typing import Optional


class CategoryModel(BaseDataModel):
    """
    CategoryModel class for interacting with the categories table in the database.
    Inherits from BaseDataModel to utilize common database functionalities.
    """
    def __init__(self, db_client: object):
        super().__init__(db_client)
        self.db_client = db_client

    @classmethod
    async def create_instance(cls, db_client: object):
        """
        Asynchronous factory method to create an instance of CategoryModel.

        :param db_client: The database client/session maker.
        :return: An instance of UserModel.
        """
        return cls(db_client)
    
    async def create_category(self, name: str, description: str = None):
        """
        Create a new category in the database.

        :param name: The name of the new category.
        :param description: The description of the new category.
        :return: The created category object.
        """
        async with self.db_client() as session:
            async with session.begin():
                stmt = select(Category).where(Category.name == name)
                result = await session.execute(stmt)
                category = result.scalars().first()
                if category:
                    return None  # Category with this name already exists
                
                else:
                    new_category = Category(name=name, description=description)
                    session.add(new_category)
            
            await session.refresh(new_category)
            return new_category
        
    async def get_category_by_id(self, category_id: int):
        """
        Get category by id from the database

        :param category_id: the id of the category
        :return: the category with the id = category_id 
        """
        async with self.db_client() as session:        
            stmt = select(Category).where(Category.id == category_id)
            result = await session.execute(stmt)
            category = result.scalars().first()
            category_name = category.name if category else "Unknown"
            return category_name
        
    async def get_all_categories(self, page_no: int= 1, page_size: int = 10):
        """
        Get all categories from the database

        :return: all the categories
        """
        async with self.db_client() as session:
            stmt = select(Category).offset((page_no-1)*page_size).limit(page_size)
            result = await session.execute(stmt)
            categories = result.scalars().all()
            return categories
        
    async def update_category(self, category_id: int, 
                              name: Optional[str]= None, 
                              description: Optional[str]= None)-> Category:


        category = await self.get_category_by_id(category_id= category_id)

        if not category:
            return {
                "status": ResponseStatus.CATEGORY_NOT_FOUND.value,
            }            
        
        if name is not None:
            category.name = name
        if description is not None:
            category.description = description

        await self.session.commit()
        await self.session.refresh(category)
        


        return {
            "status": ResponseStatus.CATEGORY_UPDATED_SUCCESSFULLY,
            "data": category
        }
    
    async def delete_category(self, category_id: int, 
                              name: Optional[str]= None, 
                              description: Optional[str]= None)-> bool:
        
        async with self.db_client() as session:
            async with session.begin():
                stmt = select(Category).where(Category.id == category_id)
                result = session.execute(stmt)
                category = result.scalars().first()

                if category:
                    session.delete(category)
                    return True
            return False
        
    async def find_by_name(self, name: str)-> Category:

        async with self.db_client() as session:
            async with session.begin():
                stmt = select(Category).where(Category.name == name)
                result = session.execute(stmt)
                category = result.scalars().first()
                return category
            
    async def exists(self, category_id) -> bool:
        async with self.db_client() as session:
            async with session.begin():
                stmt = select(Category).where(Category.id == category_id)
                result = session.execute(stmt)
                category = result.scalars().first()

                if not category:
                    return False
                
                return True
    
    async def count_categories(self) -> int:
        async with self.db_client() as session:
            async with session.begin():
                stmt = select(Category)
                result = session.execute(stmt)
                categories = result.scalars().all()
                return len(categories)




    
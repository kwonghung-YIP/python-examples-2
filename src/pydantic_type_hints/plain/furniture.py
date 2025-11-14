from typing import Literal
from .product import getHash, isEqual, mapProps, ProductCategory, Product, ProductFactory

PRODUCT_FAMILY_FURNITURE = 'furniture'
FURNITURE_CATEGORY_TABLE = 'table'
FURNITURE_CATEGORY_CHAIR = 'chair'

class FurnitureCategory(ProductCategory):

    def __init__(self, family:str, category:str) -> None:
        super().__init__(family)
        self.category: str = category

    def __hash__(self) -> int:
        return getHash(self,'family','category')
    
    def __eq__(self, value) -> bool:
        return isEqual(self,value,'family','category')
    
    def __repr__(self) -> str:
        return f"{type(self)}:family={self.family},category={self.category}"

class Furniture(Product):

    def __init__(self,**kwargs) -> None:
        self.family: Literal['furntiure'] = PRODUCT_FAMILY_FURNITURE
        self.category: str
        self.brand: str
        super().__init__(**kwargs|dict(family=self.family))
        mapProps(self,kwargs,'category','brand')

    @property
    def type(self) -> ProductCategory:
        return FurnitureCategory(self.family,self.category)

class TableCategory(FurnitureCategory):
    def __init__(self, family:str, category:str, tableCategory:str) -> None:
        super().__init__(family,category)
        self.tableCategory: str = tableCategory

    def __hash__(self) -> int:
        return getHash(self,'family','category','tableCategory')
    
    def __eq__(self, value) -> bool:
        return isEqual(self,value,'family','category','tableCategory')
    
    def __repr__(self) -> str:
        return f"{type(self)}:family={self.family},category={self.category},tableCategory={self.tableCategory}"

class Table(Furniture):

    def __init__(self,**kwargs) -> None:
        self.category: Literal['table'] = FURNITURE_CATEGORY_TABLE
        self.tableCategory: str
        super().__init__(**kwargs|dict(category=self.category))
        mapProps(self,kwargs,'tableCategory')
        self.tableCategory = kwargs['tableCategory']

    @property
    def type(self) -> ProductCategory:
        return TableCategory(self.family,self.category,self.tableCategory)

class ChairCategory(FurnitureCategory):
    def __init__(self, family:str, category:str, chairCategory:str) -> None:
        super().__init__(family,category)
        self.chairCategory: str = chairCategory

    def __hash__(self) -> int:
        return getHash(self,'family','category','chairCategory')
    
    def __eq__(self, value) -> bool:
        return isEqual(self,value,'family','category','chairCategory')
    
    def __repr__(self) -> str:
        return f"{type(self)}:family={self.family},category={self.category},chairCategory={self.chairCategory}"

class Chair(Furniture):

    def __init__(self,**kwargs) -> None:
        self.category: Literal['chair'] = FURNITURE_CATEGORY_CHAIR
        self.chairCategory: str
        super().__init__(**kwargs|dict(category=self.category))
        mapProps(self,kwargs,'chairCategory')

    @property
    def type(self) -> ProductCategory:
        return ChairCategory(self.family,self.category,self.chairCategory)

ProductFactory.register(ProductCategory('furniture'),Furniture)
ProductFactory.register(TableCategory(PRODUCT_FAMILY_FURNITURE,\
    FURNITURE_CATEGORY_TABLE,'dining-table'),Table)
ProductFactory.register(ChairCategory(PRODUCT_FAMILY_FURNITURE,\
    FURNITURE_CATEGORY_CHAIR,'office-chair'),Chair)
ProductFactory.register(FurnitureCategory(PRODUCT_FAMILY_FURNITURE,'bed'),Furniture)

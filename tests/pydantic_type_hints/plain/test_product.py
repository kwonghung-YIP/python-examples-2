import pytest
from pydantic_type_hints.plain.product import ProductCategory, Product
from pydantic_type_hints.plain.furniture import FurnitureCategory, TableCategory, ChairCategory
from pydantic_type_hints.plain.furniture import Furniture, Table, Chair
from pydantic_type_hints.plain import furniture
from uuid import UUID

FAMILY_MOBILE_PHONE = 'mobile-phone'

class TestProductCategory:

    def test_hash_and_eq(self):
        """
        Test the __hash__() and __eq__ functions for ProductCategory
        """

        mobile1 = ProductCategory(FAMILY_MOBILE_PHONE)
        mobile2 = ProductCategory(FAMILY_MOBILE_PHONE)

        assert mobile1.family==FAMILY_MOBILE_PHONE

        assert not mobile1 is mobile2, "mobile1/2 have different object reference"
        assert mobile1==mobile2, "mobile1/2 are equal since they share the same family property value"
        assert mobile1.__hash__()==mobile2.__hash__(), "mobile1/2 also share the same hash value"

        table = FurnitureCategory(furniture.PRODUCT_FAMILY_FURNITURE,furniture.FURNITURE_CATEGORY_TABLE)
        officeDesk = TableCategory(furniture.PRODUCT_FAMILY_FURNITURE,furniture.FURNITURE_CATEGORY_TABLE,'office-desk')

        assert officeDesk.family==furniture.PRODUCT_FAMILY_FURNITURE
        assert officeDesk.category==furniture.FURNITURE_CATEGORY_TABLE
        assert officeDesk.tableCategory=='office-desk'

        assert table!=officeDesk, "subclass and its parent class are not identical even they have the same attribute values"

    def test_work_with_mapand_set(self):
        """
        ProductCategory should be hashable and used as key of map
        """

        gardenChair1 = ChairCategory(furniture.PRODUCT_FAMILY_FURNITURE,furniture.FURNITURE_CATEGORY_CHAIR,"garden-chair")
        gardenChair2 = ChairCategory(furniture.PRODUCT_FAMILY_FURNITURE,furniture.FURNITURE_CATEGORY_CHAIR,"garden-chair")

        # ChairCategory is hashable and can be assigned as key of the map
        map1:dict[ProductCategory,str] = {gardenChair1:"value-1",gardenChair2:"value-2"}

        assert len(map1) == 1, "create map1 with duplicated keys and only 1 item will be remained"
        assert map1[gardenChair1] == "value-2", "for duplicated key, the one being inserted later will overwrite the previous (value-2)"
        assert gardenChair1 in map1 and gardenChair2 in map1, "key lookup based on __hash__ and __eq__ but not the object reference"

        # create a set with duplicated entries
        set1:set[ProductCategory] = {gardenChair2, gardenChair1}

        assert type(set1) == set, "class for set1 should be set"
        assert len(set1) == 1, "set is not allow duplicated so only 1 item is remained"
        assert next(iter(set1)) is gardenChair2, "different from map, the duplicated element comes later is rejected and not inserted into the set"

        map2 = {
            ChairCategory('furniture','chair','office-chair'): 'office-chair',
            ChairCategory('furniture','chair','dining-chair'): 'dining-chair',
            TableCategory('furniture','table','office-desk'): 'office-desk',
            TableCategory('furniture','table','dining-chair'): 'dining-chair',
            FurnitureCategory('furniture','bed'): 'bed',
            FurnitureCategory('furniture','lamp'): 'lamp',
            ProductCategory('cpu'):'cpu'
        }

        assert len(map2) == 7, "All keys in map2 should be unique"

class TestProduct:

    def test_create_instance_from_abstract_class(self):
        with pytest.raises(TypeError,match="Can't instantiate abstract class Product"):
            product = Product(family="backpack",title="backpack#1")
        
    
class TestFurniture:

    def test_furniture_init(self):
        bed = Furniture(category="bed",title="Double Bed",desc="Double bed with drawers",brand="Sweet Dream")
        
        assert type(bed.id) == UUID, "A new random UUID should be assigned to the id property"
        assert bed.family == furniture.PRODUCT_FAMILY_FURNITURE
        assert bed.category == "bed"
        assert bed.title == "Double Bed"
        assert bed.desc == "Double bed with drawers"
        assert bed.brand == 'Sweet Dream'
        
        category = bed.type
        assert type(category) == FurnitureCategory
        assert category.family == bed.family
        assert category.category == bed.category

    def test_table_init(self):
        officeDesk = Table(id='25b62149-7cf0-40ee-96c1-2069085c7ca8',
            tableCategory="office-desk",title="Office Desk",brand="Work Hard Wooden")
        
        assert officeDesk.id == '25b62149-7cf0-40ee-96c1-2069085c7ca8', "use the provided uuid instead of generated a new one"
        assert officeDesk.family == furniture.PRODUCT_FAMILY_FURNITURE
        assert officeDesk.category == furniture.FURNITURE_CATEGORY_TABLE
        assert officeDesk.tableCategory == "office-desk"
        assert officeDesk.title == "Office Desk"
        assert officeDesk.desc is None
        assert officeDesk.brand == 'Work Hard Wooden'
        
        category = officeDesk.type
        assert type(category) == TableCategory
        assert category.family == officeDesk.family
        assert category.category == officeDesk.category
        assert category.tableCategory == officeDesk.tableCategory

    def test_chair_init(self):
        gardenChair = Chair(id='25b62149-7cf0-40ee-96c1-2069085c7ca8',
            chairCategory="garden-chair",title="Garden Chair",brand="Indina Outdoor Furniture")
        
        assert gardenChair.id == '25b62149-7cf0-40ee-96c1-2069085c7ca8', "use the provided uuid instead of generated a new one"
        assert gardenChair.family == furniture.PRODUCT_FAMILY_FURNITURE
        assert gardenChair.category == furniture.FURNITURE_CATEGORY_CHAIR
        assert gardenChair.chairCategory == "garden-chair"
        assert gardenChair.title == "Garden Chair"
        assert gardenChair.desc is None
        assert gardenChair.brand == 'Indina Outdoor Furniture'
        
        category = gardenChair.type
        assert type(category) == ChairCategory
        assert category.family == gardenChair.family
        assert category.category == gardenChair.category
        assert category.chairCategory == gardenChair.chairCategory

    def test_class_attibutes(self):
        chair1 = Chair(chairCategory="office-chair",title="Air Mesh",brand="iKoolo")
        chair2 = Chair(chairCategory="garden-chair",title="Outdoor Garden Chair",brand="Your Garden")

        assert chair1.title != chair2.title
        assert chair1.chairCategory != chair2.chairCategory 

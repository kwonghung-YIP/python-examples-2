import pytest
from pydantic_type_hints.plain.product import ProductFactory
from pydantic_type_hints.plain.furniture import TableCategory, Table, ChairCategory, Chair
import json

class TestProductFactory:

    def test_resolve_table(self):
        #ProductFactory.register(TableCategory('furniture','table','office-desk'),Table)
        #ProductFactory.register(TableCategory('furniture','table','dining-desk'),Table)
        #ProductFactory.register(ChairCategory('furniture','chair','garden-chair'),Chair)

        factory = ProductFactory.instance()

        assert hasattr(factory,'_productCatagolue')
        assert len(factory._productCatagolue) == 3
        
        raw = dict(id='25b62149-7cf0-40ee-96c1-2069085c7ca8',family='furniture',\
                category='table',tableCategory='dining-table',title='Solid Oak Wood Dining Table', brand='Home Design')
        diningTable = ProductFactory.buildFromDict(raw)
        
        assert type(diningTable) == Table
        assert diningTable.id == '25b62149-7cf0-40ee-96c1-2069085c7ca8'
        assert diningTable.title == 'Solid Oak Wood Dining Table'
        assert diningTable.brand == 'Home Design'

        category = diningTable.type

        assert type(category) == TableCategory
        assert category.family == 'furniture'
        assert category.category == 'table'
        assert category.tableCategory == 'dining-table'

    def test_load_from_json(self):
        ProductFactory.register(TableCategory("furniture","table","adjustable-table"),Table)

        with open('tests/pydantic_type_hints/plain/furniture-data.json','r') as jsonfile:
            data = json.load(jsonfile)
            
            product1 = ProductFactory.buildFromDict(data[0])
            assert type(product1) == Table, "first elements in furniture-data.json should parsed as Table instance"

            product2 = ProductFactory.buildFromDict(data[1])
            assert type(product2) == Chair, "second elements in furniture-data.json should parsed as Chair instance"
            assert product2.id == data[1]['id']
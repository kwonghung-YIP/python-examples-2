import logging
from abc import ABC, abstractmethod
from typing import Self, Type, Any
from uuid import UUID, uuid4
from functools import reduce

log = logging.getLogger(__name__)

def nvl[T](value:T,default:T) -> T:
    return default if value is None else value

def getHash(self,*attributes:str) -> int:
    key = '-'.join(map(lambda attr:getattr(self,attr),attributes))
    #print(f"getHash:key:{key}")
    return key.__hash__()

def isEqual[T](self:T,other:Any,*attributes:str) -> bool:
    if type(self) == type(other):
        # the lambda being passed into the map() get the same attributes from both self and other
        # and return a tuple, therefore the return from map() is a list of tuple
        attrValues = map(lambda attr:(getattr(self,attr),getattr(other,attr)),attributes)
        # the lambda being passed into the reduce() comparing attribute values
        # and return True if they all are the same
        return reduce(lambda result,values: result and values[0] == values[1],attrValues,True)
    else:
        return False

def mapProps(self:Any,data:dict[str,Any],*fields:str|tuple[str,Any]) -> None:
    fieldList = map(lambda f: (f,None) if type(f)==str else f, fields)
    for property, default in fieldList:
        #print(f"{property}:{default}")
        setattr(self,property,data.get(property,default))

class ProductCategory:
    def __init__(self, family:str) -> None:
        self.family: str = family

    def __hash__(self) -> int:
        return getHash(self,'family')
    
    def __eq__(self, value) -> bool:
        return isEqual(self,value,'family')
    
    def __repr__(self) -> str:
        return f"{type(self)}:family={self.family}"
    
class Product(ABC):

    def __init__(self,**kwargs) -> None:
        self.family: str
        mapProps(self,kwargs,('id',uuid4()),'family','title','desc')

    @property
    @abstractmethod
    def type(self) -> ProductCategory:
        return ProductCategory(self.family)

    def __hash__(self) -> int:
        return self.id.__hash__()
    
    def __eq__(self,other) -> bool:
        return self.id == other.id if isinstance(other,Product) else False

    def __repr__(self) -> str:
        return f"{type(self)}:id={self.id},type={self.type},title={self.title}"

class ProductFactory:
    _instance:Self = None

    @classmethod
    def instance(cls) -> Self:
        if cls._instance is None:
            instance = cls.__new__(cls)
            instance._productCatagolue: dict[ProductCategory,Type] = {}
            cls._instance = instance
        return cls._instance

    @classmethod
    def register(cls,category:ProductCategory,productClass:Type[Product]) -> None:
        log.info(f"register:{category}->{productClass}")
        factory = cls.instance()
        factory._productCatagolue[category] = productClass
        doc_view = sorted(factory._productCatagolue.items(),key=lambda item:len(vars(item[0])),reverse=True)
        factory._productCatagolue = dict(doc_view)

    @classmethod
    def buildFromDict(cls,rawData:dict[str,Any]) -> Product:
        factory = cls.instance()
        productClass = factory.resolveProductClass(rawData)
        log.info(f"Resolve productClass:{productClass}")
        product = productClass.__new__(productClass)
        product.__init__(**rawData)
        return product
    
    def __init__(self:Type,*args,**kargs) -> None:
        raise RuntimeError("call Product.instance() to get the singleton instance")
    
    def resolveProductClass(self, rawData:dict[str,Any]) -> Type[Product]:
        for category, productClass in self._productCatagolue.items():
            #print(f"{category}:{productClass}")
            #print(rawData)
            #print([(getattr(category,p),rawData.get(property)) for p in vars(category).keys()])
            if all (getattr(category,property) == rawData.get(property) for property in vars(category).keys()):
                return productClass
        raise RuntimeError(f"Cannot find ProductCategory for {rawData}")

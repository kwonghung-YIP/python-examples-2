from .person import Name, Person

if __name__ == "__main__":
    john = Person(**({"name":{"title":"Mr","firstName":"John","lastName":"Doe"},"dob":"1994-03-16","email":"john.doe@gmail.com"}))
    print(john.model_dump())
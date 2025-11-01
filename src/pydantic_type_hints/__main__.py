from .models import SimpleModel, Name

if __name__ == "__main__":
    obj = SimpleModel()
    name = Name("John","Doe")
    print(dir(name))
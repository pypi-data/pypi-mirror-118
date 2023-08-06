# -----------------------------------------------------------
# Module to increase encapsulation in Python, not allowing the access to private members outside their classes
#
# (C) 2021 Antonio Pérez, Spain
# Released under MIT License
# email ingovanpe@gmail.com
# -----------------------------------------------------------

# The module inspect is imported as it will help us to determine whether an attribute is being called from the class
# or outside the class
import inspect


def private_attributes_dec(*args):
    """We pass a series a strings with the name of public attributes we want to turn private and this decorator
    will make them and private attributes in the class not accessible or modifiable"""
    def private_members_decorator(class_):
        # This is the part of the decorator who gets the class we are modifying in the attribute class_
        # We create two new members in our class that are basically clones of the magic methods to get and attribute
        # and set an attribute
        class_.__getattr__orig = class_.__getattribute__
        class_.__setattr__orig = class_.__setattr__

        def new_getattr(self, name: str):
            """This method will modify how the magic method to get attributes works, making impossible for developers
            to get a private attribute or a public attribute we set as private in the decorator outside the class"""
            # We get the current frame where the attribute was called from
            f: inspect.FrameInfo = inspect.currentframe()
            # By default, we will consider that it is not being called from the class (or a subclass). However, we will
            # check if that is the case using the current frame (f) and checking if it also being called from a subclass
            # and in that case we set it to True
            from_class: bool = False
            if 'self' in f.f_back.f_locals and issubclass(type(f.f_back.f_locals['self']), class_):
                from_class = True
            # If the attribute being called is private (starts with __ or _className__ or is in the list of attributes
            # provided to the decorator and it is not being called from the class or a subclass,
            # we raise an AttributeError (as we won't allow developers to get that attribute)
            if (name.startswith("__") or name.startswith("_{0}__".format(class_.__name__)) or name in args) and \
                    not from_class:
                raise AttributeError("We can't access private attribute {0}".format(name))
            # Otherwise, we just return the result of calling the copy we did of the usual magic method to get an
            # attribute (so we are returning that attribute)
            return class_.__getattr__orig(self, name)

        def new_setattr(self, name: str, value):
            """This method will modify how the magic method to set attributes works, making impossible for developers
            to set a private attribute or a public attribute we set as private in the decorator outside the class
            to a new value"""
            # We get the current frame where the attribute was called from
            f: inspect.FrameInfo = inspect.currentframe()
            # By default, we will consider that it is not being called from the class (or a subclass). However, we will
            # check if that is the case using the current frame (f) and checking if it also being called from a subclass
            # and in that case we set it to True
            from_class: bool = False
            if 'self' in f.f_back.f_locals and issubclass(type(f.f_back.f_locals['self']), class_):
                from_class = True
            # If the attribute being called is private (starts with __ or _className__ or is in the list of attributes
            # provided to the decorator and it is not being called from the class or a subclass,
            # we raise an AttributeError (as we won't allow developers to set that attribute to a new value)
            if (name.startswith("__") or name.startswith("_{0}__".format(class_.__name__)) or name in args)\
                    and not from_class:
                raise AttributeError("We can't modify private attribute {0}".format(name))
            # Otherwise, we just return the result of calling the copy we did of the usual magic method to set an
            # attribute to return a new value
            return class_.__setattr__orig(self, name, value)
        # We replace the standard magic methods to get and set attributes with the new ones we defined above
        class_.__getattribute__ = new_getattr
        class_.__setattr__ = new_setattr
        # We return our modified class
        return class_
    # We return the middle decorator
    return private_members_decorator


if __name__ == "__main__":
    # We are providing some examples here:
    # Case 1: Root class and private attribute (starts with __) -> Attribute __d
    # Case 2: Root class and public attribute, however we set it as private using the decorator (We pass the name of the
    # attribute in the decorator) -> Attribute a
    # Case 3: Root class and private attribute, that was turned into a property with a setter and deleter
    @private_attributes_dec("a")
    class Example:
        def __init__(self):
            self.a: int = 12
            self.b: int = 12
            self.c: int = 12
            self.__d: int = 12
            self.__e: int = 12

        # Case 1.2: We call to a method defined in the class that accesses that private attribute
        def get_d(self):
            return self.__d

        # Case 1.3: We call to a method defined in the class that sets that private attribute to a new value
        def set_d(self, value: int):
            self.__d = value

        # Case 2.2: We call to a method defined in the class that accesses that attribute we made private
        def get_a(self):
            return self.a

        # Case 2.3: We call to a method defined in the class that sets that attribute we made private to a new value
        def set_a(self, value: int):
            self.a = value

        # Case 3.1: Private attribute made property
        @property
        def e(self) -> int:
            return self.__e

        # Case 3.2: Private attribute made a property, setter
        @e.setter
        def e(self, value: int):
            self.__e = value

        # Case 3.3: Private attribute made a property, deleter
        @e.deleter
        def e(self):
            self.__e = None

    e: Example = Example()
    # Case 1.1: Trying to access the private attribute outside the class -> We will raise an AttributeError
    try:
        print(e._Example__d)
    except AttributeError:
        assert True
        print("The attribute __d (_Example__d) can't be accessed outside the class")
    else:
        assert False
    # Case 1.2: We call to a method defined in the class that accesses that private attribute -> The method works
    try:
        print(e.get_d())
    except AttributeError:
        print("Error, we raised an AttributeError")
        assert False
    else:
        assert True
    # Case 1.3: We call to a method defined in the class that accesses that private attribute -> The method works
    try:
        e.set_d(13)
    except AttributeError:
        print("Error, we raised an AttributeError")
        assert False
    else:
        assert e.get_d() == 13
    # Case 1.4: We try to access __dict__ -> We raise an AttributeError cause __dict__ is now a private attribute
    try:
        print(e.__dict__)
    except AttributeError:
        assert True
        print("The attribute __dict__ can't be accessed outside the class, it's private now")
    else:
        assert False
    # Case 1.5: We try to modify __dict__ -> We raise an AttributeError cause __dict__ is now a private attribute
    try:
        e.__dict__["b"] = 3
    except AttributeError:
        assert True
        print("The attribute __dict__ can't be accessed outside the class, it's private now")
    else:
        assert False
    # Case 2.1: We try to access a public attribute that we altered to make private using the arguments in the decorator
    # -> We raise an AttributeError
    try:
        print(e.a)
    except AttributeError:
        assert True
        print("The attribute a can't be accessed outside the class")
    else:
        assert False
    # Case 2.2: We call to a method defined in the class that accesses that attribute we made private
    # -> The method works
    try:
        print(e.get_a())
    except AttributeError:
        print("Error, we raised an AttributeError")
        assert False
    else:
        assert True
    # Case 2.3: We call to a method defined in the class that accesses that attribute we made private
    # -> The method works
    try:
        e.set_a(13)
    except AttributeError:
        print("Error, we raised an AttributeError")
        assert False
    else:
        assert e.get_a() == 13
    # Case 3.1: We try to access a private attribute that was turned into a property -> We can access the property
    try:
        print(e.e)
    except AttributeError:
        print("Error, we raised an AttributeError")
        assert False
    else:
        assert True
    # Case 3.2: We try to set a new value to a private attribute that where we defined a set method-> The method works
    try:
        e.e = 3
    except AttributeError:
        print("Error, we raised an AttributeError")
        assert False
    else:
        assert e.e == 3
    # Case 3.3: We try to delete a private attribute turned into a property where we set up a deleter -> It works
    try:
        del e.e
    except AttributeError:
        print("Error, we raised an AttributeError")
        assert False
    else:
        assert e.e == None

    # Case 4: Public attribute turned private using the decorator and now handled in the subclass
    # Case 5: Private attribute turned property with setter and deleter
    class SubclassExample(Example):
        def __init__(self):
            Example.__init__(self)

        # Case 4.1: We access public attribute turned private inside a subclass
        def get_a_v2(self):
            return self.a

        # Case 4.2: We set a public attribute turned private inside a subclass
        def set_a_v2(self, value: int):
            self.a = value


    se = SubclassExample()
    # Case 4.1: We access public attribute turned private inside a subclass -> The method works (subclasses can access
    # them)
    try:
        print(se.get_a_v2())
    except AttributeError:
        print("Error, we raised an AttributeError")
        assert False
    else:
        assert True
    # Case 4.2: We call to a method defined in the class that accesses that attribute we made private
    # -> The method works (subclasses can access them)
    try:
        se.set_a_v2(14)
    except AttributeError:
        print("Error, we raised an AttributeError")
        assert False
    else:
        assert se.get_a() == 14
    # Case 5.1: Private attribute turned property with setter and deleter, we try to get the property -> Method works
    try:
        print(se.e)
    except AttributeError:
        print("Error, we raised an AttributeError")
        assert False
    else:
        assert True
    # Case 5.2: Private attribute turned property with setter and deleter, we try to use the setter
    # -> Method works
    try:
        se.e = 5
    except AttributeError:
        print("Error, we raised an AttributeError")
        assert False
    else:
        assert se.e == 5
    # Case 5.3: Private attribute turned property with setter and deleter, we try to use the deleter -> Method works
    try:
        del se.e
    except AttributeError:
        print("Error, we raised an AttributeError")
        assert False
    else:
        assert se.e == None
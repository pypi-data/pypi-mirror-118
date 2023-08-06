class classproperty(property):

    def __get__(self, cls, owner):
        return classmethod(self.fget).__get__(None, owner)()


class staticproperty(property):

    def __get__(self, cls, owner):
        return staticmethod(self.fget).__get__(None, owner)()

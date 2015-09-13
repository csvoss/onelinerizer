__a, _A__a, _B__a, __b, _A__b, _B__b, __c, _A__c, _B__c = 0, 1, 2, 3, 4, 5, 6, 7, 8
print __a, _A__a, _B__a, __b, _A__b, _B__b, __c, _A__c, _B__c
class A(object):
    __a = 9
    print __a, _A__a, _B__a, __b, _A__b, _B__b, __c, _A__c, _B__c
    def f(self):
        print __a, _A__a, _B__a, __b, _A__b, _B__b, __c, _A__c, _B__c
    class B(object):
        __b = 10
        print __a, _A__a, _B__a, __b, _A__b, _B__b, __c, _A__c, _B__c
        def f(self):
            print __a, _A__a, _B__a, __b, _A__b, _B__b, __c, _A__c, _B__c

A().f()
A().B().f()

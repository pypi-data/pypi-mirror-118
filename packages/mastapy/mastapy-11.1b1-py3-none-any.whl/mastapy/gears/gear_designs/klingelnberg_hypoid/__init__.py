'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._915 import KlingelnbergCycloPalloidHypoidGearDesign
    from ._916 import KlingelnbergCycloPalloidHypoidGearMeshDesign
    from ._917 import KlingelnbergCycloPalloidHypoidGearSetDesign
    from ._918 import KlingelnbergCycloPalloidHypoidMeshedGearDesign

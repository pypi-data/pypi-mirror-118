'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._506 import BevelGearMeshRating
    from ._507 import BevelGearRating
    from ._508 import BevelGearSetRating

'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._894 import WormDesign
    from ._895 import WormGearDesign
    from ._896 import WormGearMeshDesign
    from ._897 import WormGearSetDesign
    from ._898 import WormWheelDesign

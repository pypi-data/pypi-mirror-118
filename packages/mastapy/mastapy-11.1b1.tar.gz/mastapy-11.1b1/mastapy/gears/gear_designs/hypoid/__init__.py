'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._923 import HypoidGearDesign
    from ._924 import HypoidGearMeshDesign
    from ._925 import HypoidGearSetDesign
    from ._926 import HypoidMeshedGearDesign

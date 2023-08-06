'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._899 import StraightBevelDiffGearDesign
    from ._900 import StraightBevelDiffGearMeshDesign
    from ._901 import StraightBevelDiffGearSetDesign
    from ._902 import StraightBevelDiffMeshedGearDesign

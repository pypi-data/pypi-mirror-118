'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._882 import DesignConstraint
    from ._883 import DesignConstraintCollectionDatabase
    from ._884 import DesignConstraintsCollection
    from ._885 import GearDesign
    from ._886 import GearDesignComponent
    from ._887 import GearMeshDesign
    from ._888 import GearSetDesign
    from ._889 import SelectedDesignConstraintsCollection

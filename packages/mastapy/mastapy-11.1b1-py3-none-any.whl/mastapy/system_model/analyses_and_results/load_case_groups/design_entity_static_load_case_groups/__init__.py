'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._5364 import AbstractAssemblyStaticLoadCaseGroup
    from ._5365 import ComponentStaticLoadCaseGroup
    from ._5366 import ConnectionStaticLoadCaseGroup
    from ._5367 import DesignEntityStaticLoadCaseGroup
    from ._5368 import GearSetStaticLoadCaseGroup
    from ._5369 import PartStaticLoadCaseGroup

'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._1219 import KeyedJointDesign
    from ._1220 import KeyTypes
    from ._1221 import KeywayJointHalfDesign
    from ._1222 import NumberOfKeys

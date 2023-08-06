'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._2051 import ClutchConnection
    from ._2052 import ClutchSocket
    from ._2053 import ConceptCouplingConnection
    from ._2054 import ConceptCouplingSocket
    from ._2055 import CouplingConnection
    from ._2056 import CouplingSocket
    from ._2057 import PartToPartShearCouplingConnection
    from ._2058 import PartToPartShearCouplingSocket
    from ._2059 import SpringDamperConnection
    from ._2060 import SpringDamperSocket
    from ._2061 import TorqueConverterConnection
    from ._2062 import TorqueConverterPumpSocket
    from ._2063 import TorqueConverterTurbineSocket

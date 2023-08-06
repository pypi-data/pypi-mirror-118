'''_2486.py

OilSealSystemDeflection
'''


from mastapy._internal import constructor
from mastapy.system_model.part_model import _2174
from mastapy.system_model.analyses_and_results.static_loads import _6611
from mastapy.system_model.analyses_and_results.power_flows import _3811
from mastapy.system_model.analyses_and_results.system_deflections import _2430
from mastapy._internal.python_net import python_net_import

_OIL_SEAL_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'OilSealSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('OilSealSystemDeflection',)


class OilSealSystemDeflection(_2430.ConnectorSystemDeflection):
    '''OilSealSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _OIL_SEAL_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'OilSealSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def reliability_for_oil_seal(self) -> 'float':
        '''float: 'ReliabilityForOilSeal' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ReliabilityForOilSeal

    @property
    def component_design(self) -> '_2174.OilSeal':
        '''OilSeal: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2174.OilSeal)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6611.OilSealLoadCase':
        '''OilSealLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6611.OilSealLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def power_flow_results(self) -> '_3811.OilSealPowerFlow':
        '''OilSealPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3811.OilSealPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None

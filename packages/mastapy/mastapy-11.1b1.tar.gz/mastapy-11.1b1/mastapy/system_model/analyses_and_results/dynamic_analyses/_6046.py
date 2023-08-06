'''_6046.py

PlanetCarrierDynamicAnalysis
'''


from mastapy.system_model.part_model import _2177
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6620
from mastapy.system_model.analyses_and_results.dynamic_analyses import _6038
from mastapy._internal.python_net import python_net_import

_PLANET_CARRIER_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses', 'PlanetCarrierDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('PlanetCarrierDynamicAnalysis',)


class PlanetCarrierDynamicAnalysis(_6038.MountableComponentDynamicAnalysis):
    '''PlanetCarrierDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _PLANET_CARRIER_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PlanetCarrierDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2177.PlanetCarrier':
        '''PlanetCarrier: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2177.PlanetCarrier)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6620.PlanetCarrierLoadCase':
        '''PlanetCarrierLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6620.PlanetCarrierLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

'''_6050.py

RingPinsDynamicAnalysis
'''


from mastapy.system_model.part_model.cycloidal import _2277
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6628
from mastapy.system_model.analyses_and_results.dynamic_analyses import _6038
from mastapy._internal.python_net import python_net_import

_RING_PINS_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses', 'RingPinsDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('RingPinsDynamicAnalysis',)


class RingPinsDynamicAnalysis(_6038.MountableComponentDynamicAnalysis):
    '''RingPinsDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _RING_PINS_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RingPinsDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2277.RingPins':
        '''RingPins: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2277.RingPins)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6628.RingPinsLoadCase':
        '''RingPinsLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6628.RingPinsLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

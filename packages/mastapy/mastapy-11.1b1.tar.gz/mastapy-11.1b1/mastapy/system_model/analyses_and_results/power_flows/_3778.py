'''_3778.py

CycloidalDiscPowerFlow
'''


from mastapy.system_model.part_model.cycloidal import _2276
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6540
from mastapy.system_model.analyses_and_results.power_flows import _3734
from mastapy._internal.python_net import python_net_import

_CYCLOIDAL_DISC_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'CycloidalDiscPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('CycloidalDiscPowerFlow',)


class CycloidalDiscPowerFlow(_3734.AbstractShaftPowerFlow):
    '''CycloidalDiscPowerFlow

    This is a mastapy class.
    '''

    TYPE = _CYCLOIDAL_DISC_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CycloidalDiscPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2276.CycloidalDisc':
        '''CycloidalDisc: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2276.CycloidalDisc)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6540.CycloidalDiscLoadCase':
        '''CycloidalDiscLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6540.CycloidalDiscLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

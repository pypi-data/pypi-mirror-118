'''_3957.py

RollingRingCompoundPowerFlow
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2303
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.power_flows import _3828
from mastapy.system_model.analyses_and_results.power_flows.compound import _3904
from mastapy._internal.python_net import python_net_import

_ROLLING_RING_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'RollingRingCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('RollingRingCompoundPowerFlow',)


class RollingRingCompoundPowerFlow(_3904.CouplingHalfCompoundPowerFlow):
    '''RollingRingCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _ROLLING_RING_COMPOUND_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RollingRingCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2303.RollingRing':
        '''RollingRing: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2303.RollingRing)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_3828.RollingRingPowerFlow]':
        '''List[RollingRingPowerFlow]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_3828.RollingRingPowerFlow))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_3828.RollingRingPowerFlow]':
        '''List[RollingRingPowerFlow]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_3828.RollingRingPowerFlow))
        return value

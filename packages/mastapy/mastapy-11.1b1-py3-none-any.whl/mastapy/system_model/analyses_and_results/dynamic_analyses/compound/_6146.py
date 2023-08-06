'''_6146.py

FEPartCompoundDynamicAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2161
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.dynamic_analyses import _6017
from mastapy.system_model.analyses_and_results.dynamic_analyses.compound import _6092
from mastapy._internal.python_net import python_net_import

_FE_PART_COMPOUND_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound', 'FEPartCompoundDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('FEPartCompoundDynamicAnalysis',)


class FEPartCompoundDynamicAnalysis(_6092.AbstractShaftOrHousingCompoundDynamicAnalysis):
    '''FEPartCompoundDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _FE_PART_COMPOUND_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FEPartCompoundDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2161.FEPart':
        '''FEPart: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2161.FEPart)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_6017.FEPartDynamicAnalysis]':
        '''List[FEPartDynamicAnalysis]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_6017.FEPartDynamicAnalysis))
        return value

    @property
    def planetaries(self) -> 'List[FEPartCompoundDynamicAnalysis]':
        '''List[FEPartCompoundDynamicAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(FEPartCompoundDynamicAnalysis))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_6017.FEPartDynamicAnalysis]':
        '''List[FEPartDynamicAnalysis]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_6017.FEPartDynamicAnalysis))
        return value

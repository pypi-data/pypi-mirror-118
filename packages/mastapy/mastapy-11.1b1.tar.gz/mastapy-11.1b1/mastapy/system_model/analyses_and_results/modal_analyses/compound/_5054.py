'''_5054.py

SynchroniserHalfCompoundModalAnalysis
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2311
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses import _4907
from mastapy.system_model.analyses_and_results.modal_analyses.compound import _5055
from mastapy._internal.python_net import python_net_import

_SYNCHRONISER_HALF_COMPOUND_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound', 'SynchroniserHalfCompoundModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('SynchroniserHalfCompoundModalAnalysis',)


class SynchroniserHalfCompoundModalAnalysis(_5055.SynchroniserPartCompoundModalAnalysis):
    '''SynchroniserHalfCompoundModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _SYNCHRONISER_HALF_COMPOUND_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SynchroniserHalfCompoundModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2311.SynchroniserHalf':
        '''SynchroniserHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2311.SynchroniserHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_4907.SynchroniserHalfModalAnalysis]':
        '''List[SynchroniserHalfModalAnalysis]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_4907.SynchroniserHalfModalAnalysis))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_4907.SynchroniserHalfModalAnalysis]':
        '''List[SynchroniserHalfModalAnalysis]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_4907.SynchroniserHalfModalAnalysis))
        return value

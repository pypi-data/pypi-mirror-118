'''_5909.py

PowerLoadCompoundHarmonicAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2180
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5742
from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import _5944
from mastapy._internal.python_net import python_net_import

_POWER_LOAD_COMPOUND_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Compound', 'PowerLoadCompoundHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('PowerLoadCompoundHarmonicAnalysis',)


class PowerLoadCompoundHarmonicAnalysis(_5944.VirtualComponentCompoundHarmonicAnalysis):
    '''PowerLoadCompoundHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _POWER_LOAD_COMPOUND_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PowerLoadCompoundHarmonicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2180.PowerLoad':
        '''PowerLoad: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2180.PowerLoad)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_5742.PowerLoadHarmonicAnalysis]':
        '''List[PowerLoadHarmonicAnalysis]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_5742.PowerLoadHarmonicAnalysis))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_5742.PowerLoadHarmonicAnalysis]':
        '''List[PowerLoadHarmonicAnalysis]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_5742.PowerLoadHarmonicAnalysis))
        return value

'''_4149.py

BearingCompoundParametricStudyTool
'''


from typing import List

from mastapy.bearings.bearing_results import _1673, _1681, _1684
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.bearings.bearing_results.rolling import (
    _1711, _1718, _1726, _1742,
    _1766
)
from mastapy.system_model.part_model import _2149
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4002
from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import _4177
from mastapy._internal.python_net import python_net_import

_BEARING_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound', 'BearingCompoundParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('BearingCompoundParametricStudyTool',)


class BearingCompoundParametricStudyTool(_4177.ConnectorCompoundParametricStudyTool):
    '''BearingCompoundParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _BEARING_COMPOUND_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BearingCompoundParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def bearing_duty_cycle_results(self) -> '_1673.LoadedBearingDutyCycle':
        '''LoadedBearingDutyCycle: 'BearingDutyCycleResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1673.LoadedBearingDutyCycle.TYPE not in self.wrapped.BearingDutyCycleResults.__class__.__mro__:
            raise CastException('Failed to cast bearing_duty_cycle_results to LoadedBearingDutyCycle. Expected: {}.'.format(self.wrapped.BearingDutyCycleResults.__class__.__qualname__))

        return constructor.new_override(self.wrapped.BearingDutyCycleResults.__class__)(self.wrapped.BearingDutyCycleResults) if self.wrapped.BearingDutyCycleResults else None

    @property
    def component_design(self) -> '_2149.Bearing':
        '''Bearing: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2149.Bearing)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_analysis_cases_ready(self) -> 'List[_4002.BearingParametricStudyTool]':
        '''List[BearingParametricStudyTool]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_4002.BearingParametricStudyTool))
        return value

    @property
    def planetaries(self) -> 'List[BearingCompoundParametricStudyTool]':
        '''List[BearingCompoundParametricStudyTool]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(BearingCompoundParametricStudyTool))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_4002.BearingParametricStudyTool]':
        '''List[BearingParametricStudyTool]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_4002.BearingParametricStudyTool))
        return value

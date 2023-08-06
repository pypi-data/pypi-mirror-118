'''_4128.py

SynchroniserSleeveParametricStudyTool
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2313
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6656
from mastapy.system_model.analyses_and_results.system_deflections import _2525
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4127
from mastapy._internal.python_net import python_net_import

_SYNCHRONISER_SLEEVE_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools', 'SynchroniserSleeveParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('SynchroniserSleeveParametricStudyTool',)


class SynchroniserSleeveParametricStudyTool(_4127.SynchroniserPartParametricStudyTool):
    '''SynchroniserSleeveParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _SYNCHRONISER_SLEEVE_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SynchroniserSleeveParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2313.SynchroniserSleeve':
        '''SynchroniserSleeve: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2313.SynchroniserSleeve)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6656.SynchroniserSleeveLoadCase':
        '''SynchroniserSleeveLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6656.SynchroniserSleeveLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def component_system_deflection_results(self) -> 'List[_2525.SynchroniserSleeveSystemDeflection]':
        '''List[SynchroniserSleeveSystemDeflection]: 'ComponentSystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSystemDeflectionResults, constructor.new(_2525.SynchroniserSleeveSystemDeflection))
        return value

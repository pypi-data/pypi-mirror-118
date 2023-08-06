'''_4132.py

TorqueConverterTurbineParametricStudyTool
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2317
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6661
from mastapy.system_model.analyses_and_results.system_deflections import _2533
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4032
from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_TURBINE_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools', 'TorqueConverterTurbineParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('TorqueConverterTurbineParametricStudyTool',)


class TorqueConverterTurbineParametricStudyTool(_4032.CouplingHalfParametricStudyTool):
    '''TorqueConverterTurbineParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _TORQUE_CONVERTER_TURBINE_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'TorqueConverterTurbineParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2317.TorqueConverterTurbine':
        '''TorqueConverterTurbine: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2317.TorqueConverterTurbine)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6661.TorqueConverterTurbineLoadCase':
        '''TorqueConverterTurbineLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6661.TorqueConverterTurbineLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def component_system_deflection_results(self) -> 'List[_2533.TorqueConverterTurbineSystemDeflection]':
        '''List[TorqueConverterTurbineSystemDeflection]: 'ComponentSystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSystemDeflectionResults, constructor.new(_2533.TorqueConverterTurbineSystemDeflection))
        return value

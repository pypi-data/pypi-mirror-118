'''_2656.py

SpiralBevelGearSetCompoundSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model.gears import _2251
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.system_deflections.compound import _2654, _2655, _2571
from mastapy.system_model.analyses_and_results.system_deflections import _2510
from mastapy._internal.python_net import python_net_import

_SPIRAL_BEVEL_GEAR_SET_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'SpiralBevelGearSetCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('SpiralBevelGearSetCompoundSystemDeflection',)


class SpiralBevelGearSetCompoundSystemDeflection(_2571.BevelGearSetCompoundSystemDeflection):
    '''SpiralBevelGearSetCompoundSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _SPIRAL_BEVEL_GEAR_SET_COMPOUND_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpiralBevelGearSetCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2251.SpiralBevelGearSet':
        '''SpiralBevelGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2251.SpiralBevelGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2251.SpiralBevelGearSet':
        '''SpiralBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2251.SpiralBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def spiral_bevel_gears_compound_system_deflection(self) -> 'List[_2654.SpiralBevelGearCompoundSystemDeflection]':
        '''List[SpiralBevelGearCompoundSystemDeflection]: 'SpiralBevelGearsCompoundSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearsCompoundSystemDeflection, constructor.new(_2654.SpiralBevelGearCompoundSystemDeflection))
        return value

    @property
    def spiral_bevel_meshes_compound_system_deflection(self) -> 'List[_2655.SpiralBevelGearMeshCompoundSystemDeflection]':
        '''List[SpiralBevelGearMeshCompoundSystemDeflection]: 'SpiralBevelMeshesCompoundSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelMeshesCompoundSystemDeflection, constructor.new(_2655.SpiralBevelGearMeshCompoundSystemDeflection))
        return value

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_2510.SpiralBevelGearSetSystemDeflection]':
        '''List[SpiralBevelGearSetSystemDeflection]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_2510.SpiralBevelGearSetSystemDeflection))
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_2510.SpiralBevelGearSetSystemDeflection]':
        '''List[SpiralBevelGearSetSystemDeflection]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_2510.SpiralBevelGearSetSystemDeflection))
        return value

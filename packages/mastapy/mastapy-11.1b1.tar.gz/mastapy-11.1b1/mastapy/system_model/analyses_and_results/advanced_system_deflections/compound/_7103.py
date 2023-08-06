'''_7103.py

BevelDifferentialGearSetCompoundAdvancedSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model.gears import _2223
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import _7101, _7102, _7108
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _6970
from mastapy._internal.python_net import python_net_import

_BEVEL_DIFFERENTIAL_GEAR_SET_COMPOUND_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections.Compound', 'BevelDifferentialGearSetCompoundAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelDifferentialGearSetCompoundAdvancedSystemDeflection',)


class BevelDifferentialGearSetCompoundAdvancedSystemDeflection(_7108.BevelGearSetCompoundAdvancedSystemDeflection):
    '''BevelDifferentialGearSetCompoundAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _BEVEL_DIFFERENTIAL_GEAR_SET_COMPOUND_ADVANCED_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelDifferentialGearSetCompoundAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2223.BevelDifferentialGearSet':
        '''BevelDifferentialGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2223.BevelDifferentialGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2223.BevelDifferentialGearSet':
        '''BevelDifferentialGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2223.BevelDifferentialGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def bevel_differential_gears_compound_advanced_system_deflection(self) -> 'List[_7101.BevelDifferentialGearCompoundAdvancedSystemDeflection]':
        '''List[BevelDifferentialGearCompoundAdvancedSystemDeflection]: 'BevelDifferentialGearsCompoundAdvancedSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearsCompoundAdvancedSystemDeflection, constructor.new(_7101.BevelDifferentialGearCompoundAdvancedSystemDeflection))
        return value

    @property
    def bevel_differential_meshes_compound_advanced_system_deflection(self) -> 'List[_7102.BevelDifferentialGearMeshCompoundAdvancedSystemDeflection]':
        '''List[BevelDifferentialGearMeshCompoundAdvancedSystemDeflection]: 'BevelDifferentialMeshesCompoundAdvancedSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialMeshesCompoundAdvancedSystemDeflection, constructor.new(_7102.BevelDifferentialGearMeshCompoundAdvancedSystemDeflection))
        return value

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_6970.BevelDifferentialGearSetAdvancedSystemDeflection]':
        '''List[BevelDifferentialGearSetAdvancedSystemDeflection]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_6970.BevelDifferentialGearSetAdvancedSystemDeflection))
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_6970.BevelDifferentialGearSetAdvancedSystemDeflection]':
        '''List[BevelDifferentialGearSetAdvancedSystemDeflection]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_6970.BevelDifferentialGearSetAdvancedSystemDeflection))
        return value

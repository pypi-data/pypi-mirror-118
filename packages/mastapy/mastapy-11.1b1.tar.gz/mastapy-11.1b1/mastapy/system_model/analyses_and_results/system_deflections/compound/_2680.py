'''_2680.py

WormGearSetCompoundSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model.gears import _2259
from mastapy._internal import constructor, conversion
from mastapy.gears.rating.worm import _340
from mastapy.system_model.analyses_and_results.system_deflections.compound import _2678, _2679, _2614
from mastapy.system_model.analyses_and_results.system_deflections import _2539
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_SET_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'WormGearSetCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearSetCompoundSystemDeflection',)


class WormGearSetCompoundSystemDeflection(_2614.GearSetCompoundSystemDeflection):
    '''WormGearSetCompoundSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _WORM_GEAR_SET_COMPOUND_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'WormGearSetCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2259.WormGearSet':
        '''WormGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2259.WormGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2259.WormGearSet':
        '''WormGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2259.WormGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def worm_gear_set_rating(self) -> '_340.WormGearSetDutyCycleRating':
        '''WormGearSetDutyCycleRating: 'WormGearSetRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_340.WormGearSetDutyCycleRating)(self.wrapped.WormGearSetRating) if self.wrapped.WormGearSetRating else None

    @property
    def worm_gears_compound_system_deflection(self) -> 'List[_2678.WormGearCompoundSystemDeflection]':
        '''List[WormGearCompoundSystemDeflection]: 'WormGearsCompoundSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearsCompoundSystemDeflection, constructor.new(_2678.WormGearCompoundSystemDeflection))
        return value

    @property
    def worm_meshes_compound_system_deflection(self) -> 'List[_2679.WormGearMeshCompoundSystemDeflection]':
        '''List[WormGearMeshCompoundSystemDeflection]: 'WormMeshesCompoundSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormMeshesCompoundSystemDeflection, constructor.new(_2679.WormGearMeshCompoundSystemDeflection))
        return value

    @property
    def assembly_analysis_cases_ready(self) -> 'List[_2539.WormGearSetSystemDeflection]':
        '''List[WormGearSetSystemDeflection]: 'AssemblyAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCasesReady, constructor.new(_2539.WormGearSetSystemDeflection))
        return value

    @property
    def assembly_analysis_cases(self) -> 'List[_2539.WormGearSetSystemDeflection]':
        '''List[WormGearSetSystemDeflection]: 'AssemblyAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAnalysisCases, constructor.new(_2539.WormGearSetSystemDeflection))
        return value

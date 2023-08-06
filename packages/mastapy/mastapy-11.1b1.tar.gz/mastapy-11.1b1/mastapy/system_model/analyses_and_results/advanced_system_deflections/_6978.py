'''_6978.py

ClutchAdvancedSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2285
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6516
from mastapy.system_model.analyses_and_results.system_deflections import _2415
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _6995
from mastapy._internal.python_net import python_net_import

_CLUTCH_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections', 'ClutchAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('ClutchAdvancedSystemDeflection',)


class ClutchAdvancedSystemDeflection(_6995.CouplingAdvancedSystemDeflection):
    '''ClutchAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _CLUTCH_ADVANCED_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ClutchAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2285.Clutch':
        '''Clutch: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2285.Clutch)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6516.ClutchLoadCase':
        '''ClutchLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6516.ClutchLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def assembly_system_deflection_results(self) -> 'List[_2415.ClutchSystemDeflection]':
        '''List[ClutchSystemDeflection]: 'AssemblySystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblySystemDeflectionResults, constructor.new(_2415.ClutchSystemDeflection))
        return value

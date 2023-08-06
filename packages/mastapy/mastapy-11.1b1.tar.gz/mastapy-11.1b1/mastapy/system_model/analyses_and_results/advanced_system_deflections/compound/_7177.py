'''_7177.py

PowerLoadCompoundAdvancedSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model import _2180
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _7047
from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import _7212
from mastapy._internal.python_net import python_net_import

_POWER_LOAD_COMPOUND_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections.Compound', 'PowerLoadCompoundAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('PowerLoadCompoundAdvancedSystemDeflection',)


class PowerLoadCompoundAdvancedSystemDeflection(_7212.VirtualComponentCompoundAdvancedSystemDeflection):
    '''PowerLoadCompoundAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _POWER_LOAD_COMPOUND_ADVANCED_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PowerLoadCompoundAdvancedSystemDeflection.TYPE'):
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
    def component_analysis_cases_ready(self) -> 'List[_7047.PowerLoadAdvancedSystemDeflection]':
        '''List[PowerLoadAdvancedSystemDeflection]: 'ComponentAnalysisCasesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCasesReady, constructor.new(_7047.PowerLoadAdvancedSystemDeflection))
        return value

    @property
    def component_analysis_cases(self) -> 'List[_7047.PowerLoadAdvancedSystemDeflection]':
        '''List[PowerLoadAdvancedSystemDeflection]: 'ComponentAnalysisCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAnalysisCases, constructor.new(_7047.PowerLoadAdvancedSystemDeflection))
        return value

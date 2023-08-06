'''_2464.py

GuideDxfModelSystemDeflection
'''


from mastapy.system_model.part_model import _2163
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6578
from mastapy.system_model.analyses_and_results.power_flows import _3794
from mastapy.system_model.analyses_and_results.system_deflections import _2417
from mastapy._internal.python_net import python_net_import

_GUIDE_DXF_MODEL_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'GuideDxfModelSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('GuideDxfModelSystemDeflection',)


class GuideDxfModelSystemDeflection(_2417.ComponentSystemDeflection):
    '''GuideDxfModelSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _GUIDE_DXF_MODEL_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'GuideDxfModelSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2163.GuideDxfModel':
        '''GuideDxfModel: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2163.GuideDxfModel)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6578.GuideDxfModelLoadCase':
        '''GuideDxfModelLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6578.GuideDxfModelLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def power_flow_results(self) -> '_3794.GuideDxfModelPowerFlow':
        '''GuideDxfModelPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3794.GuideDxfModelPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None

'''_2413.py

ClutchConnectionSystemDeflection
'''


from mastapy.system_model.connections_and_sockets.couplings import _2051
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6514
from mastapy.system_model.analyses_and_results.power_flows import _3753
from mastapy.system_model.analyses_and_results.system_deflections import _2431
from mastapy._internal.python_net import python_net_import

_CLUTCH_CONNECTION_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'ClutchConnectionSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('ClutchConnectionSystemDeflection',)


class ClutchConnectionSystemDeflection(_2431.CouplingConnectionSystemDeflection):
    '''ClutchConnectionSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _CLUTCH_CONNECTION_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ClutchConnectionSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_2051.ClutchConnection':
        '''ClutchConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2051.ClutchConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6514.ClutchConnectionLoadCase':
        '''ClutchConnectionLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6514.ClutchConnectionLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None

    @property
    def power_flow_results(self) -> '_3753.ClutchConnectionPowerFlow':
        '''ClutchConnectionPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3753.ClutchConnectionPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None

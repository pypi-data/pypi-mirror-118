'''_1981.py

Connection
'''


from mastapy._internal.implicit import list_with_selected_item
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy._internal import constructor
from mastapy.system_model.connections_and_sockets import (
    _2005, _1975, _1976, _1983,
    _1985, _1987, _1988, _1989,
    _1991, _1992, _1993, _1994,
    _1995, _1997, _1998, _1999,
    _2002, _2003
)
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.connections_and_sockets.gears import (
    _2009, _2011, _2013, _2015,
    _2017, _2019, _2021, _2023,
    _2025, _2026, _2030, _2031,
    _2033, _2035, _2037, _2039,
    _2041
)
from mastapy.system_model.connections_and_sockets.cycloidal import (
    _2042, _2043, _2045, _2046,
    _2048, _2049
)
from mastapy.system_model.connections_and_sockets.couplings import (
    _2052, _2054, _2056, _2058,
    _2060, _2062, _2063
)
from mastapy.system_model.part_model import (
    _2153, _2145, _2146, _2149,
    _2151, _2156, _2157, _2160,
    _2161, _2163, _2170, _2171,
    _2172, _2174, _2177, _2179,
    _2180, _2185, _2187
)
from mastapy.system_model.part_model.shaft_model import _2190
from mastapy.system_model.part_model.gears import (
    _2220, _2222, _2224, _2225,
    _2226, _2228, _2230, _2232,
    _2234, _2235, _2237, _2241,
    _2243, _2245, _2247, _2250,
    _2252, _2254, _2256, _2257,
    _2258, _2260
)
from mastapy.system_model.part_model.cycloidal import _2276, _2277
from mastapy.system_model.part_model.couplings import (
    _2286, _2289, _2291, _2294,
    _2296, _2297, _2303, _2305,
    _2308, _2311, _2312, _2313,
    _2315, _2317
)
from mastapy._internal.python_net import python_net_import
from mastapy.system_model import _1919

_COMPONENT = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'Component')
_SOCKET = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'Socket')
_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'Connection')


__docformat__ = 'restructuredtext en'
__all__ = ('Connection',)


class Connection(_1919.DesignEntity):
    '''Connection

    This is a mastapy class.
    '''

    TYPE = _CONNECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'Connection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def drawing_position(self) -> 'list_with_selected_item.ListWithSelectedItem_str':
        '''list_with_selected_item.ListWithSelectedItem_str: 'DrawingPosition' is the original name of this property.'''

        return constructor.new(list_with_selected_item.ListWithSelectedItem_str)(self.wrapped.DrawingPosition) if self.wrapped.DrawingPosition else None

    @drawing_position.setter
    def drawing_position(self, value: 'list_with_selected_item.ListWithSelectedItem_str.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_str.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_str.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else None)
        self.wrapped.DrawingPosition = value

    @property
    def speed_ratio_from_a_to_b(self) -> 'float':
        '''float: 'SpeedRatioFromAToB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SpeedRatioFromAToB

    @property
    def torque_ratio_from_a_to_b(self) -> 'float':
        '''float: 'TorqueRatioFromAToB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TorqueRatioFromAToB

    @property
    def unique_name(self) -> 'str':
        '''str: 'UniqueName' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.UniqueName

    @property
    def connection_id(self) -> 'str':
        '''str: 'ConnectionID' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ConnectionID

    @property
    def socket_a(self) -> '_2005.Socket':
        '''Socket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2005.Socket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to Socket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_bearing_inner_socket(self) -> '_1975.BearingInnerSocket':
        '''BearingInnerSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1975.BearingInnerSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to BearingInnerSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_bearing_outer_socket(self) -> '_1976.BearingOuterSocket':
        '''BearingOuterSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1976.BearingOuterSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to BearingOuterSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_cvt_pulley_socket(self) -> '_1983.CVTPulleySocket':
        '''CVTPulleySocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1983.CVTPulleySocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to CVTPulleySocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_cylindrical_socket(self) -> '_1985.CylindricalSocket':
        '''CylindricalSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1985.CylindricalSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to CylindricalSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_electric_machine_stator_socket(self) -> '_1987.ElectricMachineStatorSocket':
        '''ElectricMachineStatorSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1987.ElectricMachineStatorSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to ElectricMachineStatorSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_inner_shaft_socket(self) -> '_1988.InnerShaftSocket':
        '''InnerShaftSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1988.InnerShaftSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to InnerShaftSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_inner_shaft_socket_base(self) -> '_1989.InnerShaftSocketBase':
        '''InnerShaftSocketBase: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1989.InnerShaftSocketBase.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to InnerShaftSocketBase. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_mountable_component_inner_socket(self) -> '_1991.MountableComponentInnerSocket':
        '''MountableComponentInnerSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1991.MountableComponentInnerSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to MountableComponentInnerSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_mountable_component_outer_socket(self) -> '_1992.MountableComponentOuterSocket':
        '''MountableComponentOuterSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1992.MountableComponentOuterSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to MountableComponentOuterSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_mountable_component_socket(self) -> '_1993.MountableComponentSocket':
        '''MountableComponentSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1993.MountableComponentSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to MountableComponentSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_outer_shaft_socket(self) -> '_1994.OuterShaftSocket':
        '''OuterShaftSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1994.OuterShaftSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to OuterShaftSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_outer_shaft_socket_base(self) -> '_1995.OuterShaftSocketBase':
        '''OuterShaftSocketBase: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1995.OuterShaftSocketBase.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to OuterShaftSocketBase. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_planetary_socket(self) -> '_1997.PlanetarySocket':
        '''PlanetarySocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1997.PlanetarySocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to PlanetarySocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_planetary_socket_base(self) -> '_1998.PlanetarySocketBase':
        '''PlanetarySocketBase: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1998.PlanetarySocketBase.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to PlanetarySocketBase. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_pulley_socket(self) -> '_1999.PulleySocket':
        '''PulleySocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1999.PulleySocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to PulleySocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_rolling_ring_socket(self) -> '_2002.RollingRingSocket':
        '''RollingRingSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2002.RollingRingSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to RollingRingSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_shaft_socket(self) -> '_2003.ShaftSocket':
        '''ShaftSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2003.ShaftSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to ShaftSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_agma_gleason_conical_gear_teeth_socket(self) -> '_2009.AGMAGleasonConicalGearTeethSocket':
        '''AGMAGleasonConicalGearTeethSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2009.AGMAGleasonConicalGearTeethSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to AGMAGleasonConicalGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_bevel_differential_gear_teeth_socket(self) -> '_2011.BevelDifferentialGearTeethSocket':
        '''BevelDifferentialGearTeethSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2011.BevelDifferentialGearTeethSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to BevelDifferentialGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_bevel_gear_teeth_socket(self) -> '_2013.BevelGearTeethSocket':
        '''BevelGearTeethSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2013.BevelGearTeethSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to BevelGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_concept_gear_teeth_socket(self) -> '_2015.ConceptGearTeethSocket':
        '''ConceptGearTeethSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2015.ConceptGearTeethSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to ConceptGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_conical_gear_teeth_socket(self) -> '_2017.ConicalGearTeethSocket':
        '''ConicalGearTeethSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2017.ConicalGearTeethSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to ConicalGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_cylindrical_gear_teeth_socket(self) -> '_2019.CylindricalGearTeethSocket':
        '''CylindricalGearTeethSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2019.CylindricalGearTeethSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to CylindricalGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_face_gear_teeth_socket(self) -> '_2021.FaceGearTeethSocket':
        '''FaceGearTeethSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2021.FaceGearTeethSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to FaceGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_gear_teeth_socket(self) -> '_2023.GearTeethSocket':
        '''GearTeethSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2023.GearTeethSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to GearTeethSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_hypoid_gear_teeth_socket(self) -> '_2025.HypoidGearTeethSocket':
        '''HypoidGearTeethSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2025.HypoidGearTeethSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to HypoidGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_klingelnberg_conical_gear_teeth_socket(self) -> '_2026.KlingelnbergConicalGearTeethSocket':
        '''KlingelnbergConicalGearTeethSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2026.KlingelnbergConicalGearTeethSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to KlingelnbergConicalGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_klingelnberg_hypoid_gear_teeth_socket(self) -> '_2030.KlingelnbergHypoidGearTeethSocket':
        '''KlingelnbergHypoidGearTeethSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2030.KlingelnbergHypoidGearTeethSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to KlingelnbergHypoidGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_klingelnberg_spiral_bevel_gear_teeth_socket(self) -> '_2031.KlingelnbergSpiralBevelGearTeethSocket':
        '''KlingelnbergSpiralBevelGearTeethSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2031.KlingelnbergSpiralBevelGearTeethSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to KlingelnbergSpiralBevelGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_spiral_bevel_gear_teeth_socket(self) -> '_2033.SpiralBevelGearTeethSocket':
        '''SpiralBevelGearTeethSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2033.SpiralBevelGearTeethSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to SpiralBevelGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_straight_bevel_diff_gear_teeth_socket(self) -> '_2035.StraightBevelDiffGearTeethSocket':
        '''StraightBevelDiffGearTeethSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2035.StraightBevelDiffGearTeethSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to StraightBevelDiffGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_straight_bevel_gear_teeth_socket(self) -> '_2037.StraightBevelGearTeethSocket':
        '''StraightBevelGearTeethSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2037.StraightBevelGearTeethSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to StraightBevelGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_worm_gear_teeth_socket(self) -> '_2039.WormGearTeethSocket':
        '''WormGearTeethSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2039.WormGearTeethSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to WormGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_zerol_bevel_gear_teeth_socket(self) -> '_2041.ZerolBevelGearTeethSocket':
        '''ZerolBevelGearTeethSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2041.ZerolBevelGearTeethSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to ZerolBevelGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_cycloidal_disc_axial_left_socket(self) -> '_2042.CycloidalDiscAxialLeftSocket':
        '''CycloidalDiscAxialLeftSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2042.CycloidalDiscAxialLeftSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to CycloidalDiscAxialLeftSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_cycloidal_disc_axial_right_socket(self) -> '_2043.CycloidalDiscAxialRightSocket':
        '''CycloidalDiscAxialRightSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2043.CycloidalDiscAxialRightSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to CycloidalDiscAxialRightSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_cycloidal_disc_inner_socket(self) -> '_2045.CycloidalDiscInnerSocket':
        '''CycloidalDiscInnerSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2045.CycloidalDiscInnerSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to CycloidalDiscInnerSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_cycloidal_disc_outer_socket(self) -> '_2046.CycloidalDiscOuterSocket':
        '''CycloidalDiscOuterSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2046.CycloidalDiscOuterSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to CycloidalDiscOuterSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_cycloidal_disc_planetary_bearing_socket(self) -> '_2048.CycloidalDiscPlanetaryBearingSocket':
        '''CycloidalDiscPlanetaryBearingSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2048.CycloidalDiscPlanetaryBearingSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to CycloidalDiscPlanetaryBearingSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_ring_pins_socket(self) -> '_2049.RingPinsSocket':
        '''RingPinsSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2049.RingPinsSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to RingPinsSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_clutch_socket(self) -> '_2052.ClutchSocket':
        '''ClutchSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2052.ClutchSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to ClutchSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_concept_coupling_socket(self) -> '_2054.ConceptCouplingSocket':
        '''ConceptCouplingSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2054.ConceptCouplingSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to ConceptCouplingSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_coupling_socket(self) -> '_2056.CouplingSocket':
        '''CouplingSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2056.CouplingSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to CouplingSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_part_to_part_shear_coupling_socket(self) -> '_2058.PartToPartShearCouplingSocket':
        '''PartToPartShearCouplingSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2058.PartToPartShearCouplingSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to PartToPartShearCouplingSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_spring_damper_socket(self) -> '_2060.SpringDamperSocket':
        '''SpringDamperSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2060.SpringDamperSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to SpringDamperSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_torque_converter_pump_socket(self) -> '_2062.TorqueConverterPumpSocket':
        '''TorqueConverterPumpSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2062.TorqueConverterPumpSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to TorqueConverterPumpSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_a_of_type_torque_converter_turbine_socket(self) -> '_2063.TorqueConverterTurbineSocket':
        '''TorqueConverterTurbineSocket: 'SocketA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2063.TorqueConverterTurbineSocket.TYPE not in self.wrapped.SocketA.__class__.__mro__:
            raise CastException('Failed to cast socket_a to TorqueConverterTurbineSocket. Expected: {}.'.format(self.wrapped.SocketA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketA.__class__)(self.wrapped.SocketA) if self.wrapped.SocketA else None

    @property
    def socket_b(self) -> '_2005.Socket':
        '''Socket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2005.Socket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to Socket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_bearing_inner_socket(self) -> '_1975.BearingInnerSocket':
        '''BearingInnerSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1975.BearingInnerSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to BearingInnerSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_bearing_outer_socket(self) -> '_1976.BearingOuterSocket':
        '''BearingOuterSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1976.BearingOuterSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to BearingOuterSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_cvt_pulley_socket(self) -> '_1983.CVTPulleySocket':
        '''CVTPulleySocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1983.CVTPulleySocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to CVTPulleySocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_cylindrical_socket(self) -> '_1985.CylindricalSocket':
        '''CylindricalSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1985.CylindricalSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to CylindricalSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_electric_machine_stator_socket(self) -> '_1987.ElectricMachineStatorSocket':
        '''ElectricMachineStatorSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1987.ElectricMachineStatorSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to ElectricMachineStatorSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_inner_shaft_socket(self) -> '_1988.InnerShaftSocket':
        '''InnerShaftSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1988.InnerShaftSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to InnerShaftSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_inner_shaft_socket_base(self) -> '_1989.InnerShaftSocketBase':
        '''InnerShaftSocketBase: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1989.InnerShaftSocketBase.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to InnerShaftSocketBase. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_mountable_component_inner_socket(self) -> '_1991.MountableComponentInnerSocket':
        '''MountableComponentInnerSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1991.MountableComponentInnerSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to MountableComponentInnerSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_mountable_component_outer_socket(self) -> '_1992.MountableComponentOuterSocket':
        '''MountableComponentOuterSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1992.MountableComponentOuterSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to MountableComponentOuterSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_mountable_component_socket(self) -> '_1993.MountableComponentSocket':
        '''MountableComponentSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1993.MountableComponentSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to MountableComponentSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_outer_shaft_socket(self) -> '_1994.OuterShaftSocket':
        '''OuterShaftSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1994.OuterShaftSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to OuterShaftSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_outer_shaft_socket_base(self) -> '_1995.OuterShaftSocketBase':
        '''OuterShaftSocketBase: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1995.OuterShaftSocketBase.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to OuterShaftSocketBase. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_planetary_socket(self) -> '_1997.PlanetarySocket':
        '''PlanetarySocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1997.PlanetarySocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to PlanetarySocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_planetary_socket_base(self) -> '_1998.PlanetarySocketBase':
        '''PlanetarySocketBase: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1998.PlanetarySocketBase.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to PlanetarySocketBase. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_pulley_socket(self) -> '_1999.PulleySocket':
        '''PulleySocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1999.PulleySocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to PulleySocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_rolling_ring_socket(self) -> '_2002.RollingRingSocket':
        '''RollingRingSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2002.RollingRingSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to RollingRingSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_shaft_socket(self) -> '_2003.ShaftSocket':
        '''ShaftSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2003.ShaftSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to ShaftSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_agma_gleason_conical_gear_teeth_socket(self) -> '_2009.AGMAGleasonConicalGearTeethSocket':
        '''AGMAGleasonConicalGearTeethSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2009.AGMAGleasonConicalGearTeethSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to AGMAGleasonConicalGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_bevel_differential_gear_teeth_socket(self) -> '_2011.BevelDifferentialGearTeethSocket':
        '''BevelDifferentialGearTeethSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2011.BevelDifferentialGearTeethSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to BevelDifferentialGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_bevel_gear_teeth_socket(self) -> '_2013.BevelGearTeethSocket':
        '''BevelGearTeethSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2013.BevelGearTeethSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to BevelGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_concept_gear_teeth_socket(self) -> '_2015.ConceptGearTeethSocket':
        '''ConceptGearTeethSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2015.ConceptGearTeethSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to ConceptGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_conical_gear_teeth_socket(self) -> '_2017.ConicalGearTeethSocket':
        '''ConicalGearTeethSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2017.ConicalGearTeethSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to ConicalGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_cylindrical_gear_teeth_socket(self) -> '_2019.CylindricalGearTeethSocket':
        '''CylindricalGearTeethSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2019.CylindricalGearTeethSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to CylindricalGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_face_gear_teeth_socket(self) -> '_2021.FaceGearTeethSocket':
        '''FaceGearTeethSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2021.FaceGearTeethSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to FaceGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_gear_teeth_socket(self) -> '_2023.GearTeethSocket':
        '''GearTeethSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2023.GearTeethSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to GearTeethSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_hypoid_gear_teeth_socket(self) -> '_2025.HypoidGearTeethSocket':
        '''HypoidGearTeethSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2025.HypoidGearTeethSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to HypoidGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_klingelnberg_conical_gear_teeth_socket(self) -> '_2026.KlingelnbergConicalGearTeethSocket':
        '''KlingelnbergConicalGearTeethSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2026.KlingelnbergConicalGearTeethSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to KlingelnbergConicalGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_klingelnberg_hypoid_gear_teeth_socket(self) -> '_2030.KlingelnbergHypoidGearTeethSocket':
        '''KlingelnbergHypoidGearTeethSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2030.KlingelnbergHypoidGearTeethSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to KlingelnbergHypoidGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_klingelnberg_spiral_bevel_gear_teeth_socket(self) -> '_2031.KlingelnbergSpiralBevelGearTeethSocket':
        '''KlingelnbergSpiralBevelGearTeethSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2031.KlingelnbergSpiralBevelGearTeethSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to KlingelnbergSpiralBevelGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_spiral_bevel_gear_teeth_socket(self) -> '_2033.SpiralBevelGearTeethSocket':
        '''SpiralBevelGearTeethSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2033.SpiralBevelGearTeethSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to SpiralBevelGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_straight_bevel_diff_gear_teeth_socket(self) -> '_2035.StraightBevelDiffGearTeethSocket':
        '''StraightBevelDiffGearTeethSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2035.StraightBevelDiffGearTeethSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to StraightBevelDiffGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_straight_bevel_gear_teeth_socket(self) -> '_2037.StraightBevelGearTeethSocket':
        '''StraightBevelGearTeethSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2037.StraightBevelGearTeethSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to StraightBevelGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_worm_gear_teeth_socket(self) -> '_2039.WormGearTeethSocket':
        '''WormGearTeethSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2039.WormGearTeethSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to WormGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_zerol_bevel_gear_teeth_socket(self) -> '_2041.ZerolBevelGearTeethSocket':
        '''ZerolBevelGearTeethSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2041.ZerolBevelGearTeethSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to ZerolBevelGearTeethSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_cycloidal_disc_axial_left_socket(self) -> '_2042.CycloidalDiscAxialLeftSocket':
        '''CycloidalDiscAxialLeftSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2042.CycloidalDiscAxialLeftSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to CycloidalDiscAxialLeftSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_cycloidal_disc_axial_right_socket(self) -> '_2043.CycloidalDiscAxialRightSocket':
        '''CycloidalDiscAxialRightSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2043.CycloidalDiscAxialRightSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to CycloidalDiscAxialRightSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_cycloidal_disc_inner_socket(self) -> '_2045.CycloidalDiscInnerSocket':
        '''CycloidalDiscInnerSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2045.CycloidalDiscInnerSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to CycloidalDiscInnerSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_cycloidal_disc_outer_socket(self) -> '_2046.CycloidalDiscOuterSocket':
        '''CycloidalDiscOuterSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2046.CycloidalDiscOuterSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to CycloidalDiscOuterSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_cycloidal_disc_planetary_bearing_socket(self) -> '_2048.CycloidalDiscPlanetaryBearingSocket':
        '''CycloidalDiscPlanetaryBearingSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2048.CycloidalDiscPlanetaryBearingSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to CycloidalDiscPlanetaryBearingSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_ring_pins_socket(self) -> '_2049.RingPinsSocket':
        '''RingPinsSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2049.RingPinsSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to RingPinsSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_clutch_socket(self) -> '_2052.ClutchSocket':
        '''ClutchSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2052.ClutchSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to ClutchSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_concept_coupling_socket(self) -> '_2054.ConceptCouplingSocket':
        '''ConceptCouplingSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2054.ConceptCouplingSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to ConceptCouplingSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_coupling_socket(self) -> '_2056.CouplingSocket':
        '''CouplingSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2056.CouplingSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to CouplingSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_part_to_part_shear_coupling_socket(self) -> '_2058.PartToPartShearCouplingSocket':
        '''PartToPartShearCouplingSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2058.PartToPartShearCouplingSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to PartToPartShearCouplingSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_spring_damper_socket(self) -> '_2060.SpringDamperSocket':
        '''SpringDamperSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2060.SpringDamperSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to SpringDamperSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_torque_converter_pump_socket(self) -> '_2062.TorqueConverterPumpSocket':
        '''TorqueConverterPumpSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2062.TorqueConverterPumpSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to TorqueConverterPumpSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def socket_b_of_type_torque_converter_turbine_socket(self) -> '_2063.TorqueConverterTurbineSocket':
        '''TorqueConverterTurbineSocket: 'SocketB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2063.TorqueConverterTurbineSocket.TYPE not in self.wrapped.SocketB.__class__.__mro__:
            raise CastException('Failed to cast socket_b to TorqueConverterTurbineSocket. Expected: {}.'.format(self.wrapped.SocketB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.SocketB.__class__)(self.wrapped.SocketB) if self.wrapped.SocketB else None

    @property
    def owner_a(self) -> '_2153.Component':
        '''Component: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2153.Component.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to Component. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_abstract_shaft(self) -> '_2145.AbstractShaft':
        '''AbstractShaft: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2145.AbstractShaft.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to AbstractShaft. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_abstract_shaft_or_housing(self) -> '_2146.AbstractShaftOrHousing':
        '''AbstractShaftOrHousing: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2146.AbstractShaftOrHousing.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to AbstractShaftOrHousing. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_bearing(self) -> '_2149.Bearing':
        '''Bearing: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2149.Bearing.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to Bearing. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_bolt(self) -> '_2151.Bolt':
        '''Bolt: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2151.Bolt.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to Bolt. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_connector(self) -> '_2156.Connector':
        '''Connector: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2156.Connector.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to Connector. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_datum(self) -> '_2157.Datum':
        '''Datum: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2157.Datum.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to Datum. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_external_cad_model(self) -> '_2160.ExternalCADModel':
        '''ExternalCADModel: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2160.ExternalCADModel.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to ExternalCADModel. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_fe_part(self) -> '_2161.FEPart':
        '''FEPart: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2161.FEPart.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to FEPart. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_guide_dxf_model(self) -> '_2163.GuideDxfModel':
        '''GuideDxfModel: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2163.GuideDxfModel.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to GuideDxfModel. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_mass_disc(self) -> '_2170.MassDisc':
        '''MassDisc: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2170.MassDisc.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to MassDisc. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_measurement_component(self) -> '_2171.MeasurementComponent':
        '''MeasurementComponent: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2171.MeasurementComponent.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to MeasurementComponent. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_mountable_component(self) -> '_2172.MountableComponent':
        '''MountableComponent: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2172.MountableComponent.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to MountableComponent. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_oil_seal(self) -> '_2174.OilSeal':
        '''OilSeal: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2174.OilSeal.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to OilSeal. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_planet_carrier(self) -> '_2177.PlanetCarrier':
        '''PlanetCarrier: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2177.PlanetCarrier.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to PlanetCarrier. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_point_load(self) -> '_2179.PointLoad':
        '''PointLoad: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2179.PointLoad.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to PointLoad. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_power_load(self) -> '_2180.PowerLoad':
        '''PowerLoad: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2180.PowerLoad.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to PowerLoad. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_unbalanced_mass(self) -> '_2185.UnbalancedMass':
        '''UnbalancedMass: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2185.UnbalancedMass.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to UnbalancedMass. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_virtual_component(self) -> '_2187.VirtualComponent':
        '''VirtualComponent: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2187.VirtualComponent.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to VirtualComponent. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_shaft(self) -> '_2190.Shaft':
        '''Shaft: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2190.Shaft.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to Shaft. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_agma_gleason_conical_gear(self) -> '_2220.AGMAGleasonConicalGear':
        '''AGMAGleasonConicalGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2220.AGMAGleasonConicalGear.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to AGMAGleasonConicalGear. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_bevel_differential_gear(self) -> '_2222.BevelDifferentialGear':
        '''BevelDifferentialGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2222.BevelDifferentialGear.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to BevelDifferentialGear. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_bevel_differential_planet_gear(self) -> '_2224.BevelDifferentialPlanetGear':
        '''BevelDifferentialPlanetGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2224.BevelDifferentialPlanetGear.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to BevelDifferentialPlanetGear. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_bevel_differential_sun_gear(self) -> '_2225.BevelDifferentialSunGear':
        '''BevelDifferentialSunGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2225.BevelDifferentialSunGear.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to BevelDifferentialSunGear. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_bevel_gear(self) -> '_2226.BevelGear':
        '''BevelGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2226.BevelGear.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to BevelGear. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_concept_gear(self) -> '_2228.ConceptGear':
        '''ConceptGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2228.ConceptGear.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to ConceptGear. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_conical_gear(self) -> '_2230.ConicalGear':
        '''ConicalGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2230.ConicalGear.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to ConicalGear. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_cylindrical_gear(self) -> '_2232.CylindricalGear':
        '''CylindricalGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2232.CylindricalGear.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to CylindricalGear. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_cylindrical_planet_gear(self) -> '_2234.CylindricalPlanetGear':
        '''CylindricalPlanetGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2234.CylindricalPlanetGear.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to CylindricalPlanetGear. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_face_gear(self) -> '_2235.FaceGear':
        '''FaceGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2235.FaceGear.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to FaceGear. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_gear(self) -> '_2237.Gear':
        '''Gear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2237.Gear.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to Gear. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_hypoid_gear(self) -> '_2241.HypoidGear':
        '''HypoidGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2241.HypoidGear.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to HypoidGear. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_klingelnberg_cyclo_palloid_conical_gear(self) -> '_2243.KlingelnbergCycloPalloidConicalGear':
        '''KlingelnbergCycloPalloidConicalGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2243.KlingelnbergCycloPalloidConicalGear.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to KlingelnbergCycloPalloidConicalGear. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_klingelnberg_cyclo_palloid_hypoid_gear(self) -> '_2245.KlingelnbergCycloPalloidHypoidGear':
        '''KlingelnbergCycloPalloidHypoidGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2245.KlingelnbergCycloPalloidHypoidGear.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to KlingelnbergCycloPalloidHypoidGear. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear(self) -> '_2247.KlingelnbergCycloPalloidSpiralBevelGear':
        '''KlingelnbergCycloPalloidSpiralBevelGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2247.KlingelnbergCycloPalloidSpiralBevelGear.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to KlingelnbergCycloPalloidSpiralBevelGear. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_spiral_bevel_gear(self) -> '_2250.SpiralBevelGear':
        '''SpiralBevelGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2250.SpiralBevelGear.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to SpiralBevelGear. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_straight_bevel_diff_gear(self) -> '_2252.StraightBevelDiffGear':
        '''StraightBevelDiffGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2252.StraightBevelDiffGear.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to StraightBevelDiffGear. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_straight_bevel_gear(self) -> '_2254.StraightBevelGear':
        '''StraightBevelGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2254.StraightBevelGear.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to StraightBevelGear. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_straight_bevel_planet_gear(self) -> '_2256.StraightBevelPlanetGear':
        '''StraightBevelPlanetGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2256.StraightBevelPlanetGear.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to StraightBevelPlanetGear. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_straight_bevel_sun_gear(self) -> '_2257.StraightBevelSunGear':
        '''StraightBevelSunGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2257.StraightBevelSunGear.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to StraightBevelSunGear. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_worm_gear(self) -> '_2258.WormGear':
        '''WormGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2258.WormGear.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to WormGear. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_zerol_bevel_gear(self) -> '_2260.ZerolBevelGear':
        '''ZerolBevelGear: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2260.ZerolBevelGear.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to ZerolBevelGear. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_cycloidal_disc(self) -> '_2276.CycloidalDisc':
        '''CycloidalDisc: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2276.CycloidalDisc.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to CycloidalDisc. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_ring_pins(self) -> '_2277.RingPins':
        '''RingPins: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2277.RingPins.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to RingPins. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_clutch_half(self) -> '_2286.ClutchHalf':
        '''ClutchHalf: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2286.ClutchHalf.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to ClutchHalf. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_concept_coupling_half(self) -> '_2289.ConceptCouplingHalf':
        '''ConceptCouplingHalf: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2289.ConceptCouplingHalf.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to ConceptCouplingHalf. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_coupling_half(self) -> '_2291.CouplingHalf':
        '''CouplingHalf: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2291.CouplingHalf.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to CouplingHalf. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_cvt_pulley(self) -> '_2294.CVTPulley':
        '''CVTPulley: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2294.CVTPulley.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to CVTPulley. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_part_to_part_shear_coupling_half(self) -> '_2296.PartToPartShearCouplingHalf':
        '''PartToPartShearCouplingHalf: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2296.PartToPartShearCouplingHalf.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to PartToPartShearCouplingHalf. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_pulley(self) -> '_2297.Pulley':
        '''Pulley: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2297.Pulley.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to Pulley. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_rolling_ring(self) -> '_2303.RollingRing':
        '''RollingRing: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2303.RollingRing.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to RollingRing. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_shaft_hub_connection(self) -> '_2305.ShaftHubConnection':
        '''ShaftHubConnection: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2305.ShaftHubConnection.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to ShaftHubConnection. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_spring_damper_half(self) -> '_2308.SpringDamperHalf':
        '''SpringDamperHalf: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2308.SpringDamperHalf.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to SpringDamperHalf. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_synchroniser_half(self) -> '_2311.SynchroniserHalf':
        '''SynchroniserHalf: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2311.SynchroniserHalf.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to SynchroniserHalf. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_synchroniser_part(self) -> '_2312.SynchroniserPart':
        '''SynchroniserPart: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2312.SynchroniserPart.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to SynchroniserPart. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_synchroniser_sleeve(self) -> '_2313.SynchroniserSleeve':
        '''SynchroniserSleeve: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2313.SynchroniserSleeve.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to SynchroniserSleeve. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_torque_converter_pump(self) -> '_2315.TorqueConverterPump':
        '''TorqueConverterPump: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2315.TorqueConverterPump.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to TorqueConverterPump. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_a_of_type_torque_converter_turbine(self) -> '_2317.TorqueConverterTurbine':
        '''TorqueConverterTurbine: 'OwnerA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2317.TorqueConverterTurbine.TYPE not in self.wrapped.OwnerA.__class__.__mro__:
            raise CastException('Failed to cast owner_a to TorqueConverterTurbine. Expected: {}.'.format(self.wrapped.OwnerA.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerA.__class__)(self.wrapped.OwnerA) if self.wrapped.OwnerA else None

    @property
    def owner_b(self) -> '_2153.Component':
        '''Component: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2153.Component.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to Component. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_abstract_shaft(self) -> '_2145.AbstractShaft':
        '''AbstractShaft: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2145.AbstractShaft.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to AbstractShaft. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_abstract_shaft_or_housing(self) -> '_2146.AbstractShaftOrHousing':
        '''AbstractShaftOrHousing: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2146.AbstractShaftOrHousing.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to AbstractShaftOrHousing. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_bearing(self) -> '_2149.Bearing':
        '''Bearing: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2149.Bearing.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to Bearing. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_bolt(self) -> '_2151.Bolt':
        '''Bolt: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2151.Bolt.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to Bolt. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_connector(self) -> '_2156.Connector':
        '''Connector: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2156.Connector.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to Connector. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_datum(self) -> '_2157.Datum':
        '''Datum: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2157.Datum.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to Datum. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_external_cad_model(self) -> '_2160.ExternalCADModel':
        '''ExternalCADModel: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2160.ExternalCADModel.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to ExternalCADModel. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_fe_part(self) -> '_2161.FEPart':
        '''FEPart: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2161.FEPart.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to FEPart. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_guide_dxf_model(self) -> '_2163.GuideDxfModel':
        '''GuideDxfModel: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2163.GuideDxfModel.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to GuideDxfModel. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_mass_disc(self) -> '_2170.MassDisc':
        '''MassDisc: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2170.MassDisc.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to MassDisc. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_measurement_component(self) -> '_2171.MeasurementComponent':
        '''MeasurementComponent: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2171.MeasurementComponent.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to MeasurementComponent. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_mountable_component(self) -> '_2172.MountableComponent':
        '''MountableComponent: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2172.MountableComponent.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to MountableComponent. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_oil_seal(self) -> '_2174.OilSeal':
        '''OilSeal: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2174.OilSeal.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to OilSeal. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_planet_carrier(self) -> '_2177.PlanetCarrier':
        '''PlanetCarrier: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2177.PlanetCarrier.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to PlanetCarrier. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_point_load(self) -> '_2179.PointLoad':
        '''PointLoad: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2179.PointLoad.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to PointLoad. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_power_load(self) -> '_2180.PowerLoad':
        '''PowerLoad: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2180.PowerLoad.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to PowerLoad. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_unbalanced_mass(self) -> '_2185.UnbalancedMass':
        '''UnbalancedMass: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2185.UnbalancedMass.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to UnbalancedMass. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_virtual_component(self) -> '_2187.VirtualComponent':
        '''VirtualComponent: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2187.VirtualComponent.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to VirtualComponent. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_shaft(self) -> '_2190.Shaft':
        '''Shaft: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2190.Shaft.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to Shaft. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_agma_gleason_conical_gear(self) -> '_2220.AGMAGleasonConicalGear':
        '''AGMAGleasonConicalGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2220.AGMAGleasonConicalGear.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to AGMAGleasonConicalGear. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_bevel_differential_gear(self) -> '_2222.BevelDifferentialGear':
        '''BevelDifferentialGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2222.BevelDifferentialGear.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to BevelDifferentialGear. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_bevel_differential_planet_gear(self) -> '_2224.BevelDifferentialPlanetGear':
        '''BevelDifferentialPlanetGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2224.BevelDifferentialPlanetGear.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to BevelDifferentialPlanetGear. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_bevel_differential_sun_gear(self) -> '_2225.BevelDifferentialSunGear':
        '''BevelDifferentialSunGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2225.BevelDifferentialSunGear.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to BevelDifferentialSunGear. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_bevel_gear(self) -> '_2226.BevelGear':
        '''BevelGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2226.BevelGear.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to BevelGear. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_concept_gear(self) -> '_2228.ConceptGear':
        '''ConceptGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2228.ConceptGear.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to ConceptGear. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_conical_gear(self) -> '_2230.ConicalGear':
        '''ConicalGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2230.ConicalGear.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to ConicalGear. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_cylindrical_gear(self) -> '_2232.CylindricalGear':
        '''CylindricalGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2232.CylindricalGear.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to CylindricalGear. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_cylindrical_planet_gear(self) -> '_2234.CylindricalPlanetGear':
        '''CylindricalPlanetGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2234.CylindricalPlanetGear.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to CylindricalPlanetGear. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_face_gear(self) -> '_2235.FaceGear':
        '''FaceGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2235.FaceGear.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to FaceGear. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_gear(self) -> '_2237.Gear':
        '''Gear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2237.Gear.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to Gear. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_hypoid_gear(self) -> '_2241.HypoidGear':
        '''HypoidGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2241.HypoidGear.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to HypoidGear. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_klingelnberg_cyclo_palloid_conical_gear(self) -> '_2243.KlingelnbergCycloPalloidConicalGear':
        '''KlingelnbergCycloPalloidConicalGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2243.KlingelnbergCycloPalloidConicalGear.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to KlingelnbergCycloPalloidConicalGear. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_klingelnberg_cyclo_palloid_hypoid_gear(self) -> '_2245.KlingelnbergCycloPalloidHypoidGear':
        '''KlingelnbergCycloPalloidHypoidGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2245.KlingelnbergCycloPalloidHypoidGear.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to KlingelnbergCycloPalloidHypoidGear. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear(self) -> '_2247.KlingelnbergCycloPalloidSpiralBevelGear':
        '''KlingelnbergCycloPalloidSpiralBevelGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2247.KlingelnbergCycloPalloidSpiralBevelGear.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to KlingelnbergCycloPalloidSpiralBevelGear. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_spiral_bevel_gear(self) -> '_2250.SpiralBevelGear':
        '''SpiralBevelGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2250.SpiralBevelGear.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to SpiralBevelGear. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_straight_bevel_diff_gear(self) -> '_2252.StraightBevelDiffGear':
        '''StraightBevelDiffGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2252.StraightBevelDiffGear.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to StraightBevelDiffGear. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_straight_bevel_gear(self) -> '_2254.StraightBevelGear':
        '''StraightBevelGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2254.StraightBevelGear.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to StraightBevelGear. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_straight_bevel_planet_gear(self) -> '_2256.StraightBevelPlanetGear':
        '''StraightBevelPlanetGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2256.StraightBevelPlanetGear.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to StraightBevelPlanetGear. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_straight_bevel_sun_gear(self) -> '_2257.StraightBevelSunGear':
        '''StraightBevelSunGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2257.StraightBevelSunGear.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to StraightBevelSunGear. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_worm_gear(self) -> '_2258.WormGear':
        '''WormGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2258.WormGear.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to WormGear. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_zerol_bevel_gear(self) -> '_2260.ZerolBevelGear':
        '''ZerolBevelGear: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2260.ZerolBevelGear.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to ZerolBevelGear. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_cycloidal_disc(self) -> '_2276.CycloidalDisc':
        '''CycloidalDisc: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2276.CycloidalDisc.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to CycloidalDisc. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_ring_pins(self) -> '_2277.RingPins':
        '''RingPins: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2277.RingPins.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to RingPins. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_clutch_half(self) -> '_2286.ClutchHalf':
        '''ClutchHalf: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2286.ClutchHalf.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to ClutchHalf. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_concept_coupling_half(self) -> '_2289.ConceptCouplingHalf':
        '''ConceptCouplingHalf: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2289.ConceptCouplingHalf.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to ConceptCouplingHalf. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_coupling_half(self) -> '_2291.CouplingHalf':
        '''CouplingHalf: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2291.CouplingHalf.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to CouplingHalf. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_cvt_pulley(self) -> '_2294.CVTPulley':
        '''CVTPulley: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2294.CVTPulley.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to CVTPulley. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_part_to_part_shear_coupling_half(self) -> '_2296.PartToPartShearCouplingHalf':
        '''PartToPartShearCouplingHalf: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2296.PartToPartShearCouplingHalf.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to PartToPartShearCouplingHalf. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_pulley(self) -> '_2297.Pulley':
        '''Pulley: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2297.Pulley.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to Pulley. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_rolling_ring(self) -> '_2303.RollingRing':
        '''RollingRing: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2303.RollingRing.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to RollingRing. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_shaft_hub_connection(self) -> '_2305.ShaftHubConnection':
        '''ShaftHubConnection: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2305.ShaftHubConnection.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to ShaftHubConnection. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_spring_damper_half(self) -> '_2308.SpringDamperHalf':
        '''SpringDamperHalf: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2308.SpringDamperHalf.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to SpringDamperHalf. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_synchroniser_half(self) -> '_2311.SynchroniserHalf':
        '''SynchroniserHalf: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2311.SynchroniserHalf.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to SynchroniserHalf. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_synchroniser_part(self) -> '_2312.SynchroniserPart':
        '''SynchroniserPart: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2312.SynchroniserPart.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to SynchroniserPart. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_synchroniser_sleeve(self) -> '_2313.SynchroniserSleeve':
        '''SynchroniserSleeve: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2313.SynchroniserSleeve.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to SynchroniserSleeve. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_torque_converter_pump(self) -> '_2315.TorqueConverterPump':
        '''TorqueConverterPump: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2315.TorqueConverterPump.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to TorqueConverterPump. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    @property
    def owner_b_of_type_torque_converter_turbine(self) -> '_2317.TorqueConverterTurbine':
        '''TorqueConverterTurbine: 'OwnerB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2317.TorqueConverterTurbine.TYPE not in self.wrapped.OwnerB.__class__.__mro__:
            raise CastException('Failed to cast owner_b to TorqueConverterTurbine. Expected: {}.'.format(self.wrapped.OwnerB.__class__.__qualname__))

        return constructor.new_override(self.wrapped.OwnerB.__class__)(self.wrapped.OwnerB) if self.wrapped.OwnerB else None

    def socket_for(self, component: '_2153.Component') -> '_2005.Socket':
        ''' 'SocketFor' is the original name of this method.

        Args:
            component (mastapy.system_model.part_model.Component)

        Returns:
            mastapy.system_model.connections_and_sockets.Socket
        '''

        method_result = self.wrapped.SocketFor(component.wrapped if component else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def other_owner(self, component: '_2153.Component') -> '_2153.Component':
        ''' 'OtherOwner' is the original name of this method.

        Args:
            component (mastapy.system_model.part_model.Component)

        Returns:
            mastapy.system_model.part_model.Component
        '''

        method_result = self.wrapped.OtherOwner(component.wrapped if component else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def other_socket_for_component(self, component: '_2153.Component') -> '_2005.Socket':
        ''' 'OtherSocket' is the original name of this method.

        Args:
            component (mastapy.system_model.part_model.Component)

        Returns:
            mastapy.system_model.connections_and_sockets.Socket
        '''

        method_result = self.wrapped.OtherSocket.Overloads[_COMPONENT](component.wrapped if component else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

    def other_socket(self, socket: '_2005.Socket') -> '_2005.Socket':
        ''' 'OtherSocket' is the original name of this method.

        Args:
            socket (mastapy.system_model.connections_and_sockets.Socket)

        Returns:
            mastapy.system_model.connections_and_sockets.Socket
        '''

        method_result = self.wrapped.OtherSocket.Overloads[_SOCKET](socket.wrapped if socket else None)
        return constructor.new_override(method_result.__class__)(method_result) if method_result else None

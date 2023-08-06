'''_739.py

ConicalMeshMicroGeometryConfigBase
'''


from mastapy.gears.manufacturing.bevel import (
    _730, _728, _729, _740,
    _741, _746
)
from mastapy._internal import constructor
from mastapy._internal.cast_exception import CastException
from mastapy.gears.gear_designs.conical import _1084
from mastapy.gears.gear_designs.zerol_bevel import _891
from mastapy.gears.gear_designs.straight_bevel_diff import _900
from mastapy.gears.gear_designs.straight_bevel import _904
from mastapy.gears.gear_designs.spiral_bevel import _908
from mastapy.gears.gear_designs.klingelnberg_spiral_bevel import _912
from mastapy.gears.gear_designs.klingelnberg_hypoid import _916
from mastapy.gears.gear_designs.klingelnberg_conical import _920
from mastapy.gears.gear_designs.hypoid import _924
from mastapy.gears.gear_designs.bevel import _1110
from mastapy.gears.gear_designs.agma_gleason_conical import _1123
from mastapy.gears.analysis import _1151
from mastapy._internal.python_net import python_net_import

_CONICAL_MESH_MICRO_GEOMETRY_CONFIG_BASE = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Bevel', 'ConicalMeshMicroGeometryConfigBase')


__docformat__ = 'restructuredtext en'
__all__ = ('ConicalMeshMicroGeometryConfigBase',)


class ConicalMeshMicroGeometryConfigBase(_1151.GearMeshImplementationDetail):
    '''ConicalMeshMicroGeometryConfigBase

    This is a mastapy class.
    '''

    TYPE = _CONICAL_MESH_MICRO_GEOMETRY_CONFIG_BASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConicalMeshMicroGeometryConfigBase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def wheel_config(self) -> '_730.ConicalGearMicroGeometryConfigBase':
        '''ConicalGearMicroGeometryConfigBase: 'WheelConfig' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _730.ConicalGearMicroGeometryConfigBase.TYPE not in self.wrapped.WheelConfig.__class__.__mro__:
            raise CastException('Failed to cast wheel_config to ConicalGearMicroGeometryConfigBase. Expected: {}.'.format(self.wrapped.WheelConfig.__class__.__qualname__))

        return constructor.new_override(self.wrapped.WheelConfig.__class__)(self.wrapped.WheelConfig) if self.wrapped.WheelConfig else None

    @property
    def wheel_config_of_type_conical_gear_manufacturing_config(self) -> '_728.ConicalGearManufacturingConfig':
        '''ConicalGearManufacturingConfig: 'WheelConfig' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _728.ConicalGearManufacturingConfig.TYPE not in self.wrapped.WheelConfig.__class__.__mro__:
            raise CastException('Failed to cast wheel_config to ConicalGearManufacturingConfig. Expected: {}.'.format(self.wrapped.WheelConfig.__class__.__qualname__))

        return constructor.new_override(self.wrapped.WheelConfig.__class__)(self.wrapped.WheelConfig) if self.wrapped.WheelConfig else None

    @property
    def wheel_config_of_type_conical_gear_micro_geometry_config(self) -> '_729.ConicalGearMicroGeometryConfig':
        '''ConicalGearMicroGeometryConfig: 'WheelConfig' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _729.ConicalGearMicroGeometryConfig.TYPE not in self.wrapped.WheelConfig.__class__.__mro__:
            raise CastException('Failed to cast wheel_config to ConicalGearMicroGeometryConfig. Expected: {}.'.format(self.wrapped.WheelConfig.__class__.__qualname__))

        return constructor.new_override(self.wrapped.WheelConfig.__class__)(self.wrapped.WheelConfig) if self.wrapped.WheelConfig else None

    @property
    def wheel_config_of_type_conical_pinion_manufacturing_config(self) -> '_740.ConicalPinionManufacturingConfig':
        '''ConicalPinionManufacturingConfig: 'WheelConfig' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _740.ConicalPinionManufacturingConfig.TYPE not in self.wrapped.WheelConfig.__class__.__mro__:
            raise CastException('Failed to cast wheel_config to ConicalPinionManufacturingConfig. Expected: {}.'.format(self.wrapped.WheelConfig.__class__.__qualname__))

        return constructor.new_override(self.wrapped.WheelConfig.__class__)(self.wrapped.WheelConfig) if self.wrapped.WheelConfig else None

    @property
    def wheel_config_of_type_conical_pinion_micro_geometry_config(self) -> '_741.ConicalPinionMicroGeometryConfig':
        '''ConicalPinionMicroGeometryConfig: 'WheelConfig' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _741.ConicalPinionMicroGeometryConfig.TYPE not in self.wrapped.WheelConfig.__class__.__mro__:
            raise CastException('Failed to cast wheel_config to ConicalPinionMicroGeometryConfig. Expected: {}.'.format(self.wrapped.WheelConfig.__class__.__qualname__))

        return constructor.new_override(self.wrapped.WheelConfig.__class__)(self.wrapped.WheelConfig) if self.wrapped.WheelConfig else None

    @property
    def wheel_config_of_type_conical_wheel_manufacturing_config(self) -> '_746.ConicalWheelManufacturingConfig':
        '''ConicalWheelManufacturingConfig: 'WheelConfig' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _746.ConicalWheelManufacturingConfig.TYPE not in self.wrapped.WheelConfig.__class__.__mro__:
            raise CastException('Failed to cast wheel_config to ConicalWheelManufacturingConfig. Expected: {}.'.format(self.wrapped.WheelConfig.__class__.__qualname__))

        return constructor.new_override(self.wrapped.WheelConfig.__class__)(self.wrapped.WheelConfig) if self.wrapped.WheelConfig else None

    @property
    def mesh(self) -> '_1084.ConicalGearMeshDesign':
        '''ConicalGearMeshDesign: 'Mesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1084.ConicalGearMeshDesign.TYPE not in self.wrapped.Mesh.__class__.__mro__:
            raise CastException('Failed to cast mesh to ConicalGearMeshDesign. Expected: {}.'.format(self.wrapped.Mesh.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Mesh.__class__)(self.wrapped.Mesh) if self.wrapped.Mesh else None

    @property
    def mesh_of_type_zerol_bevel_gear_mesh_design(self) -> '_891.ZerolBevelGearMeshDesign':
        '''ZerolBevelGearMeshDesign: 'Mesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _891.ZerolBevelGearMeshDesign.TYPE not in self.wrapped.Mesh.__class__.__mro__:
            raise CastException('Failed to cast mesh to ZerolBevelGearMeshDesign. Expected: {}.'.format(self.wrapped.Mesh.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Mesh.__class__)(self.wrapped.Mesh) if self.wrapped.Mesh else None

    @property
    def mesh_of_type_straight_bevel_diff_gear_mesh_design(self) -> '_900.StraightBevelDiffGearMeshDesign':
        '''StraightBevelDiffGearMeshDesign: 'Mesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _900.StraightBevelDiffGearMeshDesign.TYPE not in self.wrapped.Mesh.__class__.__mro__:
            raise CastException('Failed to cast mesh to StraightBevelDiffGearMeshDesign. Expected: {}.'.format(self.wrapped.Mesh.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Mesh.__class__)(self.wrapped.Mesh) if self.wrapped.Mesh else None

    @property
    def mesh_of_type_straight_bevel_gear_mesh_design(self) -> '_904.StraightBevelGearMeshDesign':
        '''StraightBevelGearMeshDesign: 'Mesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _904.StraightBevelGearMeshDesign.TYPE not in self.wrapped.Mesh.__class__.__mro__:
            raise CastException('Failed to cast mesh to StraightBevelGearMeshDesign. Expected: {}.'.format(self.wrapped.Mesh.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Mesh.__class__)(self.wrapped.Mesh) if self.wrapped.Mesh else None

    @property
    def mesh_of_type_spiral_bevel_gear_mesh_design(self) -> '_908.SpiralBevelGearMeshDesign':
        '''SpiralBevelGearMeshDesign: 'Mesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _908.SpiralBevelGearMeshDesign.TYPE not in self.wrapped.Mesh.__class__.__mro__:
            raise CastException('Failed to cast mesh to SpiralBevelGearMeshDesign. Expected: {}.'.format(self.wrapped.Mesh.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Mesh.__class__)(self.wrapped.Mesh) if self.wrapped.Mesh else None

    @property
    def mesh_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_design(self) -> '_912.KlingelnbergCycloPalloidSpiralBevelGearMeshDesign':
        '''KlingelnbergCycloPalloidSpiralBevelGearMeshDesign: 'Mesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _912.KlingelnbergCycloPalloidSpiralBevelGearMeshDesign.TYPE not in self.wrapped.Mesh.__class__.__mro__:
            raise CastException('Failed to cast mesh to KlingelnbergCycloPalloidSpiralBevelGearMeshDesign. Expected: {}.'.format(self.wrapped.Mesh.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Mesh.__class__)(self.wrapped.Mesh) if self.wrapped.Mesh else None

    @property
    def mesh_of_type_klingelnberg_cyclo_palloid_hypoid_gear_mesh_design(self) -> '_916.KlingelnbergCycloPalloidHypoidGearMeshDesign':
        '''KlingelnbergCycloPalloidHypoidGearMeshDesign: 'Mesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _916.KlingelnbergCycloPalloidHypoidGearMeshDesign.TYPE not in self.wrapped.Mesh.__class__.__mro__:
            raise CastException('Failed to cast mesh to KlingelnbergCycloPalloidHypoidGearMeshDesign. Expected: {}.'.format(self.wrapped.Mesh.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Mesh.__class__)(self.wrapped.Mesh) if self.wrapped.Mesh else None

    @property
    def mesh_of_type_klingelnberg_conical_gear_mesh_design(self) -> '_920.KlingelnbergConicalGearMeshDesign':
        '''KlingelnbergConicalGearMeshDesign: 'Mesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _920.KlingelnbergConicalGearMeshDesign.TYPE not in self.wrapped.Mesh.__class__.__mro__:
            raise CastException('Failed to cast mesh to KlingelnbergConicalGearMeshDesign. Expected: {}.'.format(self.wrapped.Mesh.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Mesh.__class__)(self.wrapped.Mesh) if self.wrapped.Mesh else None

    @property
    def mesh_of_type_hypoid_gear_mesh_design(self) -> '_924.HypoidGearMeshDesign':
        '''HypoidGearMeshDesign: 'Mesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _924.HypoidGearMeshDesign.TYPE not in self.wrapped.Mesh.__class__.__mro__:
            raise CastException('Failed to cast mesh to HypoidGearMeshDesign. Expected: {}.'.format(self.wrapped.Mesh.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Mesh.__class__)(self.wrapped.Mesh) if self.wrapped.Mesh else None

    @property
    def mesh_of_type_bevel_gear_mesh_design(self) -> '_1110.BevelGearMeshDesign':
        '''BevelGearMeshDesign: 'Mesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1110.BevelGearMeshDesign.TYPE not in self.wrapped.Mesh.__class__.__mro__:
            raise CastException('Failed to cast mesh to BevelGearMeshDesign. Expected: {}.'.format(self.wrapped.Mesh.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Mesh.__class__)(self.wrapped.Mesh) if self.wrapped.Mesh else None

    @property
    def mesh_of_type_agma_gleason_conical_gear_mesh_design(self) -> '_1123.AGMAGleasonConicalGearMeshDesign':
        '''AGMAGleasonConicalGearMeshDesign: 'Mesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1123.AGMAGleasonConicalGearMeshDesign.TYPE not in self.wrapped.Mesh.__class__.__mro__:
            raise CastException('Failed to cast mesh to AGMAGleasonConicalGearMeshDesign. Expected: {}.'.format(self.wrapped.Mesh.__class__.__qualname__))

        return constructor.new_override(self.wrapped.Mesh.__class__)(self.wrapped.Mesh) if self.wrapped.Mesh else None

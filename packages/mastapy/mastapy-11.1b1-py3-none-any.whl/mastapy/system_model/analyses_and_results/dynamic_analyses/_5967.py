'''_5967.py

AssemblyDynamicAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2143, _2182
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.static_loads import _6500, _6633
from mastapy.system_model.analyses_and_results.dynamic_analyses import (
    _5968, _5970, _5973, _5979,
    _5980, _5982, _5987, _5991,
    _6001, _6003, _6005, _6009,
    _6016, _6017, _6018, _6025,
    _6032, _6035, _6036, _6037,
    _6039, _6042, _6046, _6047,
    _6048, _6057, _6050, _6052,
    _6056, _6062, _6064, _6068,
    _6071, _6074, _6079, _6082,
    _6086, _6089, _5960
)
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses', 'AssemblyDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblyDynamicAnalysis',)


class AssemblyDynamicAnalysis(_5960.AbstractAssemblyDynamicAnalysis):
    '''AssemblyDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AssemblyDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2143.Assembly':
        '''Assembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2143.Assembly.TYPE not in self.wrapped.AssemblyDesign.__class__.__mro__:
            raise CastException('Failed to cast assembly_design to Assembly. Expected: {}.'.format(self.wrapped.AssemblyDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.AssemblyDesign.__class__)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6500.AssemblyLoadCase':
        '''AssemblyLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _6500.AssemblyLoadCase.TYPE not in self.wrapped.AssemblyLoadCase.__class__.__mro__:
            raise CastException('Failed to cast assembly_load_case to AssemblyLoadCase. Expected: {}.'.format(self.wrapped.AssemblyLoadCase.__class__.__qualname__))

        return constructor.new_override(self.wrapped.AssemblyLoadCase.__class__)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def bearings(self) -> 'List[_5968.BearingDynamicAnalysis]':
        '''List[BearingDynamicAnalysis]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_5968.BearingDynamicAnalysis))
        return value

    @property
    def belt_drives(self) -> 'List[_5970.BeltDriveDynamicAnalysis]':
        '''List[BeltDriveDynamicAnalysis]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeltDrives, constructor.new(_5970.BeltDriveDynamicAnalysis))
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_5973.BevelDifferentialGearSetDynamicAnalysis]':
        '''List[BevelDifferentialGearSetDynamicAnalysis]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearSets, constructor.new(_5973.BevelDifferentialGearSetDynamicAnalysis))
        return value

    @property
    def bolts(self) -> 'List[_5979.BoltDynamicAnalysis]':
        '''List[BoltDynamicAnalysis]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bolts, constructor.new(_5979.BoltDynamicAnalysis))
        return value

    @property
    def bolted_joints(self) -> 'List[_5980.BoltedJointDynamicAnalysis]':
        '''List[BoltedJointDynamicAnalysis]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_5980.BoltedJointDynamicAnalysis))
        return value

    @property
    def clutches(self) -> 'List[_5982.ClutchDynamicAnalysis]':
        '''List[ClutchDynamicAnalysis]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Clutches, constructor.new(_5982.ClutchDynamicAnalysis))
        return value

    @property
    def concept_couplings(self) -> 'List[_5987.ConceptCouplingDynamicAnalysis]':
        '''List[ConceptCouplingDynamicAnalysis]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptCouplings, constructor.new(_5987.ConceptCouplingDynamicAnalysis))
        return value

    @property
    def concept_gear_sets(self) -> 'List[_5991.ConceptGearSetDynamicAnalysis]':
        '''List[ConceptGearSetDynamicAnalysis]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearSets, constructor.new(_5991.ConceptGearSetDynamicAnalysis))
        return value

    @property
    def cv_ts(self) -> 'List[_6001.CVTDynamicAnalysis]':
        '''List[CVTDynamicAnalysis]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CVTs, constructor.new(_6001.CVTDynamicAnalysis))
        return value

    @property
    def cycloidal_assemblies(self) -> 'List[_6003.CycloidalAssemblyDynamicAnalysis]':
        '''List[CycloidalAssemblyDynamicAnalysis]: 'CycloidalAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CycloidalAssemblies, constructor.new(_6003.CycloidalAssemblyDynamicAnalysis))
        return value

    @property
    def cycloidal_discs(self) -> 'List[_6005.CycloidalDiscDynamicAnalysis]':
        '''List[CycloidalDiscDynamicAnalysis]: 'CycloidalDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CycloidalDiscs, constructor.new(_6005.CycloidalDiscDynamicAnalysis))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_6009.CylindricalGearSetDynamicAnalysis]':
        '''List[CylindricalGearSetDynamicAnalysis]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_6009.CylindricalGearSetDynamicAnalysis))
        return value

    @property
    def face_gear_sets(self) -> 'List[_6016.FaceGearSetDynamicAnalysis]':
        '''List[FaceGearSetDynamicAnalysis]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearSets, constructor.new(_6016.FaceGearSetDynamicAnalysis))
        return value

    @property
    def fe_parts(self) -> 'List[_6017.FEPartDynamicAnalysis]':
        '''List[FEPartDynamicAnalysis]: 'FEParts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FEParts, constructor.new(_6017.FEPartDynamicAnalysis))
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_6018.FlexiblePinAssemblyDynamicAnalysis]':
        '''List[FlexiblePinAssemblyDynamicAnalysis]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FlexiblePinAssemblies, constructor.new(_6018.FlexiblePinAssemblyDynamicAnalysis))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_6025.HypoidGearSetDynamicAnalysis]':
        '''List[HypoidGearSetDynamicAnalysis]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_6025.HypoidGearSetDynamicAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_6032.KlingelnbergCycloPalloidHypoidGearSetDynamicAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetDynamicAnalysis]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearSets, constructor.new(_6032.KlingelnbergCycloPalloidHypoidGearSetDynamicAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_6035.KlingelnbergCycloPalloidSpiralBevelGearSetDynamicAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetDynamicAnalysis]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets, constructor.new(_6035.KlingelnbergCycloPalloidSpiralBevelGearSetDynamicAnalysis))
        return value

    @property
    def mass_discs(self) -> 'List[_6036.MassDiscDynamicAnalysis]':
        '''List[MassDiscDynamicAnalysis]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassDiscs, constructor.new(_6036.MassDiscDynamicAnalysis))
        return value

    @property
    def measurement_components(self) -> 'List[_6037.MeasurementComponentDynamicAnalysis]':
        '''List[MeasurementComponentDynamicAnalysis]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeasurementComponents, constructor.new(_6037.MeasurementComponentDynamicAnalysis))
        return value

    @property
    def oil_seals(self) -> 'List[_6039.OilSealDynamicAnalysis]':
        '''List[OilSealDynamicAnalysis]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_6039.OilSealDynamicAnalysis))
        return value

    @property
    def part_to_part_shear_couplings(self) -> 'List[_6042.PartToPartShearCouplingDynamicAnalysis]':
        '''List[PartToPartShearCouplingDynamicAnalysis]: 'PartToPartShearCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PartToPartShearCouplings, constructor.new(_6042.PartToPartShearCouplingDynamicAnalysis))
        return value

    @property
    def planet_carriers(self) -> 'List[_6046.PlanetCarrierDynamicAnalysis]':
        '''List[PlanetCarrierDynamicAnalysis]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetCarriers, constructor.new(_6046.PlanetCarrierDynamicAnalysis))
        return value

    @property
    def point_loads(self) -> 'List[_6047.PointLoadDynamicAnalysis]':
        '''List[PointLoadDynamicAnalysis]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_6047.PointLoadDynamicAnalysis))
        return value

    @property
    def power_loads(self) -> 'List[_6048.PowerLoadDynamicAnalysis]':
        '''List[PowerLoadDynamicAnalysis]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_6048.PowerLoadDynamicAnalysis))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_6057.ShaftHubConnectionDynamicAnalysis]':
        '''List[ShaftHubConnectionDynamicAnalysis]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_6057.ShaftHubConnectionDynamicAnalysis))
        return value

    @property
    def ring_pins(self) -> 'List[_6050.RingPinsDynamicAnalysis]':
        '''List[RingPinsDynamicAnalysis]: 'RingPins' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RingPins, constructor.new(_6050.RingPinsDynamicAnalysis))
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_6052.RollingRingAssemblyDynamicAnalysis]':
        '''List[RollingRingAssemblyDynamicAnalysis]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingRingAssemblies, constructor.new(_6052.RollingRingAssemblyDynamicAnalysis))
        return value

    @property
    def shafts(self) -> 'List[_6056.ShaftDynamicAnalysis]':
        '''List[ShaftDynamicAnalysis]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_6056.ShaftDynamicAnalysis))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_6062.SpiralBevelGearSetDynamicAnalysis]':
        '''List[SpiralBevelGearSetDynamicAnalysis]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_6062.SpiralBevelGearSetDynamicAnalysis))
        return value

    @property
    def spring_dampers(self) -> 'List[_6064.SpringDamperDynamicAnalysis]':
        '''List[SpringDamperDynamicAnalysis]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDampers, constructor.new(_6064.SpringDamperDynamicAnalysis))
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_6068.StraightBevelDiffGearSetDynamicAnalysis]':
        '''List[StraightBevelDiffGearSetDynamicAnalysis]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearSets, constructor.new(_6068.StraightBevelDiffGearSetDynamicAnalysis))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_6071.StraightBevelGearSetDynamicAnalysis]':
        '''List[StraightBevelGearSetDynamicAnalysis]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_6071.StraightBevelGearSetDynamicAnalysis))
        return value

    @property
    def synchronisers(self) -> 'List[_6074.SynchroniserDynamicAnalysis]':
        '''List[SynchroniserDynamicAnalysis]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Synchronisers, constructor.new(_6074.SynchroniserDynamicAnalysis))
        return value

    @property
    def torque_converters(self) -> 'List[_6079.TorqueConverterDynamicAnalysis]':
        '''List[TorqueConverterDynamicAnalysis]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TorqueConverters, constructor.new(_6079.TorqueConverterDynamicAnalysis))
        return value

    @property
    def unbalanced_masses(self) -> 'List[_6082.UnbalancedMassDynamicAnalysis]':
        '''List[UnbalancedMassDynamicAnalysis]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnbalancedMasses, constructor.new(_6082.UnbalancedMassDynamicAnalysis))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_6086.WormGearSetDynamicAnalysis]':
        '''List[WormGearSetDynamicAnalysis]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_6086.WormGearSetDynamicAnalysis))
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_6089.ZerolBevelGearSetDynamicAnalysis]':
        '''List[ZerolBevelGearSetDynamicAnalysis]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearSets, constructor.new(_6089.ZerolBevelGearSetDynamicAnalysis))
        return value

'''_5077.py

AssemblyMultibodyDynamicsAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2143, _2182
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.static_loads import _6500, _6633
from mastapy.system_model.analyses_and_results.mbd_analyses import (
    _5078, _5081, _5084, _5091,
    _5090, _5094, _5100, _5103,
    _5113, _5115, _5117, _5121,
    _5127, _5128, _5129, _5137,
    _5148, _5151, _5152, _5156,
    _5158, _5162, _5165, _5166,
    _5167, _5177, _5169, _5171,
    _5178, _5184, _5187, _5190,
    _5193, _5197, _5202, _5206,
    _5211, _5214, _5142, _5071,
    _5133, _5069
)
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'AssemblyMultibodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblyMultibodyDynamicsAnalysis',)


class AssemblyMultibodyDynamicsAnalysis(_5069.AbstractAssemblyMultibodyDynamicsAnalysis):
    '''AssemblyMultibodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY_MULTIBODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AssemblyMultibodyDynamicsAnalysis.TYPE'):
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
    def bearings(self) -> 'List[_5078.BearingMultibodyDynamicsAnalysis]':
        '''List[BearingMultibodyDynamicsAnalysis]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_5078.BearingMultibodyDynamicsAnalysis))
        return value

    @property
    def belt_drives(self) -> 'List[_5081.BeltDriveMultibodyDynamicsAnalysis]':
        '''List[BeltDriveMultibodyDynamicsAnalysis]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeltDrives, constructor.new(_5081.BeltDriveMultibodyDynamicsAnalysis))
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_5084.BevelDifferentialGearSetMultibodyDynamicsAnalysis]':
        '''List[BevelDifferentialGearSetMultibodyDynamicsAnalysis]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearSets, constructor.new(_5084.BevelDifferentialGearSetMultibodyDynamicsAnalysis))
        return value

    @property
    def bolts(self) -> 'List[_5091.BoltMultibodyDynamicsAnalysis]':
        '''List[BoltMultibodyDynamicsAnalysis]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bolts, constructor.new(_5091.BoltMultibodyDynamicsAnalysis))
        return value

    @property
    def bolted_joints(self) -> 'List[_5090.BoltedJointMultibodyDynamicsAnalysis]':
        '''List[BoltedJointMultibodyDynamicsAnalysis]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_5090.BoltedJointMultibodyDynamicsAnalysis))
        return value

    @property
    def clutches(self) -> 'List[_5094.ClutchMultibodyDynamicsAnalysis]':
        '''List[ClutchMultibodyDynamicsAnalysis]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Clutches, constructor.new(_5094.ClutchMultibodyDynamicsAnalysis))
        return value

    @property
    def concept_couplings(self) -> 'List[_5100.ConceptCouplingMultibodyDynamicsAnalysis]':
        '''List[ConceptCouplingMultibodyDynamicsAnalysis]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptCouplings, constructor.new(_5100.ConceptCouplingMultibodyDynamicsAnalysis))
        return value

    @property
    def concept_gear_sets(self) -> 'List[_5103.ConceptGearSetMultibodyDynamicsAnalysis]':
        '''List[ConceptGearSetMultibodyDynamicsAnalysis]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearSets, constructor.new(_5103.ConceptGearSetMultibodyDynamicsAnalysis))
        return value

    @property
    def cv_ts(self) -> 'List[_5113.CVTMultibodyDynamicsAnalysis]':
        '''List[CVTMultibodyDynamicsAnalysis]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CVTs, constructor.new(_5113.CVTMultibodyDynamicsAnalysis))
        return value

    @property
    def cycloidal_assemblies(self) -> 'List[_5115.CycloidalAssemblyMultibodyDynamicsAnalysis]':
        '''List[CycloidalAssemblyMultibodyDynamicsAnalysis]: 'CycloidalAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CycloidalAssemblies, constructor.new(_5115.CycloidalAssemblyMultibodyDynamicsAnalysis))
        return value

    @property
    def cycloidal_discs(self) -> 'List[_5117.CycloidalDiscMultibodyDynamicsAnalysis]':
        '''List[CycloidalDiscMultibodyDynamicsAnalysis]: 'CycloidalDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CycloidalDiscs, constructor.new(_5117.CycloidalDiscMultibodyDynamicsAnalysis))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_5121.CylindricalGearSetMultibodyDynamicsAnalysis]':
        '''List[CylindricalGearSetMultibodyDynamicsAnalysis]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_5121.CylindricalGearSetMultibodyDynamicsAnalysis))
        return value

    @property
    def face_gear_sets(self) -> 'List[_5127.FaceGearSetMultibodyDynamicsAnalysis]':
        '''List[FaceGearSetMultibodyDynamicsAnalysis]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearSets, constructor.new(_5127.FaceGearSetMultibodyDynamicsAnalysis))
        return value

    @property
    def fe_parts(self) -> 'List[_5128.FEPartMultibodyDynamicsAnalysis]':
        '''List[FEPartMultibodyDynamicsAnalysis]: 'FEParts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FEParts, constructor.new(_5128.FEPartMultibodyDynamicsAnalysis))
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_5129.FlexiblePinAssemblyMultibodyDynamicsAnalysis]':
        '''List[FlexiblePinAssemblyMultibodyDynamicsAnalysis]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FlexiblePinAssemblies, constructor.new(_5129.FlexiblePinAssemblyMultibodyDynamicsAnalysis))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_5137.HypoidGearSetMultibodyDynamicsAnalysis]':
        '''List[HypoidGearSetMultibodyDynamicsAnalysis]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_5137.HypoidGearSetMultibodyDynamicsAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_5148.KlingelnbergCycloPalloidHypoidGearSetMultibodyDynamicsAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetMultibodyDynamicsAnalysis]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearSets, constructor.new(_5148.KlingelnbergCycloPalloidHypoidGearSetMultibodyDynamicsAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_5151.KlingelnbergCycloPalloidSpiralBevelGearSetMultibodyDynamicsAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetMultibodyDynamicsAnalysis]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets, constructor.new(_5151.KlingelnbergCycloPalloidSpiralBevelGearSetMultibodyDynamicsAnalysis))
        return value

    @property
    def mass_discs(self) -> 'List[_5152.MassDiscMultibodyDynamicsAnalysis]':
        '''List[MassDiscMultibodyDynamicsAnalysis]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassDiscs, constructor.new(_5152.MassDiscMultibodyDynamicsAnalysis))
        return value

    @property
    def measurement_components(self) -> 'List[_5156.MeasurementComponentMultibodyDynamicsAnalysis]':
        '''List[MeasurementComponentMultibodyDynamicsAnalysis]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeasurementComponents, constructor.new(_5156.MeasurementComponentMultibodyDynamicsAnalysis))
        return value

    @property
    def oil_seals(self) -> 'List[_5158.OilSealMultibodyDynamicsAnalysis]':
        '''List[OilSealMultibodyDynamicsAnalysis]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_5158.OilSealMultibodyDynamicsAnalysis))
        return value

    @property
    def part_to_part_shear_couplings(self) -> 'List[_5162.PartToPartShearCouplingMultibodyDynamicsAnalysis]':
        '''List[PartToPartShearCouplingMultibodyDynamicsAnalysis]: 'PartToPartShearCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PartToPartShearCouplings, constructor.new(_5162.PartToPartShearCouplingMultibodyDynamicsAnalysis))
        return value

    @property
    def planet_carriers(self) -> 'List[_5165.PlanetCarrierMultibodyDynamicsAnalysis]':
        '''List[PlanetCarrierMultibodyDynamicsAnalysis]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetCarriers, constructor.new(_5165.PlanetCarrierMultibodyDynamicsAnalysis))
        return value

    @property
    def point_loads(self) -> 'List[_5166.PointLoadMultibodyDynamicsAnalysis]':
        '''List[PointLoadMultibodyDynamicsAnalysis]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_5166.PointLoadMultibodyDynamicsAnalysis))
        return value

    @property
    def power_loads(self) -> 'List[_5167.PowerLoadMultibodyDynamicsAnalysis]':
        '''List[PowerLoadMultibodyDynamicsAnalysis]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_5167.PowerLoadMultibodyDynamicsAnalysis))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_5177.ShaftHubConnectionMultibodyDynamicsAnalysis]':
        '''List[ShaftHubConnectionMultibodyDynamicsAnalysis]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_5177.ShaftHubConnectionMultibodyDynamicsAnalysis))
        return value

    @property
    def ring_pins(self) -> 'List[_5169.RingPinsMultibodyDynamicsAnalysis]':
        '''List[RingPinsMultibodyDynamicsAnalysis]: 'RingPins' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RingPins, constructor.new(_5169.RingPinsMultibodyDynamicsAnalysis))
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_5171.RollingRingAssemblyMultibodyDynamicsAnalysis]':
        '''List[RollingRingAssemblyMultibodyDynamicsAnalysis]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingRingAssemblies, constructor.new(_5171.RollingRingAssemblyMultibodyDynamicsAnalysis))
        return value

    @property
    def shafts(self) -> 'List[_5178.ShaftMultibodyDynamicsAnalysis]':
        '''List[ShaftMultibodyDynamicsAnalysis]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_5178.ShaftMultibodyDynamicsAnalysis))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_5184.SpiralBevelGearSetMultibodyDynamicsAnalysis]':
        '''List[SpiralBevelGearSetMultibodyDynamicsAnalysis]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_5184.SpiralBevelGearSetMultibodyDynamicsAnalysis))
        return value

    @property
    def spring_dampers(self) -> 'List[_5187.SpringDamperMultibodyDynamicsAnalysis]':
        '''List[SpringDamperMultibodyDynamicsAnalysis]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDampers, constructor.new(_5187.SpringDamperMultibodyDynamicsAnalysis))
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_5190.StraightBevelDiffGearSetMultibodyDynamicsAnalysis]':
        '''List[StraightBevelDiffGearSetMultibodyDynamicsAnalysis]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearSets, constructor.new(_5190.StraightBevelDiffGearSetMultibodyDynamicsAnalysis))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_5193.StraightBevelGearSetMultibodyDynamicsAnalysis]':
        '''List[StraightBevelGearSetMultibodyDynamicsAnalysis]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_5193.StraightBevelGearSetMultibodyDynamicsAnalysis))
        return value

    @property
    def synchronisers(self) -> 'List[_5197.SynchroniserMultibodyDynamicsAnalysis]':
        '''List[SynchroniserMultibodyDynamicsAnalysis]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Synchronisers, constructor.new(_5197.SynchroniserMultibodyDynamicsAnalysis))
        return value

    @property
    def torque_converters(self) -> 'List[_5202.TorqueConverterMultibodyDynamicsAnalysis]':
        '''List[TorqueConverterMultibodyDynamicsAnalysis]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TorqueConverters, constructor.new(_5202.TorqueConverterMultibodyDynamicsAnalysis))
        return value

    @property
    def unbalanced_masses(self) -> 'List[_5206.UnbalancedMassMultibodyDynamicsAnalysis]':
        '''List[UnbalancedMassMultibodyDynamicsAnalysis]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnbalancedMasses, constructor.new(_5206.UnbalancedMassMultibodyDynamicsAnalysis))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_5211.WormGearSetMultibodyDynamicsAnalysis]':
        '''List[WormGearSetMultibodyDynamicsAnalysis]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_5211.WormGearSetMultibodyDynamicsAnalysis))
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_5214.ZerolBevelGearSetMultibodyDynamicsAnalysis]':
        '''List[ZerolBevelGearSetMultibodyDynamicsAnalysis]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearSets, constructor.new(_5214.ZerolBevelGearSetMultibodyDynamicsAnalysis))
        return value

    @property
    def connections(self) -> 'List[_5142.InterMountableComponentConnectionMultibodyDynamicsAnalysis]':
        '''List[InterMountableComponentConnectionMultibodyDynamicsAnalysis]: 'Connections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Connections, constructor.new(_5142.InterMountableComponentConnectionMultibodyDynamicsAnalysis))
        return value

    @property
    def shafts_and_housings(self) -> 'List[_5071.AbstractShaftOrHousingMultibodyDynamicsAnalysis]':
        '''List[AbstractShaftOrHousingMultibodyDynamicsAnalysis]: 'ShaftsAndHousings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftsAndHousings, constructor.new(_5071.AbstractShaftOrHousingMultibodyDynamicsAnalysis))
        return value

    @property
    def gear_sets(self) -> 'List[_5133.GearSetMultibodyDynamicsAnalysis]':
        '''List[GearSetMultibodyDynamicsAnalysis]: 'GearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.GearSets, constructor.new(_5133.GearSetMultibodyDynamicsAnalysis))
        return value

'''_5377.py

AssemblyHarmonicAnalysisOfSingleExcitation
'''


from typing import List

from mastapy.system_model.part_model import _2143, _2182
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.static_loads import _6500, _6633
from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
    _5378, _5380, _5383, _5390,
    _5389, _5393, _5398, _5401,
    _5411, _5413, _5415, _5419,
    _5425, _5426, _5427, _5435,
    _5442, _5445, _5446, _5447,
    _5449, _5453, _5456, _5457,
    _5458, _5467, _5460, _5462,
    _5466, _5472, _5475, _5478,
    _5481, _5485, _5489, _5492,
    _5496, _5499, _5370
)
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalysesSingleExcitation', 'AssemblyHarmonicAnalysisOfSingleExcitation')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblyHarmonicAnalysisOfSingleExcitation',)


class AssemblyHarmonicAnalysisOfSingleExcitation(_5370.AbstractAssemblyHarmonicAnalysisOfSingleExcitation):
    '''AssemblyHarmonicAnalysisOfSingleExcitation

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AssemblyHarmonicAnalysisOfSingleExcitation.TYPE'):
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
    def bearings(self) -> 'List[_5378.BearingHarmonicAnalysisOfSingleExcitation]':
        '''List[BearingHarmonicAnalysisOfSingleExcitation]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_5378.BearingHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def belt_drives(self) -> 'List[_5380.BeltDriveHarmonicAnalysisOfSingleExcitation]':
        '''List[BeltDriveHarmonicAnalysisOfSingleExcitation]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeltDrives, constructor.new(_5380.BeltDriveHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_5383.BevelDifferentialGearSetHarmonicAnalysisOfSingleExcitation]':
        '''List[BevelDifferentialGearSetHarmonicAnalysisOfSingleExcitation]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearSets, constructor.new(_5383.BevelDifferentialGearSetHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def bolts(self) -> 'List[_5390.BoltHarmonicAnalysisOfSingleExcitation]':
        '''List[BoltHarmonicAnalysisOfSingleExcitation]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bolts, constructor.new(_5390.BoltHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def bolted_joints(self) -> 'List[_5389.BoltedJointHarmonicAnalysisOfSingleExcitation]':
        '''List[BoltedJointHarmonicAnalysisOfSingleExcitation]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_5389.BoltedJointHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def clutches(self) -> 'List[_5393.ClutchHarmonicAnalysisOfSingleExcitation]':
        '''List[ClutchHarmonicAnalysisOfSingleExcitation]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Clutches, constructor.new(_5393.ClutchHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def concept_couplings(self) -> 'List[_5398.ConceptCouplingHarmonicAnalysisOfSingleExcitation]':
        '''List[ConceptCouplingHarmonicAnalysisOfSingleExcitation]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptCouplings, constructor.new(_5398.ConceptCouplingHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def concept_gear_sets(self) -> 'List[_5401.ConceptGearSetHarmonicAnalysisOfSingleExcitation]':
        '''List[ConceptGearSetHarmonicAnalysisOfSingleExcitation]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearSets, constructor.new(_5401.ConceptGearSetHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def cv_ts(self) -> 'List[_5411.CVTHarmonicAnalysisOfSingleExcitation]':
        '''List[CVTHarmonicAnalysisOfSingleExcitation]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CVTs, constructor.new(_5411.CVTHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def cycloidal_assemblies(self) -> 'List[_5413.CycloidalAssemblyHarmonicAnalysisOfSingleExcitation]':
        '''List[CycloidalAssemblyHarmonicAnalysisOfSingleExcitation]: 'CycloidalAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CycloidalAssemblies, constructor.new(_5413.CycloidalAssemblyHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def cycloidal_discs(self) -> 'List[_5415.CycloidalDiscHarmonicAnalysisOfSingleExcitation]':
        '''List[CycloidalDiscHarmonicAnalysisOfSingleExcitation]: 'CycloidalDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CycloidalDiscs, constructor.new(_5415.CycloidalDiscHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_5419.CylindricalGearSetHarmonicAnalysisOfSingleExcitation]':
        '''List[CylindricalGearSetHarmonicAnalysisOfSingleExcitation]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_5419.CylindricalGearSetHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def face_gear_sets(self) -> 'List[_5425.FaceGearSetHarmonicAnalysisOfSingleExcitation]':
        '''List[FaceGearSetHarmonicAnalysisOfSingleExcitation]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearSets, constructor.new(_5425.FaceGearSetHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def fe_parts(self) -> 'List[_5426.FEPartHarmonicAnalysisOfSingleExcitation]':
        '''List[FEPartHarmonicAnalysisOfSingleExcitation]: 'FEParts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FEParts, constructor.new(_5426.FEPartHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_5427.FlexiblePinAssemblyHarmonicAnalysisOfSingleExcitation]':
        '''List[FlexiblePinAssemblyHarmonicAnalysisOfSingleExcitation]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FlexiblePinAssemblies, constructor.new(_5427.FlexiblePinAssemblyHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_5435.HypoidGearSetHarmonicAnalysisOfSingleExcitation]':
        '''List[HypoidGearSetHarmonicAnalysisOfSingleExcitation]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_5435.HypoidGearSetHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_5442.KlingelnbergCycloPalloidHypoidGearSetHarmonicAnalysisOfSingleExcitation]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetHarmonicAnalysisOfSingleExcitation]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearSets, constructor.new(_5442.KlingelnbergCycloPalloidHypoidGearSetHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_5445.KlingelnbergCycloPalloidSpiralBevelGearSetHarmonicAnalysisOfSingleExcitation]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetHarmonicAnalysisOfSingleExcitation]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets, constructor.new(_5445.KlingelnbergCycloPalloidSpiralBevelGearSetHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def mass_discs(self) -> 'List[_5446.MassDiscHarmonicAnalysisOfSingleExcitation]':
        '''List[MassDiscHarmonicAnalysisOfSingleExcitation]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassDiscs, constructor.new(_5446.MassDiscHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def measurement_components(self) -> 'List[_5447.MeasurementComponentHarmonicAnalysisOfSingleExcitation]':
        '''List[MeasurementComponentHarmonicAnalysisOfSingleExcitation]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeasurementComponents, constructor.new(_5447.MeasurementComponentHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def oil_seals(self) -> 'List[_5449.OilSealHarmonicAnalysisOfSingleExcitation]':
        '''List[OilSealHarmonicAnalysisOfSingleExcitation]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_5449.OilSealHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def part_to_part_shear_couplings(self) -> 'List[_5453.PartToPartShearCouplingHarmonicAnalysisOfSingleExcitation]':
        '''List[PartToPartShearCouplingHarmonicAnalysisOfSingleExcitation]: 'PartToPartShearCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PartToPartShearCouplings, constructor.new(_5453.PartToPartShearCouplingHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def planet_carriers(self) -> 'List[_5456.PlanetCarrierHarmonicAnalysisOfSingleExcitation]':
        '''List[PlanetCarrierHarmonicAnalysisOfSingleExcitation]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetCarriers, constructor.new(_5456.PlanetCarrierHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def point_loads(self) -> 'List[_5457.PointLoadHarmonicAnalysisOfSingleExcitation]':
        '''List[PointLoadHarmonicAnalysisOfSingleExcitation]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_5457.PointLoadHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def power_loads(self) -> 'List[_5458.PowerLoadHarmonicAnalysisOfSingleExcitation]':
        '''List[PowerLoadHarmonicAnalysisOfSingleExcitation]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_5458.PowerLoadHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_5467.ShaftHubConnectionHarmonicAnalysisOfSingleExcitation]':
        '''List[ShaftHubConnectionHarmonicAnalysisOfSingleExcitation]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_5467.ShaftHubConnectionHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def ring_pins(self) -> 'List[_5460.RingPinsHarmonicAnalysisOfSingleExcitation]':
        '''List[RingPinsHarmonicAnalysisOfSingleExcitation]: 'RingPins' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RingPins, constructor.new(_5460.RingPinsHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_5462.RollingRingAssemblyHarmonicAnalysisOfSingleExcitation]':
        '''List[RollingRingAssemblyHarmonicAnalysisOfSingleExcitation]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingRingAssemblies, constructor.new(_5462.RollingRingAssemblyHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def shafts(self) -> 'List[_5466.ShaftHarmonicAnalysisOfSingleExcitation]':
        '''List[ShaftHarmonicAnalysisOfSingleExcitation]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_5466.ShaftHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_5472.SpiralBevelGearSetHarmonicAnalysisOfSingleExcitation]':
        '''List[SpiralBevelGearSetHarmonicAnalysisOfSingleExcitation]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_5472.SpiralBevelGearSetHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def spring_dampers(self) -> 'List[_5475.SpringDamperHarmonicAnalysisOfSingleExcitation]':
        '''List[SpringDamperHarmonicAnalysisOfSingleExcitation]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDampers, constructor.new(_5475.SpringDamperHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_5478.StraightBevelDiffGearSetHarmonicAnalysisOfSingleExcitation]':
        '''List[StraightBevelDiffGearSetHarmonicAnalysisOfSingleExcitation]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearSets, constructor.new(_5478.StraightBevelDiffGearSetHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_5481.StraightBevelGearSetHarmonicAnalysisOfSingleExcitation]':
        '''List[StraightBevelGearSetHarmonicAnalysisOfSingleExcitation]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_5481.StraightBevelGearSetHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def synchronisers(self) -> 'List[_5485.SynchroniserHarmonicAnalysisOfSingleExcitation]':
        '''List[SynchroniserHarmonicAnalysisOfSingleExcitation]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Synchronisers, constructor.new(_5485.SynchroniserHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def torque_converters(self) -> 'List[_5489.TorqueConverterHarmonicAnalysisOfSingleExcitation]':
        '''List[TorqueConverterHarmonicAnalysisOfSingleExcitation]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TorqueConverters, constructor.new(_5489.TorqueConverterHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def unbalanced_masses(self) -> 'List[_5492.UnbalancedMassHarmonicAnalysisOfSingleExcitation]':
        '''List[UnbalancedMassHarmonicAnalysisOfSingleExcitation]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnbalancedMasses, constructor.new(_5492.UnbalancedMassHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_5496.WormGearSetHarmonicAnalysisOfSingleExcitation]':
        '''List[WormGearSetHarmonicAnalysisOfSingleExcitation]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_5496.WormGearSetHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_5499.ZerolBevelGearSetHarmonicAnalysisOfSingleExcitation]':
        '''List[ZerolBevelGearSetHarmonicAnalysisOfSingleExcitation]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearSets, constructor.new(_5499.ZerolBevelGearSetHarmonicAnalysisOfSingleExcitation))
        return value

'''_3210.py

AssemblySteadyStateSynchronousResponse
'''


from typing import List

from mastapy.system_model.part_model import _2143, _2182
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.static_loads import _6500, _6633
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import (
    _3211, _3213, _3215, _3223,
    _3222, _3226, _3231, _3233,
    _3245, _3246, _3249, _3251,
    _3258, _3260, _3261, _3267,
    _3274, _3277, _3279, _3280,
    _3282, _3286, _3289, _3290,
    _3291, _3299, _3293, _3295,
    _3300, _3304, _3308, _3313,
    _3316, _3323, _3326, _3328,
    _3331, _3334, _3203
)
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses', 'AssemblySteadyStateSynchronousResponse')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblySteadyStateSynchronousResponse',)


class AssemblySteadyStateSynchronousResponse(_3203.AbstractAssemblySteadyStateSynchronousResponse):
    '''AssemblySteadyStateSynchronousResponse

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY_STEADY_STATE_SYNCHRONOUS_RESPONSE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AssemblySteadyStateSynchronousResponse.TYPE'):
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
    def bearings(self) -> 'List[_3211.BearingSteadyStateSynchronousResponse]':
        '''List[BearingSteadyStateSynchronousResponse]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_3211.BearingSteadyStateSynchronousResponse))
        return value

    @property
    def belt_drives(self) -> 'List[_3213.BeltDriveSteadyStateSynchronousResponse]':
        '''List[BeltDriveSteadyStateSynchronousResponse]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeltDrives, constructor.new(_3213.BeltDriveSteadyStateSynchronousResponse))
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_3215.BevelDifferentialGearSetSteadyStateSynchronousResponse]':
        '''List[BevelDifferentialGearSetSteadyStateSynchronousResponse]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearSets, constructor.new(_3215.BevelDifferentialGearSetSteadyStateSynchronousResponse))
        return value

    @property
    def bolts(self) -> 'List[_3223.BoltSteadyStateSynchronousResponse]':
        '''List[BoltSteadyStateSynchronousResponse]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bolts, constructor.new(_3223.BoltSteadyStateSynchronousResponse))
        return value

    @property
    def bolted_joints(self) -> 'List[_3222.BoltedJointSteadyStateSynchronousResponse]':
        '''List[BoltedJointSteadyStateSynchronousResponse]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_3222.BoltedJointSteadyStateSynchronousResponse))
        return value

    @property
    def clutches(self) -> 'List[_3226.ClutchSteadyStateSynchronousResponse]':
        '''List[ClutchSteadyStateSynchronousResponse]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Clutches, constructor.new(_3226.ClutchSteadyStateSynchronousResponse))
        return value

    @property
    def concept_couplings(self) -> 'List[_3231.ConceptCouplingSteadyStateSynchronousResponse]':
        '''List[ConceptCouplingSteadyStateSynchronousResponse]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptCouplings, constructor.new(_3231.ConceptCouplingSteadyStateSynchronousResponse))
        return value

    @property
    def concept_gear_sets(self) -> 'List[_3233.ConceptGearSetSteadyStateSynchronousResponse]':
        '''List[ConceptGearSetSteadyStateSynchronousResponse]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearSets, constructor.new(_3233.ConceptGearSetSteadyStateSynchronousResponse))
        return value

    @property
    def cv_ts(self) -> 'List[_3245.CVTSteadyStateSynchronousResponse]':
        '''List[CVTSteadyStateSynchronousResponse]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CVTs, constructor.new(_3245.CVTSteadyStateSynchronousResponse))
        return value

    @property
    def cycloidal_assemblies(self) -> 'List[_3246.CycloidalAssemblySteadyStateSynchronousResponse]':
        '''List[CycloidalAssemblySteadyStateSynchronousResponse]: 'CycloidalAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CycloidalAssemblies, constructor.new(_3246.CycloidalAssemblySteadyStateSynchronousResponse))
        return value

    @property
    def cycloidal_discs(self) -> 'List[_3249.CycloidalDiscSteadyStateSynchronousResponse]':
        '''List[CycloidalDiscSteadyStateSynchronousResponse]: 'CycloidalDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CycloidalDiscs, constructor.new(_3249.CycloidalDiscSteadyStateSynchronousResponse))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_3251.CylindricalGearSetSteadyStateSynchronousResponse]':
        '''List[CylindricalGearSetSteadyStateSynchronousResponse]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_3251.CylindricalGearSetSteadyStateSynchronousResponse))
        return value

    @property
    def face_gear_sets(self) -> 'List[_3258.FaceGearSetSteadyStateSynchronousResponse]':
        '''List[FaceGearSetSteadyStateSynchronousResponse]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearSets, constructor.new(_3258.FaceGearSetSteadyStateSynchronousResponse))
        return value

    @property
    def fe_parts(self) -> 'List[_3260.FEPartSteadyStateSynchronousResponse]':
        '''List[FEPartSteadyStateSynchronousResponse]: 'FEParts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FEParts, constructor.new(_3260.FEPartSteadyStateSynchronousResponse))
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_3261.FlexiblePinAssemblySteadyStateSynchronousResponse]':
        '''List[FlexiblePinAssemblySteadyStateSynchronousResponse]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FlexiblePinAssemblies, constructor.new(_3261.FlexiblePinAssemblySteadyStateSynchronousResponse))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_3267.HypoidGearSetSteadyStateSynchronousResponse]':
        '''List[HypoidGearSetSteadyStateSynchronousResponse]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_3267.HypoidGearSetSteadyStateSynchronousResponse))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_3274.KlingelnbergCycloPalloidHypoidGearSetSteadyStateSynchronousResponse]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetSteadyStateSynchronousResponse]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearSets, constructor.new(_3274.KlingelnbergCycloPalloidHypoidGearSetSteadyStateSynchronousResponse))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_3277.KlingelnbergCycloPalloidSpiralBevelGearSetSteadyStateSynchronousResponse]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetSteadyStateSynchronousResponse]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets, constructor.new(_3277.KlingelnbergCycloPalloidSpiralBevelGearSetSteadyStateSynchronousResponse))
        return value

    @property
    def mass_discs(self) -> 'List[_3279.MassDiscSteadyStateSynchronousResponse]':
        '''List[MassDiscSteadyStateSynchronousResponse]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassDiscs, constructor.new(_3279.MassDiscSteadyStateSynchronousResponse))
        return value

    @property
    def measurement_components(self) -> 'List[_3280.MeasurementComponentSteadyStateSynchronousResponse]':
        '''List[MeasurementComponentSteadyStateSynchronousResponse]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeasurementComponents, constructor.new(_3280.MeasurementComponentSteadyStateSynchronousResponse))
        return value

    @property
    def oil_seals(self) -> 'List[_3282.OilSealSteadyStateSynchronousResponse]':
        '''List[OilSealSteadyStateSynchronousResponse]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_3282.OilSealSteadyStateSynchronousResponse))
        return value

    @property
    def part_to_part_shear_couplings(self) -> 'List[_3286.PartToPartShearCouplingSteadyStateSynchronousResponse]':
        '''List[PartToPartShearCouplingSteadyStateSynchronousResponse]: 'PartToPartShearCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PartToPartShearCouplings, constructor.new(_3286.PartToPartShearCouplingSteadyStateSynchronousResponse))
        return value

    @property
    def planet_carriers(self) -> 'List[_3289.PlanetCarrierSteadyStateSynchronousResponse]':
        '''List[PlanetCarrierSteadyStateSynchronousResponse]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetCarriers, constructor.new(_3289.PlanetCarrierSteadyStateSynchronousResponse))
        return value

    @property
    def point_loads(self) -> 'List[_3290.PointLoadSteadyStateSynchronousResponse]':
        '''List[PointLoadSteadyStateSynchronousResponse]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_3290.PointLoadSteadyStateSynchronousResponse))
        return value

    @property
    def power_loads(self) -> 'List[_3291.PowerLoadSteadyStateSynchronousResponse]':
        '''List[PowerLoadSteadyStateSynchronousResponse]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_3291.PowerLoadSteadyStateSynchronousResponse))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_3299.ShaftHubConnectionSteadyStateSynchronousResponse]':
        '''List[ShaftHubConnectionSteadyStateSynchronousResponse]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_3299.ShaftHubConnectionSteadyStateSynchronousResponse))
        return value

    @property
    def ring_pins(self) -> 'List[_3293.RingPinsSteadyStateSynchronousResponse]':
        '''List[RingPinsSteadyStateSynchronousResponse]: 'RingPins' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RingPins, constructor.new(_3293.RingPinsSteadyStateSynchronousResponse))
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_3295.RollingRingAssemblySteadyStateSynchronousResponse]':
        '''List[RollingRingAssemblySteadyStateSynchronousResponse]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingRingAssemblies, constructor.new(_3295.RollingRingAssemblySteadyStateSynchronousResponse))
        return value

    @property
    def shafts(self) -> 'List[_3300.ShaftSteadyStateSynchronousResponse]':
        '''List[ShaftSteadyStateSynchronousResponse]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_3300.ShaftSteadyStateSynchronousResponse))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_3304.SpiralBevelGearSetSteadyStateSynchronousResponse]':
        '''List[SpiralBevelGearSetSteadyStateSynchronousResponse]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_3304.SpiralBevelGearSetSteadyStateSynchronousResponse))
        return value

    @property
    def spring_dampers(self) -> 'List[_3308.SpringDamperSteadyStateSynchronousResponse]':
        '''List[SpringDamperSteadyStateSynchronousResponse]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDampers, constructor.new(_3308.SpringDamperSteadyStateSynchronousResponse))
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_3313.StraightBevelDiffGearSetSteadyStateSynchronousResponse]':
        '''List[StraightBevelDiffGearSetSteadyStateSynchronousResponse]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearSets, constructor.new(_3313.StraightBevelDiffGearSetSteadyStateSynchronousResponse))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_3316.StraightBevelGearSetSteadyStateSynchronousResponse]':
        '''List[StraightBevelGearSetSteadyStateSynchronousResponse]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_3316.StraightBevelGearSetSteadyStateSynchronousResponse))
        return value

    @property
    def synchronisers(self) -> 'List[_3323.SynchroniserSteadyStateSynchronousResponse]':
        '''List[SynchroniserSteadyStateSynchronousResponse]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Synchronisers, constructor.new(_3323.SynchroniserSteadyStateSynchronousResponse))
        return value

    @property
    def torque_converters(self) -> 'List[_3326.TorqueConverterSteadyStateSynchronousResponse]':
        '''List[TorqueConverterSteadyStateSynchronousResponse]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TorqueConverters, constructor.new(_3326.TorqueConverterSteadyStateSynchronousResponse))
        return value

    @property
    def unbalanced_masses(self) -> 'List[_3328.UnbalancedMassSteadyStateSynchronousResponse]':
        '''List[UnbalancedMassSteadyStateSynchronousResponse]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnbalancedMasses, constructor.new(_3328.UnbalancedMassSteadyStateSynchronousResponse))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_3331.WormGearSetSteadyStateSynchronousResponse]':
        '''List[WormGearSetSteadyStateSynchronousResponse]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_3331.WormGearSetSteadyStateSynchronousResponse))
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_3334.ZerolBevelGearSetSteadyStateSynchronousResponse]':
        '''List[ZerolBevelGearSetSteadyStateSynchronousResponse]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearSets, constructor.new(_3334.ZerolBevelGearSetSteadyStateSynchronousResponse))
        return value

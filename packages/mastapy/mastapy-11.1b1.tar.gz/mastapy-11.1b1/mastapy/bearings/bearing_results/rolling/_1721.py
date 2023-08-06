'''_1721.py

LoadedBallBearingResults
'''


from mastapy._internal import constructor
from mastapy.bearings.bearing_results.rolling import _1795, _1752
from mastapy._internal.python_net import python_net_import

_LOADED_BALL_BEARING_RESULTS = python_net_import('SMT.MastaAPI.Bearings.BearingResults.Rolling', 'LoadedBallBearingResults')


__docformat__ = 'restructuredtext en'
__all__ = ('LoadedBallBearingResults',)


class LoadedBallBearingResults(_1752.LoadedRollingBearingResults):
    '''LoadedBallBearingResults

    This is a mastapy class.
    '''

    TYPE = _LOADED_BALL_BEARING_RESULTS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'LoadedBallBearingResults.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def use_element_contact_angles_for_angular_velocities(self) -> 'bool':
        '''bool: 'UseElementContactAnglesForAngularVelocities' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.UseElementContactAnglesForAngularVelocities

    @property
    def track_truncation(self) -> '_1795.TrackTruncationSafetyFactorResults':
        '''TrackTruncationSafetyFactorResults: 'TrackTruncation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1795.TrackTruncationSafetyFactorResults)(self.wrapped.TrackTruncation) if self.wrapped.TrackTruncation else None

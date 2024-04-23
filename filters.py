import cv2
import numpy as np
import utils


def recolorRC(src, dst):
    """Simulate conversion from BGR to RC (red, cyan).
    The source and destination images must both be in BGR format.
    Blues and greens are replaced with cyans.
    Pseudocode:
    dst.b = dst.g = 0.5 * (src.b + src.g)
    dst.r = src.r
    """
    b, g, r = cv2.split(src)
    cv2.addWeighted(b, 0.5, g, 0.5, 0, b)
    return cv2.merge((b, b, r), dst)


def recolorRGV(src, dst):
    """Simulate conversion from BGR to RGV (red, green, value).

    The source and destination images must both be in BGR format.

    Blues are desaturated.

    Pseudocode:
    dst.b = min(src.b, src.g, src.r)
    dst.g = src.g
    dst.r = src.r

    """
    b, g, r = cv2.split(src)
    cv2.min(b, g, b)
    cv2.min(b, r, b)
    return cv2.merge((b, g, r), dst)


def recolorCMV(src, dst):
    """Simulate conversion from BGR to CMV (cyan, magenta, value).
    The source and destination images must both be in BGR format.
    Yellows are desaturated.
    Pseudocode:
    dst.b = max(src.b, src.g, src.r)
    dst.g = src.g
    dst.r = src.r
    """

    b, g, r = cv2.split(src)
    cv2.max(b, g, b)
    cv2.max(b, r, b)
    return cv2.merge((b, g, r), dst)


class vFuncFilter:
    """A filter that applies a function to V(or all channels of BGR)"""

    def __init__(self, vFunc=None, dtype=np.uint8) -> None:
        length = np.iinfo(dtype).max + 1
        self._vLookupArray = utils.createLookupArray(vFunc, length)

    def apply(self, src, dst):
        """apply the filter with a BGR or grayscale source/destination"""
        srcFlatView = utils.createFlatView(src)
        srcDestView = utils.createFlatView(dst)


class vCurveFilter(vFuncFilter):
    """A filter that applies a curve to V(or all channels of BGR)"""

    def __init__(self, vPoints, dtype=np.uint8):
        vFuncFilter.__init__(self, utils.createCurveFunc(vPoints), dtype)


class BGRFuncFilter(object):
    """A filter that applies different functions to each of BGR."""

    def __init__(self, vFunc=None, bFunc=None, gFunc=None, rFunc=None, dtype=np.uint8):
        length = np.iinfo(dtype).max + 1
        self._bLookupArray = utils.createLookupArray(
            utils.createCompositeFunc(bFunc, vFunc), length
        )
        self._gLookupArray = utils.createLookupArray(
            utils.createCompositeFunc(gFunc, vFunc), length
        )
        self._rLookupArray = utils.createLookupArray(
            utils.createCompositeFunc(rFunc, vFunc), length
        )

    def apply(self, src, dst):
        """Apply the filter with a BGR source/destination."""
        b, g, r = cv2.split(src)
        utils.applyLookupArray(self._bLookupArray, b, b)
        utils.applyLookupArray(self._gLookupArray, g, g)
        utils.applyLookupArray(self._rLookupArray, r, r)
        cv2.merge([b, g, r], dst)


class BGRCurveFilter(BGRFuncFilter):
    """A filter that applies different curves to each of BGR."""

    def __init__(
        self, vPoints=None, bPoints=None, gPoints=None, rPoints=None, dtype=np.uint8
    ):
        BGRFuncFilter.__init__(
            self,
            utils.createCurveFunc(vPoints),
            utils.createCurveFunc(bPoints),
            utils.createCurveFunc(gPoints),
            utils.createCurveFunc(rPoints),
            dtype,
        )


class BGRPortraCurveFilter(BGRCurveFilter):
    """A filter that applies kodak portra like-filters to each of BGR."""

    def __init__(self, dtype=np.uint8):
        BGRCurveFilter.__init__(
            self,
            vPoints=[(0, 0), (23, 20), (157, 173), (255, 255)],
            bPoints=[(0, 0), (41, 46), (231, 228), (255, 255)],
            gPoints=[(0, 0), (52, 47), (189, 196), (255, 255)],
            rPoints=[(0, 0), (69, 69), (213, 218), (255, 255)],
            dtype=dtype,
        )


class BGRProviaCurveFilter(BGRCurveFilter):
    """A filter that applies Provia-like curves to BGR."""

    def __init__(self, dtype=np.uint8):
        BGRCurveFilter.__init__(
            self,
            bPoints=[(0, 0), (35, 25), (205, 227), (255, 255)],
            gPoints=[(0, 0), (27, 21), (196, 207), (255, 255)],
            rPoints=[(0, 0), (59, 54), (202, 210), (255, 255)],
            dtype=dtype,
        )

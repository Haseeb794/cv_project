import cv2
import numpy as np
import utils 
def recolorRC(src,dst):
    """Simulate conversion from BGR to RC (red, cyan).
    The source and destination images must both be in BGR format.
    Blues and greens are replaced with cyans.
    Pseudocode:
    dst.b = dst.g = 0.5 * (src.b + src.g)
    dst.r = src.r
    """
    b, g, r = cv2.split(src)
    cv2.addWeighted(b, 0.5, g, 0.5, 0, b)
    cv2.merge((b, b, r), dst)
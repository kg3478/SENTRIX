# ai/local_fallback_engine.py
#
# ARCHITECTURE: Pure-OpenCV heuristics used when cloud threat engine is
# unavailable or has exceeded MAX_CONSECUTIVE_FAIL.
# Detects weapon-like elongated objects by shape analysis in the hand-zone ROI.
# Intentionally simple — prototype quality, not production accuracy.
# Always returns a float score; never raises.

import cv2


class LocalFallbackEngine:
    """
    OpenCV-based weapon heuristic detector.
    Looks for elongated contours in the mid-frame hand-height region.
    """

    def detect_weapon_heuristic(self, frame) -> float:
        """
        Strategy: scan lower-middle region of frame for elongated dark objects
        that might indicate a weapon being held.
        Returns 0.0 (no hit) or 0.35 (low-confidence hit).
        """
        try:
            gray    = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            edges   = cv2.Canny(blurred, 50, 150)

            h, w = frame.shape[:2]
            roi  = edges[h // 3 : 2 * h // 3, w // 4 : 3 * w // 4]

            contours, _ = cv2.findContours(
                roi, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
            )

            for contour in contours:
                area = cv2.contourArea(contour)
                if area < 500:
                    continue
                _, _, cw, ch = cv2.boundingRect(contour)
                aspect = cw / max(ch, 1)
                if aspect > 4.5 or aspect < 0.2:  # very elongated → weapon-like (made stricter to avoid phones)
                    return 0.35

            return 0.0

        except Exception:
            return 0.0

    # Legacy alias used by old system_engine
    def detect_weapon(self, frame) -> float:
        return self.detect_weapon_heuristic(frame)
// Small seek-safe motion helpers shared by the scenes (DESIGN.md §6: enters ease out, exits ease in, nothing bounces).
// Every helper adds fromTo tweens to the given paused timeline at an absolute scene time.
window.fx = {
  ENTER: "power3.out",
  EXIT: "power2.in",
  // rise 16 px and fade in over 0.25 s, starting at t
  in(tl, sel, t, d = 0.25, y = 16) {
    tl.fromTo(sel, { opacity: 0, y }, { opacity: 1, y: 0, duration: d, ease: this.ENTER }, t);
  },
  // fade out over 0.18 s, starting at t (a scene leaves completely before the next one arrives)
  out(tl, sel, t, d = 0.18) {
    tl.fromTo(sel, { opacity: 1 }, { opacity: 0, duration: d, ease: this.EXIT, immediateRender: false }, t);
  },
  // a fact stamp: lands from slightly larger, no overshoot
  stamp(tl, sel, t, rot = -2) {
    tl.fromTo(sel, { opacity: 0, scale: 1.25, rotation: rot }, { opacity: 1, scale: 1, rotation: rot, duration: 0.35, ease: this.ENTER }, t);
  },
  // turn a card: back (portrait) to face (role), 0.9 s
  flip(tl, sel, t) {
    tl.fromTo(sel, { rotationY: 0 }, { rotationY: 180, duration: 0.9, ease: "power2.inOut" }, t);
  },
};

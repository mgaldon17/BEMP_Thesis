// ----------------------------------------------------------------------------
//  fragment.glsl — soft circular particle
//  Draws each point as a soft-edged disc. Alpha decays as the particle
//  scatters away from "home" so the cloud dissolves into the void rather
//  than leaving hard dots floating.
// ----------------------------------------------------------------------------

uniform float uOpacity;    // global fade (used by the loader / scene)

varying vec3 vColor;
varying float vProgress;   // 0 assembled .. 1 scattered (per particle)

void main() {
  // gl_PointCoord is 0..1 across the point sprite; centre it.
  vec2 uv = gl_PointCoord - 0.5;
  float d = length(uv);

  // Soft circular mask: 1 in the middle, fading to 0 at the edge.
  float circle = smoothstep(0.5, 0.18, d);
  if (circle <= 0.0) discard;

  // Fade out as the particle disperses (keeps the dark palette clean).
  float scatterFade = 1.0 - vProgress * 0.75;

  float alpha = circle * scatterFade * uOpacity;

  // A faint core boost gives each particle a tiny glow that Bloom picks up.
  vec3 col = vColor + vColor * (1.0 - smoothstep(0.0, 0.25, d)) * 0.4;

  gl_FragColor = vec4(col, alpha);
}

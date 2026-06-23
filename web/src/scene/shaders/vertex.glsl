// ----------------------------------------------------------------------------
//  vertex.glsl — the decompose displacement
//  Each particle starts at its assembled `position` (built from the source
//  image) and is pushed along a curl-noise flow as uProgress 0 -> 1.
//  A per-particle staggered smoothstep makes the dispersal feel organic
//  rather than everything moving at once.
// ----------------------------------------------------------------------------

uniform float uProgress;   // 0 = fully assembled, 1 = fully scattered
uniform float uTime;       // seconds, drives the slow noise drift
uniform float uFreq;       // spatial frequency of the curl field
uniform float uAmplitude;  // how far particles travel when scattered
uniform float uSize;       // base point size in world units

attribute vec3 aColor;     // pixel colour sampled from the source image
attribute float aRandom;   // per-particle seed 0..1 (delay + amplitude)
attribute vec3 aSeed;      // base random direction (adds variety to flow)

varying vec3 vColor;
varying float vProgress;   // local (per-particle) dispersal amount

// curlNoise() + snoise() are prepended at build time (see DecomposeParticles).

void main() {
  vColor = aColor;

  // Curl-noise flow field sampled at the assembled position, drifting in time.
  vec3 flow = curlNoise(position * uFreq + uTime * 0.08 + aSeed);

  // Fully-scattered target: travel distance varies per particle via aRandom.
  vec3 scattered = position + flow * (aRandom * uAmplitude);

  // Staggered reveal: each particle has its own [start, end] window inside
  // the global 0..1 progress, so they don't all let go simultaneously.
  float p = smoothstep(aRandom * 0.4, 0.4 + aRandom * 0.6, uProgress);
  vProgress = p;

  vec3 finalPos = mix(position, scattered, p);

  vec4 mvPosition = modelViewMatrix * vec4(finalPos, 1.0);
  gl_Position = projectionMatrix * mvPosition;

  // Perspective sizing: closer particles are bigger, and points grow slightly
  // as they scatter so the cloud reads as expanding energy.
  gl_PointSize = uSize * (1.0 + p * 0.6) * (300.0 / -mvPosition.z);
}

import SexticC3.Model

-- Generated from the v1 certificate.
namespace SexticC3
def delta {R : Type*} [CommRing R] (a b c d : R) : R :=
  (3125) * d^4 + (256) * c^5 + (-1600) * b * c^3 * d + (2250) * b^2 * c * d^2 + (-27) * b^4 * c^2 + (108) * b^5 * d + (2000) * a * c^2 * d^2 + (-3750) * a * b * d^3 + (144) * a * b^2 * c^3 + (-630) * a * b^3 * c * d + (-128) * a^2 * c^4 + (560) * a^2 * b * c^2 * d + (825) * a^2 * b^2 * d^2 + (-900) * a^3 * c * d^2 + (-4) * a^3 * b^2 * c^2 + (16) * a^3 * b^3 * d + (16) * a^4 * c^3 + (-72) * a^4 * b * c * d + (108) * a^5 * d^2
end SexticC3

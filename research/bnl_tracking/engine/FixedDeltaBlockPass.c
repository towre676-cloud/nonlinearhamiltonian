/* Original fixed-delta 4D guard/map kernel. Uses Accelerator Toolbox's
 * Apache-2.0 integrator interface headers; retain their upstream LICENSE.
 * A guard rejection means UNCERTAIN and must trigger charged native fallback.
 * ct is intentionally unchanged; RF/radiation must be off, dp must be fixed.
 */
#include "atelem.c"

struct elem { double *A4; double *B4; double *Radius4; double FixedDelta; };

ExportMode struct elem *trackFunction(const atElem *data, struct elem *elem,
        double *r, int n, struct parameters *param)
{
    if (!elem) {
        double *a=atGetDoubleArray(data,"A4"); check_error();
        double *b=atGetDoubleArray(data,"B4"); check_error();
        double *radius=atGetDoubleArray(data,"Radius4"); check_error();
        double dp=atGetDouble(data,"FixedDelta"); check_error();
        elem=(struct elem*)atMalloc(sizeof(struct elem));
        elem->A4=a;elem->B4=b;elem->Radius4=radius;elem->FixedDelta=dp;
    }
    for (int k=0;k<n;k++) {
        double *v=r+6*k;
        if (!atIsNaN(v[0])) {
            if (v[4]!=elem->FixedDelta || !isfinite(v[5]) ||
                !isfinite(v[0]) || !isfinite(v[1]) || !isfinite(v[2]) || !isfinite(v[3]) ||
                fabs(v[0])>elem->Radius4[0] || fabs(v[1])>elem->Radius4[1] ||
                fabs(v[2])>elem->Radius4[2] || fabs(v[3])>elem->Radius4[3]) {
                v[0]=NAN; continue;
            }
            double u[4]={v[0],v[1],v[2],v[3]};
            for (int i=0;i<4;i++)
                v[i]=elem->B4[i]+elem->A4[i]*u[0]+elem->A4[i+4]*u[1]+
                    elem->A4[i+8]*u[2]+elem->A4[i+12]*u[3];
        }
    }
    return elem;
}
MODULE_DEF(FixedDeltaBlockPass)

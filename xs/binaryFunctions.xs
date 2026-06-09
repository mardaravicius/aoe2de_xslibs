const int _cMtN = 624;
const int _cMtM = 397;
int _cMtNm = -1;
const int _cMtW = 32;
const int _cMtR = 31;
int _cMtMatrixA = -1;
int _cMtUpperMask = -1;
int _cMtLowerMask = -1;
int _cMtA = -1;
const int _cMtU = 11;
const int _cMtS = 7;
const int _cMtT = 15;
const int _cMtL = 18;
int _cMtB = -1;
const int _cMtC = -272236544;
int _cMtF = -1;
bool _mtSeedSet = false;
int _mtStateArray = -1;
int _mtStateIndex = 0;

int _xsBitShiftRightDivide(int x = -1, int n = -1, int divisor = -1) {
    if (n == 31) {
        if (x < 0) {
            return (-1);
        }
        return (0);
    }
    return (x / divisor);
}

int xsBitShiftLeft(int x = 0, int n = 0) {
    if ((n < 0) || (n >= 32)) {
        return (0);
    }
    return (x * (0 + pow(2.0, n)));
}

int xsBitShiftRightArithmetic(int x = 0, int n = 0) {
    if ((n < 0) || (n >= 32)) {
        if (x < 0) {
            return (-1);
        }
        return (0);
    }
    return (_xsBitShiftRightDivide(x, n, 0 + pow(2.0, n)));
}

int xsBitShiftRightLogical(int x = 0, int n = 0) {
    if ((n < 0) || (n >= 32)) {
        return (0);
    }
    if (x < 0) {
        x = x + (-214748364 * 10 - 8);
        x = _xsBitShiftRightDivide(x, n, 0 + pow(2.0, n));
        return (x + (0 + pow(2.0, 31 - n)));
    }
    return (_xsBitShiftRightDivide(x, n, 0 + pow(2.0, n)));
}

void xsMtSeed(int seed = 0) {
    if (_mtStateArray < 0) {
        _cMtMatrixA = -172748368 * 10 - 1;
        _cMtUpperMask = xsBitShiftLeft(-1, _cMtR);
        _cMtLowerMask = xsBitShiftRightLogical(-1, _cMtW - _cMtR);
        _cMtA = -172748368 * 10 - 1;
        _cMtB = -165803865 * 10 - 6;
        _cMtF = 181243325 * 10 + 3;
        _cMtNm = _cMtN - _cMtM;
        _mtStateArray = xsArrayCreateInt(_cMtN, 0, "_mtStateArray");
    }
    xsArraySetInt(_mtStateArray, 0, seed);
    int i = 1;
    while (i < _cMtN) {
        seed = (_cMtF * bitXor(seed, xsBitShiftRightLogical(seed, _cMtW - 2))) + i;
        xsArraySetInt(_mtStateArray, i, seed);
        i++;
    }
    _mtStateIndex = 0;
    _mtSeedSet = true;
}

int xsMtRandom() {
    if (_mtSeedSet == false) {
        xsMtSeed(((xsGetRandomNumber() * 32768) + xsGetRandomNumber()) + xsBitShiftLeft(xsGetRandomNumber(), 30));
    }
    int k = _mtStateIndex;
    int j = k - (_cMtN - 1);
    if (j < 0) {
        j = j + _cMtN;
    }
    int x = bitOr(bitAnd(xsArrayGetInt(_mtStateArray, k), _cMtUpperMask), bitAnd(xsArrayGetInt(_mtStateArray, j), _cMtLowerMask));
    int xa = xsBitShiftRightLogical(x, 1);
    if (bitAnd(x, 1) != 0) {
        xa = bitXor(xa, _cMtA);
    }
    j = k - _cMtNm;
    if (j < 0) {
        j = j + _cMtN;
    }
    x = bitXor(xsArrayGetInt(_mtStateArray, j), xa);
    xsArraySetInt(_mtStateArray, k, x);
    k++;
    if (k >= _cMtN) {
        k = 0;
    }
    _mtStateIndex = k;
    int y = bitXor(x, xsBitShiftRightLogical(x, _cMtU));
    y = bitXor(y, bitAnd(xsBitShiftLeft(y, _cMtS), _cMtB));
    y = bitXor(y, bitAnd(xsBitShiftLeft(y, _cMtT), _cMtC));
    return (bitXor(y, xsBitShiftRightLogical(y, _cMtL)));
}

int xsMtRandomUniformRange(int start = 0, int end = 999999999) {
    if (end <= start) {
        return (-1);
    }
    int dst = end - start;
    if (dst == 1) {
        return (start);
    }
    int dstM = dst - 1;
    if (bitAnd(dst, dstM) == 0) {
        return (bitAnd(xsMtRandom(), dstM) + start);
    }
    if (dst > 0) {
        while (true) {
            int r = xsBitShiftRightLogical(xsMtRandom(), 1);
            int c = r % dst;
            if (((r + dstM) - c) >= 0) {
                return (c + start);
            }
        }
    }
    while (true) {
        int rr = xsMtRandom();
        if ((rr >= start) && (rr < end)) {
            return (rr);
        }
    }
    return (-1);
}

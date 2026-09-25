const int _cMtN = 624;
const int _cMtM = 397;
int _cMtNm = -1;
const int _cMtW = 32;
const int _cMtR = 31;
const int _cMtW2 = 30;
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
int _cMtIntMax = -1;
int _cMtFloat1AsInt = -1;
bool _mtSeedNotSet = true;
int _mtStateArray = -1;
int _mtStateIndex = 0;

int _xsBitShiftRightLogical(int x = 0, int n = 0) {
    if (x < 0) {
        x = x + bitLsh(-1, 31);
        x = bitRsh(x, n);
        return (x + bitLsh(1, 31 - n));
    }
    return (bitRsh(x, n));
}

int xsBitShiftRightLogical(int x = 0, int n = 0) {
    if ((n < 0) || (n >= 32)) {
        return (0);
    }
    return (_xsBitShiftRightLogical(x, n));
}

void xsMtSeed(int seed = 0) {
    if (_mtStateArray < 0) {
        _cMtMatrixA = -172748368 * 10 - 1;
        _cMtUpperMask = bitLsh(-1, _cMtR);
        _cMtLowerMask = _xsBitShiftRightLogical(-1, _cMtW - _cMtR);
        _cMtA = -172748368 * 10 - 1;
        _cMtB = -165803865 * 10 - 6;
        _cMtF = 181243325 * 10 + 3;
        _cMtNm = _cMtN - _cMtM;
        _mtStateArray = xsArrayCreateInt(_cMtN, 0, "_mtStateArray");
        _cMtIntMax = 214748364 * 10 + 7;
        _cMtFloat1AsInt = 106535321 * 10 + 6;
    }
    xsArraySetInt(_mtStateArray, 0, seed);
    int i = 1;
    while (i < _cMtN) {
        seed = (_cMtF * bitXor(seed, _xsBitShiftRightLogical(seed, _cMtW2))) + i;
        xsArraySetInt(_mtStateArray, i, seed);
        i++;
    }
    _mtStateIndex = 0;
    _mtSeedNotSet = false;
}

int xsMtRandom() {
    if (_mtSeedNotSet) {
        xsMtSeed((bitRsh(xsGetRandomNumber(), 4) + bitLsh(bitRsh(xsGetRandomNumber(), 4), 11)) + bitLsh(bitRsh(xsGetRandomNumber(), 5), 22));
    }
    int k = _mtStateIndex;
    int j = k - (_cMtN - 1);
    if (j < 0) {
        j = j + _cMtN;
    }
    int x = bitOr(bitAnd(xsArrayGetInt(_mtStateArray, k), _cMtUpperMask), bitAnd(xsArrayGetInt(_mtStateArray, j), _cMtLowerMask));
    int xa = _xsBitShiftRightLogical(x, 1);
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
    int y = bitXor(x, _xsBitShiftRightLogical(x, _cMtU));
    y = bitXor(y, bitAnd(bitLsh(y, _cMtS), _cMtB));
    y = bitXor(y, bitAnd(bitLsh(y, _cMtT), _cMtC));
    return (bitXor(_xsBitShiftRightLogical(y, _cMtL), y));
}

float xsMtRandomFloat() {
    int bits = bitOr(bitAnd(xsMtRandom(), _cMtIntMax) / 256, _cMtFloat1AsInt);
    return (bitCastToFloat(bits) - 1.0);
}

bool xsMtRandomBool() {
    return (xsMtRandom() > -1);
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
            int r = _xsBitShiftRightLogical(xsMtRandom(), 1);
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

int _bitOperatorPowers = -1;
int _cBitOperatorIntMinValue = -1;
const int _cMtN = 624;
const int _cMtM = 397;
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

int _xsBitOperatorGetIntMinValue() {
    if (_cBitOperatorIntMinValue == -1) {
        _cBitOperatorIntMinValue = -214748364 * 10 - 8;
    }
    return (_cBitOperatorIntMinValue);
}

int _xsBitGetPowers() {
    if (_bitOperatorPowers == -1) {
        _bitOperatorPowers = xsArrayCreateInt(32, 1, "_bitOperatorPowers");
        for (i = 1; < 32) {
            xsArraySetInt(_bitOperatorPowers, i, xsArrayGetInt(_bitOperatorPowers, i - 1) * 2);
        }
    }
    return (_bitOperatorPowers);
}

int _xsBitGet(int x = 0, int i = 0, int powers = -1) {
    int mod = xsArrayGetInt(powers, i + 1);
    int b = (x % mod) / xsArrayGetInt(powers, i);
    if (b < 0) {
        b = b + 2;
    }
    return (b);
}

int _xsBitSet(int bit = 0, int i = 0, int powers = -1) {
    return (bit * xsArrayGetInt(powers, i));
}

int _xsBitShiftRightDivide(int x = -1, int n = -1, int powers = -1) {
    if (n == 31) {
        int p = xsArrayGetInt(powers, 30);
        return ((x / p) / 2);
    }
    return (x / xsArrayGetInt(powers, n));
}

int xsBitShiftRightLogical(int x = 0, int n = 0) {
    if ((n < 0) || (n >= 32)) {
        return (0);
    }
    int powers = _xsBitGetPowers();
    if (x < 0) {
        x = x + _xsBitOperatorGetIntMinValue();
        x = _xsBitShiftRightDivide(x, n, powers);
        return (x + xsArrayGetInt(powers, 31 - n));
    }
    return (_xsBitShiftRightDivide(x, n, powers));
}

int xsBitShiftRightArithmetic(int x = 0, int n = 0) {
    if ((n < 0) || (n >= 32)) {
        if (x < 0) {
            return (-1);
        }
        return (0);
    }
    return (_xsBitShiftRightDivide(x, n, _xsBitGetPowers()));
}

int xsBitShiftLeft(int x = 0, int n = 0) {
    if ((n < 0) || (n >= 32)) {
        return (0);
    }
    return (x * xsArrayGetInt(_xsBitGetPowers(), n));
}

int xsBitNot(int n = 0) {
    return ((n * -1) - 1);
}

int xsBitAnd(int a = 0, int b = 0) {
    int powers = _xsBitGetPowers();
    int res = 0;
    for (i = 0; < 31) {
        int abit = _xsBitGet(a, i, powers);
        int bbit = _xsBitGet(b, i, powers);
        int bit = abit * bbit;
        res = res + _xsBitSet(bit, i, powers);
    }
    if ((a < 0) && (b < 0)) {
        res = res + _xsBitOperatorGetIntMinValue();
    }
    return (res);
}

int xsBitOr(int a = 0, int b = 0) {
    int powers = _xsBitGetPowers();
    int res = 0;
    for (i = 0; < 31) {
        int abit = _xsBitGet(a, i, powers);
        int bbit = _xsBitGet(b, i, powers);
        int bit = (abit + bbit) - (abit * bbit);
        res = res + _xsBitSet(bit, i, powers);
    }
    if ((a < 0) || (b < 0)) {
        res = res + _xsBitOperatorGetIntMinValue();
    }
    return (res);
}

int xsBitXor(int a = 0, int b = 0) {
    int powers = _xsBitGetPowers();
    int res = 0;
    for (i = 0; < 31) {
        int abit = _xsBitGet(a, i, powers);
        int bbit = _xsBitGet(b, i, powers);
        int bit = (abit + bbit) % 2;
        res = res + _xsBitSet(bit, i, powers);
    }
    if (((a < 0) && (b >= 0)) || ((a >= 0) && (b < 0))) {
        res = res + _xsBitOperatorGetIntMinValue();
    }
    return (res);
}

void xsMtSeed(int seed = 0) {
    if (_mtStateArray < 0) {
        _cMtMatrixA = -172748368 * 10 - 1;
        _cMtUpperMask = -214748364 * 10 - 8;
        _cMtLowerMask = 214748364 * 10 + 7;
        _cMtA = -172748368 * 10 - 1;
        _cMtB = -165803865 * 10 - 6;
        _cMtF = 181243325 * 10 + 3;
        _mtStateArray = xsArrayCreateInt(_cMtN, 0, "_mtStateArray");
    }
    xsArraySetInt(_mtStateArray, 0, seed);
    int i = 1;
    while (i < _cMtN) {
        seed = (_cMtF * xsBitXor(seed, xsBitShiftRightLogical(seed, _cMtW - 2))) + i;
        xsArraySetInt(_mtStateArray, i, seed);
        i++;
    }
    _mtStateIndex = 0;
    _mtSeedSet = true;
}

int xsMtRandom() {
    if (_mtSeedSet == false) {
        xsMtSeed((xsGetRandomNumber() * 65536) + xsGetRandomNumber());
    }
    int k = _mtStateIndex;
    int j = k - (_cMtN - 1);
    if (j < 0) {
        j = j + _cMtN;
    }
    int x = xsBitOr(xsBitAnd(xsArrayGetInt(_mtStateArray, k), _cMtUpperMask), xsBitAnd(xsArrayGetInt(_mtStateArray, j), _cMtLowerMask));
    int xa = xsBitShiftRightLogical(x, 1);
    if (xsBitAnd(x, 1) != 0) {
        xa = xsBitXor(xa, _cMtA);
    }
    j = k - (_cMtN - _cMtM);
    if (j < 0) {
        j = j + _cMtN;
    }
    x = xsBitXor(xsArrayGetInt(_mtStateArray, j), xa);
    xsArraySetInt(_mtStateArray, k, x);
    k++;
    if (k >= _cMtN) {
        k = 0;
    }
    _mtStateIndex = k;
    int y = xsBitXor(x, xsBitShiftRightLogical(x, _cMtU));
    y = xsBitXor(y, xsBitAnd(xsBitShiftLeft(y, _cMtS), _cMtB));
    y = xsBitXor(y, xsBitAnd(xsBitShiftLeft(y, _cMtT), _cMtC));
    int z = xsBitXor(y, xsBitShiftRightLogical(y, _cMtL));
    return (z);
}

int xsMtRandomUniformRange(int start = 0, int end = 999999999) {
    int rg = end - start;
    if (rg <= 0) {
        return (-1);
    }
    if (rg == 1) {
        return (start);
    }
    if (xsBitAnd(rg, rg - 1) == 0) {
        return (start + xsBitAnd(xsMtRandom(), rg - 1));
    }
    int threshold = (-1 * rg) % rg;
    while (true) {
        int r = xsMtRandom();
        int unsignedR = r + _xsBitOperatorGetIntMinValue();
        if (unsignedR >= threshold) {
            int result = unsignedR % rg;
            return (start + result);
        }
    }
}

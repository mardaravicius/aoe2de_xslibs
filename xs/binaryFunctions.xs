int _bitOperatorPowers = -1;
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

int _xsBitGetPowers() {
    if (_bitOperatorPowers == -1) {
        _bitOperatorPowers = xsArrayCreateInt(32, 1, "_bitOperatorPowers");
        for (i = 1; < 32) {
            xsArraySetInt(_bitOperatorPowers, i, xsArrayGetInt(_bitOperatorPowers, i - 1) * 2);
        }
    }
    return (_bitOperatorPowers);
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
        x = x + xsArrayGetInt(powers, 31);
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
    for (i = 0; < 32) {
        int m = xsArrayGetInt(powers, 31 - i);
        int an = a * m;
        int bn = b * m;
        if ((an < 0) && (bn < 0)) {
            res = res + (1 * xsArrayGetInt(powers, i));
        }
    }
    return (res);
}

int xsBitOr(int a = 0, int b = 0) {
    int powers = _xsBitGetPowers();
    int res = 0;
    for (i = 0; < 32) {
        int m = xsArrayGetInt(powers, 31 - i);
        int an = a * m;
        int bn = b * m;
        if ((an < 0) || (bn < 0)) {
            res = res + (1 * xsArrayGetInt(powers, i));
        }
    }
    return (res);
}

int xsBitXor(int a = 0, int b = 0) {
    int powers = _xsBitGetPowers();
    int res = 0;
    for (i = 0; < 32) {
        int m = xsArrayGetInt(powers, 31 - i);
        int an = a * m;
        int bn = b * m;
        if (((an < 0) && (bn >= 0)) || ((an >= 0) && (bn < 0))) {
            res = res + (1 * xsArrayGetInt(powers, i));
        }
    }
    return (res);
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
    j = k - _cMtNm;
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
    return (xsBitXor(y, xsBitShiftRightLogical(y, _cMtL)));
}

int xsMtRandomUniformRange(int start = 0, int end = 999999999) {
    if (end <= start) {
        return (-1);
    }
    int dist = end - start;
    if (dist == 1) {
        return (start);
    }
    int distm = dist - 1;
    if (xsBitAnd(dist, distm) == 0) {
        return (xsBitAnd(xsMtRandom(), distm) + start);
    }
    if (dist > 0) {
        while (true) {
            int r = xsBitShiftRightLogical(xsMtRandom(), 1);
            int c = r % dist;
            if (((r + distm) - c) >= 0) {
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

int _cXoSplitmix32A = -1;
const int _cXoSplitmix32B = 569420461;
int _cXoSplitmix32C = -1;
int _cXoIntMax = -1;
int _cXoFloat1AsInt = -1;
int _xoSplitmix32S = 0;
int _xoS0 = 0;
int _xoS1 = 0;
int _xoS2 = 0;
int _xoS3 = 0;
bool _xoSeedNotSet = true;

int _xoBitShiftRightLogical(int x = -1, int n = -1) {
    if (x < 0) {
        x = x + bitLsh(-1, 31);
        x = bitRsh(x, n);
        return (x + bitLsh(1, 31 - n));
    }
    return (bitRsh(x, n));
}

int _xoRotl(int x = -1, int k = -1) {
    return (bitOr(bitLsh(x, k), _xoBitShiftRightLogical(x, 32 - k)));
}

int _xoSplitmix32() {
    _xoSplitmix32S = _xoSplitmix32S + _cXoSplitmix32A;
    int z = _xoSplitmix32S;
    z = bitXor(z, _xoBitShiftRightLogical(z, 16));
    z = z * _cXoSplitmix32B;
    z = bitXor(z, _xoBitShiftRightLogical(z, 15));
    z = z * _cXoSplitmix32C;
    z = bitXor(z, _xoBitShiftRightLogical(z, 15));
    return (z);
}

void xsXoSeed(int seed = 0) {
    if (_cXoSplitmix32A < 0) {
        _cXoSplitmix32A = -164053152 * 10 - 7;
        _cXoSplitmix32C = 193528975 * 10 + 1;
        _cXoIntMax = 214748364 * 10 + 7;
        _cXoFloat1AsInt = 106535321 * 10 + 6;
    }
    _xoSplitmix32S = seed;
    _xoS0 = _xoSplitmix32();
    _xoS1 = _xoSplitmix32();
    _xoS2 = _xoSplitmix32();
    _xoS3 = _xoSplitmix32();
    if ((_xoS0 == 0) && (_xoS1 == 0) && (_xoS2 == 0) && (_xoS3 == 0)) {
        _xoS0 = 1;
    }
    _xoSeedNotSet = false;
}

int xsXoRandom() {
    if (_xoSeedNotSet) {
        xsXoSeed((bitRsh(xsGetRandomNumber(), 4) + bitLsh(bitRsh(xsGetRandomNumber(), 4), 11)) + bitLsh(bitRsh(xsGetRandomNumber(), 5), 22));
    }
    int result = _xoRotl(_xoS1 * 5, 7) * 9;
    int t = bitLsh(_xoS1, 9);
    _xoS2 = bitXor(_xoS2, _xoS0);
    _xoS3 = bitXor(_xoS3, _xoS1);
    _xoS1 = bitXor(_xoS1, _xoS2);
    _xoS0 = bitXor(_xoS0, _xoS3);
    _xoS2 = bitXor(_xoS2, t);
    _xoS3 = _xoRotl(_xoS3, 11);
    return (result);
}

float xsXoRandomFloat() {
    int bits = bitOr(bitAnd(xsXoRandom(), _cXoIntMax) / 256, _cXoFloat1AsInt);
    return (bitCastToFloat(bits) - 1.0);
}

bool xsXoRandomBool() {
    return (xsXoRandom() > -1);
}

int xsXoRandomUniformRange(int start = 0, int end = 999999999) {
    if (end <= start) {
        return (-1);
    }
    int dst = end - start;
    if (dst == 1) {
        return (start);
    }
    int dstM = dst - 1;
    if (bitAnd(dst, dstM) == 0) {
        return (bitAnd(xsXoRandom(), dstM) + start);
    }
    if (dst > 0) {
        while (true) {
            int r = _xoBitShiftRightLogical(xsXoRandom(), 1);
            int c = r % dst;
            if (((r + dstM) - c) >= 0) {
                return (c + start);
            }
        }
    }
    while (true) {
        int rr = xsXoRandom();
        if ((rr >= start) && (rr < end)) {
            return (rr);
        }
    }
    return (-1);
}

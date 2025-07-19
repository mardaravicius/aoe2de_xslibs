extern const int cIntIntDictSuccess = 0;
extern const int cIntIntDictGenericError = -1;
extern const int cIntIntDictNoKeyError = -2;
extern const int cIntIntDictResizeFailedError = -3;
extern const int cIntIntDictMaxCapacityError = -4;
extern const int cIntIntDictMaxCapacity = 999999999;
extern const float cIntIntDictMaxLoadFactor = 0.75;
extern const int cIntIntDictEmptyParam = -999999999;
extern const int cIntIntDictInitialNumOfBuckets = 17;
extern const int cIntIntDictInitialBucketSize = 3;
extern const int cIntIntDictMinBucketSize = 3;
extern const int cIntIntDictHashConstant = 16777619;
int _cIntIntDictLastOperationStatus = cIntIntDictSuccess;
bool _cIntIntDictKeyExists = false;
int _intIntDictTempArray = -1;
int _intIntDictIteratorPrevKey = -1;
int _intIntDictIteratorPrevIdx = 1;

int _xsIntIntDictHash(int key = -1, int numOfBuckets = 0) {
    int hash = key * cIntIntDictHashConstant;
    hash = hash % numOfBuckets;
    if (hash < 0) {
        hash = hash + numOfBuckets;
    }
    return (hash + 1);
}

int _xsIntIntDictReplace(int dct = -1, int key = -1, int val = 0, int numOfBuckets = 0) {
    int hash = _xsIntIntDictHash(key, numOfBuckets);
    int bucket = xsArrayGetInt(dct, hash);
    if (bucket < 0) {
        bucket = xsArrayCreateInt(cIntIntDictInitialBucketSize, cIntIntDictEmptyParam);
        if (bucket < 0) {
            _cIntIntDictLastOperationStatus = cIntIntDictResizeFailedError;
            return (cIntIntDictGenericError);
        }
        xsArraySetInt(bucket, 1, key);
        xsArraySetInt(bucket, 2, val);
        xsArraySetInt(bucket, 0, 2);
        xsArraySetInt(dct, hash, bucket);
        _cIntIntDictLastOperationStatus = cIntIntDictNoKeyError;
        return (cIntIntDictGenericError);
    }
    int bucketSize = xsArrayGetInt(bucket, 0);
    int j = 1;
    bool found = false;
    int foundValue = cIntIntDictGenericError;
    while ((j <= bucketSize) && (found == false)) {
        int storedKey = xsArrayGetInt(bucket, j);
        if (storedKey == key) {
            foundValue = xsArrayGetInt(bucket, j + 1);
            xsArraySetInt(bucket, j + 1, val);
            found = true;
        }
        j = j + 2;
    }
    if (found == false) {
        int bucketCapacity = xsArrayGetSize(bucket);
        if (((bucketCapacity - 1) - bucketSize) < 2) {
            int newBucketCapacity = ((bucketCapacity - 1) * 2) + 1;
            if (newBucketCapacity > cIntIntDictMaxCapacity) {
                _cIntIntDictLastOperationStatus = cIntIntDictMaxCapacityError;
                return (cIntIntDictGenericError);
            }
            int r = xsArrayResizeInt(bucket, newBucketCapacity);
            if (r != 1) {
                _cIntIntDictLastOperationStatus = cIntIntDictResizeFailedError;
                return (cIntIntDictGenericError);
            }
        }
        xsArraySetInt(bucket, bucketSize + 1, key);
        xsArraySetInt(bucket, bucketSize + 2, val);
        xsArraySetInt(bucket, 0, bucketSize + 2);
        _cIntIntDictLastOperationStatus = cIntIntDictNoKeyError;
    } else {
        _cIntIntDictLastOperationStatus = cIntIntDictSuccess;
    }
    return (foundValue);
}

int _xsIntIntDictMoveToTempArray(int dct = -1, int totalSize = 0, int dictCapacity = 0) {
    int tempDataSize = totalSize * 2;
    if (_intIntDictTempArray < 0) {
        _intIntDictTempArray = xsArrayCreateInt(tempDataSize, cIntIntDictEmptyParam);
        if (_intIntDictTempArray < 0) {
            return (cIntIntDictResizeFailedError);
        }
    } else {
        int tempArrCapacity = xsArrayGetSize(_intIntDictTempArray);
        if (tempArrCapacity < tempDataSize) {
            if (tempDataSize > cIntIntDictMaxCapacity) {
                return (cIntIntDictMaxCapacityError);
            }
            int r = xsArrayResizeInt(_intIntDictTempArray, tempDataSize);
            if (r != 1) {
                return (cIntIntDictResizeFailedError);
            }
        }
    }
    int t = 0;
    for (i = 1; < dictCapacity) {
        int bucket = xsArrayGetInt(dct, i);
        if (bucket >= 0) {
            int bucketSize = xsArrayGetInt(bucket, 0);
            int j = 1;
            while (j <= bucketSize) {
                int storedKey = xsArrayGetInt(bucket, j);
                int storedVal = xsArrayGetInt(bucket, j + 1);
                xsArraySetInt(_intIntDictTempArray, t, storedKey);
                xsArraySetInt(_intIntDictTempArray, t + 1, storedVal);
                t = t + 2;
                j = j + 2;
            }
            xsArraySetInt(bucket, 0, 0);
        }
    }
    return (tempDataSize);
}

int xsIntIntDictPut(int dct = -1, int key = -1, int val = 0) {
    int totalSize = xsArrayGetInt(dct, 0);
    int dictCapacity = xsArrayGetSize(dct);
    int previousValue = _xsIntIntDictReplace(dct, key, val, dictCapacity - 1);
    if (_cIntIntDictLastOperationStatus == cIntIntDictNoKeyError) {
        totalSize++;
        xsArraySetInt(dct, 0, totalSize);
    } else if (_cIntIntDictLastOperationStatus == cIntIntDictSuccess) {
        return (previousValue);
    } else {
        return (cIntIntDictGenericError);
    }
    float loadFactor = (0.0 + totalSize) / (dictCapacity - 1);
    if (loadFactor > cIntIntDictMaxLoadFactor) {
        int storeStatus = _cIntIntDictLastOperationStatus;
        int tempDataSize = _xsIntIntDictMoveToTempArray(dct, totalSize, dictCapacity);
        if (tempDataSize < 0) {
            _cIntIntDictLastOperationStatus = tempDataSize;
            return (cIntIntDictGenericError);
        }
        int newDictCapacity = ((dictCapacity - 1) * 2) + 1;
        if (newDictCapacity > cIntIntDictMaxCapacity) {
            _cIntIntDictLastOperationStatus = cIntIntDictResizeFailedError;
            return (cIntIntDictGenericError);
        }
        int r = xsArrayResizeInt(dct, newDictCapacity);
        if (r != 1) {
            _cIntIntDictLastOperationStatus = cIntIntDictResizeFailedError;
            return (cIntIntDictGenericError);
        }
        for (b = dictCapacity; < newDictCapacity) {
            xsArraySetInt(dct, b, cIntIntDictEmptyParam);
        }
        dictCapacity = newDictCapacity;
        int t = 0;
        while (t < tempDataSize) {
            _xsIntIntDictReplace(dct, xsArrayGetInt(_intIntDictTempArray, t), xsArrayGetInt(_intIntDictTempArray, t + 1), dictCapacity - 1);
            if ((_cIntIntDictLastOperationStatus < 0) && (_cIntIntDictLastOperationStatus != cIntIntDictNoKeyError)) {
                return (cIntIntDictGenericError);
            }
            t = t + 2;
        }
        _cIntIntDictLastOperationStatus = storeStatus;
    }
    return (cIntIntDictGenericError);
}

int xsIntIntDictCreate() {
    int dct = xsArrayCreateInt(cIntIntDictInitialNumOfBuckets, cIntIntDictEmptyParam);
    xsArraySetInt(dct, 0, 0);
    return (dct);
}

int xsIntIntDict(int k1 = cIntIntDictEmptyParam, int v1 = 0, int k2 = cIntIntDictEmptyParam, int v2 = 0, int k3 = cIntIntDictEmptyParam, int v3 = 0, int k4 = cIntIntDictEmptyParam, int v4 = 0, int k5 = cIntIntDictEmptyParam, int v5 = 0, int k6 = cIntIntDictEmptyParam, int v6 = 0) {
    int dct = xsIntIntDictCreate();
    if (dct < 0) {
        return (cIntIntDictGenericError);
    }
    if (k1 == cIntIntDictEmptyParam) {
        return (dct);
    }
    xsIntIntDictPut(dct, k1, v1);
    if (k2 == cIntIntDictEmptyParam) {
        return (dct);
    }
    xsIntIntDictPut(dct, k2, v2);
    if (k3 == cIntIntDictEmptyParam) {
        return (dct);
    }
    xsIntIntDictPut(dct, k3, v3);
    if (k4 == cIntIntDictEmptyParam) {
        return (dct);
    }
    xsIntIntDictPut(dct, k4, v4);
    if (k5 == cIntIntDictEmptyParam) {
        return (dct);
    }
    xsIntIntDictPut(dct, k5, v5);
    if (k6 == cIntIntDictEmptyParam) {
        return (dct);
    }
    xsIntIntDictPut(dct, k6, v6);
    return (dct);
}

int xsIntIntDictGet(int dct = -1, int key = -1, int dft = -1) {
    int dictCapacity = xsArrayGetSize(dct);
    int hash = _xsIntIntDictHash(key, dictCapacity - 1);
    int bucket = xsArrayGetInt(dct, hash);
    if (bucket < 0) {
        _cIntIntDictLastOperationStatus = cIntIntDictNoKeyError;
        return (dft);
    }
    int bucketSize = xsArrayGetInt(bucket, 0);
    int j = 1;
    while (j <= bucketSize) {
        int storedKey = xsArrayGetInt(bucket, j);
        if (key == storedKey) {
            _cIntIntDictLastOperationStatus = cIntIntDictSuccess;
            return (xsArrayGetInt(bucket, j + 1));
        }
        j = j + 2;
    }
    _cIntIntDictLastOperationStatus = cIntIntDictNoKeyError;
    return (dft);
}

int xsIntIntDictRemove(int dct = -1, int key = -1) {
    int totalSize = xsArrayGetInt(dct, 0);
    int dictCapacity = xsArrayGetSize(dct);
    int hash = _xsIntIntDictHash(key, dictCapacity - 1);
    int bucket = xsArrayGetInt(dct, hash);
    if (bucket < 0) {
        _cIntIntDictLastOperationStatus = cIntIntDictNoKeyError;
        return (cIntIntDictGenericError);
    }
    bool found = false;
    int foundValue = cIntIntDictGenericError;
    int bucketSize = xsArrayGetInt(bucket, 0);
    int j = 1;
    while (j <= bucketSize) {
        int storedKey = xsArrayGetInt(bucket, j);
        if (found) {
            xsArraySetInt(bucket, j - 2, storedKey);
            xsArraySetInt(bucket, j - 1, xsArrayGetInt(bucket, j + 1));
        } else if (storedKey == key) {
            found = true;
            foundValue = xsArrayGetInt(bucket, j + 1);
            xsArraySetInt(bucket, 0, bucketSize - 2);
            xsArraySetInt(dct, 0, totalSize - 1);
        }
        j = j + 2;
    }
    int bucketCapacity = xsArrayGetSize(bucket);
    if (found) {
        int sizeThreshold = (bucketCapacity - 1) / 2;
        if ((sizeThreshold >= (bucketSize - 2)) && (bucketCapacity > cIntIntDictMinBucketSize)) {
            int r = xsArrayResizeInt(bucket, sizeThreshold + 1);
            if (r != 0) {
                _cIntIntDictLastOperationStatus = cIntIntDictResizeFailedError;
                return (cIntIntDictGenericError);
            }
        }
        _cIntIntDictLastOperationStatus = cIntIntDictSuccess;
    } else {
        _cIntIntDictLastOperationStatus = cIntIntDictNoKeyError;
    }
    return (foundValue);
}

bool xsIntIntDictContains(int dct = -1, int key = -1) {
    int dictCapacity = xsArrayGetSize(dct);
    int hash = _xsIntIntDictHash(key, dictCapacity - 1);
    int bucket = xsArrayGetInt(dct, hash);
    if (bucket < 0) {
        return (false);
    }
    int bucketSize = xsArrayGetInt(bucket, 0);
    int j = 1;
    while (j <= bucketSize) {
        int storedKey = xsArrayGetInt(bucket, j);
        if (key == storedKey) {
            return (true);
        }
        j = j + 2;
    }
    return (false);
}

int xsIntIntDictSize(int dct = -1) {
    return (xsArrayGetInt(dct, 0));
}

int xsIntIntDictClear(int dct = -1) {
    int dictCapacity = xsArrayGetSize(dct);
    for (i = 1; < dictCapacity) {
        int bucket = xsArrayGetInt(dct, i);
        if (bucket >= 0) {
            xsArraySetInt(bucket, 0, 0);
            int bucketCapacity = xsArrayGetSize(bucket);
            if (bucketCapacity > cIntIntDictMinBucketSize) {
                int r1 = xsArrayResizeInt(bucket, cIntIntDictMinBucketSize);
                if (r1 != 1) {
                    return (cIntIntDictGenericError);
                }
            }
        }
    }
    xsArraySetInt(dct, 0, 0);
    if (dictCapacity > cIntIntDictInitialNumOfBuckets) {
        int r2 = xsArrayResizeInt(dct, cIntIntDictInitialNumOfBuckets);
        if (r2 != 1) {
            return (cIntIntDictGenericError);
        }
    }
    return (cIntIntDictSuccess);
}

int xsIntIntDictCopy(int dct = -1) {
    int dictCapacity = xsArrayGetSize(dct);
    int newDct = xsArrayCreateInt(dictCapacity, cIntIntDictEmptyParam);
    if (newDct < 0) {
        return (cIntIntDictResizeFailedError);
    }
    for (i = 1; < dictCapacity) {
        int bucket = xsArrayGetInt(dct, i);
        if (bucket >= 0) {
            int bucketCapacity = xsArrayGetSize(bucket);
            int bucketSize = xsArrayGetInt(bucket, 0);
            int newBucket = xsArrayCreateInt(bucketCapacity, cIntIntDictEmptyParam);
            if (newBucket < 0) {
                return (cIntIntDictResizeFailedError);
            }
            for (j = 0; <= bucketSize) {
                xsArraySetInt(newBucket, j, xsArrayGetInt(bucket, j));
            }
            xsArraySetInt(newDct, i, newBucket);
        }
    }
    xsArraySetInt(newDct, 0, xsArrayGetInt(dct, 0));
    return (newDct);
}

void xsIntIntDctIteratorStart() {
    _intIntDictIteratorPrevIdx = 0;
    _intIntDictIteratorPrevKey = -1;
}

bool xsIntIntDctIteratorHasNext(int dct = -1) {
    int totalSize = xsArrayGetInt(dct, 0);
    return (_intIntDictIteratorPrevIdx < totalSize);
}

int _xsIntIntDctIteratorNext(int dct = -1, bool returnKey = true) {
    int b = -1;
    int bucket = -1;
    int bucketSize = -1;
    int idx = 1;
    int dictCapacity = xsArrayGetSize(dct);
    bool found = false;
    int storedKey = -1;
    if (_intIntDictIteratorPrevIdx == 0) {
        int i = 1;
        while ((i < dictCapacity) && (found == false)) {
            bucket = xsArrayGetInt(dct, i);
            bucketSize = xsArrayGetInt(bucket, 0);
            if ((bucket >= 0) && (bucketSize > 0)) {
                found = true;
                b = i;
            }
            i++;
        }
    } else {
        int hash = _xsIntIntDictHash(_intIntDictIteratorPrevKey, dictCapacity - 1);
        bucket = xsArrayGetInt(dct, hash);
        bucketSize = xsArrayGetInt(bucket, 0);
        int j = 1;
        while ((j <= bucketSize) && (found == false)) {
            storedKey = xsArrayGetInt(bucket, j);
            if (_intIntDictIteratorPrevKey == storedKey) {
                idx = j + 2;
                b = hash;
                found = true;
            }
            j = j + 2;
        }
    }
    if (found == false) {
        _intIntDictIteratorPrevIdx = cIntIntDictMaxCapacity;
        _cIntIntDictLastOperationStatus = cIntIntDictGenericError;
        return (cIntIntDictGenericError);
    }
    for (k = b; < dictCapacity) {
        if (found) {
            found = false;
        } else {
            bucket = xsArrayGetInt(dct, k);
            bucketSize = xsArrayGetInt(bucket, 0);
        }
        if (bucket >= 0) {
            int l = idx;
            while (l < bucketSize) {
                storedKey = xsArrayGetInt(bucket, l);
                _cIntIntDictLastOperationStatus = cIntIntDictSuccess;
                _intIntDictIteratorPrevIdx++;
                _intIntDictIteratorPrevKey = storedKey;
                if (returnKey) {
                    return (storedKey);
                } else {
                    return (xsArrayGetInt(bucket, l + 1));
                }
                l = l + 2;
            }
        }
        idx = 1;
    }
    _intIntDictIteratorPrevIdx = cIntIntDictMaxCapacity;
    _cIntIntDictLastOperationStatus = cIntIntDictGenericError;
    return (cIntIntDictGenericError);
}

int xsIntIntDctIteratorNextKey(int dct = -1) {
    return (_xsIntIntDctIteratorNext(dct, true));
}

int xsIntIntDctIteratorNextValue(int dct = -1) {
    return (_xsIntIntDctIteratorNext(dct, false));
}

string xsIntIntDictToString(int dct = -1) {
    int dictSize = xsArrayGetSize(dct);
    string s = "{";
    bool first = true;
    for (i = 1; < dictSize) {
        int bucket = xsArrayGetInt(dct, i);
        if (bucket >= 0) {
            int bucketSize = xsArrayGetInt(bucket, 0);
            int j = 1;
            while (j <= bucketSize) {
                int key = xsArrayGetInt(bucket, j);
                int val = xsArrayGetInt(bucket, j + 1);
                if (first) {
                    first = false;
                } else {
                    s = s + ", ";
                }
                s = s + (key + ": " + val);
                j = j + 2;
            }
        }
    }
    s = s + "}";
    return (s);
}

int xsIntIntDictLastError() {
    return (_cIntIntDictLastOperationStatus);
}

int xsIntIntDictUpdate(int source = -1, int dct = -1) {
    xsIntIntDctIteratorStart();
    while (xsIntIntDctIteratorHasNext(dct)) {
        int key = xsIntIntDctIteratorNextKey(dct);
        int err = xsIntIntDictLastError();
        if (err != 0) {
            return (err);
        }
        int val = xsIntIntDictGet(dct, key);
        err = xsIntIntDictLastError();
        if (err != 0) {
            return (err);
        }
        xsIntIntDictPut(source, key, val);
        err = xsIntIntDictLastError();
        if ((err != 0) && (err != cIntIntDictNoKeyError)) {
            return (err);
        }
        _cIntIntDictLastOperationStatus = cIntIntDictSuccess;
    }
    return (cIntIntDictSuccess);
}

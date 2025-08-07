extern const int cIntIntDictSuccess = 0;
extern const int cIntIntDictGenericError = -1;
extern const int cIntIntDictNoKeyError = -2;
extern const int cIntIntDictResizeFailedError = -3;
extern const int cIntIntDictMaxCapacityError = -4;
extern const int cIntIntDictMaxCapacity = 999999999;
extern const float cIntIntDictMaxLoadFactor = 0.75;
extern const int cIntIntDictEmptyParam = -999999999;
extern const int cIntIntDictInitialNumOfBuckets = 49;
extern const int cIntIntDictInitialBucketSize = 4;
extern const int cIntIntDictMinBucketSize = 2;
extern const int cIntIntDictHashConstant = 16777619;
int _intIntDictLastOperationStatus = cIntIntDictSuccess;
int _intIntDictTempArray = -1;

int _xsIntIntDictHash(int key = -1, int capacity = 0) {
    int hash = key * cIntIntDictHashConstant;
    int numOfBuckets = (capacity - 1) / 3;
    hash = hash % numOfBuckets;
    if (hash < 0) {
        hash = hash + numOfBuckets;
    }
    return ((hash * 3) + 1);
}

int _xsIntIntDictReplace(int dct = -1, int key = -1, int val = 0, int capacity = 0) {
    int hash = _xsIntIntDictHash(key, capacity);
    int bucketType = xsArrayGetInt(dct, hash);
    int bucketArr = 0;
    int storedKey = 0;
    int storedVal = 0;
    if (bucketType == 0) {
        xsArraySetInt(dct, hash, 1);
        xsArraySetInt(dct, hash + 1, key);
        xsArraySetInt(dct, hash + 2, val);
        _intIntDictLastOperationStatus = cIntIntDictNoKeyError;
        return (cIntIntDictGenericError);
    } else if (bucketType == 1) {
        storedKey = xsArrayGetInt(dct, hash + 1);
        if (storedKey == key) {
            storedVal = xsArrayGetInt(dct, hash + 2);
            xsArraySetInt(dct, hash + 2, val);
            _intIntDictLastOperationStatus = cIntIntDictSuccess;
            return (storedVal);
        } else {
            bucketArr = xsArrayCreateInt(cIntIntDictInitialBucketSize, 0);
            if (bucketArr < 0) {
                _intIntDictLastOperationStatus = cIntIntDictResizeFailedError;
                return (cIntIntDictGenericError);
            }
            xsArraySetInt(bucketArr, 0, storedKey);
            xsArraySetInt(bucketArr, 1, xsArrayGetInt(dct, hash + 2));
            xsArraySetInt(bucketArr, 2, key);
            xsArraySetInt(bucketArr, 3, val);
            xsArraySetInt(dct, hash, 2);
            xsArraySetInt(dct, hash + 1, bucketArr);
            xsArraySetInt(dct, hash + 2, 4);
            _intIntDictLastOperationStatus = cIntIntDictNoKeyError;
            return (cIntIntDictGenericError);
        }
    } else if (bucketType == 2) {
        bucketArr = xsArrayGetInt(dct, hash + 1);
        int bucketSize = xsArrayGetInt(dct, hash + 2);
        int i = 0;
        while (i < bucketSize) {
            storedKey = xsArrayGetInt(bucketArr, i);
            if (storedKey == key) {
                storedVal = xsArrayGetInt(bucketArr, i + 1);
                xsArraySetInt(bucketArr, i + 1, val);
                _intIntDictLastOperationStatus = cIntIntDictSuccess;
                return (storedVal);
            }
            i = i + 2;
        }
        int bucketCapacity = xsArrayGetSize(bucketArr);
        if ((bucketCapacity - bucketSize) < 2) {
            int newCapacity = bucketCapacity * 2;
            if (newCapacity > cIntIntDictMaxCapacity) {
                _intIntDictLastOperationStatus = cIntIntDictMaxCapacityError;
                return (cIntIntDictGenericError);
            }
            int r = xsArrayResizeInt(bucketArr, newCapacity);
            if (r != 1) {
                _intIntDictLastOperationStatus = cIntIntDictResizeFailedError;
                return (cIntIntDictGenericError);
            }
        }
        xsArraySetInt(bucketArr, bucketSize, key);
        xsArraySetInt(bucketArr, bucketSize + 1, val);
        xsArraySetInt(dct, hash + 2, bucketSize + 2);
        _intIntDictLastOperationStatus = cIntIntDictNoKeyError;
        return (cIntIntDictGenericError);
    }
    _intIntDictLastOperationStatus = cIntIntDictGenericError;
    return (cIntIntDictGenericError);
}

int _xsIntIntDictMoveToTempArray(int dct = -1, int size = 0, int capacity = 0) {
    int tempDataSize = size * 2;
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
    int i = 1;
    while (i < capacity) {
        int bucketType = xsArrayGetInt(dct, i);
        if (bucketType == 1) {
            xsArraySetInt(_intIntDictTempArray, t, xsArrayGetInt(dct, i + 1));
            xsArraySetInt(_intIntDictTempArray, t + 1, xsArrayGetInt(dct, i + 2));
            xsArraySetInt(dct, i, 0);
            t = t + 2;
        } else if (bucketType == 2) {
            int bucketArr = xsArrayGetInt(dct, i + 1);
            int bucketSize = xsArrayGetInt(dct, i + 2);
            int j = 0;
            while (j < bucketSize) {
                int storedKey = xsArrayGetInt(bucketArr, j);
                int storedVal = xsArrayGetInt(bucketArr, j + 1);
                xsArraySetInt(_intIntDictTempArray, t, storedKey);
                xsArraySetInt(_intIntDictTempArray, t + 1, storedVal);
                t = t + 2;
                j = j + 2;
            }
            xsArraySetInt(dct, i + 2, 0);
        }
        i = i + 3;
    }
    return (tempDataSize);
}

void _xsIntIntDictClearArrays(int dct = -1, int capacity = -1, int newCapacity = -1) {
    int i = 1;
    while (i < capacity) {
        int bucketType = xsArrayGetInt(dct, i);
        if (bucketType == 1) {
            xsArraySetInt(dct, i, 0);
        } else if (bucketType == 2) {
            xsArraySetInt(dct, i + 2, 0);
        }
        i = i + 3;
    }
    int j = capacity;
    while (j < newCapacity) {
        xsArraySetInt(dct, j, 0);
        j = j + 3;
    }
}

int xsIntIntDictPut(int dct = -1, int key = -1, int val = 0) {
    int size = xsArrayGetInt(dct, 0);
    int capacity = xsArrayGetSize(dct);
    int previousValue = _xsIntIntDictReplace(dct, key, val, capacity);
    if (_intIntDictLastOperationStatus == cIntIntDictNoKeyError) {
        size++;
        xsArraySetInt(dct, 0, size);
    } else if (_intIntDictLastOperationStatus == cIntIntDictSuccess) {
        return (previousValue);
    } else {
        return (cIntIntDictGenericError);
    }
    float loadFactor = (0.0 + size) / ((capacity - 1) / 3);
    if (loadFactor > cIntIntDictMaxLoadFactor) {
        int storeStatus = _intIntDictLastOperationStatus;
        int tempDataSize = _xsIntIntDictMoveToTempArray(dct, size, capacity);
        if (tempDataSize < 0) {
            _intIntDictLastOperationStatus = tempDataSize;
            return (cIntIntDictGenericError);
        }
        int newCapacity = ((capacity - 1) * 2) + 1;
        if (newCapacity > cIntIntDictMaxCapacity) {
            _intIntDictLastOperationStatus = cIntIntDictResizeFailedError;
            return (cIntIntDictGenericError);
        }
        int r = xsArrayResizeInt(dct, newCapacity);
        if (r != 1) {
            _intIntDictLastOperationStatus = cIntIntDictResizeFailedError;
            return (cIntIntDictGenericError);
        }
        _xsIntIntDictClearArrays(dct, capacity, newCapacity);
        int t = 0;
        while (t < tempDataSize) {
            _xsIntIntDictReplace(dct, xsArrayGetInt(_intIntDictTempArray, t), xsArrayGetInt(_intIntDictTempArray, t + 1), newCapacity);
            if ((_intIntDictLastOperationStatus < 0) && (_intIntDictLastOperationStatus != cIntIntDictNoKeyError)) {
                return (cIntIntDictGenericError);
            }
            t = t + 2;
        }
        _intIntDictLastOperationStatus = storeStatus;
    }
    return (cIntIntDictGenericError);
}

int xsIntIntDictCreate() {
    int dct = xsArrayCreateInt(cIntIntDictInitialNumOfBuckets, 0);
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
    int capacity = xsArrayGetSize(dct);
    int hash = _xsIntIntDictHash(key, capacity);
    int bucketType = xsArrayGetInt(dct, hash);
    if (bucketType == 0) {
        _intIntDictLastOperationStatus = cIntIntDictNoKeyError;
        return (dft);
    } else if (bucketType == 1) {
        if (xsArrayGetInt(dct, hash + 1) == key) {
            _intIntDictLastOperationStatus = cIntIntDictSuccess;
            return (xsArrayGetInt(dct, hash + 2));
        }
        _intIntDictLastOperationStatus = cIntIntDictNoKeyError;
        return (dft);
    } else if (bucketType == 2) {
        int bucketArr = xsArrayGetInt(dct, hash + 1);
        int bucketSize = xsArrayGetInt(dct, hash + 2);
        int j = 0;
        while (j < bucketSize) {
            if (key == xsArrayGetInt(bucketArr, j)) {
                _intIntDictLastOperationStatus = cIntIntDictSuccess;
                return (xsArrayGetInt(bucketArr, j + 1));
            }
            j = j + 2;
        }
    }
    _intIntDictLastOperationStatus = cIntIntDictNoKeyError;
    return (dft);
}

int xsIntIntDictRemove(int dct = -1, int key = -1) {
    int size = xsArrayGetInt(dct, 0);
    int capacity = xsArrayGetSize(dct);
    int hash = _xsIntIntDictHash(key, capacity);
    int bucketType = xsArrayGetInt(dct, hash);
    int storedKey = 0;
    if (bucketType == 0) {
        _intIntDictLastOperationStatus = cIntIntDictNoKeyError;
        return (cIntIntDictGenericError);
    }
    if (bucketType == 1) {
        storedKey = xsArrayGetInt(dct, hash + 1);
        if (storedKey == key) {
            xsArraySetInt(dct, hash, 0);
            xsArraySetInt(dct, 0, size - 1);
            _intIntDictLastOperationStatus = cIntIntDictSuccess;
            return (xsArrayGetInt(dct, hash + 2));
        }
        _intIntDictLastOperationStatus = cIntIntDictNoKeyError;
        return (cIntIntDictGenericError);
    }
    if (bucketType == 2) {
        int bucketArr = xsArrayGetInt(dct, hash + 1);
        int bucketSize = xsArrayGetInt(dct, hash + 2);
        bool found = false;
        int prevValue = 0;
        int i = 0;
        while (i < bucketSize) {
            storedKey = xsArrayGetInt(bucketArr, i);
            if (found) {
                xsArraySetInt(bucketArr, i - 2, storedKey);
                xsArraySetInt(bucketArr, i - 1, xsArrayGetInt(bucketArr, i + 1));
            } else if (storedKey == key) {
                found = true;
                prevValue = xsArrayGetInt(bucketArr, i + 1);
                xsArraySetInt(bucketArr, hash + 2, bucketSize - 2);
                xsArraySetInt(dct, 0, size - 1);
            }
            i = i + 2;
        }
        if (found) {
            _intIntDictLastOperationStatus = cIntIntDictSuccess;
            return (prevValue);
        }
        _intIntDictLastOperationStatus = cIntIntDictNoKeyError;
        return (cIntIntDictGenericError);
    }
    _intIntDictLastOperationStatus = cIntIntDictGenericError;
    return (cIntIntDictGenericError);
}

bool xsIntIntDictContains(int dct = -1, int key = -1) {
    int capacity = xsArrayGetSize(dct);
    int hash = _xsIntIntDictHash(key, capacity);
    int bucketType = xsArrayGetInt(dct, hash);
    if (bucketType == 0) {
        return (false);
    }
    if (bucketType == 1) {
        if (xsArrayGetInt(dct, hash + 1) == key) {
            return (true);
        }
        return (false);
    }
    if (bucketType == 2) {
        int bucketSize = xsArrayGetInt(dct, hash + 2);
        int j = 0;
        while (j < bucketSize) {
            if (key == xsArrayGetInt(dct, j)) {
                return (true);
            }
            j = j + 2;
        }
    }
    return (false);
}

int xsIntIntDictSize(int dct = -1) {
    return (xsArrayGetInt(dct, 0));
}

int xsIntIntDictClear(int dct = -1) {
    int dictCapacity = xsArrayGetSize(dct);
    int i = 1;
    while (i < dictCapacity) {
        int bucketType = xsArrayGetInt(dct, i);
        if (bucketType == 1) {
            xsArraySetInt(dct, i, 0);
        } else if (bucketType == 2) {
            xsArraySetInt(dct, i + 2, 0);
            int bucketArr = xsArrayGetInt(dct, i + 1);
            int bucketCapacity = xsArrayGetSize(bucketArr);
            if (bucketCapacity > cIntIntDictMinBucketSize) {
                int r1 = xsArrayResizeInt(bucketType, cIntIntDictMinBucketSize);
                if (r1 != 1) {
                    return (cIntIntDictGenericError);
                }
            }
        }
        i = i + 3;
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
    int capacity = xsArrayGetSize(dct);
    int newDct = xsArrayCreateInt(capacity, 0);
    if (newDct < 0) {
        return (cIntIntDictResizeFailedError);
    }
    int i = 1;
    while (i < capacity) {
        int bucketType = xsArrayGetInt(dct, i);
        if (bucketType == 1) {
            xsArraySetInt(newDct, i, 1);
            xsArraySetInt(newDct, i + 1, xsArrayGetInt(dct, i + 1));
            xsArraySetInt(newDct, i + 2, xsArrayGetInt(dct, i + 2));
        } else if (bucketType == 2) {
            int bucketArr = xsArrayGetInt(dct, i + 1);
            int bucketSize = xsArrayGetInt(dct, i + 2);
            int bucketCapacity = xsArrayGetSize(bucketArr);
            int newBucketArr = xsArrayCreateInt(bucketCapacity, 0);
            if (newBucketArr < 0) {
                return (cIntIntDictResizeFailedError);
            }
            for (j = 0; < bucketSize) {
                xsArraySetInt(newBucketArr, j, xsArrayGetInt(bucketArr, j));
            }
            xsArraySetInt(newDct, i, 2);
            xsArraySetInt(newDct, i + 1, newBucketArr);
            xsArraySetInt(newDct, i + 2, bucketSize);
        }
        i = i + 3;
    }
    xsArraySetInt(newDct, 0, xsArrayGetInt(dct, 0));
    return (newDct);
}

int _xsIntIntFindNextFromBucket(int bucket = -1, int dct = -1, int dictSize = -1) {
    int i = bucket;
    while (i < dictSize) {
        int bucketType = xsArrayGetInt(dct, i);
        if (bucketType == 1) {
            _intIntDictLastOperationStatus = cIntIntDictSuccess;
            return (xsArrayGetInt(dct, i + 1));
        }
        if ((bucketType == 2) && (xsArrayGetInt(dct, i + 2) > 0)) {
            _intIntDictLastOperationStatus = cIntIntDictSuccess;
            return (xsArrayGetInt(xsArrayGetInt(dct, i + 1), 0));
        }
        i = i + 3;
    }
    _intIntDictLastOperationStatus = cIntIntDictNoKeyError;
    return (cIntIntDictGenericError);
}

int xsIntIntDictNextKey(int dct = -1, bool isFirst = true, int prevKey = -1) {
    int dictSize = xsArrayGetSize(dct);
    if (isFirst) {
        return (_xsIntIntFindNextFromBucket(1, dct, dictSize));
    }
    int hash = _xsIntIntDictHash(prevKey, dictSize);
    int bucketType = xsArrayGetInt(dct, hash);
    if (bucketType == 2) {
        int bucketArr = xsArrayGetInt(dct, hash + 1);
        int bucketSize = xsArrayGetInt(dct, hash + 2);
        int i = 0;
        bool found = false;
        while ((i < bucketSize) && (found == false)) {
            int storedKey = xsArrayGetInt(bucketArr, i);
            if (storedKey == prevKey) {
                if ((i + 2) < bucketSize) {
                    _intIntDictLastOperationStatus = cIntIntDictSuccess;
                    return (xsArrayGetInt(bucketArr, i + 2));
                }
                found = true;
            }
            i = i + 2;
        }
        if (found == false) {
            _intIntDictLastOperationStatus = cIntIntDictNoKeyError;
            return (cIntIntDictGenericError);
        }
    }
    return (_xsIntIntFindNextFromBucket(hash + 3, dct, dictSize));
}

bool xsIntIntDictHasNext(int dct = -1, bool isFirst = true, int prevKey = -1) {
    xsIntIntDictNextKey(dct, isFirst, prevKey);
    bool r = _intIntDictLastOperationStatus != cIntIntDictNoKeyError;
    _intIntDictLastOperationStatus = cIntIntDictSuccess;
    return (r);
}

string xsIntIntDictToString(int dct = -1) {
    int dictSize = xsArrayGetSize(dct);
    string s = "{";
    int key = 0;
    int val = 0;
    bool first = true;
    int i = 1;
    while (i < dictSize) {
        int bucketType = xsArrayGetInt(dct, i);
        if (bucketType == 1) {
            key = xsArrayGetInt(dct, i + 1);
            val = xsArrayGetInt(dct, i + 2);
            if (first) {
                first = false;
            } else {
                s = s + ", ";
            }
            s = s + (key + ": " + val);
        } else if (bucketType == 2) {
            int bucketArr = xsArrayGetInt(dct, i + 1);
            int bucketSize = xsArrayGetInt(dct, i + 2);
            int j = 0;
            while (j < bucketSize) {
                key = xsArrayGetInt(bucketArr, j);
                val = xsArrayGetInt(bucketArr, j + 1);
                if (first) {
                    first = false;
                } else {
                    s = s + ", ";
                }
                s = s + (key + ": " + val);
                j = j + 2;
            }
        }
        i = i + 3;
    }
    s = s + "}";
    return (s);
}

int xsIntIntDictLastError() {
    return (_intIntDictLastOperationStatus);
}

int xsIntIntDictUpdate(int source = -1, int dct = -1) {
    int key = xsIntIntDictNextKey(dct);
    while (xsIntIntDictLastError() != cIntIntDictNoKeyError) {
        int val = xsIntIntDictGet(dct, key);
        int err = xsIntIntDictLastError();
        if (err != 0) {
            return (err);
        }
        xsIntIntDictPut(source, key, val);
        err = xsIntIntDictLastError();
        if ((err != 0) && (err != cIntIntDictNoKeyError)) {
            return (err);
        }
        key = xsIntIntDictNextKey(dct, false, key);
    }
    _intIntDictLastOperationStatus = cIntIntDictSuccess;
    return (cIntIntDictSuccess);
}

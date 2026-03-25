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
int _intIntDictEmptyBucket = 0;
int _intIntDictInlineBucket = 1;
int _intIntDictArrayBucket = 2;
int _intIntDictLastOperationStatus = cIntIntDictSuccess;
int _intIntDictTempArray = -1;

/*
    Creates an empty int-to-int dictionary.
    @return created dict id, or `cIntIntDictGenericError` on error
*/
int xsIntIntDictCreate() {
    int dct = xsArrayCreateInt(cIntIntDictInitialNumOfBuckets, 0);
    xsArraySetInt(dct, 0, 0);
    return (dct);
}

int _xsIntIntDictHash(int key = -1, int capacity = 0) {
    int hash = key * cIntIntDictHashConstant;
    int numOfBuckets = (capacity - 1) / 3;
    hash = hash % numOfBuckets;
    if (hash < 0) {
        hash = hash + numOfBuckets;
    }
    return ((hash * 3) + 1);
}

int _xsIntIntDictFindKeyInArray(int bucketArr = -1, int bucketSize = 0, int key = -1) {
    int i = 0;
    while (i < bucketSize) {
        if (key == xsArrayGetInt(bucketArr, i)) {
            return (i);
        }
        i = i + 2;
    }
    return (-1);
}

int _xsIntIntDictReplace(int dct = -1, int key = -1, int val = 0, int capacity = 0) {
    int hash = _xsIntIntDictHash(key, capacity);
    int bucketType = xsArrayGetInt(dct, hash);
    int bucketArr = 0;
    int storedKey = 0;
    int storedVal = 0;
    if (bucketType == _intIntDictEmptyBucket) {
        xsArraySetInt(dct, hash, _intIntDictInlineBucket);
        xsArraySetInt(dct, hash + 1, key);
        xsArraySetInt(dct, hash + 2, val);
        _intIntDictLastOperationStatus = cIntIntDictNoKeyError;
        return (cIntIntDictGenericError);
    } else if (bucketType == _intIntDictInlineBucket) {
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
            xsArraySetInt(dct, hash, _intIntDictArrayBucket);
            xsArraySetInt(dct, hash + 1, bucketArr);
            xsArraySetInt(dct, hash + 2, 4);
            _intIntDictLastOperationStatus = cIntIntDictNoKeyError;
            return (cIntIntDictGenericError);
        }
    } else if (bucketType == _intIntDictArrayBucket) {
        bucketArr = xsArrayGetInt(dct, hash + 1);
        int bucketSize = xsArrayGetInt(dct, hash + 2);
        int foundIdx = _xsIntIntDictFindKeyInArray(bucketArr, bucketSize, key);
        if (foundIdx >= 0) {
            storedVal = xsArrayGetInt(bucketArr, foundIdx + 1);
            xsArraySetInt(bucketArr, foundIdx + 1, val);
            _intIntDictLastOperationStatus = cIntIntDictSuccess;
            return (storedVal);
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
        if (bucketType == _intIntDictInlineBucket) {
            xsArraySetInt(_intIntDictTempArray, t, xsArrayGetInt(dct, i + 1));
            xsArraySetInt(_intIntDictTempArray, t + 1, xsArrayGetInt(dct, i + 2));
            xsArraySetInt(dct, i, _intIntDictEmptyBucket);
            t = t + 2;
        } else if (bucketType == _intIntDictArrayBucket) {
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
    int j = capacity;
    while (j < newCapacity) {
        xsArraySetInt(dct, j, _intIntDictEmptyBucket);
        j = j + 3;
    }
}

int _xsIntIntDictRehashIfNeeded(int dct = -1, int size = 0, int capacity = 0) {
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
    return (cIntIntDictSuccess);
}

/*
    Inserts or updates a key-value pair. Triggers a rehash when load factor exceeds the threshold. Sets last error on completion.
    @param dct - dict id
    @param key - key to insert or update
    @param val - value to associate with the key
    @return previous value if the key already existed, or `cIntIntDictGenericError` if newly inserted or on error.
        Because -1 is both the error sentinel and a valid previous value, callers must check
        `xs_int_int_dict_last_error()` to distinguish - `cIntIntDictSuccess` means the key
        existed and the returned value is valid; `cIntIntDictNoKeyError` means a new key
        was inserted; any other negative status indicates an error.
*/
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
    _xsIntIntDictRehashIfNeeded(dct, size, capacity);
    return (cIntIntDictGenericError);
}

/*
    Creates a dict with provided key-value pairs. The first key that equals `cIntIntDictEmptyParam` will stop further insertion.
    This function can create a dict with 6 entries at the maximum, but further entries can be added with `xsIntIntDictPut`.
    @param k1 through k6 - key at a given position
    @param v1 through v6 - value associated with the corresponding key
    @return created dict id, or `cIntIntDictGenericError` on error
*/
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

/*
    Returns the value associated with the given key. Sets last error on completion.
    @param dct - dict id
    @param key - key to look up
    @param dft - default value returned if the key is not found
    @return value for the key, or `dft` if not found
*/
int xsIntIntDictGet(int dct = -1, int key = -1, int dft = -1) {
    int capacity = xsArrayGetSize(dct);
    int hash = _xsIntIntDictHash(key, capacity);
    int bucketType = xsArrayGetInt(dct, hash);
    if (bucketType == _intIntDictEmptyBucket) {
        _intIntDictLastOperationStatus = cIntIntDictNoKeyError;
        return (dft);
    } else if (bucketType == _intIntDictInlineBucket) {
        if (xsArrayGetInt(dct, hash + 1) == key) {
            _intIntDictLastOperationStatus = cIntIntDictSuccess;
            return (xsArrayGetInt(dct, hash + 2));
        }
        _intIntDictLastOperationStatus = cIntIntDictNoKeyError;
        return (dft);
    } else if (bucketType == _intIntDictArrayBucket) {
        int bucketArr = xsArrayGetInt(dct, hash + 1);
        int bucketSize = xsArrayGetInt(dct, hash + 2);
        int foundIdx = _xsIntIntDictFindKeyInArray(bucketArr, bucketSize, key);
        if (foundIdx >= 0) {
            _intIntDictLastOperationStatus = cIntIntDictSuccess;
            return (xsArrayGetInt(bucketArr, foundIdx + 1));
        }
    }
    _intIntDictLastOperationStatus = cIntIntDictNoKeyError;
    return (dft);
}

/*
    Removes the entry with the given key from the dict. Sets last error on completion.
    @param dct - dict id
    @param key - key to remove
    @return value that was associated with the key, or `cIntIntDictGenericError` if not found
*/
int xsIntIntDictRemove(int dct = -1, int key = -1) {
    int size = xsArrayGetInt(dct, 0);
    int capacity = xsArrayGetSize(dct);
    int hash = _xsIntIntDictHash(key, capacity);
    int bucketType = xsArrayGetInt(dct, hash);
    int storedKey = 0;
    if (bucketType == _intIntDictEmptyBucket) {
        _intIntDictLastOperationStatus = cIntIntDictNoKeyError;
        return (cIntIntDictGenericError);
    }
    if (bucketType == _intIntDictInlineBucket) {
        storedKey = xsArrayGetInt(dct, hash + 1);
        if (storedKey == key) {
            xsArraySetInt(dct, hash, _intIntDictEmptyBucket);
            xsArraySetInt(dct, 0, size - 1);
            _intIntDictLastOperationStatus = cIntIntDictSuccess;
            return (xsArrayGetInt(dct, hash + 2));
        }
        _intIntDictLastOperationStatus = cIntIntDictNoKeyError;
        return (cIntIntDictGenericError);
    }
    if (bucketType == _intIntDictArrayBucket) {
        int bucketArr = xsArrayGetInt(dct, hash + 1);
        int bucketSize = xsArrayGetInt(dct, hash + 2);
        int foundIdx = _xsIntIntDictFindKeyInArray(bucketArr, bucketSize, key);
        if (foundIdx >= 0) {
            int prevValue = xsArrayGetInt(bucketArr, foundIdx + 1);
            int i = foundIdx + 2;
            while (i < bucketSize) {
                xsArraySetInt(bucketArr, i - 2, xsArrayGetInt(bucketArr, i));
                xsArraySetInt(bucketArr, i - 1, xsArrayGetInt(bucketArr, i + 1));
                i = i + 2;
            }
            xsArraySetInt(dct, hash + 2, bucketSize - 2);
            xsArraySetInt(dct, 0, size - 1);
            _intIntDictLastOperationStatus = cIntIntDictSuccess;
            return (prevValue);
        }
        _intIntDictLastOperationStatus = cIntIntDictNoKeyError;
        return (cIntIntDictGenericError);
    }
    _intIntDictLastOperationStatus = cIntIntDictGenericError;
    return (cIntIntDictGenericError);
}

/*
    Checks whether the dict contains the given key.
    @param dct - dict id
    @param key - key to search for
    @return true if the key is found, false otherwise
*/
bool xsIntIntDictContains(int dct = -1, int key = -1) {
    int capacity = xsArrayGetSize(dct);
    int hash = _xsIntIntDictHash(key, capacity);
    int bucketType = xsArrayGetInt(dct, hash);
    if (bucketType == _intIntDictEmptyBucket) {
        return (false);
    }
    if (bucketType == _intIntDictInlineBucket) {
        return (xsArrayGetInt(dct, hash + 1) == key);
    }
    if (bucketType == _intIntDictArrayBucket) {
        int bucketArr = xsArrayGetInt(dct, hash + 1);
        int bucketSize = xsArrayGetInt(dct, hash + 2);
        return (_xsIntIntDictFindKeyInArray(bucketArr, bucketSize, key) >= 0);
    }
    return (false);
}

/*
    Returns the number of key-value pairs in the dict.
    @param dct - dict id
    @return dict size
*/
int xsIntIntDictSize(int dct = -1) {
    return (xsArrayGetInt(dct, 0));
}

/*
    Removes all entries from the dict and shrinks the backing arrays.
    @param dct - dict id
    @return `cIntIntDictSuccess` on success, or `cIntIntDictGenericError` on error
*/
int xsIntIntDictClear(int dct = -1) {
    int dictCapacity = xsArrayGetSize(dct);
    int i = 1;
    while (i < dictCapacity) {
        int bucketType = xsArrayGetInt(dct, i);
        if (bucketType == _intIntDictInlineBucket) {
            xsArraySetInt(dct, i, _intIntDictEmptyBucket);
        } else if (bucketType == _intIntDictArrayBucket) {
            xsArraySetInt(dct, i + 2, 0);
            int bucketArr = xsArrayGetInt(dct, i + 1);
            int bucketCapacity = xsArrayGetSize(bucketArr);
            if (bucketCapacity > cIntIntDictMinBucketSize) {
                int r1 = xsArrayResizeInt(bucketArr, cIntIntDictMinBucketSize);
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

/*
    Returns a deep copy of the dict.
    @param dct - dict id
    @return new dict id, or `cIntIntDictResizeFailedError` on error
*/
int xsIntIntDictCopy(int dct = -1) {
    int capacity = xsArrayGetSize(dct);
    int newDct = xsArrayCreateInt(capacity, 0);
    if (newDct < 0) {
        return (cIntIntDictResizeFailedError);
    }
    int i = 1;
    while (i < capacity) {
        int bucketType = xsArrayGetInt(dct, i);
        if (bucketType == _intIntDictInlineBucket) {
            xsArraySetInt(newDct, i, _intIntDictInlineBucket);
            xsArraySetInt(newDct, i + 1, xsArrayGetInt(dct, i + 1));
            xsArraySetInt(newDct, i + 2, xsArrayGetInt(dct, i + 2));
        } else if (bucketType == _intIntDictArrayBucket) {
            int bucketArr = xsArrayGetInt(dct, i + 1);
            int bucketSize = xsArrayGetInt(dct, i + 2);
            if (bucketSize > 0) {
                int bucketCapacity = xsArrayGetSize(bucketArr);
                int newBucketArr = xsArrayCreateInt(bucketCapacity, 0);
                if (newBucketArr < 0) {
                    return (cIntIntDictResizeFailedError);
                }
                for (j = 0; < bucketSize) {
                    xsArraySetInt(newBucketArr, j, xsArrayGetInt(bucketArr, j));
                }
                xsArraySetInt(newDct, i, _intIntDictArrayBucket);
                xsArraySetInt(newDct, i + 1, newBucketArr);
                xsArraySetInt(newDct, i + 2, bucketSize);
            }
        }
        i = i + 3;
    }
    xsArraySetInt(newDct, 0, xsArrayGetInt(dct, 0));
    return (newDct);
}

/*
    Returns a string representation of the dict in the format `{k1 - v1, k2 - v2, ...}`.
    @param dct - dict id
    @return string representation of the dict
*/
string xsIntIntDictToString(int dct = -1) {
    int dictSize = xsArrayGetSize(dct);
    string s = "{";
    int key = 0;
    int val = 0;
    bool first = true;
    int i = 1;
    while (i < dictSize) {
        int bucketType = xsArrayGetInt(dct, i);
        if (bucketType == _intIntDictInlineBucket) {
            key = xsArrayGetInt(dct, i + 1);
            val = xsArrayGetInt(dct, i + 2);
            if (first) {
                first = false;
            } else {
                s = s + ", ";
            }
            s = s + (key + ": " + val);
        } else if (bucketType == _intIntDictArrayBucket) {
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

/*
    Returns the status code of the last operation that sets it (put, get, remove, next_key, has_next).
    @return `cIntIntDictSuccess` if the last such operation succeeded, or a negative error code
*/
int xsIntIntDictLastError() {
    return (_intIntDictLastOperationStatus);
}

int _xsIntIntFindNextFromBucket(int bucket = -1, int dct = -1, int dictSize = -1) {
    int i = bucket;
    while (i < dictSize) {
        int bucketType = xsArrayGetInt(dct, i);
        if (bucketType == _intIntDictInlineBucket) {
            _intIntDictLastOperationStatus = cIntIntDictSuccess;
            return (xsArrayGetInt(dct, i + 1));
        }
        if ((bucketType == _intIntDictArrayBucket) && (xsArrayGetInt(dct, i + 2) > 0)) {
            _intIntDictLastOperationStatus = cIntIntDictSuccess;
            return (xsArrayGetInt(xsArrayGetInt(dct, i + 1), 0));
        }
        i = i + 3;
    }
    _intIntDictLastOperationStatus = cIntIntDictNoKeyError;
    return (cIntIntDictGenericError);
}

/*
    Returns the next key in the dict for stateless iteration. Sets last error on completion.
    @param dct - dict id
    @param is_first - if true, returns the first key in the dict
    @param prev_key - the previous key returned by this function (ignored if `isFirst` is true)
    @return next key, or `cIntIntDictGenericError` if no more keys (last error set to `cIntIntDictNoKeyError`)
*/
int xsIntIntDictNextKey(int dct = -1, bool isFirst = true, int prevKey = -1) {
    int dictSize = xsArrayGetSize(dct);
    if (isFirst) {
        return (_xsIntIntFindNextFromBucket(1, dct, dictSize));
    }
    int hash = _xsIntIntDictHash(prevKey, dictSize);
    int bucketType = xsArrayGetInt(dct, hash);
    if (bucketType == _intIntDictArrayBucket) {
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

/*
    Checks whether there is a next key in the dict for stateless iteration.
    @param dct - dict id
    @param is_first - if true, checks whether the dict has any keys
    @param prev_key - the previous key (ignored if `isFirst` is true)
    @return true if there is a next key, false otherwise
*/
bool xsIntIntDictHasNext(int dct = -1, bool isFirst = true, int prevKey = -1) {
    xsIntIntDictNextKey(dct, isFirst, prevKey);
    bool r = _intIntDictLastOperationStatus != cIntIntDictNoKeyError;
    _intIntDictLastOperationStatus = cIntIntDictSuccess;
    return (r);
}

/*
    Inserts all key-value pairs from another dict into the source dict, overwriting existing keys.
    @param source - dict id to update
    @param dct - dict id whose entries are copied into source
    @return `cIntIntDictSuccess` on success, or a negative error code
*/
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

/*
    Inserts the key-value pair only if the key is not already present. Sets last error on completion.
    @param dct - dict id
    @param key - key to insert
    @param val - value to associate with the key
    @return existing value if the key was already present, or `cIntIntDictGenericError` if newly inserted or on error.
        Callers must check `xs_int_int_dict_last_error()` to distinguish - `cIntIntDictSuccess` means the key
        already existed and the returned value is the existing one; `cIntIntDictNoKeyError` means a new key
        was inserted; any other negative status indicates an error.
*/
int xsIntIntDictPutIfAbsent(int dct = -1, int key = -1, int val = 0) {
    int size = xsArrayGetInt(dct, 0);
    int capacity = xsArrayGetSize(dct);
    int hash = _xsIntIntDictHash(key, capacity);
    int bucketType = xsArrayGetInt(dct, hash);
    int bucketArr = 0;
    if (bucketType == _intIntDictEmptyBucket) {
        xsArraySetInt(dct, hash, _intIntDictInlineBucket);
        xsArraySetInt(dct, hash + 1, key);
        xsArraySetInt(dct, hash + 2, val);
        _intIntDictLastOperationStatus = cIntIntDictNoKeyError;
    } else if (bucketType == _intIntDictInlineBucket) {
        if (xsArrayGetInt(dct, hash + 1) == key) {
            _intIntDictLastOperationStatus = cIntIntDictSuccess;
            return (xsArrayGetInt(dct, hash + 2));
        }
        bucketArr = xsArrayCreateInt(cIntIntDictInitialBucketSize, 0);
        if (bucketArr < 0) {
            _intIntDictLastOperationStatus = cIntIntDictResizeFailedError;
            return (cIntIntDictGenericError);
        }
        xsArraySetInt(bucketArr, 0, xsArrayGetInt(dct, hash + 1));
        xsArraySetInt(bucketArr, 1, xsArrayGetInt(dct, hash + 2));
        xsArraySetInt(bucketArr, 2, key);
        xsArraySetInt(bucketArr, 3, val);
        xsArraySetInt(dct, hash, _intIntDictArrayBucket);
        xsArraySetInt(dct, hash + 1, bucketArr);
        xsArraySetInt(dct, hash + 2, 4);
        _intIntDictLastOperationStatus = cIntIntDictNoKeyError;
    } else if (bucketType == _intIntDictArrayBucket) {
        bucketArr = xsArrayGetInt(dct, hash + 1);
        int bucketSize = xsArrayGetInt(dct, hash + 2);
        int foundIdx = _xsIntIntDictFindKeyInArray(bucketArr, bucketSize, key);
        if (foundIdx >= 0) {
            _intIntDictLastOperationStatus = cIntIntDictSuccess;
            return (xsArrayGetInt(bucketArr, foundIdx + 1));
        }
        int bucketCapacity = xsArrayGetSize(bucketArr);
        if ((bucketCapacity - bucketSize) < 2) {
            int newBucketCapacity = bucketCapacity * 2;
            if (newBucketCapacity > cIntIntDictMaxCapacity) {
                _intIntDictLastOperationStatus = cIntIntDictMaxCapacityError;
                return (cIntIntDictGenericError);
            }
            int r = xsArrayResizeInt(bucketArr, newBucketCapacity);
            if (r != 1) {
                _intIntDictLastOperationStatus = cIntIntDictResizeFailedError;
                return (cIntIntDictGenericError);
            }
        }
        xsArraySetInt(bucketArr, bucketSize, key);
        xsArraySetInt(bucketArr, bucketSize + 1, val);
        xsArraySetInt(dct, hash + 2, bucketSize + 2);
        _intIntDictLastOperationStatus = cIntIntDictNoKeyError;
    } else {
        _intIntDictLastOperationStatus = cIntIntDictGenericError;
        return (cIntIntDictGenericError);
    }
    size++;
    xsArraySetInt(dct, 0, size);
    _xsIntIntDictRehashIfNeeded(dct, size, capacity);
    return (cIntIntDictGenericError);
}

/*
    Returns a new int array containing all keys in the dict. Order is arbitrary.
    @param dct - dict id
    @return array id, or `cIntIntDictResizeFailedError` on allocation failure
*/
int xsIntIntDictKeys(int dct = -1) {
    int size = xsArrayGetInt(dct, 0);
    int arr = xsArrayCreateInt(size, 0);
    if (arr < 0) {
        return (cIntIntDictResizeFailedError);
    }
    int capacity = xsArrayGetSize(dct);
    int idx = 0;
    int i = 1;
    while (i < capacity) {
        int bucketType = xsArrayGetInt(dct, i);
        if (bucketType == _intIntDictInlineBucket) {
            xsArraySetInt(arr, idx, xsArrayGetInt(dct, i + 1));
            idx++;
        } else if (bucketType == _intIntDictArrayBucket) {
            int bucketArr = xsArrayGetInt(dct, i + 1);
            int bucketSize = xsArrayGetInt(dct, i + 2);
            int j = 0;
            while (j < bucketSize) {
                xsArraySetInt(arr, idx, xsArrayGetInt(bucketArr, j));
                idx++;
                j = j + 2;
            }
        }
        i = i + 3;
    }
    return (arr);
}

/*
    Returns a new int array containing all values in the dict. Order matches `xsIntIntDictKeys`.
    @param dct - dict id
    @return array id, or `cIntIntDictResizeFailedError` on allocation failure
*/
int xsIntIntDictValues(int dct = -1) {
    int size = xsArrayGetInt(dct, 0);
    int arr = xsArrayCreateInt(size, 0);
    if (arr < 0) {
        return (cIntIntDictResizeFailedError);
    }
    int capacity = xsArrayGetSize(dct);
    int idx = 0;
    int i = 1;
    while (i < capacity) {
        int bucketType = xsArrayGetInt(dct, i);
        if (bucketType == _intIntDictInlineBucket) {
            xsArraySetInt(arr, idx, xsArrayGetInt(dct, i + 2));
            idx++;
        } else if (bucketType == _intIntDictArrayBucket) {
            int bucketArr = xsArrayGetInt(dct, i + 1);
            int bucketSize = xsArrayGetInt(dct, i + 2);
            int j = 0;
            while (j < bucketSize) {
                xsArraySetInt(arr, idx, xsArrayGetInt(bucketArr, j + 1));
                idx++;
                j = j + 2;
            }
        }
        i = i + 3;
    }
    return (arr);
}

/*
    Returns true if both dicts contain the same key-value pairs.
    @param a - first dict id
    @param b - second dict id
    @return true if both dicts are equal, false otherwise
*/
bool xsIntIntDictEquals(int a = -1, int b = -1) {
    int sizeA = xsArrayGetInt(a, 0);
    int sizeB = xsArrayGetInt(b, 0);
    if (sizeA != sizeB) {
        return (false);
    }
    int capacity = xsArrayGetSize(a);
    int i = 1;
    while (i < capacity) {
        int bucketType = xsArrayGetInt(a, i);
        if (bucketType == _intIntDictInlineBucket) {
            int key = xsArrayGetInt(a, i + 1);
            int val = xsArrayGetInt(a, i + 2);
            if (xsIntIntDictGet(b, key) != val) {
                return (false);
            }
            if (xsIntIntDictLastError() != cIntIntDictSuccess) {
                return (false);
            }
        } else if (bucketType == _intIntDictArrayBucket) {
            int bucketArr = xsArrayGetInt(a, i + 1);
            int bucketSize = xsArrayGetInt(a, i + 2);
            int j = 0;
            while (j < bucketSize) {
                key = xsArrayGetInt(bucketArr, j);
                val = xsArrayGetInt(bucketArr, j + 1);
                if (xsIntIntDictGet(b, key) != val) {
                    return (false);
                }
                if (xsIntIntDictLastError() != cIntIntDictSuccess) {
                    return (false);
                }
                j = j + 2;
            }
        }
        i = i + 3;
    }
    return (true);
}

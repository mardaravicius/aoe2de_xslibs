extern const int cFloatIntDictSuccess = 0;
extern const int cFloatIntDictGenericError = -1;
extern const float cFloatIntDictGenericErrorFloat = -1.0;
extern const int cFloatIntDictNoKeyError = -2;
extern const int cFloatIntDictResizeFailedError = -3;
extern const int cFloatIntDictMaxCapacityError = -4;
extern const int cFloatIntDictMaxCapacity = 999999999;
extern const float cFloatIntDictMaxLoadFactor = 0.75;
extern const float cFloatIntDictEmptyKey = -9999999.0;
extern const int cFloatIntDictEmptyKeyBits = -887581057;
extern const int cFloatIntDictCanonicalNanBits = -8388607;
extern const int cFloatIntDictInitialCapacity = 33;
extern const int cFloatIntDictHashConstant = 16777619;
int _floatIntDictLastOperationStatus = cFloatIntDictSuccess;
int _floatIntDictTempArray = -1;

int _xsFloatIntDictKeyBits(float key = 0.0) {
    if (key != key) {
        return (cFloatIntDictCanonicalNanBits);
    }
    if (key == 0.0) {
        return (0);
    }
    return (bitCastToInt(key));
}

/*
    Creates an empty float-to-int dictionary.
    Keys equal to `cFloatIntDictEmptyKey` (-9999999.0) are reserved as the internal empty-slot
    sentinel and cannot be stored. `put` and `putIfAbsent` silently reject them. Signed zero keys
    are canonicalized to `0.0`, and all NaN keys are canonicalized to a single NaN bit pattern.
    @return created dict id, or `cFloatIntDictGenericError` on error
*/
int xsFloatIntDictCreate() {
    int dct = xsArrayCreateInt(cFloatIntDictInitialCapacity, cFloatIntDictEmptyKeyBits);
    if (dct < 0) {
        return (cFloatIntDictGenericError);
    }
    xsArraySetInt(dct, 0, 0);
    return (dct);
}

int _xsFloatIntDictHash(float key = 0.0, int capacity = 0) {
    int h = _xsFloatIntDictKeyBits(key) * cFloatIntDictHashConstant;
    int numSlots = (capacity - 1) / 2;
    h = h % numSlots;
    if (h < 0) {
        h = h + numSlots;
    }
    return ((h * 2) + 1);
}

/*
    Returns array index of slot containing key, or -1 if not found.
*/
int _xsFloatIntDictFindSlot(int dct = -1, float key = 0.0, int capacity = 0) {
    int keyBits = _xsFloatIntDictKeyBits(key);
    int numSlots = (capacity - 1) / 2;
    int home = _xsFloatIntDictHash(key, capacity);
    int slot = home;
    int steps = 0;
    while (steps < numSlots) {
        int storedKeyBits = xsArrayGetInt(dct, slot);
        if (storedKeyBits == cFloatIntDictEmptyKeyBits) {
            return (-1);
        }
        if (storedKeyBits == keyBits) {
            return (slot);
        }
        slot = slot + 2;
        if (slot >= capacity) {
            slot = 1;
        }
        steps++;
    }
    return (-1);
}

int _xsFloatIntDictUpsert(int dct = -1, float key = 0.0, int val = 0, int capacity = 0) {
    int keyBits = _xsFloatIntDictKeyBits(key);
    int numSlots = (capacity - 1) / 2;
    int home = _xsFloatIntDictHash(key, capacity);
    int slot = home;
    int steps = 0;
    while (steps < numSlots) {
        int storedKeyBits = xsArrayGetInt(dct, slot);
        if (storedKeyBits == cFloatIntDictEmptyKeyBits) {
            xsArraySetInt(dct, slot, keyBits);
            xsArraySetInt(dct, slot + 1, val);
            _floatIntDictLastOperationStatus = cFloatIntDictNoKeyError;
            return (cFloatIntDictGenericError);
        }
        if (storedKeyBits == keyBits) {
            int oldVal = xsArrayGetInt(dct, slot + 1);
            xsArraySetInt(dct, slot + 1, val);
            _floatIntDictLastOperationStatus = cFloatIntDictSuccess;
            return (oldVal);
        }
        slot = slot + 2;
        if (slot >= capacity) {
            slot = 1;
        }
        steps++;
    }
    _floatIntDictLastOperationStatus = cFloatIntDictMaxCapacityError;
    return (cFloatIntDictGenericError);
}

int _xsFloatIntDictMoveToTempArray(int dct = -1, int size = 0, int capacity = 0) {
    int tempDataSize = size * 2;
    if (_floatIntDictTempArray < 0) {
        _floatIntDictTempArray = xsArrayCreateInt(tempDataSize, cFloatIntDictEmptyKeyBits);
        if (_floatIntDictTempArray < 0) {
            return (cFloatIntDictResizeFailedError);
        }
    } else {
        int tempArrCapacity = xsArrayGetSize(_floatIntDictTempArray);
        if (tempArrCapacity < tempDataSize) {
            if (tempDataSize > cFloatIntDictMaxCapacity) {
                return (cFloatIntDictMaxCapacityError);
            }
            int r = xsArrayResizeInt(_floatIntDictTempArray, tempDataSize);
            if (r != 1) {
                return (cFloatIntDictResizeFailedError);
            }
        }
    }
    int t = 0;
    int i = 1;
    while (i < capacity) {
        int storedKeyBits = xsArrayGetInt(dct, i);
        if (storedKeyBits != cFloatIntDictEmptyKeyBits) {
            xsArraySetInt(_floatIntDictTempArray, t, storedKeyBits);
            xsArraySetInt(_floatIntDictTempArray, t + 1, xsArrayGetInt(dct, i + 1));
            t = t + 2;
        }
        i = i + 2;
    }
    return (tempDataSize);
}

void _xsFloatIntDictClearSlots(int dct = -1, int capacity = -1) {
    int j = 1;
    while (j < capacity) {
        xsArraySetInt(dct, j, cFloatIntDictEmptyKeyBits);
        j = j + 2;
    }
}

int _xsFloatIntDictRehashIfNeeded(int dct = -1, int size = 0, int capacity = 0, int requiredSize = -1) {
    if (requiredSize < 0) {
        requiredSize = size;
    }
    float loadFactor = (0.0 + requiredSize) / ((capacity - 1) / 2);
    if (loadFactor > cFloatIntDictMaxLoadFactor) {
        int storeStatus = _floatIntDictLastOperationStatus;
        int newCapacity = ((capacity - 1) * 2) + 1;
        if (newCapacity > cFloatIntDictMaxCapacity) {
            _floatIntDictLastOperationStatus = cFloatIntDictMaxCapacityError;
            return (cFloatIntDictGenericError);
        }
        int tempDataSize = _xsFloatIntDictMoveToTempArray(dct, size, capacity);
        if (tempDataSize < 0) {
            _floatIntDictLastOperationStatus = tempDataSize;
            return (cFloatIntDictGenericError);
        }
        int r = xsArrayResizeInt(dct, newCapacity);
        if (r != 1) {
            _floatIntDictLastOperationStatus = cFloatIntDictResizeFailedError;
            return (cFloatIntDictGenericError);
        }
        _xsFloatIntDictClearSlots(dct, newCapacity);
        int t = 0;
        while (t < tempDataSize) {
            _xsFloatIntDictUpsert(dct, bitCastToFloat(xsArrayGetInt(_floatIntDictTempArray, t)), xsArrayGetInt(_floatIntDictTempArray, t + 1), newCapacity);
            if ((_floatIntDictLastOperationStatus < 0) && (_floatIntDictLastOperationStatus != cFloatIntDictNoKeyError)) {
                return (cFloatIntDictGenericError);
            }
            t = t + 2;
        }
        _floatIntDictLastOperationStatus = storeStatus;
    }
    return (cFloatIntDictSuccess);
}

/*
    Inserts or updates a key-value pair. Triggers a rehash when load factor exceeds the threshold.
    Sets last error on completion.
    If `key` equals `cFloatIntDictEmptyKey`, the call is a no-op and returns `cFloatIntDictGenericError`
    with last error set to `cFloatIntDictGenericError`.
    @return previous value if the key already existed, or `cFloatIntDictGenericError` if newly inserted or on error.
        Because -1 is both the error sentinel and a valid previous value, callers must check
        `xs_float_int_dict_last_error()` to distinguish - `cFloatIntDictSuccess` means the key
        existed and the returned value is valid; `cFloatIntDictNoKeyError` means a new key
        was inserted; any other negative status indicates an error.
*/
int xsFloatIntDictPut(int dct = -1, float key = 0.0, int val = 0) {
    if (key == cFloatIntDictEmptyKey) {
        _floatIntDictLastOperationStatus = cFloatIntDictGenericError;
        return (cFloatIntDictGenericError);
    }
    int size = xsArrayGetInt(dct, 0);
    int capacity = xsArrayGetSize(dct);
    int slot = _xsFloatIntDictFindSlot(dct, key, capacity);
    if (slot >= 0) {
        int oldVal = xsArrayGetInt(dct, slot + 1);
        xsArraySetInt(dct, slot + 1, val);
        _floatIntDictLastOperationStatus = cFloatIntDictSuccess;
        return (oldVal);
    }
    int r = _xsFloatIntDictRehashIfNeeded(dct, size, capacity, size + 1);
    if (r != cFloatIntDictSuccess) {
        return (cFloatIntDictGenericError);
    }
    capacity = xsArrayGetSize(dct);
    int previousValue = _xsFloatIntDictUpsert(dct, key, val, capacity);
    if (_floatIntDictLastOperationStatus == cFloatIntDictNoKeyError) {
        xsArraySetInt(dct, 0, size + 1);
        return (cFloatIntDictGenericError);
    }
    if (_floatIntDictLastOperationStatus != cFloatIntDictSuccess) {
        return (cFloatIntDictGenericError);
    }
    return (previousValue);
}

/*
    Creates a dict with provided key-value pairs. The first key that equals `cFloatIntDictEmptyKey`
    will stop further insertion.
    This function can create a dict with 6 entries at the maximum, but further entries can be added with
    `xsFloatIntDictPut`.
    @return created dict id, or `cFloatIntDictGenericError` on error
*/
int xsFloatIntDict(float k1 = cFloatIntDictEmptyKey, int v1 = 0, float k2 = cFloatIntDictEmptyKey, int v2 = 0, float k3 = cFloatIntDictEmptyKey, int v3 = 0, float k4 = cFloatIntDictEmptyKey, int v4 = 0, float k5 = cFloatIntDictEmptyKey, int v5 = 0, float k6 = cFloatIntDictEmptyKey, int v6 = 0) {
    int dct = xsFloatIntDictCreate();
    if (dct < 0) {
        return (cFloatIntDictGenericError);
    }
    if (k1 == cFloatIntDictEmptyKey) {
        return (dct);
    }
    xsFloatIntDictPut(dct, k1, v1);
    if (k2 == cFloatIntDictEmptyKey) {
        return (dct);
    }
    xsFloatIntDictPut(dct, k2, v2);
    if (k3 == cFloatIntDictEmptyKey) {
        return (dct);
    }
    xsFloatIntDictPut(dct, k3, v3);
    if (k4 == cFloatIntDictEmptyKey) {
        return (dct);
    }
    xsFloatIntDictPut(dct, k4, v4);
    if (k5 == cFloatIntDictEmptyKey) {
        return (dct);
    }
    xsFloatIntDictPut(dct, k5, v5);
    if (k6 == cFloatIntDictEmptyKey) {
        return (dct);
    }
    xsFloatIntDictPut(dct, k6, v6);
    return (dct);
}

/*
    Returns the value associated with the given key. Sets last error on completion.
    @param dft - default value returned if the key is not found
    @return value for the key, or `dft` if not found
*/
int xsFloatIntDictGet(int dct = -1, float key = 0.0, int dft = -1) {
    int capacity = xsArrayGetSize(dct);
    int slot = _xsFloatIntDictFindSlot(dct, key, capacity);
    if (slot >= 0) {
        _floatIntDictLastOperationStatus = cFloatIntDictSuccess;
        return (xsArrayGetInt(dct, slot + 1));
    }
    _floatIntDictLastOperationStatus = cFloatIntDictNoKeyError;
    return (dft);
}

/*
    Removes the entry with the given key from the dict. Sets last error on completion.
    Uses backward shift deletion to maintain the linear probing invariant (no tombstones).
    @return value that was associated with the key, or `cFloatIntDictGenericError` if not found
*/
int xsFloatIntDictRemove(int dct = -1, float key = 0.0) {
    int size = xsArrayGetInt(dct, 0);
    int capacity = xsArrayGetSize(dct);
    int numSlots = (capacity - 1) / 2;
    int slot = _xsFloatIntDictFindSlot(dct, key, capacity);
    if (slot < 0) {
        _floatIntDictLastOperationStatus = cFloatIntDictNoKeyError;
        return (cFloatIntDictGenericError);
    }
    int foundVal = xsArrayGetInt(dct, slot + 1);
    int g = slot;
    int q = g + 2;
    if (q >= capacity) {
        q = 1;
    }
    int shiftSteps = 0;
    int qKeyBits = xsArrayGetInt(dct, q);
    while ((qKeyBits != cFloatIntDictEmptyKeyBits) && (shiftSteps < numSlots)) {
        int qHome = _xsFloatIntDictHash(bitCastToFloat(qKeyBits), capacity);
        int gSlot = (g - 1) / 2;
        int qSlot = (q - 1) / 2;
        int hSlot = (qHome - 1) / 2;
        int distG = ((gSlot - hSlot) + numSlots) % numSlots;
        int distQ = ((qSlot - hSlot) + numSlots) % numSlots;
        if (distG < distQ) {
            xsArraySetInt(dct, g, qKeyBits);
            xsArraySetInt(dct, g + 1, xsArrayGetInt(dct, q + 1));
            g = q;
        }
        q = q + 2;
        if (q >= capacity) {
            q = 1;
        }
        shiftSteps++;
        qKeyBits = xsArrayGetInt(dct, q);
    }
    xsArraySetInt(dct, g, cFloatIntDictEmptyKeyBits);
    xsArraySetInt(dct, 0, size - 1);
    _floatIntDictLastOperationStatus = cFloatIntDictSuccess;
    return (foundVal);
}

/*
    Checks whether the given key exists in the dict.
    @return true if the key is found, false otherwise
*/
bool xsFloatIntDictContains(int dct = -1, float key = 0.0) {
    int capacity = xsArrayGetSize(dct);
    return (_xsFloatIntDictFindSlot(dct, key, capacity) >= 0);
}

/*
    Returns the number of key-value pairs stored in the dict.
    @return dict size
*/
int xsFloatIntDictSize(int dct = -1) {
    return (xsArrayGetInt(dct, 0));
}

/*
    Removes all entries from the dict and shrinks storage back to the initial capacity when possible.
    @return `cFloatIntDictSuccess` on success, or `cFloatIntDictGenericError` on error
*/
int xsFloatIntDictClear(int dct = -1) {
    int capacity = xsArrayGetSize(dct);
    int i = 1;
    while (i < capacity) {
        xsArraySetInt(dct, i, cFloatIntDictEmptyKeyBits);
        i = i + 2;
    }
    xsArraySetInt(dct, 0, 0);
    if (capacity > cFloatIntDictInitialCapacity) {
        int r = xsArrayResizeInt(dct, cFloatIntDictInitialCapacity);
        if (r != 1) {
            return (cFloatIntDictGenericError);
        }
    }
    return (cFloatIntDictSuccess);
}

/*
    Creates a shallow copy of the dict.
    @return new dict id, or `cFloatIntDictResizeFailedError` on error
*/
int xsFloatIntDictCopy(int dct = -1) {
    int capacity = xsArrayGetSize(dct);
    int newDct = xsArrayCreateInt(capacity, cFloatIntDictEmptyKeyBits);
    if (newDct < 0) {
        return (cFloatIntDictResizeFailedError);
    }
    int i = 1;
    while (i < capacity) {
        int storedKeyBits = xsArrayGetInt(dct, i);
        if (storedKeyBits != cFloatIntDictEmptyKeyBits) {
            xsArraySetInt(newDct, i, storedKeyBits);
            xsArraySetInt(newDct, i + 1, xsArrayGetInt(dct, i + 1));
        }
        i = i + 2;
    }
    xsArraySetInt(newDct, 0, xsArrayGetInt(dct, 0));
    return (newDct);
}

/*
    Returns a string representation of the dict.
    @return string representation of the dict
*/
string xsFloatIntDictToString(int dct = -1) {
    int capacity = xsArrayGetSize(dct);
    string s = "{";
    bool first = true;
    int i = 1;
    while (i < capacity) {
        int keyBits = xsArrayGetInt(dct, i);
        if (keyBits != cFloatIntDictEmptyKeyBits) {
            if (first) {
                first = false;
            } else {
                s = s + ", ";
            }
            s = s + (bitCastToFloat(keyBits) + ": " + xsArrayGetInt(dct, i + 1));
        }
        i = i + 2;
    }
    s = s + "}";
    return (s);
}

/*
    Returns the status of the last operation that reports errors through the dict API.
    @return `cFloatIntDictSuccess` if the last such operation succeeded, or a negative error code
*/
int xsFloatIntDictLastError() {
    return (_floatIntDictLastOperationStatus);
}

float _xsFloatIntDictFindNextOccupied(int dct = -1, int start = 1, int capacity = 0) {
    int slot = start;
    while (slot < capacity) {
        int storedKeyBits = xsArrayGetInt(dct, slot);
        if (storedKeyBits != cFloatIntDictEmptyKeyBits) {
            _floatIntDictLastOperationStatus = cFloatIntDictSuccess;
            return (bitCastToFloat(storedKeyBits));
        }
        slot = slot + 2;
    }
    _floatIntDictLastOperationStatus = cFloatIntDictNoKeyError;
    return (cFloatIntDictGenericErrorFloat);
}

/*
    Returns the next key in the dict for stateless iteration. Sets last error on completion.
    @param is_first - if true, returns the first key in the dict
    @param prev_key - the previous key returned by this function (ignored if `isFirst` is true)
    @return next key, or `cFloatIntDictGenericErrorFloat` if no more keys
        (last error set to `cFloatIntDictNoKeyError`)
*/
float xsFloatIntDictNextKey(int dct = -1, bool isFirst = true, float prevKey = cFloatIntDictEmptyKey) {
    int capacity = xsArrayGetSize(dct);
    if (isFirst) {
        return (_xsFloatIntDictFindNextOccupied(dct, 1, capacity));
    }
    int slot = _xsFloatIntDictFindSlot(dct, prevKey, capacity);
    if (slot < 0) {
        _floatIntDictLastOperationStatus = cFloatIntDictNoKeyError;
        return (cFloatIntDictGenericErrorFloat);
    }
    int nextStart = slot + 2;
    return (_xsFloatIntDictFindNextOccupied(dct, nextStart, capacity));
}

/*
    Checks whether there is a next key in the dict for stateless iteration.
    @param is_first - if true, checks whether the dict has any keys
    @param prev_key - the previous key (ignored if `isFirst` is true)
    @return true if there is a next key, false otherwise
*/
bool xsFloatIntDictHasNext(int dct = -1, bool isFirst = true, float prevKey = cFloatIntDictEmptyKey) {
    int capacity = xsArrayGetSize(dct);
    int start = 1;
    if (isFirst == false) {
        int slot = _xsFloatIntDictFindSlot(dct, prevKey, capacity);
        if (slot < 0) {
            return (false);
        }
        start = slot + 2;
    }
    while (start < capacity) {
        if (xsArrayGetInt(dct, start) != cFloatIntDictEmptyKeyBits) {
            return (true);
        }
        start = start + 2;
    }
    return (false);
}

/*
    Updates `source` with all entries from `dct`. Existing keys in `source` are overwritten.
    @return `cFloatIntDictSuccess` on success, or a negative error code
*/
int xsFloatIntDictUpdate(int source = -1, int dct = -1) {
    int capacity = xsArrayGetSize(dct);
    int i = 1;
    while (i < capacity) {
        int keyBits = xsArrayGetInt(dct, i);
        if (keyBits != cFloatIntDictEmptyKeyBits) {
            xsFloatIntDictPut(source, bitCastToFloat(keyBits), xsArrayGetInt(dct, i + 1));
            if ((_floatIntDictLastOperationStatus != cFloatIntDictSuccess) && (_floatIntDictLastOperationStatus != cFloatIntDictNoKeyError)) {
                return (_floatIntDictLastOperationStatus);
            }
        }
        i = i + 2;
    }
    _floatIntDictLastOperationStatus = cFloatIntDictSuccess;
    return (cFloatIntDictSuccess);
}

/*
    Inserts the key-value pair only if the key is not already present. Sets last error on completion.
    If `key` equals `cFloatIntDictEmptyKey`, the call is a no-op and returns
    `cFloatIntDictGenericError` with last error set to `cFloatIntDictGenericError`.
    @return existing value if the key was already present, or `cFloatIntDictGenericError`
        if newly inserted or on error. Because -1 is both the error sentinel and a valid stored
        value, callers must check `xs_float_int_dict_last_error()` to distinguish the cases.
*/
int xsFloatIntDictPutIfAbsent(int dct = -1, float key = 0.0, int val = 0) {
    if (key == cFloatIntDictEmptyKey) {
        _floatIntDictLastOperationStatus = cFloatIntDictGenericError;
        return (cFloatIntDictGenericError);
    }
    int size = xsArrayGetInt(dct, 0);
    int capacity = xsArrayGetSize(dct);
    int slot = _xsFloatIntDictFindSlot(dct, key, capacity);
    if (slot >= 0) {
        _floatIntDictLastOperationStatus = cFloatIntDictSuccess;
        return (xsArrayGetInt(dct, slot + 1));
    }
    int r = _xsFloatIntDictRehashIfNeeded(dct, size, capacity, size + 1);
    if (r != cFloatIntDictSuccess) {
        return (cFloatIntDictGenericError);
    }
    capacity = xsArrayGetSize(dct);
    int result = _xsFloatIntDictUpsert(dct, key, val, capacity);
    if (_floatIntDictLastOperationStatus == cFloatIntDictNoKeyError) {
        xsArraySetInt(dct, 0, size + 1);
        return (cFloatIntDictGenericError);
    }
    if (_floatIntDictLastOperationStatus != cFloatIntDictSuccess) {
        return (cFloatIntDictGenericError);
    }
    return (result);
}

/*
    Returns a float array containing all keys in iteration order.
    Keys are returned in canonicalized form, so `-0.0` becomes `0.0` and NaN keys use the canonical NaN payload.
    @return array id, or `cFloatIntDictResizeFailedError` on allocation failure
*/
int xsFloatIntDictKeys(int dct = -1) {
    int size = xsArrayGetInt(dct, 0);
    int arr = xsArrayCreateFloat(size, 0.0);
    if (arr < 0) {
        return (cFloatIntDictResizeFailedError);
    }
    int capacity = xsArrayGetSize(dct);
    int idx = 0;
    int i = 1;
    while (i < capacity) {
        int storedKeyBits = xsArrayGetInt(dct, i);
        if (storedKeyBits != cFloatIntDictEmptyKeyBits) {
            xsArraySetFloat(arr, idx, bitCastToFloat(storedKeyBits));
            idx++;
        }
        i = i + 2;
    }
    return (arr);
}

/*
    Returns an int array containing all values in the same order as `xsFloatIntDictKeys`.
    @return array id, or `cFloatIntDictResizeFailedError` on allocation failure
*/
int xsFloatIntDictValues(int dct = -1) {
    int size = xsArrayGetInt(dct, 0);
    int arr = xsArrayCreateInt(size, 0);
    if (arr < 0) {
        return (cFloatIntDictResizeFailedError);
    }
    int capacity = xsArrayGetSize(dct);
    int idx = 0;
    int i = 1;
    while (i < capacity) {
        int storedKeyBits = xsArrayGetInt(dct, i);
        if (storedKeyBits != cFloatIntDictEmptyKeyBits) {
            xsArraySetInt(arr, idx, xsArrayGetInt(dct, i + 1));
            idx++;
        }
        i = i + 2;
    }
    return (arr);
}

/*
    Checks whether both dicts contain the same keys and values.
    Float keys are compared using the dict's canonical key semantics for signed zero and NaN.
    @return true if both dicts are equal, false otherwise
*/
bool xsFloatIntDictEquals(int a = -1, int b = -1) {
    int sizeA = xsArrayGetInt(a, 0);
    int sizeB = xsArrayGetInt(b, 0);
    if (sizeA != sizeB) {
        return (false);
    }
    int capacity = xsArrayGetSize(a);
    int i = 1;
    while (i < capacity) {
        int keyBits = xsArrayGetInt(a, i);
        if (keyBits != cFloatIntDictEmptyKeyBits) {
            int val = xsArrayGetInt(a, i + 1);
            if (xsFloatIntDictGet(b, bitCastToFloat(keyBits)) != val) {
                return (false);
            }
            if (xsFloatIntDictLastError() != cFloatIntDictSuccess) {
                return (false);
            }
        }
        i = i + 2;
    }
    return (true);
}

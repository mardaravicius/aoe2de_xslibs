extern const int cFloatStringDictSuccess = 0;
extern const int cFloatStringDictGenericError = -1;
extern const float cFloatStringDictGenericErrorFloat = -1.0;
extern const int cFloatStringDictNoKeyError = -2;
extern const int cFloatStringDictResizeFailedError = -3;
extern const int cFloatStringDictMaxCapacityError = -4;
extern const int cFloatStringDictMaxCapacity = 999999999;
extern const float cFloatStringDictMaxLoadFactor = 0.75;
extern const float cFloatStringDictEmptyKey = -9999999.0;
extern const int cFloatStringDictEmptyKeyBits = -887581057;
extern const int cFloatStringDictCanonicalNanBits = -8388607;
extern const int cFloatStringDictInitialCapacity = 18;
extern const int cFloatStringDictHashConstant = 16777619;
int _floatStringDictLastOperationStatus = cFloatStringDictSuccess;
int _floatStringDictTempKeys = -1;
int _floatStringDictTempValues = -1;

int _xsFloatStringDictKeyBits(float key = 0.0) {
    if (key != key) {
        return (cFloatStringDictCanonicalNanBits);
    }
    if (key == 0.0) {
        return (0);
    }
    return (bitCastToInt(key));
}

int _xsFloatStringDictValuesCapacityFromIntCapacity(int capacity = 0) {
    return (capacity - 2);
}

int _xsFloatStringDictGetValuesArray(int dct = -1) {
    return (xsArrayGetInt(dct, 1));
}

int _xsFloatStringDictValueSlot(int slot = 2) {
    return (slot - 2);
}

string _xsFloatStringDictGetStoredValue(int dct = -1, int slot = 2) {
    return (xsArrayGetString(_xsFloatStringDictGetValuesArray(dct), _xsFloatStringDictValueSlot(slot)));
}

void _xsFloatStringDictSetStoredValue(int dct = -1, int slot = 2, string value = "") {
    xsArraySetString(_xsFloatStringDictGetValuesArray(dct), _xsFloatStringDictValueSlot(slot), value);
}

void _xsFloatStringDictClearSlot(int dct = -1, int slot = 2) {
    xsArraySetInt(dct, slot, cFloatStringDictEmptyKeyBits);
}

/*
    Creates an empty float-to-string dictionary.
    Keys equal to `cFloatStringDictEmptyKey` are reserved as the internal
    empty-slot sentinel and cannot be stored. `put` and `putIfAbsent` silently reject them.
    Signed zero keys are canonicalized to `0.0`, and all NaN keys are canonicalized to a
    single NaN bit pattern.
    @return created dict id, or `cFloatStringDictGenericError` on error
*/
int xsFloatStringDictCreate() {
    int dct = xsArrayCreateInt(cFloatStringDictInitialCapacity, cFloatStringDictEmptyKeyBits);
    if (dct < 0) {
        return (cFloatStringDictGenericError);
    }
    int valuesArr = xsArrayCreateString(cFloatStringDictInitialCapacity - 2);
    if (valuesArr < 0) {
        xsArrayResizeInt(dct, 0);
        return (cFloatStringDictGenericError);
    }
    xsArraySetInt(dct, 0, 0);
    xsArraySetInt(dct, 1, valuesArr);
    return (dct);
}

int _xsFloatStringDictHash(float key = 0.0, int capacity = 0) {
    int h = _xsFloatStringDictKeyBits(key) * cFloatStringDictHashConstant;
    int numSlots = _xsFloatStringDictValuesCapacityFromIntCapacity(capacity);
    h = h % numSlots;
    if (h < 0) {
        h = h + numSlots;
    }
    return (h + 2);
}

int _xsFloatStringDictFindSlot(int dct = -1, float key = 0.0, int capacity = 0) {
    int numSlots = _xsFloatStringDictValuesCapacityFromIntCapacity(capacity);
    int keyBits = _xsFloatStringDictKeyBits(key);
    int home = _xsFloatStringDictHash(key, capacity);
    int slot = home;
    int steps = 0;
    while (steps < numSlots) {
        int storedKeyBits = xsArrayGetInt(dct, slot);
        if (storedKeyBits == cFloatStringDictEmptyKeyBits) {
            return (-1);
        }
        if (storedKeyBits == keyBits) {
            return (slot);
        }
        slot++;
        if (slot >= capacity) {
            slot = 2;
        }
        steps++;
    }
    return (-1);
}

string _xsFloatStringDictUpsert(int dct = -1, float key = 0.0, string val = "", int capacity = 0) {
    int keyBits = _xsFloatStringDictKeyBits(key);
    int numSlots = _xsFloatStringDictValuesCapacityFromIntCapacity(capacity);
    int home = _xsFloatStringDictHash(key, capacity);
    int slot = home;
    int steps = 0;
    while (steps < numSlots) {
        int storedKeyBits = xsArrayGetInt(dct, slot);
        if (storedKeyBits == cFloatStringDictEmptyKeyBits) {
            xsArraySetInt(dct, slot, keyBits);
            _xsFloatStringDictSetStoredValue(dct, slot, val);
            _floatStringDictLastOperationStatus = cFloatStringDictNoKeyError;
            return ("-1");
        }
        if (storedKeyBits == keyBits) {
            string oldVal = _xsFloatStringDictGetStoredValue(dct, slot);
            _xsFloatStringDictSetStoredValue(dct, slot, val);
            _floatStringDictLastOperationStatus = cFloatStringDictSuccess;
            return (oldVal);
        }
        slot++;
        if (slot >= capacity) {
            slot = 2;
        }
        steps++;
    }
    _floatStringDictLastOperationStatus = cFloatStringDictMaxCapacityError;
    return ("-1");
}

int _xsFloatStringDictMoveToTempArrays(int dct = -1, int size = 0, int capacity = 0) {
    int tempDataSize = size;
    int maxValuesCapacity = cFloatStringDictMaxCapacity - 2;
    if (_floatStringDictTempKeys < 0) {
        _floatStringDictTempKeys = xsArrayCreateInt(tempDataSize, cFloatStringDictEmptyKeyBits);
        if (_floatStringDictTempKeys < 0) {
            return (cFloatStringDictResizeFailedError);
        }
    } else {
        int tempKeysCapacity = xsArrayGetSize(_floatStringDictTempKeys);
        if (tempKeysCapacity < tempDataSize) {
            if (tempDataSize > maxValuesCapacity) {
                return (cFloatStringDictMaxCapacityError);
            }
            int rKeys = xsArrayResizeInt(_floatStringDictTempKeys, tempDataSize);
            if (rKeys != 1) {
                return (cFloatStringDictResizeFailedError);
            }
        }
    }
    if (_floatStringDictTempValues < 0) {
        _floatStringDictTempValues = xsArrayCreateString(tempDataSize);
        if (_floatStringDictTempValues < 0) {
            return (cFloatStringDictResizeFailedError);
        }
    } else {
        int tempValuesCapacity = xsArrayGetSize(_floatStringDictTempValues);
        if (tempValuesCapacity < tempDataSize) {
            if (tempDataSize > maxValuesCapacity) {
                return (cFloatStringDictMaxCapacityError);
            }
            int rValues = xsArrayResizeString(_floatStringDictTempValues, tempDataSize);
            if (rValues != 1) {
                return (cFloatStringDictResizeFailedError);
            }
        }
    }
    int t = 0;
    for (i = 2; < capacity) {
        int storedKeyBits = xsArrayGetInt(dct, i);
        if (storedKeyBits != cFloatStringDictEmptyKeyBits) {
            xsArraySetInt(_floatStringDictTempKeys, t, storedKeyBits);
            xsArraySetString(_floatStringDictTempValues, t, _xsFloatStringDictGetStoredValue(dct, i));
            t++;
        }
    }
    return (tempDataSize);
}

void _xsFloatStringDictClearSlots(int dct = -1, int capacity = -1) {
    for (j = 2; < capacity) {
        _xsFloatStringDictClearSlot(dct, j);
    }
}

int _xsFloatStringDictRehashIfNeeded(int dct = -1, int size = 0, int capacity = 0, int requiredSize = -1) {
    if (requiredSize < 0) {
        requiredSize = size;
    }
    float loadFactor = (0.0 + requiredSize) / _xsFloatStringDictValuesCapacityFromIntCapacity(capacity);
    if (loadFactor > cFloatStringDictMaxLoadFactor) {
        int storeStatus = _floatStringDictLastOperationStatus;
        int newValuesCapacity = _xsFloatStringDictValuesCapacityFromIntCapacity(capacity) * 2;
        int newCapacity = newValuesCapacity + 2;
        if (newCapacity > cFloatStringDictMaxCapacity) {
            _floatStringDictLastOperationStatus = cFloatStringDictMaxCapacityError;
            return (cFloatStringDictGenericError);
        }
        int tempDataSize = _xsFloatStringDictMoveToTempArrays(dct, size, capacity);
        if (tempDataSize < 0) {
            _floatStringDictLastOperationStatus = tempDataSize;
            return (cFloatStringDictGenericError);
        }
        int valuesArr = _xsFloatStringDictGetValuesArray(dct);
        int rValues = xsArrayResizeString(valuesArr, newValuesCapacity);
        if (rValues != 1) {
            _floatStringDictLastOperationStatus = cFloatStringDictResizeFailedError;
            return (cFloatStringDictGenericError);
        }
        int r = xsArrayResizeInt(dct, newCapacity);
        if (r != 1) {
            _floatStringDictLastOperationStatus = cFloatStringDictResizeFailedError;
            return (cFloatStringDictGenericError);
        }
        _xsFloatStringDictClearSlots(dct, newCapacity);
        for (t = 0; < tempDataSize) {
            _xsFloatStringDictUpsert(dct, bitCastToFloat(xsArrayGetInt(_floatStringDictTempKeys, t)), xsArrayGetString(_floatStringDictTempValues, t), newCapacity);
            if ((_floatStringDictLastOperationStatus < 0) && (_floatStringDictLastOperationStatus != cFloatStringDictNoKeyError)) {
                return (cFloatStringDictGenericError);
            }
        }
        _floatStringDictLastOperationStatus = storeStatus;
    }
    return (cFloatStringDictSuccess);
}

string xsFloatStringDictPut(int dct = -1, float key = 0.0, string val = "") {
    if (key == cFloatStringDictEmptyKey) {
        _floatStringDictLastOperationStatus = cFloatStringDictGenericError;
        return ("-1");
    }
    int size = xsArrayGetInt(dct, 0);
    int capacity = xsArrayGetSize(dct);
    int slot = _xsFloatStringDictFindSlot(dct, key, capacity);
    if (slot >= 0) {
        string oldVal = _xsFloatStringDictGetStoredValue(dct, slot);
        _xsFloatStringDictSetStoredValue(dct, slot, val);
        _floatStringDictLastOperationStatus = cFloatStringDictSuccess;
        return (oldVal);
    }
    int r = _xsFloatStringDictRehashIfNeeded(dct, size, capacity, size + 1);
    if (r != cFloatStringDictSuccess) {
        return ("-1");
    }
    capacity = xsArrayGetSize(dct);
    string previousValue = _xsFloatStringDictUpsert(dct, key, val, capacity);
    if (_floatStringDictLastOperationStatus == cFloatStringDictNoKeyError) {
        xsArraySetInt(dct, 0, size + 1);
        return ("-1");
    }
    if (_floatStringDictLastOperationStatus != cFloatStringDictSuccess) {
        return ("-1");
    }
    return (previousValue);
}

/*
    Creates a dict with provided key-value pairs. The first key that equals
    `cFloatStringDictEmptyKey` will stop further insertion.
*/
int xsFloatStringDict(float k1 = cFloatStringDictEmptyKey, string v1 = "", float k2 = cFloatStringDictEmptyKey, string v2 = "", float k3 = cFloatStringDictEmptyKey, string v3 = "", float k4 = cFloatStringDictEmptyKey, string v4 = "", float k5 = cFloatStringDictEmptyKey, string v5 = "", float k6 = cFloatStringDictEmptyKey, string v6 = "") {
    int dct = xsFloatStringDictCreate();
    if (dct < 0) {
        return (cFloatStringDictGenericError);
    }
    if (k1 == cFloatStringDictEmptyKey) {
        return (dct);
    }
    xsFloatStringDictPut(dct, k1, v1);
    if (k2 == cFloatStringDictEmptyKey) {
        return (dct);
    }
    xsFloatStringDictPut(dct, k2, v2);
    if (k3 == cFloatStringDictEmptyKey) {
        return (dct);
    }
    xsFloatStringDictPut(dct, k3, v3);
    if (k4 == cFloatStringDictEmptyKey) {
        return (dct);
    }
    xsFloatStringDictPut(dct, k4, v4);
    if (k5 == cFloatStringDictEmptyKey) {
        return (dct);
    }
    xsFloatStringDictPut(dct, k5, v5);
    if (k6 == cFloatStringDictEmptyKey) {
        return (dct);
    }
    xsFloatStringDictPut(dct, k6, v6);
    return (dct);
}

/*
    Returns the value associated with the given key. Sets last error on completion.
    @return value for the key, or `dft` if not found
*/
string xsFloatStringDictGet(int dct = -1, float key = 0.0, string dft = "-1") {
    int capacity = xsArrayGetSize(dct);
    int slot = _xsFloatStringDictFindSlot(dct, key, capacity);
    if (slot >= 0) {
        _floatStringDictLastOperationStatus = cFloatStringDictSuccess;
        return (_xsFloatStringDictGetStoredValue(dct, slot));
    }
    _floatStringDictLastOperationStatus = cFloatStringDictNoKeyError;
    return (dft);
}

/*
    Removes the entry with the given key from the dict. Sets last error on completion.
    Uses backward shift deletion to maintain linear probing invariant (no tombstones).
    @return value that was associated with the key, or `"-1"` if not found
*/
string xsFloatStringDictRemove(int dct = -1, float key = 0.0) {
    int size = xsArrayGetInt(dct, 0);
    int capacity = xsArrayGetSize(dct);
    int numSlots = _xsFloatStringDictValuesCapacityFromIntCapacity(capacity);
    int slot = _xsFloatStringDictFindSlot(dct, key, capacity);
    if (slot < 0) {
        _floatStringDictLastOperationStatus = cFloatStringDictNoKeyError;
        return ("-1");
    }
    string foundVal = _xsFloatStringDictGetStoredValue(dct, slot);
    int g = slot;
    int q = g + 1;
    if (q >= capacity) {
        q = 2;
    }
    int shiftSteps = 0;
    int qKeyBits = xsArrayGetInt(dct, q);
    while ((qKeyBits != cFloatStringDictEmptyKeyBits) && (shiftSteps < numSlots)) {
        int qHome = _xsFloatStringDictHash(bitCastToFloat(qKeyBits), capacity);
        int gSlot = g - 2;
        int qSlot = q - 2;
        int hSlot = qHome - 2;
        int distG = ((gSlot - hSlot) + numSlots) % numSlots;
        int distQ = ((qSlot - hSlot) + numSlots) % numSlots;
        if (distG < distQ) {
            xsArraySetInt(dct, g, qKeyBits);
            _xsFloatStringDictSetStoredValue(dct, g, _xsFloatStringDictGetStoredValue(dct, q));
            g = q;
        }
        q++;
        if (q >= capacity) {
            q = 2;
        }
        shiftSteps++;
        qKeyBits = xsArrayGetInt(dct, q);
    }
    _xsFloatStringDictClearSlot(dct, g);
    xsArraySetInt(dct, 0, size - 1);
    _floatStringDictLastOperationStatus = cFloatStringDictSuccess;
    return (foundVal);
}

/*
    Checks whether the given key exists in the dict.
    @return true if the key is found, false otherwise
*/
bool xsFloatStringDictContains(int dct = -1, float key = 0.0) {
    int capacity = xsArrayGetSize(dct);
    return (_xsFloatStringDictFindSlot(dct, key, capacity) >= 0);
}

/*
    Returns the number of key-value pairs stored in the dict.
    @return dict size
*/
int xsFloatStringDictSize(int dct = -1) {
    return (xsArrayGetInt(dct, 0));
}

/*
    Removes all entries from the dict and shrinks storage back to the initial capacity when possible.
    @return `cFloatStringDictSuccess` on success, or `cFloatStringDictGenericError` on error
*/
int xsFloatStringDictClear(int dct = -1) {
    int capacity = xsArrayGetSize(dct);
    _xsFloatStringDictClearSlots(dct, capacity);
    xsArraySetInt(dct, 0, 0);
    if (capacity > cFloatStringDictInitialCapacity) {
        int valuesArr = _xsFloatStringDictGetValuesArray(dct);
        int r = xsArrayResizeInt(dct, cFloatStringDictInitialCapacity);
        if (r != 1) {
            return (cFloatStringDictGenericError);
        }
        int rValues = xsArrayResizeString(valuesArr, cFloatStringDictInitialCapacity - 2);
        if (rValues != 1) {
            return (cFloatStringDictGenericError);
        }
    }
    return (cFloatStringDictSuccess);
}

/*
    Creates a shallow copy of the dict.
    @return new dict id, or `cFloatStringDictResizeFailedError` on error
*/
int xsFloatStringDictCopy(int dct = -1) {
    int capacity = xsArrayGetSize(dct);
    int valuesCapacity = _xsFloatStringDictValuesCapacityFromIntCapacity(capacity);
    int newDct = xsArrayCreateInt(capacity, cFloatStringDictEmptyKeyBits);
    if (newDct < 0) {
        return (cFloatStringDictResizeFailedError);
    }
    int newValuesArr = xsArrayCreateString(valuesCapacity);
    if (newValuesArr < 0) {
        xsArrayResizeInt(newDct, 0);
        return (cFloatStringDictResizeFailedError);
    }
    xsArraySetInt(newDct, 0, xsArrayGetInt(dct, 0));
    xsArraySetInt(newDct, 1, newValuesArr);
    for (i = 2; < capacity) {
        int storedKeyBits = xsArrayGetInt(dct, i);
        if (storedKeyBits != cFloatStringDictEmptyKeyBits) {
            xsArraySetInt(newDct, i, storedKeyBits);
            xsArraySetString(newValuesArr, i - 2, _xsFloatStringDictGetStoredValue(dct, i));
        }
    }
    return (newDct);
}

/*
    Returns a string representation of the dict.
    @return string representation of the dict
*/
string xsFloatStringDictToString(int dct = -1) {
    int capacity = xsArrayGetSize(dct);
    string s = "{";
    bool first = true;
    for (i = 2; < capacity) {
        int keyBits = xsArrayGetInt(dct, i);
        if (keyBits != cFloatStringDictEmptyKeyBits) {
            if (first) {
                first = false;
            } else {
                s = s + ", ";
            }
            s = s + (bitCastToFloat(keyBits) + ": \"" + _xsFloatStringDictGetStoredValue(dct, i) + "\"");
        }
    }
    s = s + "}";
    return (s);
}

/*
    Returns the status of the last operation that reports errors through the dict API.
    @return `cFloatStringDictSuccess` if the last such operation succeeded, or a negative error code
*/
int xsFloatStringDictLastError() {
    return (_floatStringDictLastOperationStatus);
}

float _xsFloatStringDictFindNextOccupied(int dct = -1, int start = 2, int capacity = 0) {
    int slot = start;
    while (slot < capacity) {
        int storedKeyBits = xsArrayGetInt(dct, slot);
        if (storedKeyBits != cFloatStringDictEmptyKeyBits) {
            _floatStringDictLastOperationStatus = cFloatStringDictSuccess;
            return (bitCastToFloat(storedKeyBits));
        }
        slot++;
    }
    _floatStringDictLastOperationStatus = cFloatStringDictNoKeyError;
    return (cFloatStringDictGenericErrorFloat);
}

/*
    Returns the next key in the dict for stateless iteration. Sets last error on completion.
    @param is_first - if true, returns the first key in the dict
    @param prev_key - the previous key returned by this function (ignored if `isFirst` is true)
    @return next key, or `cFloatStringDictGenericErrorFloat` if no more keys
        (last error set to `cFloatStringDictNoKeyError`)
*/
float xsFloatStringDictNextKey(int dct = -1, bool isFirst = true, float prevKey = cFloatStringDictEmptyKey) {
    int capacity = xsArrayGetSize(dct);
    if (isFirst) {
        return (_xsFloatStringDictFindNextOccupied(dct, 2, capacity));
    }
    int slot = _xsFloatStringDictFindSlot(dct, prevKey, capacity);
    if (slot < 0) {
        _floatStringDictLastOperationStatus = cFloatStringDictNoKeyError;
        return (cFloatStringDictGenericErrorFloat);
    }
    int nextStart = slot + 1;
    return (_xsFloatStringDictFindNextOccupied(dct, nextStart, capacity));
}

/*
    Checks whether there is a next key in the dict for stateless iteration.
    @param is_first - if true, checks whether the dict has any keys
    @param prev_key - the previous key (ignored if `isFirst` is true)
    @return true if there is a next key, false otherwise
*/
bool xsFloatStringDictHasNext(int dct = -1, bool isFirst = true, float prevKey = cFloatStringDictEmptyKey) {
    int capacity = xsArrayGetSize(dct);
    int start = 2;
    if (isFirst == false) {
        int slot = _xsFloatStringDictFindSlot(dct, prevKey, capacity);
        if (slot < 0) {
            return (false);
        }
        start = slot + 1;
    }
    while (start < capacity) {
        if (xsArrayGetInt(dct, start) != cFloatStringDictEmptyKeyBits) {
            return (true);
        }
        start++;
    }
    return (false);
}

/*
    Updates `source` with all entries from `dct`. Existing keys in `source` are overwritten.
    @return `cFloatStringDictSuccess` on success, or a negative error code
*/
int xsFloatStringDictUpdate(int source = -1, int dct = -1) {
    int capacity = xsArrayGetSize(dct);
    for (i = 2; < capacity) {
        int keyBits = xsArrayGetInt(dct, i);
        if (keyBits != cFloatStringDictEmptyKeyBits) {
            xsFloatStringDictPut(source, bitCastToFloat(keyBits), _xsFloatStringDictGetStoredValue(dct, i));
            if ((_floatStringDictLastOperationStatus != cFloatStringDictSuccess) && (_floatStringDictLastOperationStatus != cFloatStringDictNoKeyError)) {
                return (_floatStringDictLastOperationStatus);
            }
        }
    }
    _floatStringDictLastOperationStatus = cFloatStringDictSuccess;
    return (cFloatStringDictSuccess);
}

/*
    Inserts the key-value pair only if the key is not already present. Sets last error on completion.
    If `key` equals `cFloatStringDictEmptyKey`, the call is a no-op and returns
    `"-1"` with last error set to `cFloatStringDictGenericError`.
    @return existing value if the key was already present, or `"-1"`
        if newly inserted or on error. Callers must check `xs_float_string_dict_last_error()`.
*/
string xsFloatStringDictPutIfAbsent(int dct = -1, float key = 0.0, string val = "") {
    if (key == cFloatStringDictEmptyKey) {
        _floatStringDictLastOperationStatus = cFloatStringDictGenericError;
        return ("-1");
    }
    int size = xsArrayGetInt(dct, 0);
    int capacity = xsArrayGetSize(dct);
    int slot = _xsFloatStringDictFindSlot(dct, key, capacity);
    if (slot >= 0) {
        _floatStringDictLastOperationStatus = cFloatStringDictSuccess;
        return (_xsFloatStringDictGetStoredValue(dct, slot));
    }
    int r = _xsFloatStringDictRehashIfNeeded(dct, size, capacity, size + 1);
    if (r != cFloatStringDictSuccess) {
        return ("-1");
    }
    capacity = xsArrayGetSize(dct);
    string result = _xsFloatStringDictUpsert(dct, key, val, capacity);
    if (_floatStringDictLastOperationStatus == cFloatStringDictNoKeyError) {
        xsArraySetInt(dct, 0, size + 1);
        return ("-1");
    }
    if (_floatStringDictLastOperationStatus != cFloatStringDictSuccess) {
        return ("-1");
    }
    return (result);
}

/*
    Returns a float array containing all keys in iteration order.
    Keys are returned in canonicalized form, so `-0.0` becomes `0.0` and NaN keys use the canonical NaN payload.
    @return array id, or `cFloatStringDictResizeFailedError` on allocation failure
*/
int xsFloatStringDictKeys(int dct = -1) {
    int size = xsArrayGetInt(dct, 0);
    int arr = xsArrayCreateFloat(size, 0.0);
    if (arr < 0) {
        return (cFloatStringDictResizeFailedError);
    }
    int capacity = xsArrayGetSize(dct);
    int idx = 0;
    for (i = 2; < capacity) {
        int storedKeyBits = xsArrayGetInt(dct, i);
        if (storedKeyBits != cFloatStringDictEmptyKeyBits) {
            xsArraySetFloat(arr, idx, bitCastToFloat(storedKeyBits));
            idx++;
        }
    }
    return (arr);
}

/*
    Returns a string array containing all values in the same order as `xsFloatStringDictKeys`.
    @return array id, or `cFloatStringDictResizeFailedError` on allocation failure
*/
int xsFloatStringDictValues(int dct = -1) {
    int size = xsArrayGetInt(dct, 0);
    int arr = xsArrayCreateString(size);
    if (arr < 0) {
        return (cFloatStringDictResizeFailedError);
    }
    int capacity = xsArrayGetSize(dct);
    int idx = 0;
    for (i = 2; < capacity) {
        int storedKeyBits = xsArrayGetInt(dct, i);
        if (storedKeyBits != cFloatStringDictEmptyKeyBits) {
            xsArraySetString(arr, idx, _xsFloatStringDictGetStoredValue(dct, i));
            idx++;
        }
    }
    return (arr);
}

/*
    Checks whether both dicts contain the same keys and values.
    Float keys are compared using the dict's canonical key semantics for signed zero and NaN.
    @return true if both dicts are equal, false otherwise
*/
bool xsFloatStringDictEquals(int a = -1, int b = -1) {
    int sizeA = xsArrayGetInt(a, 0);
    int sizeB = xsArrayGetInt(b, 0);
    if (sizeA != sizeB) {
        return (false);
    }
    int capacity = xsArrayGetSize(a);
    for (i = 2; < capacity) {
        int keyBits = xsArrayGetInt(a, i);
        if (keyBits != cFloatStringDictEmptyKeyBits) {
            string val = _xsFloatStringDictGetStoredValue(a, i);
            if (xsFloatStringDictGet(b, bitCastToFloat(keyBits)) != val) {
                return (false);
            }
            if (xsFloatStringDictLastError() != cFloatStringDictSuccess) {
                return (false);
            }
        }
    }
    return (true);
}

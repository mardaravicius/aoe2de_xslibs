extern const int cFloatVectorDictSuccess = 0;
extern const int cFloatVectorDictGenericError = -1;
extern const int cFloatVectorDictNoKeyError = -2;
extern const int cFloatVectorDictResizeFailedError = -3;
extern const int cFloatVectorDictMaxCapacityError = -4;
extern const vector cFloatVectorDictGenericErrorVector = vector(-1.0, -1.0, -1.0);
extern const int cFloatVectorDictMaxCapacity = 999999997;
extern const float cFloatVectorDictMaxLoadFactor = 0.75;
extern const float cFloatVectorDictEmptyKey = -9999999.0;
extern const int cFloatVectorDictEmptyKeyBits = -887581057;
extern const int cFloatVectorDictCanonicalNanBits = -8388607;
extern const int cFloatVectorDictInitialCapacity = 65;
extern const int cFloatVectorDictHashConstant = 16777619;
int _floatVectorDictLastOperationStatus = cFloatVectorDictSuccess;
int _floatVectorDictTempArray = -1;

int _xsFloatVectorDictKeyBits(float key = 0.0) {
    if (key != key) {
        return (cFloatVectorDictCanonicalNanBits);
    }
    if (key == 0.0) {
        return (0);
    }
    return (bitCastToInt(key));
}

float _xsFloatVectorDictCanonicalKey(float key = 0.0) {
    return (bitCastToFloat(_xsFloatVectorDictKeyBits(key)));
}

void _xsFloatVectorDictSetSize(int dct = -1, int size = 0) {
    xsArraySetFloat(dct, 0, bitCastToFloat(size));
}

int _xsFloatVectorDictGetSize(int dct = -1) {
    return (bitCastToInt(xsArrayGetFloat(dct, 0)));
}

float _xsFloatVectorDictGetStoredKey(int dct = -1, int slot = 1) {
    return (xsArrayGetFloat(dct, slot));
}

void _xsFloatVectorDictClearSlot(int dct = -1, int slot = 1) {
    xsArraySetFloat(dct, slot, cFloatVectorDictEmptyKey);
}

void _xsFloatVectorDictSetStoredValue(int dct = -1, int slot = 1, vector value = vector(0.0, 0.0, 0.0)) {
    xsArraySetFloat(dct, slot + 1, xsVectorGetX(value));
    xsArraySetFloat(dct, slot + 2, xsVectorGetY(value));
    xsArraySetFloat(dct, slot + 3, xsVectorGetZ(value));
}

vector _xsFloatVectorDictGetStoredValue(int dct = -1, int slot = 1) {
    return (xsVectorSet(xsArrayGetFloat(dct, slot + 1), xsArrayGetFloat(dct, slot + 2), xsArrayGetFloat(dct, slot + 3)));
}

void _xsFloatVectorDictSetSlot(int dct = -1, int slot = 1, float key = 0.0, vector value = vector(0.0, 0.0, 0.0)) {
    xsArraySetFloat(dct, slot, _xsFloatVectorDictCanonicalKey(key));
    _xsFloatVectorDictSetStoredValue(dct, slot, value);
}

/*
    Creates an empty float-to-vector dictionary.
    Keys equal to `cFloatVectorDictEmptyKey` are reserved as the internal empty-slot sentinel
    and cannot be stored. `put` and `putIfAbsent` silently reject them. Signed zero keys are
    canonicalized to `0.0`, and all NaN keys are canonicalized to a single NaN bit pattern.
    @return created dict id, or `cFloatVectorDictGenericError` on error
*/
int xsFloatVectorDictCreate() {
    int dct = xsArrayCreateFloat(cFloatVectorDictInitialCapacity, cFloatVectorDictEmptyKey);
    if (dct < 0) {
        return (cFloatVectorDictGenericError);
    }
    _xsFloatVectorDictSetSize(dct, 0);
    return (dct);
}

int _xsFloatVectorDictHash(float key = 0.0, int capacity = 0) {
    int h = _xsFloatVectorDictKeyBits(key) * cFloatVectorDictHashConstant;
    int numSlots = (capacity - 1) / 4;
    h = h % numSlots;
    if (h < 0) {
        h = h + numSlots;
    }
    return ((h * 4) + 1);
}

int _xsFloatVectorDictFindSlot(int dct = -1, float key = 0.0, int capacity = 0) {
    int numSlots = (capacity - 1) / 4;
    int keyBits = _xsFloatVectorDictKeyBits(key);
    int home = _xsFloatVectorDictHash(key, capacity);
    int slot = home;
    int steps = 0;
    while (steps < numSlots) {
        float storedKey = _xsFloatVectorDictGetStoredKey(dct, slot);
        if (storedKey == cFloatVectorDictEmptyKey) {
            return (-1);
        }
        if (_xsFloatVectorDictKeyBits(storedKey) == keyBits) {
            return (slot);
        }
        slot = slot + 4;
        if (slot >= capacity) {
            slot = 1;
        }
        steps++;
    }
    return (-1);
}

vector _xsFloatVectorDictUpsert(int dct = -1, float key = 0.0, vector val = vector(0.0, 0.0, 0.0), int capacity = 0) {
    int keyBits = _xsFloatVectorDictKeyBits(key);
    int numSlots = (capacity - 1) / 4;
    int home = _xsFloatVectorDictHash(key, capacity);
    int slot = home;
    int steps = 0;
    while (steps < numSlots) {
        float storedKey = _xsFloatVectorDictGetStoredKey(dct, slot);
        if (storedKey == cFloatVectorDictEmptyKey) {
            _xsFloatVectorDictSetSlot(dct, slot, key, val);
            _floatVectorDictLastOperationStatus = cFloatVectorDictNoKeyError;
            return (cFloatVectorDictGenericErrorVector);
        }
        if (_xsFloatVectorDictKeyBits(storedKey) == keyBits) {
            vector oldVal = _xsFloatVectorDictGetStoredValue(dct, slot);
            _xsFloatVectorDictSetStoredValue(dct, slot, val);
            _floatVectorDictLastOperationStatus = cFloatVectorDictSuccess;
            return (oldVal);
        }
        slot = slot + 4;
        if (slot >= capacity) {
            slot = 1;
        }
        steps++;
    }
    _floatVectorDictLastOperationStatus = cFloatVectorDictMaxCapacityError;
    return (cFloatVectorDictGenericErrorVector);
}

int _xsFloatVectorDictMoveToTempArray(int dct = -1, int size = 0, int capacity = 0) {
    int tempDataSize = size * 4;
    if (_floatVectorDictTempArray < 0) {
        _floatVectorDictTempArray = xsArrayCreateFloat(tempDataSize, cFloatVectorDictEmptyKey);
        if (_floatVectorDictTempArray < 0) {
            return (cFloatVectorDictResizeFailedError);
        }
    } else {
        int tempArrCapacity = xsArrayGetSize(_floatVectorDictTempArray);
        if (tempArrCapacity < tempDataSize) {
            if (tempDataSize > cFloatVectorDictMaxCapacity) {
                return (cFloatVectorDictMaxCapacityError);
            }
            int r = xsArrayResizeFloat(_floatVectorDictTempArray, tempDataSize);
            if (r != 1) {
                return (cFloatVectorDictResizeFailedError);
            }
        }
    }
    int t = 0;
    int i = 1;
    while (i < capacity) {
        float storedKey = _xsFloatVectorDictGetStoredKey(dct, i);
        if (storedKey != cFloatVectorDictEmptyKey) {
            xsArraySetFloat(_floatVectorDictTempArray, t, xsArrayGetFloat(dct, i));
            xsArraySetFloat(_floatVectorDictTempArray, t + 1, xsArrayGetFloat(dct, i + 1));
            xsArraySetFloat(_floatVectorDictTempArray, t + 2, xsArrayGetFloat(dct, i + 2));
            xsArraySetFloat(_floatVectorDictTempArray, t + 3, xsArrayGetFloat(dct, i + 3));
            t = t + 4;
        }
        i = i + 4;
    }
    return (tempDataSize);
}

void _xsFloatVectorDictClearSlots(int dct = -1, int capacity = -1) {
    int j = 1;
    while (j < capacity) {
        _xsFloatVectorDictClearSlot(dct, j);
        j = j + 4;
    }
}

int _xsFloatVectorDictRehashIfNeeded(int dct = -1, int size = 0, int capacity = 0, int requiredSize = -1) {
    if (requiredSize < 0) {
        requiredSize = size;
    }
    float loadFactor = (0.0 + requiredSize) / ((capacity - 1) / 4);
    if (loadFactor > cFloatVectorDictMaxLoadFactor) {
        int storeStatus = _floatVectorDictLastOperationStatus;
        int newCapacity = ((capacity - 1) * 2) + 1;
        if (newCapacity > cFloatVectorDictMaxCapacity) {
            _floatVectorDictLastOperationStatus = cFloatVectorDictMaxCapacityError;
            return (cFloatVectorDictGenericError);
        }
        int tempDataSize = _xsFloatVectorDictMoveToTempArray(dct, size, capacity);
        if (tempDataSize < 0) {
            _floatVectorDictLastOperationStatus = tempDataSize;
            return (cFloatVectorDictGenericError);
        }
        int r = xsArrayResizeFloat(dct, newCapacity);
        if (r != 1) {
            _floatVectorDictLastOperationStatus = cFloatVectorDictResizeFailedError;
            return (cFloatVectorDictGenericError);
        }
        _xsFloatVectorDictClearSlots(dct, newCapacity);
        int t = 0;
        while (t < tempDataSize) {
            _xsFloatVectorDictUpsert(dct, xsArrayGetFloat(_floatVectorDictTempArray, t), xsVectorSet(xsArrayGetFloat(_floatVectorDictTempArray, t + 1), xsArrayGetFloat(_floatVectorDictTempArray, t + 2), xsArrayGetFloat(_floatVectorDictTempArray, t + 3)), newCapacity);
            if ((_floatVectorDictLastOperationStatus < 0) && (_floatVectorDictLastOperationStatus != cFloatVectorDictNoKeyError)) {
                return (cFloatVectorDictGenericError);
            }
            t = t + 4;
        }
        _floatVectorDictLastOperationStatus = storeStatus;
    }
    return (cFloatVectorDictSuccess);
}

/*
    Inserts or updates a key-value pair. Triggers a rehash when load factor exceeds the threshold.
    If `key` equals `cFloatVectorDictEmptyKey`, the call is a no-op and returns
    `cFloatVectorDictGenericErrorVector` with last error set to `cFloatVectorDictGenericError`.
*/
vector xsFloatVectorDictPut(int dct = -1, float key = 0.0, vector val = vector(0.0, 0.0, 0.0)) {
    if (key == cFloatVectorDictEmptyKey) {
        _floatVectorDictLastOperationStatus = cFloatVectorDictGenericError;
        return (cFloatVectorDictGenericErrorVector);
    }
    int size = _xsFloatVectorDictGetSize(dct);
    int capacity = xsArrayGetSize(dct);
    int slot = _xsFloatVectorDictFindSlot(dct, key, capacity);
    if (slot >= 0) {
        vector oldVal = _xsFloatVectorDictGetStoredValue(dct, slot);
        _xsFloatVectorDictSetStoredValue(dct, slot, val);
        _floatVectorDictLastOperationStatus = cFloatVectorDictSuccess;
        return (oldVal);
    }
    int r = _xsFloatVectorDictRehashIfNeeded(dct, size, capacity, size + 1);
    if (r != cFloatVectorDictSuccess) {
        return (cFloatVectorDictGenericErrorVector);
    }
    capacity = xsArrayGetSize(dct);
    vector previousValue = _xsFloatVectorDictUpsert(dct, key, val, capacity);
    if (_floatVectorDictLastOperationStatus == cFloatVectorDictNoKeyError) {
        _xsFloatVectorDictSetSize(dct, size + 1);
        return (cFloatVectorDictGenericErrorVector);
    }
    if (_floatVectorDictLastOperationStatus != cFloatVectorDictSuccess) {
        return (cFloatVectorDictGenericErrorVector);
    }
    return (previousValue);
}

/*
    Creates a dict with provided key-value pairs. The first key that equals
    `cFloatVectorDictEmptyKey` will stop further insertion.
*/
int xsFloatVectorDict(float k1 = cFloatVectorDictEmptyKey, vector v1 = vector(0.0, 0.0, 0.0), float k2 = cFloatVectorDictEmptyKey, vector v2 = vector(0.0, 0.0, 0.0), float k3 = cFloatVectorDictEmptyKey, vector v3 = vector(0.0, 0.0, 0.0), float k4 = cFloatVectorDictEmptyKey, vector v4 = vector(0.0, 0.0, 0.0), float k5 = cFloatVectorDictEmptyKey, vector v5 = vector(0.0, 0.0, 0.0), float k6 = cFloatVectorDictEmptyKey, vector v6 = vector(0.0, 0.0, 0.0)) {
    int dct = xsFloatVectorDictCreate();
    if (dct < 0) {
        return (cFloatVectorDictGenericError);
    }
    if (k1 == cFloatVectorDictEmptyKey) {
        return (dct);
    }
    xsFloatVectorDictPut(dct, k1, v1);
    if (k2 == cFloatVectorDictEmptyKey) {
        return (dct);
    }
    xsFloatVectorDictPut(dct, k2, v2);
    if (k3 == cFloatVectorDictEmptyKey) {
        return (dct);
    }
    xsFloatVectorDictPut(dct, k3, v3);
    if (k4 == cFloatVectorDictEmptyKey) {
        return (dct);
    }
    xsFloatVectorDictPut(dct, k4, v4);
    if (k5 == cFloatVectorDictEmptyKey) {
        return (dct);
    }
    xsFloatVectorDictPut(dct, k5, v5);
    if (k6 == cFloatVectorDictEmptyKey) {
        return (dct);
    }
    xsFloatVectorDictPut(dct, k6, v6);
    return (dct);
}

/*
    Returns the value associated with the given key. Sets last error on completion.
    @return value for the key, or `dft` if not found
*/
vector xsFloatVectorDictGet(int dct = -1, float key = 0.0, vector dft = cFloatVectorDictGenericErrorVector) {
    int capacity = xsArrayGetSize(dct);
    int slot = _xsFloatVectorDictFindSlot(dct, key, capacity);
    if (slot >= 0) {
        _floatVectorDictLastOperationStatus = cFloatVectorDictSuccess;
        return (_xsFloatVectorDictGetStoredValue(dct, slot));
    }
    _floatVectorDictLastOperationStatus = cFloatVectorDictNoKeyError;
    return (dft);
}

/*
    Removes the entry with the given key from the dict. Uses backward shift deletion to
    maintain linear probing invariant. Sets last error on completion.
    @return value that was associated with the key, or `cFloatVectorDictGenericErrorVector` if not found
*/
vector xsFloatVectorDictRemove(int dct = -1, float key = 0.0) {
    int size = _xsFloatVectorDictGetSize(dct);
    int capacity = xsArrayGetSize(dct);
    int numSlots = (capacity - 1) / 4;
    int slot = _xsFloatVectorDictFindSlot(dct, key, capacity);
    if (slot < 0) {
        _floatVectorDictLastOperationStatus = cFloatVectorDictNoKeyError;
        return (cFloatVectorDictGenericErrorVector);
    }
    vector foundVal = _xsFloatVectorDictGetStoredValue(dct, slot);
    int g = slot;
    int q = g + 4;
    if (q >= capacity) {
        q = 1;
    }
    int shiftSteps = 0;
    float qKey = _xsFloatVectorDictGetStoredKey(dct, q);
    while ((qKey != cFloatVectorDictEmptyKey) && (shiftSteps < numSlots)) {
        int qHome = _xsFloatVectorDictHash(qKey, capacity);
        int gSlot = (g - 1) / 4;
        int qSlot = (q - 1) / 4;
        int hSlot = (qHome - 1) / 4;
        int distG = ((gSlot - hSlot) + numSlots) % numSlots;
        int distQ = ((qSlot - hSlot) + numSlots) % numSlots;
        if (distG < distQ) {
            xsArraySetFloat(dct, g, xsArrayGetFloat(dct, q));
            xsArraySetFloat(dct, g + 1, xsArrayGetFloat(dct, q + 1));
            xsArraySetFloat(dct, g + 2, xsArrayGetFloat(dct, q + 2));
            xsArraySetFloat(dct, g + 3, xsArrayGetFloat(dct, q + 3));
            g = q;
        }
        q = q + 4;
        if (q >= capacity) {
            q = 1;
        }
        shiftSteps++;
        qKey = _xsFloatVectorDictGetStoredKey(dct, q);
    }
    _xsFloatVectorDictClearSlot(dct, g);
    _xsFloatVectorDictSetSize(dct, size - 1);
    _floatVectorDictLastOperationStatus = cFloatVectorDictSuccess;
    return (foundVal);
}

/*
    Checks whether the given key exists in the dict.
    @return true if the key is found, false otherwise
*/
bool xsFloatVectorDictContains(int dct = -1, float key = 0.0) {
    int capacity = xsArrayGetSize(dct);
    return (_xsFloatVectorDictFindSlot(dct, key, capacity) >= 0);
}

/*
    Returns the number of key-value pairs stored in the dict.
    @return dict size
*/
int xsFloatVectorDictSize(int dct = -1) {
    return (_xsFloatVectorDictGetSize(dct));
}

/*
    Removes all entries from the dict and shrinks storage back to the initial capacity when possible.
    @return `cFloatVectorDictSuccess` on success, or `cFloatVectorDictGenericError` on error
*/
int xsFloatVectorDictClear(int dct = -1) {
    int capacity = xsArrayGetSize(dct);
    int i = 1;
    while (i < capacity) {
        _xsFloatVectorDictClearSlot(dct, i);
        i = i + 4;
    }
    _xsFloatVectorDictSetSize(dct, 0);
    if (capacity > cFloatVectorDictInitialCapacity) {
        int r = xsArrayResizeFloat(dct, cFloatVectorDictInitialCapacity);
        if (r != 1) {
            return (cFloatVectorDictGenericError);
        }
    }
    return (cFloatVectorDictSuccess);
}

/*
    Creates a shallow copy of the dict.
    @return new dict id, or `cFloatVectorDictResizeFailedError` on error
*/
int xsFloatVectorDictCopy(int dct = -1) {
    int capacity = xsArrayGetSize(dct);
    int newDct = xsArrayCreateFloat(capacity, cFloatVectorDictEmptyKey);
    if (newDct < 0) {
        return (cFloatVectorDictResizeFailedError);
    }
    int i = 1;
    while (i < capacity) {
        float storedKey = _xsFloatVectorDictGetStoredKey(dct, i);
        if (storedKey != cFloatVectorDictEmptyKey) {
            xsArraySetFloat(newDct, i, xsArrayGetFloat(dct, i));
            xsArraySetFloat(newDct, i + 1, xsArrayGetFloat(dct, i + 1));
            xsArraySetFloat(newDct, i + 2, xsArrayGetFloat(dct, i + 2));
            xsArraySetFloat(newDct, i + 3, xsArrayGetFloat(dct, i + 3));
        }
        i = i + 4;
    }
    _xsFloatVectorDictSetSize(newDct, _xsFloatVectorDictGetSize(dct));
    return (newDct);
}

/*
    Returns a string representation of the dict.
    @return string representation of the dict
*/
string xsFloatVectorDictToString(int dct = -1) {
    int capacity = xsArrayGetSize(dct);
    string s = "{";
    bool first = true;
    int i = 1;
    while (i < capacity) {
        float key = _xsFloatVectorDictGetStoredKey(dct, i);
        if (key != cFloatVectorDictEmptyKey) {
            if (first) {
                first = false;
            } else {
                s = s + ", ";
            }
            s = s + (key + ": " + _xsFloatVectorDictGetStoredValue(dct, i));
        }
        i = i + 4;
    }
    s = s + "}";
    return (s);
}

/*
    Returns the status of the last operation that reports errors through the dict API.
    @return `cFloatVectorDictSuccess` if the last such operation succeeded, or a negative error code
*/
int xsFloatVectorDictLastError() {
    return (_floatVectorDictLastOperationStatus);
}

float _xsFloatVectorDictFindNextOccupied(int dct = -1, int start = 1, int capacity = 0) {
    int slot = start;
    while (slot < capacity) {
        float storedKey = _xsFloatVectorDictGetStoredKey(dct, slot);
        if (storedKey != cFloatVectorDictEmptyKey) {
            _floatVectorDictLastOperationStatus = cFloatVectorDictSuccess;
            return (storedKey);
        }
        slot = slot + 4;
    }
    _floatVectorDictLastOperationStatus = cFloatVectorDictNoKeyError;
    return (cFloatVectorDictEmptyKey);
}

/*
    Returns the next key in the dict for stateless iteration. Sets last error on completion.
    @param is_first - if true, returns the first key in the dict
    @param prev_key - the previous key returned by this function (ignored if `isFirst` is true)
    @return next key, or `cFloatVectorDictEmptyKey` if no more keys
        (last error set to `cFloatVectorDictNoKeyError`)
*/
float xsFloatVectorDictNextKey(int dct = -1, bool isFirst = true, float prevKey = cFloatVectorDictEmptyKey) {
    int capacity = xsArrayGetSize(dct);
    if (isFirst) {
        return (_xsFloatVectorDictFindNextOccupied(dct, 1, capacity));
    }
    int slot = _xsFloatVectorDictFindSlot(dct, prevKey, capacity);
    if (slot < 0) {
        _floatVectorDictLastOperationStatus = cFloatVectorDictNoKeyError;
        return (cFloatVectorDictEmptyKey);
    }
    int nextStart = slot + 4;
    return (_xsFloatVectorDictFindNextOccupied(dct, nextStart, capacity));
}

/*
    Checks whether there is a next key in the dict for stateless iteration.
    @param is_first - if true, checks whether the dict has any keys
    @param prev_key - the previous key (ignored if `isFirst` is true)
    @return true if there is a next key, false otherwise
*/
bool xsFloatVectorDictHasNext(int dct = -1, bool isFirst = true, float prevKey = cFloatVectorDictEmptyKey) {
    int capacity = xsArrayGetSize(dct);
    int start = 1;
    if (isFirst == false) {
        int slot = _xsFloatVectorDictFindSlot(dct, prevKey, capacity);
        if (slot < 0) {
            return (false);
        }
        start = slot + 4;
    }
    while (start < capacity) {
        if (_xsFloatVectorDictGetStoredKey(dct, start) != cFloatVectorDictEmptyKey) {
            return (true);
        }
        start = start + 4;
    }
    return (false);
}

/*
    Updates `source` with all entries from `dct`. Existing keys in `source` are overwritten.
    @return `cFloatVectorDictSuccess` on success, or a negative error code
*/
int xsFloatVectorDictUpdate(int source = -1, int dct = -1) {
    int capacity = xsArrayGetSize(dct);
    int i = 1;
    while (i < capacity) {
        float key = _xsFloatVectorDictGetStoredKey(dct, i);
        if (key != cFloatVectorDictEmptyKey) {
            xsFloatVectorDictPut(source, key, _xsFloatVectorDictGetStoredValue(dct, i));
            if ((_floatVectorDictLastOperationStatus != cFloatVectorDictSuccess) && (_floatVectorDictLastOperationStatus != cFloatVectorDictNoKeyError)) {
                return (_floatVectorDictLastOperationStatus);
            }
        }
        i = i + 4;
    }
    _floatVectorDictLastOperationStatus = cFloatVectorDictSuccess;
    return (cFloatVectorDictSuccess);
}

/*
    Inserts the key-value pair only if the key is not already present. Sets last error on completion.
    If `key` equals `cFloatVectorDictEmptyKey`, the call is a no-op and returns
    `cFloatVectorDictGenericErrorVector` with last error set to `cFloatVectorDictGenericError`.
*/
vector xsFloatVectorDictPutIfAbsent(int dct = -1, float key = 0.0, vector val = vector(0.0, 0.0, 0.0)) {
    if (key == cFloatVectorDictEmptyKey) {
        _floatVectorDictLastOperationStatus = cFloatVectorDictGenericError;
        return (cFloatVectorDictGenericErrorVector);
    }
    int size = _xsFloatVectorDictGetSize(dct);
    int capacity = xsArrayGetSize(dct);
    int slot = _xsFloatVectorDictFindSlot(dct, key, capacity);
    if (slot >= 0) {
        _floatVectorDictLastOperationStatus = cFloatVectorDictSuccess;
        return (_xsFloatVectorDictGetStoredValue(dct, slot));
    }
    int r = _xsFloatVectorDictRehashIfNeeded(dct, size, capacity, size + 1);
    if (r != cFloatVectorDictSuccess) {
        return (cFloatVectorDictGenericErrorVector);
    }
    capacity = xsArrayGetSize(dct);
    vector result = _xsFloatVectorDictUpsert(dct, key, val, capacity);
    if (_floatVectorDictLastOperationStatus == cFloatVectorDictNoKeyError) {
        _xsFloatVectorDictSetSize(dct, size + 1);
        return (cFloatVectorDictGenericErrorVector);
    }
    if (_floatVectorDictLastOperationStatus != cFloatVectorDictSuccess) {
        return (cFloatVectorDictGenericErrorVector);
    }
    return (result);
}

/*
    Returns a float array containing all keys in iteration order.
    Keys are returned in canonicalized form, so `-0.0` becomes `0.0` and NaN keys use the canonical NaN payload.
    @return array id, or `cFloatVectorDictResizeFailedError` on allocation failure
*/
int xsFloatVectorDictKeys(int dct = -1) {
    int size = _xsFloatVectorDictGetSize(dct);
    int arr = xsArrayCreateFloat(size, 0.0);
    if (arr < 0) {
        return (cFloatVectorDictResizeFailedError);
    }
    int capacity = xsArrayGetSize(dct);
    int idx = 0;
    int i = 1;
    while (i < capacity) {
        float storedKey = _xsFloatVectorDictGetStoredKey(dct, i);
        if (storedKey != cFloatVectorDictEmptyKey) {
            xsArraySetFloat(arr, idx, storedKey);
            idx++;
        }
        i = i + 4;
    }
    return (arr);
}

/*
    Returns a vector array containing all values in the same order as `xsFloatVectorDictKeys`.
    @return array id, or `cFloatVectorDictResizeFailedError` on allocation failure
*/
int xsFloatVectorDictValues(int dct = -1) {
    int size = _xsFloatVectorDictGetSize(dct);
    int arr = xsArrayCreateVector(size, vector(0.0, 0.0, 0.0));
    if (arr < 0) {
        return (cFloatVectorDictResizeFailedError);
    }
    int capacity = xsArrayGetSize(dct);
    int idx = 0;
    int i = 1;
    while (i < capacity) {
        float storedKey = _xsFloatVectorDictGetStoredKey(dct, i);
        if (storedKey != cFloatVectorDictEmptyKey) {
            xsArraySetVector(arr, idx, _xsFloatVectorDictGetStoredValue(dct, i));
            idx++;
        }
        i = i + 4;
    }
    return (arr);
}

/*
    Checks whether both dicts contain the same keys and values.
    Float keys are compared using the dict's canonical key semantics for signed zero and NaN.
    @return true if both dicts are equal, false otherwise
*/
bool xsFloatVectorDictEquals(int a = -1, int b = -1) {
    int sizeA = _xsFloatVectorDictGetSize(a);
    int sizeB = _xsFloatVectorDictGetSize(b);
    if (sizeA != sizeB) {
        return (false);
    }
    int capacity = xsArrayGetSize(a);
    int i = 1;
    while (i < capacity) {
        float key = _xsFloatVectorDictGetStoredKey(a, i);
        if (key != cFloatVectorDictEmptyKey) {
            vector val = _xsFloatVectorDictGetStoredValue(a, i);
            if (xsFloatVectorDictGet(b, key) != val) {
                return (false);
            }
            if (xsFloatVectorDictLastError() != cFloatVectorDictSuccess) {
                return (false);
            }
        }
        i = i + 4;
    }
    return (true);
}

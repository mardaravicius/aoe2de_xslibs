extern const int cVectorVectorDictSuccess = 0;
extern const int cVectorVectorDictGenericError = -1;
extern const int cVectorVectorDictNoKeyError = -2;
extern const int cVectorVectorDictResizeFailedError = -3;
extern const int cVectorVectorDictMaxCapacityError = -4;
extern const vector cVectorVectorDictGenericErrorVector = vector(-1.0, -1.0, -1.0);
extern const int cVectorVectorDictMaxCapacity = 999999997;
extern const float cVectorVectorDictMaxLoadFactor = 0.75;
extern const vector cVectorVectorDictEmptyKey = vector(-9999999.0, -9999999.0, -9999999.0);
extern const int cVectorVectorDictInitialCapacity = 97;
extern const int cVectorVectorDictHashConstant = 16777619;
int _vectorVectorDictLastOperationStatus = cVectorVectorDictSuccess;
int _vectorVectorDictTempArray = -1;

void _xsVectorVectorDictSetSize(int dct = -1, int size = 0) {
    xsArraySetFloat(dct, 0, bitCastToFloat(size));
}

int _xsVectorVectorDictGetSize(int dct = -1) {
    return (bitCastToInt(xsArrayGetFloat(dct, 0)));
}

vector _xsVectorVectorDictGetStoredKey(int dct = -1, int slot = 1) {
    return (xsVectorSet(xsArrayGetFloat(dct, slot), xsArrayGetFloat(dct, slot + 1), xsArrayGetFloat(dct, slot + 2)));
}

void _xsVectorVectorDictSetStoredKey(int dct = -1, int slot = 1, vector key = vector(0.0, 0.0, 0.0)) {
    xsArraySetFloat(dct, slot, xsVectorGetX(key));
    xsArraySetFloat(dct, slot + 1, xsVectorGetY(key));
    xsArraySetFloat(dct, slot + 2, xsVectorGetZ(key));
}

void _xsVectorVectorDictClearSlot(int dct = -1, int slot = 1) {
    _xsVectorVectorDictSetStoredKey(dct, slot, cVectorVectorDictEmptyKey);
}

void _xsVectorVectorDictSetStoredValue(int dct = -1, int slot = 1, vector value = vector(0.0, 0.0, 0.0)) {
    xsArraySetFloat(dct, slot + 3, xsVectorGetX(value));
    xsArraySetFloat(dct, slot + 4, xsVectorGetY(value));
    xsArraySetFloat(dct, slot + 5, xsVectorGetZ(value));
}

vector _xsVectorVectorDictGetStoredValue(int dct = -1, int slot = 1) {
    return (xsVectorSet(xsArrayGetFloat(dct, slot + 3), xsArrayGetFloat(dct, slot + 4), xsArrayGetFloat(dct, slot + 5)));
}

void _xsVectorVectorDictSetSlot(int dct = -1, int slot = 1, vector key = vector(0.0, 0.0, 0.0), vector value = vector(0.0, 0.0, 0.0)) {
    _xsVectorVectorDictSetStoredKey(dct, slot, key);
    _xsVectorVectorDictSetStoredValue(dct, slot, value);
}

/*
    Creates an empty vector-to-vector dictionary.
    Keys equal to `cVectorVectorDictEmptyKey` are reserved as the internal empty-slot sentinel
    and cannot be stored. `put` and `putIfAbsent` silently reject them.
    @return created dict id, or `cVectorVectorDictGenericError` on error
*/
int xsVectorVectorDictCreate() {
    int dct = xsArrayCreateFloat(cVectorVectorDictInitialCapacity, xsVectorGetX(cVectorVectorDictEmptyKey));
    if (dct < 0) {
        return (cVectorVectorDictGenericError);
    }
    int i = 2;
    while (i < cVectorVectorDictInitialCapacity) {
        xsArraySetFloat(dct, i, xsVectorGetY(cVectorVectorDictEmptyKey));
        xsArraySetFloat(dct, i + 1, xsVectorGetZ(cVectorVectorDictEmptyKey));
        i = i + 6;
    }
    _xsVectorVectorDictSetSize(dct, 0);
    return (dct);
}

int _xsVectorVectorDictHash(vector key = vector(0.0, 0.0, 0.0), int capacity = 0) {
    int h = bitCastToInt(xsVectorGetX(key)) * cVectorVectorDictHashConstant;
    h = (h + bitCastToInt(xsVectorGetY(key))) * cVectorVectorDictHashConstant;
    h = (h + bitCastToInt(xsVectorGetZ(key))) * cVectorVectorDictHashConstant;
    int numSlots = (capacity - 1) / 6;
    h = h % numSlots;
    if (h < 0) {
        h = h + numSlots;
    }
    return ((h * 6) + 1);
}

int _xsVectorVectorDictFindSlot(int dct = -1, vector key = vector(0.0, 0.0, 0.0), int capacity = 0) {
    int numSlots = (capacity - 1) / 6;
    int home = _xsVectorVectorDictHash(key, capacity);
    int slot = home;
    int steps = 0;
    while (steps < numSlots) {
        vector storedKey = _xsVectorVectorDictGetStoredKey(dct, slot);
        if (storedKey == cVectorVectorDictEmptyKey) {
            return (-1);
        }
        if (storedKey == key) {
            return (slot);
        }
        slot = slot + 6;
        if (slot >= capacity) {
            slot = 1;
        }
        steps++;
    }
    return (-1);
}

vector _xsVectorVectorDictUpsert(int dct = -1, vector key = vector(0.0, 0.0, 0.0), vector val = vector(0.0, 0.0, 0.0), int capacity = 0) {
    int numSlots = (capacity - 1) / 6;
    int home = _xsVectorVectorDictHash(key, capacity);
    int slot = home;
    int steps = 0;
    while (steps < numSlots) {
        vector storedKey = _xsVectorVectorDictGetStoredKey(dct, slot);
        if (storedKey == cVectorVectorDictEmptyKey) {
            _xsVectorVectorDictSetSlot(dct, slot, key, val);
            _vectorVectorDictLastOperationStatus = cVectorVectorDictNoKeyError;
            return (cVectorVectorDictGenericErrorVector);
        }
        if (storedKey == key) {
            vector oldVal = _xsVectorVectorDictGetStoredValue(dct, slot);
            _xsVectorVectorDictSetStoredValue(dct, slot, val);
            _vectorVectorDictLastOperationStatus = cVectorVectorDictSuccess;
            return (oldVal);
        }
        slot = slot + 6;
        if (slot >= capacity) {
            slot = 1;
        }
        steps++;
    }
    _vectorVectorDictLastOperationStatus = cVectorVectorDictMaxCapacityError;
    return (cVectorVectorDictGenericErrorVector);
}

int _xsVectorVectorDictMoveToTempArray(int dct = -1, int size = 0, int capacity = 0) {
    int tempDataSize = size * 6;
    if (_vectorVectorDictTempArray < 0) {
        _vectorVectorDictTempArray = xsArrayCreateFloat(tempDataSize, xsVectorGetX(cVectorVectorDictEmptyKey));
        if (_vectorVectorDictTempArray < 0) {
            return (cVectorVectorDictResizeFailedError);
        }
    } else {
        int tempArrCapacity = xsArrayGetSize(_vectorVectorDictTempArray);
        if (tempArrCapacity < tempDataSize) {
            if (tempDataSize > cVectorVectorDictMaxCapacity) {
                return (cVectorVectorDictMaxCapacityError);
            }
            int r = xsArrayResizeFloat(_vectorVectorDictTempArray, tempDataSize);
            if (r != 1) {
                return (cVectorVectorDictResizeFailedError);
            }
        }
    }
    int tempIdx = 2;
    while (tempIdx < tempDataSize) {
        xsArraySetFloat(_vectorVectorDictTempArray, tempIdx, xsVectorGetY(cVectorVectorDictEmptyKey));
        xsArraySetFloat(_vectorVectorDictTempArray, tempIdx + 1, xsVectorGetZ(cVectorVectorDictEmptyKey));
        tempIdx = tempIdx + 6;
    }
    int t = 0;
    int slotIdx = 1;
    while (slotIdx < capacity) {
        vector storedKey = _xsVectorVectorDictGetStoredKey(dct, slotIdx);
        if (storedKey != cVectorVectorDictEmptyKey) {
            xsArraySetFloat(_vectorVectorDictTempArray, t, xsArrayGetFloat(dct, slotIdx));
            xsArraySetFloat(_vectorVectorDictTempArray, t + 1, xsArrayGetFloat(dct, slotIdx + 1));
            xsArraySetFloat(_vectorVectorDictTempArray, t + 2, xsArrayGetFloat(dct, slotIdx + 2));
            xsArraySetFloat(_vectorVectorDictTempArray, t + 3, xsArrayGetFloat(dct, slotIdx + 3));
            xsArraySetFloat(_vectorVectorDictTempArray, t + 4, xsArrayGetFloat(dct, slotIdx + 4));
            xsArraySetFloat(_vectorVectorDictTempArray, t + 5, xsArrayGetFloat(dct, slotIdx + 5));
            t = t + 6;
        }
        slotIdx = slotIdx + 6;
    }
    return (tempDataSize);
}

void _xsVectorVectorDictClearSlots(int dct = -1, int capacity = -1) {
    int j = 1;
    while (j < capacity) {
        _xsVectorVectorDictClearSlot(dct, j);
        j = j + 6;
    }
}

int _xsVectorVectorDictRehashIfNeeded(int dct = -1, int size = 0, int capacity = 0, int requiredSize = -1) {
    if (requiredSize < 0) {
        requiredSize = size;
    }
    float loadFactor = (0.0 + requiredSize) / ((capacity - 1) / 6);
    if (loadFactor > cVectorVectorDictMaxLoadFactor) {
        int storeStatus = _vectorVectorDictLastOperationStatus;
        int newCapacity = ((capacity - 1) * 2) + 1;
        if (newCapacity > cVectorVectorDictMaxCapacity) {
            _vectorVectorDictLastOperationStatus = cVectorVectorDictMaxCapacityError;
            return (cVectorVectorDictGenericError);
        }
        int tempDataSize = _xsVectorVectorDictMoveToTempArray(dct, size, capacity);
        if (tempDataSize < 0) {
            _vectorVectorDictLastOperationStatus = tempDataSize;
            return (cVectorVectorDictGenericError);
        }
        int r = xsArrayResizeFloat(dct, newCapacity);
        if (r != 1) {
            _vectorVectorDictLastOperationStatus = cVectorVectorDictResizeFailedError;
            return (cVectorVectorDictGenericError);
        }
        _xsVectorVectorDictClearSlots(dct, newCapacity);
        int t = 0;
        while (t < tempDataSize) {
            _xsVectorVectorDictUpsert(dct, xsVectorSet(xsArrayGetFloat(_vectorVectorDictTempArray, t), xsArrayGetFloat(_vectorVectorDictTempArray, t + 1), xsArrayGetFloat(_vectorVectorDictTempArray, t + 2)), xsVectorSet(xsArrayGetFloat(_vectorVectorDictTempArray, t + 3), xsArrayGetFloat(_vectorVectorDictTempArray, t + 4), xsArrayGetFloat(_vectorVectorDictTempArray, t + 5)), newCapacity);
            if ((_vectorVectorDictLastOperationStatus < 0) && (_vectorVectorDictLastOperationStatus != cVectorVectorDictNoKeyError)) {
                return (cVectorVectorDictGenericError);
            }
            t = t + 6;
        }
        _vectorVectorDictLastOperationStatus = storeStatus;
    }
    return (cVectorVectorDictSuccess);
}

/*
    Inserts or updates a key-value pair. Triggers a rehash when load factor exceeds the threshold.
    If `key` equals `cVectorVectorDictEmptyKey`, the call is a no-op and returns
    `cVectorVectorDictGenericErrorVector` with last error set to `cVectorVectorDictGenericError`.
*/
vector xsVectorVectorDictPut(int dct = -1, vector key = vector(0.0, 0.0, 0.0), vector val = vector(0.0, 0.0, 0.0)) {
    if (key == cVectorVectorDictEmptyKey) {
        _vectorVectorDictLastOperationStatus = cVectorVectorDictGenericError;
        return (cVectorVectorDictGenericErrorVector);
    }
    int size = _xsVectorVectorDictGetSize(dct);
    int capacity = xsArrayGetSize(dct);
    int slot = _xsVectorVectorDictFindSlot(dct, key, capacity);
    if (slot >= 0) {
        vector oldVal = _xsVectorVectorDictGetStoredValue(dct, slot);
        _xsVectorVectorDictSetStoredValue(dct, slot, val);
        _vectorVectorDictLastOperationStatus = cVectorVectorDictSuccess;
        return (oldVal);
    }
    int r = _xsVectorVectorDictRehashIfNeeded(dct, size, capacity, size + 1);
    if (r != cVectorVectorDictSuccess) {
        return (cVectorVectorDictGenericErrorVector);
    }
    capacity = xsArrayGetSize(dct);
    vector previousValue = _xsVectorVectorDictUpsert(dct, key, val, capacity);
    if (_vectorVectorDictLastOperationStatus == cVectorVectorDictNoKeyError) {
        _xsVectorVectorDictSetSize(dct, size + 1);
        return (cVectorVectorDictGenericErrorVector);
    }
    if (_vectorVectorDictLastOperationStatus != cVectorVectorDictSuccess) {
        return (cVectorVectorDictGenericErrorVector);
    }
    return (previousValue);
}

/*
    Creates a dict with provided key-value pairs. The first key that equals
    `cVectorVectorDictEmptyKey` will stop further insertion.
*/
int xsVectorVectorDict(vector k1 = cVectorVectorDictEmptyKey, vector v1 = vector(0.0, 0.0, 0.0), vector k2 = cVectorVectorDictEmptyKey, vector v2 = vector(0.0, 0.0, 0.0), vector k3 = cVectorVectorDictEmptyKey, vector v3 = vector(0.0, 0.0, 0.0), vector k4 = cVectorVectorDictEmptyKey, vector v4 = vector(0.0, 0.0, 0.0), vector k5 = cVectorVectorDictEmptyKey, vector v5 = vector(0.0, 0.0, 0.0), vector k6 = cVectorVectorDictEmptyKey, vector v6 = vector(0.0, 0.0, 0.0)) {
    int dct = xsVectorVectorDictCreate();
    if (dct < 0) {
        return (cVectorVectorDictGenericError);
    }
    if (k1 == cVectorVectorDictEmptyKey) {
        return (dct);
    }
    xsVectorVectorDictPut(dct, k1, v1);
    if (k2 == cVectorVectorDictEmptyKey) {
        return (dct);
    }
    xsVectorVectorDictPut(dct, k2, v2);
    if (k3 == cVectorVectorDictEmptyKey) {
        return (dct);
    }
    xsVectorVectorDictPut(dct, k3, v3);
    if (k4 == cVectorVectorDictEmptyKey) {
        return (dct);
    }
    xsVectorVectorDictPut(dct, k4, v4);
    if (k5 == cVectorVectorDictEmptyKey) {
        return (dct);
    }
    xsVectorVectorDictPut(dct, k5, v5);
    if (k6 == cVectorVectorDictEmptyKey) {
        return (dct);
    }
    xsVectorVectorDictPut(dct, k6, v6);
    return (dct);
}

/*
    Returns the value associated with the given key. Sets last error on completion.
*/
vector xsVectorVectorDictGet(int dct = -1, vector key = vector(0.0, 0.0, 0.0), vector dft = cVectorVectorDictGenericErrorVector) {
    int capacity = xsArrayGetSize(dct);
    int slot = _xsVectorVectorDictFindSlot(dct, key, capacity);
    if (slot >= 0) {
        _vectorVectorDictLastOperationStatus = cVectorVectorDictSuccess;
        return (_xsVectorVectorDictGetStoredValue(dct, slot));
    }
    _vectorVectorDictLastOperationStatus = cVectorVectorDictNoKeyError;
    return (dft);
}

/*
    Removes the entry with the given key from the dict. Uses backward shift deletion to
    maintain linear probing invariant.
*/
vector xsVectorVectorDictRemove(int dct = -1, vector key = vector(0.0, 0.0, 0.0)) {
    int size = _xsVectorVectorDictGetSize(dct);
    int capacity = xsArrayGetSize(dct);
    int numSlots = (capacity - 1) / 6;
    int slot = _xsVectorVectorDictFindSlot(dct, key, capacity);
    if (slot < 0) {
        _vectorVectorDictLastOperationStatus = cVectorVectorDictNoKeyError;
        return (cVectorVectorDictGenericErrorVector);
    }
    vector foundVal = _xsVectorVectorDictGetStoredValue(dct, slot);
    int g = slot;
    int q = g + 6;
    if (q >= capacity) {
        q = 1;
    }
    int shiftSteps = 0;
    vector qKey = _xsVectorVectorDictGetStoredKey(dct, q);
    while ((qKey != cVectorVectorDictEmptyKey) && (shiftSteps < numSlots)) {
        int qHome = _xsVectorVectorDictHash(qKey, capacity);
        int gSlot = (g - 1) / 6;
        int qSlot = (q - 1) / 6;
        int hSlot = (qHome - 1) / 6;
        int distG = ((gSlot - hSlot) + numSlots) % numSlots;
        int distQ = ((qSlot - hSlot) + numSlots) % numSlots;
        if (distG < distQ) {
            xsArraySetFloat(dct, g, xsArrayGetFloat(dct, q));
            xsArraySetFloat(dct, g + 1, xsArrayGetFloat(dct, q + 1));
            xsArraySetFloat(dct, g + 2, xsArrayGetFloat(dct, q + 2));
            xsArraySetFloat(dct, g + 3, xsArrayGetFloat(dct, q + 3));
            xsArraySetFloat(dct, g + 4, xsArrayGetFloat(dct, q + 4));
            xsArraySetFloat(dct, g + 5, xsArrayGetFloat(dct, q + 5));
            g = q;
        }
        q = q + 6;
        if (q >= capacity) {
            q = 1;
        }
        shiftSteps++;
        qKey = _xsVectorVectorDictGetStoredKey(dct, q);
    }
    _xsVectorVectorDictClearSlot(dct, g);
    _xsVectorVectorDictSetSize(dct, size - 1);
    _vectorVectorDictLastOperationStatus = cVectorVectorDictSuccess;
    return (foundVal);
}

bool xsVectorVectorDictContains(int dct = -1, vector key = vector(0.0, 0.0, 0.0)) {
    int capacity = xsArrayGetSize(dct);
    return (_xsVectorVectorDictFindSlot(dct, key, capacity) >= 0);
}

int xsVectorVectorDictSize(int dct = -1) {
    return (_xsVectorVectorDictGetSize(dct));
}

/*
    Removes all entries from the dict and shrinks the backing array.
*/
int xsVectorVectorDictClear(int dct = -1) {
    int capacity = xsArrayGetSize(dct);
    int i = 1;
    while (i < capacity) {
        _xsVectorVectorDictClearSlot(dct, i);
        i = i + 6;
    }
    _xsVectorVectorDictSetSize(dct, 0);
    if (capacity > cVectorVectorDictInitialCapacity) {
        int r = xsArrayResizeFloat(dct, cVectorVectorDictInitialCapacity);
        if (r != 1) {
            return (cVectorVectorDictGenericError);
        }
    }
    return (cVectorVectorDictSuccess);
}

/*
    Returns a deep copy of the dict.
*/
int xsVectorVectorDictCopy(int dct = -1) {
    int capacity = xsArrayGetSize(dct);
    int newDct = xsArrayCreateFloat(capacity, xsVectorGetX(cVectorVectorDictEmptyKey));
    if (newDct < 0) {
        return (cVectorVectorDictResizeFailedError);
    }
    int tempIdx = 2;
    while (tempIdx < capacity) {
        xsArraySetFloat(newDct, tempIdx, xsVectorGetY(cVectorVectorDictEmptyKey));
        xsArraySetFloat(newDct, tempIdx + 1, xsVectorGetZ(cVectorVectorDictEmptyKey));
        tempIdx = tempIdx + 6;
    }
    int slotIdx = 1;
    while (slotIdx < capacity) {
        vector storedKey = _xsVectorVectorDictGetStoredKey(dct, slotIdx);
        if (storedKey != cVectorVectorDictEmptyKey) {
            xsArraySetFloat(newDct, slotIdx, xsArrayGetFloat(dct, slotIdx));
            xsArraySetFloat(newDct, slotIdx + 1, xsArrayGetFloat(dct, slotIdx + 1));
            xsArraySetFloat(newDct, slotIdx + 2, xsArrayGetFloat(dct, slotIdx + 2));
            xsArraySetFloat(newDct, slotIdx + 3, xsArrayGetFloat(dct, slotIdx + 3));
            xsArraySetFloat(newDct, slotIdx + 4, xsArrayGetFloat(dct, slotIdx + 4));
            xsArraySetFloat(newDct, slotIdx + 5, xsArrayGetFloat(dct, slotIdx + 5));
        }
        slotIdx = slotIdx + 6;
    }
    _xsVectorVectorDictSetSize(newDct, _xsVectorVectorDictGetSize(dct));
    return (newDct);
}

/*
    Returns a string representation of the dict in the format `{(x1, y1, z1) - (a1, b1, c1), ...}`.
*/
string xsVectorVectorDictToString(int dct = -1) {
    int capacity = xsArrayGetSize(dct);
    string s = "{";
    bool first = true;
    int i = 1;
    while (i < capacity) {
        vector key = _xsVectorVectorDictGetStoredKey(dct, i);
        if (key != cVectorVectorDictEmptyKey) {
            if (first) {
                first = false;
            } else {
                s = s + ", ";
            }
            s = s + (("" + key) + ": " + _xsVectorVectorDictGetStoredValue(dct, i));
        }
        i = i + 6;
    }
    s = s + "}";
    return (s);
}

int xsVectorVectorDictLastError() {
    return (_vectorVectorDictLastOperationStatus);
}

vector _xsVectorVectorDictFindNextOccupied(int dct = -1, int start = 1, int capacity = 0) {
    int slot = start;
    while (slot < capacity) {
        vector storedKey = _xsVectorVectorDictGetStoredKey(dct, slot);
        if (storedKey != cVectorVectorDictEmptyKey) {
            _vectorVectorDictLastOperationStatus = cVectorVectorDictSuccess;
            return (storedKey);
        }
        slot = slot + 6;
    }
    _vectorVectorDictLastOperationStatus = cVectorVectorDictNoKeyError;
    return (cVectorVectorDictGenericErrorVector);
}

/*
    Returns the next key in the dict for stateless iteration. Sets last error on completion.
*/
vector xsVectorVectorDictNextKey(int dct = -1, bool isFirst = true, vector prevKey = cVectorVectorDictEmptyKey) {
    int capacity = xsArrayGetSize(dct);
    if (isFirst) {
        return (_xsVectorVectorDictFindNextOccupied(dct, 1, capacity));
    }
    int slot = _xsVectorVectorDictFindSlot(dct, prevKey, capacity);
    if (slot < 0) {
        _vectorVectorDictLastOperationStatus = cVectorVectorDictNoKeyError;
        return (cVectorVectorDictGenericErrorVector);
    }
    int nextStart = slot + 6;
    return (_xsVectorVectorDictFindNextOccupied(dct, nextStart, capacity));
}

bool xsVectorVectorDictHasNext(int dct = -1, bool isFirst = true, vector prevKey = cVectorVectorDictEmptyKey) {
    int capacity = xsArrayGetSize(dct);
    int start = 1;
    if (isFirst == false) {
        int slot = _xsVectorVectorDictFindSlot(dct, prevKey, capacity);
        if (slot < 0) {
            return (false);
        }
        start = slot + 6;
    }
    while (start < capacity) {
        if (_xsVectorVectorDictGetStoredKey(dct, start) != cVectorVectorDictEmptyKey) {
            return (true);
        }
        start = start + 6;
    }
    return (false);
}

/*
    Inserts all key-value pairs from another dict into the source dict, overwriting existing keys.
*/
int xsVectorVectorDictUpdate(int source = -1, int dct = -1) {
    int capacity = xsArrayGetSize(dct);
    int i = 1;
    while (i < capacity) {
        vector key = _xsVectorVectorDictGetStoredKey(dct, i);
        if (key != cVectorVectorDictEmptyKey) {
            xsVectorVectorDictPut(source, key, _xsVectorVectorDictGetStoredValue(dct, i));
            if ((_vectorVectorDictLastOperationStatus != cVectorVectorDictSuccess) && (_vectorVectorDictLastOperationStatus != cVectorVectorDictNoKeyError)) {
                return (_vectorVectorDictLastOperationStatus);
            }
        }
        i = i + 6;
    }
    _vectorVectorDictLastOperationStatus = cVectorVectorDictSuccess;
    return (cVectorVectorDictSuccess);
}

/*
    Inserts the key-value pair only if the key is not already present. Sets last error on completion.
*/
vector xsVectorVectorDictPutIfAbsent(int dct = -1, vector key = vector(0.0, 0.0, 0.0), vector val = vector(0.0, 0.0, 0.0)) {
    if (key == cVectorVectorDictEmptyKey) {
        _vectorVectorDictLastOperationStatus = cVectorVectorDictGenericError;
        return (cVectorVectorDictGenericErrorVector);
    }
    int size = _xsVectorVectorDictGetSize(dct);
    int capacity = xsArrayGetSize(dct);
    int slot = _xsVectorVectorDictFindSlot(dct, key, capacity);
    if (slot >= 0) {
        _vectorVectorDictLastOperationStatus = cVectorVectorDictSuccess;
        return (_xsVectorVectorDictGetStoredValue(dct, slot));
    }
    int r = _xsVectorVectorDictRehashIfNeeded(dct, size, capacity, size + 1);
    if (r != cVectorVectorDictSuccess) {
        return (cVectorVectorDictGenericErrorVector);
    }
    capacity = xsArrayGetSize(dct);
    vector result = _xsVectorVectorDictUpsert(dct, key, val, capacity);
    if (_vectorVectorDictLastOperationStatus == cVectorVectorDictNoKeyError) {
        _xsVectorVectorDictSetSize(dct, size + 1);
        return (cVectorVectorDictGenericErrorVector);
    }
    if (_vectorVectorDictLastOperationStatus != cVectorVectorDictSuccess) {
        return (cVectorVectorDictGenericErrorVector);
    }
    return (result);
}

/*
    Returns a new vector array containing all keys in the dict. Order is arbitrary.
*/
int xsVectorVectorDictKeys(int dct = -1) {
    int size = _xsVectorVectorDictGetSize(dct);
    int arr = xsArrayCreateVector(size, vector(0.0, 0.0, 0.0));
    if (arr < 0) {
        return (cVectorVectorDictResizeFailedError);
    }
    int capacity = xsArrayGetSize(dct);
    int idx = 0;
    int i = 1;
    while (i < capacity) {
        vector storedKey = _xsVectorVectorDictGetStoredKey(dct, i);
        if (storedKey != cVectorVectorDictEmptyKey) {
            xsArraySetVector(arr, idx, storedKey);
            idx++;
        }
        i = i + 6;
    }
    return (arr);
}

/*
    Returns a new vector array containing all values in the dict. Order matches `xsVectorVectorDictKeys`.
*/
int xsVectorVectorDictValues(int dct = -1) {
    int size = _xsVectorVectorDictGetSize(dct);
    int arr = xsArrayCreateVector(size, vector(0.0, 0.0, 0.0));
    if (arr < 0) {
        return (cVectorVectorDictResizeFailedError);
    }
    int capacity = xsArrayGetSize(dct);
    int idx = 0;
    int i = 1;
    while (i < capacity) {
        vector storedKey = _xsVectorVectorDictGetStoredKey(dct, i);
        if (storedKey != cVectorVectorDictEmptyKey) {
            xsArraySetVector(arr, idx, _xsVectorVectorDictGetStoredValue(dct, i));
            idx++;
        }
        i = i + 6;
    }
    return (arr);
}

/*
    Returns true if both dicts contain the same key-value pairs.
*/
bool xsVectorVectorDictEquals(int a = -1, int b = -1) {
    int sizeA = _xsVectorVectorDictGetSize(a);
    int sizeB = _xsVectorVectorDictGetSize(b);
    if (sizeA != sizeB) {
        return (false);
    }
    int capacity = xsArrayGetSize(a);
    int i = 1;
    while (i < capacity) {
        vector key = _xsVectorVectorDictGetStoredKey(a, i);
        if (key != cVectorVectorDictEmptyKey) {
            vector val = _xsVectorVectorDictGetStoredValue(a, i);
            if (xsVectorVectorDictGet(b, key) != val) {
                return (false);
            }
            if (xsVectorVectorDictLastError() != cVectorVectorDictSuccess) {
                return (false);
            }
        }
        i = i + 6;
    }
    return (true);
}

extern const int cVectorIntDictSuccess = 0;
extern const int cVectorIntDictGenericError = -1;
extern const int cVectorIntDictNoKeyError = -2;
extern const int cVectorIntDictResizeFailedError = -3;
extern const int cVectorIntDictMaxCapacityError = -4;
extern const vector cVectorIntDictGenericErrorVector = vector(-1.0, -1.0, -1.0);
extern const int cVectorIntDictMaxCapacity = 999999997;
extern const float cVectorIntDictMaxLoadFactor = 0.75;
extern const vector cVectorIntDictEmptyKey = vector(-9999999.0, -9999999.0, -9999999.0);
extern const int cVectorIntDictInitialCapacity = 65;
extern const int cVectorIntDictHashConstant = 16777619;
int _vectorIntDictLastOperationStatus = cVectorIntDictSuccess;
int _vectorIntDictTempArray = -1;

void _xsVectorIntDictSetSize(int dct = -1, int size = 0) {
    xsArraySetFloat(dct, 0, bitCastToFloat(size));
}

int _xsVectorIntDictGetSize(int dct = -1) {
    return (bitCastToInt(xsArrayGetFloat(dct, 0)));
}

vector _xsVectorIntDictGetStoredKey(int dct = -1, int slot = 1) {
    return (xsVectorSet(xsArrayGetFloat(dct, slot), xsArrayGetFloat(dct, slot + 1), xsArrayGetFloat(dct, slot + 2)));
}

void _xsVectorIntDictSetStoredKey(int dct = -1, int slot = 1, vector key = vector(0.0, 0.0, 0.0)) {
    xsArraySetFloat(dct, slot, xsVectorGetX(key));
    xsArraySetFloat(dct, slot + 1, xsVectorGetY(key));
    xsArraySetFloat(dct, slot + 2, xsVectorGetZ(key));
}

void _xsVectorIntDictClearSlot(int dct = -1, int slot = 1) {
    _xsVectorIntDictSetStoredKey(dct, slot, cVectorIntDictEmptyKey);
}

void _xsVectorIntDictSetStoredValue(int dct = -1, int slot = 1, int val = 0) {
    xsArraySetFloat(dct, slot + 3, bitCastToFloat(val));
}

int _xsVectorIntDictGetStoredValue(int dct = -1, int slot = 1) {
    return (bitCastToInt(xsArrayGetFloat(dct, slot + 3)));
}

void _xsVectorIntDictSetSlot(int dct = -1, int slot = 1, vector key = vector(0.0, 0.0, 0.0), int val = 0) {
    _xsVectorIntDictSetStoredKey(dct, slot, key);
    _xsVectorIntDictSetStoredValue(dct, slot, val);
}

/*
    Creates an empty vector-to-int dictionary.
    Keys equal to `cVectorIntDictEmptyKey` are reserved as the internal empty-slot sentinel
    and cannot be stored. `put` and `putIfAbsent` silently reject them.
    @return created dict id, or `cVectorIntDictGenericError` on error
*/
int xsVectorIntDictCreate() {
    int dct = xsArrayCreateFloat(cVectorIntDictInitialCapacity, xsVectorGetX(cVectorIntDictEmptyKey));
    if (dct < 0) {
        return (cVectorIntDictGenericError);
    }
    int i = 2;
    while (i < cVectorIntDictInitialCapacity) {
        xsArraySetFloat(dct, i, xsVectorGetY(cVectorIntDictEmptyKey));
        xsArraySetFloat(dct, i + 1, xsVectorGetZ(cVectorIntDictEmptyKey));
        i = i + 4;
    }
    _xsVectorIntDictSetSize(dct, 0);
    return (dct);
}

int _xsVectorIntDictHash(vector key = vector(0.0, 0.0, 0.0), int capacity = 0) {
    int hash = bitCastToInt(xsVectorGetX(key)) * cVectorIntDictHashConstant;
    hash = (hash + bitCastToInt(xsVectorGetY(key))) * cVectorIntDictHashConstant;
    hash = (hash + bitCastToInt(xsVectorGetZ(key))) * cVectorIntDictHashConstant;
    int numSlots = (capacity - 1) / 4;
    hash = hash % numSlots;
    if (hash < 0) {
        hash = hash + numSlots;
    }
    return ((hash * 4) + 1);
}

int _xsVectorIntDictFindSlot(int dct = -1, vector key = vector(0.0, 0.0, 0.0), int capacity = 0) {
    int numSlots = (capacity - 1) / 4;
    int home = _xsVectorIntDictHash(key, capacity);
    int slot = home;
    int steps = 0;
    while (steps < numSlots) {
        vector storedKey = _xsVectorIntDictGetStoredKey(dct, slot);
        if (storedKey == cVectorIntDictEmptyKey) {
            return (-1);
        }
        if (storedKey == key) {
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

int _xsVectorIntDictUpsert(int dct = -1, vector key = vector(0.0, 0.0, 0.0), int val = 0, int capacity = 0) {
    int numSlots = (capacity - 1) / 4;
    int home = _xsVectorIntDictHash(key, capacity);
    int slot = home;
    int steps = 0;
    while (steps < numSlots) {
        vector storedKey = _xsVectorIntDictGetStoredKey(dct, slot);
        if (storedKey == cVectorIntDictEmptyKey) {
            _xsVectorIntDictSetSlot(dct, slot, key, val);
            _vectorIntDictLastOperationStatus = cVectorIntDictNoKeyError;
            return (cVectorIntDictGenericError);
        }
        if (storedKey == key) {
            int oldVal = _xsVectorIntDictGetStoredValue(dct, slot);
            _xsVectorIntDictSetStoredValue(dct, slot, val);
            _vectorIntDictLastOperationStatus = cVectorIntDictSuccess;
            return (oldVal);
        }
        slot = slot + 4;
        if (slot >= capacity) {
            slot = 1;
        }
        steps++;
    }
    _vectorIntDictLastOperationStatus = cVectorIntDictMaxCapacityError;
    return (cVectorIntDictGenericError);
}

int _xsVectorIntDictMoveToTempArray(int dct = -1, int size = 0, int capacity = 0) {
    int tempDataSize = size * 4;
    if (_vectorIntDictTempArray < 0) {
        _vectorIntDictTempArray = xsArrayCreateFloat(tempDataSize, xsVectorGetX(cVectorIntDictEmptyKey));
        if (_vectorIntDictTempArray < 0) {
            return (cVectorIntDictResizeFailedError);
        }
    } else {
        int tempArrCapacity = xsArrayGetSize(_vectorIntDictTempArray);
        if (tempArrCapacity < tempDataSize) {
            if (tempDataSize > cVectorIntDictMaxCapacity) {
                return (cVectorIntDictMaxCapacityError);
            }
            int r = xsArrayResizeFloat(_vectorIntDictTempArray, tempDataSize);
            if (r != 1) {
                return (cVectorIntDictResizeFailedError);
            }
        }
    }
    int tempIdx = 2;
    while (tempIdx < tempDataSize) {
        xsArraySetFloat(_vectorIntDictTempArray, tempIdx, xsVectorGetY(cVectorIntDictEmptyKey));
        xsArraySetFloat(_vectorIntDictTempArray, tempIdx + 1, xsVectorGetZ(cVectorIntDictEmptyKey));
        tempIdx = tempIdx + 4;
    }
    int t = 0;
    int slotIdx = 1;
    while (slotIdx < capacity) {
        vector storedKey = _xsVectorIntDictGetStoredKey(dct, slotIdx);
        if (storedKey != cVectorIntDictEmptyKey) {
            xsArraySetFloat(_vectorIntDictTempArray, t, xsArrayGetFloat(dct, slotIdx));
            xsArraySetFloat(_vectorIntDictTempArray, t + 1, xsArrayGetFloat(dct, slotIdx + 1));
            xsArraySetFloat(_vectorIntDictTempArray, t + 2, xsArrayGetFloat(dct, slotIdx + 2));
            xsArraySetFloat(_vectorIntDictTempArray, t + 3, xsArrayGetFloat(dct, slotIdx + 3));
            t = t + 4;
        }
        slotIdx = slotIdx + 4;
    }
    return (tempDataSize);
}

void _xsVectorIntDictClearSlots(int dct = -1, int capacity = -1) {
    int j = 1;
    while (j < capacity) {
        _xsVectorIntDictClearSlot(dct, j);
        j = j + 4;
    }
}

int _xsVectorIntDictRehashIfNeeded(int dct = -1, int size = 0, int capacity = 0, int requiredSize = -1) {
    if (requiredSize < 0) {
        requiredSize = size;
    }
    float loadFactor = (0.0 + requiredSize) / ((capacity - 1) / 4);
    if (loadFactor > cVectorIntDictMaxLoadFactor) {
        int storeStatus = _vectorIntDictLastOperationStatus;
        int newCapacity = ((capacity - 1) * 2) + 1;
        if (newCapacity > cVectorIntDictMaxCapacity) {
            _vectorIntDictLastOperationStatus = cVectorIntDictMaxCapacityError;
            return (cVectorIntDictGenericError);
        }
        int tempDataSize = _xsVectorIntDictMoveToTempArray(dct, size, capacity);
        if (tempDataSize < 0) {
            _vectorIntDictLastOperationStatus = tempDataSize;
            return (cVectorIntDictGenericError);
        }
        int r = xsArrayResizeFloat(dct, newCapacity);
        if (r != 1) {
            _vectorIntDictLastOperationStatus = cVectorIntDictResizeFailedError;
            return (cVectorIntDictGenericError);
        }
        _xsVectorIntDictClearSlots(dct, newCapacity);
        int t = 0;
        while (t < tempDataSize) {
            _xsVectorIntDictUpsert(dct, xsVectorSet(xsArrayGetFloat(_vectorIntDictTempArray, t), xsArrayGetFloat(_vectorIntDictTempArray, t + 1), xsArrayGetFloat(_vectorIntDictTempArray, t + 2)), bitCastToInt(xsArrayGetFloat(_vectorIntDictTempArray, t + 3)), newCapacity);
            if ((_vectorIntDictLastOperationStatus < 0) && (_vectorIntDictLastOperationStatus != cVectorIntDictNoKeyError)) {
                return (cVectorIntDictGenericError);
            }
            t = t + 4;
        }
        _vectorIntDictLastOperationStatus = storeStatus;
    }
    return (cVectorIntDictSuccess);
}

/*
    Inserts or updates a key-value pair. Triggers a rehash when load factor exceeds the threshold.
    If `key` equals `cVectorIntDictEmptyKey`, the call is a no-op and returns
    `cVectorIntDictGenericError` with last error set to `cVectorIntDictGenericError`.
*/
int xsVectorIntDictPut(int dct = -1, vector key = vector(0.0, 0.0, 0.0), int val = 0) {
    if (key == cVectorIntDictEmptyKey) {
        _vectorIntDictLastOperationStatus = cVectorIntDictGenericError;
        return (cVectorIntDictGenericError);
    }
    int size = _xsVectorIntDictGetSize(dct);
    int capacity = xsArrayGetSize(dct);
    int slot = _xsVectorIntDictFindSlot(dct, key, capacity);
    if (slot >= 0) {
        int oldVal = _xsVectorIntDictGetStoredValue(dct, slot);
        _xsVectorIntDictSetStoredValue(dct, slot, val);
        _vectorIntDictLastOperationStatus = cVectorIntDictSuccess;
        return (oldVal);
    }
    int r = _xsVectorIntDictRehashIfNeeded(dct, size, capacity, size + 1);
    if (r != cVectorIntDictSuccess) {
        return (cVectorIntDictGenericError);
    }
    capacity = xsArrayGetSize(dct);
    int previousValue = _xsVectorIntDictUpsert(dct, key, val, capacity);
    if (_vectorIntDictLastOperationStatus == cVectorIntDictNoKeyError) {
        _xsVectorIntDictSetSize(dct, size + 1);
        return (cVectorIntDictGenericError);
    }
    if (_vectorIntDictLastOperationStatus != cVectorIntDictSuccess) {
        return (cVectorIntDictGenericError);
    }
    return (previousValue);
}

/*
    Creates a dict with provided key-value pairs. The first key that equals
    `cVectorIntDictEmptyKey` will stop further insertion.
*/
int xsVectorIntDict(vector k1 = cVectorIntDictEmptyKey, int v1 = 0, vector k2 = cVectorIntDictEmptyKey, int v2 = 0, vector k3 = cVectorIntDictEmptyKey, int v3 = 0, vector k4 = cVectorIntDictEmptyKey, int v4 = 0, vector k5 = cVectorIntDictEmptyKey, int v5 = 0, vector k6 = cVectorIntDictEmptyKey, int v6 = 0) {
    int dct = xsVectorIntDictCreate();
    if (dct < 0) {
        return (cVectorIntDictGenericError);
    }
    if (k1 == cVectorIntDictEmptyKey) {
        return (dct);
    }
    xsVectorIntDictPut(dct, k1, v1);
    if (k2 == cVectorIntDictEmptyKey) {
        return (dct);
    }
    xsVectorIntDictPut(dct, k2, v2);
    if (k3 == cVectorIntDictEmptyKey) {
        return (dct);
    }
    xsVectorIntDictPut(dct, k3, v3);
    if (k4 == cVectorIntDictEmptyKey) {
        return (dct);
    }
    xsVectorIntDictPut(dct, k4, v4);
    if (k5 == cVectorIntDictEmptyKey) {
        return (dct);
    }
    xsVectorIntDictPut(dct, k5, v5);
    if (k6 == cVectorIntDictEmptyKey) {
        return (dct);
    }
    xsVectorIntDictPut(dct, k6, v6);
    return (dct);
}

/*
    Returns the value associated with the given key. Sets last error on completion.
*/
int xsVectorIntDictGet(int dct = -1, vector key = vector(0.0, 0.0, 0.0), int dft = -1) {
    int capacity = xsArrayGetSize(dct);
    int slot = _xsVectorIntDictFindSlot(dct, key, capacity);
    if (slot >= 0) {
        _vectorIntDictLastOperationStatus = cVectorIntDictSuccess;
        return (_xsVectorIntDictGetStoredValue(dct, slot));
    }
    _vectorIntDictLastOperationStatus = cVectorIntDictNoKeyError;
    return (dft);
}

/*
    Removes the entry with the given key from the dict. Uses backward shift deletion to
    maintain linear probing invariant.
*/
int xsVectorIntDictRemove(int dct = -1, vector key = vector(0.0, 0.0, 0.0)) {
    int size = _xsVectorIntDictGetSize(dct);
    int capacity = xsArrayGetSize(dct);
    int numSlots = (capacity - 1) / 4;
    int slot = _xsVectorIntDictFindSlot(dct, key, capacity);
    if (slot < 0) {
        _vectorIntDictLastOperationStatus = cVectorIntDictNoKeyError;
        return (cVectorIntDictGenericError);
    }
    int foundVal = _xsVectorIntDictGetStoredValue(dct, slot);
    int g = slot;
    int q = g + 4;
    if (q >= capacity) {
        q = 1;
    }
    int shiftSteps = 0;
    vector qKey = _xsVectorIntDictGetStoredKey(dct, q);
    while ((qKey != cVectorIntDictEmptyKey) && (shiftSteps < numSlots)) {
        int qHome = _xsVectorIntDictHash(qKey, capacity);
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
        qKey = _xsVectorIntDictGetStoredKey(dct, q);
    }
    _xsVectorIntDictClearSlot(dct, g);
    _xsVectorIntDictSetSize(dct, size - 1);
    _vectorIntDictLastOperationStatus = cVectorIntDictSuccess;
    return (foundVal);
}

bool xsVectorIntDictContains(int dct = -1, vector key = vector(0.0, 0.0, 0.0)) {
    int capacity = xsArrayGetSize(dct);
    return (_xsVectorIntDictFindSlot(dct, key, capacity) >= 0);
}

int xsVectorIntDictSize(int dct = -1) {
    return (_xsVectorIntDictGetSize(dct));
}

/*
    Removes all entries from the dict and shrinks the backing array.
*/
int xsVectorIntDictClear(int dct = -1) {
    int capacity = xsArrayGetSize(dct);
    int i = 1;
    while (i < capacity) {
        _xsVectorIntDictClearSlot(dct, i);
        i = i + 4;
    }
    _xsVectorIntDictSetSize(dct, 0);
    if (capacity > cVectorIntDictInitialCapacity) {
        int r = xsArrayResizeFloat(dct, cVectorIntDictInitialCapacity);
        if (r != 1) {
            return (cVectorIntDictGenericError);
        }
    }
    return (cVectorIntDictSuccess);
}

/*
    Returns a deep copy of the dict.
*/
int xsVectorIntDictCopy(int dct = -1) {
    int capacity = xsArrayGetSize(dct);
    int newDct = xsArrayCreateFloat(capacity, xsVectorGetX(cVectorIntDictEmptyKey));
    if (newDct < 0) {
        return (cVectorIntDictResizeFailedError);
    }
    int tempIdx = 2;
    while (tempIdx < capacity) {
        xsArraySetFloat(newDct, tempIdx, xsVectorGetY(cVectorIntDictEmptyKey));
        xsArraySetFloat(newDct, tempIdx + 1, xsVectorGetZ(cVectorIntDictEmptyKey));
        tempIdx = tempIdx + 4;
    }
    int slotIdx = 1;
    while (slotIdx < capacity) {
        vector storedKey = _xsVectorIntDictGetStoredKey(dct, slotIdx);
        if (storedKey != cVectorIntDictEmptyKey) {
            xsArraySetFloat(newDct, slotIdx, xsArrayGetFloat(dct, slotIdx));
            xsArraySetFloat(newDct, slotIdx + 1, xsArrayGetFloat(dct, slotIdx + 1));
            xsArraySetFloat(newDct, slotIdx + 2, xsArrayGetFloat(dct, slotIdx + 2));
            xsArraySetFloat(newDct, slotIdx + 3, xsArrayGetFloat(dct, slotIdx + 3));
        }
        slotIdx = slotIdx + 4;
    }
    _xsVectorIntDictSetSize(newDct, _xsVectorIntDictGetSize(dct));
    return (newDct);
}

/*
    Returns a string representation of the dict in the format `{(x1, y1, z1) - v1, ...}`.
*/
string xsVectorIntDictToString(int dct = -1) {
    int capacity = xsArrayGetSize(dct);
    string s = "{";
    bool first = true;
    int i = 1;
    while (i < capacity) {
        vector key = _xsVectorIntDictGetStoredKey(dct, i);
        if (key != cVectorIntDictEmptyKey) {
            if (first) {
                first = false;
            } else {
                s = s + ", ";
            }
            s = s + (key + ": " + _xsVectorIntDictGetStoredValue(dct, i));
        }
        i = i + 4;
    }
    s = s + "}";
    return (s);
}

int xsVectorIntDictLastError() {
    return (_vectorIntDictLastOperationStatus);
}

vector _xsVectorIntDictFindNextOccupied(int dct = -1, int start = 1, int capacity = 0) {
    int slot = start;
    while (slot < capacity) {
        vector storedKey = _xsVectorIntDictGetStoredKey(dct, slot);
        if (storedKey != cVectorIntDictEmptyKey) {
            _vectorIntDictLastOperationStatus = cVectorIntDictSuccess;
            return (storedKey);
        }
        slot = slot + 4;
    }
    _vectorIntDictLastOperationStatus = cVectorIntDictNoKeyError;
    return (cVectorIntDictGenericErrorVector);
}

/*
    Returns the next key in the dict for stateless iteration. Sets last error on completion.
*/
vector xsVectorIntDictNextKey(int dct = -1, bool isFirst = true, vector prevKey = cVectorIntDictEmptyKey) {
    int capacity = xsArrayGetSize(dct);
    if (isFirst) {
        return (_xsVectorIntDictFindNextOccupied(dct, 1, capacity));
    }
    int slot = _xsVectorIntDictFindSlot(dct, prevKey, capacity);
    if (slot < 0) {
        _vectorIntDictLastOperationStatus = cVectorIntDictNoKeyError;
        return (cVectorIntDictGenericErrorVector);
    }
    int nextStart = slot + 4;
    return (_xsVectorIntDictFindNextOccupied(dct, nextStart, capacity));
}

bool xsVectorIntDictHasNext(int dct = -1, bool isFirst = true, vector prevKey = cVectorIntDictEmptyKey) {
    int capacity = xsArrayGetSize(dct);
    int start = 1;
    if (isFirst == false) {
        int slot = _xsVectorIntDictFindSlot(dct, prevKey, capacity);
        if (slot < 0) {
            return (false);
        }
        start = slot + 4;
    }
    while (start < capacity) {
        if (_xsVectorIntDictGetStoredKey(dct, start) != cVectorIntDictEmptyKey) {
            return (true);
        }
        start = start + 4;
    }
    return (false);
}

/*
    Inserts all key-value pairs from another dict into the source dict, overwriting existing keys.
*/
int xsVectorIntDictUpdate(int source = -1, int dct = -1) {
    int capacity = xsArrayGetSize(dct);
    int i = 1;
    while (i < capacity) {
        vector key = _xsVectorIntDictGetStoredKey(dct, i);
        if (key != cVectorIntDictEmptyKey) {
            xsVectorIntDictPut(source, key, _xsVectorIntDictGetStoredValue(dct, i));
            if ((_vectorIntDictLastOperationStatus != cVectorIntDictSuccess) && (_vectorIntDictLastOperationStatus != cVectorIntDictNoKeyError)) {
                return (_vectorIntDictLastOperationStatus);
            }
        }
        i = i + 4;
    }
    _vectorIntDictLastOperationStatus = cVectorIntDictSuccess;
    return (cVectorIntDictSuccess);
}

/*
    Inserts the key-value pair only if the key is not already present. Sets last error on completion.
*/
int xsVectorIntDictPutIfAbsent(int dct = -1, vector key = vector(0.0, 0.0, 0.0), int val = 0) {
    if (key == cVectorIntDictEmptyKey) {
        _vectorIntDictLastOperationStatus = cVectorIntDictGenericError;
        return (cVectorIntDictGenericError);
    }
    int size = _xsVectorIntDictGetSize(dct);
    int capacity = xsArrayGetSize(dct);
    int slot = _xsVectorIntDictFindSlot(dct, key, capacity);
    if (slot >= 0) {
        _vectorIntDictLastOperationStatus = cVectorIntDictSuccess;
        return (_xsVectorIntDictGetStoredValue(dct, slot));
    }
    int r = _xsVectorIntDictRehashIfNeeded(dct, size, capacity, size + 1);
    if (r != cVectorIntDictSuccess) {
        return (cVectorIntDictGenericError);
    }
    capacity = xsArrayGetSize(dct);
    int result = _xsVectorIntDictUpsert(dct, key, val, capacity);
    if (_vectorIntDictLastOperationStatus == cVectorIntDictNoKeyError) {
        _xsVectorIntDictSetSize(dct, size + 1);
        return (cVectorIntDictGenericError);
    }
    if (_vectorIntDictLastOperationStatus != cVectorIntDictSuccess) {
        return (cVectorIntDictGenericError);
    }
    return (result);
}

/*
    Returns a new vector array containing all keys in the dict. Order is arbitrary.
*/
int xsVectorIntDictKeys(int dct = -1) {
    int size = _xsVectorIntDictGetSize(dct);
    int arr = xsArrayCreateVector(size, vector(0.0, 0.0, 0.0));
    if (arr < 0) {
        return (cVectorIntDictResizeFailedError);
    }
    int capacity = xsArrayGetSize(dct);
    int idx = 0;
    int i = 1;
    while (i < capacity) {
        vector storedKey = _xsVectorIntDictGetStoredKey(dct, i);
        if (storedKey != cVectorIntDictEmptyKey) {
            xsArraySetVector(arr, idx, storedKey);
            idx++;
        }
        i = i + 4;
    }
    return (arr);
}

/*
    Returns a new int array containing all values in the dict. Order matches `xsVectorIntDictKeys`.
*/
int xsVectorIntDictValues(int dct = -1) {
    int size = _xsVectorIntDictGetSize(dct);
    int arr = xsArrayCreateInt(size, 0);
    if (arr < 0) {
        return (cVectorIntDictResizeFailedError);
    }
    int capacity = xsArrayGetSize(dct);
    int idx = 0;
    int i = 1;
    while (i < capacity) {
        vector storedKey = _xsVectorIntDictGetStoredKey(dct, i);
        if (storedKey != cVectorIntDictEmptyKey) {
            xsArraySetInt(arr, idx, _xsVectorIntDictGetStoredValue(dct, i));
            idx++;
        }
        i = i + 4;
    }
    return (arr);
}

/*
    Returns true if both dicts contain the same key-value pairs.
*/
bool xsVectorIntDictEquals(int a = -1, int b = -1) {
    int sizeA = _xsVectorIntDictGetSize(a);
    int sizeB = _xsVectorIntDictGetSize(b);
    if (sizeA != sizeB) {
        return (false);
    }
    int capacity = xsArrayGetSize(a);
    int i = 1;
    while (i < capacity) {
        vector key = _xsVectorIntDictGetStoredKey(a, i);
        if (key != cVectorIntDictEmptyKey) {
            int val = _xsVectorIntDictGetStoredValue(a, i);
            if (xsVectorIntDictGet(b, key) != val) {
                return (false);
            }
            if (xsVectorIntDictLastError() != cVectorIntDictSuccess) {
                return (false);
            }
        }
        i = i + 4;
    }
    return (true);
}

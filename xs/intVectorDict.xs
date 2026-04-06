extern const int cIntVectorDictSuccess = 0;
extern const int cIntVectorDictGenericError = -1;
extern const int cIntVectorDictNoKeyError = -2;
extern const int cIntVectorDictResizeFailedError = -3;
extern const int cIntVectorDictMaxCapacityError = -4;
extern const vector cIntVectorDictGenericErrorVector = vector(-1.0, -1.0, -1.0);
extern const int cIntVectorDictMaxCapacity = 999999997;
extern const float cIntVectorDictMaxLoadFactor = 0.75;
extern const int cIntVectorDictEmptyKey = -999999999;
extern const int cIntVectorDictInitialCapacity = 65;
extern const int cIntVectorDictHashConstant = 16777619;
int _intVectorDictLastOperationStatus = cIntVectorDictSuccess;
int _intVectorDictTempArray = -1;

void _xsIntVectorDictSetSize(int dct = -1, int size = 0) {
    xsArraySetFloat(dct, 0, bitCastToFloat(size));
}

int _xsIntVectorDictGetSize(int dct = -1) {
    return (bitCastToInt(xsArrayGetFloat(dct, 0)));
}

int _xsIntVectorDictGetStoredKey(int dct = -1, int slot = 1) {
    return (bitCastToInt(xsArrayGetFloat(dct, slot)));
}

void _xsIntVectorDictSetStoredKey(int dct = -1, int slot = 1, int key = -1) {
    xsArraySetFloat(dct, slot, bitCastToFloat(key));
}

void _xsIntVectorDictClearSlot(int dct = -1, int slot = 1) {
    _xsIntVectorDictSetStoredKey(dct, slot, cIntVectorDictEmptyKey);
}

void _xsIntVectorDictSetStoredValue(int dct = -1, int slot = 1, vector value = vector(0.0, 0.0, 0.0)) {
    xsArraySetFloat(dct, slot + 1, xsVectorGetX(value));
    xsArraySetFloat(dct, slot + 2, xsVectorGetY(value));
    xsArraySetFloat(dct, slot + 3, xsVectorGetZ(value));
}

vector _xsIntVectorDictGetStoredValue(int dct = -1, int slot = 1) {
    return (xsVectorSet(xsArrayGetFloat(dct, slot + 1), xsArrayGetFloat(dct, slot + 2), xsArrayGetFloat(dct, slot + 3)));
}

void _xsIntVectorDictSetSlot(int dct = -1, int slot = 1, int key = -1, vector value = vector(0.0, 0.0, 0.0)) {
    _xsIntVectorDictSetStoredKey(dct, slot, key);
    _xsIntVectorDictSetStoredValue(dct, slot, value);
}

/*
    Creates an empty int-to-vector dictionary.
    Keys equal to `cIntVectorDictEmptyKey` are reserved as the internal empty-slot sentinel
    and cannot be stored. `put` and `putIfAbsent` silently reject them.
    @return created dict id, or `cIntVectorDictGenericError` on error
*/
int xsIntVectorDictCreate() {
    int dct = xsArrayCreateFloat(cIntVectorDictInitialCapacity, bitCastToFloat(cIntVectorDictEmptyKey));
    if (dct < 0) {
        return (cIntVectorDictGenericError);
    }
    _xsIntVectorDictSetSize(dct, 0);
    return (dct);
}

int _xsIntVectorDictHash(int key = -1, int capacity = 0) {
    int h = key * cIntVectorDictHashConstant;
    int numSlots = (capacity - 1) / 4;
    h = h % numSlots;
    if (h < 0) {
        h = h + numSlots;
    }
    return ((h * 4) + 1);
}

int _xsIntVectorDictFindSlot(int dct = -1, int key = -1, int capacity = 0) {
    int numSlots = (capacity - 1) / 4;
    int home = _xsIntVectorDictHash(key, capacity);
    int slot = home;
    int steps = 0;
    while (steps < numSlots) {
        int storedKey = _xsIntVectorDictGetStoredKey(dct, slot);
        if (storedKey == cIntVectorDictEmptyKey) {
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

vector _xsIntVectorDictUpsert(int dct = -1, int key = -1, vector val = vector(0.0, 0.0, 0.0), int capacity = 0) {
    int numSlots = (capacity - 1) / 4;
    int home = _xsIntVectorDictHash(key, capacity);
    int slot = home;
    int steps = 0;
    while (steps < numSlots) {
        int storedKey = _xsIntVectorDictGetStoredKey(dct, slot);
        if (storedKey == cIntVectorDictEmptyKey) {
            _xsIntVectorDictSetSlot(dct, slot, key, val);
            _intVectorDictLastOperationStatus = cIntVectorDictNoKeyError;
            return (cIntVectorDictGenericErrorVector);
        }
        if (storedKey == key) {
            vector oldVal = _xsIntVectorDictGetStoredValue(dct, slot);
            _xsIntVectorDictSetStoredValue(dct, slot, val);
            _intVectorDictLastOperationStatus = cIntVectorDictSuccess;
            return (oldVal);
        }
        slot = slot + 4;
        if (slot >= capacity) {
            slot = 1;
        }
        steps++;
    }
    _intVectorDictLastOperationStatus = cIntVectorDictMaxCapacityError;
    return (cIntVectorDictGenericErrorVector);
}

int _xsIntVectorDictMoveToTempArray(int dct = -1, int size = 0, int capacity = 0) {
    int tempDataSize = size * 4;
    if (_intVectorDictTempArray < 0) {
        _intVectorDictTempArray = xsArrayCreateFloat(tempDataSize, bitCastToFloat(cIntVectorDictEmptyKey));
        if (_intVectorDictTempArray < 0) {
            return (cIntVectorDictResizeFailedError);
        }
    } else {
        int tempArrCapacity = xsArrayGetSize(_intVectorDictTempArray);
        if (tempArrCapacity < tempDataSize) {
            if (tempDataSize > cIntVectorDictMaxCapacity) {
                return (cIntVectorDictMaxCapacityError);
            }
            int r = xsArrayResizeFloat(_intVectorDictTempArray, tempDataSize);
            if (r != 1) {
                return (cIntVectorDictResizeFailedError);
            }
        }
    }
    int t = 0;
    int i = 1;
    while (i < capacity) {
        int storedKey = _xsIntVectorDictGetStoredKey(dct, i);
        if (storedKey != cIntVectorDictEmptyKey) {
            xsArraySetFloat(_intVectorDictTempArray, t, xsArrayGetFloat(dct, i));
            xsArraySetFloat(_intVectorDictTempArray, t + 1, xsArrayGetFloat(dct, i + 1));
            xsArraySetFloat(_intVectorDictTempArray, t + 2, xsArrayGetFloat(dct, i + 2));
            xsArraySetFloat(_intVectorDictTempArray, t + 3, xsArrayGetFloat(dct, i + 3));
            t = t + 4;
        }
        i = i + 4;
    }
    return (tempDataSize);
}

void _xsIntVectorDictClearSlots(int dct = -1, int capacity = -1) {
    int j = 1;
    while (j < capacity) {
        _xsIntVectorDictClearSlot(dct, j);
        j = j + 4;
    }
}

int _xsIntVectorDictRehashIfNeeded(int dct = -1, int size = 0, int capacity = 0, int requiredSize = -1) {
    if (requiredSize < 0) {
        requiredSize = size;
    }
    float loadFactor = (0.0 + requiredSize) / ((capacity - 1) / 4);
    if (loadFactor > cIntVectorDictMaxLoadFactor) {
        int storeStatus = _intVectorDictLastOperationStatus;
        int newCapacity = ((capacity - 1) * 2) + 1;
        if (newCapacity > cIntVectorDictMaxCapacity) {
            _intVectorDictLastOperationStatus = cIntVectorDictMaxCapacityError;
            return (cIntVectorDictGenericError);
        }
        int tempDataSize = _xsIntVectorDictMoveToTempArray(dct, size, capacity);
        if (tempDataSize < 0) {
            _intVectorDictLastOperationStatus = tempDataSize;
            return (cIntVectorDictGenericError);
        }
        int r = xsArrayResizeFloat(dct, newCapacity);
        if (r != 1) {
            _intVectorDictLastOperationStatus = cIntVectorDictResizeFailedError;
            return (cIntVectorDictGenericError);
        }
        _xsIntVectorDictClearSlots(dct, newCapacity);
        int t = 0;
        while (t < tempDataSize) {
            _xsIntVectorDictUpsert(dct, bitCastToInt(xsArrayGetFloat(_intVectorDictTempArray, t)), xsVectorSet(xsArrayGetFloat(_intVectorDictTempArray, t + 1), xsArrayGetFloat(_intVectorDictTempArray, t + 2), xsArrayGetFloat(_intVectorDictTempArray, t + 3)), newCapacity);
            if ((_intVectorDictLastOperationStatus < 0) && (_intVectorDictLastOperationStatus != cIntVectorDictNoKeyError)) {
                return (cIntVectorDictGenericError);
            }
            t = t + 4;
        }
        _intVectorDictLastOperationStatus = storeStatus;
    }
    return (cIntVectorDictSuccess);
}

/*
    Inserts or updates a key-value pair. Triggers a rehash when load factor exceeds the threshold.
    If `key` equals `cIntVectorDictEmptyKey`, the call is a no-op and returns
    `cIntVectorDictGenericErrorVector` with last error set to `cIntVectorDictGenericError`.
*/
vector xsIntVectorDictPut(int dct = -1, int key = -1, vector val = vector(0.0, 0.0, 0.0)) {
    if (key == cIntVectorDictEmptyKey) {
        _intVectorDictLastOperationStatus = cIntVectorDictGenericError;
        return (cIntVectorDictGenericErrorVector);
    }
    int size = _xsIntVectorDictGetSize(dct);
    int capacity = xsArrayGetSize(dct);
    int slot = _xsIntVectorDictFindSlot(dct, key, capacity);
    if (slot >= 0) {
        vector oldVal = _xsIntVectorDictGetStoredValue(dct, slot);
        _xsIntVectorDictSetStoredValue(dct, slot, val);
        _intVectorDictLastOperationStatus = cIntVectorDictSuccess;
        return (oldVal);
    }
    int r = _xsIntVectorDictRehashIfNeeded(dct, size, capacity, size + 1);
    if (r != cIntVectorDictSuccess) {
        return (cIntVectorDictGenericErrorVector);
    }
    capacity = xsArrayGetSize(dct);
    vector previousValue = _xsIntVectorDictUpsert(dct, key, val, capacity);
    if (_intVectorDictLastOperationStatus == cIntVectorDictNoKeyError) {
        _xsIntVectorDictSetSize(dct, size + 1);
        return (cIntVectorDictGenericErrorVector);
    }
    if (_intVectorDictLastOperationStatus != cIntVectorDictSuccess) {
        return (cIntVectorDictGenericErrorVector);
    }
    return (previousValue);
}

/*
    Creates a dict with provided key-value pairs. The first key that equals
    `cIntVectorDictEmptyKey` will stop further insertion.
*/
int xsIntVectorDict(int k1 = cIntVectorDictEmptyKey, vector v1 = vector(0.0, 0.0, 0.0), int k2 = cIntVectorDictEmptyKey, vector v2 = vector(0.0, 0.0, 0.0), int k3 = cIntVectorDictEmptyKey, vector v3 = vector(0.0, 0.0, 0.0), int k4 = cIntVectorDictEmptyKey, vector v4 = vector(0.0, 0.0, 0.0), int k5 = cIntVectorDictEmptyKey, vector v5 = vector(0.0, 0.0, 0.0), int k6 = cIntVectorDictEmptyKey, vector v6 = vector(0.0, 0.0, 0.0)) {
    int dct = xsIntVectorDictCreate();
    if (dct < 0) {
        return (cIntVectorDictGenericError);
    }
    if (k1 == cIntVectorDictEmptyKey) {
        return (dct);
    }
    xsIntVectorDictPut(dct, k1, v1);
    if (k2 == cIntVectorDictEmptyKey) {
        return (dct);
    }
    xsIntVectorDictPut(dct, k2, v2);
    if (k3 == cIntVectorDictEmptyKey) {
        return (dct);
    }
    xsIntVectorDictPut(dct, k3, v3);
    if (k4 == cIntVectorDictEmptyKey) {
        return (dct);
    }
    xsIntVectorDictPut(dct, k4, v4);
    if (k5 == cIntVectorDictEmptyKey) {
        return (dct);
    }
    xsIntVectorDictPut(dct, k5, v5);
    if (k6 == cIntVectorDictEmptyKey) {
        return (dct);
    }
    xsIntVectorDictPut(dct, k6, v6);
    return (dct);
}

/*
    Returns the value associated with the given key. Sets last error on completion.
*/
vector xsIntVectorDictGet(int dct = -1, int key = -1, vector dft = cIntVectorDictGenericErrorVector) {
    int capacity = xsArrayGetSize(dct);
    int slot = _xsIntVectorDictFindSlot(dct, key, capacity);
    if (slot >= 0) {
        _intVectorDictLastOperationStatus = cIntVectorDictSuccess;
        return (_xsIntVectorDictGetStoredValue(dct, slot));
    }
    _intVectorDictLastOperationStatus = cIntVectorDictNoKeyError;
    return (dft);
}

/*
    Removes the entry with the given key from the dict. Uses backward shift deletion to
    maintain linear probing invariant.
*/
vector xsIntVectorDictRemove(int dct = -1, int key = -1) {
    int size = _xsIntVectorDictGetSize(dct);
    int capacity = xsArrayGetSize(dct);
    int numSlots = (capacity - 1) / 4;
    int slot = _xsIntVectorDictFindSlot(dct, key, capacity);
    if (slot < 0) {
        _intVectorDictLastOperationStatus = cIntVectorDictNoKeyError;
        return (cIntVectorDictGenericErrorVector);
    }
    vector foundVal = _xsIntVectorDictGetStoredValue(dct, slot);
    int g = slot;
    int q = g + 4;
    if (q >= capacity) {
        q = 1;
    }
    int shiftSteps = 0;
    int qKey = _xsIntVectorDictGetStoredKey(dct, q);
    while ((qKey != cIntVectorDictEmptyKey) && (shiftSteps < numSlots)) {
        int qHome = _xsIntVectorDictHash(qKey, capacity);
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
        qKey = _xsIntVectorDictGetStoredKey(dct, q);
    }
    _xsIntVectorDictClearSlot(dct, g);
    _xsIntVectorDictSetSize(dct, size - 1);
    _intVectorDictLastOperationStatus = cIntVectorDictSuccess;
    return (foundVal);
}

bool xsIntVectorDictContains(int dct = -1, int key = -1) {
    int capacity = xsArrayGetSize(dct);
    return (_xsIntVectorDictFindSlot(dct, key, capacity) >= 0);
}

int xsIntVectorDictSize(int dct = -1) {
    return (_xsIntVectorDictGetSize(dct));
}

/*
    Removes all entries from the dict and shrinks the backing array.
*/
int xsIntVectorDictClear(int dct = -1) {
    int capacity = xsArrayGetSize(dct);
    int i = 1;
    while (i < capacity) {
        _xsIntVectorDictClearSlot(dct, i);
        i = i + 4;
    }
    _xsIntVectorDictSetSize(dct, 0);
    if (capacity > cIntVectorDictInitialCapacity) {
        int r = xsArrayResizeFloat(dct, cIntVectorDictInitialCapacity);
        if (r != 1) {
            return (cIntVectorDictGenericError);
        }
    }
    return (cIntVectorDictSuccess);
}

/*
    Returns a deep copy of the dict.
*/
int xsIntVectorDictCopy(int dct = -1) {
    int capacity = xsArrayGetSize(dct);
    int newDct = xsArrayCreateFloat(capacity, bitCastToFloat(cIntVectorDictEmptyKey));
    if (newDct < 0) {
        return (cIntVectorDictResizeFailedError);
    }
    int i = 1;
    while (i < capacity) {
        int storedKey = _xsIntVectorDictGetStoredKey(dct, i);
        if (storedKey != cIntVectorDictEmptyKey) {
            xsArraySetFloat(newDct, i, xsArrayGetFloat(dct, i));
            xsArraySetFloat(newDct, i + 1, xsArrayGetFloat(dct, i + 1));
            xsArraySetFloat(newDct, i + 2, xsArrayGetFloat(dct, i + 2));
            xsArraySetFloat(newDct, i + 3, xsArrayGetFloat(dct, i + 3));
        }
        i = i + 4;
    }
    _xsIntVectorDictSetSize(newDct, _xsIntVectorDictGetSize(dct));
    return (newDct);
}

/*
    Returns a string representation of the dict in the format `{k1 - (x1, y1, z1), ...}`.
*/
string xsIntVectorDictToString(int dct = -1) {
    int capacity = xsArrayGetSize(dct);
    string s = "{";
    bool first = true;
    int i = 1;
    while (i < capacity) {
        int key = _xsIntVectorDictGetStoredKey(dct, i);
        if (key != cIntVectorDictEmptyKey) {
            if (first) {
                first = false;
            } else {
                s = s + ", ";
            }
            s = s + (key + ": " + _xsIntVectorDictGetStoredValue(dct, i));
        }
        i = i + 4;
    }
    s = s + "}";
    return (s);
}

int xsIntVectorDictLastError() {
    return (_intVectorDictLastOperationStatus);
}

int _xsIntVectorDictFindNextOccupied(int dct = -1, int start = 1, int capacity = 0) {
    int slot = start;
    while (slot < capacity) {
        int storedKey = _xsIntVectorDictGetStoredKey(dct, slot);
        if (storedKey != cIntVectorDictEmptyKey) {
            _intVectorDictLastOperationStatus = cIntVectorDictSuccess;
            return (storedKey);
        }
        slot = slot + 4;
    }
    _intVectorDictLastOperationStatus = cIntVectorDictNoKeyError;
    return (cIntVectorDictGenericError);
}

/*
    Returns the next key in the dict for stateless iteration. Sets last error on completion.
*/
int xsIntVectorDictNextKey(int dct = -1, bool isFirst = true, int prevKey = -1) {
    int capacity = xsArrayGetSize(dct);
    if (isFirst) {
        return (_xsIntVectorDictFindNextOccupied(dct, 1, capacity));
    }
    int slot = _xsIntVectorDictFindSlot(dct, prevKey, capacity);
    if (slot < 0) {
        _intVectorDictLastOperationStatus = cIntVectorDictNoKeyError;
        return (cIntVectorDictGenericError);
    }
    int nextStart = slot + 4;
    return (_xsIntVectorDictFindNextOccupied(dct, nextStart, capacity));
}

bool xsIntVectorDictHasNext(int dct = -1, bool isFirst = true, int prevKey = -1) {
    int capacity = xsArrayGetSize(dct);
    int start = 1;
    if (isFirst == false) {
        int slot = _xsIntVectorDictFindSlot(dct, prevKey, capacity);
        if (slot < 0) {
            return (false);
        }
        start = slot + 4;
    }
    while (start < capacity) {
        if (_xsIntVectorDictGetStoredKey(dct, start) != cIntVectorDictEmptyKey) {
            return (true);
        }
        start = start + 4;
    }
    return (false);
}

/*
    Inserts all key-value pairs from another dict into the source dict, overwriting existing keys.
*/
int xsIntVectorDictUpdate(int source = -1, int dct = -1) {
    int capacity = xsArrayGetSize(dct);
    int i = 1;
    while (i < capacity) {
        int key = _xsIntVectorDictGetStoredKey(dct, i);
        if (key != cIntVectorDictEmptyKey) {
            xsIntVectorDictPut(source, key, _xsIntVectorDictGetStoredValue(dct, i));
            if ((_intVectorDictLastOperationStatus != cIntVectorDictSuccess) && (_intVectorDictLastOperationStatus != cIntVectorDictNoKeyError)) {
                return (_intVectorDictLastOperationStatus);
            }
        }
        i = i + 4;
    }
    _intVectorDictLastOperationStatus = cIntVectorDictSuccess;
    return (cIntVectorDictSuccess);
}

/*
    Inserts the key-value pair only if the key is not already present. Sets last error on completion.
*/
vector xsIntVectorDictPutIfAbsent(int dct = -1, int key = -1, vector val = vector(0.0, 0.0, 0.0)) {
    if (key == cIntVectorDictEmptyKey) {
        _intVectorDictLastOperationStatus = cIntVectorDictGenericError;
        return (cIntVectorDictGenericErrorVector);
    }
    int size = _xsIntVectorDictGetSize(dct);
    int capacity = xsArrayGetSize(dct);
    int slot = _xsIntVectorDictFindSlot(dct, key, capacity);
    if (slot >= 0) {
        _intVectorDictLastOperationStatus = cIntVectorDictSuccess;
        return (_xsIntVectorDictGetStoredValue(dct, slot));
    }
    int r = _xsIntVectorDictRehashIfNeeded(dct, size, capacity, size + 1);
    if (r != cIntVectorDictSuccess) {
        return (cIntVectorDictGenericErrorVector);
    }
    capacity = xsArrayGetSize(dct);
    vector result = _xsIntVectorDictUpsert(dct, key, val, capacity);
    if (_intVectorDictLastOperationStatus == cIntVectorDictNoKeyError) {
        _xsIntVectorDictSetSize(dct, size + 1);
        return (cIntVectorDictGenericErrorVector);
    }
    if (_intVectorDictLastOperationStatus != cIntVectorDictSuccess) {
        return (cIntVectorDictGenericErrorVector);
    }
    return (result);
}

/*
    Returns a new int array containing all keys in the dict. Order is arbitrary.
*/
int xsIntVectorDictKeys(int dct = -1) {
    int size = _xsIntVectorDictGetSize(dct);
    int arr = xsArrayCreateInt(size, 0);
    if (arr < 0) {
        return (cIntVectorDictResizeFailedError);
    }
    int capacity = xsArrayGetSize(dct);
    int idx = 0;
    int i = 1;
    while (i < capacity) {
        int storedKey = _xsIntVectorDictGetStoredKey(dct, i);
        if (storedKey != cIntVectorDictEmptyKey) {
            xsArraySetInt(arr, idx, storedKey);
            idx++;
        }
        i = i + 4;
    }
    return (arr);
}

/*
    Returns a new vector array containing all values in the dict. Order matches `xsIntVectorDictKeys`.
*/
int xsIntVectorDictValues(int dct = -1) {
    int size = _xsIntVectorDictGetSize(dct);
    int arr = xsArrayCreateVector(size, vector(0.0, 0.0, 0.0));
    if (arr < 0) {
        return (cIntVectorDictResizeFailedError);
    }
    int capacity = xsArrayGetSize(dct);
    int idx = 0;
    int i = 1;
    while (i < capacity) {
        int storedKey = _xsIntVectorDictGetStoredKey(dct, i);
        if (storedKey != cIntVectorDictEmptyKey) {
            xsArraySetVector(arr, idx, _xsIntVectorDictGetStoredValue(dct, i));
            idx++;
        }
        i = i + 4;
    }
    return (arr);
}

/*
    Returns true if both dicts contain the same key-value pairs.
*/
bool xsIntVectorDictEquals(int a = -1, int b = -1) {
    int sizeA = _xsIntVectorDictGetSize(a);
    int sizeB = _xsIntVectorDictGetSize(b);
    if (sizeA != sizeB) {
        return (false);
    }
    int capacity = xsArrayGetSize(a);
    int i = 1;
    while (i < capacity) {
        int key = _xsIntVectorDictGetStoredKey(a, i);
        if (key != cIntVectorDictEmptyKey) {
            vector val = _xsIntVectorDictGetStoredValue(a, i);
            if (xsIntVectorDictGet(b, key) != val) {
                return (false);
            }
            if (xsIntVectorDictLastError() != cIntVectorDictSuccess) {
                return (false);
            }
        }
        i = i + 4;
    }
    return (true);
}

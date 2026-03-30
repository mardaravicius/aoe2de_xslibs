extern const int cIntStringDictSuccess = 0;
extern const int cIntStringDictGenericError = -1;
extern const int cIntStringDictNoKeyError = -2;
extern const int cIntStringDictResizeFailedError = -3;
extern const int cIntStringDictMaxCapacityError = -4;
extern const int cIntStringDictMaxCapacity = 999999999;
extern const float cIntStringDictMaxLoadFactor = 0.75;
extern const int cIntStringDictEmptyKey = -999999999;
extern const int cIntStringDictInitialCapacity = 18;
extern const int cIntStringDictHashConstant = 16777619;
int _intStringDictLastOperationStatus = cIntStringDictSuccess;
int _intStringDictTempKeys = -1;
int _intStringDictTempValues = -1;

int _xsIntStringDictValuesCapacityFromIntCapacity(int capacity = 0) {
    return (capacity - 2);
}

int _xsIntStringDictGetValuesArray(int dct = -1) {
    return (xsArrayGetInt(dct, 1));
}

int _xsIntStringDictValueSlot(int slot = 2) {
    return (slot - 2);
}

string _xsIntStringDictGetStoredValue(int dct = -1, int slot = 2) {
    return (xsArrayGetString(_xsIntStringDictGetValuesArray(dct), _xsIntStringDictValueSlot(slot)));
}

void _xsIntStringDictSetStoredValue(int dct = -1, int slot = 2, string value = "") {
    xsArraySetString(_xsIntStringDictGetValuesArray(dct), _xsIntStringDictValueSlot(slot), value);
}

void _xsIntStringDictClearSlot(int dct = -1, int slot = 2) {
    xsArraySetInt(dct, slot, cIntStringDictEmptyKey);
}

/*
    Creates an empty int-to-string dictionary.
    Keys equal to `cIntStringDictEmptyKey` (-999999999) are reserved as the internal
    empty-slot sentinel and cannot be stored. `put` and `putIfAbsent` silently reject them.
    @return created dict id, or `cIntStringDictGenericError` on error
*/
int xsIntStringDictCreate() {
    int dct = xsArrayCreateInt(cIntStringDictInitialCapacity, cIntStringDictEmptyKey);
    if (dct < 0) {
        return (cIntStringDictGenericError);
    }
    int valuesArr = xsArrayCreateString(cIntStringDictInitialCapacity - 2);
    if (valuesArr < 0) {
        xsArrayResizeInt(dct, 0);
        return (cIntStringDictGenericError);
    }
    xsArraySetInt(dct, 0, 0);
    xsArraySetInt(dct, 1, valuesArr);
    return (dct);
}

int _xsIntStringDictHash(int key = -1, int capacity = 0) {
    int hash = key * cIntStringDictHashConstant;
    int numSlots = _xsIntStringDictValuesCapacityFromIntCapacity(capacity);
    hash = hash % numSlots;
    if (hash < 0) {
        hash = hash + numSlots;
    }
    return (hash + 2);
}

/*
    Returns int-array index of slot containing key, or -1 if not found.
*/
int _xsIntStringDictFindSlot(int dct = -1, int key = -1, int capacity = 0) {
    int numSlots = _xsIntStringDictValuesCapacityFromIntCapacity(capacity);
    int home = _xsIntStringDictHash(key, capacity);
    int slot = home;
    int steps = 0;
    while (steps < numSlots) {
        int storedKey = xsArrayGetInt(dct, slot);
        if (storedKey == cIntStringDictEmptyKey) {
            return (-1);
        }
        if (storedKey == key) {
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

string _xsIntStringDictUpsert(int dct = -1, int key = -1, string val = "", int capacity = 0) {
    int numSlots = _xsIntStringDictValuesCapacityFromIntCapacity(capacity);
    int home = _xsIntStringDictHash(key, capacity);
    int slot = home;
    int steps = 0;
    while (steps < numSlots) {
        int storedKey = xsArrayGetInt(dct, slot);
        if (storedKey == cIntStringDictEmptyKey) {
            xsArraySetInt(dct, slot, key);
            _xsIntStringDictSetStoredValue(dct, slot, val);
            _intStringDictLastOperationStatus = cIntStringDictNoKeyError;
            return ("-1");
        }
        if (storedKey == key) {
            string oldVal = _xsIntStringDictGetStoredValue(dct, slot);
            _xsIntStringDictSetStoredValue(dct, slot, val);
            _intStringDictLastOperationStatus = cIntStringDictSuccess;
            return (oldVal);
        }
        slot++;
        if (slot >= capacity) {
            slot = 2;
        }
        steps++;
    }
    _intStringDictLastOperationStatus = cIntStringDictMaxCapacityError;
    return ("-1");
}

int _xsIntStringDictMoveToTempArrays(int dct = -1, int size = 0, int capacity = 0) {
    int tempDataSize = size;
    int maxValuesCapacity = cIntStringDictMaxCapacity - 2;
    if (_intStringDictTempKeys < 0) {
        _intStringDictTempKeys = xsArrayCreateInt(tempDataSize, cIntStringDictEmptyKey);
        if (_intStringDictTempKeys < 0) {
            return (cIntStringDictResizeFailedError);
        }
    } else {
        int tempKeysCapacity = xsArrayGetSize(_intStringDictTempKeys);
        if (tempKeysCapacity < tempDataSize) {
            if (tempDataSize > maxValuesCapacity) {
                return (cIntStringDictMaxCapacityError);
            }
            int rKeys = xsArrayResizeInt(_intStringDictTempKeys, tempDataSize);
            if (rKeys != 1) {
                return (cIntStringDictResizeFailedError);
            }
        }
    }
    if (_intStringDictTempValues < 0) {
        _intStringDictTempValues = xsArrayCreateString(tempDataSize);
        if (_intStringDictTempValues < 0) {
            return (cIntStringDictResizeFailedError);
        }
    } else {
        int tempValuesCapacity = xsArrayGetSize(_intStringDictTempValues);
        if (tempValuesCapacity < tempDataSize) {
            if (tempDataSize > maxValuesCapacity) {
                return (cIntStringDictMaxCapacityError);
            }
            int rValues = xsArrayResizeString(_intStringDictTempValues, tempDataSize);
            if (rValues != 1) {
                return (cIntStringDictResizeFailedError);
            }
        }
    }
    int t = 0;
    for (i = 2; < capacity) {
        int storedKey = xsArrayGetInt(dct, i);
        if (storedKey != cIntStringDictEmptyKey) {
            xsArraySetInt(_intStringDictTempKeys, t, storedKey);
            xsArraySetString(_intStringDictTempValues, t, _xsIntStringDictGetStoredValue(dct, i));
            t++;
        }
    }
    return (tempDataSize);
}

void _xsIntStringDictClearSlots(int dct = -1, int capacity = -1) {
    for (j = 2; < capacity) {
        _xsIntStringDictClearSlot(dct, j);
    }
}

int _xsIntStringDictRehashIfNeeded(int dct = -1, int size = 0, int capacity = 0, int requiredSize = -1) {
    if (requiredSize < 0) {
        requiredSize = size;
    }
    float loadFactor = (0.0 + requiredSize) / _xsIntStringDictValuesCapacityFromIntCapacity(capacity);
    if (loadFactor > cIntStringDictMaxLoadFactor) {
        int storeStatus = _intStringDictLastOperationStatus;
        int newValuesCapacity = _xsIntStringDictValuesCapacityFromIntCapacity(capacity) * 2;
        int newCapacity = newValuesCapacity + 2;
        if (newCapacity > cIntStringDictMaxCapacity) {
            _intStringDictLastOperationStatus = cIntStringDictMaxCapacityError;
            return (cIntStringDictGenericError);
        }
        int tempDataSize = _xsIntStringDictMoveToTempArrays(dct, size, capacity);
        if (tempDataSize < 0) {
            _intStringDictLastOperationStatus = tempDataSize;
            return (cIntStringDictGenericError);
        }
        int valuesArr = _xsIntStringDictGetValuesArray(dct);
        int rValues = xsArrayResizeString(valuesArr, newValuesCapacity);
        if (rValues != 1) {
            _intStringDictLastOperationStatus = cIntStringDictResizeFailedError;
            return (cIntStringDictGenericError);
        }
        int r = xsArrayResizeInt(dct, newCapacity);
        if (r != 1) {
            _intStringDictLastOperationStatus = cIntStringDictResizeFailedError;
            return (cIntStringDictGenericError);
        }
        _xsIntStringDictClearSlots(dct, newCapacity);
        for (t = 0; < tempDataSize) {
            _xsIntStringDictUpsert(dct, xsArrayGetInt(_intStringDictTempKeys, t), xsArrayGetString(_intStringDictTempValues, t), newCapacity);
            if ((_intStringDictLastOperationStatus < 0) && (_intStringDictLastOperationStatus != cIntStringDictNoKeyError)) {
                return (cIntStringDictGenericError);
            }
        }
        _intStringDictLastOperationStatus = storeStatus;
    }
    return (cIntStringDictSuccess);
}

/*
    Inserts or updates a key-value pair. Triggers a rehash when load factor exceeds the threshold.
    Sets last error on completion.
    If `key` equals `cIntStringDictEmptyKey`, the call is a no-op and returns
    `"-1"` with last error set to `cIntStringDictGenericError`.
    @return previous value if the key already existed, or `"-1"`
        if newly inserted or on error. Callers must check `xs_int_string_dict_last_error()`.
*/
string xsIntStringDictPut(int dct = -1, int key = -1, string val = "") {
    if (key == cIntStringDictEmptyKey) {
        _intStringDictLastOperationStatus = cIntStringDictGenericError;
        return ("-1");
    }
    int size = xsArrayGetInt(dct, 0);
    int capacity = xsArrayGetSize(dct);
    int slot = _xsIntStringDictFindSlot(dct, key, capacity);
    if (slot >= 0) {
        string oldVal = _xsIntStringDictGetStoredValue(dct, slot);
        _xsIntStringDictSetStoredValue(dct, slot, val);
        _intStringDictLastOperationStatus = cIntStringDictSuccess;
        return (oldVal);
    }
    int r = _xsIntStringDictRehashIfNeeded(dct, size, capacity, size + 1);
    if (r != cIntStringDictSuccess) {
        return ("-1");
    }
    capacity = xsArrayGetSize(dct);
    string previousValue = _xsIntStringDictUpsert(dct, key, val, capacity);
    if (_intStringDictLastOperationStatus == cIntStringDictNoKeyError) {
        xsArraySetInt(dct, 0, size + 1);
        return ("-1");
    }
    if (_intStringDictLastOperationStatus != cIntStringDictSuccess) {
        return ("-1");
    }
    return (previousValue);
}

/*
    Creates a dict with provided key-value pairs. The first key that equals
    `cIntStringDictEmptyKey` will stop further insertion.
*/
int xsIntStringDict(int k1 = cIntStringDictEmptyKey, string v1 = "", int k2 = cIntStringDictEmptyKey, string v2 = "", int k3 = cIntStringDictEmptyKey, string v3 = "", int k4 = cIntStringDictEmptyKey, string v4 = "", int k5 = cIntStringDictEmptyKey, string v5 = "", int k6 = cIntStringDictEmptyKey, string v6 = "") {
    int dct = xsIntStringDictCreate();
    if (dct < 0) {
        return (cIntStringDictGenericError);
    }
    if (k1 == cIntStringDictEmptyKey) {
        return (dct);
    }
    xsIntStringDictPut(dct, k1, v1);
    if (k2 == cIntStringDictEmptyKey) {
        return (dct);
    }
    xsIntStringDictPut(dct, k2, v2);
    if (k3 == cIntStringDictEmptyKey) {
        return (dct);
    }
    xsIntStringDictPut(dct, k3, v3);
    if (k4 == cIntStringDictEmptyKey) {
        return (dct);
    }
    xsIntStringDictPut(dct, k4, v4);
    if (k5 == cIntStringDictEmptyKey) {
        return (dct);
    }
    xsIntStringDictPut(dct, k5, v5);
    if (k6 == cIntStringDictEmptyKey) {
        return (dct);
    }
    xsIntStringDictPut(dct, k6, v6);
    return (dct);
}

/*
    Returns the value associated with the given key. Sets last error on completion.
*/
string xsIntStringDictGet(int dct = -1, int key = -1, string dft = "-1") {
    int capacity = xsArrayGetSize(dct);
    int slot = _xsIntStringDictFindSlot(dct, key, capacity);
    if (slot >= 0) {
        _intStringDictLastOperationStatus = cIntStringDictSuccess;
        return (_xsIntStringDictGetStoredValue(dct, slot));
    }
    _intStringDictLastOperationStatus = cIntStringDictNoKeyError;
    return (dft);
}

/*
    Removes the entry with the given key from the dict. Sets last error on completion.
    Uses backward shift deletion to maintain linear probing invariant (no tombstones).
*/
string xsIntStringDictRemove(int dct = -1, int key = -1) {
    int size = xsArrayGetInt(dct, 0);
    int capacity = xsArrayGetSize(dct);
    int numSlots = _xsIntStringDictValuesCapacityFromIntCapacity(capacity);
    int slot = _xsIntStringDictFindSlot(dct, key, capacity);
    if (slot < 0) {
        _intStringDictLastOperationStatus = cIntStringDictNoKeyError;
        return ("-1");
    }
    string foundVal = _xsIntStringDictGetStoredValue(dct, slot);
    int g = slot;
    int q = g + 1;
    if (q >= capacity) {
        q = 2;
    }
    int shiftSteps = 0;
    int qKey = xsArrayGetInt(dct, q);
    while ((qKey != cIntStringDictEmptyKey) && (shiftSteps < numSlots)) {
        int qHome = _xsIntStringDictHash(qKey, capacity);
        int gSlot = g - 2;
        int qSlot = q - 2;
        int hSlot = qHome - 2;
        int distG = ((gSlot - hSlot) + numSlots) % numSlots;
        int distQ = ((qSlot - hSlot) + numSlots) % numSlots;
        if (distG < distQ) {
            xsArraySetInt(dct, g, qKey);
            _xsIntStringDictSetStoredValue(dct, g, _xsIntStringDictGetStoredValue(dct, q));
            g = q;
        }
        q++;
        if (q >= capacity) {
            q = 2;
        }
        shiftSteps++;
        qKey = xsArrayGetInt(dct, q);
    }
    _xsIntStringDictClearSlot(dct, g);
    xsArraySetInt(dct, 0, size - 1);
    _intStringDictLastOperationStatus = cIntStringDictSuccess;
    return (foundVal);
}

bool xsIntStringDictContains(int dct = -1, int key = -1) {
    int capacity = xsArrayGetSize(dct);
    return (_xsIntStringDictFindSlot(dct, key, capacity) >= 0);
}

int xsIntStringDictSize(int dct = -1) {
    return (xsArrayGetInt(dct, 0));
}

/*
    Removes all entries from the dict and shrinks the backing arrays.
*/
int xsIntStringDictClear(int dct = -1) {
    int capacity = xsArrayGetSize(dct);
    _xsIntStringDictClearSlots(dct, capacity);
    xsArraySetInt(dct, 0, 0);
    if (capacity > cIntStringDictInitialCapacity) {
        int valuesArr = _xsIntStringDictGetValuesArray(dct);
        int r = xsArrayResizeInt(dct, cIntStringDictInitialCapacity);
        if (r != 1) {
            return (cIntStringDictGenericError);
        }
        int rValues = xsArrayResizeString(valuesArr, cIntStringDictInitialCapacity - 2);
        if (rValues != 1) {
            return (cIntStringDictGenericError);
        }
    }
    return (cIntStringDictSuccess);
}

/*
    Returns a deep copy of the dict.
*/
int xsIntStringDictCopy(int dct = -1) {
    int capacity = xsArrayGetSize(dct);
    int valuesCapacity = _xsIntStringDictValuesCapacityFromIntCapacity(capacity);
    int newDct = xsArrayCreateInt(capacity, cIntStringDictEmptyKey);
    if (newDct < 0) {
        return (cIntStringDictResizeFailedError);
    }
    int newValuesArr = xsArrayCreateString(valuesCapacity);
    if (newValuesArr < 0) {
        xsArrayResizeInt(newDct, 0);
        return (cIntStringDictResizeFailedError);
    }
    xsArraySetInt(newDct, 0, xsArrayGetInt(dct, 0));
    xsArraySetInt(newDct, 1, newValuesArr);
    for (i = 2; < capacity) {
        int storedKey = xsArrayGetInt(dct, i);
        if (storedKey != cIntStringDictEmptyKey) {
            xsArraySetInt(newDct, i, storedKey);
            xsArraySetString(newValuesArr, i - 2, _xsIntStringDictGetStoredValue(dct, i));
        }
    }
    return (newDct);
}

/*
    Returns a string representation of the dict in the format `{k1 - "v1", k2 - "v2", ...}`.
*/
string xsIntStringDictToString(int dct = -1) {
    int capacity = xsArrayGetSize(dct);
    string s = "{";
    bool first = true;
    for (i = 2; < capacity) {
        int key = xsArrayGetInt(dct, i);
        if (key != cIntStringDictEmptyKey) {
            if (first) {
                first = false;
            } else {
                s = s + ", ";
            }
            s = s + (key + ": \"" + _xsIntStringDictGetStoredValue(dct, i) + "\"");
        }
    }
    s = s + "}";
    return (s);
}

int xsIntStringDictLastError() {
    return (_intStringDictLastOperationStatus);
}

int _xsIntStringDictFindNextOccupied(int dct = -1, int start = 2, int capacity = 0) {
    int slot = start;
    while (slot < capacity) {
        int storedKey = xsArrayGetInt(dct, slot);
        if (storedKey != cIntStringDictEmptyKey) {
            _intStringDictLastOperationStatus = cIntStringDictSuccess;
            return (storedKey);
        }
        slot++;
    }
    _intStringDictLastOperationStatus = cIntStringDictNoKeyError;
    return (cIntStringDictGenericError);
}

/*
    Returns the next key in the dict for stateless iteration. Sets last error on completion.
*/
int xsIntStringDictNextKey(int dct = -1, bool isFirst = true, int prevKey = -1) {
    int capacity = xsArrayGetSize(dct);
    if (isFirst) {
        return (_xsIntStringDictFindNextOccupied(dct, 2, capacity));
    }
    int slot = _xsIntStringDictFindSlot(dct, prevKey, capacity);
    if (slot < 0) {
        _intStringDictLastOperationStatus = cIntStringDictNoKeyError;
        return (cIntStringDictGenericError);
    }
    int nextStart = slot + 1;
    return (_xsIntStringDictFindNextOccupied(dct, nextStart, capacity));
}

bool xsIntStringDictHasNext(int dct = -1, bool isFirst = true, int prevKey = -1) {
    int capacity = xsArrayGetSize(dct);
    int start = 2;
    if (isFirst == false) {
        int slot = _xsIntStringDictFindSlot(dct, prevKey, capacity);
        if (slot < 0) {
            return (false);
        }
        start = slot + 1;
    }
    while (start < capacity) {
        if (xsArrayGetInt(dct, start) != cIntStringDictEmptyKey) {
            return (true);
        }
        start++;
    }
    return (false);
}

/*
    Inserts all key-value pairs from another dict into the source dict, overwriting existing keys.
*/
int xsIntStringDictUpdate(int source = -1, int dct = -1) {
    int capacity = xsArrayGetSize(dct);
    for (i = 2; < capacity) {
        int key = xsArrayGetInt(dct, i);
        if (key != cIntStringDictEmptyKey) {
            xsIntStringDictPut(source, key, _xsIntStringDictGetStoredValue(dct, i));
            if ((_intStringDictLastOperationStatus != cIntStringDictSuccess) && (_intStringDictLastOperationStatus != cIntStringDictNoKeyError)) {
                return (_intStringDictLastOperationStatus);
            }
        }
    }
    _intStringDictLastOperationStatus = cIntStringDictSuccess;
    return (cIntStringDictSuccess);
}

/*
    Inserts the key-value pair only if the key is not already present. Sets last error on completion.
    If `key` equals `cIntStringDictEmptyKey`, the call is a no-op and returns
    `"-1"` with last error set to `cIntStringDictGenericError`.
*/
string xsIntStringDictPutIfAbsent(int dct = -1, int key = -1, string val = "") {
    if (key == cIntStringDictEmptyKey) {
        _intStringDictLastOperationStatus = cIntStringDictGenericError;
        return ("-1");
    }
    int size = xsArrayGetInt(dct, 0);
    int capacity = xsArrayGetSize(dct);
    int slot = _xsIntStringDictFindSlot(dct, key, capacity);
    if (slot >= 0) {
        _intStringDictLastOperationStatus = cIntStringDictSuccess;
        return (_xsIntStringDictGetStoredValue(dct, slot));
    }
    int r = _xsIntStringDictRehashIfNeeded(dct, size, capacity, size + 1);
    if (r != cIntStringDictSuccess) {
        return ("-1");
    }
    capacity = xsArrayGetSize(dct);
    string result = _xsIntStringDictUpsert(dct, key, val, capacity);
    if (_intStringDictLastOperationStatus == cIntStringDictNoKeyError) {
        xsArraySetInt(dct, 0, size + 1);
        return ("-1");
    }
    if (_intStringDictLastOperationStatus != cIntStringDictSuccess) {
        return ("-1");
    }
    return (result);
}

/*
    Returns a new int array containing all keys in the dict. Order is arbitrary.
*/
int xsIntStringDictKeys(int dct = -1) {
    int size = xsArrayGetInt(dct, 0);
    int arr = xsArrayCreateInt(size, 0);
    if (arr < 0) {
        return (cIntStringDictResizeFailedError);
    }
    int capacity = xsArrayGetSize(dct);
    int idx = 0;
    for (i = 2; < capacity) {
        int storedKey = xsArrayGetInt(dct, i);
        if (storedKey != cIntStringDictEmptyKey) {
            xsArraySetInt(arr, idx, storedKey);
            idx++;
        }
    }
    return (arr);
}

/*
    Returns a new string array containing all values in the dict. Order matches
    `xsIntStringDictKeys`.
*/
int xsIntStringDictValues(int dct = -1) {
    int size = xsArrayGetInt(dct, 0);
    int arr = xsArrayCreateString(size);
    if (arr < 0) {
        return (cIntStringDictResizeFailedError);
    }
    int capacity = xsArrayGetSize(dct);
    int idx = 0;
    for (i = 2; < capacity) {
        int storedKey = xsArrayGetInt(dct, i);
        if (storedKey != cIntStringDictEmptyKey) {
            xsArraySetString(arr, idx, _xsIntStringDictGetStoredValue(dct, i));
            idx++;
        }
    }
    return (arr);
}

/*
    Returns true if both dicts contain the same key-value pairs.
*/
bool xsIntStringDictEquals(int a = -1, int b = -1) {
    int sizeA = xsArrayGetInt(a, 0);
    int sizeB = xsArrayGetInt(b, 0);
    if (sizeA != sizeB) {
        return (false);
    }
    int capacity = xsArrayGetSize(a);
    for (i = 2; < capacity) {
        int key = xsArrayGetInt(a, i);
        if (key != cIntStringDictEmptyKey) {
            string val = _xsIntStringDictGetStoredValue(a, i);
            if (xsIntStringDictGet(b, key) != val) {
                return (false);
            }
            if (xsIntStringDictLastError() != cIntStringDictSuccess) {
                return (false);
            }
        }
    }
    return (true);
}

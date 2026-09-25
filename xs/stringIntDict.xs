extern const int cStringIntDictSuccess = 0;
extern const int cStringIntDictGenericError = -1;
extern const int cStringIntDictNoKeyError = -2;
extern const int cStringIntDictResizeFailedError = -3;
extern const int cStringIntDictMaxCapacityError = -4;
extern const int cStringIntDictMaxCapacity = 249999998;
extern const float cStringIntDictMaxLoadFactor = 0.75;
extern const int cStringIntDictInitialCapacity = 18;
extern const int cStringIntDictHashConstant = 16777619;
int _stringIntDictLastOperationStatus = cStringIntDictSuccess;
int _stringIntDictTempKeys = -1;
int _stringIntDictTempValues = -1;

int _xsStringIntDictKeysCapacityFromIntCapacity(int capacity = 0) {
    return (capacity - 2);
}

int _xsStringIntDictGetKeysArray(int dct = -1) {
    return (xsArrayGetInt(dct, 1));
}

string _xsStringIntDictGetStoredKey(int dct = -1, int slot = 2, int keysArr = -2) {
    if (keysArr < -1) {
        keysArr = _xsStringIntDictGetKeysArray(dct);
    }
    return (xsArrayGetString(keysArr, slot - 2));
}

void _xsStringIntDictSetStoredKey(int dct = -1, int slot = 2, string key = "", int keysArr = -2) {
    if (keysArr < -1) {
        keysArr = _xsStringIntDictGetKeysArray(dct);
    }
    xsArraySetString(keysArr, slot - 2, key);
}

int _xsStringIntDictGetStoredValue(int dct = -1, int slot = 2) {
    return (xsArrayGetInt(dct, slot));
}

void _xsStringIntDictSetStoredValue(int dct = -1, int slot = 2, int value = 0) {
    xsArraySetInt(dct, slot, value);
}

void _xsStringIntDictClearSlot(int dct = -1, int slot = 2, int keysArr = -2) {
    _xsStringIntDictSetStoredKey(dct, slot, "!<[empty", keysArr);
}

/*
    Creates an empty string-to-int dictionary.
    Keys equal to `"!<[empty"` are reserved as the internal
    empty-slot sentinel and cannot be stored. `put` and `putIfAbsent` silently reject them.
    @return created dict id, or `cStringIntDictGenericError` on error
*/
int xsStringIntDictCreate() {
    int dct = xsArrayCreateInt(cStringIntDictInitialCapacity, 0);
    if (dct < 0) {
        return (cStringIntDictGenericError);
    }
    int keysCapacity = _xsStringIntDictKeysCapacityFromIntCapacity(cStringIntDictInitialCapacity);
    int keysArr = xsArrayCreateString(keysCapacity, "!<[empty");
    if (keysArr < 0) {
        xsArrayResizeInt(dct, 0);
        return (cStringIntDictGenericError);
    }
    xsArraySetInt(dct, 0, 0);
    xsArraySetInt(dct, 1, keysArr);
    return (dct);
}

int _xsStringIntDictHash(string key = "", int capacity = 0) {
    int h = 0;
    int n = strLen(key);
    for (i = 0; < n) {
        int ch = ord(strCharAt(key, i));
        h = (h + ch) * cStringIntDictHashConstant;
    }
    int numSlots = _xsStringIntDictKeysCapacityFromIntCapacity(capacity);
    h = h % numSlots;
    if (h < 0) {
        h = h + numSlots;
    }
    return (h + 2);
}

/*
    Returns int-array index of slot containing key, or -1 if not found.
*/
int _xsStringIntDictFindSlot(int dct = -1, string key = "", int capacity = 0) {
    int numSlots = _xsStringIntDictKeysCapacityFromIntCapacity(capacity);
    int keysArr = _xsStringIntDictGetKeysArray(dct);
    int home = _xsStringIntDictHash(key, capacity);
    int slot = home;
    int steps = 0;
    while (steps < numSlots) {
        string storedKey = _xsStringIntDictGetStoredKey(dct, slot, keysArr);
        if (storedKey == "!<[empty") {
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

int _xsStringIntDictUpsert(int dct = -1, string key = "", int val = 0, int capacity = 0) {
    int numSlots = _xsStringIntDictKeysCapacityFromIntCapacity(capacity);
    int keysArr = _xsStringIntDictGetKeysArray(dct);
    int slot = _xsStringIntDictHash(key, capacity);
    int steps = 0;
    while (steps < numSlots) {
        string storedKey = _xsStringIntDictGetStoredKey(dct, slot, keysArr);
        if (storedKey == "!<[empty") {
            _xsStringIntDictSetStoredKey(dct, slot, key, keysArr);
            _xsStringIntDictSetStoredValue(dct, slot, val);
            _stringIntDictLastOperationStatus = cStringIntDictNoKeyError;
            return (cStringIntDictGenericError);
        }
        if (storedKey == key) {
            int oldVal = _xsStringIntDictGetStoredValue(dct, slot);
            _xsStringIntDictSetStoredValue(dct, slot, val);
            _stringIntDictLastOperationStatus = cStringIntDictSuccess;
            return (oldVal);
        }
        slot++;
        if (slot >= capacity) {
            slot = 2;
        }
        steps++;
    }
    _stringIntDictLastOperationStatus = cStringIntDictMaxCapacityError;
    return (cStringIntDictGenericError);
}

int _xsStringIntDictMoveToTempArrays(int dct = -1, int size = 0, int capacity = 0) {
    int maxKeysCapacity = cStringIntDictMaxCapacity - 2;
    if (_stringIntDictTempKeys < 0) {
        _stringIntDictTempKeys = xsArrayCreateString(size, "!<[empty");
        if (_stringIntDictTempKeys < 0) {
            return (cStringIntDictResizeFailedError);
        }
    } else {
        int tempKeysCapacity = xsArrayGetSize(_stringIntDictTempKeys);
        if (tempKeysCapacity < size) {
            if (size > maxKeysCapacity) {
                return (cStringIntDictMaxCapacityError);
            }
            int rKeys = xsArrayResizeString(_stringIntDictTempKeys, size);
            if (rKeys != 1) {
                return (cStringIntDictResizeFailedError);
            }
        }
    }
    if (_stringIntDictTempValues < 0) {
        _stringIntDictTempValues = xsArrayCreateInt(size, 0);
        if (_stringIntDictTempValues < 0) {
            return (cStringIntDictResizeFailedError);
        }
    } else {
        int tempValuesCapacity = xsArrayGetSize(_stringIntDictTempValues);
        if (tempValuesCapacity < size) {
            if (size > maxKeysCapacity) {
                return (cStringIntDictMaxCapacityError);
            }
            int rValues = xsArrayResizeInt(_stringIntDictTempValues, size);
            if (rValues != 1) {
                return (cStringIntDictResizeFailedError);
            }
        }
    }
    int keysArr = _xsStringIntDictGetKeysArray(dct);
    int t = 0;
    for (i = 2; < capacity) {
        string storedKey = _xsStringIntDictGetStoredKey(dct, i, keysArr);
        if (storedKey != "!<[empty") {
            xsArraySetString(_stringIntDictTempKeys, t, storedKey);
            xsArraySetInt(_stringIntDictTempValues, t, _xsStringIntDictGetStoredValue(dct, i));
            t++;
        }
    }
    return (size);
}

void _xsStringIntDictClearSlots(int dct = -1, int capacity = -1) {
    int keysArr = _xsStringIntDictGetKeysArray(dct);
    for (j = 2; < capacity) {
        _xsStringIntDictClearSlot(dct, j, keysArr);
    }
}

int _xsStringIntDictRehashIfNeeded(int dct = -1, int size = 0, int capacity = 0, int requiredSize = -1) {
    if (requiredSize < 0) {
        requiredSize = size;
    }
    float loadFactor = (0.0 + requiredSize) / _xsStringIntDictKeysCapacityFromIntCapacity(capacity);
    if (loadFactor > cStringIntDictMaxLoadFactor) {
        int storeStatus = _stringIntDictLastOperationStatus;
        int newKeysCapacity = _xsStringIntDictKeysCapacityFromIntCapacity(capacity) * 2;
        int newCapacity = newKeysCapacity + 2;
        if (newCapacity > cStringIntDictMaxCapacity) {
            newCapacity = cStringIntDictMaxCapacity;
        }
        if (newCapacity <= capacity) {
            _stringIntDictLastOperationStatus = cStringIntDictMaxCapacityError;
            return (cStringIntDictGenericError);
        }
        newKeysCapacity = _xsStringIntDictKeysCapacityFromIntCapacity(newCapacity);
        int tempDataSize = _xsStringIntDictMoveToTempArrays(dct, size, capacity);
        if (tempDataSize < 0) {
            _stringIntDictLastOperationStatus = tempDataSize;
            return (cStringIntDictGenericError);
        }
        int keysArr = _xsStringIntDictGetKeysArray(dct);
        int rKeys = xsArrayResizeString(keysArr, newKeysCapacity);
        if (rKeys != 1) {
            _stringIntDictLastOperationStatus = cStringIntDictResizeFailedError;
            return (cStringIntDictGenericError);
        }
        int r = xsArrayResizeInt(dct, newCapacity);
        if (r != 1) {
            _stringIntDictLastOperationStatus = cStringIntDictResizeFailedError;
            return (cStringIntDictGenericError);
        }
        _xsStringIntDictClearSlots(dct, newCapacity);
        for (t = 0; < tempDataSize) {
            _xsStringIntDictUpsert(dct, xsArrayGetString(_stringIntDictTempKeys, t), xsArrayGetInt(_stringIntDictTempValues, t), newCapacity);
            if ((_stringIntDictLastOperationStatus < 0) && (_stringIntDictLastOperationStatus != cStringIntDictNoKeyError)) {
                return (cStringIntDictGenericError);
            }
        }
        _stringIntDictLastOperationStatus = storeStatus;
    }
    return (cStringIntDictSuccess);
}

/*
    Inserts or updates a key-value pair. Triggers a rehash when load factor exceeds the threshold.
    Sets last error on completion.
    If `key` equals `"!<[empty"`, the call is a no-op and returns
    `cStringIntDictGenericError` with last error set to `cStringIntDictGenericError`.
    @return previous value if the key already existed, or `cStringIntDictGenericError`
        if newly inserted or on error. Callers must check `xs_string_int_dict_last_error()`.
*/
int xsStringIntDictPut(int dct = -1, string key = "", int val = 0) {
    if (key == "!<[empty") {
        _stringIntDictLastOperationStatus = cStringIntDictGenericError;
        return (cStringIntDictGenericError);
    }
    int size = xsArrayGetInt(dct, 0);
    int capacity = xsArrayGetSize(dct);
    int slot = _xsStringIntDictFindSlot(dct, key, capacity);
    if (slot >= 0) {
        int oldVal = _xsStringIntDictGetStoredValue(dct, slot);
        _xsStringIntDictSetStoredValue(dct, slot, val);
        _stringIntDictLastOperationStatus = cStringIntDictSuccess;
        return (oldVal);
    }
    int r = _xsStringIntDictRehashIfNeeded(dct, size, capacity, size + 1);
    if (r != cStringIntDictSuccess) {
        return (cStringIntDictGenericError);
    }
    capacity = xsArrayGetSize(dct);
    int previousValue = _xsStringIntDictUpsert(dct, key, val, capacity);
    if (_stringIntDictLastOperationStatus == cStringIntDictNoKeyError) {
        xsArraySetInt(dct, 0, size + 1);
        return (cStringIntDictGenericError);
    }
    if (_stringIntDictLastOperationStatus != cStringIntDictSuccess) {
        return (cStringIntDictGenericError);
    }
    return (previousValue);
}

/*
    Creates a dict with provided key-value pairs. The first key that equals
    `"!<[empty"` will stop further insertion.
*/
int xsStringIntDict(string k1 = "!<[empty", int v1 = 0, string k2 = "!<[empty", int v2 = 0, string k3 = "!<[empty", int v3 = 0, string k4 = "!<[empty", int v4 = 0, string k5 = "!<[empty", int v5 = 0, string k6 = "!<[empty", int v6 = 0) {
    int dct = xsStringIntDictCreate();
    if (dct < 0) {
        return (cStringIntDictGenericError);
    }
    if (k1 == "!<[empty") {
        return (dct);
    }
    xsStringIntDictPut(dct, k1, v1);
    if (k2 == "!<[empty") {
        return (dct);
    }
    xsStringIntDictPut(dct, k2, v2);
    if (k3 == "!<[empty") {
        return (dct);
    }
    xsStringIntDictPut(dct, k3, v3);
    if (k4 == "!<[empty") {
        return (dct);
    }
    xsStringIntDictPut(dct, k4, v4);
    if (k5 == "!<[empty") {
        return (dct);
    }
    xsStringIntDictPut(dct, k5, v5);
    if (k6 == "!<[empty") {
        return (dct);
    }
    xsStringIntDictPut(dct, k6, v6);
    return (dct);
}

/*
    Returns the value associated with the given key. Sets last error on completion.
*/
int xsStringIntDictGet(int dct = -1, string key = "", int dft = -1) {
    int capacity = xsArrayGetSize(dct);
    int slot = _xsStringIntDictFindSlot(dct, key, capacity);
    if (slot >= 0) {
        _stringIntDictLastOperationStatus = cStringIntDictSuccess;
        return (_xsStringIntDictGetStoredValue(dct, slot));
    }
    _stringIntDictLastOperationStatus = cStringIntDictNoKeyError;
    return (dft);
}

/*
    Removes the entry with the given key from the dict. Sets last error on completion.
    Uses backward shift deletion to maintain linear probing invariant (no tombstones).
*/
int xsStringIntDictRemove(int dct = -1, string key = "") {
    int size = xsArrayGetInt(dct, 0);
    int capacity = xsArrayGetSize(dct);
    int numSlots = _xsStringIntDictKeysCapacityFromIntCapacity(capacity);
    int slot = _xsStringIntDictFindSlot(dct, key, capacity);
    if (slot < 0) {
        _stringIntDictLastOperationStatus = cStringIntDictNoKeyError;
        return (cStringIntDictGenericError);
    }
    int foundVal = _xsStringIntDictGetStoredValue(dct, slot);
    int g = slot;
    int q = g + 1;
    if (q >= capacity) {
        q = 2;
    }
    int shiftSteps = 0;
    int keysArr = _xsStringIntDictGetKeysArray(dct);
    string qKey = _xsStringIntDictGetStoredKey(dct, q, keysArr);
    while ((qKey != "!<[empty") && (shiftSteps < numSlots)) {
        int qHome = _xsStringIntDictHash(qKey, capacity);
        int gSlot = g - 2;
        int qSlot = q - 2;
        int hSlot = qHome - 2;
        int distG = ((gSlot - hSlot) + numSlots) % numSlots;
        int distQ = ((qSlot - hSlot) + numSlots) % numSlots;
        if (distG < distQ) {
            _xsStringIntDictSetStoredKey(dct, g, qKey, keysArr);
            _xsStringIntDictSetStoredValue(dct, g, _xsStringIntDictGetStoredValue(dct, q));
            g = q;
        }
        q++;
        if (q >= capacity) {
            q = 2;
        }
        shiftSteps++;
        qKey = _xsStringIntDictGetStoredKey(dct, q, keysArr);
    }
    _xsStringIntDictClearSlot(dct, g, keysArr);
    xsArraySetInt(dct, 0, size - 1);
    _stringIntDictLastOperationStatus = cStringIntDictSuccess;
    return (foundVal);
}

bool xsStringIntDictContains(int dct = -1, string key = "") {
    int capacity = xsArrayGetSize(dct);
    return (_xsStringIntDictFindSlot(dct, key, capacity) >= 0);
}

int xsStringIntDictSize(int dct = -1) {
    return (xsArrayGetInt(dct, 0));
}

/*
    Removes all entries from the dict and shrinks the backing arrays.
*/
int xsStringIntDictClear(int dct = -1) {
    int capacity = xsArrayGetSize(dct);
    if (capacity > cStringIntDictInitialCapacity) {
        int keysCapacity = _xsStringIntDictKeysCapacityFromIntCapacity(cStringIntDictInitialCapacity);
        int newKeysArr = xsArrayCreateString(keysCapacity, "!<[empty");
        if (newKeysArr < 0) {
            return (cStringIntDictGenericError);
        }
        int oldKeysArr = _xsStringIntDictGetKeysArray(dct);
        int r = xsArrayResizeInt(dct, cStringIntDictInitialCapacity);
        if (r != 1) {
            xsArrayResizeString(newKeysArr, 0);
            return (cStringIntDictGenericError);
        }
        xsArraySetInt(dct, 0, 0);
        xsArraySetInt(dct, 1, newKeysArr);
        xsArrayResizeString(oldKeysArr, 0);
        return (cStringIntDictSuccess);
    }
    _xsStringIntDictClearSlots(dct, capacity);
    xsArraySetInt(dct, 0, 0);
    return (cStringIntDictSuccess);
}

/*
    Returns a deep copy of the dict.
*/
int xsStringIntDictCopy(int dct = -1) {
    int capacity = xsArrayGetSize(dct);
    int keysCapacity = _xsStringIntDictKeysCapacityFromIntCapacity(capacity);
    int newDct = xsArrayCreateInt(capacity, 0);
    if (newDct < 0) {
        return (cStringIntDictResizeFailedError);
    }
    int newKeysArr = xsArrayCreateString(keysCapacity, "!<[empty");
    if (newKeysArr < 0) {
        xsArrayResizeInt(newDct, 0);
        return (cStringIntDictResizeFailedError);
    }
    xsArraySetInt(newDct, 0, xsArrayGetInt(dct, 0));
    xsArraySetInt(newDct, 1, newKeysArr);
    int keysArr = _xsStringIntDictGetKeysArray(dct);
    for (i = 2; < capacity) {
        string storedKey = _xsStringIntDictGetStoredKey(dct, i, keysArr);
        if (storedKey != "!<[empty") {
            xsArraySetString(newKeysArr, i - 2, storedKey);
            xsArraySetInt(newDct, i, _xsStringIntDictGetStoredValue(dct, i));
        }
    }
    return (newDct);
}

/*
    Returns a string representation of the dict in the format `{"k1" - v1, "k2" - v2, ...}`.
*/
string xsStringIntDictToString(int dct = -1) {
    int capacity = xsArrayGetSize(dct);
    int keysArr = _xsStringIntDictGetKeysArray(dct);
    string s = "{";
    bool first = true;
    for (i = 2; < capacity) {
        string key = _xsStringIntDictGetStoredKey(dct, i, keysArr);
        if (key != "!<[empty") {
            if (first) {
                first = false;
            } else {
                s = s + ", ";
            }
            s = s + ("\"" + key + "\": " + _xsStringIntDictGetStoredValue(dct, i));
        }
    }
    s = s + "}";
    return (s);
}

int xsStringIntDictLastError() {
    return (_stringIntDictLastOperationStatus);
}

string _xsStringIntDictFindNextOccupied(int dct = -1, int start = 2, int capacity = 0) {
    int keysArr = _xsStringIntDictGetKeysArray(dct);
    int slot = start;
    while (slot < capacity) {
        string storedKey = _xsStringIntDictGetStoredKey(dct, slot, keysArr);
        if (storedKey != "!<[empty") {
            _stringIntDictLastOperationStatus = cStringIntDictSuccess;
            return (storedKey);
        }
        slot++;
    }
    _stringIntDictLastOperationStatus = cStringIntDictNoKeyError;
    return ("-1");
}

/*
    Returns the next key in the dict for stateless iteration. Sets last error on completion.
    Order is arbitrary.
*/
string xsStringIntDictNextKey(int dct = -1, bool isFirst = true, string prevKey = "!<[empty") {
    int capacity = xsArrayGetSize(dct);
    if (isFirst) {
        return (_xsStringIntDictFindNextOccupied(dct, 2, capacity));
    }
    int slot = _xsStringIntDictFindSlot(dct, prevKey, capacity);
    if (slot < 0) {
        _stringIntDictLastOperationStatus = cStringIntDictNoKeyError;
        return ("-1");
    }
    int nextStart = slot + 1;
    return (_xsStringIntDictFindNextOccupied(dct, nextStart, capacity));
}

bool xsStringIntDictHasNext(int dct = -1, bool isFirst = true, string prevKey = "!<[empty") {
    int capacity = xsArrayGetSize(dct);
    int start = 2;
    if (isFirst == false) {
        int slot = _xsStringIntDictFindSlot(dct, prevKey, capacity);
        if (slot < 0) {
            return (false);
        }
        start = slot + 1;
    }
    int keysArr = _xsStringIntDictGetKeysArray(dct);
    while (start < capacity) {
        if (_xsStringIntDictGetStoredKey(dct, start, keysArr) != "!<[empty") {
            return (true);
        }
        start++;
    }
    return (false);
}

/*
    Inserts all key-value pairs from another dict into the source dict, overwriting existing keys.
*/
int xsStringIntDictUpdate(int source = -1, int dct = -1) {
    int capacity = xsArrayGetSize(dct);
    int keysArr = _xsStringIntDictGetKeysArray(dct);
    for (i = 2; < capacity) {
        string key = _xsStringIntDictGetStoredKey(dct, i, keysArr);
        if (key != "!<[empty") {
            xsStringIntDictPut(source, key, _xsStringIntDictGetStoredValue(dct, i));
            if ((_stringIntDictLastOperationStatus != cStringIntDictSuccess) && (_stringIntDictLastOperationStatus != cStringIntDictNoKeyError)) {
                return (_stringIntDictLastOperationStatus);
            }
        }
    }
    _stringIntDictLastOperationStatus = cStringIntDictSuccess;
    return (cStringIntDictSuccess);
}

/*
    Inserts the key-value pair only if the key is not already present. Sets last error on completion.
    If `key` equals `"!<[empty"`, the call is a no-op and returns
    `cStringIntDictGenericError` with last error set to `cStringIntDictGenericError`.
*/
int xsStringIntDictPutIfAbsent(int dct = -1, string key = "", int val = 0) {
    if (key == "!<[empty") {
        _stringIntDictLastOperationStatus = cStringIntDictGenericError;
        return (cStringIntDictGenericError);
    }
    int size = xsArrayGetInt(dct, 0);
    int capacity = xsArrayGetSize(dct);
    int slot = _xsStringIntDictFindSlot(dct, key, capacity);
    if (slot >= 0) {
        _stringIntDictLastOperationStatus = cStringIntDictSuccess;
        return (_xsStringIntDictGetStoredValue(dct, slot));
    }
    int r = _xsStringIntDictRehashIfNeeded(dct, size, capacity, size + 1);
    if (r != cStringIntDictSuccess) {
        return (cStringIntDictGenericError);
    }
    capacity = xsArrayGetSize(dct);
    int result = _xsStringIntDictUpsert(dct, key, val, capacity);
    if (_stringIntDictLastOperationStatus == cStringIntDictNoKeyError) {
        xsArraySetInt(dct, 0, size + 1);
        return (cStringIntDictGenericError);
    }
    if (_stringIntDictLastOperationStatus != cStringIntDictSuccess) {
        return (cStringIntDictGenericError);
    }
    return (result);
}

/*
    Returns a new string array containing all keys in the dict. Order is arbitrary.
*/
int xsStringIntDictKeys(int dct = -1, int outArr = -1) {
    int size = xsArrayGetInt(dct, 0);
    int arr = outArr;
    if (arr < 0) {
        arr = xsArrayCreateString(size);
        if (arr < 0) {
            return (cStringIntDictResizeFailedError);
        }
    } else {
        int r = xsArrayResizeString(arr, size);
        if (r != 1) {
            return (cStringIntDictResizeFailedError);
        }
    }
    int capacity = xsArrayGetSize(dct);
    int keysArr = _xsStringIntDictGetKeysArray(dct);
    int idx = 0;
    for (i = 2; < capacity) {
        string storedKey = _xsStringIntDictGetStoredKey(dct, i, keysArr);
        if (storedKey != "!<[empty") {
            xsArraySetString(arr, idx, storedKey);
            idx++;
        }
    }
    return (arr);
}

/*
    Returns a new int array containing all values in the dict. Order matches `xsStringIntDictKeys`.
*/
int xsStringIntDictValues(int dct = -1, int outArr = -1) {
    int size = xsArrayGetInt(dct, 0);
    int arr = outArr;
    if (arr < 0) {
        arr = xsArrayCreateInt(size, 0);
        if (arr < 0) {
            return (cStringIntDictResizeFailedError);
        }
    } else {
        int r = xsArrayResizeInt(arr, size);
        if (r != 1) {
            return (cStringIntDictResizeFailedError);
        }
    }
    int capacity = xsArrayGetSize(dct);
    int keysArr = _xsStringIntDictGetKeysArray(dct);
    int idx = 0;
    for (i = 2; < capacity) {
        string storedKey = _xsStringIntDictGetStoredKey(dct, i, keysArr);
        if (storedKey != "!<[empty") {
            xsArraySetInt(arr, idx, _xsStringIntDictGetStoredValue(dct, i));
            idx++;
        }
    }
    return (arr);
}

/*
    Returns true if both dicts contain the same key-value pairs.
*/
bool xsStringIntDictEquals(int a = -1, int b = -1) {
    int sizeA = xsArrayGetInt(a, 0);
    int sizeB = xsArrayGetInt(b, 0);
    if (sizeA != sizeB) {
        return (false);
    }
    int capacity = xsArrayGetSize(a);
    int keysArr = _xsStringIntDictGetKeysArray(a);
    for (i = 2; < capacity) {
        string key = _xsStringIntDictGetStoredKey(a, i, keysArr);
        if (key != "!<[empty") {
            int val = _xsStringIntDictGetStoredValue(a, i);
            if (xsStringIntDictGet(b, key) != val) {
                return (false);
            }
            if (xsStringIntDictLastError() != cStringIntDictSuccess) {
                return (false);
            }
        }
    }
    return (true);
}

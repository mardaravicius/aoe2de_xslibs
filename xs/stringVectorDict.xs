extern const int cStringVectorDictSuccess = 0;
extern const int cStringVectorDictGenericError = -1;
extern const int cStringVectorDictNoKeyError = -2;
extern const int cStringVectorDictResizeFailedError = -3;
extern const int cStringVectorDictMaxCapacityError = -4;
extern const vector cStringVectorDictGenericErrorVector = vector(-1.0, -1.0, -1.0);
extern const int cStringVectorDictMaxCapacity = 333333330;
extern const float cStringVectorDictMaxLoadFactor = 0.75;
extern const int cStringVectorDictInitialCapacity = 16;
extern const int cStringVectorDictHashConstant = 16777619;
int _stringVectorDictLastOperationStatus = cStringVectorDictSuccess;
int _stringVectorDictTempKeys = -1;
int _stringVectorDictTempValues = -1;

int _xsStringVectorDictGetKeysArray(int dct = -1) {
    return (xsArrayGetInt(dct, 1));
}

int _xsStringVectorDictGetValuesArray(int dct = -1) {
    return (xsArrayGetInt(dct, 2));
}

int _xsStringVectorDictCapacity(int dct = -1) {
    return (xsArrayGetSize(_xsStringVectorDictGetKeysArray(dct)));
}

int _xsStringVectorDictKeyIndex(int slot = 0) {
    return (slot);
}

int _xsStringVectorDictValueBase(int slot = 0) {
    return (slot * 3);
}

string _xsStringVectorDictGetStoredKey(int dct = -1, int slot = 0) {
    return (xsArrayGetString(_xsStringVectorDictGetKeysArray(dct), _xsStringVectorDictKeyIndex(slot)));
}

void _xsStringVectorDictSetStoredKey(int dct = -1, int slot = 0, string key = "") {
    xsArraySetString(_xsStringVectorDictGetKeysArray(dct), _xsStringVectorDictKeyIndex(slot), key);
}

vector _xsStringVectorDictGetStoredValue(int dct = -1, int slot = 0) {
    int valuesArr = _xsStringVectorDictGetValuesArray(dct);
    int base = _xsStringVectorDictValueBase(slot);
    return (xsVectorSet(xsArrayGetFloat(valuesArr, base), xsArrayGetFloat(valuesArr, base + 1), xsArrayGetFloat(valuesArr, base + 2)));
}

void _xsStringVectorDictSetStoredValue(int dct = -1, int slot = 0, vector value = vector(0.0, 0.0, 0.0)) {
    int valuesArr = _xsStringVectorDictGetValuesArray(dct);
    int base = _xsStringVectorDictValueBase(slot);
    xsArraySetFloat(valuesArr, base, xsVectorGetX(value));
    xsArraySetFloat(valuesArr, base + 1, xsVectorGetY(value));
    xsArraySetFloat(valuesArr, base + 2, xsVectorGetZ(value));
}

void _xsStringVectorDictClearSlot(int dct = -1, int slot = 0) {
    _xsStringVectorDictSetStoredKey(dct, slot, "!<[empty");
}

/*
    Creates an empty string-to-vector dictionary.
    Keys equal to `"!<[empty"` are reserved as the internal
    empty-slot sentinel and cannot be stored. `put` and `putIfAbsent` silently reject them.
    @return created dict id, or `cStringVectorDictGenericError` on error
*/
int xsStringVectorDictCreate() {
    int dct = xsArrayCreateInt(3, 0);
    if (dct < 0) {
        return (cStringVectorDictGenericError);
    }
    int keysArr = xsArrayCreateString(cStringVectorDictInitialCapacity, "!<[empty");
    if (keysArr < 0) {
        xsArrayResizeInt(dct, 0);
        return (cStringVectorDictGenericError);
    }
    int valuesArr = xsArrayCreateFloat(cStringVectorDictInitialCapacity * 3, 0.0);
    if (valuesArr < 0) {
        xsArrayResizeString(keysArr, 0);
        xsArrayResizeInt(dct, 0);
        return (cStringVectorDictGenericError);
    }
    xsArraySetInt(dct, 0, 0);
    xsArraySetInt(dct, 1, keysArr);
    xsArraySetInt(dct, 2, valuesArr);
    return (dct);
}

int _xsStringVectorDictHash(string key = "", int capacity = 0) {
    int h = 0;
    int n = strLen(key);
    for (i = 0; < n) {
        int ch = ord(strCharAt(key, i));
        h = (h + ch) * cStringVectorDictHashConstant;
    }
    h = h % capacity;
    if (h < 0) {
        h = h + capacity;
    }
    return (h);
}

/*
    Returns slot index containing key, or -1 if not found.
*/
int _xsStringVectorDictFindSlot(int dct = -1, string key = "", int capacity = 0) {
    int numSlots = capacity;
    int home = _xsStringVectorDictHash(key, capacity);
    int slot = home;
    int steps = 0;
    while (steps < numSlots) {
        string storedKey = _xsStringVectorDictGetStoredKey(dct, slot);
        if (storedKey == "!<[empty") {
            return (-1);
        }
        if (storedKey == key) {
            return (slot);
        }
        slot++;
        if (slot >= capacity) {
            slot = 0;
        }
        steps++;
    }
    return (-1);
}

vector _xsStringVectorDictUpsert(int dct = -1, string key = "", vector val = vector(0.0, 0.0, 0.0), int capacity = 0) {
    int numSlots = capacity;
    int slot = _xsStringVectorDictHash(key, capacity);
    int steps = 0;
    while (steps < numSlots) {
        string storedKey = _xsStringVectorDictGetStoredKey(dct, slot);
        if (storedKey == "!<[empty") {
            _xsStringVectorDictSetStoredKey(dct, slot, key);
            _xsStringVectorDictSetStoredValue(dct, slot, val);
            _stringVectorDictLastOperationStatus = cStringVectorDictNoKeyError;
            return (cStringVectorDictGenericErrorVector);
        }
        if (storedKey == key) {
            vector oldVal = _xsStringVectorDictGetStoredValue(dct, slot);
            _xsStringVectorDictSetStoredValue(dct, slot, val);
            _stringVectorDictLastOperationStatus = cStringVectorDictSuccess;
            return (oldVal);
        }
        slot++;
        if (slot >= capacity) {
            slot = 0;
        }
        steps++;
    }
    _stringVectorDictLastOperationStatus = cStringVectorDictMaxCapacityError;
    return (cStringVectorDictGenericErrorVector);
}

int _xsStringVectorDictMoveToTempArrays(int dct = -1, int size = 0, int capacity = 0) {
    int tempDataSize = size;
    int tempFloatSize = size * 3;
    int maxSlots = cStringVectorDictMaxCapacity;
    if (_stringVectorDictTempKeys < 0) {
        _stringVectorDictTempKeys = xsArrayCreateString(tempDataSize, "!<[empty");
        if (_stringVectorDictTempKeys < 0) {
            return (cStringVectorDictResizeFailedError);
        }
    } else {
        int tempKeysCapacity = xsArrayGetSize(_stringVectorDictTempKeys);
        if (tempKeysCapacity < tempDataSize) {
            if (tempDataSize > maxSlots) {
                return (cStringVectorDictMaxCapacityError);
            }
            int rKeys = xsArrayResizeString(_stringVectorDictTempKeys, tempDataSize);
            if (rKeys != 1) {
                return (cStringVectorDictResizeFailedError);
            }
        }
    }
    if (_stringVectorDictTempValues < 0) {
        _stringVectorDictTempValues = xsArrayCreateFloat(tempFloatSize, 0.0);
        if (_stringVectorDictTempValues < 0) {
            return (cStringVectorDictResizeFailedError);
        }
    } else {
        int tempValuesCapacity = xsArrayGetSize(_stringVectorDictTempValues);
        if (tempValuesCapacity < tempFloatSize) {
            if (tempDataSize > maxSlots) {
                return (cStringVectorDictMaxCapacityError);
            }
            int rValues = xsArrayResizeFloat(_stringVectorDictTempValues, tempFloatSize);
            if (rValues != 1) {
                return (cStringVectorDictResizeFailedError);
            }
        }
    }
    int t = 0;
    for (i = 0; < capacity) {
        string storedKey = _xsStringVectorDictGetStoredKey(dct, i);
        if (storedKey != "!<[empty") {
            xsArraySetString(_stringVectorDictTempKeys, t, storedKey);
            vector value = _xsStringVectorDictGetStoredValue(dct, i);
            int base = t * 3;
            xsArraySetFloat(_stringVectorDictTempValues, base, xsVectorGetX(value));
            xsArraySetFloat(_stringVectorDictTempValues, base + 1, xsVectorGetY(value));
            xsArraySetFloat(_stringVectorDictTempValues, base + 2, xsVectorGetZ(value));
            t++;
        }
    }
    return (tempDataSize);
}

void _xsStringVectorDictClearSlots(int dct = -1, int capacity = -1) {
    for (j = 0; < capacity) {
        _xsStringVectorDictClearSlot(dct, j);
    }
}

int _xsStringVectorDictRehashIfNeeded(int dct = -1, int size = 0, int capacity = 0, int requiredSize = -1) {
    if (requiredSize < 0) {
        requiredSize = size;
    }
    float loadFactor = (0.0 + requiredSize) / capacity;
    if (loadFactor > cStringVectorDictMaxLoadFactor) {
        int storeStatus = _stringVectorDictLastOperationStatus;
        int newCapacity = capacity * 2;
        if (newCapacity > cStringVectorDictMaxCapacity) {
            newCapacity = cStringVectorDictMaxCapacity;
        }
        if (newCapacity <= capacity) {
            _stringVectorDictLastOperationStatus = cStringVectorDictMaxCapacityError;
            return (cStringVectorDictGenericError);
        }
        int tempDataSize = _xsStringVectorDictMoveToTempArrays(dct, size, capacity);
        if (tempDataSize < 0) {
            _stringVectorDictLastOperationStatus = tempDataSize;
            return (cStringVectorDictGenericError);
        }
        int valuesArr = _xsStringVectorDictGetValuesArray(dct);
        int rValues = xsArrayResizeFloat(valuesArr, newCapacity * 3);
        if (rValues != 1) {
            _stringVectorDictLastOperationStatus = cStringVectorDictResizeFailedError;
            return (cStringVectorDictGenericError);
        }
        int keysArr = _xsStringVectorDictGetKeysArray(dct);
        int rKeys = xsArrayResizeString(keysArr, newCapacity);
        if (rKeys != 1) {
            _stringVectorDictLastOperationStatus = cStringVectorDictResizeFailedError;
            return (cStringVectorDictGenericError);
        }
        _xsStringVectorDictClearSlots(dct, newCapacity);
        for (t = 0; < tempDataSize) {
            int base = t * 3;
            _xsStringVectorDictUpsert(dct, xsArrayGetString(_stringVectorDictTempKeys, t), xsVectorSet(xsArrayGetFloat(_stringVectorDictTempValues, base), xsArrayGetFloat(_stringVectorDictTempValues, base + 1), xsArrayGetFloat(_stringVectorDictTempValues, base + 2)), newCapacity);
            if ((_stringVectorDictLastOperationStatus < 0) && (_stringVectorDictLastOperationStatus != cStringVectorDictNoKeyError)) {
                return (cStringVectorDictGenericError);
            }
        }
        _stringVectorDictLastOperationStatus = storeStatus;
    }
    return (cStringVectorDictSuccess);
}

/*
    Inserts or updates a key-value pair. Triggers a rehash when load factor exceeds the threshold.
    Sets last error on completion.
    If `key` equals `"!<[empty"`, the call is a no-op and returns
    `cStringVectorDictGenericErrorVector` with last error set to `cStringVectorDictGenericError`.
    @return previous value if the key already existed, or `cStringVectorDictGenericErrorVector`
        if newly inserted or on error. Callers must check `xs_string_vector_dict_last_error()`.
*/
vector xsStringVectorDictPut(int dct = -1, string key = "", vector val = vector(0.0, 0.0, 0.0)) {
    if (key == "!<[empty") {
        _stringVectorDictLastOperationStatus = cStringVectorDictGenericError;
        return (cStringVectorDictGenericErrorVector);
    }
    int size = xsArrayGetInt(dct, 0);
    int capacity = _xsStringVectorDictCapacity(dct);
    int slot = _xsStringVectorDictFindSlot(dct, key, capacity);
    if (slot >= 0) {
        vector oldVal = _xsStringVectorDictGetStoredValue(dct, slot);
        _xsStringVectorDictSetStoredValue(dct, slot, val);
        _stringVectorDictLastOperationStatus = cStringVectorDictSuccess;
        return (oldVal);
    }
    int r = _xsStringVectorDictRehashIfNeeded(dct, size, capacity, size + 1);
    if (r != cStringVectorDictSuccess) {
        return (cStringVectorDictGenericErrorVector);
    }
    capacity = _xsStringVectorDictCapacity(dct);
    vector previousValue = _xsStringVectorDictUpsert(dct, key, val, capacity);
    if (_stringVectorDictLastOperationStatus == cStringVectorDictNoKeyError) {
        xsArraySetInt(dct, 0, size + 1);
        return (cStringVectorDictGenericErrorVector);
    }
    if (_stringVectorDictLastOperationStatus != cStringVectorDictSuccess) {
        return (cStringVectorDictGenericErrorVector);
    }
    return (previousValue);
}

/*
    Creates a dict with provided key-value pairs. The first key that equals
    `"!<[empty"` will stop further insertion.
*/
int xsStringVectorDict(string k1 = "!<[empty", vector v1 = vector(0.0, 0.0, 0.0), string k2 = "!<[empty", vector v2 = vector(0.0, 0.0, 0.0), string k3 = "!<[empty", vector v3 = vector(0.0, 0.0, 0.0), string k4 = "!<[empty", vector v4 = vector(0.0, 0.0, 0.0), string k5 = "!<[empty", vector v5 = vector(0.0, 0.0, 0.0), string k6 = "!<[empty", vector v6 = vector(0.0, 0.0, 0.0)) {
    int dct = xsStringVectorDictCreate();
    if (dct < 0) {
        return (cStringVectorDictGenericError);
    }
    if (k1 == "!<[empty") {
        return (dct);
    }
    xsStringVectorDictPut(dct, k1, v1);
    if (k2 == "!<[empty") {
        return (dct);
    }
    xsStringVectorDictPut(dct, k2, v2);
    if (k3 == "!<[empty") {
        return (dct);
    }
    xsStringVectorDictPut(dct, k3, v3);
    if (k4 == "!<[empty") {
        return (dct);
    }
    xsStringVectorDictPut(dct, k4, v4);
    if (k5 == "!<[empty") {
        return (dct);
    }
    xsStringVectorDictPut(dct, k5, v5);
    if (k6 == "!<[empty") {
        return (dct);
    }
    xsStringVectorDictPut(dct, k6, v6);
    return (dct);
}

/*
    Returns the value associated with the given key. Sets last error on completion.
*/
vector xsStringVectorDictGet(int dct = -1, string key = "", vector dft = cStringVectorDictGenericErrorVector) {
    int capacity = _xsStringVectorDictCapacity(dct);
    int slot = _xsStringVectorDictFindSlot(dct, key, capacity);
    if (slot >= 0) {
        _stringVectorDictLastOperationStatus = cStringVectorDictSuccess;
        return (_xsStringVectorDictGetStoredValue(dct, slot));
    }
    _stringVectorDictLastOperationStatus = cStringVectorDictNoKeyError;
    return (dft);
}

/*
    Removes the entry with the given key from the dict. Sets last error on completion.
    Uses backward shift deletion to maintain linear probing invariant (no tombstones).
*/
vector xsStringVectorDictRemove(int dct = -1, string key = "") {
    int size = xsArrayGetInt(dct, 0);
    int capacity = _xsStringVectorDictCapacity(dct);
    int numSlots = capacity;
    int slot = _xsStringVectorDictFindSlot(dct, key, capacity);
    if (slot < 0) {
        _stringVectorDictLastOperationStatus = cStringVectorDictNoKeyError;
        return (cStringVectorDictGenericErrorVector);
    }
    vector foundVal = _xsStringVectorDictGetStoredValue(dct, slot);
    int g = slot;
    int q = g + 1;
    if (q >= capacity) {
        q = 0;
    }
    int shiftSteps = 0;
    string qKey = _xsStringVectorDictGetStoredKey(dct, q);
    while ((qKey != "!<[empty") && (shiftSteps < numSlots)) {
        int qHome = _xsStringVectorDictHash(qKey, capacity);
        int distG = ((g - qHome) + numSlots) % numSlots;
        int distQ = ((q - qHome) + numSlots) % numSlots;
        if (distG < distQ) {
            _xsStringVectorDictSetStoredKey(dct, g, qKey);
            _xsStringVectorDictSetStoredValue(dct, g, _xsStringVectorDictGetStoredValue(dct, q));
            g = q;
        }
        q++;
        if (q >= capacity) {
            q = 0;
        }
        shiftSteps++;
        qKey = _xsStringVectorDictGetStoredKey(dct, q);
    }
    _xsStringVectorDictClearSlot(dct, g);
    xsArraySetInt(dct, 0, size - 1);
    _stringVectorDictLastOperationStatus = cStringVectorDictSuccess;
    return (foundVal);
}

bool xsStringVectorDictContains(int dct = -1, string key = "") {
    int capacity = _xsStringVectorDictCapacity(dct);
    return (_xsStringVectorDictFindSlot(dct, key, capacity) >= 0);
}

int xsStringVectorDictSize(int dct = -1) {
    return (xsArrayGetInt(dct, 0));
}

/*
    Removes all entries from the dict and shrinks the backing arrays.
*/
int xsStringVectorDictClear(int dct = -1) {
    int capacity = _xsStringVectorDictCapacity(dct);
    if (capacity > cStringVectorDictInitialCapacity) {
        int newKeysArr = xsArrayCreateString(cStringVectorDictInitialCapacity, "!<[empty");
        if (newKeysArr < 0) {
            return (cStringVectorDictGenericError);
        }
        int newValuesArr = xsArrayCreateFloat(cStringVectorDictInitialCapacity * 3, 0.0);
        if (newValuesArr < 0) {
            xsArrayResizeString(newKeysArr, 0);
            return (cStringVectorDictGenericError);
        }
        int oldKeysArr = _xsStringVectorDictGetKeysArray(dct);
        int oldValuesArr = _xsStringVectorDictGetValuesArray(dct);
        xsArraySetInt(dct, 0, 0);
        xsArraySetInt(dct, 1, newKeysArr);
        xsArraySetInt(dct, 2, newValuesArr);
        xsArrayResizeString(oldKeysArr, 0);
        xsArrayResizeFloat(oldValuesArr, 0);
        return (cStringVectorDictSuccess);
    }
    _xsStringVectorDictClearSlots(dct, capacity);
    xsArraySetInt(dct, 0, 0);
    return (cStringVectorDictSuccess);
}

/*
    Returns a deep copy of the dict.
*/
int xsStringVectorDictCopy(int dct = -1) {
    int capacity = _xsStringVectorDictCapacity(dct);
    int newDct = xsArrayCreateInt(3, 0);
    if (newDct < 0) {
        return (cStringVectorDictResizeFailedError);
    }
    int newKeysArr = xsArrayCreateString(capacity, "!<[empty");
    if (newKeysArr < 0) {
        xsArrayResizeInt(newDct, 0);
        return (cStringVectorDictResizeFailedError);
    }
    int newValuesArr = xsArrayCreateFloat(capacity * 3, 0.0);
    if (newValuesArr < 0) {
        xsArrayResizeString(newKeysArr, 0);
        xsArrayResizeInt(newDct, 0);
        return (cStringVectorDictResizeFailedError);
    }
    xsArraySetInt(newDct, 0, xsArrayGetInt(dct, 0));
    xsArraySetInt(newDct, 1, newKeysArr);
    xsArraySetInt(newDct, 2, newValuesArr);
    for (i = 0; < capacity) {
        string storedKey = _xsStringVectorDictGetStoredKey(dct, i);
        if (storedKey != "!<[empty") {
            xsArraySetString(newKeysArr, _xsStringVectorDictKeyIndex(i), storedKey);
            vector value = _xsStringVectorDictGetStoredValue(dct, i);
            int base = _xsStringVectorDictValueBase(i);
            xsArraySetFloat(newValuesArr, base, xsVectorGetX(value));
            xsArraySetFloat(newValuesArr, base + 1, xsVectorGetY(value));
            xsArraySetFloat(newValuesArr, base + 2, xsVectorGetZ(value));
        }
    }
    return (newDct);
}

/*
    Returns a string representation of the dict in the format `{"k1" - (x1, y1, z1), ...}`.
*/
string xsStringVectorDictToString(int dct = -1) {
    int capacity = _xsStringVectorDictCapacity(dct);
    string s = "{";
    bool first = true;
    for (i = 0; < capacity) {
        string key = _xsStringVectorDictGetStoredKey(dct, i);
        if (key != "!<[empty") {
            if (first) {
                first = false;
            } else {
                s = s + ", ";
            }
            s = s + ("\"" + key + "\": " + _xsStringVectorDictGetStoredValue(dct, i));
        }
    }
    s = s + "}";
    return (s);
}

int xsStringVectorDictLastError() {
    return (_stringVectorDictLastOperationStatus);
}

string _xsStringVectorDictFindNextOccupied(int dct = -1, int start = 0, int capacity = 0) {
    int slot = start;
    while (slot < capacity) {
        string storedKey = _xsStringVectorDictGetStoredKey(dct, slot);
        if (storedKey != "!<[empty") {
            _stringVectorDictLastOperationStatus = cStringVectorDictSuccess;
            return (storedKey);
        }
        slot++;
    }
    _stringVectorDictLastOperationStatus = cStringVectorDictNoKeyError;
    return ("-1");
}

/*
    Returns the next key in the dict for stateless iteration. Sets last error on completion.
    Order is arbitrary.
*/
string xsStringVectorDictNextKey(int dct = -1, bool isFirst = true, string prevKey = "!<[empty") {
    int capacity = _xsStringVectorDictCapacity(dct);
    if (isFirst) {
        return (_xsStringVectorDictFindNextOccupied(dct, 0, capacity));
    }
    int slot = _xsStringVectorDictFindSlot(dct, prevKey, capacity);
    if (slot < 0) {
        _stringVectorDictLastOperationStatus = cStringVectorDictNoKeyError;
        return ("-1");
    }
    int nextStart = slot + 1;
    return (_xsStringVectorDictFindNextOccupied(dct, nextStart, capacity));
}

bool xsStringVectorDictHasNext(int dct = -1, bool isFirst = true, string prevKey = "!<[empty") {
    int capacity = _xsStringVectorDictCapacity(dct);
    int start = 0;
    if (isFirst == false) {
        int slot = _xsStringVectorDictFindSlot(dct, prevKey, capacity);
        if (slot < 0) {
            return (false);
        }
        start = slot + 1;
    }
    while (start < capacity) {
        if (_xsStringVectorDictGetStoredKey(dct, start) != "!<[empty") {
            return (true);
        }
        start++;
    }
    return (false);
}

/*
    Inserts all key-value pairs from another dict into the source dict, overwriting existing keys.
*/
int xsStringVectorDictUpdate(int source = -1, int dct = -1) {
    int capacity = _xsStringVectorDictCapacity(dct);
    for (i = 0; < capacity) {
        string key = _xsStringVectorDictGetStoredKey(dct, i);
        if (key != "!<[empty") {
            xsStringVectorDictPut(source, key, _xsStringVectorDictGetStoredValue(dct, i));
            if ((_stringVectorDictLastOperationStatus != cStringVectorDictSuccess) && (_stringVectorDictLastOperationStatus != cStringVectorDictNoKeyError)) {
                return (_stringVectorDictLastOperationStatus);
            }
        }
    }
    _stringVectorDictLastOperationStatus = cStringVectorDictSuccess;
    return (cStringVectorDictSuccess);
}

/*
    Inserts the key-value pair only if the key is not already present. Sets last error on completion.
    If `key` equals `"!<[empty"`, the call is a no-op and returns
    `cStringVectorDictGenericErrorVector` with last error set to `cStringVectorDictGenericError`.
*/
vector xsStringVectorDictPutIfAbsent(int dct = -1, string key = "", vector val = vector(0.0, 0.0, 0.0)) {
    if (key == "!<[empty") {
        _stringVectorDictLastOperationStatus = cStringVectorDictGenericError;
        return (cStringVectorDictGenericErrorVector);
    }
    int size = xsArrayGetInt(dct, 0);
    int capacity = _xsStringVectorDictCapacity(dct);
    int slot = _xsStringVectorDictFindSlot(dct, key, capacity);
    if (slot >= 0) {
        _stringVectorDictLastOperationStatus = cStringVectorDictSuccess;
        return (_xsStringVectorDictGetStoredValue(dct, slot));
    }
    int r = _xsStringVectorDictRehashIfNeeded(dct, size, capacity, size + 1);
    if (r != cStringVectorDictSuccess) {
        return (cStringVectorDictGenericErrorVector);
    }
    capacity = _xsStringVectorDictCapacity(dct);
    vector result = _xsStringVectorDictUpsert(dct, key, val, capacity);
    if (_stringVectorDictLastOperationStatus == cStringVectorDictNoKeyError) {
        xsArraySetInt(dct, 0, size + 1);
        return (cStringVectorDictGenericErrorVector);
    }
    if (_stringVectorDictLastOperationStatus != cStringVectorDictSuccess) {
        return (cStringVectorDictGenericErrorVector);
    }
    return (result);
}

/*
    Returns a new string array containing all keys in the dict. Order is arbitrary.
*/
int xsStringVectorDictKeys(int dct = -1, int outArr = -1) {
    int size = xsArrayGetInt(dct, 0);
    int arr = outArr;
    if (arr < 0) {
        arr = xsArrayCreateString(size);
        if (arr < 0) {
            return (cStringVectorDictResizeFailedError);
        }
    } else {
        int r = xsArrayResizeString(arr, size);
        if (r != 1) {
            return (cStringVectorDictResizeFailedError);
        }
    }
    int capacity = _xsStringVectorDictCapacity(dct);
    int idx = 0;
    for (i = 0; < capacity) {
        string storedKey = _xsStringVectorDictGetStoredKey(dct, i);
        if (storedKey != "!<[empty") {
            xsArraySetString(arr, idx, storedKey);
            idx++;
        }
    }
    return (arr);
}

/*
    Returns a new vector array containing all values in the dict. Order matches `xsStringVectorDictKeys`.
*/
int xsStringVectorDictValues(int dct = -1, int outArr = -1) {
    int size = xsArrayGetInt(dct, 0);
    int arr = outArr;
    if (arr < 0) {
        arr = xsArrayCreateVector(size, vector(0.0, 0.0, 0.0));
        if (arr < 0) {
            return (cStringVectorDictResizeFailedError);
        }
    } else {
        int currentSize = xsArrayGetSize(arr);
        if (currentSize != size) {
            return (cStringVectorDictResizeFailedError);
        }
    }
    int capacity = _xsStringVectorDictCapacity(dct);
    int idx = 0;
    for (i = 0; < capacity) {
        string storedKey = _xsStringVectorDictGetStoredKey(dct, i);
        if (storedKey != "!<[empty") {
            int r = xsArraySetVector(arr, idx, _xsStringVectorDictGetStoredValue(dct, i));
            if (r != 1) {
                return (cStringVectorDictResizeFailedError);
            }
            idx++;
        }
    }
    return (arr);
}

/*
    Returns true if both dicts contain the same key-value pairs.
*/
bool xsStringVectorDictEquals(int a = -1, int b = -1) {
    int sizeA = xsArrayGetInt(a, 0);
    int sizeB = xsArrayGetInt(b, 0);
    if (sizeA != sizeB) {
        return (false);
    }
    int capacity = _xsStringVectorDictCapacity(a);
    for (i = 0; < capacity) {
        string key = _xsStringVectorDictGetStoredKey(a, i);
        if (key != "!<[empty") {
            vector val = _xsStringVectorDictGetStoredValue(a, i);
            if (xsStringVectorDictGet(b, key) != val) {
                return (false);
            }
            if (xsStringVectorDictLastError() != cStringVectorDictSuccess) {
                return (false);
            }
        }
    }
    return (true);
}

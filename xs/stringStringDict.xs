extern const int cStringStringDictSuccess = 0;
extern const int cStringStringDictGenericError = -1;
extern const int cStringStringDictNoKeyError = -2;
extern const int cStringStringDictResizeFailedError = -3;
extern const int cStringStringDictMaxCapacityError = -4;
extern const int cStringStringDictMaxCapacity = 333333331;
extern const float cStringStringDictMaxLoadFactor = 0.75;
extern const int cStringStringDictInitialCapacity = 16;
extern const int cStringStringDictHashConstant = 16777619;
int _stringStringDictLastOperationStatus = cStringStringDictSuccess;
int _stringStringDictTempKeys = -1;
int _stringStringDictTempValues = -1;

int _xsStringStringDictGetStringsArray(int dct = -1) {
    return (xsArrayGetInt(dct, 1));
}

int _xsStringStringDictCapacity(int dct = -1) {
    return (xsArrayGetSize(_xsStringStringDictGetStringsArray(dct)) / 2);
}

int _xsStringStringDictKeyIndex(int slot = 0) {
    return (slot * 2);
}

int _xsStringStringDictValueIndex(int slot = 0) {
    return (_xsStringStringDictKeyIndex(slot) + 1);
}

string _xsStringStringDictGetStoredKey(int dct = -1, int slot = 0) {
    return (xsArrayGetString(_xsStringStringDictGetStringsArray(dct), _xsStringStringDictKeyIndex(slot)));
}

void _xsStringStringDictSetStoredKey(int dct = -1, int slot = 0, string key = "") {
    xsArraySetString(_xsStringStringDictGetStringsArray(dct), _xsStringStringDictKeyIndex(slot), key);
}

string _xsStringStringDictGetStoredValue(int dct = -1, int slot = 0) {
    return (xsArrayGetString(_xsStringStringDictGetStringsArray(dct), _xsStringStringDictValueIndex(slot)));
}

void _xsStringStringDictSetStoredValue(int dct = -1, int slot = 0, string value = "") {
    xsArraySetString(_xsStringStringDictGetStringsArray(dct), _xsStringStringDictValueIndex(slot), value);
}

void _xsStringStringDictClearSlot(int dct = -1, int slot = 0) {
    _xsStringStringDictSetStoredKey(dct, slot, "!<[empty");
}

/*
    Creates an empty string-to-string dictionary.
    Keys equal to `"!<[empty"` are reserved as the internal
    empty-slot sentinel and cannot be stored. `put` and `putIfAbsent` silently reject them.
    @return created dict id, or `cStringStringDictGenericError` on error
*/
int xsStringStringDictCreate() {
    int dct = xsArrayCreateInt(2, 0);
    if (dct < 0) {
        return (cStringStringDictGenericError);
    }
    int stringsArr = xsArrayCreateString(cStringStringDictInitialCapacity * 2, "!<[empty");
    if (stringsArr < 0) {
        xsArrayResizeInt(dct, 0);
        return (cStringStringDictGenericError);
    }
    xsArraySetInt(dct, 0, 0);
    xsArraySetInt(dct, 1, stringsArr);
    return (dct);
}

int _xsStringStringDictHash(string key = "", int capacity = 0) {
    int h = 0;
    int n = strLen(key);
    for (i = 0; < n) {
        int ch = ord(strCharAt(key, i));
        h = (h + ch) * cStringStringDictHashConstant;
    }
    int numSlots = capacity;
    h = h % numSlots;
    if (h < 0) {
        h = h + numSlots;
    }
    return (h);
}

/*
    Returns slot index containing key, or -1 if not found.
*/
int _xsStringStringDictFindSlot(int dct = -1, string key = "", int capacity = 0) {
    int numSlots = capacity;
    int home = _xsStringStringDictHash(key, capacity);
    int slot = home;
    int steps = 0;
    while (steps < numSlots) {
        string storedKey = _xsStringStringDictGetStoredKey(dct, slot);
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

string _xsStringStringDictUpsert(int dct = -1, string key = "", string val = "", int capacity = 0) {
    int numSlots = capacity;
    int home = _xsStringStringDictHash(key, capacity);
    int slot = home;
    int steps = 0;
    while (steps < numSlots) {
        string storedKey = _xsStringStringDictGetStoredKey(dct, slot);
        if (storedKey == "!<[empty") {
            _xsStringStringDictSetStoredKey(dct, slot, key);
            _xsStringStringDictSetStoredValue(dct, slot, val);
            _stringStringDictLastOperationStatus = cStringStringDictNoKeyError;
            return ("-1");
        }
        if (storedKey == key) {
            string oldVal = _xsStringStringDictGetStoredValue(dct, slot);
            _xsStringStringDictSetStoredValue(dct, slot, val);
            _stringStringDictLastOperationStatus = cStringStringDictSuccess;
            return (oldVal);
        }
        slot++;
        if (slot >= capacity) {
            slot = 0;
        }
        steps++;
    }
    _stringStringDictLastOperationStatus = cStringStringDictMaxCapacityError;
    return ("-1");
}

int _xsStringStringDictMoveToTempArrays(int dct = -1, int size = 0, int capacity = 0) {
    int tempDataSize = size;
    int maxSlots = cStringStringDictMaxCapacity;
    if (_stringStringDictTempKeys < 0) {
        _stringStringDictTempKeys = xsArrayCreateString(tempDataSize, "!<[empty");
        if (_stringStringDictTempKeys < 0) {
            return (cStringStringDictResizeFailedError);
        }
    } else {
        int tempKeysCapacity = xsArrayGetSize(_stringStringDictTempKeys);
        if (tempKeysCapacity < tempDataSize) {
            if (tempDataSize > maxSlots) {
                return (cStringStringDictMaxCapacityError);
            }
            int rKeys = xsArrayResizeString(_stringStringDictTempKeys, tempDataSize);
            if (rKeys != 1) {
                return (cStringStringDictResizeFailedError);
            }
        }
    }
    if (_stringStringDictTempValues < 0) {
        _stringStringDictTempValues = xsArrayCreateString(tempDataSize);
        if (_stringStringDictTempValues < 0) {
            return (cStringStringDictResizeFailedError);
        }
    } else {
        int tempValuesCapacity = xsArrayGetSize(_stringStringDictTempValues);
        if (tempValuesCapacity < tempDataSize) {
            if (tempDataSize > maxSlots) {
                return (cStringStringDictMaxCapacityError);
            }
            int rValues = xsArrayResizeString(_stringStringDictTempValues, tempDataSize);
            if (rValues != 1) {
                return (cStringStringDictResizeFailedError);
            }
        }
    }
    int t = 0;
    for (i = 0; < capacity) {
        string storedKey = _xsStringStringDictGetStoredKey(dct, i);
        if (storedKey != "!<[empty") {
            xsArraySetString(_stringStringDictTempKeys, t, storedKey);
            xsArraySetString(_stringStringDictTempValues, t, _xsStringStringDictGetStoredValue(dct, i));
            t++;
        }
    }
    return (tempDataSize);
}

void _xsStringStringDictClearSlots(int dct = -1, int capacity = -1) {
    for (j = 0; < capacity) {
        _xsStringStringDictClearSlot(dct, j);
    }
}

int _xsStringStringDictRehashIfNeeded(int dct = -1, int size = 0, int capacity = 0, int requiredSize = -1) {
    if (requiredSize < 0) {
        requiredSize = size;
    }
    float loadFactor = (0.0 + requiredSize) / capacity;
    if (loadFactor > cStringStringDictMaxLoadFactor) {
        int storeStatus = _stringStringDictLastOperationStatus;
        int newCapacity = capacity * 2;
        if (newCapacity > cStringStringDictMaxCapacity) {
            newCapacity = cStringStringDictMaxCapacity;
        }
        if (newCapacity <= capacity) {
            _stringStringDictLastOperationStatus = cStringStringDictMaxCapacityError;
            return (cStringStringDictGenericError);
        }
        int tempDataSize = _xsStringStringDictMoveToTempArrays(dct, size, capacity);
        if (tempDataSize < 0) {
            _stringStringDictLastOperationStatus = tempDataSize;
            return (cStringStringDictGenericError);
        }
        int stringsArr = _xsStringStringDictGetStringsArray(dct);
        int rStrings = xsArrayResizeString(stringsArr, newCapacity * 2);
        if (rStrings != 1) {
            _stringStringDictLastOperationStatus = cStringStringDictResizeFailedError;
            return (cStringStringDictGenericError);
        }
        _xsStringStringDictClearSlots(dct, newCapacity);
        for (t = 0; < tempDataSize) {
            _xsStringStringDictUpsert(dct, xsArrayGetString(_stringStringDictTempKeys, t), xsArrayGetString(_stringStringDictTempValues, t), newCapacity);
            if ((_stringStringDictLastOperationStatus < 0) && (_stringStringDictLastOperationStatus != cStringStringDictNoKeyError)) {
                return (cStringStringDictGenericError);
            }
        }
        _stringStringDictLastOperationStatus = storeStatus;
    }
    return (cStringStringDictSuccess);
}

/*
    Inserts or updates a key-value pair. Triggers a rehash when load factor exceeds the threshold.
    Sets last error on completion.
    If `key` equals `"!<[empty"`, the call is a no-op and returns
    `"-1"` with last error set to `cStringStringDictGenericError`.
    @return previous value if the key already existed, or `"-1"`
        if newly inserted or on error. Callers must check `xs_string_string_dict_last_error()`.
*/
string xsStringStringDictPut(int dct = -1, string key = "", string val = "") {
    if (key == "!<[empty") {
        _stringStringDictLastOperationStatus = cStringStringDictGenericError;
        return ("-1");
    }
    int size = xsArrayGetInt(dct, 0);
    int capacity = _xsStringStringDictCapacity(dct);
    int slot = _xsStringStringDictFindSlot(dct, key, capacity);
    if (slot >= 0) {
        string oldVal = _xsStringStringDictGetStoredValue(dct, slot);
        _xsStringStringDictSetStoredValue(dct, slot, val);
        _stringStringDictLastOperationStatus = cStringStringDictSuccess;
        return (oldVal);
    }
    int r = _xsStringStringDictRehashIfNeeded(dct, size, capacity, size + 1);
    if (r != cStringStringDictSuccess) {
        return ("-1");
    }
    capacity = _xsStringStringDictCapacity(dct);
    string previousValue = _xsStringStringDictUpsert(dct, key, val, capacity);
    if (_stringStringDictLastOperationStatus == cStringStringDictNoKeyError) {
        xsArraySetInt(dct, 0, size + 1);
        return ("-1");
    }
    if (_stringStringDictLastOperationStatus != cStringStringDictSuccess) {
        return ("-1");
    }
    return (previousValue);
}

/*
    Creates a dict with provided key-value pairs. The first key that equals
    `"!<[empty"` will stop further insertion.
*/
int xsStringStringDict(string k1 = "!<[empty", string v1 = "", string k2 = "!<[empty", string v2 = "", string k3 = "!<[empty", string v3 = "", string k4 = "!<[empty", string v4 = "", string k5 = "!<[empty", string v5 = "", string k6 = "!<[empty", string v6 = "") {
    int dct = xsStringStringDictCreate();
    if (dct < 0) {
        return (cStringStringDictGenericError);
    }
    if (k1 == "!<[empty") {
        return (dct);
    }
    xsStringStringDictPut(dct, k1, v1);
    if (k2 == "!<[empty") {
        return (dct);
    }
    xsStringStringDictPut(dct, k2, v2);
    if (k3 == "!<[empty") {
        return (dct);
    }
    xsStringStringDictPut(dct, k3, v3);
    if (k4 == "!<[empty") {
        return (dct);
    }
    xsStringStringDictPut(dct, k4, v4);
    if (k5 == "!<[empty") {
        return (dct);
    }
    xsStringStringDictPut(dct, k5, v5);
    if (k6 == "!<[empty") {
        return (dct);
    }
    xsStringStringDictPut(dct, k6, v6);
    return (dct);
}

/*
    Returns the value associated with the given key. Sets last error on completion.
*/
string xsStringStringDictGet(int dct = -1, string key = "", string dft = "-1") {
    int capacity = _xsStringStringDictCapacity(dct);
    int slot = _xsStringStringDictFindSlot(dct, key, capacity);
    if (slot >= 0) {
        _stringStringDictLastOperationStatus = cStringStringDictSuccess;
        return (_xsStringStringDictGetStoredValue(dct, slot));
    }
    _stringStringDictLastOperationStatus = cStringStringDictNoKeyError;
    return (dft);
}

/*
    Removes the entry with the given key from the dict. Sets last error on completion.
    Uses backward shift deletion to maintain linear probing invariant (no tombstones).
*/
string xsStringStringDictRemove(int dct = -1, string key = "") {
    int size = xsArrayGetInt(dct, 0);
    int capacity = _xsStringStringDictCapacity(dct);
    int numSlots = capacity;
    int slot = _xsStringStringDictFindSlot(dct, key, capacity);
    if (slot < 0) {
        _stringStringDictLastOperationStatus = cStringStringDictNoKeyError;
        return ("-1");
    }
    string foundVal = _xsStringStringDictGetStoredValue(dct, slot);
    int g = slot;
    int q = g + 1;
    if (q >= capacity) {
        q = 0;
    }
    int shiftSteps = 0;
    string qKey = _xsStringStringDictGetStoredKey(dct, q);
    while ((qKey != "!<[empty") && (shiftSteps < numSlots)) {
        int qHome = _xsStringStringDictHash(qKey, capacity);
        int distG = ((g - qHome) + numSlots) % numSlots;
        int distQ = ((q - qHome) + numSlots) % numSlots;
        if (distG < distQ) {
            _xsStringStringDictSetStoredKey(dct, g, qKey);
            _xsStringStringDictSetStoredValue(dct, g, _xsStringStringDictGetStoredValue(dct, q));
            g = q;
        }
        q++;
        if (q >= capacity) {
            q = 0;
        }
        shiftSteps++;
        qKey = _xsStringStringDictGetStoredKey(dct, q);
    }
    _xsStringStringDictClearSlot(dct, g);
    xsArraySetInt(dct, 0, size - 1);
    _stringStringDictLastOperationStatus = cStringStringDictSuccess;
    return (foundVal);
}

bool xsStringStringDictContains(int dct = -1, string key = "") {
    int capacity = _xsStringStringDictCapacity(dct);
    return (_xsStringStringDictFindSlot(dct, key, capacity) >= 0);
}

int xsStringStringDictSize(int dct = -1) {
    return (xsArrayGetInt(dct, 0));
}

/*
    Removes all entries from the dict and shrinks the backing arrays.
*/
int xsStringStringDictClear(int dct = -1) {
    int capacity = _xsStringStringDictCapacity(dct);
    if (capacity > cStringStringDictInitialCapacity) {
        int newStringsArr = xsArrayCreateString(cStringStringDictInitialCapacity * 2, "!<[empty");
        if (newStringsArr < 0) {
            return (cStringStringDictGenericError);
        }
        int oldStringsArr = _xsStringStringDictGetStringsArray(dct);
        xsArraySetInt(dct, 0, 0);
        xsArraySetInt(dct, 1, newStringsArr);
        xsArrayResizeString(oldStringsArr, 0);
        return (cStringStringDictSuccess);
    }
    _xsStringStringDictClearSlots(dct, capacity);
    xsArraySetInt(dct, 0, 0);
    return (cStringStringDictSuccess);
}

/*
    Returns a deep copy of the dict.
*/
int xsStringStringDictCopy(int dct = -1) {
    int capacity = _xsStringStringDictCapacity(dct);
    int newDct = xsArrayCreateInt(2, 0);
    if (newDct < 0) {
        return (cStringStringDictResizeFailedError);
    }
    int newStringsArr = xsArrayCreateString(capacity * 2, "!<[empty");
    if (newStringsArr < 0) {
        xsArrayResizeInt(newDct, 0);
        return (cStringStringDictResizeFailedError);
    }
    xsArraySetInt(newDct, 0, xsArrayGetInt(dct, 0));
    xsArraySetInt(newDct, 1, newStringsArr);
    for (i = 0; < capacity) {
        string storedKey = _xsStringStringDictGetStoredKey(dct, i);
        if (storedKey != "!<[empty") {
            xsArraySetString(newStringsArr, _xsStringStringDictKeyIndex(i), storedKey);
            xsArraySetString(newStringsArr, _xsStringStringDictValueIndex(i), _xsStringStringDictGetStoredValue(dct, i));
        }
    }
    return (newDct);
}

/*
    Returns a string representation of the dict in the format `{"k1" - "v1", "k2" - "v2", ...}`.
*/
string xsStringStringDictToString(int dct = -1) {
    int capacity = _xsStringStringDictCapacity(dct);
    string s = "{";
    bool first = true;
    for (i = 0; < capacity) {
        string key = _xsStringStringDictGetStoredKey(dct, i);
        if (key != "!<[empty") {
            if (first) {
                first = false;
            } else {
                s = s + ", ";
            }
            s = s + ("\"" + key + "\": \"" + _xsStringStringDictGetStoredValue(dct, i) + "\"");
        }
    }
    s = s + "}";
    return (s);
}

int xsStringStringDictLastError() {
    return (_stringStringDictLastOperationStatus);
}

string _xsStringStringDictFindNextOccupied(int dct = -1, int start = 0, int capacity = 0) {
    int slot = start;
    while (slot < capacity) {
        string storedKey = _xsStringStringDictGetStoredKey(dct, slot);
        if (storedKey != "!<[empty") {
            _stringStringDictLastOperationStatus = cStringStringDictSuccess;
            return (storedKey);
        }
        slot++;
    }
    _stringStringDictLastOperationStatus = cStringStringDictNoKeyError;
    return ("-1");
}

/*
    Returns the next key in the dict for stateless iteration. Sets last error on completion.
    Order is arbitrary.
*/
string xsStringStringDictNextKey(int dct = -1, bool isFirst = true, string prevKey = "!<[empty") {
    int capacity = _xsStringStringDictCapacity(dct);
    if (isFirst) {
        return (_xsStringStringDictFindNextOccupied(dct, 0, capacity));
    }
    int slot = _xsStringStringDictFindSlot(dct, prevKey, capacity);
    if (slot < 0) {
        _stringStringDictLastOperationStatus = cStringStringDictNoKeyError;
        return ("-1");
    }
    int nextStart = slot + 1;
    return (_xsStringStringDictFindNextOccupied(dct, nextStart, capacity));
}

bool xsStringStringDictHasNext(int dct = -1, bool isFirst = true, string prevKey = "!<[empty") {
    int capacity = _xsStringStringDictCapacity(dct);
    int start = 0;
    if (isFirst == false) {
        int slot = _xsStringStringDictFindSlot(dct, prevKey, capacity);
        if (slot < 0) {
            return (false);
        }
        start = slot + 1;
    }
    while (start < capacity) {
        if (_xsStringStringDictGetStoredKey(dct, start) != "!<[empty") {
            return (true);
        }
        start++;
    }
    return (false);
}

/*
    Inserts all key-value pairs from another dict into the source dict, overwriting existing keys.
*/
int xsStringStringDictUpdate(int source = -1, int dct = -1) {
    int capacity = _xsStringStringDictCapacity(dct);
    for (i = 0; < capacity) {
        string key = _xsStringStringDictGetStoredKey(dct, i);
        if (key != "!<[empty") {
            xsStringStringDictPut(source, key, _xsStringStringDictGetStoredValue(dct, i));
            if ((_stringStringDictLastOperationStatus != cStringStringDictSuccess) && (_stringStringDictLastOperationStatus != cStringStringDictNoKeyError)) {
                return (_stringStringDictLastOperationStatus);
            }
        }
    }
    _stringStringDictLastOperationStatus = cStringStringDictSuccess;
    return (cStringStringDictSuccess);
}

/*
    Inserts the key-value pair only if the key is not already present. Sets last error on completion.
    If `key` equals `"!<[empty"`, the call is a no-op and returns
    `"-1"` with last error set to `cStringStringDictGenericError`.
*/
string xsStringStringDictPutIfAbsent(int dct = -1, string key = "", string val = "") {
    if (key == "!<[empty") {
        _stringStringDictLastOperationStatus = cStringStringDictGenericError;
        return ("-1");
    }
    int size = xsArrayGetInt(dct, 0);
    int capacity = _xsStringStringDictCapacity(dct);
    int slot = _xsStringStringDictFindSlot(dct, key, capacity);
    if (slot >= 0) {
        _stringStringDictLastOperationStatus = cStringStringDictSuccess;
        return (_xsStringStringDictGetStoredValue(dct, slot));
    }
    int r = _xsStringStringDictRehashIfNeeded(dct, size, capacity, size + 1);
    if (r != cStringStringDictSuccess) {
        return ("-1");
    }
    capacity = _xsStringStringDictCapacity(dct);
    string result = _xsStringStringDictUpsert(dct, key, val, capacity);
    if (_stringStringDictLastOperationStatus == cStringStringDictNoKeyError) {
        xsArraySetInt(dct, 0, size + 1);
        return ("-1");
    }
    if (_stringStringDictLastOperationStatus != cStringStringDictSuccess) {
        return ("-1");
    }
    return (result);
}

/*
    Returns a new string array containing all keys in the dict. Order is arbitrary.
*/
int xsStringStringDictKeys(int dct = -1, int outArr = -1) {
    int size = xsArrayGetInt(dct, 0);
    int arr = outArr;
    if (arr < 0) {
        arr = xsArrayCreateString(size);
        if (arr < 0) {
            return (cStringStringDictResizeFailedError);
        }
    } else {
        int r = xsArrayResizeString(arr, size);
        if (r != 1) {
            return (cStringStringDictResizeFailedError);
        }
    }
    int capacity = _xsStringStringDictCapacity(dct);
    int idx = 0;
    for (i = 0; < capacity) {
        string storedKey = _xsStringStringDictGetStoredKey(dct, i);
        if (storedKey != "!<[empty") {
            xsArraySetString(arr, idx, storedKey);
            idx++;
        }
    }
    return (arr);
}

/*
    Returns a new string array containing all values in the dict. Order matches `xsStringStringDictKeys`.
*/
int xsStringStringDictValues(int dct = -1, int outArr = -1) {
    int size = xsArrayGetInt(dct, 0);
    int arr = outArr;
    if (arr < 0) {
        arr = xsArrayCreateString(size);
        if (arr < 0) {
            return (cStringStringDictResizeFailedError);
        }
    } else {
        int r = xsArrayResizeString(arr, size);
        if (r != 1) {
            return (cStringStringDictResizeFailedError);
        }
    }
    int capacity = _xsStringStringDictCapacity(dct);
    int idx = 0;
    for (i = 0; < capacity) {
        string storedKey = _xsStringStringDictGetStoredKey(dct, i);
        if (storedKey != "!<[empty") {
            xsArraySetString(arr, idx, _xsStringStringDictGetStoredValue(dct, i));
            idx++;
        }
    }
    return (arr);
}

/*
    Returns true if both dicts contain the same key-value pairs.
*/
bool xsStringStringDictEquals(int a = -1, int b = -1) {
    int sizeA = xsArrayGetInt(a, 0);
    int sizeB = xsArrayGetInt(b, 0);
    if (sizeA != sizeB) {
        return (false);
    }
    int capacity = _xsStringStringDictCapacity(a);
    for (i = 0; < capacity) {
        string key = _xsStringStringDictGetStoredKey(a, i);
        if (key != "!<[empty") {
            string val = _xsStringStringDictGetStoredValue(a, i);
            if (xsStringStringDictGet(b, key) != val) {
                return (false);
            }
            if (xsStringStringDictLastError() != cStringStringDictSuccess) {
                return (false);
            }
        }
    }
    return (true);
}

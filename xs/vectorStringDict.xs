extern const int cVectorStringDictSuccess = 0;
extern const int cVectorStringDictGenericError = -1;
extern const int cVectorStringDictNoKeyError = -2;
extern const int cVectorStringDictResizeFailedError = -3;
extern const int cVectorStringDictMaxCapacityError = -4;
extern const vector cVectorStringDictGenericErrorVector = vector(-1.0, -1.0, -1.0);
extern const int cVectorStringDictMaxCapacity = 999999998;
extern const float cVectorStringDictMaxLoadFactor = 0.75;
extern const vector cVectorStringDictEmptyKey = vector(-9999999.0, -9999999.0, -9999999.0);
extern const int cVectorStringDictInitialCapacity = 50;
extern const int cVectorStringDictHashConstant = 16777619;
int _vectorStringDictLastOperationStatus = cVectorStringDictSuccess;
int _vectorStringDictTempKeys = -1;
int _vectorStringDictTempValues = -1;

void _xsVectorStringDictSetSize(int dct = -1, int size = 0) {
    xsArraySetFloat(dct, 0, bitCastToFloat(size));
}

int _xsVectorStringDictGetSize(int dct = -1) {
    return (bitCastToInt(xsArrayGetFloat(dct, 0)));
}

void _xsVectorStringDictSetValuesArray(int dct = -1, int arr = -1) {
    xsArraySetFloat(dct, 1, bitCastToFloat(arr));
}

int _xsVectorStringDictGetValuesArray(int dct = -1) {
    return (bitCastToInt(xsArrayGetFloat(dct, 1)));
}

int _xsVectorStringDictNumSlots(int capacity = 0) {
    return ((capacity - 2) / 3);
}

int _xsVectorStringDictValueSlot(int slot = 2) {
    return ((slot - 2) / 3);
}

vector _xsVectorStringDictGetStoredKey(int dct = -1, int slot = 2) {
    return (xsVectorSet(xsArrayGetFloat(dct, slot), xsArrayGetFloat(dct, slot + 1), xsArrayGetFloat(dct, slot + 2)));
}

void _xsVectorStringDictSetStoredKey(int dct = -1, int slot = 2, vector key = vector(0.0, 0.0, 0.0)) {
    xsArraySetFloat(dct, slot, xsVectorGetX(key));
    xsArraySetFloat(dct, slot + 1, xsVectorGetY(key));
    xsArraySetFloat(dct, slot + 2, xsVectorGetZ(key));
}

void _xsVectorStringDictClearSlot(int dct = -1, int slot = 2) {
    _xsVectorStringDictSetStoredKey(dct, slot, cVectorStringDictEmptyKey);
}

string _xsVectorStringDictGetStoredValue(int dct = -1, int slot = 2) {
    return (xsArrayGetString(_xsVectorStringDictGetValuesArray(dct), _xsVectorStringDictValueSlot(slot)));
}

void _xsVectorStringDictSetStoredValue(int dct = -1, int slot = 2, string value = "") {
    xsArraySetString(_xsVectorStringDictGetValuesArray(dct), _xsVectorStringDictValueSlot(slot), value);
}

void _xsVectorStringDictSetSlot(int dct = -1, int slot = 2, vector key = vector(0.0, 0.0, 0.0), string value = "") {
    _xsVectorStringDictSetStoredKey(dct, slot, key);
    _xsVectorStringDictSetStoredValue(dct, slot, value);
}

/*
    Creates an empty vector-to-string dictionary.
    Keys equal to `cVectorStringDictEmptyKey` are reserved as the internal empty-slot sentinel
    and cannot be stored. `put` and `putIfAbsent` silently reject them.
    @return created dict id, or `cVectorStringDictGenericError` on error
*/
int xsVectorStringDictCreate() {
    int dct = xsArrayCreateFloat(cVectorStringDictInitialCapacity, xsVectorGetX(cVectorStringDictEmptyKey));
    if (dct < 0) {
        return (cVectorStringDictGenericError);
    }
    int valuesArr = xsArrayCreateString(_xsVectorStringDictNumSlots(cVectorStringDictInitialCapacity));
    if (valuesArr < 0) {
        xsArrayResizeFloat(dct, 0);
        return (cVectorStringDictGenericError);
    }
    int i = 3;
    while (i < cVectorStringDictInitialCapacity) {
        xsArraySetFloat(dct, i, xsVectorGetY(cVectorStringDictEmptyKey));
        xsArraySetFloat(dct, i + 1, xsVectorGetZ(cVectorStringDictEmptyKey));
        i = i + 3;
    }
    _xsVectorStringDictSetSize(dct, 0);
    _xsVectorStringDictSetValuesArray(dct, valuesArr);
    return (dct);
}

int _xsVectorStringDictHash(vector key = vector(0.0, 0.0, 0.0), int capacity = 0) {
    int hash = bitCastToInt(xsVectorGetX(key)) * cVectorStringDictHashConstant;
    hash = (hash + bitCastToInt(xsVectorGetY(key))) * cVectorStringDictHashConstant;
    hash = (hash + bitCastToInt(xsVectorGetZ(key))) * cVectorStringDictHashConstant;
    int numSlots = _xsVectorStringDictNumSlots(capacity);
    hash = hash % numSlots;
    if (hash < 0) {
        hash = hash + numSlots;
    }
    return ((hash * 3) + 2);
}

int _xsVectorStringDictFindSlot(int dct = -1, vector key = vector(0.0, 0.0, 0.0), int capacity = 0) {
    int numSlots = _xsVectorStringDictNumSlots(capacity);
    int home = _xsVectorStringDictHash(key, capacity);
    int slot = home;
    int steps = 0;
    while (steps < numSlots) {
        vector storedKey = _xsVectorStringDictGetStoredKey(dct, slot);
        if (storedKey == cVectorStringDictEmptyKey) {
            return (-1);
        }
        if (storedKey == key) {
            return (slot);
        }
        slot = slot + 3;
        if (slot >= capacity) {
            slot = 2;
        }
        steps++;
    }
    return (-1);
}

string _xsVectorStringDictUpsert(int dct = -1, vector key = vector(0.0, 0.0, 0.0), string val = "", int capacity = 0) {
    int numSlots = _xsVectorStringDictNumSlots(capacity);
    int home = _xsVectorStringDictHash(key, capacity);
    int slot = home;
    int steps = 0;
    while (steps < numSlots) {
        vector storedKey = _xsVectorStringDictGetStoredKey(dct, slot);
        if (storedKey == cVectorStringDictEmptyKey) {
            _xsVectorStringDictSetSlot(dct, slot, key, val);
            _vectorStringDictLastOperationStatus = cVectorStringDictNoKeyError;
            return ("-1");
        }
        if (storedKey == key) {
            string oldVal = _xsVectorStringDictGetStoredValue(dct, slot);
            _xsVectorStringDictSetStoredValue(dct, slot, val);
            _vectorStringDictLastOperationStatus = cVectorStringDictSuccess;
            return (oldVal);
        }
        slot = slot + 3;
        if (slot >= capacity) {
            slot = 2;
        }
        steps++;
    }
    _vectorStringDictLastOperationStatus = cVectorStringDictMaxCapacityError;
    return ("-1");
}

int _xsVectorStringDictMoveToTempArrays(int dct = -1, int size = 0, int capacity = 0) {
    int tempDataSize = size * 3;
    int maxValuesCapacity = _xsVectorStringDictNumSlots(cVectorStringDictMaxCapacity);
    if (_vectorStringDictTempKeys < 0) {
        _vectorStringDictTempKeys = xsArrayCreateFloat(tempDataSize, xsVectorGetX(cVectorStringDictEmptyKey));
        if (_vectorStringDictTempKeys < 0) {
            return (cVectorStringDictResizeFailedError);
        }
    } else {
        int tempKeysCapacity = xsArrayGetSize(_vectorStringDictTempKeys);
        if (tempKeysCapacity < tempDataSize) {
            if ((tempDataSize / 3) > maxValuesCapacity) {
                return (cVectorStringDictMaxCapacityError);
            }
            int rKeys = xsArrayResizeFloat(_vectorStringDictTempKeys, tempDataSize);
            if (rKeys != 1) {
                return (cVectorStringDictResizeFailedError);
            }
        }
    }
    int i = 1;
    while (i < tempDataSize) {
        xsArraySetFloat(_vectorStringDictTempKeys, i, xsVectorGetY(cVectorStringDictEmptyKey));
        xsArraySetFloat(_vectorStringDictTempKeys, i + 1, xsVectorGetZ(cVectorStringDictEmptyKey));
        i = i + 3;
    }
    if (_vectorStringDictTempValues < 0) {
        _vectorStringDictTempValues = xsArrayCreateString(size);
        if (_vectorStringDictTempValues < 0) {
            return (cVectorStringDictResizeFailedError);
        }
    } else {
        int tempValuesCapacity = xsArrayGetSize(_vectorStringDictTempValues);
        if (tempValuesCapacity < size) {
            if (size > maxValuesCapacity) {
                return (cVectorStringDictMaxCapacityError);
            }
            int rValues = xsArrayResizeString(_vectorStringDictTempValues, size);
            if (rValues != 1) {
                return (cVectorStringDictResizeFailedError);
            }
        }
    }
    int t = 0;
    int slotIdx = 2;
    while (slotIdx < capacity) {
        vector storedKey = _xsVectorStringDictGetStoredKey(dct, slotIdx);
        if (storedKey != cVectorStringDictEmptyKey) {
            xsArraySetFloat(_vectorStringDictTempKeys, t, xsArrayGetFloat(dct, slotIdx));
            xsArraySetFloat(_vectorStringDictTempKeys, t + 1, xsArrayGetFloat(dct, slotIdx + 1));
            xsArraySetFloat(_vectorStringDictTempKeys, t + 2, xsArrayGetFloat(dct, slotIdx + 2));
            xsArraySetString(_vectorStringDictTempValues, t / 3, _xsVectorStringDictGetStoredValue(dct, slotIdx));
            t = t + 3;
        }
        slotIdx = slotIdx + 3;
    }
    return (tempDataSize);
}

void _xsVectorStringDictClearSlots(int dct = -1, int capacity = -1) {
    int j = 2;
    while (j < capacity) {
        _xsVectorStringDictClearSlot(dct, j);
        j = j + 3;
    }
}

int _xsVectorStringDictRehashIfNeeded(int dct = -1, int size = 0, int capacity = 0, int requiredSize = -1) {
    if (requiredSize < 0) {
        requiredSize = size;
    }
    float loadFactor = (0.0 + requiredSize) / _xsVectorStringDictNumSlots(capacity);
    if (loadFactor > cVectorStringDictMaxLoadFactor) {
        int storeStatus = _vectorStringDictLastOperationStatus;
        int newValuesCapacity = _xsVectorStringDictNumSlots(capacity) * 2;
        int newCapacity = (newValuesCapacity * 3) + 2;
        if (newCapacity > cVectorStringDictMaxCapacity) {
            _vectorStringDictLastOperationStatus = cVectorStringDictMaxCapacityError;
            return (cVectorStringDictGenericError);
        }
        int tempDataSize = _xsVectorStringDictMoveToTempArrays(dct, size, capacity);
        if (tempDataSize < 0) {
            _vectorStringDictLastOperationStatus = tempDataSize;
            return (cVectorStringDictGenericError);
        }
        int valuesArr = _xsVectorStringDictGetValuesArray(dct);
        int rValues = xsArrayResizeString(valuesArr, newValuesCapacity);
        if (rValues != 1) {
            _vectorStringDictLastOperationStatus = cVectorStringDictResizeFailedError;
            return (cVectorStringDictGenericError);
        }
        int r = xsArrayResizeFloat(dct, newCapacity);
        if (r != 1) {
            _vectorStringDictLastOperationStatus = cVectorStringDictResizeFailedError;
            return (cVectorStringDictGenericError);
        }
        _xsVectorStringDictClearSlots(dct, newCapacity);
        int t = 0;
        while (t < tempDataSize) {
            _xsVectorStringDictUpsert(dct, xsVectorSet(xsArrayGetFloat(_vectorStringDictTempKeys, t), xsArrayGetFloat(_vectorStringDictTempKeys, t + 1), xsArrayGetFloat(_vectorStringDictTempKeys, t + 2)), xsArrayGetString(_vectorStringDictTempValues, t / 3), newCapacity);
            if ((_vectorStringDictLastOperationStatus < 0) && (_vectorStringDictLastOperationStatus != cVectorStringDictNoKeyError)) {
                return (cVectorStringDictGenericError);
            }
            t = t + 3;
        }
        _vectorStringDictLastOperationStatus = storeStatus;
    }
    return (cVectorStringDictSuccess);
}

/*
    Inserts or updates a key-value pair. Triggers a rehash when load factor exceeds the threshold.
    If `key` equals `cVectorStringDictEmptyKey`, the call is a no-op and returns
    `"-1"` with last error set to `cVectorStringDictGenericError`.
*/
string xsVectorStringDictPut(int dct = -1, vector key = vector(0.0, 0.0, 0.0), string val = "") {
    if (key == cVectorStringDictEmptyKey) {
        _vectorStringDictLastOperationStatus = cVectorStringDictGenericError;
        return ("-1");
    }
    int size = _xsVectorStringDictGetSize(dct);
    int capacity = xsArrayGetSize(dct);
    int slot = _xsVectorStringDictFindSlot(dct, key, capacity);
    if (slot >= 0) {
        string oldVal = _xsVectorStringDictGetStoredValue(dct, slot);
        _xsVectorStringDictSetStoredValue(dct, slot, val);
        _vectorStringDictLastOperationStatus = cVectorStringDictSuccess;
        return (oldVal);
    }
    int r = _xsVectorStringDictRehashIfNeeded(dct, size, capacity, size + 1);
    if (r != cVectorStringDictSuccess) {
        return ("-1");
    }
    capacity = xsArrayGetSize(dct);
    string previousValue = _xsVectorStringDictUpsert(dct, key, val, capacity);
    if (_vectorStringDictLastOperationStatus == cVectorStringDictNoKeyError) {
        _xsVectorStringDictSetSize(dct, size + 1);
        return ("-1");
    }
    if (_vectorStringDictLastOperationStatus != cVectorStringDictSuccess) {
        return ("-1");
    }
    return (previousValue);
}

/*
    Creates a dict with provided key-value pairs. The first key that equals
    `cVectorStringDictEmptyKey` will stop further insertion.
*/
int xsVectorStringDict(vector k1 = cVectorStringDictEmptyKey, string v1 = "", vector k2 = cVectorStringDictEmptyKey, string v2 = "", vector k3 = cVectorStringDictEmptyKey, string v3 = "", vector k4 = cVectorStringDictEmptyKey, string v4 = "", vector k5 = cVectorStringDictEmptyKey, string v5 = "", vector k6 = cVectorStringDictEmptyKey, string v6 = "") {
    int dct = xsVectorStringDictCreate();
    if (dct < 0) {
        return (cVectorStringDictGenericError);
    }
    if (k1 == cVectorStringDictEmptyKey) {
        return (dct);
    }
    xsVectorStringDictPut(dct, k1, v1);
    if (k2 == cVectorStringDictEmptyKey) {
        return (dct);
    }
    xsVectorStringDictPut(dct, k2, v2);
    if (k3 == cVectorStringDictEmptyKey) {
        return (dct);
    }
    xsVectorStringDictPut(dct, k3, v3);
    if (k4 == cVectorStringDictEmptyKey) {
        return (dct);
    }
    xsVectorStringDictPut(dct, k4, v4);
    if (k5 == cVectorStringDictEmptyKey) {
        return (dct);
    }
    xsVectorStringDictPut(dct, k5, v5);
    if (k6 == cVectorStringDictEmptyKey) {
        return (dct);
    }
    xsVectorStringDictPut(dct, k6, v6);
    return (dct);
}

/*
    Returns the value associated with the given key. Sets last error on completion.
*/
string xsVectorStringDictGet(int dct = -1, vector key = vector(0.0, 0.0, 0.0), string dft = "-1") {
    int capacity = xsArrayGetSize(dct);
    int slot = _xsVectorStringDictFindSlot(dct, key, capacity);
    if (slot >= 0) {
        _vectorStringDictLastOperationStatus = cVectorStringDictSuccess;
        return (_xsVectorStringDictGetStoredValue(dct, slot));
    }
    _vectorStringDictLastOperationStatus = cVectorStringDictNoKeyError;
    return (dft);
}

/*
    Removes the entry with the given key from the dict. Uses backward shift deletion to
    maintain linear probing invariant.
*/
string xsVectorStringDictRemove(int dct = -1, vector key = vector(0.0, 0.0, 0.0)) {
    int size = _xsVectorStringDictGetSize(dct);
    int capacity = xsArrayGetSize(dct);
    int numSlots = _xsVectorStringDictNumSlots(capacity);
    int slot = _xsVectorStringDictFindSlot(dct, key, capacity);
    if (slot < 0) {
        _vectorStringDictLastOperationStatus = cVectorStringDictNoKeyError;
        return ("-1");
    }
    string foundVal = _xsVectorStringDictGetStoredValue(dct, slot);
    int g = slot;
    int q = g + 3;
    if (q >= capacity) {
        q = 2;
    }
    int shiftSteps = 0;
    vector qKey = _xsVectorStringDictGetStoredKey(dct, q);
    while ((qKey != cVectorStringDictEmptyKey) && (shiftSteps < numSlots)) {
        int qHome = _xsVectorStringDictHash(qKey, capacity);
        int gSlot = (g - 2) / 3;
        int qSlot = (q - 2) / 3;
        int hSlot = (qHome - 2) / 3;
        int distG = ((gSlot - hSlot) + numSlots) % numSlots;
        int distQ = ((qSlot - hSlot) + numSlots) % numSlots;
        if (distG < distQ) {
            xsArraySetFloat(dct, g, xsArrayGetFloat(dct, q));
            xsArraySetFloat(dct, g + 1, xsArrayGetFloat(dct, q + 1));
            xsArraySetFloat(dct, g + 2, xsArrayGetFloat(dct, q + 2));
            _xsVectorStringDictSetStoredValue(dct, g, _xsVectorStringDictGetStoredValue(dct, q));
            g = q;
        }
        q = q + 3;
        if (q >= capacity) {
            q = 2;
        }
        shiftSteps++;
        qKey = _xsVectorStringDictGetStoredKey(dct, q);
    }
    _xsVectorStringDictClearSlot(dct, g);
    _xsVectorStringDictSetSize(dct, size - 1);
    _vectorStringDictLastOperationStatus = cVectorStringDictSuccess;
    return (foundVal);
}

bool xsVectorStringDictContains(int dct = -1, vector key = vector(0.0, 0.0, 0.0)) {
    int capacity = xsArrayGetSize(dct);
    return (_xsVectorStringDictFindSlot(dct, key, capacity) >= 0);
}

int xsVectorStringDictSize(int dct = -1) {
    return (_xsVectorStringDictGetSize(dct));
}

/*
    Removes all entries from the dict and shrinks the backing arrays.
*/
int xsVectorStringDictClear(int dct = -1) {
    int capacity = xsArrayGetSize(dct);
    int valuesArr = _xsVectorStringDictGetValuesArray(dct);
    _xsVectorStringDictClearSlots(dct, capacity);
    _xsVectorStringDictSetSize(dct, 0);
    if (capacity > cVectorStringDictInitialCapacity) {
        int r = xsArrayResizeFloat(dct, cVectorStringDictInitialCapacity);
        if (r != 1) {
            return (cVectorStringDictGenericError);
        }
        int rValues = xsArrayResizeString(valuesArr, _xsVectorStringDictNumSlots(cVectorStringDictInitialCapacity));
        if (rValues != 1) {
            return (cVectorStringDictGenericError);
        }
    }
    return (cVectorStringDictSuccess);
}

/*
    Returns a deep copy of the dict.
*/
int xsVectorStringDictCopy(int dct = -1) {
    int capacity = xsArrayGetSize(dct);
    int valuesCapacity = _xsVectorStringDictNumSlots(capacity);
    int newDct = xsArrayCreateFloat(capacity, xsVectorGetX(cVectorStringDictEmptyKey));
    if (newDct < 0) {
        return (cVectorStringDictResizeFailedError);
    }
    int newValuesArr = xsArrayCreateString(valuesCapacity);
    if (newValuesArr < 0) {
        xsArrayResizeFloat(newDct, 0);
        return (cVectorStringDictResizeFailedError);
    }
    int i = 3;
    while (i < capacity) {
        xsArraySetFloat(newDct, i, xsVectorGetY(cVectorStringDictEmptyKey));
        xsArraySetFloat(newDct, i + 1, xsVectorGetZ(cVectorStringDictEmptyKey));
        i = i + 3;
    }
    _xsVectorStringDictSetSize(newDct, _xsVectorStringDictGetSize(dct));
    _xsVectorStringDictSetValuesArray(newDct, newValuesArr);
    int slotIdx = 2;
    while (slotIdx < capacity) {
        vector storedKey = _xsVectorStringDictGetStoredKey(dct, slotIdx);
        if (storedKey != cVectorStringDictEmptyKey) {
            xsArraySetFloat(newDct, slotIdx, xsArrayGetFloat(dct, slotIdx));
            xsArraySetFloat(newDct, slotIdx + 1, xsArrayGetFloat(dct, slotIdx + 1));
            xsArraySetFloat(newDct, slotIdx + 2, xsArrayGetFloat(dct, slotIdx + 2));
            xsArraySetString(newValuesArr, _xsVectorStringDictValueSlot(slotIdx), _xsVectorStringDictGetStoredValue(dct, slotIdx));
        }
        slotIdx = slotIdx + 3;
    }
    return (newDct);
}

/*
    Returns a string representation of the dict in the format `{(x1, y1, z1) - "v1", ...}`.
*/
string xsVectorStringDictToString(int dct = -1) {
    int capacity = xsArrayGetSize(dct);
    string s = "{";
    bool first = true;
    int i = 2;
    while (i < capacity) {
        vector key = _xsVectorStringDictGetStoredKey(dct, i);
        if (key != cVectorStringDictEmptyKey) {
            if (first) {
                first = false;
            } else {
                s = s + ", ";
            }
            s = s + (key + ": \"" + _xsVectorStringDictGetStoredValue(dct, i) + "\"");
        }
        i = i + 3;
    }
    s = s + "}";
    return (s);
}

int xsVectorStringDictLastError() {
    return (_vectorStringDictLastOperationStatus);
}

vector _xsVectorStringDictFindNextOccupied(int dct = -1, int start = 2, int capacity = 0) {
    int slot = start;
    while (slot < capacity) {
        vector storedKey = _xsVectorStringDictGetStoredKey(dct, slot);
        if (storedKey != cVectorStringDictEmptyKey) {
            _vectorStringDictLastOperationStatus = cVectorStringDictSuccess;
            return (storedKey);
        }
        slot = slot + 3;
    }
    _vectorStringDictLastOperationStatus = cVectorStringDictNoKeyError;
    return (cVectorStringDictGenericErrorVector);
}

/*
    Returns the next key in the dict for stateless iteration. Sets last error on completion.
*/
vector xsVectorStringDictNextKey(int dct = -1, bool isFirst = true, vector prevKey = cVectorStringDictEmptyKey) {
    int capacity = xsArrayGetSize(dct);
    if (isFirst) {
        return (_xsVectorStringDictFindNextOccupied(dct, 2, capacity));
    }
    int slot = _xsVectorStringDictFindSlot(dct, prevKey, capacity);
    if (slot < 0) {
        _vectorStringDictLastOperationStatus = cVectorStringDictNoKeyError;
        return (cVectorStringDictGenericErrorVector);
    }
    int nextStart = slot + 3;
    return (_xsVectorStringDictFindNextOccupied(dct, nextStart, capacity));
}

bool xsVectorStringDictHasNext(int dct = -1, bool isFirst = true, vector prevKey = cVectorStringDictEmptyKey) {
    int capacity = xsArrayGetSize(dct);
    int start = 2;
    if (isFirst == false) {
        int slot = _xsVectorStringDictFindSlot(dct, prevKey, capacity);
        if (slot < 0) {
            return (false);
        }
        start = slot + 3;
    }
    while (start < capacity) {
        if (_xsVectorStringDictGetStoredKey(dct, start) != cVectorStringDictEmptyKey) {
            return (true);
        }
        start = start + 3;
    }
    return (false);
}

/*
    Inserts all key-value pairs from another dict into the source dict, overwriting existing keys.
*/
int xsVectorStringDictUpdate(int source = -1, int dct = -1) {
    int capacity = xsArrayGetSize(dct);
    int i = 2;
    while (i < capacity) {
        vector key = _xsVectorStringDictGetStoredKey(dct, i);
        if (key != cVectorStringDictEmptyKey) {
            xsVectorStringDictPut(source, key, _xsVectorStringDictGetStoredValue(dct, i));
            if ((_vectorStringDictLastOperationStatus != cVectorStringDictSuccess) && (_vectorStringDictLastOperationStatus != cVectorStringDictNoKeyError)) {
                return (_vectorStringDictLastOperationStatus);
            }
        }
        i = i + 3;
    }
    _vectorStringDictLastOperationStatus = cVectorStringDictSuccess;
    return (cVectorStringDictSuccess);
}

/*
    Inserts the key-value pair only if the key is not already present. Sets last error on completion.
*/
string xsVectorStringDictPutIfAbsent(int dct = -1, vector key = vector(0.0, 0.0, 0.0), string val = "") {
    if (key == cVectorStringDictEmptyKey) {
        _vectorStringDictLastOperationStatus = cVectorStringDictGenericError;
        return ("-1");
    }
    int size = _xsVectorStringDictGetSize(dct);
    int capacity = xsArrayGetSize(dct);
    int slot = _xsVectorStringDictFindSlot(dct, key, capacity);
    if (slot >= 0) {
        _vectorStringDictLastOperationStatus = cVectorStringDictSuccess;
        return (_xsVectorStringDictGetStoredValue(dct, slot));
    }
    int r = _xsVectorStringDictRehashIfNeeded(dct, size, capacity, size + 1);
    if (r != cVectorStringDictSuccess) {
        return ("-1");
    }
    capacity = xsArrayGetSize(dct);
    string result = _xsVectorStringDictUpsert(dct, key, val, capacity);
    if (_vectorStringDictLastOperationStatus == cVectorStringDictNoKeyError) {
        _xsVectorStringDictSetSize(dct, size + 1);
        return ("-1");
    }
    if (_vectorStringDictLastOperationStatus != cVectorStringDictSuccess) {
        return ("-1");
    }
    return (result);
}

/*
    Returns a new vector array containing all keys in the dict. Order is arbitrary.
*/
int xsVectorStringDictKeys(int dct = -1) {
    int size = _xsVectorStringDictGetSize(dct);
    int arr = xsArrayCreateVector(size, vector(0.0, 0.0, 0.0));
    if (arr < 0) {
        return (cVectorStringDictResizeFailedError);
    }
    int capacity = xsArrayGetSize(dct);
    int idx = 0;
    int i = 2;
    while (i < capacity) {
        vector storedKey = _xsVectorStringDictGetStoredKey(dct, i);
        if (storedKey != cVectorStringDictEmptyKey) {
            xsArraySetVector(arr, idx, storedKey);
            idx++;
        }
        i = i + 3;
    }
    return (arr);
}

/*
    Returns a new string array containing all values in the dict. Order matches
    `xsVectorStringDictKeys`.
*/
int xsVectorStringDictValues(int dct = -1) {
    int size = _xsVectorStringDictGetSize(dct);
    int arr = xsArrayCreateString(size);
    if (arr < 0) {
        return (cVectorStringDictResizeFailedError);
    }
    int capacity = xsArrayGetSize(dct);
    int idx = 0;
    int i = 2;
    while (i < capacity) {
        vector storedKey = _xsVectorStringDictGetStoredKey(dct, i);
        if (storedKey != cVectorStringDictEmptyKey) {
            xsArraySetString(arr, idx, _xsVectorStringDictGetStoredValue(dct, i));
            idx++;
        }
        i = i + 3;
    }
    return (arr);
}

/*
    Returns true if both dicts contain the same key-value pairs.
*/
bool xsVectorStringDictEquals(int a = -1, int b = -1) {
    int sizeA = _xsVectorStringDictGetSize(a);
    int sizeB = _xsVectorStringDictGetSize(b);
    if (sizeA != sizeB) {
        return (false);
    }
    int capacity = xsArrayGetSize(a);
    int i = 2;
    while (i < capacity) {
        vector key = _xsVectorStringDictGetStoredKey(a, i);
        if (key != cVectorStringDictEmptyKey) {
            string val = _xsVectorStringDictGetStoredValue(a, i);
            if (xsVectorStringDictGet(b, key) != val) {
                return (false);
            }
            if (xsVectorStringDictLastError() != cVectorStringDictSuccess) {
                return (false);
            }
        }
        i = i + 3;
    }
    return (true);
}

extern const int cIntIntDictSuccess = 0;
extern const int cIntIntDictGenericError = -1;
extern const int cIntIntDictNoKeyError = -2;
extern const int cIntIntDictResizeFailedError = -3;
extern const int cIntIntDictMaxCapacityError = -4;
extern const int cIntIntDictMaxCapacity = 999999999;
extern const float cIntIntDictMaxLoadFactor = 0.75;
extern const int cIntIntDictEmptyKey = -999999999;
extern const int cIntIntDictInitialCapacity = 33;
extern const int cIntIntDictHashConstant = 16777619;
int _intIntDictLastOperationStatus = cIntIntDictSuccess;
int _intIntDictTempArray = -1;

/*
    Creates an empty int-to-int dictionary.
    Keys equal to `cIntIntDictEmptyKey` (-999999999) are reserved as the internal empty-slot
    sentinel and cannot be stored. `put` and `putIfAbsent` silently reject them.
    @return created dict id, or `cIntIntDictGenericError` on error
*/
int xsIntIntDictCreate() {
    int dct = xsArrayCreateInt(cIntIntDictInitialCapacity, cIntIntDictEmptyKey);
    xsArraySetInt(dct, 0, 0);
    return (dct);
}

int _xsIntIntDictHash(int key = -1, int capacity = 0) {
    int h = key * cIntIntDictHashConstant;
    int numSlots = (capacity - 1) / 2;
    h = h % numSlots;
    if (h < 0) {
        h = h + numSlots;
    }
    return ((h * 2) + 1);
}

/*
    Returns array index of slot containing key, or -1 if not found.
*/
int _xsIntIntDictFindSlot(int dct = -1, int key = -1, int capacity = 0) {
    int numSlots = (capacity - 1) / 2;
    int home = _xsIntIntDictHash(key, capacity);
    int slot = home;
    int steps = 0;
    while (steps < numSlots) {
        int storedKey = xsArrayGetInt(dct, slot);
        if (storedKey == cIntIntDictEmptyKey) {
            return (-1);
        }
        if (storedKey == key) {
            return (slot);
        }
        slot = slot + 2;
        if (slot >= capacity) {
            slot = 1;
        }
        steps++;
    }
    return (-1);
}

int _xsIntIntDictUpsert(int dct = -1, int key = -1, int val = 0, int capacity = 0) {
    int numSlots = (capacity - 1) / 2;
    int home = _xsIntIntDictHash(key, capacity);
    int slot = home;
    int steps = 0;
    while (steps < numSlots) {
        int storedKey = xsArrayGetInt(dct, slot);
        if (storedKey == cIntIntDictEmptyKey) {
            xsArraySetInt(dct, slot, key);
            xsArraySetInt(dct, slot + 1, val);
            _intIntDictLastOperationStatus = cIntIntDictNoKeyError;
            return (cIntIntDictGenericError);
        }
        if (storedKey == key) {
            int oldVal = xsArrayGetInt(dct, slot + 1);
            xsArraySetInt(dct, slot + 1, val);
            _intIntDictLastOperationStatus = cIntIntDictSuccess;
            return (oldVal);
        }
        slot = slot + 2;
        if (slot >= capacity) {
            slot = 1;
        }
        steps++;
    }
    _intIntDictLastOperationStatus = cIntIntDictMaxCapacityError;
    return (cIntIntDictGenericError);
}

int _xsIntIntDictMoveToTempArray(int dct = -1, int size = 0, int capacity = 0) {
    int tempDataSize = size * 2;
    if (_intIntDictTempArray < 0) {
        _intIntDictTempArray = xsArrayCreateInt(tempDataSize, cIntIntDictEmptyKey);
        if (_intIntDictTempArray < 0) {
            return (cIntIntDictResizeFailedError);
        }
    } else {
        int tempArrCapacity = xsArrayGetSize(_intIntDictTempArray);
        if (tempArrCapacity < tempDataSize) {
            if (tempDataSize > cIntIntDictMaxCapacity) {
                return (cIntIntDictMaxCapacityError);
            }
            int r = xsArrayResizeInt(_intIntDictTempArray, tempDataSize);
            if (r != 1) {
                return (cIntIntDictResizeFailedError);
            }
        }
    }
    int t = 0;
    int i = 1;
    while (i < capacity) {
        int storedKey = xsArrayGetInt(dct, i);
        if (storedKey != cIntIntDictEmptyKey) {
            xsArraySetInt(_intIntDictTempArray, t, storedKey);
            xsArraySetInt(_intIntDictTempArray, t + 1, xsArrayGetInt(dct, i + 1));
            t = t + 2;
        }
        i = i + 2;
    }
    return (tempDataSize);
}

void _xsIntIntDictClearSlots(int dct = -1, int capacity = -1) {
    int j = 1;
    while (j < capacity) {
        xsArraySetInt(dct, j, cIntIntDictEmptyKey);
        j = j + 2;
    }
}

int _xsIntIntDictRehashIfNeeded(int dct = -1, int size = 0, int capacity = 0, int requiredSize = -1) {
    if (requiredSize < 0) {
        requiredSize = size;
    }
    float loadFactor = (0.0 + requiredSize) / ((capacity - 1) / 2);
    if (loadFactor > cIntIntDictMaxLoadFactor) {
        int storeStatus = _intIntDictLastOperationStatus;
        int newCapacity = ((capacity - 1) * 2) + 1;
        if (newCapacity > cIntIntDictMaxCapacity) {
            _intIntDictLastOperationStatus = cIntIntDictMaxCapacityError;
            return (cIntIntDictGenericError);
        }
        int tempDataSize = _xsIntIntDictMoveToTempArray(dct, size, capacity);
        if (tempDataSize < 0) {
            _intIntDictLastOperationStatus = tempDataSize;
            return (cIntIntDictGenericError);
        }
        int r = xsArrayResizeInt(dct, newCapacity);
        if (r != 1) {
            _intIntDictLastOperationStatus = cIntIntDictResizeFailedError;
            return (cIntIntDictGenericError);
        }
        _xsIntIntDictClearSlots(dct, newCapacity);
        int t = 0;
        while (t < tempDataSize) {
            _xsIntIntDictUpsert(dct, xsArrayGetInt(_intIntDictTempArray, t), xsArrayGetInt(_intIntDictTempArray, t + 1), newCapacity);
            if ((_intIntDictLastOperationStatus < 0) && (_intIntDictLastOperationStatus != cIntIntDictNoKeyError)) {
                return (cIntIntDictGenericError);
            }
            t = t + 2;
        }
        _intIntDictLastOperationStatus = storeStatus;
    }
    return (cIntIntDictSuccess);
}

/*
    Inserts or updates a key-value pair. Triggers a rehash when load factor exceeds the threshold. Sets last error on completion.
    If `key` equals `cIntIntDictEmptyKey`, the call is a no-op and returns `cIntIntDictGenericError`
    with last error set to `cIntIntDictGenericError`.
    @param dct - dict id
    @param key - key to insert or update (must not equal `cIntIntDictEmptyKey`)
    @param val - value to associate with the key
    @return previous value if the key already existed, or `cIntIntDictGenericError` if newly inserted or on error.
        Because -1 is both the error sentinel and a valid previous value, callers must check
        `xs_int_int_dict_last_error()` to distinguish - `cIntIntDictSuccess` means the key
        existed and the returned value is valid; `cIntIntDictNoKeyError` means a new key
        was inserted; any other negative status indicates an error.
*/
int xsIntIntDictPut(int dct = -1, int key = -1, int val = 0) {
    if (key == cIntIntDictEmptyKey) {
        _intIntDictLastOperationStatus = cIntIntDictGenericError;
        return (cIntIntDictGenericError);
    }
    int size = xsArrayGetInt(dct, 0);
    int capacity = xsArrayGetSize(dct);
    int slot = _xsIntIntDictFindSlot(dct, key, capacity);
    if (slot >= 0) {
        int oldVal = xsArrayGetInt(dct, slot + 1);
        xsArraySetInt(dct, slot + 1, val);
        _intIntDictLastOperationStatus = cIntIntDictSuccess;
        return (oldVal);
    }
    int r = _xsIntIntDictRehashIfNeeded(dct, size, capacity, size + 1);
    if (r != cIntIntDictSuccess) {
        return (cIntIntDictGenericError);
    }
    capacity = xsArrayGetSize(dct);
    int previousValue = _xsIntIntDictUpsert(dct, key, val, capacity);
    if (_intIntDictLastOperationStatus == cIntIntDictNoKeyError) {
        xsArraySetInt(dct, 0, size + 1);
        return (cIntIntDictGenericError);
    }
    if (_intIntDictLastOperationStatus != cIntIntDictSuccess) {
        return (cIntIntDictGenericError);
    }
    return (previousValue);
}

/*
    Creates a dict with provided key-value pairs. The first key that equals `cIntIntDictEmptyKey` will stop further insertion.
    This function can create a dict with 6 entries at the maximum, but further entries can be added with `xsIntIntDictPut`.
    @param k1 through k6 - key at a given position (must not equal `cIntIntDictEmptyKey`)
    @param v1 through v6 - value associated with the corresponding key
    @return created dict id, or `cIntIntDictGenericError` on error
*/
int xsIntIntDict(int k1 = cIntIntDictEmptyKey, int v1 = 0, int k2 = cIntIntDictEmptyKey, int v2 = 0, int k3 = cIntIntDictEmptyKey, int v3 = 0, int k4 = cIntIntDictEmptyKey, int v4 = 0, int k5 = cIntIntDictEmptyKey, int v5 = 0, int k6 = cIntIntDictEmptyKey, int v6 = 0) {
    int dct = xsIntIntDictCreate();
    if (dct < 0) {
        return (cIntIntDictGenericError);
    }
    if (k1 == cIntIntDictEmptyKey) {
        return (dct);
    }
    xsIntIntDictPut(dct, k1, v1);
    if (k2 == cIntIntDictEmptyKey) {
        return (dct);
    }
    xsIntIntDictPut(dct, k2, v2);
    if (k3 == cIntIntDictEmptyKey) {
        return (dct);
    }
    xsIntIntDictPut(dct, k3, v3);
    if (k4 == cIntIntDictEmptyKey) {
        return (dct);
    }
    xsIntIntDictPut(dct, k4, v4);
    if (k5 == cIntIntDictEmptyKey) {
        return (dct);
    }
    xsIntIntDictPut(dct, k5, v5);
    if (k6 == cIntIntDictEmptyKey) {
        return (dct);
    }
    xsIntIntDictPut(dct, k6, v6);
    return (dct);
}

/*
    Returns the value associated with the given key. Sets last error on completion.
    @param dct - dict id
    @param key - key to look up
    @param dft - default value returned if the key is not found
    @return value for the key, or `dft` if not found
*/
int xsIntIntDictGet(int dct = -1, int key = -1, int dft = -1) {
    int capacity = xsArrayGetSize(dct);
    int slot = _xsIntIntDictFindSlot(dct, key, capacity);
    if (slot >= 0) {
        _intIntDictLastOperationStatus = cIntIntDictSuccess;
        return (xsArrayGetInt(dct, slot + 1));
    }
    _intIntDictLastOperationStatus = cIntIntDictNoKeyError;
    return (dft);
}

/*
    Removes the entry with the given key from the dict. Sets last error on completion.
    Uses backward shift deletion to maintain linear probing invariant (no tombstones).
    @param dct - dict id
    @param key - key to remove
    @return value that was associated with the key, or `cIntIntDictGenericError` if not found
*/
int xsIntIntDictRemove(int dct = -1, int key = -1) {
    int size = xsArrayGetInt(dct, 0);
    int capacity = xsArrayGetSize(dct);
    int numSlots = (capacity - 1) / 2;
    int slot = _xsIntIntDictFindSlot(dct, key, capacity);
    if (slot < 0) {
        _intIntDictLastOperationStatus = cIntIntDictNoKeyError;
        return (cIntIntDictGenericError);
    }
    int foundVal = xsArrayGetInt(dct, slot + 1);
    int g = slot;
    int q = g + 2;
    if (q >= capacity) {
        q = 1;
    }
    int shiftSteps = 0;
    int qKey = xsArrayGetInt(dct, q);
    while ((qKey != cIntIntDictEmptyKey) && (shiftSteps < numSlots)) {
        int qHome = _xsIntIntDictHash(qKey, capacity);
        int gSlot = (g - 1) / 2;
        int qSlot = (q - 1) / 2;
        int hSlot = (qHome - 1) / 2;
        int distG = ((gSlot - hSlot) + numSlots) % numSlots;
        int distQ = ((qSlot - hSlot) + numSlots) % numSlots;
        if (distG < distQ) {
            xsArraySetInt(dct, g, qKey);
            xsArraySetInt(dct, g + 1, xsArrayGetInt(dct, q + 1));
            g = q;
        }
        q = q + 2;
        if (q >= capacity) {
            q = 1;
        }
        shiftSteps++;
        qKey = xsArrayGetInt(dct, q);
    }
    xsArraySetInt(dct, g, cIntIntDictEmptyKey);
    xsArraySetInt(dct, 0, size - 1);
    _intIntDictLastOperationStatus = cIntIntDictSuccess;
    return (foundVal);
}

/*
    Checks whether the dict contains the given key.
    @param dct - dict id
    @param key - key to search for
    @return true if the key is found, false otherwise
*/
bool xsIntIntDictContains(int dct = -1, int key = -1) {
    int capacity = xsArrayGetSize(dct);
    return (_xsIntIntDictFindSlot(dct, key, capacity) >= 0);
}

/*
    Returns the number of key-value pairs in the dict.
    @param dct - dict id
    @return dict size
*/
int xsIntIntDictSize(int dct = -1) {
    return (xsArrayGetInt(dct, 0));
}

/*
    Removes all entries from the dict and shrinks the backing array.
    @param dct - dict id
    @return `cIntIntDictSuccess` on success, or `cIntIntDictGenericError` on error
*/
int xsIntIntDictClear(int dct = -1) {
    int capacity = xsArrayGetSize(dct);
    int i = 1;
    while (i < capacity) {
        xsArraySetInt(dct, i, cIntIntDictEmptyKey);
        i = i + 2;
    }
    xsArraySetInt(dct, 0, 0);
    if (capacity > cIntIntDictInitialCapacity) {
        int r = xsArrayResizeInt(dct, cIntIntDictInitialCapacity);
        if (r != 1) {
            return (cIntIntDictGenericError);
        }
    }
    return (cIntIntDictSuccess);
}

/*
    Returns a deep copy of the dict.
    @param dct - dict id
    @return new dict id, or `cIntIntDictResizeFailedError` on error
*/
int xsIntIntDictCopy(int dct = -1) {
    int capacity = xsArrayGetSize(dct);
    int newDct = xsArrayCreateInt(capacity, cIntIntDictEmptyKey);
    if (newDct < 0) {
        return (cIntIntDictResizeFailedError);
    }
    int i = 1;
    while (i < capacity) {
        int storedKey = xsArrayGetInt(dct, i);
        if (storedKey != cIntIntDictEmptyKey) {
            xsArraySetInt(newDct, i, storedKey);
            xsArraySetInt(newDct, i + 1, xsArrayGetInt(dct, i + 1));
        }
        i = i + 2;
    }
    xsArraySetInt(newDct, 0, xsArrayGetInt(dct, 0));
    return (newDct);
}

/*
    Returns a string representation of the dict in the format `{k1 - v1, k2 - v2, ...}`.
    @param dct - dict id
    @return string representation of the dict
*/
string xsIntIntDictToString(int dct = -1) {
    int capacity = xsArrayGetSize(dct);
    string s = "{";
    int key = 0;
    int val = 0;
    bool first = true;
    int i = 1;
    while (i < capacity) {
        key = xsArrayGetInt(dct, i);
        if (key != cIntIntDictEmptyKey) {
            val = xsArrayGetInt(dct, i + 1);
            if (first) {
                first = false;
            } else {
                s = s + ", ";
            }
            s = s + (key + ": " + val);
        }
        i = i + 2;
    }
    s = s + "}";
    return (s);
}

/*
    Returns the status code of the last operation that sets it (put, get, remove, next_key, has_next).
    @return `cIntIntDictSuccess` if the last such operation succeeded, or a negative error code
*/
int xsIntIntDictLastError() {
    return (_intIntDictLastOperationStatus);
}

int _xsIntIntDictFindNextOccupied(int dct = -1, int start = 1, int capacity = 0) {
    int slot = start;
    while (slot < capacity) {
        int storedKey = xsArrayGetInt(dct, slot);
        if (storedKey != cIntIntDictEmptyKey) {
            _intIntDictLastOperationStatus = cIntIntDictSuccess;
            return (storedKey);
        }
        slot = slot + 2;
    }
    _intIntDictLastOperationStatus = cIntIntDictNoKeyError;
    return (cIntIntDictGenericError);
}

/*
    Returns the next key in the dict for stateless iteration. Sets last error on completion.
    @param dct - dict id
    @param is_first - if true, returns the first key in the dict
    @param prev_key - the previous key returned by this function (ignored if `isFirst` is true)
    @return next key, or `cIntIntDictGenericError` if no more keys (last error set to `cIntIntDictNoKeyError`)
*/
int xsIntIntDictNextKey(int dct = -1, bool isFirst = true, int prevKey = -1) {
    int capacity = xsArrayGetSize(dct);
    if (isFirst) {
        return (_xsIntIntDictFindNextOccupied(dct, 1, capacity));
    }
    int slot = _xsIntIntDictFindSlot(dct, prevKey, capacity);
    if (slot < 0) {
        _intIntDictLastOperationStatus = cIntIntDictNoKeyError;
        return (cIntIntDictGenericError);
    }
    int nextStart = slot + 2;
    return (_xsIntIntDictFindNextOccupied(dct, nextStart, capacity));
}

/*
    Checks whether there is a next key in the dict for stateless iteration.
    @param dct - dict id
    @param is_first - if true, checks whether the dict has any keys
    @param prev_key - the previous key (ignored if `isFirst` is true)
    @return true if there is a next key, false otherwise
*/
bool xsIntIntDictHasNext(int dct = -1, bool isFirst = true, int prevKey = -1) {
    int capacity = xsArrayGetSize(dct);
    int start = 1;
    if (isFirst == false) {
        int slot = _xsIntIntDictFindSlot(dct, prevKey, capacity);
        if (slot < 0) {
            return (false);
        }
        start = slot + 2;
    }
    while (start < capacity) {
        if (xsArrayGetInt(dct, start) != cIntIntDictEmptyKey) {
            return (true);
        }
        start = start + 2;
    }
    return (false);
}

/*
    Inserts all key-value pairs from another dict into the source dict, overwriting existing keys.
    @param source - dict id to update
    @param dct - dict id whose entries are copied into source
    @return `cIntIntDictSuccess` on success, or a negative error code
*/
int xsIntIntDictUpdate(int source = -1, int dct = -1) {
    int capacity = xsArrayGetSize(dct);
    int i = 1;
    while (i < capacity) {
        int key = xsArrayGetInt(dct, i);
        if (key != cIntIntDictEmptyKey) {
            xsIntIntDictPut(source, key, xsArrayGetInt(dct, i + 1));
            if ((_intIntDictLastOperationStatus != cIntIntDictSuccess) && (_intIntDictLastOperationStatus != cIntIntDictNoKeyError)) {
                return (_intIntDictLastOperationStatus);
            }
        }
        i = i + 2;
    }
    _intIntDictLastOperationStatus = cIntIntDictSuccess;
    return (cIntIntDictSuccess);
}

/*
    Inserts the key-value pair only if the key is not already present. Sets last error on completion.
    If `key` equals `cIntIntDictEmptyKey`, the call is a no-op and returns `cIntIntDictGenericError`
    with last error set to `cIntIntDictGenericError`.
    @param dct - dict id
    @param key - key to insert (must not equal `cIntIntDictEmptyKey`)
    @param val - value to associate with the key
    @return existing value if the key was already present, or `cIntIntDictGenericError` if newly inserted or on error.
        Callers must check `xs_int_int_dict_last_error()` to distinguish - `cIntIntDictSuccess` means the key
        already existed and the returned value is the existing one; `cIntIntDictNoKeyError` means a new key
        was inserted; any other negative status indicates an error.
*/
int xsIntIntDictPutIfAbsent(int dct = -1, int key = -1, int val = 0) {
    if (key == cIntIntDictEmptyKey) {
        _intIntDictLastOperationStatus = cIntIntDictGenericError;
        return (cIntIntDictGenericError);
    }
    int size = xsArrayGetInt(dct, 0);
    int capacity = xsArrayGetSize(dct);
    int slot = _xsIntIntDictFindSlot(dct, key, capacity);
    if (slot >= 0) {
        _intIntDictLastOperationStatus = cIntIntDictSuccess;
        return (xsArrayGetInt(dct, slot + 1));
    }
    int r = _xsIntIntDictRehashIfNeeded(dct, size, capacity, size + 1);
    if (r != cIntIntDictSuccess) {
        return (cIntIntDictGenericError);
    }
    capacity = xsArrayGetSize(dct);
    int result = _xsIntIntDictUpsert(dct, key, val, capacity);
    if (_intIntDictLastOperationStatus == cIntIntDictNoKeyError) {
        xsArraySetInt(dct, 0, size + 1);
        return (cIntIntDictGenericError);
    }
    if (_intIntDictLastOperationStatus != cIntIntDictSuccess) {
        return (cIntIntDictGenericError);
    }
    return (result);
}

/*
    Returns a new int array containing all keys in the dict. Order is arbitrary.
    @param dct - dict id
    @return array id, or `cIntIntDictResizeFailedError` on allocation failure
*/
int xsIntIntDictKeys(int dct = -1) {
    int size = xsArrayGetInt(dct, 0);
    int arr = xsArrayCreateInt(size, 0);
    if (arr < 0) {
        return (cIntIntDictResizeFailedError);
    }
    int capacity = xsArrayGetSize(dct);
    int idx = 0;
    int i = 1;
    while (i < capacity) {
        int storedKey = xsArrayGetInt(dct, i);
        if (storedKey != cIntIntDictEmptyKey) {
            xsArraySetInt(arr, idx, storedKey);
            idx++;
        }
        i = i + 2;
    }
    return (arr);
}

/*
    Returns a new int array containing all values in the dict. Order matches `xsIntIntDictKeys`.
    @param dct - dict id
    @return array id, or `cIntIntDictResizeFailedError` on allocation failure
*/
int xsIntIntDictValues(int dct = -1) {
    int size = xsArrayGetInt(dct, 0);
    int arr = xsArrayCreateInt(size, 0);
    if (arr < 0) {
        return (cIntIntDictResizeFailedError);
    }
    int capacity = xsArrayGetSize(dct);
    int idx = 0;
    int i = 1;
    while (i < capacity) {
        int storedKey = xsArrayGetInt(dct, i);
        if (storedKey != cIntIntDictEmptyKey) {
            xsArraySetInt(arr, idx, xsArrayGetInt(dct, i + 1));
            idx++;
        }
        i = i + 2;
    }
    return (arr);
}

/*
    Returns true if both dicts contain the same key-value pairs.
    @param a - first dict id
    @param b - second dict id
    @return true if both dicts are equal, false otherwise
*/
bool xsIntIntDictEquals(int a = -1, int b = -1) {
    int sizeA = xsArrayGetInt(a, 0);
    int sizeB = xsArrayGetInt(b, 0);
    if (sizeA != sizeB) {
        return (false);
    }
    int capacity = xsArrayGetSize(a);
    int i = 1;
    while (i < capacity) {
        int key = xsArrayGetInt(a, i);
        if (key != cIntIntDictEmptyKey) {
            int val = xsArrayGetInt(a, i + 1);
            if (xsIntIntDictGet(b, key) != val) {
                return (false);
            }
            if (xsIntIntDictLastError() != cIntIntDictSuccess) {
                return (false);
            }
        }
        i = i + 2;
    }
    return (true);
}

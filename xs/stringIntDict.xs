extern const int cStringIntDictSuccess = 0;
extern const int cStringIntDictGenericError = -1;
extern const int cStringIntDictNoKeyError = -2;
extern const int cStringIntDictResizeFailedError = -3;
extern const int cStringIntDictMaxCapacityError = -4;
extern const int cStringIntDictMaxCapacity = 249999998;
extern const int cStringIntDictInitialCapacity = 16;
extern const int cStringIntDictHeaderSize = 4;
extern const int cStringIntDictNodeStride = 4;
int _stringIntDictLastOperationStatus = cStringIntDictSuccess;
int _stringIntDictResultValue = cStringIntDictGenericError;
bool _stringIntDictInsertedNew = false;
bool _stringIntDictRemoved = false;

int _xsStringIntDictEffectiveInitialCapacity() {
    int capacity = cStringIntDictInitialCapacity;
    if (capacity > cStringIntDictMaxCapacity) {
        capacity = cStringIntDictMaxCapacity;
    }
    if (capacity < 0) {
        return (0);
    }
    return (capacity);
}

int _xsStringIntDictGetKeysArray(int dct = -1) {
    return (xsArrayGetInt(dct, 1));
}

void _xsStringIntDictSetKeysArray(int dct = -1, int arr = -1) {
    xsArraySetInt(dct, 1, arr);
}

int _xsStringIntDictGetRoot(int dct = -1) {
    return (xsArrayGetInt(dct, 2));
}

void _xsStringIntDictSetRoot(int dct = -1, int root = -1) {
    xsArraySetInt(dct, 2, root);
}

int _xsStringIntDictGetFreeHead(int dct = -1) {
    return (xsArrayGetInt(dct, 3));
}

void _xsStringIntDictSetFreeHead(int dct = -1, int head = -1) {
    xsArraySetInt(dct, 3, head);
}

int _xsStringIntDictCapacityFromDataSize(int dataSize = 0) {
    return ((dataSize - cStringIntDictHeaderSize) / cStringIntDictNodeStride);
}

int _xsStringIntDictCapacity(int dct = -1) {
    return (_xsStringIntDictCapacityFromDataSize(xsArrayGetSize(dct)));
}

int _xsStringIntDictNodeBase(int node = 0) {
    return (cStringIntDictHeaderSize + (node * cStringIntDictNodeStride));
}

int _xsStringIntDictValueSlot(int node = 0) {
    return (_xsStringIntDictNodeBase(node));
}

int _xsStringIntDictLeftSlot(int node = 0) {
    return (_xsStringIntDictNodeBase(node) + 1);
}

int _xsStringIntDictRightSlot(int node = 0) {
    return (_xsStringIntDictNodeBase(node) + 2);
}

int _xsStringIntDictHeightSlot(int node = 0) {
    return (_xsStringIntDictNodeBase(node) + 3);
}

string _xsStringIntDictGetStoredKey(int dct = -1, int node = 0) {
    return (xsArrayGetString(_xsStringIntDictGetKeysArray(dct), node));
}

void _xsStringIntDictSetStoredKey(int dct = -1, int node = 0, string key = "") {
    xsArraySetString(_xsStringIntDictGetKeysArray(dct), node, key);
}

int _xsStringIntDictGetStoredValue(int dct = -1, int node = 0) {
    return (xsArrayGetInt(dct, _xsStringIntDictValueSlot(node)));
}

void _xsStringIntDictSetStoredValue(int dct = -1, int node = 0, int value = 0) {
    xsArraySetInt(dct, _xsStringIntDictValueSlot(node), value);
}

int _xsStringIntDictGetLeft(int dct = -1, int node = 0) {
    return (xsArrayGetInt(dct, _xsStringIntDictLeftSlot(node)));
}

void _xsStringIntDictSetLeft(int dct = -1, int node = 0, int child = -1) {
    xsArraySetInt(dct, _xsStringIntDictLeftSlot(node), child);
}

int _xsStringIntDictGetRight(int dct = -1, int node = 0) {
    return (xsArrayGetInt(dct, _xsStringIntDictRightSlot(node)));
}

void _xsStringIntDictSetRight(int dct = -1, int node = 0, int child = -1) {
    xsArraySetInt(dct, _xsStringIntDictRightSlot(node), child);
}

int _xsStringIntDictGetHeightOrNext(int dct = -1, int node = 0) {
    return (xsArrayGetInt(dct, _xsStringIntDictHeightSlot(node)));
}

void _xsStringIntDictSetHeightOrNext(int dct = -1, int node = 0, int value = 0) {
    xsArraySetInt(dct, _xsStringIntDictHeightSlot(node), value);
}

void _xsStringIntDictInitializeFreeNodes(int dct = -1, int start = 0, int stop = 0, int nextHead = -1) {
    for (i = start; < stop) {
        _xsStringIntDictSetStoredKey(dct, i, "!<[empty");
        _xsStringIntDictSetStoredValue(dct, i, 0);
        _xsStringIntDictSetLeft(dct, i, -1);
        _xsStringIntDictSetRight(dct, i, -1);
        int nextFree = nextHead;
        if ((i + 1) < stop) {
            nextFree = i + 1;
        }
        _xsStringIntDictSetHeightOrNext(dct, i, nextFree);
    }
}

/*
    Creates an empty string-to-int dictionary.
    Keys equal to `"!<[empty"` are reserved as the internal empty-key sentinel
    and cannot be stored. `put` and `putIfAbsent` silently reject them.
    @return created dict id, or `cStringIntDictGenericError` on error
*/
int xsStringIntDictCreate() {
    int capacity = _xsStringIntDictEffectiveInitialCapacity();
    int dataSize = cStringIntDictHeaderSize + (capacity * cStringIntDictNodeStride);
    int dct = xsArrayCreateInt(dataSize, -1);
    if (dct < 0) {
        return (cStringIntDictGenericError);
    }
    int keysArr = xsArrayCreateString(capacity, "!<[empty");
    if (keysArr < 0) {
        xsArrayResizeInt(dct, 0);
        return (cStringIntDictGenericError);
    }
    xsArraySetInt(dct, 0, 0);
    _xsStringIntDictSetKeysArray(dct, keysArr);
    _xsStringIntDictSetRoot(dct, -1);
    _xsStringIntDictSetFreeHead(dct, -1);
    if (capacity > 0) {
        _xsStringIntDictInitializeFreeNodes(dct, 0, capacity, -1);
        _xsStringIntDictSetFreeHead(dct, 0);
    }
    return (dct);
}

int _xsStringIntDictResize(int dct = -1, int newCapacity = 0) {
    int oldCapacity = _xsStringIntDictCapacity(dct);
    if (newCapacity <= oldCapacity) {
        return (cStringIntDictSuccess);
    }
    if (newCapacity > cStringIntDictMaxCapacity) {
        return (cStringIntDictMaxCapacityError);
    }
    int keysArr = _xsStringIntDictGetKeysArray(dct);
    int rKeys = xsArrayResizeString(keysArr, newCapacity);
    if (rKeys != 1) {
        return (cStringIntDictResizeFailedError);
    }
    int oldFreeHead = _xsStringIntDictGetFreeHead(dct);
    int newDataSize = cStringIntDictHeaderSize + (newCapacity * cStringIntDictNodeStride);
    int r = xsArrayResizeInt(dct, newDataSize);
    if (r != 1) {
        return (cStringIntDictResizeFailedError);
    }
    _xsStringIntDictInitializeFreeNodes(dct, oldCapacity, newCapacity, oldFreeHead);
    _xsStringIntDictSetFreeHead(dct, oldCapacity);
    return (cStringIntDictSuccess);
}

int _xsStringIntDictEnsureCapacity(int dct = -1, int requiredSize = 0) {
    int capacity = _xsStringIntDictCapacity(dct);
    if (requiredSize <= capacity) {
        return (cStringIntDictSuccess);
    }
    if (requiredSize > cStringIntDictMaxCapacity) {
        return (cStringIntDictMaxCapacityError);
    }
    int newCapacity = capacity;
    if (newCapacity < 1) {
        newCapacity = 1;
    }
    while (newCapacity < requiredSize) {
        if (newCapacity > (cStringIntDictMaxCapacity / 2)) {
            newCapacity = cStringIntDictMaxCapacity;
        } else {
            newCapacity = newCapacity * 2;
        }
    }
    return (_xsStringIntDictResize(dct, newCapacity));
}

int _xsStringIntDictAllocateNode(int dct = -1, string key = "", int value = 0) {
    int freeHead = _xsStringIntDictGetFreeHead(dct);
    if (freeHead < 0) {
        return (-1);
    }
    _xsStringIntDictSetFreeHead(dct, _xsStringIntDictGetHeightOrNext(dct, freeHead));
    _xsStringIntDictSetStoredKey(dct, freeHead, key);
    _xsStringIntDictSetStoredValue(dct, freeHead, value);
    _xsStringIntDictSetLeft(dct, freeHead, -1);
    _xsStringIntDictSetRight(dct, freeHead, -1);
    _xsStringIntDictSetHeightOrNext(dct, freeHead, 1);
    return (freeHead);
}

void _xsStringIntDictFreeNode(int dct = -1, int node = -1) {
    _xsStringIntDictSetStoredKey(dct, node, "!<[empty");
    _xsStringIntDictSetStoredValue(dct, node, 0);
    _xsStringIntDictSetLeft(dct, node, -1);
    _xsStringIntDictSetRight(dct, node, -1);
    _xsStringIntDictSetHeightOrNext(dct, node, _xsStringIntDictGetFreeHead(dct));
    _xsStringIntDictSetFreeHead(dct, node);
}

int _xsStringIntDictHeight(int dct = -1, int node = -1) {
    if (node < 0) {
        return (0);
    }
    return (_xsStringIntDictGetHeightOrNext(dct, node));
}

void _xsStringIntDictRefreshHeight(int dct = -1, int node = -1) {
    int leftHeight = _xsStringIntDictHeight(dct, _xsStringIntDictGetLeft(dct, node));
    int rightHeight = _xsStringIntDictHeight(dct, _xsStringIntDictGetRight(dct, node));
    if (leftHeight > rightHeight) {
        _xsStringIntDictSetHeightOrNext(dct, node, leftHeight + 1);
    } else {
        _xsStringIntDictSetHeightOrNext(dct, node, rightHeight + 1);
    }
}

int _xsStringIntDictBalanceFactor(int dct = -1, int node = -1) {
    return (_xsStringIntDictHeight(dct, _xsStringIntDictGetLeft(dct, node)) - _xsStringIntDictHeight(dct, _xsStringIntDictGetRight(dct, node)));
}

int _xsStringIntDictRotateLeft(int dct = -1, int node = -1) {
    int newRoot = _xsStringIntDictGetRight(dct, node);
    int moved = _xsStringIntDictGetLeft(dct, newRoot);
    _xsStringIntDictSetRight(dct, node, moved);
    _xsStringIntDictSetLeft(dct, newRoot, node);
    _xsStringIntDictRefreshHeight(dct, node);
    _xsStringIntDictRefreshHeight(dct, newRoot);
    return (newRoot);
}

int _xsStringIntDictRotateRight(int dct = -1, int node = -1) {
    int newRoot = _xsStringIntDictGetLeft(dct, node);
    int moved = _xsStringIntDictGetRight(dct, newRoot);
    _xsStringIntDictSetLeft(dct, node, moved);
    _xsStringIntDictSetRight(dct, newRoot, node);
    _xsStringIntDictRefreshHeight(dct, node);
    _xsStringIntDictRefreshHeight(dct, newRoot);
    return (newRoot);
}

int _xsStringIntDictRebalance(int dct = -1, int node = -1) {
    _xsStringIntDictRefreshHeight(dct, node);
    int balance = _xsStringIntDictBalanceFactor(dct, node);
    if (balance > 1) {
        int left = _xsStringIntDictGetLeft(dct, node);
        if (_xsStringIntDictBalanceFactor(dct, left) < 0) {
            _xsStringIntDictSetLeft(dct, node, _xsStringIntDictRotateLeft(dct, left));
        }
        return (_xsStringIntDictRotateRight(dct, node));
    }
    if (balance < -1) {
        int right = _xsStringIntDictGetRight(dct, node);
        if (_xsStringIntDictBalanceFactor(dct, right) > 0) {
            _xsStringIntDictSetRight(dct, node, _xsStringIntDictRotateRight(dct, right));
        }
        return (_xsStringIntDictRotateLeft(dct, node));
    }
    return (node);
}

int _xsStringIntDictFindNode(int dct = -1, string key = "") {
    int node = _xsStringIntDictGetRoot(dct);
    while (node >= 0) {
        string storedKey = _xsStringIntDictGetStoredKey(dct, node);
        if (key == storedKey) {
            return (node);
        }
        if (key < storedKey) {
            node = _xsStringIntDictGetLeft(dct, node);
        } else {
            node = _xsStringIntDictGetRight(dct, node);
        }
    }
    return (-1);
}

int _xsStringIntDictInsertNode(int dct = -1, int node = -1, string key = "", int value = 0) {
    if (node < 0) {
        _stringIntDictInsertedNew = true;
        _stringIntDictResultValue = cStringIntDictGenericError;
        return (_xsStringIntDictAllocateNode(dct, key, value));
    }
    string storedKey = _xsStringIntDictGetStoredKey(dct, node);
    if (key == storedKey) {
        _stringIntDictInsertedNew = false;
        _stringIntDictResultValue = _xsStringIntDictGetStoredValue(dct, node);
        _xsStringIntDictSetStoredValue(dct, node, value);
        return (node);
    }
    if (key < storedKey) {
        _xsStringIntDictSetLeft(dct, node, _xsStringIntDictInsertNode(dct, _xsStringIntDictGetLeft(dct, node), key, value));
    } else {
        _xsStringIntDictSetRight(dct, node, _xsStringIntDictInsertNode(dct, _xsStringIntDictGetRight(dct, node), key, value));
    }
    return (_xsStringIntDictRebalance(dct, node));
}

int _xsStringIntDictMinNode(int dct = -1, int node = -1) {
    int current = node;
    while (current >= 0) {
        int left = _xsStringIntDictGetLeft(dct, current);
        if (left < 0) {
            return (current);
        }
        current = left;
    }
    return (-1);
}

int _xsStringIntDictRemoveMin(int dct = -1, int node = -1) {
    int left = _xsStringIntDictGetLeft(dct, node);
    if (left < 0) {
        int right = _xsStringIntDictGetRight(dct, node);
        _xsStringIntDictFreeNode(dct, node);
        return (right);
    }
    _xsStringIntDictSetLeft(dct, node, _xsStringIntDictRemoveMin(dct, left));
    return (_xsStringIntDictRebalance(dct, node));
}

int _xsStringIntDictRemoveNode(int dct = -1, int node = -1, string key = "") {
    if (node < 0) {
        return (-1);
    }
    string storedKey = _xsStringIntDictGetStoredKey(dct, node);
    if (key < storedKey) {
        _xsStringIntDictSetLeft(dct, node, _xsStringIntDictRemoveNode(dct, _xsStringIntDictGetLeft(dct, node), key));
        return (_xsStringIntDictRebalance(dct, node));
    }
    if (key > storedKey) {
        _xsStringIntDictSetRight(dct, node, _xsStringIntDictRemoveNode(dct, _xsStringIntDictGetRight(dct, node), key));
        return (_xsStringIntDictRebalance(dct, node));
    }
    _stringIntDictRemoved = true;
    _stringIntDictResultValue = _xsStringIntDictGetStoredValue(dct, node);
    int left = _xsStringIntDictGetLeft(dct, node);
    int right = _xsStringIntDictGetRight(dct, node);
    if (left < 0) {
        _xsStringIntDictFreeNode(dct, node);
        return (right);
    }
    if (right < 0) {
        _xsStringIntDictFreeNode(dct, node);
        return (left);
    }
    int successor = _xsStringIntDictMinNode(dct, right);
    _xsStringIntDictSetStoredKey(dct, node, _xsStringIntDictGetStoredKey(dct, successor));
    _xsStringIntDictSetStoredValue(dct, node, _xsStringIntDictGetStoredValue(dct, successor));
    _xsStringIntDictSetRight(dct, node, _xsStringIntDictRemoveMin(dct, right));
    return (_xsStringIntDictRebalance(dct, node));
}

int _xsStringIntDictFindSuccessorNode(int dct = -1, string key = "") {
    int node = _xsStringIntDictGetRoot(dct);
    int successor = -1;
    while (node >= 0) {
        string storedKey = _xsStringIntDictGetStoredKey(dct, node);
        if (key < storedKey) {
            successor = node;
            node = _xsStringIntDictGetLeft(dct, node);
        } else if (key > storedKey) {
            node = _xsStringIntDictGetRight(dct, node);
        } else {
            int right = _xsStringIntDictGetRight(dct, node);
            if (right >= 0) {
                return (_xsStringIntDictMinNode(dct, right));
            }
            return (successor);
        }
    }
    return (-1);
}

int _xsStringIntDictKeysFill(int dct = -1, int node = -1, int arr = -1, int idx = 0) {
    if (node < 0) {
        return (idx);
    }
    idx = _xsStringIntDictKeysFill(dct, _xsStringIntDictGetLeft(dct, node), arr, idx);
    xsArraySetString(arr, idx, _xsStringIntDictGetStoredKey(dct, node));
    idx++;
    return (_xsStringIntDictKeysFill(dct, _xsStringIntDictGetRight(dct, node), arr, idx));
}

int _xsStringIntDictValuesFill(int dct = -1, int node = -1, int arr = -1, int idx = 0) {
    if (node < 0) {
        return (idx);
    }
    idx = _xsStringIntDictValuesFill(dct, _xsStringIntDictGetLeft(dct, node), arr, idx);
    xsArraySetInt(arr, idx, _xsStringIntDictGetStoredValue(dct, node));
    idx++;
    return (_xsStringIntDictValuesFill(dct, _xsStringIntDictGetRight(dct, node), arr, idx));
}

bool _xsStringIntDictEqualsWalk(int a = -1, int b = -1, int node = -1) {
    if (node < 0) {
        return (true);
    }
    if (_xsStringIntDictEqualsWalk(a, b, _xsStringIntDictGetLeft(a, node)) == false) {
        return (false);
    }
    string key = _xsStringIntDictGetStoredKey(a, node);
    int val = _xsStringIntDictGetStoredValue(a, node);
    int other = _xsStringIntDictFindNode(b, key);
    if (other < 0) {
        return (false);
    }
    if (_xsStringIntDictGetStoredValue(b, other) != val) {
        return (false);
    }
    return (_xsStringIntDictEqualsWalk(a, b, _xsStringIntDictGetRight(a, node)));
}

int _xsStringIntDictUpdateWalk(int source = -1, int dct = -1, int node = -1) {
    if (node < 0) {
        return (cStringIntDictSuccess);
    }
    int leftResult = _xsStringIntDictUpdateWalk(source, dct, _xsStringIntDictGetLeft(dct, node));
    if (leftResult != cStringIntDictSuccess) {
        return (leftResult);
    }
    string key = _xsStringIntDictGetStoredKey(dct, node);
    int val = _xsStringIntDictGetStoredValue(dct, node);
    int existing = _xsStringIntDictFindNode(source, key);
    if (existing >= 0) {
        _xsStringIntDictSetStoredValue(source, existing, val);
        _stringIntDictLastOperationStatus = cStringIntDictSuccess;
    } else {
        int size = xsArrayGetInt(source, 0);
        int resizeResult = _xsStringIntDictEnsureCapacity(source, size + 1);
        if (resizeResult != cStringIntDictSuccess) {
            _stringIntDictLastOperationStatus = resizeResult;
            return (resizeResult);
        }
        _stringIntDictInsertedNew = false;
        _stringIntDictResultValue = cStringIntDictGenericError;
        _xsStringIntDictSetRoot(source, _xsStringIntDictInsertNode(source, _xsStringIntDictGetRoot(source), key, val));
        if (_stringIntDictInsertedNew) {
            xsArraySetInt(source, 0, size + 1);
            _stringIntDictLastOperationStatus = cStringIntDictNoKeyError;
        } else {
            _stringIntDictLastOperationStatus = cStringIntDictSuccess;
        }
    }
    return (_xsStringIntDictUpdateWalk(source, dct, _xsStringIntDictGetRight(dct, node)));
}

string _xsStringIntDictToStringContents(int dct = -1, int node = -1) {
    if (node < 0) {
        return ("");
    }
    string left = _xsStringIntDictToStringContents(dct, _xsStringIntDictGetLeft(dct, node));
    string current = (("\"" + _xsStringIntDictGetStoredKey(dct, node)) + "\": ") + ("" + _xsStringIntDictGetStoredValue(dct, node));
    string combined = current;
    if (left != "") {
        combined = (left + ", ") + current;
    }
    string right = _xsStringIntDictToStringContents(dct, _xsStringIntDictGetRight(dct, node));
    if (right != "") {
        combined = combined + (", " + right);
    }
    return (combined);
}

/*
    Inserts or updates a key-value pair. Sets last error on completion.
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
    int existing = _xsStringIntDictFindNode(dct, key);
    if (existing >= 0) {
        int oldVal = _xsStringIntDictGetStoredValue(dct, existing);
        _xsStringIntDictSetStoredValue(dct, existing, val);
        _stringIntDictLastOperationStatus = cStringIntDictSuccess;
        return (oldVal);
    }
    int size = xsArrayGetInt(dct, 0);
    int r = _xsStringIntDictEnsureCapacity(dct, size + 1);
    if (r != cStringIntDictSuccess) {
        _stringIntDictLastOperationStatus = r;
        return (cStringIntDictGenericError);
    }
    _stringIntDictInsertedNew = false;
    _stringIntDictResultValue = cStringIntDictGenericError;
    _xsStringIntDictSetRoot(dct, _xsStringIntDictInsertNode(dct, _xsStringIntDictGetRoot(dct), key, val));
    if (_stringIntDictInsertedNew) {
        xsArraySetInt(dct, 0, size + 1);
        _stringIntDictLastOperationStatus = cStringIntDictNoKeyError;
        return (cStringIntDictGenericError);
    }
    _stringIntDictLastOperationStatus = cStringIntDictSuccess;
    return (_stringIntDictResultValue);
}

/*
    Creates a dict with provided key-value pairs. The first key that equals
    the reserved empty-key sentinel will stop further insertion.
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
    int node = _xsStringIntDictFindNode(dct, key);
    if (node >= 0) {
        _stringIntDictLastOperationStatus = cStringIntDictSuccess;
        return (_xsStringIntDictGetStoredValue(dct, node));
    }
    _stringIntDictLastOperationStatus = cStringIntDictNoKeyError;
    return (dft);
}

/*
    Removes the entry with the given key from the dict. Sets last error on completion.
*/
int xsStringIntDictRemove(int dct = -1, string key = "") {
    _stringIntDictRemoved = false;
    _stringIntDictResultValue = cStringIntDictGenericError;
    _xsStringIntDictSetRoot(dct, _xsStringIntDictRemoveNode(dct, _xsStringIntDictGetRoot(dct), key));
    if (_stringIntDictRemoved == false) {
        _stringIntDictLastOperationStatus = cStringIntDictNoKeyError;
        return (cStringIntDictGenericError);
    }
    xsArraySetInt(dct, 0, xsArrayGetInt(dct, 0) - 1);
    _stringIntDictLastOperationStatus = cStringIntDictSuccess;
    return (_stringIntDictResultValue);
}

bool xsStringIntDictContains(int dct = -1, string key = "") {
    return (_xsStringIntDictFindNode(dct, key) >= 0);
}

int xsStringIntDictSize(int dct = -1) {
    return (xsArrayGetInt(dct, 0));
}

/*
    Removes all entries from the dict and shrinks the backing arrays.
*/
int xsStringIntDictClear(int dct = -1) {
    int targetCapacity = _xsStringIntDictEffectiveInitialCapacity();
    int currentCapacity = _xsStringIntDictCapacity(dct);
    if (currentCapacity > targetCapacity) {
        int oldKeysArr = _xsStringIntDictGetKeysArray(dct);
        int newKeysArr = xsArrayCreateString(targetCapacity, "!<[empty");
        if (newKeysArr < 0) {
            return (cStringIntDictGenericError);
        }
        int newDataSize = cStringIntDictHeaderSize + (targetCapacity * cStringIntDictNodeStride);
        int r = xsArrayResizeInt(dct, newDataSize);
        if (r != 1) {
            xsArrayResizeString(newKeysArr, 0);
            return (cStringIntDictGenericError);
        }
        _xsStringIntDictSetKeysArray(dct, newKeysArr);
        xsArrayResizeString(oldKeysArr, 0);
        currentCapacity = targetCapacity;
    }
    xsArraySetInt(dct, 0, 0);
    _xsStringIntDictSetRoot(dct, -1);
    _xsStringIntDictSetFreeHead(dct, -1);
    if (currentCapacity > 0) {
        _xsStringIntDictInitializeFreeNodes(dct, 0, currentCapacity, -1);
        _xsStringIntDictSetFreeHead(dct, 0);
    }
    return (cStringIntDictSuccess);
}

/*
    Returns a deep copy of the dict.
*/
int xsStringIntDictCopy(int dct = -1) {
    int dataSize = xsArrayGetSize(dct);
    int capacity = _xsStringIntDictCapacity(dct);
    int newDct = xsArrayCreateInt(dataSize, -1);
    if (newDct < 0) {
        return (cStringIntDictResizeFailedError);
    }
    int newKeysArr = xsArrayCreateString(capacity, "!<[empty");
    if (newKeysArr < 0) {
        xsArrayResizeInt(newDct, 0);
        return (cStringIntDictResizeFailedError);
    }
    for (i = 0; < dataSize) {
        xsArraySetInt(newDct, i, xsArrayGetInt(dct, i));
    }
    _xsStringIntDictSetKeysArray(newDct, newKeysArr);
    int keysArr = _xsStringIntDictGetKeysArray(dct);
    for (j = 0; < capacity) {
        xsArraySetString(newKeysArr, j, xsArrayGetString(keysArr, j));
    }
    return (newDct);
}

/*
    Returns a string representation of the dict in the format `{"k1" - v1, "k2" - v2, ...}`.
*/
string xsStringIntDictToString(int dct = -1) {
    return (("{" + _xsStringIntDictToStringContents(dct, _xsStringIntDictGetRoot(dct))) + "}");
}

int xsStringIntDictLastError() {
    return (_stringIntDictLastOperationStatus);
}

/*
    Returns the next key in the dict for stateless iteration. Sets last error on completion.
*/
string xsStringIntDictNextKey(int dct = -1, bool isFirst = true, string prevKey = "!<[empty") {
    int nextNode = -1;
    if (isFirst) {
        nextNode = _xsStringIntDictMinNode(dct, _xsStringIntDictGetRoot(dct));
    } else {
        int node = _xsStringIntDictFindNode(dct, prevKey);
        if (node < 0) {
            _stringIntDictLastOperationStatus = cStringIntDictNoKeyError;
            return ("-1");
        }
        nextNode = _xsStringIntDictFindSuccessorNode(dct, prevKey);
    }
    if (nextNode < 0) {
        _stringIntDictLastOperationStatus = cStringIntDictNoKeyError;
        return ("-1");
    }
    _stringIntDictLastOperationStatus = cStringIntDictSuccess;
    return (_xsStringIntDictGetStoredKey(dct, nextNode));
}

bool xsStringIntDictHasNext(int dct = -1, bool isFirst = true, string prevKey = "!<[empty") {
    if (isFirst) {
        return (_xsStringIntDictGetRoot(dct) >= 0);
    }
    if (_xsStringIntDictFindNode(dct, prevKey) < 0) {
        return (false);
    }
    return (_xsStringIntDictFindSuccessorNode(dct, prevKey) >= 0);
}

/*
    Inserts all key-value pairs from another dict into the source dict, overwriting existing keys.
*/
int xsStringIntDictUpdate(int source = -1, int dct = -1) {
    int result = _xsStringIntDictUpdateWalk(source, dct, _xsStringIntDictGetRoot(dct));
    if (result != cStringIntDictSuccess) {
        return (result);
    }
    _stringIntDictLastOperationStatus = cStringIntDictSuccess;
    return (cStringIntDictSuccess);
}

/*
    Inserts the key-value pair only if the key is not already present. Sets last error on completion.
    If `key` equals the reserved empty-key sentinel, the call is a no-op and returns
    `cStringIntDictGenericError` with last error set to `cStringIntDictGenericError`.
*/
int xsStringIntDictPutIfAbsent(int dct = -1, string key = "", int val = 0) {
    if (key == "!<[empty") {
        _stringIntDictLastOperationStatus = cStringIntDictGenericError;
        return (cStringIntDictGenericError);
    }
    int existing = _xsStringIntDictFindNode(dct, key);
    if (existing >= 0) {
        _stringIntDictLastOperationStatus = cStringIntDictSuccess;
        return (_xsStringIntDictGetStoredValue(dct, existing));
    }
    int size = xsArrayGetInt(dct, 0);
    int r = _xsStringIntDictEnsureCapacity(dct, size + 1);
    if (r != cStringIntDictSuccess) {
        _stringIntDictLastOperationStatus = r;
        return (cStringIntDictGenericError);
    }
    _stringIntDictInsertedNew = false;
    _stringIntDictResultValue = cStringIntDictGenericError;
    _xsStringIntDictSetRoot(dct, _xsStringIntDictInsertNode(dct, _xsStringIntDictGetRoot(dct), key, val));
    if (_stringIntDictInsertedNew) {
        xsArraySetInt(dct, 0, size + 1);
        _stringIntDictLastOperationStatus = cStringIntDictNoKeyError;
        return (cStringIntDictGenericError);
    }
    _stringIntDictLastOperationStatus = cStringIntDictSuccess;
    return (_stringIntDictResultValue);
}

/*
    Returns a new string array containing all keys in the dict. Order is lexicographic.
*/
int xsStringIntDictKeys(int dct = -1) {
    int size = xsArrayGetInt(dct, 0);
    int arr = xsArrayCreateString(size);
    if (arr < 0) {
        return (cStringIntDictResizeFailedError);
    }
    _xsStringIntDictKeysFill(dct, _xsStringIntDictGetRoot(dct), arr);
    return (arr);
}

/*
    Returns a new int array containing all values in the dict. Order matches `xsStringIntDictKeys`.
*/
int xsStringIntDictValues(int dct = -1) {
    int size = xsArrayGetInt(dct, 0);
    int arr = xsArrayCreateInt(size, 0);
    if (arr < 0) {
        return (cStringIntDictResizeFailedError);
    }
    _xsStringIntDictValuesFill(dct, _xsStringIntDictGetRoot(dct), arr);
    return (arr);
}

/*
    Returns true if both dicts contain the same key-value pairs.
*/
bool xsStringIntDictEquals(int a = -1, int b = -1) {
    if (xsArrayGetInt(a, 0) != xsArrayGetInt(b, 0)) {
        return (false);
    }
    return (_xsStringIntDictEqualsWalk(a, b, _xsStringIntDictGetRoot(a)));
}

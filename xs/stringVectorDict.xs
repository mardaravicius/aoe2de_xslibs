extern const int cStringVectorDictSuccess = 0;
extern const int cStringVectorDictGenericError = -1;
extern const int cStringVectorDictNoKeyError = -2;
extern const int cStringVectorDictResizeFailedError = -3;
extern const int cStringVectorDictMaxCapacityError = -4;
extern const vector cStringVectorDictGenericErrorVector = vector(-1.0, -1.0, -1.0);
extern const int cStringVectorDictMaxCapacity = 333333330;
extern const int cStringVectorDictInitialCapacity = 16;
extern const int cStringVectorDictHeaderSize = 5;
extern const int cStringVectorDictNodeStride = 3;
extern const int cStringVectorDictValueStride = 3;
int _stringVectorDictLastOperationStatus = cStringVectorDictSuccess;

int _xsStringVectorDictEffectiveInitialCapacity() {
    int capacity = cStringVectorDictInitialCapacity;
    if (capacity > cStringVectorDictMaxCapacity) {
        capacity = cStringVectorDictMaxCapacity;
    }
    if (capacity < 0) {
        return (0);
    }
    return (capacity);
}

int _xsStringVectorDictGetKeysArray(int dct = -1) {
    return (xsArrayGetInt(dct, 1));
}

void _xsStringVectorDictSetKeysArray(int dct = -1, int arr = -1) {
    xsArraySetInt(dct, 1, arr);
}

int _xsStringVectorDictGetValuesArray(int dct = -1) {
    return (xsArrayGetInt(dct, 2));
}

void _xsStringVectorDictSetValuesArray(int dct = -1, int arr = -1) {
    xsArraySetInt(dct, 2, arr);
}

int _xsStringVectorDictGetRoot(int dct = -1) {
    return (xsArrayGetInt(dct, 3));
}

void _xsStringVectorDictSetRoot(int dct = -1, int root = -1) {
    xsArraySetInt(dct, 3, root);
}

int _xsStringVectorDictGetFreeHead(int dct = -1) {
    return (xsArrayGetInt(dct, 4));
}

void _xsStringVectorDictSetFreeHead(int dct = -1, int head = -1) {
    xsArraySetInt(dct, 4, head);
}

int _xsStringVectorDictCapacityFromDataSize(int dataSize = 0) {
    return ((dataSize - cStringVectorDictHeaderSize) / cStringVectorDictNodeStride);
}

int _xsStringVectorDictCapacity(int dct = -1) {
    return (_xsStringVectorDictCapacityFromDataSize(xsArrayGetSize(dct)));
}

int _xsStringVectorDictNodeBase(int node = 0) {
    return (cStringVectorDictHeaderSize + (node * cStringVectorDictNodeStride));
}

int _xsStringVectorDictLeftSlot(int node = 0) {
    return (_xsStringVectorDictNodeBase(node));
}

int _xsStringVectorDictRightSlot(int node = 0) {
    return (_xsStringVectorDictNodeBase(node) + 1);
}

int _xsStringVectorDictHeightSlot(int node = 0) {
    return (_xsStringVectorDictNodeBase(node) + 2);
}

int _xsStringVectorDictValueBase(int node = 0) {
    return (node * cStringVectorDictValueStride);
}

string _xsStringVectorDictGetStoredKey(int dct = -1, int node = 0) {
    return (xsArrayGetString(_xsStringVectorDictGetKeysArray(dct), node));
}

void _xsStringVectorDictSetStoredKey(int dct = -1, int node = 0, string key = "") {
    xsArraySetString(_xsStringVectorDictGetKeysArray(dct), node, key);
}

vector _xsStringVectorDictGetStoredValue(int dct = -1, int node = 0) {
    int valuesArr = _xsStringVectorDictGetValuesArray(dct);
    int base = _xsStringVectorDictValueBase(node);
    return (xsVectorSet(xsArrayGetFloat(valuesArr, base), xsArrayGetFloat(valuesArr, base + 1), xsArrayGetFloat(valuesArr, base + 2)));
}

void _xsStringVectorDictSetStoredValue(int dct = -1, int node = 0, vector value = vector(0.0, 0.0, 0.0)) {
    int valuesArr = _xsStringVectorDictGetValuesArray(dct);
    int base = _xsStringVectorDictValueBase(node);
    xsArraySetFloat(valuesArr, base, xsVectorGetX(value));
    xsArraySetFloat(valuesArr, base + 1, xsVectorGetY(value));
    xsArraySetFloat(valuesArr, base + 2, xsVectorGetZ(value));
}

int _xsStringVectorDictGetLeft(int dct = -1, int node = 0) {
    return (xsArrayGetInt(dct, _xsStringVectorDictLeftSlot(node)));
}

void _xsStringVectorDictSetLeft(int dct = -1, int node = 0, int child = -1) {
    xsArraySetInt(dct, _xsStringVectorDictLeftSlot(node), child);
}

int _xsStringVectorDictGetRight(int dct = -1, int node = 0) {
    return (xsArrayGetInt(dct, _xsStringVectorDictRightSlot(node)));
}

void _xsStringVectorDictSetRight(int dct = -1, int node = 0, int child = -1) {
    xsArraySetInt(dct, _xsStringVectorDictRightSlot(node), child);
}

int _xsStringVectorDictGetHeightOrNext(int dct = -1, int node = 0) {
    return (xsArrayGetInt(dct, _xsStringVectorDictHeightSlot(node)));
}

void _xsStringVectorDictSetHeightOrNext(int dct = -1, int node = 0, int value = 0) {
    xsArraySetInt(dct, _xsStringVectorDictHeightSlot(node), value);
}

void _xsStringVectorDictInitializeFreeNodes(int dct = -1, int start = 0, int stop = 0, int nextHead = -1) {
    for (i = start; < stop) {
        _xsStringVectorDictSetStoredKey(dct, i, "!<[empty");
        _xsStringVectorDictSetStoredValue(dct, i, vector(0.0, 0.0, 0.0));
        _xsStringVectorDictSetLeft(dct, i, -1);
        _xsStringVectorDictSetRight(dct, i, -1);
        int nextFree = nextHead;
        if ((i + 1) < stop) {
            nextFree = i + 1;
        }
        _xsStringVectorDictSetHeightOrNext(dct, i, nextFree);
    }
}

/*
    Creates an empty string-to-vector dictionary.
    Keys equal to `"!<[empty"` are reserved as the internal empty-key sentinel
    and cannot be stored. `put` and `putIfAbsent` silently reject them.
    @return created dict id, or `cStringVectorDictGenericError` on error
*/
int xsStringVectorDictCreate() {
    int capacity = _xsStringVectorDictEffectiveInitialCapacity();
    int dataSize = cStringVectorDictHeaderSize + (capacity * cStringVectorDictNodeStride);
    int dct = xsArrayCreateInt(dataSize, -1);
    if (dct < 0) {
        return (cStringVectorDictGenericError);
    }
    int keysArr = xsArrayCreateString(capacity, "!<[empty");
    if (keysArr < 0) {
        xsArrayResizeInt(dct, 0);
        return (cStringVectorDictGenericError);
    }
    int valuesArr = xsArrayCreateFloat(capacity * cStringVectorDictValueStride, 0.0);
    if (valuesArr < 0) {
        xsArrayResizeString(keysArr, 0);
        xsArrayResizeInt(dct, 0);
        return (cStringVectorDictGenericError);
    }
    xsArraySetInt(dct, 0, 0);
    _xsStringVectorDictSetKeysArray(dct, keysArr);
    _xsStringVectorDictSetValuesArray(dct, valuesArr);
    _xsStringVectorDictSetRoot(dct, -1);
    _xsStringVectorDictSetFreeHead(dct, -1);
    if (capacity > 0) {
        _xsStringVectorDictInitializeFreeNodes(dct, 0, capacity, -1);
        _xsStringVectorDictSetFreeHead(dct, 0);
    }
    return (dct);
}

int _xsStringVectorDictResize(int dct = -1, int newCapacity = 0) {
    int oldCapacity = _xsStringVectorDictCapacity(dct);
    if (newCapacity <= oldCapacity) {
        return (cStringVectorDictSuccess);
    }
    if (newCapacity > cStringVectorDictMaxCapacity) {
        return (cStringVectorDictMaxCapacityError);
    }
    int keysArr = _xsStringVectorDictGetKeysArray(dct);
    int rKeys = xsArrayResizeString(keysArr, newCapacity);
    if (rKeys != 1) {
        return (cStringVectorDictResizeFailedError);
    }
    int valuesArr = _xsStringVectorDictGetValuesArray(dct);
    int newValuesSize = newCapacity * cStringVectorDictValueStride;
    int rValues = xsArrayResizeFloat(valuesArr, newValuesSize);
    if (rValues != 1) {
        return (cStringVectorDictResizeFailedError);
    }
    int oldFreeHead = _xsStringVectorDictGetFreeHead(dct);
    int newDataSize = cStringVectorDictHeaderSize + (newCapacity * cStringVectorDictNodeStride);
    int r = xsArrayResizeInt(dct, newDataSize);
    if (r != 1) {
        return (cStringVectorDictResizeFailedError);
    }
    _xsStringVectorDictInitializeFreeNodes(dct, oldCapacity, newCapacity, oldFreeHead);
    _xsStringVectorDictSetFreeHead(dct, oldCapacity);
    return (cStringVectorDictSuccess);
}

int _xsStringVectorDictEnsureCapacity(int dct = -1, int requiredSize = 0) {
    int capacity = _xsStringVectorDictCapacity(dct);
    if (requiredSize <= capacity) {
        return (cStringVectorDictSuccess);
    }
    if (requiredSize > cStringVectorDictMaxCapacity) {
        return (cStringVectorDictMaxCapacityError);
    }
    int newCapacity = capacity;
    if (newCapacity < 1) {
        newCapacity = 1;
    }
    while (newCapacity < requiredSize) {
        if (newCapacity > (cStringVectorDictMaxCapacity / 2)) {
            newCapacity = cStringVectorDictMaxCapacity;
        } else {
            newCapacity = newCapacity * 2;
        }
    }
    return (_xsStringVectorDictResize(dct, newCapacity));
}

int _xsStringVectorDictAllocateNode(int dct = -1, string key = "", vector value = vector(0.0, 0.0, 0.0)) {
    int freeHead = _xsStringVectorDictGetFreeHead(dct);
    if (freeHead < 0) {
        return (-1);
    }
    _xsStringVectorDictSetFreeHead(dct, _xsStringVectorDictGetHeightOrNext(dct, freeHead));
    _xsStringVectorDictSetStoredKey(dct, freeHead, key);
    _xsStringVectorDictSetStoredValue(dct, freeHead, value);
    _xsStringVectorDictSetLeft(dct, freeHead, -1);
    _xsStringVectorDictSetRight(dct, freeHead, -1);
    _xsStringVectorDictSetHeightOrNext(dct, freeHead, 1);
    return (freeHead);
}

void _xsStringVectorDictFreeNode(int dct = -1, int node = -1) {
    _xsStringVectorDictSetStoredKey(dct, node, "!<[empty");
    _xsStringVectorDictSetStoredValue(dct, node, vector(0.0, 0.0, 0.0));
    _xsStringVectorDictSetLeft(dct, node, -1);
    _xsStringVectorDictSetRight(dct, node, -1);
    _xsStringVectorDictSetHeightOrNext(dct, node, _xsStringVectorDictGetFreeHead(dct));
    _xsStringVectorDictSetFreeHead(dct, node);
}

int _xsStringVectorDictHeight(int dct = -1, int node = -1) {
    if (node < 0) {
        return (0);
    }
    return (_xsStringVectorDictGetHeightOrNext(dct, node));
}

void _xsStringVectorDictRefreshHeight(int dct = -1, int node = -1) {
    int leftHeight = _xsStringVectorDictHeight(dct, _xsStringVectorDictGetLeft(dct, node));
    int rightHeight = _xsStringVectorDictHeight(dct, _xsStringVectorDictGetRight(dct, node));
    if (leftHeight > rightHeight) {
        _xsStringVectorDictSetHeightOrNext(dct, node, leftHeight + 1);
    } else {
        _xsStringVectorDictSetHeightOrNext(dct, node, rightHeight + 1);
    }
}

int _xsStringVectorDictBalanceFactor(int dct = -1, int node = -1) {
    return (_xsStringVectorDictHeight(dct, _xsStringVectorDictGetLeft(dct, node)) - _xsStringVectorDictHeight(dct, _xsStringVectorDictGetRight(dct, node)));
}

int _xsStringVectorDictRotateLeft(int dct = -1, int node = -1) {
    int newRoot = _xsStringVectorDictGetRight(dct, node);
    int moved = _xsStringVectorDictGetLeft(dct, newRoot);
    _xsStringVectorDictSetRight(dct, node, moved);
    _xsStringVectorDictSetLeft(dct, newRoot, node);
    _xsStringVectorDictRefreshHeight(dct, node);
    _xsStringVectorDictRefreshHeight(dct, newRoot);
    return (newRoot);
}

int _xsStringVectorDictRotateRight(int dct = -1, int node = -1) {
    int newRoot = _xsStringVectorDictGetLeft(dct, node);
    int moved = _xsStringVectorDictGetRight(dct, newRoot);
    _xsStringVectorDictSetLeft(dct, node, moved);
    _xsStringVectorDictSetRight(dct, newRoot, node);
    _xsStringVectorDictRefreshHeight(dct, node);
    _xsStringVectorDictRefreshHeight(dct, newRoot);
    return (newRoot);
}

int _xsStringVectorDictRebalance(int dct = -1, int node = -1) {
    _xsStringVectorDictRefreshHeight(dct, node);
    int balance = _xsStringVectorDictBalanceFactor(dct, node);
    if (balance > 1) {
        int left = _xsStringVectorDictGetLeft(dct, node);
        if (_xsStringVectorDictBalanceFactor(dct, left) < 0) {
            _xsStringVectorDictSetLeft(dct, node, _xsStringVectorDictRotateLeft(dct, left));
        }
        return (_xsStringVectorDictRotateRight(dct, node));
    }
    if (balance < -1) {
        int right = _xsStringVectorDictGetRight(dct, node);
        if (_xsStringVectorDictBalanceFactor(dct, right) > 0) {
            _xsStringVectorDictSetRight(dct, node, _xsStringVectorDictRotateRight(dct, right));
        }
        return (_xsStringVectorDictRotateLeft(dct, node));
    }
    return (node);
}

int _xsStringVectorDictFindNode(int dct = -1, string key = "") {
    int node = _xsStringVectorDictGetRoot(dct);
    while (node >= 0) {
        string storedKey = _xsStringVectorDictGetStoredKey(dct, node);
        if (key == storedKey) {
            return (node);
        }
        if (key < storedKey) {
            node = _xsStringVectorDictGetLeft(dct, node);
        } else {
            node = _xsStringVectorDictGetRight(dct, node);
        }
    }
    return (-1);
}

int _xsStringVectorDictInsertNode(int dct = -1, int node = -1, string key = "", vector value = vector(0.0, 0.0, 0.0)) {
    if (node < 0) {
        return (_xsStringVectorDictAllocateNode(dct, key, value));
    }
    string storedKey = _xsStringVectorDictGetStoredKey(dct, node);
    if (key == storedKey) {
        _xsStringVectorDictSetStoredValue(dct, node, value);
        return (node);
    }
    if (key < storedKey) {
        _xsStringVectorDictSetLeft(dct, node, _xsStringVectorDictInsertNode(dct, _xsStringVectorDictGetLeft(dct, node), key, value));
    } else {
        _xsStringVectorDictSetRight(dct, node, _xsStringVectorDictInsertNode(dct, _xsStringVectorDictGetRight(dct, node), key, value));
    }
    return (_xsStringVectorDictRebalance(dct, node));
}

int _xsStringVectorDictMinNode(int dct = -1, int node = -1) {
    int current = node;
    while (current >= 0) {
        int left = _xsStringVectorDictGetLeft(dct, current);
        if (left < 0) {
            return (current);
        }
        current = left;
    }
    return (-1);
}

int _xsStringVectorDictRemoveMin(int dct = -1, int node = -1) {
    int left = _xsStringVectorDictGetLeft(dct, node);
    if (left < 0) {
        int right = _xsStringVectorDictGetRight(dct, node);
        _xsStringVectorDictFreeNode(dct, node);
        return (right);
    }
    _xsStringVectorDictSetLeft(dct, node, _xsStringVectorDictRemoveMin(dct, left));
    return (_xsStringVectorDictRebalance(dct, node));
}

int _xsStringVectorDictRemoveNode(int dct = -1, int node = -1, string key = "") {
    if (node < 0) {
        return (-1);
    }
    string storedKey = _xsStringVectorDictGetStoredKey(dct, node);
    if (key < storedKey) {
        _xsStringVectorDictSetLeft(dct, node, _xsStringVectorDictRemoveNode(dct, _xsStringVectorDictGetLeft(dct, node), key));
        return (_xsStringVectorDictRebalance(dct, node));
    }
    if (key > storedKey) {
        _xsStringVectorDictSetRight(dct, node, _xsStringVectorDictRemoveNode(dct, _xsStringVectorDictGetRight(dct, node), key));
        return (_xsStringVectorDictRebalance(dct, node));
    }
    int left = _xsStringVectorDictGetLeft(dct, node);
    int right = _xsStringVectorDictGetRight(dct, node);
    if (left < 0) {
        _xsStringVectorDictFreeNode(dct, node);
        return (right);
    }
    if (right < 0) {
        _xsStringVectorDictFreeNode(dct, node);
        return (left);
    }
    int successor = _xsStringVectorDictMinNode(dct, right);
    _xsStringVectorDictSetStoredKey(dct, node, _xsStringVectorDictGetStoredKey(dct, successor));
    _xsStringVectorDictSetStoredValue(dct, node, _xsStringVectorDictGetStoredValue(dct, successor));
    _xsStringVectorDictSetRight(dct, node, _xsStringVectorDictRemoveMin(dct, right));
    return (_xsStringVectorDictRebalance(dct, node));
}

int _xsStringVectorDictFindSuccessorNode(int dct = -1, string key = "") {
    int node = _xsStringVectorDictGetRoot(dct);
    int successor = -1;
    while (node >= 0) {
        string storedKey = _xsStringVectorDictGetStoredKey(dct, node);
        if (key < storedKey) {
            successor = node;
            node = _xsStringVectorDictGetLeft(dct, node);
        } else if (key > storedKey) {
            node = _xsStringVectorDictGetRight(dct, node);
        } else {
            int right = _xsStringVectorDictGetRight(dct, node);
            if (right >= 0) {
                return (_xsStringVectorDictMinNode(dct, right));
            }
            return (successor);
        }
    }
    return (-1);
}

int _xsStringVectorDictKeysFill(int dct = -1, int node = -1, int arr = -1, int idx = 0) {
    if (node < 0) {
        return (idx);
    }
    idx = _xsStringVectorDictKeysFill(dct, _xsStringVectorDictGetLeft(dct, node), arr, idx);
    xsArraySetString(arr, idx, _xsStringVectorDictGetStoredKey(dct, node));
    idx++;
    return (_xsStringVectorDictKeysFill(dct, _xsStringVectorDictGetRight(dct, node), arr, idx));
}

int _xsStringVectorDictValuesFill(int dct = -1, int node = -1, int arr = -1, int idx = 0) {
    if (node < 0) {
        return (idx);
    }
    idx = _xsStringVectorDictValuesFill(dct, _xsStringVectorDictGetLeft(dct, node), arr, idx);
    xsArraySetVector(arr, idx, _xsStringVectorDictGetStoredValue(dct, node));
    idx++;
    return (_xsStringVectorDictValuesFill(dct, _xsStringVectorDictGetRight(dct, node), arr, idx));
}

bool _xsStringVectorDictEqualsWalk(int a = -1, int b = -1, int node = -1) {
    if (node < 0) {
        return (true);
    }
    if (_xsStringVectorDictEqualsWalk(a, b, _xsStringVectorDictGetLeft(a, node)) == false) {
        return (false);
    }
    string key = _xsStringVectorDictGetStoredKey(a, node);
    vector val = _xsStringVectorDictGetStoredValue(a, node);
    int other = _xsStringVectorDictFindNode(b, key);
    if (other < 0) {
        return (false);
    }
    if (_xsStringVectorDictGetStoredValue(b, other) != val) {
        return (false);
    }
    return (_xsStringVectorDictEqualsWalk(a, b, _xsStringVectorDictGetRight(a, node)));
}

int _xsStringVectorDictUpdateWalk(int source = -1, int dct = -1, int node = -1) {
    if (node < 0) {
        return (cStringVectorDictSuccess);
    }
    int leftResult = _xsStringVectorDictUpdateWalk(source, dct, _xsStringVectorDictGetLeft(dct, node));
    if (leftResult != cStringVectorDictSuccess) {
        return (leftResult);
    }
    string key = _xsStringVectorDictGetStoredKey(dct, node);
    vector val = _xsStringVectorDictGetStoredValue(dct, node);
    int existing = _xsStringVectorDictFindNode(source, key);
    if (existing >= 0) {
        _xsStringVectorDictSetStoredValue(source, existing, val);
        _stringVectorDictLastOperationStatus = cStringVectorDictSuccess;
    } else {
        int size = xsArrayGetInt(source, 0);
        int resizeResult = _xsStringVectorDictEnsureCapacity(source, size + 1);
        if (resizeResult != cStringVectorDictSuccess) {
            _stringVectorDictLastOperationStatus = resizeResult;
            return (resizeResult);
        }
        _xsStringVectorDictSetRoot(source, _xsStringVectorDictInsertNode(source, _xsStringVectorDictGetRoot(source), key, val));
        xsArraySetInt(source, 0, size + 1);
        _stringVectorDictLastOperationStatus = cStringVectorDictNoKeyError;
    }
    return (_xsStringVectorDictUpdateWalk(source, dct, _xsStringVectorDictGetRight(dct, node)));
}

string _xsStringVectorDictToStringContents(int dct = -1, int node = -1) {
    if (node < 0) {
        return ("");
    }
    string left = _xsStringVectorDictToStringContents(dct, _xsStringVectorDictGetLeft(dct, node));
    string current = (("\"" + _xsStringVectorDictGetStoredKey(dct, node)) + "\": ") + ("" + _xsStringVectorDictGetStoredValue(dct, node));
    string combined = current;
    if (left != "") {
        combined = (left + ", ") + current;
    }
    string right = _xsStringVectorDictToStringContents(dct, _xsStringVectorDictGetRight(dct, node));
    if (right != "") {
        combined = combined + (", " + right);
    }
    return (combined);
}

/*
    Inserts or updates a key-value pair. Sets last error on completion.
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
    int existing = _xsStringVectorDictFindNode(dct, key);
    if (existing >= 0) {
        vector oldVal = _xsStringVectorDictGetStoredValue(dct, existing);
        _xsStringVectorDictSetStoredValue(dct, existing, val);
        _stringVectorDictLastOperationStatus = cStringVectorDictSuccess;
        return (oldVal);
    }
    int size = xsArrayGetInt(dct, 0);
    int r = _xsStringVectorDictEnsureCapacity(dct, size + 1);
    if (r != cStringVectorDictSuccess) {
        _stringVectorDictLastOperationStatus = r;
        return (cStringVectorDictGenericErrorVector);
    }
    _xsStringVectorDictSetRoot(dct, _xsStringVectorDictInsertNode(dct, _xsStringVectorDictGetRoot(dct), key, val));
    xsArraySetInt(dct, 0, size + 1);
    _stringVectorDictLastOperationStatus = cStringVectorDictNoKeyError;
    return (cStringVectorDictGenericErrorVector);
}

/*
    Creates a dict with provided key-value pairs. The first key that equals
    the reserved empty-key sentinel will stop further insertion.
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
    int node = _xsStringVectorDictFindNode(dct, key);
    if (node >= 0) {
        _stringVectorDictLastOperationStatus = cStringVectorDictSuccess;
        return (_xsStringVectorDictGetStoredValue(dct, node));
    }
    _stringVectorDictLastOperationStatus = cStringVectorDictNoKeyError;
    return (dft);
}

/*
    Removes the entry with the given key from the dict. Sets last error on completion.
*/
vector xsStringVectorDictRemove(int dct = -1, string key = "") {
    int node = _xsStringVectorDictFindNode(dct, key);
    if (node < 0) {
        _stringVectorDictLastOperationStatus = cStringVectorDictNoKeyError;
        return (cStringVectorDictGenericErrorVector);
    }
    vector oldVal = _xsStringVectorDictGetStoredValue(dct, node);
    _xsStringVectorDictSetRoot(dct, _xsStringVectorDictRemoveNode(dct, _xsStringVectorDictGetRoot(dct), key));
    xsArraySetInt(dct, 0, xsArrayGetInt(dct, 0) - 1);
    _stringVectorDictLastOperationStatus = cStringVectorDictSuccess;
    return (oldVal);
}

bool xsStringVectorDictContains(int dct = -1, string key = "") {
    return (_xsStringVectorDictFindNode(dct, key) >= 0);
}

int xsStringVectorDictSize(int dct = -1) {
    return (xsArrayGetInt(dct, 0));
}

/*
    Removes all entries from the dict and shrinks the backing arrays.
*/
int xsStringVectorDictClear(int dct = -1) {
    int targetCapacity = _xsStringVectorDictEffectiveInitialCapacity();
    int currentCapacity = _xsStringVectorDictCapacity(dct);
    if (currentCapacity > targetCapacity) {
        int oldKeysArr = _xsStringVectorDictGetKeysArray(dct);
        int newKeysArr = xsArrayCreateString(targetCapacity, "!<[empty");
        if (newKeysArr < 0) {
            return (cStringVectorDictGenericError);
        }
        int newValuesArr = xsArrayCreateFloat(targetCapacity * cStringVectorDictValueStride, 0.0);
        if (newValuesArr < 0) {
            xsArrayResizeString(newKeysArr, 0);
            return (cStringVectorDictGenericError);
        }
        int newDataSize = cStringVectorDictHeaderSize + (targetCapacity * cStringVectorDictNodeStride);
        int r = xsArrayResizeInt(dct, newDataSize);
        if (r != 1) {
            xsArrayResizeString(newKeysArr, 0);
            xsArrayResizeFloat(newValuesArr, 0);
            return (cStringVectorDictGenericError);
        }
        int oldValuesArr = _xsStringVectorDictGetValuesArray(dct);
        _xsStringVectorDictSetKeysArray(dct, newKeysArr);
        _xsStringVectorDictSetValuesArray(dct, newValuesArr);
        xsArrayResizeString(oldKeysArr, 0);
        xsArrayResizeFloat(oldValuesArr, 0);
        currentCapacity = targetCapacity;
    }
    xsArraySetInt(dct, 0, 0);
    _xsStringVectorDictSetRoot(dct, -1);
    _xsStringVectorDictSetFreeHead(dct, -1);
    if (currentCapacity > 0) {
        _xsStringVectorDictInitializeFreeNodes(dct, 0, currentCapacity, -1);
        _xsStringVectorDictSetFreeHead(dct, 0);
    }
    return (cStringVectorDictSuccess);
}

/*
    Returns a deep copy of the dict.
*/
int xsStringVectorDictCopy(int dct = -1) {
    int dataSize = xsArrayGetSize(dct);
    int capacity = _xsStringVectorDictCapacity(dct);
    int newDct = xsArrayCreateInt(dataSize, -1);
    if (newDct < 0) {
        return (cStringVectorDictResizeFailedError);
    }
    int newKeysArr = xsArrayCreateString(capacity, "!<[empty");
    if (newKeysArr < 0) {
        xsArrayResizeInt(newDct, 0);
        return (cStringVectorDictResizeFailedError);
    }
    int newValuesArr = xsArrayCreateFloat(capacity * cStringVectorDictValueStride, 0.0);
    if (newValuesArr < 0) {
        xsArrayResizeString(newKeysArr, 0);
        xsArrayResizeInt(newDct, 0);
        return (cStringVectorDictResizeFailedError);
    }
    for (i = 0; < dataSize) {
        xsArraySetInt(newDct, i, xsArrayGetInt(dct, i));
    }
    _xsStringVectorDictSetKeysArray(newDct, newKeysArr);
    _xsStringVectorDictSetValuesArray(newDct, newValuesArr);
    int keysArr = _xsStringVectorDictGetKeysArray(dct);
    for (j = 0; < capacity) {
        xsArraySetString(newKeysArr, j, xsArrayGetString(keysArr, j));
    }
    int valuesArr = _xsStringVectorDictGetValuesArray(dct);
    int valuesSize = capacity * cStringVectorDictValueStride;
    for (k = 0; < valuesSize) {
        xsArraySetFloat(newValuesArr, k, xsArrayGetFloat(valuesArr, k));
    }
    return (newDct);
}

/*
    Returns a string representation of the dict in the format `{"k1" - (x1, y1, z1), ...}`.
*/
string xsStringVectorDictToString(int dct = -1) {
    return (("{" + _xsStringVectorDictToStringContents(dct, _xsStringVectorDictGetRoot(dct))) + "}");
}

int xsStringVectorDictLastError() {
    return (_stringVectorDictLastOperationStatus);
}

/*
    Returns the next key in the dict for stateless iteration. Sets last error on completion.
*/
string xsStringVectorDictNextKey(int dct = -1, bool isFirst = true, string prevKey = "!<[empty") {
    int nextNode = -1;
    if (isFirst) {
        nextNode = _xsStringVectorDictMinNode(dct, _xsStringVectorDictGetRoot(dct));
    } else {
        int node = _xsStringVectorDictFindNode(dct, prevKey);
        if (node < 0) {
            _stringVectorDictLastOperationStatus = cStringVectorDictNoKeyError;
            return ("-1");
        }
        nextNode = _xsStringVectorDictFindSuccessorNode(dct, prevKey);
    }
    if (nextNode < 0) {
        _stringVectorDictLastOperationStatus = cStringVectorDictNoKeyError;
        return ("-1");
    }
    _stringVectorDictLastOperationStatus = cStringVectorDictSuccess;
    return (_xsStringVectorDictGetStoredKey(dct, nextNode));
}

bool xsStringVectorDictHasNext(int dct = -1, bool isFirst = true, string prevKey = "!<[empty") {
    if (isFirst) {
        return (_xsStringVectorDictGetRoot(dct) >= 0);
    }
    if (_xsStringVectorDictFindNode(dct, prevKey) < 0) {
        return (false);
    }
    return (_xsStringVectorDictFindSuccessorNode(dct, prevKey) >= 0);
}

/*
    Inserts all key-value pairs from another dict into the source dict, overwriting existing keys.
*/
int xsStringVectorDictUpdate(int source = -1, int dct = -1) {
    int result = _xsStringVectorDictUpdateWalk(source, dct, _xsStringVectorDictGetRoot(dct));
    if (result != cStringVectorDictSuccess) {
        return (result);
    }
    _stringVectorDictLastOperationStatus = cStringVectorDictSuccess;
    return (cStringVectorDictSuccess);
}

/*
    Inserts the key-value pair only if the key is not already present. Sets last error on completion.
    If `key` equals the reserved empty-key sentinel, the call is a no-op and returns
    `cStringVectorDictGenericErrorVector` with last error set to `cStringVectorDictGenericError`.
*/
vector xsStringVectorDictPutIfAbsent(int dct = -1, string key = "", vector val = vector(0.0, 0.0, 0.0)) {
    if (key == "!<[empty") {
        _stringVectorDictLastOperationStatus = cStringVectorDictGenericError;
        return (cStringVectorDictGenericErrorVector);
    }
    int existing = _xsStringVectorDictFindNode(dct, key);
    if (existing >= 0) {
        _stringVectorDictLastOperationStatus = cStringVectorDictSuccess;
        return (_xsStringVectorDictGetStoredValue(dct, existing));
    }
    int size = xsArrayGetInt(dct, 0);
    int r = _xsStringVectorDictEnsureCapacity(dct, size + 1);
    if (r != cStringVectorDictSuccess) {
        _stringVectorDictLastOperationStatus = r;
        return (cStringVectorDictGenericErrorVector);
    }
    _xsStringVectorDictSetRoot(dct, _xsStringVectorDictInsertNode(dct, _xsStringVectorDictGetRoot(dct), key, val));
    xsArraySetInt(dct, 0, size + 1);
    _stringVectorDictLastOperationStatus = cStringVectorDictNoKeyError;
    return (cStringVectorDictGenericErrorVector);
}

/*
    Returns a new string array containing all keys in the dict. Order is lexicographic.
*/
int xsStringVectorDictKeys(int dct = -1) {
    int size = xsArrayGetInt(dct, 0);
    int arr = xsArrayCreateString(size);
    if (arr < 0) {
        return (cStringVectorDictResizeFailedError);
    }
    _xsStringVectorDictKeysFill(dct, _xsStringVectorDictGetRoot(dct), arr);
    return (arr);
}

/*
    Returns a new vector array containing all values in the dict. Order matches `xsStringVectorDictKeys`.
*/
int xsStringVectorDictValues(int dct = -1) {
    int size = xsArrayGetInt(dct, 0);
    int arr = xsArrayCreateVector(size, vector(0.0, 0.0, 0.0));
    if (arr < 0) {
        return (cStringVectorDictResizeFailedError);
    }
    _xsStringVectorDictValuesFill(dct, _xsStringVectorDictGetRoot(dct), arr);
    return (arr);
}

/*
    Returns true if both dicts contain the same key-value pairs.
*/
bool xsStringVectorDictEquals(int a = -1, int b = -1) {
    if (xsArrayGetInt(a, 0) != xsArrayGetInt(b, 0)) {
        return (false);
    }
    return (_xsStringVectorDictEqualsWalk(a, b, _xsStringVectorDictGetRoot(a)));
}

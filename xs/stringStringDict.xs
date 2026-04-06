extern const int cStringStringDictSuccess = 0;
extern const int cStringStringDictGenericError = -1;
extern const int cStringStringDictNoKeyError = -2;
extern const int cStringStringDictResizeFailedError = -3;
extern const int cStringStringDictMaxCapacityError = -4;
extern const int cStringStringDictMaxCapacity = 333333331;
extern const int cStringStringDictInitialCapacity = 16;
extern const int cStringStringDictHeaderSize = 4;
extern const int cStringStringDictNodeStride = 3;
extern const int cStringStringDictStringStride = 2;
int _stringStringDictLastOperationStatus = cStringStringDictSuccess;

int _xsStringStringDictEffectiveInitialCapacity() {
    int capacity = cStringStringDictInitialCapacity;
    if (capacity > cStringStringDictMaxCapacity) {
        capacity = cStringStringDictMaxCapacity;
    }
    if (capacity < 0) {
        return (0);
    }
    return (capacity);
}

int _xsStringStringDictGetStringsArray(int dct = -1) {
    return (xsArrayGetInt(dct, 1));
}

void _xsStringStringDictSetStringsArray(int dct = -1, int arr = -1) {
    xsArraySetInt(dct, 1, arr);
}

int _xsStringStringDictGetRoot(int dct = -1) {
    return (xsArrayGetInt(dct, 2));
}

void _xsStringStringDictSetRoot(int dct = -1, int root = -1) {
    xsArraySetInt(dct, 2, root);
}

int _xsStringStringDictGetFreeHead(int dct = -1) {
    return (xsArrayGetInt(dct, 3));
}

void _xsStringStringDictSetFreeHead(int dct = -1, int head = -1) {
    xsArraySetInt(dct, 3, head);
}

int _xsStringStringDictCapacityFromDataSize(int dataSize = 0) {
    return ((dataSize - cStringStringDictHeaderSize) / cStringStringDictNodeStride);
}

int _xsStringStringDictCapacity(int dct = -1) {
    return (_xsStringStringDictCapacityFromDataSize(xsArrayGetSize(dct)));
}

int _xsStringStringDictNodeBase(int node = 0) {
    return (cStringStringDictHeaderSize + (node * cStringStringDictNodeStride));
}

int _xsStringStringDictLeftSlot(int node = 0) {
    return (_xsStringStringDictNodeBase(node));
}

int _xsStringStringDictRightSlot(int node = 0) {
    return (_xsStringStringDictNodeBase(node) + 1);
}

int _xsStringStringDictHeightSlot(int node = 0) {
    return (_xsStringStringDictNodeBase(node) + 2);
}

int _xsStringStringDictStringBase(int node = 0) {
    return (node * cStringStringDictStringStride);
}

int _xsStringStringDictKeySlot(int node = 0) {
    return (_xsStringStringDictStringBase(node));
}

int _xsStringStringDictValueSlot(int node = 0) {
    return (_xsStringStringDictStringBase(node) + 1);
}

string _xsStringStringDictGetStoredKey(int dct = -1, int node = 0) {
    return (xsArrayGetString(_xsStringStringDictGetStringsArray(dct), _xsStringStringDictKeySlot(node)));
}

void _xsStringStringDictSetStoredKey(int dct = -1, int node = 0, string key = "") {
    xsArraySetString(_xsStringStringDictGetStringsArray(dct), _xsStringStringDictKeySlot(node), key);
}

string _xsStringStringDictGetStoredValue(int dct = -1, int node = 0) {
    return (xsArrayGetString(_xsStringStringDictGetStringsArray(dct), _xsStringStringDictValueSlot(node)));
}

void _xsStringStringDictSetStoredValue(int dct = -1, int node = 0, string value = "") {
    xsArraySetString(_xsStringStringDictGetStringsArray(dct), _xsStringStringDictValueSlot(node), value);
}

int _xsStringStringDictGetLeft(int dct = -1, int node = 0) {
    return (xsArrayGetInt(dct, _xsStringStringDictLeftSlot(node)));
}

void _xsStringStringDictSetLeft(int dct = -1, int node = 0, int child = -1) {
    xsArraySetInt(dct, _xsStringStringDictLeftSlot(node), child);
}

int _xsStringStringDictGetRight(int dct = -1, int node = 0) {
    return (xsArrayGetInt(dct, _xsStringStringDictRightSlot(node)));
}

void _xsStringStringDictSetRight(int dct = -1, int node = 0, int child = -1) {
    xsArraySetInt(dct, _xsStringStringDictRightSlot(node), child);
}

int _xsStringStringDictGetHeightOrNext(int dct = -1, int node = 0) {
    return (xsArrayGetInt(dct, _xsStringStringDictHeightSlot(node)));
}

void _xsStringStringDictSetHeightOrNext(int dct = -1, int node = 0, int value = 0) {
    xsArraySetInt(dct, _xsStringStringDictHeightSlot(node), value);
}

void _xsStringStringDictInitializeFreeNodes(int dct = -1, int start = 0, int stop = 0, int nextHead = -1) {
    for (i = start; < stop) {
        _xsStringStringDictSetStoredKey(dct, i, "!<[empty");
        _xsStringStringDictSetStoredValue(dct, i, "");
        _xsStringStringDictSetLeft(dct, i, -1);
        _xsStringStringDictSetRight(dct, i, -1);
        int nextFree = nextHead;
        if ((i + 1) < stop) {
            nextFree = i + 1;
        }
        _xsStringStringDictSetHeightOrNext(dct, i, nextFree);
    }
}

/*
    Creates an empty string-to-string dictionary.
    Keys equal to `"!<[empty"` are reserved as the internal empty-key sentinel
    and cannot be stored. `put` and `putIfAbsent` silently reject them.
    @return created dict id, or `cStringStringDictGenericError` on error
*/
int xsStringStringDictCreate() {
    int capacity = _xsStringStringDictEffectiveInitialCapacity();
    int dataSize = cStringStringDictHeaderSize + (capacity * cStringStringDictNodeStride);
    int dct = xsArrayCreateInt(dataSize, -1);
    if (dct < 0) {
        return (cStringStringDictGenericError);
    }
    int stringsArr = xsArrayCreateString(capacity * cStringStringDictStringStride, "");
    if (stringsArr < 0) {
        xsArrayResizeInt(dct, 0);
        return (cStringStringDictGenericError);
    }
    xsArraySetInt(dct, 0, 0);
    _xsStringStringDictSetStringsArray(dct, stringsArr);
    _xsStringStringDictSetRoot(dct, -1);
    _xsStringStringDictSetFreeHead(dct, -1);
    if (capacity > 0) {
        _xsStringStringDictInitializeFreeNodes(dct, 0, capacity, -1);
        _xsStringStringDictSetFreeHead(dct, 0);
    }
    return (dct);
}

int _xsStringStringDictResize(int dct = -1, int newCapacity = 0) {
    int oldCapacity = _xsStringStringDictCapacity(dct);
    if (newCapacity <= oldCapacity) {
        return (cStringStringDictSuccess);
    }
    if (newCapacity > cStringStringDictMaxCapacity) {
        return (cStringStringDictMaxCapacityError);
    }
    int stringsArr = _xsStringStringDictGetStringsArray(dct);
    int newStringsSize = newCapacity * cStringStringDictStringStride;
    int rStrings = xsArrayResizeString(stringsArr, newStringsSize);
    if (rStrings != 1) {
        return (cStringStringDictResizeFailedError);
    }
    int oldFreeHead = _xsStringStringDictGetFreeHead(dct);
    int newDataSize = cStringStringDictHeaderSize + (newCapacity * cStringStringDictNodeStride);
    int r = xsArrayResizeInt(dct, newDataSize);
    if (r != 1) {
        return (cStringStringDictResizeFailedError);
    }
    _xsStringStringDictInitializeFreeNodes(dct, oldCapacity, newCapacity, oldFreeHead);
    _xsStringStringDictSetFreeHead(dct, oldCapacity);
    return (cStringStringDictSuccess);
}

int _xsStringStringDictEnsureCapacity(int dct = -1, int requiredSize = 0) {
    int capacity = _xsStringStringDictCapacity(dct);
    if (requiredSize <= capacity) {
        return (cStringStringDictSuccess);
    }
    if (requiredSize > cStringStringDictMaxCapacity) {
        return (cStringStringDictMaxCapacityError);
    }
    int newCapacity = capacity;
    if (newCapacity < 1) {
        newCapacity = 1;
    }
    while (newCapacity < requiredSize) {
        if (newCapacity > (cStringStringDictMaxCapacity / 2)) {
            newCapacity = cStringStringDictMaxCapacity;
        } else {
            newCapacity = newCapacity * 2;
        }
    }
    return (_xsStringStringDictResize(dct, newCapacity));
}

int _xsStringStringDictAllocateNode(int dct = -1, string key = "", string value = "") {
    int freeHead = _xsStringStringDictGetFreeHead(dct);
    if (freeHead < 0) {
        return (-1);
    }
    _xsStringStringDictSetFreeHead(dct, _xsStringStringDictGetHeightOrNext(dct, freeHead));
    _xsStringStringDictSetStoredKey(dct, freeHead, key);
    _xsStringStringDictSetStoredValue(dct, freeHead, value);
    _xsStringStringDictSetLeft(dct, freeHead, -1);
    _xsStringStringDictSetRight(dct, freeHead, -1);
    _xsStringStringDictSetHeightOrNext(dct, freeHead, 1);
    return (freeHead);
}

void _xsStringStringDictFreeNode(int dct = -1, int node = -1) {
    _xsStringStringDictSetStoredKey(dct, node, "!<[empty");
    _xsStringStringDictSetStoredValue(dct, node, "");
    _xsStringStringDictSetLeft(dct, node, -1);
    _xsStringStringDictSetRight(dct, node, -1);
    _xsStringStringDictSetHeightOrNext(dct, node, _xsStringStringDictGetFreeHead(dct));
    _xsStringStringDictSetFreeHead(dct, node);
}

int _xsStringStringDictHeight(int dct = -1, int node = -1) {
    if (node < 0) {
        return (0);
    }
    return (_xsStringStringDictGetHeightOrNext(dct, node));
}

void _xsStringStringDictRefreshHeight(int dct = -1, int node = -1) {
    int leftHeight = _xsStringStringDictHeight(dct, _xsStringStringDictGetLeft(dct, node));
    int rightHeight = _xsStringStringDictHeight(dct, _xsStringStringDictGetRight(dct, node));
    if (leftHeight > rightHeight) {
        _xsStringStringDictSetHeightOrNext(dct, node, leftHeight + 1);
    } else {
        _xsStringStringDictSetHeightOrNext(dct, node, rightHeight + 1);
    }
}

int _xsStringStringDictBalanceFactor(int dct = -1, int node = -1) {
    return (_xsStringStringDictHeight(dct, _xsStringStringDictGetLeft(dct, node)) - _xsStringStringDictHeight(dct, _xsStringStringDictGetRight(dct, node)));
}

int _xsStringStringDictRotateLeft(int dct = -1, int node = -1) {
    int newRoot = _xsStringStringDictGetRight(dct, node);
    int moved = _xsStringStringDictGetLeft(dct, newRoot);
    _xsStringStringDictSetRight(dct, node, moved);
    _xsStringStringDictSetLeft(dct, newRoot, node);
    _xsStringStringDictRefreshHeight(dct, node);
    _xsStringStringDictRefreshHeight(dct, newRoot);
    return (newRoot);
}

int _xsStringStringDictRotateRight(int dct = -1, int node = -1) {
    int newRoot = _xsStringStringDictGetLeft(dct, node);
    int moved = _xsStringStringDictGetRight(dct, newRoot);
    _xsStringStringDictSetLeft(dct, node, moved);
    _xsStringStringDictSetRight(dct, newRoot, node);
    _xsStringStringDictRefreshHeight(dct, node);
    _xsStringStringDictRefreshHeight(dct, newRoot);
    return (newRoot);
}

int _xsStringStringDictRebalance(int dct = -1, int node = -1) {
    _xsStringStringDictRefreshHeight(dct, node);
    int balance = _xsStringStringDictBalanceFactor(dct, node);
    if (balance > 1) {
        int left = _xsStringStringDictGetLeft(dct, node);
        if (_xsStringStringDictBalanceFactor(dct, left) < 0) {
            _xsStringStringDictSetLeft(dct, node, _xsStringStringDictRotateLeft(dct, left));
        }
        return (_xsStringStringDictRotateRight(dct, node));
    }
    if (balance < -1) {
        int right = _xsStringStringDictGetRight(dct, node);
        if (_xsStringStringDictBalanceFactor(dct, right) > 0) {
            _xsStringStringDictSetRight(dct, node, _xsStringStringDictRotateRight(dct, right));
        }
        return (_xsStringStringDictRotateLeft(dct, node));
    }
    return (node);
}

int _xsStringStringDictFindNode(int dct = -1, string key = "") {
    int node = _xsStringStringDictGetRoot(dct);
    while (node >= 0) {
        string storedKey = _xsStringStringDictGetStoredKey(dct, node);
        if (key == storedKey) {
            return (node);
        }
        if (key < storedKey) {
            node = _xsStringStringDictGetLeft(dct, node);
        } else {
            node = _xsStringStringDictGetRight(dct, node);
        }
    }
    return (-1);
}

int _xsStringStringDictInsertNode(int dct = -1, int node = -1, string key = "", string value = "") {
    if (node < 0) {
        return (_xsStringStringDictAllocateNode(dct, key, value));
    }
    string storedKey = _xsStringStringDictGetStoredKey(dct, node);
    if (key == storedKey) {
        _xsStringStringDictSetStoredValue(dct, node, value);
        return (node);
    }
    if (key < storedKey) {
        _xsStringStringDictSetLeft(dct, node, _xsStringStringDictInsertNode(dct, _xsStringStringDictGetLeft(dct, node), key, value));
    } else {
        _xsStringStringDictSetRight(dct, node, _xsStringStringDictInsertNode(dct, _xsStringStringDictGetRight(dct, node), key, value));
    }
    return (_xsStringStringDictRebalance(dct, node));
}

int _xsStringStringDictMinNode(int dct = -1, int node = -1) {
    int current = node;
    while (current >= 0) {
        int left = _xsStringStringDictGetLeft(dct, current);
        if (left < 0) {
            return (current);
        }
        current = left;
    }
    return (-1);
}

int _xsStringStringDictRemoveMin(int dct = -1, int node = -1) {
    int left = _xsStringStringDictGetLeft(dct, node);
    if (left < 0) {
        int right = _xsStringStringDictGetRight(dct, node);
        _xsStringStringDictFreeNode(dct, node);
        return (right);
    }
    _xsStringStringDictSetLeft(dct, node, _xsStringStringDictRemoveMin(dct, left));
    return (_xsStringStringDictRebalance(dct, node));
}

int _xsStringStringDictRemoveNode(int dct = -1, int node = -1, string key = "") {
    if (node < 0) {
        return (-1);
    }
    string storedKey = _xsStringStringDictGetStoredKey(dct, node);
    if (key < storedKey) {
        _xsStringStringDictSetLeft(dct, node, _xsStringStringDictRemoveNode(dct, _xsStringStringDictGetLeft(dct, node), key));
        return (_xsStringStringDictRebalance(dct, node));
    }
    if (key > storedKey) {
        _xsStringStringDictSetRight(dct, node, _xsStringStringDictRemoveNode(dct, _xsStringStringDictGetRight(dct, node), key));
        return (_xsStringStringDictRebalance(dct, node));
    }
    int left = _xsStringStringDictGetLeft(dct, node);
    int right = _xsStringStringDictGetRight(dct, node);
    if (left < 0) {
        _xsStringStringDictFreeNode(dct, node);
        return (right);
    }
    if (right < 0) {
        _xsStringStringDictFreeNode(dct, node);
        return (left);
    }
    int successor = _xsStringStringDictMinNode(dct, right);
    _xsStringStringDictSetStoredKey(dct, node, _xsStringStringDictGetStoredKey(dct, successor));
    _xsStringStringDictSetStoredValue(dct, node, _xsStringStringDictGetStoredValue(dct, successor));
    _xsStringStringDictSetRight(dct, node, _xsStringStringDictRemoveMin(dct, right));
    return (_xsStringStringDictRebalance(dct, node));
}

int _xsStringStringDictFindSuccessorNode(int dct = -1, string key = "") {
    int node = _xsStringStringDictGetRoot(dct);
    int successor = -1;
    while (node >= 0) {
        string storedKey = _xsStringStringDictGetStoredKey(dct, node);
        if (key < storedKey) {
            successor = node;
            node = _xsStringStringDictGetLeft(dct, node);
        } else if (key > storedKey) {
            node = _xsStringStringDictGetRight(dct, node);
        } else {
            int right = _xsStringStringDictGetRight(dct, node);
            if (right >= 0) {
                return (_xsStringStringDictMinNode(dct, right));
            }
            return (successor);
        }
    }
    return (-1);
}

int _xsStringStringDictKeysFill(int dct = -1, int node = -1, int arr = -1, int idx = 0) {
    if (node < 0) {
        return (idx);
    }
    idx = _xsStringStringDictKeysFill(dct, _xsStringStringDictGetLeft(dct, node), arr, idx);
    xsArraySetString(arr, idx, _xsStringStringDictGetStoredKey(dct, node));
    idx++;
    return (_xsStringStringDictKeysFill(dct, _xsStringStringDictGetRight(dct, node), arr, idx));
}

int _xsStringStringDictValuesFill(int dct = -1, int node = -1, int arr = -1, int idx = 0) {
    if (node < 0) {
        return (idx);
    }
    idx = _xsStringStringDictValuesFill(dct, _xsStringStringDictGetLeft(dct, node), arr, idx);
    xsArraySetString(arr, idx, _xsStringStringDictGetStoredValue(dct, node));
    idx++;
    return (_xsStringStringDictValuesFill(dct, _xsStringStringDictGetRight(dct, node), arr, idx));
}

bool _xsStringStringDictEqualsWalk(int a = -1, int b = -1, int node = -1) {
    if (node < 0) {
        return (true);
    }
    if (_xsStringStringDictEqualsWalk(a, b, _xsStringStringDictGetLeft(a, node)) == false) {
        return (false);
    }
    string key = _xsStringStringDictGetStoredKey(a, node);
    string val = _xsStringStringDictGetStoredValue(a, node);
    int other = _xsStringStringDictFindNode(b, key);
    if (other < 0) {
        return (false);
    }
    if (_xsStringStringDictGetStoredValue(b, other) != val) {
        return (false);
    }
    return (_xsStringStringDictEqualsWalk(a, b, _xsStringStringDictGetRight(a, node)));
}

int _xsStringStringDictUpdateWalk(int source = -1, int dct = -1, int node = -1) {
    if (node < 0) {
        return (cStringStringDictSuccess);
    }
    int leftResult = _xsStringStringDictUpdateWalk(source, dct, _xsStringStringDictGetLeft(dct, node));
    if (leftResult != cStringStringDictSuccess) {
        return (leftResult);
    }
    string key = _xsStringStringDictGetStoredKey(dct, node);
    string val = _xsStringStringDictGetStoredValue(dct, node);
    int existing = _xsStringStringDictFindNode(source, key);
    if (existing >= 0) {
        _xsStringStringDictSetStoredValue(source, existing, val);
        _stringStringDictLastOperationStatus = cStringStringDictSuccess;
    } else {
        int size = xsArrayGetInt(source, 0);
        int resizeResult = _xsStringStringDictEnsureCapacity(source, size + 1);
        if (resizeResult != cStringStringDictSuccess) {
            _stringStringDictLastOperationStatus = resizeResult;
            return (resizeResult);
        }
        _xsStringStringDictSetRoot(source, _xsStringStringDictInsertNode(source, _xsStringStringDictGetRoot(source), key, val));
        xsArraySetInt(source, 0, size + 1);
        _stringStringDictLastOperationStatus = cStringStringDictNoKeyError;
    }
    return (_xsStringStringDictUpdateWalk(source, dct, _xsStringStringDictGetRight(dct, node)));
}

string _xsStringStringDictToStringContents(int dct = -1, int node = -1) {
    if (node < 0) {
        return ("");
    }
    string left = _xsStringStringDictToStringContents(dct, _xsStringStringDictGetLeft(dct, node));
    string current = ((("\"" + _xsStringStringDictGetStoredKey(dct, node)) + "\": \"") + _xsStringStringDictGetStoredValue(dct, node)) + "\"";
    string combined = current;
    if (left != "") {
        combined = (left + ", ") + current;
    }
    string right = _xsStringStringDictToStringContents(dct, _xsStringStringDictGetRight(dct, node));
    if (right != "") {
        combined = combined + (", " + right);
    }
    return (combined);
}

/*
    Inserts or updates a key-value pair. Sets last error on completion.
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
    int existing = _xsStringStringDictFindNode(dct, key);
    if (existing >= 0) {
        string oldVal = _xsStringStringDictGetStoredValue(dct, existing);
        _xsStringStringDictSetStoredValue(dct, existing, val);
        _stringStringDictLastOperationStatus = cStringStringDictSuccess;
        return (oldVal);
    }
    int size = xsArrayGetInt(dct, 0);
    int r = _xsStringStringDictEnsureCapacity(dct, size + 1);
    if (r != cStringStringDictSuccess) {
        _stringStringDictLastOperationStatus = r;
        return ("-1");
    }
    _xsStringStringDictSetRoot(dct, _xsStringStringDictInsertNode(dct, _xsStringStringDictGetRoot(dct), key, val));
    xsArraySetInt(dct, 0, size + 1);
    _stringStringDictLastOperationStatus = cStringStringDictNoKeyError;
    return ("-1");
}

/*
    Creates a dict with provided key-value pairs. The first key that equals
    the reserved empty-key sentinel will stop further insertion.
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
    int node = _xsStringStringDictFindNode(dct, key);
    if (node >= 0) {
        _stringStringDictLastOperationStatus = cStringStringDictSuccess;
        return (_xsStringStringDictGetStoredValue(dct, node));
    }
    _stringStringDictLastOperationStatus = cStringStringDictNoKeyError;
    return (dft);
}

/*
    Removes the entry with the given key from the dict. Sets last error on completion.
*/
string xsStringStringDictRemove(int dct = -1, string key = "") {
    int node = _xsStringStringDictFindNode(dct, key);
    if (node < 0) {
        _stringStringDictLastOperationStatus = cStringStringDictNoKeyError;
        return ("-1");
    }
    string oldVal = _xsStringStringDictGetStoredValue(dct, node);
    _xsStringStringDictSetRoot(dct, _xsStringStringDictRemoveNode(dct, _xsStringStringDictGetRoot(dct), key));
    xsArraySetInt(dct, 0, xsArrayGetInt(dct, 0) - 1);
    _stringStringDictLastOperationStatus = cStringStringDictSuccess;
    return (oldVal);
}

bool xsStringStringDictContains(int dct = -1, string key = "") {
    return (_xsStringStringDictFindNode(dct, key) >= 0);
}

int xsStringStringDictSize(int dct = -1) {
    return (xsArrayGetInt(dct, 0));
}

/*
    Removes all entries from the dict and shrinks the backing arrays.
*/
int xsStringStringDictClear(int dct = -1) {
    int targetCapacity = _xsStringStringDictEffectiveInitialCapacity();
    int currentCapacity = _xsStringStringDictCapacity(dct);
    if (currentCapacity > targetCapacity) {
        int newStringsSize = targetCapacity * cStringStringDictStringStride;
        int oldStringsArr = _xsStringStringDictGetStringsArray(dct);
        int newStringsArr = xsArrayCreateString(newStringsSize, "");
        if (newStringsArr < 0) {
            return (cStringStringDictGenericError);
        }
        int newDataSize = cStringStringDictHeaderSize + (targetCapacity * cStringStringDictNodeStride);
        int r = xsArrayResizeInt(dct, newDataSize);
        if (r != 1) {
            xsArrayResizeString(newStringsArr, 0);
            return (cStringStringDictGenericError);
        }
        _xsStringStringDictSetStringsArray(dct, newStringsArr);
        xsArrayResizeString(oldStringsArr, 0);
        currentCapacity = targetCapacity;
    }
    xsArraySetInt(dct, 0, 0);
    _xsStringStringDictSetRoot(dct, -1);
    _xsStringStringDictSetFreeHead(dct, -1);
    if (currentCapacity > 0) {
        _xsStringStringDictInitializeFreeNodes(dct, 0, currentCapacity, -1);
        _xsStringStringDictSetFreeHead(dct, 0);
    }
    return (cStringStringDictSuccess);
}

/*
    Returns a deep copy of the dict.
*/
int xsStringStringDictCopy(int dct = -1) {
    int dataSize = xsArrayGetSize(dct);
    int capacity = _xsStringStringDictCapacity(dct);
    int newDct = xsArrayCreateInt(dataSize, -1);
    if (newDct < 0) {
        return (cStringStringDictResizeFailedError);
    }
    int newStringsArr = xsArrayCreateString(capacity * cStringStringDictStringStride, "");
    if (newStringsArr < 0) {
        xsArrayResizeInt(newDct, 0);
        return (cStringStringDictResizeFailedError);
    }
    for (i = 0; < dataSize) {
        xsArraySetInt(newDct, i, xsArrayGetInt(dct, i));
    }
    _xsStringStringDictSetStringsArray(newDct, newStringsArr);
    int stringsArr = _xsStringStringDictGetStringsArray(dct);
    for (i = 0; < capacity * cStringStringDictStringStride) {
        xsArraySetString(newStringsArr, i, xsArrayGetString(stringsArr, i));
    }
    return (newDct);
}

/*
    Returns a string representation of the dict in the format `{"k1" - "v1", "k2" - "v2", ...}`.
*/
string xsStringStringDictToString(int dct = -1) {
    return (("{" + _xsStringStringDictToStringContents(dct, _xsStringStringDictGetRoot(dct))) + "}");
}

int xsStringStringDictLastError() {
    return (_stringStringDictLastOperationStatus);
}

/*
    Returns the next key in the dict for stateless iteration. Sets last error on completion.
*/
string xsStringStringDictNextKey(int dct = -1, bool isFirst = true, string prevKey = "!<[empty") {
    int nextNode = -1;
    if (isFirst) {
        nextNode = _xsStringStringDictMinNode(dct, _xsStringStringDictGetRoot(dct));
    } else {
        int node = _xsStringStringDictFindNode(dct, prevKey);
        if (node < 0) {
            _stringStringDictLastOperationStatus = cStringStringDictNoKeyError;
            return ("-1");
        }
        nextNode = _xsStringStringDictFindSuccessorNode(dct, prevKey);
    }
    if (nextNode < 0) {
        _stringStringDictLastOperationStatus = cStringStringDictNoKeyError;
        return ("-1");
    }
    _stringStringDictLastOperationStatus = cStringStringDictSuccess;
    return (_xsStringStringDictGetStoredKey(dct, nextNode));
}

bool xsStringStringDictHasNext(int dct = -1, bool isFirst = true, string prevKey = "!<[empty") {
    if (isFirst) {
        return (_xsStringStringDictGetRoot(dct) >= 0);
    }
    if (_xsStringStringDictFindNode(dct, prevKey) < 0) {
        return (false);
    }
    return (_xsStringStringDictFindSuccessorNode(dct, prevKey) >= 0);
}

/*
    Inserts all key-value pairs from another dict into the source dict, overwriting existing keys.
*/
int xsStringStringDictUpdate(int source = -1, int dct = -1) {
    int result = _xsStringStringDictUpdateWalk(source, dct, _xsStringStringDictGetRoot(dct));
    if (result != cStringStringDictSuccess) {
        return (result);
    }
    _stringStringDictLastOperationStatus = cStringStringDictSuccess;
    return (cStringStringDictSuccess);
}

/*
    Inserts the key-value pair only if the key is not already present. Sets last error on completion.
    If `key` equals the reserved empty-key sentinel, the call is a no-op and returns
    `"-1"` with last error set to `cStringStringDictGenericError`.
*/
string xsStringStringDictPutIfAbsent(int dct = -1, string key = "", string val = "") {
    if (key == "!<[empty") {
        _stringStringDictLastOperationStatus = cStringStringDictGenericError;
        return ("-1");
    }
    int existing = _xsStringStringDictFindNode(dct, key);
    if (existing >= 0) {
        _stringStringDictLastOperationStatus = cStringStringDictSuccess;
        return (_xsStringStringDictGetStoredValue(dct, existing));
    }
    int size = xsArrayGetInt(dct, 0);
    int r = _xsStringStringDictEnsureCapacity(dct, size + 1);
    if (r != cStringStringDictSuccess) {
        _stringStringDictLastOperationStatus = r;
        return ("-1");
    }
    _xsStringStringDictSetRoot(dct, _xsStringStringDictInsertNode(dct, _xsStringStringDictGetRoot(dct), key, val));
    xsArraySetInt(dct, 0, size + 1);
    _stringStringDictLastOperationStatus = cStringStringDictNoKeyError;
    return ("-1");
}

/*
    Returns a new string array containing all keys in the dict. Order is lexicographic.
*/
int xsStringStringDictKeys(int dct = -1) {
    int size = xsArrayGetInt(dct, 0);
    int arr = xsArrayCreateString(size);
    if (arr < 0) {
        return (cStringStringDictResizeFailedError);
    }
    _xsStringStringDictKeysFill(dct, _xsStringStringDictGetRoot(dct), arr);
    return (arr);
}

/*
    Returns a new string array containing all values in the dict. Order matches `xsStringStringDictKeys`.
*/
int xsStringStringDictValues(int dct = -1) {
    int size = xsArrayGetInt(dct, 0);
    int arr = xsArrayCreateString(size);
    if (arr < 0) {
        return (cStringStringDictResizeFailedError);
    }
    _xsStringStringDictValuesFill(dct, _xsStringStringDictGetRoot(dct), arr);
    return (arr);
}

/*
    Returns true if both dicts contain the same key-value pairs.
*/
bool xsStringStringDictEquals(int a = -1, int b = -1) {
    if (xsArrayGetInt(a, 0) != xsArrayGetInt(b, 0)) {
        return (false);
    }
    return (_xsStringStringDictEqualsWalk(a, b, _xsStringStringDictGetRoot(a)));
}

extern const int cStringListSuccess = 0;
extern const int cStringListGenericError = -1;
extern const int cStringListIndexOutOfRangeError = -2;
extern const int cStringListResizeFailedError = -3;
extern const int cStringListMaxCapacityError = -4;
extern const int cStringListMaxCapacity = 999999999;
extern const int cStringListEmptyIntParam = -999999999;
int _intListLastOperationStatus = cStringListSuccess;

int xsStringListSize(int lst = -1) {
    return (xsArrayGetInt(lst, 0));
}

/*
    Creates a list with provided values. The first value that equals `cStringListEmptyParam` will stop further insertion.
    This Function can create a list with 12 values at the maximum, but further values can be added with other functions.
    @param v1 through v11 - value at a given index of a list
    @return created list id, or error if negative
*/
int xsStringList(string v0 = "!<[empty", string v1 = "!<[empty", string v2 = "!<[empty", string v3 = "!<[empty", string v4 = "!<[empty", string v5 = "!<[empty", string v6 = "!<[empty", string v7 = "!<[empty", string v8 = "!<[empty", string v9 = "!<[empty", string v10 = "!<[empty", string v11 = "!<[empty") {
    int strLst = xsArrayCreateString(12);
    int lst = xsArrayCreateInt(2, strLst);
    if ((strLst < 0) || (lst < 0)) {
        return (cStringListGenericError);
    }
    if (v0 == "!<[empty") {
        xsArraySetInt(lst, 0, 0);
        return (lst);
    }
    xsArraySetString(strLst, 0, v0);
    if (v1 == "!<[empty") {
        xsArraySetInt(lst, 0, 1);
        return (lst);
    }
    xsArraySetString(strLst, 1, v1);
    if (v2 == "!<[empty") {
        xsArraySetInt(lst, 0, 2);
        return (lst);
    }
    xsArraySetString(strLst, 2, v2);
    if (v3 == "!<[empty") {
        xsArraySetInt(lst, 0, 3);
        return (lst);
    }
    xsArraySetString(strLst, 3, v3);
    if (v4 == "!<[empty") {
        xsArraySetInt(lst, 0, 4);
        return (lst);
    }
    xsArraySetString(strLst, 4, v4);
    if (v5 == "!<[empty") {
        xsArraySetInt(lst, 0, 5);
        return (lst);
    }
    xsArraySetString(strLst, 5, v5);
    if (v6 == "!<[empty") {
        xsArraySetInt(lst, 0, 6);
        return (lst);
    }
    xsArraySetString(strLst, 6, v6);
    if (v7 == "!<[empty") {
        xsArraySetInt(lst, 0, 7);
        return (lst);
    }
    xsArraySetString(strLst, 7, v7);
    if (v8 == "!<[empty") {
        xsArraySetInt(lst, 0, 8);
        return (lst);
    }
    xsArraySetString(strLst, 8, v8);
    if (v9 == "!<[empty") {
        xsArraySetInt(lst, 0, 9);
        return (lst);
    }
    xsArraySetString(strLst, 9, v9);
    if (v10 == "!<[empty") {
        xsArraySetInt(lst, 0, 10);
        return (lst);
    }
    xsArraySetString(strLst, 10, v10);
    if (v11 == "!<[empty") {
        xsArraySetInt(lst, 0, 11);
        return (lst);
    }
    xsArraySetString(strLst, 11, v11);
    xsArraySetInt(lst, 0, 12);
    return (lst);
}

/*
    Creates empty list for string values. List is a dynamic array that grows and shrinks as values are added and removed.
    @param capacity - initial list capacity
    @return created list id, or error if negative
*/
int xsStringListCreate(int capacity = 7) {
    if ((capacity < 0) || (capacity >= cStringListMaxCapacity)) {
        return (cStringListGenericError);
    }
    int lst = xsArrayCreateInt(2, 0);
    int strLst = xsArrayCreateString(capacity);
    if ((lst < 0) || (strLst < 0)) {
        return (cStringListGenericError);
    }
    xsArraySetInt(lst, 1, strLst);
    return (lst);
}

int xsStringListFromRepeatedVal(string value = "", int times = 0) {
    if ((times < 0) || (times > cStringListMaxCapacity)) {
        return (cStringListGenericError);
    }
    int lst = xsArrayCreateInt(2, times);
    int strLst = xsArrayCreateString(times, value);
    if ((strLst < 0) || (lst < 0)) {
        return (cStringListGenericError);
    }
    xsArraySetInt(lst, 1, strLst);
    return (lst);
}

int xsStringListFromRepeatedList(int lst = -1, int times = 0) {
    int size = xsArrayGetInt(lst, 0);
    int newCapacity = size * times;
    if (newCapacity > cStringListMaxCapacity) {
        return (cStringListGenericError);
    }
    int newStrLst = xsArrayCreateString(newCapacity);
    int newLst = xsArrayCreateInt(2, newCapacity);
    if ((newStrLst < 0) || (newLst < 0)) {
        return (cStringListGenericError);
    }
    int strLst = xsArrayGetInt(lst, 1);
    for (i = 0; < size) {
        string val = xsArrayGetString(strLst, i);
        int j = i;
        while (j < newCapacity) {
            xsArraySetString(newStrLst, j, val);
            j = j + size;
        }
    }
    xsArraySetInt(newLst, 1, newStrLst);
    return (newLst);
}

int xsStringListFromArray(int arr = -1) {
    int arrSize = xsArrayGetSize(arr);
    if (arrSize > cStringListMaxCapacity) {
        return (cStringListMaxCapacityError);
    }
    int newStrLst = xsArrayCreateString(arrSize);
    int lst = xsArrayCreateInt(2, arrSize);
    if ((lst < 0) || (newStrLst < 0)) {
        return (cStringListGenericError);
    }
    for (i = 0; < arrSize) {
        xsArraySetString(newStrLst, i, xsArrayGetString(arr, i));
    }
    xsArraySetInt(lst, 1, newStrLst);
    return (lst);
}

int xsStringListUseArrayAsSource(int arr = -1) {
    int arrSize = xsArrayGetSize(arr);
    if (arrSize > cStringListMaxCapacity) {
        return (cStringListMaxCapacityError);
    }
    int lst = xsArrayCreateInt(2, arrSize);
    if (lst < 0) {
        return (cStringListGenericError);
    }
    xsArraySetInt(lst, 1, arr);
    return (lst);
}

string xsStringListGet(int lst = -1, int idx = -1) {
    int size = xsStringListSize(lst);
    if ((idx < 0) || (idx >= size)) {
        _intListLastOperationStatus = cStringListIndexOutOfRangeError;
        return ("" + cStringListGenericError);
    }
    _intListLastOperationStatus = cStringListSuccess;
    return (xsArrayGetString(xsArrayGetInt(lst, 1), idx));
}

int xsStringListSet(int lst = -1, int idx = -1, string value = "") {
    int size = xsArrayGetInt(lst, 0);
    if ((idx < 0) || (idx >= size)) {
        return (cStringListIndexOutOfRangeError);
    }
    xsArraySetString(xsArrayGetInt(lst, 1), idx, value);
    return (cStringListSuccess);
}

int _xsStringListExtendStringArray(int lst = -1, int capacity = 0) {
    if (capacity == cStringListMaxCapacity) {
        return (cStringListMaxCapacityError);
    }
    int newCapacity = capacity * 2;
    if (newCapacity > cStringListMaxCapacity) {
        newCapacity = cStringListMaxCapacity;
    }
    if (newCapacity == 0) {
        newCapacity = 8;
    }
    int r = xsArrayResizeString(lst, newCapacity);
    if (r != 1) {
        return (cStringListResizeFailedError);
    }
    return (cStringListSuccess);
}

int _xsStringListShrinkStringArray(int lst = -1, int size = 0, int capacity = 0) {
    if (size <= (capacity / 2)) {
        int r = xsArrayResizeString(lst, size);
        if (r != 1) {
            return (cStringListResizeFailedError);
        }
    }
    return (cStringListSuccess);
}

string xsStringListToString(int lst = -1) {
    int size = xsArrayGetInt(lst, 0);
    int strLst = xsArrayGetInt(lst, 1);
    if (size == 0) {
        return ("[]");
    }
    string s = "[\"";
    for (i = 0; < size) {
        s = s + xsArrayGetString(strLst, i);
        if (i < (size - 1)) {
            s = s + "\", \"";
        } else {
            s = s + "\"";
        }
    }
    s = s + "]";
    return (s);
}

int xsStringListAppend(int lst = -1, string value = "") {
    int strLst = xsArrayGetInt(lst, 1);
    int capacity = xsArrayGetSize(strLst);
    int size = xsArrayGetInt(lst, 0);
    if (capacity == size) {
        int r = _xsStringListExtendStringArray(strLst, capacity);
        if (r != cStringListSuccess) {
            return (r);
        }
    }
    xsArraySetString(strLst, size, value);
    xsArraySetInt(lst, 0, size + 1);
    return (cStringListSuccess);
}

string xsStringListPop(int lst = -1, int idx = cStringListMaxCapacity) {
    int strLst = xsArrayGetInt(lst, 1);
    int capacity = xsArrayGetSize(strLst);
    int size = xsArrayGetInt(lst, 0);
    if (idx == cStringListMaxCapacity) {
        idx = size - 1;
    } else if ((idx < 0) || (idx >= size)) {
        _intListLastOperationStatus = cStringListIndexOutOfRangeError;
        return ("" + cStringListGenericError);
    }
    string removedElem = xsArrayGetString(strLst, idx);
    for (i = idx; < size - 1) {
        xsArraySetString(strLst, i, xsArrayGetString(strLst, i + 1));
    }
    int r = _xsStringListShrinkStringArray(strLst, size, capacity);
    if (r != cStringListSuccess) {
        _intListLastOperationStatus = r;
        return ("" + cStringListGenericError);
    }
    xsArraySetInt(lst, 0, size - 1);
    _intListLastOperationStatus = cStringListSuccess;
    return (removedElem);
}

int xsStringListInsert(int lst = -1, int idx = -1, string value = "") {
    int size = xsArrayGetInt(lst, 0);
    if ((idx < 0) || (idx > size)) {
        return (cStringListIndexOutOfRangeError);
    }
    int newSize = size + 1;
    int strLst = xsArrayGetInt(lst, 1);
    int capacity = xsArrayGetSize(strLst);
    if (capacity < newSize) {
        int r = _xsStringListExtendStringArray(strLst, capacity);
        if (r != cStringListSuccess) {
            return (r);
        }
    }
    for (i = newSize; > idx) {
        xsArraySetString(strLst, i, xsArrayGetString(strLst, i - 1));
    }
    xsArraySetString(strLst, idx, value);
    xsArraySetInt(lst, 0, newSize);
    return (cStringListSuccess);
}

int xsStringListRemove(int lst = -1, string value = "") {
    int strLst = xsArrayGetInt(lst, 1);
    int size = xsArrayGetInt(lst, 0);
    int foundIdx = -1;
    int i = 0;
    while ((i < size) && (foundIdx == -1)) {
        string cVal = xsArrayGetString(strLst, i);
        if (cVal == value) {
            foundIdx = i;
        }
        i++;
    }
    if (foundIdx == -1) {
        return (cStringListGenericError);
    }
    int newSize = size - 1;
    for (j = foundIdx; < newSize) {
        xsArraySetString(strLst, j, xsArrayGetString(strLst, j + 1));
    }
    int capacity = xsArrayGetSize(strLst);
    int r = _xsStringListShrinkStringArray(strLst, size, capacity);
    if (r != cStringListSuccess) {
        return (r);
    }
    xsArraySetInt(lst, 0, newSize);
    return (foundIdx);
}

int xsStringListIndex(int lst = -1, string value = "", int start = 0, int stop = cStringListEmptyIntParam) {
    int size = xsArrayGetInt(lst, 0);
    int strLst = xsArrayGetInt(lst, 1);
    if ((stop == cStringListEmptyIntParam) || (stop > size)) {
        stop = size;
    }
    if (start < 0) {
        start = start + size;
    }
    if (stop < 0) {
        stop = stop + size;
    }
    if (start < 0) {
        start = 0;
    }
    if (stop > size) {
        stop = size;
    }
    for (i = start; < stop) {
        if (xsArrayGetString(strLst, i) == value) {
            return (i);
        }
    }
    return (cStringListGenericError);
}

bool xsStringListContains(int lst = -1, string value = "") {
    return (xsStringListIndex(lst, value) > -1);
}

bool _xsStringListCompareElem(string a = "", string b = "", bool reverse = false) {
    if (reverse) {
        return (a > b);
    }
    return (a < b);
}

void _xsStringListSiftDown(int lst = -1, int start = -1, int end = -1, bool reverse = false) {
    int root = start;
    while (true) {
        int child = (2 * root) + 1;
        if (child > end) {
            return;
        }
        string childVal = xsArrayGetString(lst, child);
        string childVal1 = xsArrayGetString(lst, child + 1);
        if (((child + 1) <= end) && _xsStringListCompareElem(childVal, childVal1, reverse)) {
            child++;
            childVal = childVal1;
        }
        string rootVal = xsArrayGetString(lst, root);
        if (_xsStringListCompareElem(rootVal, childVal, reverse)) {
            xsArraySetString(lst, root, childVal);
            xsArraySetString(lst, child, rootVal);
            root = child;
        } else {
            return;
        }
    }
}

void xsStringListSort(int lst = -1, bool reverse = false) {
    int size = xsArrayGetInt(lst, 0);
    int strLst = xsArrayGetInt(lst, 1);
    for (start = (size / 2) - 1; > -1) {
        _xsStringListSiftDown(strLst, start, size - 1, reverse);
    }
    for (end = size - 1; > 0) {
        string temp = xsArrayGetString(strLst, 0);
        xsArraySetString(strLst, 0, xsArrayGetString(strLst, end));
        xsArraySetString(strLst, end, temp);
        _xsStringListSiftDown(strLst, 0, end - 1, reverse);
    }
}

int xsStringListClear(int lst = -1) {
    int strList = xsArrayGetInt(lst, 1);
    int capacity = xsArrayGetSize(strList);
    if (capacity > 8) {
        int r = xsArrayResizeString(strList, 8);
        if (r != 1) {
            return (cStringListResizeFailedError);
        }
    }
    xsArraySetInt(lst, 0, 0);
    return (cStringListSuccess);
}

int xsStringListCopy(int lst = -1, int start = 0, int end = cStringListMaxCapacity) {
    int size = xsArrayGetInt(lst, 0);
    int fr = 0;
    if (start < 0) {
        fr = size + start;
    } else {
        fr = start;
    }
    int to = 0;
    if (end < 0) {
        to = size + end;
    } else {
        to = end;
    }
    if (fr < 0) {
        fr = 0;
    }
    if (to > size) {
        to = size;
    }
    int newSize = to - fr;
    if (newSize < 0) {
        newSize = 0;
    }
    int newLst = xsArrayCreateInt(2, newSize);
    int newStrLst = xsArrayCreateString(newSize);
    if ((newLst < 0) || (newStrLst < 0)) {
        return (cStringListGenericError);
    }
    xsArraySetInt(newLst, 1, newStrLst);
    int strLst = xsArrayGetInt(lst, 1);
    for (i = fr; < to) {
        xsArraySetString(newStrLst, i - fr, xsArrayGetString(strLst, i));
    }
    return (newLst);
}

int xsStringListExtend(int source = -1, int lst = -1) {
    int sourceSize = xsArrayGetInt(source, 0);
    int toAdd = xsArrayGetInt(lst, 0);
    int strSource = xsArrayGetInt(source, 1);
    int capacity = xsArrayGetSize(strSource);
    int newSize = sourceSize + toAdd;
    if (newSize > capacity) {
        if (newSize > cStringListMaxCapacity) {
            return (cStringListMaxCapacityError);
        }
        int r = xsArrayResizeString(strSource, newSize);
        if (r != 1) {
            return (cStringListResizeFailedError);
        }
    }
    int strList = xsArrayGetInt(lst, 1);
    for (i = 0; < toAdd) {
        xsArraySetString(strSource, i + sourceSize, xsArrayGetString(strList, i));
    }
    xsArraySetInt(source, 0, newSize);
    return (cStringListSuccess);
}

int xsStringListExtendWithArray(int source = -1, int arr = -1) {
    int sourceSize = xsArrayGetInt(source, 0);
    int toAdd = xsArrayGetSize(arr);
    int strSource = xsArrayGetInt(source, 1);
    int capacity = xsArrayGetSize(strSource);
    int newSize = sourceSize + toAdd;
    if (newSize > capacity) {
        if ((newSize > cStringListMaxCapacity) || (newSize < 0)) {
            return (cStringListMaxCapacityError);
        }
        int r = xsArrayResizeString(strSource, newSize);
        if (r != 1) {
            return (cStringListResizeFailedError);
        }
    }
    for (i = 0; < toAdd) {
        xsArraySetString(strSource, i + sourceSize, xsArrayGetString(arr, i));
    }
    xsArraySetInt(source, 0, newSize);
    return (cStringListSuccess);
}

int xsStringListCompare(int lst1 = -1, int lst2 = -1) {
    int size1 = xsArrayGetInt(lst1, 0);
    int size2 = xsArrayGetInt(lst2, 0);
    int strList1 = xsArrayGetInt(lst1, 1);
    int strList2 = xsArrayGetInt(lst2, 1);
    int i = 0;
    while ((i < size1) && (i < size2)) {
        string v1 = xsArrayGetString(strList1, i);
        string v2 = xsArrayGetString(strList2, i);
        if (v1 < v2) {
            return (-1);
        }
        if (v1 > v2) {
            return (1);
        }
        i++;
    }
    if (size1 < size2) {
        return (-1);
    }
    if (size1 > size2) {
        return (1);
    }
    return (0);
}

int xsStringListCount(int lst = -1, string value = "") {
    int count = 0;
    int size = xsArrayGetInt(lst, 0);
    int strList = xsArrayGetInt(lst, 1);
    for (i = 0; < size) {
        if (xsArrayGetString(strList, i) == value) {
            count++;
        }
    }
    return (count);
}

string xsStringListMin(int lst = -1) {
    int size = xsArrayGetInt(lst, 0);
    if (size == 0) {
        _intListLastOperationStatus = cStringListIndexOutOfRangeError;
        return ("" + cStringListGenericError);
    }
    int strList = xsArrayGetInt(lst, 1);
    string m = xsArrayGetString(strList, 0);
    if (size == 1) {
        _intListLastOperationStatus = cStringListSuccess;
        return (m);
    }
    for (i = 1; < size) {
        string v = xsArrayGetString(strList, i);
        if (v < m) {
            m = v;
        }
    }
    _intListLastOperationStatus = cStringListSuccess;
    return (m);
}

string xsStringListMax(int lst = -1) {
    int size = xsArrayGetInt(lst, 0);
    if (size == 0) {
        _intListLastOperationStatus = cStringListIndexOutOfRangeError;
        return ("" + cStringListGenericError);
    }
    int strList = xsArrayGetInt(lst, 1);
    string m = xsArrayGetString(strList, 0);
    if (size == 1) {
        _intListLastOperationStatus = cStringListSuccess;
        return (m);
    }
    for (i = 1; < size) {
        string v = xsArrayGetString(strList, i);
        if (v > m) {
            m = v;
        }
    }
    _intListLastOperationStatus = cStringListSuccess;
    return (m);
}

int xsStringListLastError() {
    return (_intListLastOperationStatus);
}

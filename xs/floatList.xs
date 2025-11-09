extern const int cFloatListSuccess = 0;
extern const int cFloatListGenericError = -1;
extern const float cFloatListGenericErrorFloat = -1.0;
extern const int cFloatListIndexOutOfRangeError = -2;
extern const int cFloatListResizeFailedError = -3;
extern const int cFloatListMaxCapacityError = -4;
extern const int cFloatListMaxCapacity = 999999999;
extern const float cFloatListEmptyParam = -9999999.0;
extern const int cFloatListEmptyIntParam = -999999999;
int _floatListLastOperationStatus = cFloatListSuccess;

int xsFloatListSize(int lst = -1) {
    return (bitCastToInt(xsArrayGetFloat(lst, 0)));
}

void _xsFloatListSetSize(int lst = -1, int size = 0) {
    xsArraySetFloat(lst, 0, bitCastToFloat(size));
}

/*
    Creates a list with provided values. The first value that equals `cFloatListEmptyParam` will stop further insertion.
    This Function can create a list with 12 values at the maximum, but further values can be added with other functions.
    @param v1 through v11 - value at a given index of a list
    @return created list id, or error if negative
*/
int xsFloatList(float v0 = cFloatListEmptyParam, float v1 = cFloatListEmptyParam, float v2 = cFloatListEmptyParam, float v3 = cFloatListEmptyParam, float v4 = cFloatListEmptyParam, float v5 = cFloatListEmptyParam, float v6 = cFloatListEmptyParam, float v7 = cFloatListEmptyParam, float v8 = cFloatListEmptyParam, float v9 = cFloatListEmptyParam, float v10 = cFloatListEmptyParam, float v11 = cFloatListEmptyParam) {
    int lst = xsArrayCreateFloat(13);
    if (lst < 0) {
        return (cFloatListGenericError);
    }
    if (v0 == cFloatListEmptyParam) {
        _xsFloatListSetSize(lst, 0);
        return (lst);
    }
    xsArraySetFloat(lst, 1, v0);
    if (v1 == cFloatListEmptyParam) {
        _xsFloatListSetSize(lst, 1);
        return (lst);
    }
    xsArraySetFloat(lst, 2, v1);
    if (v2 == cFloatListEmptyParam) {
        _xsFloatListSetSize(lst, 2);
        return (lst);
    }
    xsArraySetFloat(lst, 3, v2);
    if (v3 == cFloatListEmptyParam) {
        _xsFloatListSetSize(lst, 3);
        return (lst);
    }
    xsArraySetFloat(lst, 4, v3);
    if (v4 == cFloatListEmptyParam) {
        _xsFloatListSetSize(lst, 4);
        return (lst);
    }
    xsArraySetFloat(lst, 5, v4);
    if (v5 == cFloatListEmptyParam) {
        _xsFloatListSetSize(lst, 5);
        return (lst);
    }
    xsArraySetFloat(lst, 6, v5);
    if (v6 == cFloatListEmptyParam) {
        _xsFloatListSetSize(lst, 6);
        return (lst);
    }
    xsArraySetFloat(lst, 7, v6);
    if (v7 == cFloatListEmptyParam) {
        _xsFloatListSetSize(lst, 7);
        return (lst);
    }
    xsArraySetFloat(lst, 8, v7);
    if (v8 == cFloatListEmptyParam) {
        _xsFloatListSetSize(lst, 8);
        return (lst);
    }
    xsArraySetFloat(lst, 9, v8);
    if (v9 == cFloatListEmptyParam) {
        _xsFloatListSetSize(lst, 9);
        return (lst);
    }
    xsArraySetFloat(lst, 10, v9);
    if (v10 == cFloatListEmptyParam) {
        _xsFloatListSetSize(lst, 10);
        return (lst);
    }
    xsArraySetFloat(lst, 11, v10);
    if (v11 == cFloatListEmptyParam) {
        _xsFloatListSetSize(lst, 11);
        return (lst);
    }
    xsArraySetFloat(lst, 12, v11);
    _xsFloatListSetSize(lst, 12);
    return (lst);
}

/*
    Creates empty list for float values. List is a dynamic array that grows and shrinks as values are added and removed.
    @param capacity - initial list capacity
    @return created list id, or error if negative
*/
int xsFloatListCreate(int capacity = 7) {
    if ((capacity < 0) || (capacity >= cFloatListMaxCapacity)) {
        return (cFloatListGenericError);
    }
    int lst = xsArrayCreateFloat(capacity + 1);
    if (lst < 0) {
        return (cFloatListGenericError);
    }
    _xsFloatListSetSize(lst, 0);
    return (lst);
}

int xsFloatListFromRepeatedVal(float value = 0.0, int times = 0) {
    if ((times < 0) || (times >= cFloatListMaxCapacity)) {
        return (cFloatListGenericError);
    }
    int lst = xsArrayCreateFloat(times + 1, value);
    if (lst < 0) {
        return (cFloatListGenericError);
    }
    _xsFloatListSetSize(lst, times);
    return (lst);
}

int xsFloatListFromRepeatedList(int lst = -1, int times = 0) {
    int size = xsFloatListSize(lst);
    int newCapacity = (size * times) + 1;
    if (newCapacity > cFloatListMaxCapacity) {
        return (cFloatListGenericError);
    }
    int newLst = xsArrayCreateFloat(newCapacity);
    if (newLst < 0) {
        return (cFloatListGenericError);
    }
    for (i = 1; <= size) {
        float val = xsArrayGetFloat(lst, i);
        int j = i;
        while (j < newCapacity) {
            xsArraySetFloat(newLst, j, val);
            j = j + size;
        }
    }
    _xsFloatListSetSize(newLst, newCapacity - 1);
    return (newLst);
}

int xsFloatListFromArray(int arr = -1) {
    int arrSize = xsArrayGetSize(arr);
    int lst = xsFloatListCreate(arrSize);
    if (lst < 0) {
        return (lst);
    }
    for (i = 0; < arrSize) {
        xsArraySetFloat(lst, i + 1, xsArrayGetFloat(arr, i));
    }
    _xsFloatListSetSize(lst, arrSize);
    return (lst);
}

int xsFloatListUseArrayAsSource(int arr = -1) {
    int arrSize = xsArrayGetSize(arr);
    if ((arrSize + 1) > cFloatListMaxCapacity) {
        return (cFloatListMaxCapacityError);
    }
    int r = xsArrayResizeFloat(arr, arrSize + 1);
    if (r < 0) {
        return (cFloatListResizeFailedError);
    }
    for (i = arrSize - 1; > -1) {
        xsArraySetFloat(arr, i + 1, xsArrayGetFloat(arr, i));
    }
    _xsFloatListSetSize(arr, arrSize);
    return (arr);
}

float xsFloatListGet(int lst = -1, int idx = -1) {
    int size = xsFloatListSize(lst);
    if ((idx < 0) || (idx >= size)) {
        _floatListLastOperationStatus = cFloatListIndexOutOfRangeError;
        return (cFloatListGenericErrorFloat);
    }
    _floatListLastOperationStatus = cFloatListSuccess;
    return (xsArrayGetFloat(lst, idx + 1));
}

int xsFloatListSet(int lst = -1, int idx = -1, float value = 0.0) {
    int size = xsFloatListSize(lst);
    if ((idx < 0) || (idx >= size)) {
        return (cFloatListIndexOutOfRangeError);
    }
    xsArraySetFloat(lst, idx + 1, value);
    return (cFloatListSuccess);
}

int _xsFloatListExtendIntArray(int lst = -1, int capacity = 0) {
    if (capacity == cFloatListMaxCapacity) {
        return (cFloatListMaxCapacityError);
    }
    int newCapacity = capacity * 2;
    if (newCapacity > cFloatListMaxCapacity) {
        newCapacity = cFloatListMaxCapacity;
    }
    int r = xsArrayResizeFloat(lst, newCapacity);
    if (r != 1) {
        return (cFloatListResizeFailedError);
    }
    return (cFloatListSuccess);
}

int _xsFloatListShrinkIntArray(int lst = -1, int size = 0, int capacity = 0) {
    if (size <= (capacity / 2)) {
        int r = xsArrayResizeFloat(lst, size);
        if (r != 1) {
            return (cFloatListResizeFailedError);
        }
    }
    return (cFloatListSuccess);
}

string xsFloatListToString(int lst = -1) {
    int size = xsFloatListSize(lst);
    string s = "[";
    for (i = 1; <= size) {
        s = s + ("" + xsArrayGetFloat(lst, i));
        if (i < size) {
            s = s + ", ";
        }
    }
    s = s + "]";
    return (s);
}

int xsFloatListAppend(int lst = -1, float value = 0) {
    int capacity = xsArrayGetSize(lst);
    int size = xsFloatListSize(lst);
    int nextIdx = size + 1;
    if (capacity == nextIdx) {
        int r = _xsFloatListExtendIntArray(lst, capacity);
        if (r != cFloatListSuccess) {
            return (r);
        }
    }
    xsArraySetFloat(lst, nextIdx, value);
    _xsFloatListSetSize(lst, nextIdx);
    return (cFloatListSuccess);
}

float xsFloatListPop(int lst = -1, int idx = cFloatListMaxCapacity) {
    int capacity = xsArrayGetSize(lst);
    int size = xsFloatListSize(lst);
    if (idx == cFloatListMaxCapacity) {
        idx = size - 1;
    } else if ((idx < 0) || (idx >= size)) {
        _floatListLastOperationStatus = cFloatListIndexOutOfRangeError;
        return (cFloatListGenericErrorFloat);
    }
    float removedElem = xsArrayGetFloat(lst, idx + 1);
    for (i = idx + 2; <= size) {
        xsArraySetFloat(lst, i - 1, xsArrayGetFloat(lst, i));
    }
    int r = _xsFloatListShrinkIntArray(lst, size, capacity);
    if (r != cFloatListSuccess) {
        _floatListLastOperationStatus = r;
        return (cFloatListGenericErrorFloat);
    }
    _xsFloatListSetSize(lst, size - 1);
    _floatListLastOperationStatus = cFloatListSuccess;
    return (removedElem);
}

int xsFloatListInsert(int lst = -1, int idx = -1, float value = 0) {
    int capacity = xsArrayGetSize(lst);
    int size = xsFloatListSize(lst);
    if ((idx < 0) || (idx > size)) {
        return (cFloatListIndexOutOfRangeError);
    }
    int newSize = size + 1;
    if (capacity == newSize) {
        int r = _xsFloatListExtendIntArray(lst, capacity);
        if (r != cFloatListSuccess) {
            return (r);
        }
    }
    for (i = size; > idx) {
        xsArraySetFloat(lst, i + 1, xsArrayGetFloat(lst, i));
    }
    xsArraySetFloat(lst, idx + 1, value);
    _xsFloatListSetSize(lst, newSize);
    return (cFloatListSuccess);
}

int xsFloatListRemove(int lst = -1, float value = -1) {
    int capacity = xsArrayGetSize(lst);
    int size = xsFloatListSize(lst);
    int foundIdx = -1;
    int i = 1;
    while ((i <= size) && (foundIdx == -1)) {
        float cVal = xsArrayGetFloat(lst, i);
        if (cVal == value) {
            foundIdx = i;
        }
        i++;
    }
    if (foundIdx == -1) {
        return (cFloatListGenericError);
    }
    for (j = foundIdx + 1; <= size) {
        xsArraySetFloat(lst, j - 1, xsArrayGetFloat(lst, j));
    }
    int r = _xsFloatListShrinkIntArray(lst, size, capacity);
    if (r != cFloatListSuccess) {
        return (r);
    }
    _xsFloatListSetSize(lst, size - 1);
    return (foundIdx - 1);
}

int xsFloatListIndex(int lst = -1, float value = -1.0, int start = 0, int stop = cFloatListEmptyIntParam) {
    int size = xsFloatListSize(lst);
    if ((stop == cFloatListEmptyIntParam) || (stop > size)) {
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
        if (xsArrayGetFloat(lst, i + 1) == value) {
            return (i);
        }
    }
    return (cFloatListGenericError);
}

bool xsFloatListContains(int lst = -1, float value = -1.0) {
    return (xsFloatListIndex(lst, value) > -1);
}

bool _xsFloatListCompareElem(float a = -1.0, float b = -1.0, bool reverse = false) {
    if (reverse) {
        return (a > b);
    }
    return (a < b);
}

void _xsFloatListSiftDown(int lst = -1, int start = -1, int end = -1, bool reverse = false) {
    int root = start;
    while (true) {
        int child = 2 * root;
        if (child > end) {
            return;
        }
        float childVal = xsArrayGetFloat(lst, child);
        float childVal1 = xsArrayGetFloat(lst, child + 1);
        if (((child + 1) <= end) && _xsFloatListCompareElem(childVal, childVal1, reverse)) {
            child++;
            childVal = childVal1;
        }
        float rootVal = xsArrayGetFloat(lst, root);
        if (_xsFloatListCompareElem(rootVal, childVal, reverse)) {
            xsArraySetFloat(lst, root, childVal);
            xsArraySetFloat(lst, child, rootVal);
            root = child;
        } else {
            return;
        }
    }
}

void xsFloatListSort(int lst = -1, bool reverse = false) {
    int size = xsFloatListSize(lst);
    for (start = size / 2; > 0) {
        _xsFloatListSiftDown(lst, start, size, reverse);
    }
    for (end = size; > 1) {
        float temp = xsArrayGetFloat(lst, 1);
        xsArraySetFloat(lst, 1, xsArrayGetFloat(lst, end));
        xsArraySetFloat(lst, end, temp);
        _xsFloatListSiftDown(lst, 1, end - 1, reverse);
    }
}

int xsFloatListClear(int lst = -1) {
    int capacity = xsFloatListSize(lst);
    if (capacity > 8) {
        int r = xsArrayResizeFloat(lst, 8);
        if (r != 1) {
            return (cFloatListResizeFailedError);
        }
    }
    _xsFloatListSetSize(lst, 0);
    return (cFloatListSuccess);
}

int xsFloatListCopy(int lst = -1, int start = 0, int end = cFloatListMaxCapacity) {
    int size = xsFloatListSize(lst);
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
    int newLst = xsArrayCreateFloat(newSize + 1);
    if (newLst < 0) {
        return (cFloatListGenericError);
    }
    for (i = fr; <= to) {
        xsArraySetFloat(newLst, i - fr, xsArrayGetFloat(lst, i));
    }
    _xsFloatListSetSize(newLst, newSize);
    return (newLst);
}

int xsFloatListExtend(int source = -1, int lst = -1) {
    int sourceSize = xsFloatListSize(source);
    int toAdd = xsFloatListSize(lst);
    int capacity = xsArrayGetSize(source);
    int newSize = sourceSize + toAdd;
    if (newSize > capacity) {
        if (newSize >= cFloatListMaxCapacity) {
            return (cFloatListMaxCapacityError);
        }
        int r = xsArrayResizeFloat(source, newSize + 1);
        if (r != 1) {
            return (cFloatListResizeFailedError);
        }
    }
    for (i = 1; <= toAdd) {
        xsArraySetFloat(source, i + sourceSize, xsArrayGetFloat(lst, i));
    }
    _xsFloatListSetSize(source, newSize);
    return (cFloatListSuccess);
}

int xsFloatListExtendWithArray(int source = -1, int arr = -1) {
    int sourceSize = xsFloatListSize(source);
    int toAdd = xsArrayGetSize(arr);
    int capacity = xsArrayGetSize(source);
    int newSize = sourceSize + toAdd;
    if (newSize > capacity) {
        if ((newSize >= cFloatListMaxCapacity) || (newSize < 0)) {
            return (cFloatListMaxCapacityError);
        }
        int r = xsArrayResizeFloat(source, newSize + 1);
        if (r != 1) {
            return (cFloatListResizeFailedError);
        }
    }
    for (i = 0; < toAdd) {
        xsArraySetFloat(source, (i + sourceSize) + 1, xsArrayGetFloat(arr, i));
    }
    _xsFloatListSetSize(source, newSize);
    return (cFloatListSuccess);
}

int xsFloatListCompare(int lst1 = -1, int lst2 = -1) {
    int size1 = xsFloatListSize(lst1);
    int size2 = xsFloatListSize(lst2);
    int i = 1;
    while ((i <= size1) && (i <= size2)) {
        float v1 = xsArrayGetFloat(lst1, i);
        float v2 = xsArrayGetFloat(lst2, i);
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

int xsFloatListCount(int lst = -1, float value = -1.0) {
    int count = 0;
    int size = xsFloatListSize(lst);
    for (i = 1; <= size) {
        if (xsArrayGetFloat(lst, i) == value) {
            count++;
        }
    }
    return (count);
}

float xsFloatListSum(int lst = -1) {
    float s = 0.0;
    int size = xsFloatListSize(lst);
    for (i = 1; <= size) {
        s = s + xsArrayGetFloat(lst, i);
    }
    return (s);
}

float xsFloatListMin(int lst = -1) {
    int size = xsFloatListSize(lst);
    if (size == 0) {
        _floatListLastOperationStatus = cFloatListIndexOutOfRangeError;
        return (cFloatListGenericErrorFloat);
    }
    float m = xsArrayGetFloat(lst, 1);
    if (size == 1) {
        _floatListLastOperationStatus = cFloatListSuccess;
        return (m);
    }
    for (i = 2; <= size) {
        float v = xsArrayGetFloat(lst, i);
        if (v < m) {
            m = v;
        }
    }
    _floatListLastOperationStatus = cFloatListSuccess;
    return (m);
}

float xsFloatListMax(int lst = -1) {
    int size = xsFloatListSize(lst);
    if (size == 0) {
        _floatListLastOperationStatus = cFloatListIndexOutOfRangeError;
        return (cFloatListGenericErrorFloat);
    }
    float m = xsArrayGetFloat(lst, 1);
    if (size == 1) {
        _floatListLastOperationStatus = cFloatListSuccess;
        return (m);
    }
    for (i = 2; <= size) {
        float v = xsArrayGetFloat(lst, i);
        if (v > m) {
            m = v;
        }
    }
    _floatListLastOperationStatus = cFloatListSuccess;
    return (m);
}

int xsFloatListLastError() {
    return (_floatListLastOperationStatus);
}

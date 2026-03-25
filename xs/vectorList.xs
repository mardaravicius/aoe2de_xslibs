extern const int cVectorListSuccess = 0;
extern const int cVectorListGenericError = -1;
extern const vector cVectorListGenericErrorVector = vector(-1.0, -1.0, -1.0);
extern const int cVectorListIndexOutOfRangeError = -2;
extern const int cVectorListResizeFailedError = -3;
extern const int cVectorListMaxCapacityError = -4;
extern const int cVectorListMaxCapacity = 333333333;
extern const vector cVectorListEmptyParam = vector(-9999999.0, -9999999.0, -9999999.0);
extern const int cVectorListEmptyIntParam = -999999999;
int _vectorListLastOperationStatus = cVectorListSuccess;

int _xsVectorListArrCreate(int size = 0, vector value = vector(0.0, 0.0, 0.0)) {
    float x = xsVectorGetX(value);
    float y = xsVectorGetY(value);
    float z = xsVectorGetZ(value);
    size = size * 3;
    int arr = xsArrayCreateFloat(size, x);
    if ((x == y) && (x == z)) {
        return (arr);
    }
    int i = 1;
    while (i < size) {
        xsArraySetFloat(arr, i, y);
        xsArraySetFloat(arr, i + 1, z);
        i = i + 3;
    }
    return (arr);
}

void _xsVectorListArrSet(int arr = -1, int idx = 0, vector value = vector(0.0, 0.0, 0.0)) {
    idx = idx * 3;
    xsArraySetFloat(arr, idx, xsVectorGetX(value));
    xsArraySetFloat(arr, idx + 1, xsVectorGetY(value));
    xsArraySetFloat(arr, idx + 2, xsVectorGetZ(value));
}

vector _xsVectorListArrGet(int arr = -1, int idx = 0) {
    idx = idx * 3;
    float x = xsArrayGetFloat(arr, idx);
    float y = xsArrayGetFloat(arr, idx + 1);
    float z = xsArrayGetFloat(arr, idx + 2);
    return (xsVectorSet(x, y, z));
}

int _xsVectorListArrResize(int arr = -1, int size = 0) {
    return (xsArrayResizeFloat(arr, size * 3));
}

void _xsVectorListSetSize(int lst = -1, int size = 0) {
    xsArraySetFloat(lst, 0, bitCastToFloat(size));
}

int xsVectorListCapacity(int arr = -1) {
    return (xsArrayGetSize(arr) / 3);
}

/*
    Returns the number of elements in the list.
    @param lst - list id
    @return list size
*/
int xsVectorListSize(int lst = -1) {
    return (bitCastToInt(xsArrayGetFloat(lst, 0)));
}

/*
    Creates empty list for vector values. List is a dynamic array that grows and shrinks as values are added and removed.
    @param capacity - initial list capacity
    @return created list id, or `cVectorListGenericError` on error
*/
int xsVectorListCreate(int capacity = 7) {
    if ((capacity < 0) || (capacity >= cVectorListMaxCapacity)) {
        return (cVectorListGenericError);
    }
    int lst = _xsVectorListArrCreate(capacity + 1);
    if (lst < 0) {
        return (cVectorListGenericError);
    }
    _xsVectorListSetSize(lst, 0);
    return (lst);
}

/*
    Creates a list with provided values. The first value that equals `cVectorListEmptyParam` will stop further insertion.
    This Function can create a list with 12 values at the maximum, but further values can be added with other functions.
    @param v0 through v11 - value at a given index of a list
    @return created list id, or `cVectorListGenericError` on error
*/
int xsVectorList(vector v0 = cVectorListEmptyParam, vector v1 = cVectorListEmptyParam, vector v2 = cVectorListEmptyParam, vector v3 = cVectorListEmptyParam, vector v4 = cVectorListEmptyParam, vector v5 = cVectorListEmptyParam, vector v6 = cVectorListEmptyParam, vector v7 = cVectorListEmptyParam, vector v8 = cVectorListEmptyParam, vector v9 = cVectorListEmptyParam, vector v10 = cVectorListEmptyParam, vector v11 = cVectorListEmptyParam) {
    int lst = _xsVectorListArrCreate(13);
    if (lst < 0) {
        return (cVectorListGenericError);
    }
    if (v0 == cVectorListEmptyParam) {
        _xsVectorListSetSize(lst, 0);
        return (lst);
    }
    _xsVectorListArrSet(lst, 1, v0);
    if (v1 == cVectorListEmptyParam) {
        _xsVectorListSetSize(lst, 1);
        return (lst);
    }
    _xsVectorListArrSet(lst, 2, v1);
    if (v2 == cVectorListEmptyParam) {
        _xsVectorListSetSize(lst, 2);
        return (lst);
    }
    _xsVectorListArrSet(lst, 3, v2);
    if (v3 == cVectorListEmptyParam) {
        _xsVectorListSetSize(lst, 3);
        return (lst);
    }
    _xsVectorListArrSet(lst, 4, v3);
    if (v4 == cVectorListEmptyParam) {
        _xsVectorListSetSize(lst, 4);
        return (lst);
    }
    _xsVectorListArrSet(lst, 5, v4);
    if (v5 == cVectorListEmptyParam) {
        _xsVectorListSetSize(lst, 5);
        return (lst);
    }
    _xsVectorListArrSet(lst, 6, v5);
    if (v6 == cVectorListEmptyParam) {
        _xsVectorListSetSize(lst, 6);
        return (lst);
    }
    _xsVectorListArrSet(lst, 7, v6);
    if (v7 == cVectorListEmptyParam) {
        _xsVectorListSetSize(lst, 7);
        return (lst);
    }
    _xsVectorListArrSet(lst, 8, v7);
    if (v8 == cVectorListEmptyParam) {
        _xsVectorListSetSize(lst, 8);
        return (lst);
    }
    _xsVectorListArrSet(lst, 9, v8);
    if (v9 == cVectorListEmptyParam) {
        _xsVectorListSetSize(lst, 9);
        return (lst);
    }
    _xsVectorListArrSet(lst, 10, v9);
    if (v10 == cVectorListEmptyParam) {
        _xsVectorListSetSize(lst, 10);
        return (lst);
    }
    _xsVectorListArrSet(lst, 11, v10);
    if (v11 == cVectorListEmptyParam) {
        _xsVectorListSetSize(lst, 11);
        return (lst);
    }
    _xsVectorListArrSet(lst, 12, v11);
    _xsVectorListSetSize(lst, 12);
    return (lst);
}

/*
    Creates a list by repeating a single value.
    @param value - value to repeat
    @param times - number of times to repeat the value
    @return created list id, or `cVectorListGenericError` on error
*/
int xsVectorListFromRepeatedVal(vector value = vector(0.0, 0.0, 0.0), int times = 0) {
    if ((times < 0) || (times >= cVectorListMaxCapacity)) {
        return (cVectorListGenericError);
    }
    int lst = _xsVectorListArrCreate(times + 1, value);
    if (lst < 0) {
        return (cVectorListGenericError);
    }
    _xsVectorListSetSize(lst, times);
    return (lst);
}

/*
    Creates a new list by repeating all elements of the given list.
    @param lst - source list id
    @param times - number of times to repeat the list contents
    @return created list id, or `cVectorListGenericError` on error
*/
int xsVectorListFromRepeatedList(int lst = -1, int times = 0) {
    if (times < 0) {
        return (cVectorListGenericError);
    }
    int size = xsVectorListSize(lst);
    if ((times > 0) && (size > (cVectorListMaxCapacity / times))) {
        return (cVectorListMaxCapacityError);
    }
    int newCapacity = (size * times) + 1;
    if (newCapacity > cVectorListMaxCapacity) {
        return (cVectorListMaxCapacityError);
    }
    int newLst = _xsVectorListArrCreate(newCapacity);
    if (newLst < 0) {
        return (cVectorListGenericError);
    }
    for (i = 1; <= size) {
        vector val = _xsVectorListArrGet(lst, i);
        int j = i;
        while (j < newCapacity) {
            _xsVectorListArrSet(newLst, j, val);
            j = j + size;
        }
    }
    _xsVectorListSetSize(newLst, newCapacity - 1);
    return (newLst);
}

/*
    Creates a new list by copying elements from an XS array.
    @param arr - source XS array id
    @return created list id, or `cVectorListGenericError` on error
*/
int xsVectorListFromArray(int arr = -1) {
    int arrSize = xsArrayGetSize(arr);
    int lst = xsVectorListCreate(arrSize);
    if (lst < 0) {
        return (lst);
    }
    for (i = 0; < arrSize) {
        _xsVectorListArrSet(lst, i + 1, xsArrayGetVector(arr, i));
    }
    _xsVectorListSetSize(lst, arrSize);
    return (lst);
}

/*
    Returns the element at the given index. Sets last error on failure.
    @param lst - list id
    @param idx - zero-based index
    @return value at index, or `cVectorListGenericErrorVector` on error
*/
vector xsVectorListGet(int lst = -1, int idx = -1) {
    int size = xsVectorListSize(lst);
    if ((idx < 0) || (idx >= size)) {
        _vectorListLastOperationStatus = cVectorListIndexOutOfRangeError;
        return (cVectorListGenericErrorVector);
    }
    _vectorListLastOperationStatus = cVectorListSuccess;
    return (_xsVectorListArrGet(lst, idx + 1));
}

/*
    Sets the element at the given index to a new value.
    @param lst - list id
    @param idx - zero-based index
    @param value - new value to set
    @return `cVectorListSuccess` on success, or error if negative
*/
int xsVectorListSet(int lst = -1, int idx = -1, vector value = vector(0.0, 0.0, 0.0)) {
    int size = xsVectorListSize(lst);
    if ((idx < 0) || (idx >= size)) {
        return (cVectorListIndexOutOfRangeError);
    }
    _xsVectorListArrSet(lst, idx + 1, value);
    return (cVectorListSuccess);
}

int _xsVectorListExtendVectorArray(int lst = -1, int capacity = 0) {
    if (capacity >= cVectorListMaxCapacity) {
        return (cVectorListMaxCapacityError);
    }
    int newCapacity = 0;
    if (capacity > (cVectorListMaxCapacity / 2)) {
        newCapacity = cVectorListMaxCapacity;
    } else {
        newCapacity = capacity * 2;
    }
    if (newCapacity > cVectorListMaxCapacity) {
        newCapacity = cVectorListMaxCapacity;
    } else if (newCapacity == 0) {
        newCapacity = 8;
    }
    int r = _xsVectorListArrResize(lst, newCapacity);
    if (r != 1) {
        return (cVectorListResizeFailedError);
    }
    return (cVectorListSuccess);
}

int _xsVectorListShrinkVectorArray(int lst = -1, int size = 0, int capacity = 0) {
    if (size <= (capacity / 2)) {
        int r = _xsVectorListArrResize(lst, capacity / 2);
        if (r != 1) {
            return (cVectorListResizeFailedError);
        }
    }
    return (cVectorListSuccess);
}

/*
    Appends a value to the end of the list, growing the backing array if needed.
    @param lst - list id
    @param value - value to append
    @return `cVectorListSuccess` on success, or error if negative
*/
int xsVectorListAppend(int lst = -1, vector value = vector(0.0, 0.0, 0.0)) {
    int capacity = xsVectorListCapacity(lst);
    int size = xsVectorListSize(lst);
    int nextIdx = size + 1;
    if (capacity <= nextIdx) {
        int r = _xsVectorListExtendVectorArray(lst, capacity);
        if (r != cVectorListSuccess) {
            return (r);
        }
    }
    _xsVectorListArrSet(lst, nextIdx, value);
    _xsVectorListSetSize(lst, nextIdx);
    return (cVectorListSuccess);
}

/*
    Inserts a value at the given index, shifting subsequent elements to the right.
    @param lst - list id
    @param idx - zero-based index at which to insert
    @param value - value to insert
    @return `cVectorListSuccess` on success, or error if negative
*/
int xsVectorListInsert(int lst = -1, int idx = -1, vector value = vector(0.0, 0.0, 0.0)) {
    int capacity = xsVectorListCapacity(lst);
    int size = xsVectorListSize(lst);
    if ((idx < 0) || (idx > size)) {
        return (cVectorListIndexOutOfRangeError);
    }
    int newSize = size + 1;
    if (capacity <= newSize) {
        int r = _xsVectorListExtendVectorArray(lst, capacity);
        if (r != cVectorListSuccess) {
            return (r);
        }
    }
    for (i = size; > idx) {
        _xsVectorListArrSet(lst, i + 1, _xsVectorListArrGet(lst, i));
    }
    _xsVectorListArrSet(lst, idx + 1, value);
    _xsVectorListSetSize(lst, newSize);
    return (cVectorListSuccess);
}

/*
    Removes and returns the element at the given index, shifting subsequent elements to the left.
    Defaults to the last element. Sets last error on failure.
    @param lst - list id
    @param idx - zero-based index of element to remove (defaults to last)
    @return removed value, or `cVectorListGenericErrorVector` on error
*/
vector xsVectorListPop(int lst = -1, int idx = cVectorListMaxCapacity) {
    int capacity = xsVectorListCapacity(lst);
    int size = xsVectorListSize(lst);
    if (idx == cVectorListMaxCapacity) {
        idx = size - 1;
    }
    if ((idx < 0) || (idx >= size)) {
        _vectorListLastOperationStatus = cVectorListIndexOutOfRangeError;
        return (cVectorListGenericErrorVector);
    }
    vector removedElem = _xsVectorListArrGet(lst, idx + 1);
    for (i = idx + 2; <= size) {
        _xsVectorListArrSet(lst, i - 1, _xsVectorListArrGet(lst, i));
    }
    _xsVectorListSetSize(lst, size - 1);
    int r = _xsVectorListShrinkVectorArray(lst, size, capacity);
    if (r != cVectorListSuccess) {
        _vectorListLastOperationStatus = r;
        return (cVectorListGenericErrorVector);
    }
    _vectorListLastOperationStatus = cVectorListSuccess;
    return (removedElem);
}

/*
    Removes the first occurrence of the given value from the list.
    @param lst - list id
    @param value - value to remove
    @return index of the removed element, or `cVectorListGenericError` if not found
*/
int xsVectorListRemove(int lst = -1, vector value = vector(-1.0, -1.0, -1.0)) {
    int capacity = xsVectorListCapacity(lst);
    int size = xsVectorListSize(lst);
    int foundIdx = -1;
    int i = 1;
    while ((i <= size) && (foundIdx == -1)) {
        vector cVal = _xsVectorListArrGet(lst, i);
        if (cVal == value) {
            foundIdx = i;
        }
        i++;
    }
    if (foundIdx == -1) {
        return (cVectorListGenericError);
    }
    for (j = foundIdx + 1; <= size) {
        _xsVectorListArrSet(lst, j - 1, _xsVectorListArrGet(lst, j));
    }
    _xsVectorListSetSize(lst, size - 1);
    int r = _xsVectorListShrinkVectorArray(lst, size, capacity);
    if (r != cVectorListSuccess) {
        return (r);
    }
    return (foundIdx - 1);
}

/*
    Returns the index of the first occurrence of the value within the optional [start, stop) range. Negative start/stop are relative to the end.
    @param lst - list id
    @param value - value to search for
    @param start - start of search range (inclusive)
    @param stop - end of search range (exclusive), defaults to list size
    @return index of the value, or `cVectorListGenericError` if not found
*/
int xsVectorListIndex(int lst = -1, vector value = vector(-1.0, -1.0, -1.0), int start = 0, int stop = cVectorListEmptyIntParam) {
    int size = xsVectorListSize(lst);
    if ((stop == cVectorListEmptyIntParam) || (stop > size)) {
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
        if (_xsVectorListArrGet(lst, i + 1) == value) {
            return (i);
        }
    }
    return (cVectorListGenericError);
}

/*
    Checks whether the list contains the given value.
    @param lst - list id
    @param value - value to search for
    @return true if the value is found, false otherwise
*/
bool xsVectorListContains(int lst = -1, vector value = vector(-1.0, -1.0, -1.0)) {
    return (xsVectorListIndex(lst, value) > -1);
}

/*
    Returns a string representation of the list in the format `[v0, v1, ...]`.
    @param lst - list id
    @return string representation of the list
*/
string xsVectorListToString(int lst = -1) {
    int size = xsVectorListSize(lst);
    string s = "[";
    for (i = 1; <= size) {
        s = s + ("" + _xsVectorListArrGet(lst, i));
        if (i < size) {
            s = s + ", ";
        }
    }
    s = s + "]";
    return (s);
}

/*
    Returns a copy of the list, optionally sliced by [start, end). Negative start/end are relative to the end.
    @param lst - list id
    @param start - start of slice (inclusive)
    @param end - end of slice (exclusive), defaults to list size
    @return new list id, or `cVectorListGenericError` on error
*/
int xsVectorListCopy(int lst = -1, int start = 0, int end = cVectorListMaxCapacity) {
    int size = xsVectorListSize(lst);
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
    int newLst = _xsVectorListArrCreate(newSize + 1);
    if (newLst < 0) {
        return (cVectorListGenericError);
    }
    for (i = fr; < to) {
        _xsVectorListArrSet(newLst, (i - fr) + 1, _xsVectorListArrGet(lst, i + 1));
    }
    _xsVectorListSetSize(newLst, newSize);
    return (newLst);
}

/*
    Appends all elements from another list to the source list.
    @param source - list id to extend
    @param lst - list id whose elements are appended
    @return `cVectorListSuccess` on success, or error if negative
*/
int xsVectorListExtend(int source = -1, int lst = -1) {
    int sourceSize = xsVectorListSize(source);
    int toAdd = xsVectorListSize(lst);
    int capacity = xsVectorListCapacity(source);
    int newSize = sourceSize + toAdd;
    if ((newSize + 1) > capacity) {
        if (newSize >= cVectorListMaxCapacity) {
            return (cVectorListMaxCapacityError);
        }
        int r = _xsVectorListArrResize(source, newSize + 1);
        if (r != 1) {
            return (cVectorListResizeFailedError);
        }
    }
    for (i = 1; <= toAdd) {
        _xsVectorListArrSet(source, i + sourceSize, _xsVectorListArrGet(lst, i));
    }
    _xsVectorListSetSize(source, newSize);
    return (cVectorListSuccess);
}

/*
    Appends all elements from an XS array to the source list.
    @param source - list id to extend
    @param arr - XS array id whose elements are appended
    @return `cVectorListSuccess` on success, or error if negative
*/
int xsVectorListExtendWithArray(int source = -1, int arr = -1) {
    int sourceSize = xsVectorListSize(source);
    int toAdd = xsArrayGetSize(arr);
    int capacity = xsVectorListCapacity(source);
    int newSize = sourceSize + toAdd;
    if ((newSize + 1) > capacity) {
        if ((newSize >= cVectorListMaxCapacity) || (newSize < 0)) {
            return (cVectorListMaxCapacityError);
        }
        int r = _xsVectorListArrResize(source, newSize + 1);
        if (r != 1) {
            return (cVectorListResizeFailedError);
        }
    }
    for (i = 0; < toAdd) {
        _xsVectorListArrSet(source, (i + sourceSize) + 1, xsArrayGetVector(arr, i));
    }
    _xsVectorListSetSize(source, newSize);
    return (cVectorListSuccess);
}

/*
    Removes all elements from the list and shrinks the backing array.
    @param lst - list id
    @return `cVectorListSuccess` on success, or error if negative
*/
int xsVectorListClear(int lst = -1) {
    int capacity = xsVectorListCapacity(lst);
    if (capacity > 8) {
        int r = _xsVectorListArrResize(lst, 8);
        if (r != 1) {
            return (cVectorListResizeFailedError);
        }
    }
    _xsVectorListSetSize(lst, 0);
    return (cVectorListSuccess);
}

/*
    Reverses the list in-place.
    @param lst - list id
*/
void xsVectorListReverse(int lst = -1) {
    int size = xsVectorListSize(lst);
    int mid = (size + 2) / 2;
    for (i = 1; < mid) {
        vector temp = _xsVectorListArrGet(lst, i);
        int backI = (size - i) + 1;
        _xsVectorListArrSet(lst, i, _xsVectorListArrGet(lst, backI));
        _xsVectorListArrSet(lst, backI, temp);
    }
}

/*
    Counts the number of occurrences of a value in the list.
    @param lst - list id
    @param value - value to count
    @return number of occurrences
*/
int xsVectorListCount(int lst = -1, vector value = vector(-1.0, -1.0, -1.0)) {
    int count = 0;
    int size = xsVectorListSize(lst);
    for (i = 1; <= size) {
        if (_xsVectorListArrGet(lst, i) == value) {
            count++;
        }
    }
    return (count);
}

/*
    Returns the status code of the last operation that sets it (get, pop).
    @return `cVectorListSuccess` if the last such operation succeeded, or a negative error code
*/
int xsVectorListLastError() {
    return (_vectorListLastOperationStatus);
}

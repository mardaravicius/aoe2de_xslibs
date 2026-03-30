extern const int cBoolListSuccess = 0;
extern const int cBoolListGenericError = -1;
extern const int cBoolListIndexOutOfRangeError = -2;
extern const int cBoolListResizeFailedError = -3;
extern const int cBoolListMaxCapacityError = -4;
extern const int cBoolListMaxCapacity = 999999999;
extern const int cBoolListEmptyIntParam = -999999999;
int _boolListLastOperationStatus = cBoolListSuccess;

/*
    Returns the number of elements in the list.
    @param lst - list id
    @return list size
*/
int xsBoolListSize(int lst = -1) {
    return (xsArrayGetInt(lst, 0));
}

/*
    Creates empty list for bool values. List is a dynamic array that grows and shrinks as values are added and removed.
    @param capacity - initial list capacity
    @return created list id, or `cBoolListGenericError` on error
*/
int xsBoolListCreate(int capacity = 7) {
    if ((capacity < 0) || (capacity >= cBoolListMaxCapacity)) {
        return (cBoolListGenericError);
    }
    int lst = xsArrayCreateInt(2, 0);
    if (lst < 0) {
        return (cBoolListGenericError);
    }
    int boolLst = xsArrayCreateBool(capacity);
    if (boolLst < 0) {
        xsArrayResizeInt(lst, 0);
        return (cBoolListGenericError);
    }
    xsArraySetInt(lst, 1, boolLst);
    return (lst);
}

/*
    Creates a list by repeating a single value.
    @param value - value to repeat
    @param times - number of times to repeat the value
    @return created list id, or `cBoolListGenericError` on error
*/
int xsBoolListFromRepeatedVal(bool value = false, int times = 0) {
    if ((times < 0) || (times > cBoolListMaxCapacity)) {
        return (cBoolListGenericError);
    }
    int lst = xsArrayCreateInt(2, times);
    if (lst < 0) {
        return (cBoolListGenericError);
    }
    int boolLst = xsArrayCreateBool(times, value);
    if (boolLst < 0) {
        xsArrayResizeInt(lst, 0);
        return (cBoolListGenericError);
    }
    xsArraySetInt(lst, 1, boolLst);
    return (lst);
}

/*
    Creates a new list by repeating all elements of the given list.
    @param lst - source list id
    @param times - number of times to repeat the list contents
    @return created list id, or `cBoolListGenericError` on error
*/
int xsBoolListFromRepeatedList(int lst = -1, int times = 0) {
    if (times < 0) {
        return (cBoolListGenericError);
    }
    int size = xsArrayGetInt(lst, 0);
    if ((times > 0) && (size > (cBoolListMaxCapacity / times))) {
        return (cBoolListMaxCapacityError);
    }
    int newCapacity = size * times;
    if (newCapacity > cBoolListMaxCapacity) {
        return (cBoolListMaxCapacityError);
    }
    int newBoolLst = xsArrayCreateBool(newCapacity);
    if (newBoolLst < 0) {
        return (cBoolListGenericError);
    }
    int newLst = xsArrayCreateInt(2, newCapacity);
    if (newLst < 0) {
        xsArrayResizeBool(newBoolLst, 0);
        return (cBoolListGenericError);
    }
    int boolLst = xsArrayGetInt(lst, 1);
    for (i = 0; < size) {
        bool val = xsArrayGetBool(boolLst, i);
        int j = i;
        while (j < newCapacity) {
            xsArraySetBool(newBoolLst, j, val);
            j = j + size;
        }
    }
    xsArraySetInt(newLst, 1, newBoolLst);
    return (newLst);
}

/*
    Creates a new list by copying elements from an XS array.
    @param arr - source XS array id
    @return created list id, or `cBoolListGenericError` on error
*/
int xsBoolListFromArray(int arr = -1) {
    int arrSize = xsArrayGetSize(arr);
    if (arrSize > cBoolListMaxCapacity) {
        return (cBoolListMaxCapacityError);
    }
    int newBoolLst = xsArrayCreateBool(arrSize);
    if (newBoolLst < 0) {
        return (cBoolListGenericError);
    }
    int lst = xsArrayCreateInt(2, arrSize);
    if (lst < 0) {
        xsArrayResizeBool(newBoolLst, 0);
        return (cBoolListGenericError);
    }
    for (i = 0; < arrSize) {
        xsArraySetBool(newBoolLst, i, xsArrayGetBool(arr, i));
    }
    xsArraySetInt(lst, 1, newBoolLst);
    return (lst);
}

/*
    Wraps an existing XS bool array as a list without copying elements.
    @param arr - XS bool array id to use as backing storage
    @return list id, or `cBoolListMaxCapacityError`/`cBoolListGenericError` on error
*/
int xsBoolListUseArrayAsSource(int arr = -1) {
    int arrSize = xsArrayGetSize(arr);
    if (arrSize > cBoolListMaxCapacity) {
        return (cBoolListMaxCapacityError);
    }
    int lst = xsArrayCreateInt(2, arrSize);
    if (lst < 0) {
        return (cBoolListGenericError);
    }
    xsArraySetInt(lst, 1, arr);
    return (lst);
}

/*
    Returns the element at the given index. Sets last error on failure.
    @param lst - list id
    @param idx - zero-based index
    @return value at index, or `false` on error
*/
bool xsBoolListGet(int lst = -1, int idx = -1) {
    int size = xsBoolListSize(lst);
    if ((idx < 0) || (idx >= size)) {
        _boolListLastOperationStatus = cBoolListIndexOutOfRangeError;
        return (false);
    }
    _boolListLastOperationStatus = cBoolListSuccess;
    return (xsArrayGetBool(xsArrayGetInt(lst, 1), idx));
}

/*
    Sets the element at the given index to a new value.
    @param lst - list id
    @param idx - zero-based index
    @param value - new value to set
    @return `cBoolListSuccess` on success, or error if negative
*/
int xsBoolListSet(int lst = -1, int idx = -1, bool value = false) {
    int size = xsArrayGetInt(lst, 0);
    if ((idx < 0) || (idx >= size)) {
        return (cBoolListIndexOutOfRangeError);
    }
    xsArraySetBool(xsArrayGetInt(lst, 1), idx, value);
    return (cBoolListSuccess);
}

int _xsBoolListExtendBoolArray(int lst = -1, int capacity = 0) {
    if (capacity >= cBoolListMaxCapacity) {
        return (cBoolListMaxCapacityError);
    }
    int newCapacity = 0;
    if (capacity > (cBoolListMaxCapacity / 2)) {
        newCapacity = cBoolListMaxCapacity;
    } else {
        newCapacity = capacity * 2;
    }
    if (newCapacity > cBoolListMaxCapacity) {
        newCapacity = cBoolListMaxCapacity;
    } else if (newCapacity == 0) {
        newCapacity = 8;
    }
    int r = xsArrayResizeBool(lst, newCapacity);
    if (r != 1) {
        return (cBoolListResizeFailedError);
    }
    return (cBoolListSuccess);
}

int _xsBoolListShrinkBoolArray(int lst = -1, int size = 0, int capacity = 0) {
    if (size <= (capacity / 2)) {
        int r = xsArrayResizeBool(lst, capacity / 2);
        if (r != 1) {
            return (cBoolListResizeFailedError);
        }
    }
    return (cBoolListSuccess);
}

/*
    Appends a value to the end of the list, growing the backing array if needed.
    @param lst - list id
    @param value - value to append
    @return `cBoolListSuccess` on success, or error if negative
*/
int xsBoolListAppend(int lst = -1, bool value = false) {
    int boolLst = xsArrayGetInt(lst, 1);
    int capacity = xsArrayGetSize(boolLst);
    int size = xsArrayGetInt(lst, 0);
    if (capacity <= size) {
        int r = _xsBoolListExtendBoolArray(boolLst, capacity);
        if (r != cBoolListSuccess) {
            return (r);
        }
    }
    xsArraySetBool(boolLst, size, value);
    xsArraySetInt(lst, 0, size + 1);
    return (cBoolListSuccess);
}

/*
    Inserts a value at the given index, shifting subsequent elements to the right.
    @param lst - list id
    @param idx - zero-based index at which to insert
    @param value - value to insert
    @return `cBoolListSuccess` on success, or error if negative
*/
int xsBoolListInsert(int lst = -1, int idx = -1, bool value = false) {
    int size = xsArrayGetInt(lst, 0);
    if ((idx < 0) || (idx > size)) {
        return (cBoolListIndexOutOfRangeError);
    }
    int newSize = size + 1;
    int boolLst = xsArrayGetInt(lst, 1);
    int capacity = xsArrayGetSize(boolLst);
    if (capacity < newSize) {
        int r = _xsBoolListExtendBoolArray(boolLst, capacity);
        if (r != cBoolListSuccess) {
            return (r);
        }
    }
    for (i = size; > idx) {
        xsArraySetBool(boolLst, i, xsArrayGetBool(boolLst, i - 1));
    }
    xsArraySetBool(boolLst, idx, value);
    xsArraySetInt(lst, 0, newSize);
    return (cBoolListSuccess);
}

/*
    Removes and returns the element at the given index, shifting subsequent elements to the left.
    Defaults to the last element. Sets last error on failure.
    @param lst - list id
    @param idx - zero-based index of element to remove (defaults to last)
    @return removed value, or `false` on error
*/
bool xsBoolListPop(int lst = -1, int idx = cBoolListMaxCapacity) {
    int boolLst = xsArrayGetInt(lst, 1);
    int capacity = xsArrayGetSize(boolLst);
    int size = xsArrayGetInt(lst, 0);
    if (idx == cBoolListMaxCapacity) {
        idx = size - 1;
    }
    if ((idx < 0) || (idx >= size)) {
        _boolListLastOperationStatus = cBoolListIndexOutOfRangeError;
        return (false);
    }
    bool removedElem = xsArrayGetBool(boolLst, idx);
    for (i = idx; < size - 1) {
        xsArraySetBool(boolLst, i, xsArrayGetBool(boolLst, i + 1));
    }
    xsArraySetInt(lst, 0, size - 1);
    int r = _xsBoolListShrinkBoolArray(boolLst, size, capacity);
    if (r != cBoolListSuccess) {
        _boolListLastOperationStatus = r;
        return (false);
    }
    _boolListLastOperationStatus = cBoolListSuccess;
    return (removedElem);
}

/*
    Removes the first occurrence of the given value from the list.
    @param lst - list id
    @param value - value to remove
    @return index of the removed element, or `cBoolListGenericError` if not found
*/
int xsBoolListRemove(int lst = -1, bool value = false) {
    int boolLst = xsArrayGetInt(lst, 1);
    int size = xsArrayGetInt(lst, 0);
    int foundIdx = -1;
    int i = 0;
    while ((i < size) && (foundIdx == -1)) {
        bool cVal = xsArrayGetBool(boolLst, i);
        if (cVal == value) {
            foundIdx = i;
        }
        i++;
    }
    if (foundIdx == -1) {
        return (cBoolListGenericError);
    }
    int newSize = size - 1;
    for (j = foundIdx; < newSize) {
        xsArraySetBool(boolLst, j, xsArrayGetBool(boolLst, j + 1));
    }
    xsArraySetInt(lst, 0, newSize);
    int capacity = xsArrayGetSize(boolLst);
    int r = _xsBoolListShrinkBoolArray(boolLst, size, capacity);
    if (r != cBoolListSuccess) {
        return (r);
    }
    return (foundIdx);
}

/*
    Returns the index of the first occurrence of the value within the optional [start, stop) range. Negative start/stop are relative to the end.
    @param lst - list id
    @param value - value to search for
    @param start - start of search range (inclusive)
    @param stop - end of search range (exclusive), defaults to list size
    @return index of the value, or `cBoolListGenericError` if not found
*/
int xsBoolListIndex(int lst = -1, bool value = false, int start = 0, int stop = cBoolListEmptyIntParam) {
    int size = xsArrayGetInt(lst, 0);
    int boolLst = xsArrayGetInt(lst, 1);
    if ((stop == cBoolListEmptyIntParam) || (stop > size)) {
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
        if (xsArrayGetBool(boolLst, i) == value) {
            return (i);
        }
    }
    return (cBoolListGenericError);
}

/*
    Checks whether the list contains the given value.
    @param lst - list id
    @param value - value to search for
    @return true if the value is found, false otherwise
*/
bool xsBoolListContains(int lst = -1, bool value = false) {
    return (xsBoolListIndex(lst, value) > -1);
}

bool _xsBoolListCompareElem(bool a = false, bool b = false, bool reverse = false) {
    if (reverse) {
        return (a && (b == false));
    }
    return ((a == false) && b);
}

void _xsBoolListSiftDown(int lst = -1, int start = -1, int end = -1, bool reverse = false) {
    int root = start;
    while (true) {
        int child = (2 * root) + 1;
        if (child > end) {
            return;
        }
        bool childVal = xsArrayGetBool(lst, child);
        if ((child + 1) <= end) {
            bool childVal1 = xsArrayGetBool(lst, child + 1);
            if (_xsBoolListCompareElem(childVal, childVal1, reverse)) {
                child++;
                childVal = childVal1;
            }
        }
        bool rootVal = xsArrayGetBool(lst, root);
        if (_xsBoolListCompareElem(rootVal, childVal, reverse)) {
            xsArraySetBool(lst, root, childVal);
            xsArraySetBool(lst, child, rootVal);
            root = child;
        } else {
            return;
        }
    }
}

/*
    Sorts the list in-place using heapsort.
    @param lst - list id
    @param reverse - if true, sorts in descending order
*/
void xsBoolListSort(int lst = -1, bool reverse = false) {
    int size = xsArrayGetInt(lst, 0);
    int boolLst = xsArrayGetInt(lst, 1);
    for (start = (size / 2) - 1; > -1) {
        _xsBoolListSiftDown(boolLst, start, size - 1, reverse);
    }
    for (end = size - 1; > 0) {
        bool temp = xsArrayGetBool(boolLst, 0);
        xsArraySetBool(boolLst, 0, xsArrayGetBool(boolLst, end));
        xsArraySetBool(boolLst, end, temp);
        _xsBoolListSiftDown(boolLst, 0, end - 1, reverse);
    }
}

/*
    Returns a string representation of the list in the format `[true, false, ...]`.
    @param lst - list id
    @return string representation of the list
*/
string xsBoolListToString(int lst = -1) {
    int size = xsArrayGetInt(lst, 0);
    int boolLst = xsArrayGetInt(lst, 1);
    if (size == 0) {
        return ("[]");
    }
    string s = "[";
    for (i = 0; < size) {
        if (xsArrayGetBool(boolLst, i)) {
            s = s + "true";
        } else {
            s = s + "false";
        }
        if (i < (size - 1)) {
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
    @return new list id, or `cBoolListGenericError` on error
*/
int xsBoolListCopy(int lst = -1, int start = 0, int end = cBoolListMaxCapacity) {
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
    if (newLst < 0) {
        return (cBoolListGenericError);
    }
    int newBoolLst = xsArrayCreateBool(newSize);
    if (newBoolLst < 0) {
        xsArrayResizeInt(newLst, 0);
        return (cBoolListGenericError);
    }
    xsArraySetInt(newLst, 1, newBoolLst);
    int boolLst = xsArrayGetInt(lst, 1);
    for (i = fr; < to) {
        xsArraySetBool(newBoolLst, i - fr, xsArrayGetBool(boolLst, i));
    }
    return (newLst);
}

/*
    Appends all elements from another list to the source list.
    @param source - list id to extend
    @param lst - list id whose elements are appended
    @return `cBoolListSuccess` on success, or error if negative
*/
int xsBoolListExtend(int source = -1, int lst = -1) {
    int sourceSize = xsArrayGetInt(source, 0);
    int toAdd = xsArrayGetInt(lst, 0);
    int boolSource = xsArrayGetInt(source, 1);
    int capacity = xsArrayGetSize(boolSource);
    int newSize = sourceSize + toAdd;
    if (newSize > capacity) {
        if (newSize > cBoolListMaxCapacity) {
            return (cBoolListMaxCapacityError);
        }
        int r = xsArrayResizeBool(boolSource, newSize);
        if (r != 1) {
            return (cBoolListResizeFailedError);
        }
    }
    int boolList = xsArrayGetInt(lst, 1);
    for (i = 0; < toAdd) {
        xsArraySetBool(boolSource, i + sourceSize, xsArrayGetBool(boolList, i));
    }
    xsArraySetInt(source, 0, newSize);
    return (cBoolListSuccess);
}

/*
    Appends all elements from a raw XS bool array to the source list.
    @param source - list id to extend
    @param arr - raw XS bool array id whose elements are appended
    @return `cBoolListSuccess` on success, or error if negative
*/
int xsBoolListExtendWithArray(int source = -1, int arr = -1) {
    int sourceSize = xsArrayGetInt(source, 0);
    int toAdd = xsArrayGetSize(arr);
    int boolSource = xsArrayGetInt(source, 1);
    int capacity = xsArrayGetSize(boolSource);
    int newSize = sourceSize + toAdd;
    if (newSize > capacity) {
        if ((newSize > cBoolListMaxCapacity) || (newSize < 0)) {
            return (cBoolListMaxCapacityError);
        }
        int r = xsArrayResizeBool(boolSource, newSize);
        if (r != 1) {
            return (cBoolListResizeFailedError);
        }
    }
    for (i = 0; < toAdd) {
        xsArraySetBool(boolSource, i + sourceSize, xsArrayGetBool(arr, i));
    }
    xsArraySetInt(source, 0, newSize);
    return (cBoolListSuccess);
}

/*
    Removes all elements from the list and shrinks the backing array.
    @param lst - list id
    @return `cBoolListSuccess` on success, or error if negative
*/
int xsBoolListClear(int lst = -1) {
    int boolList = xsArrayGetInt(lst, 1);
    int capacity = xsArrayGetSize(boolList);
    if (capacity > 8) {
        int r = xsArrayResizeBool(boolList, 8);
        if (r != 1) {
            return (cBoolListResizeFailedError);
        }
    }
    xsArraySetInt(lst, 0, 0);
    return (cBoolListSuccess);
}

/*
    Performs lexicographic comparison of two lists.
    @param lst1 - first list id
    @param lst2 - second list id
    @return -1 if lst1 < lst2, 1 if lst1 > lst2, 0 if equal
*/
int xsBoolListCompare(int lst1 = -1, int lst2 = -1) {
    int size1 = xsArrayGetInt(lst1, 0);
    int size2 = xsArrayGetInt(lst2, 0);
    int boolList1 = xsArrayGetInt(lst1, 1);
    int boolList2 = xsArrayGetInt(lst2, 1);
    int i = 0;
    while ((i < size1) && (i < size2)) {
        bool v1 = xsArrayGetBool(boolList1, i);
        bool v2 = xsArrayGetBool(boolList2, i);
        if ((v1 == false) && v2) {
            return (-1);
        }
        if (v1 && (v2 == false)) {
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

/*
    Reverses the list in-place.
    @param lst - list id
*/
void xsBoolListReverse(int lst = -1) {
    int size = xsArrayGetInt(lst, 0);
    int boolList = xsArrayGetInt(lst, 1);
    int mid = size / 2;
    for (i = 0; < mid) {
        bool temp = xsArrayGetBool(boolList, i);
        int backI = (size - i) - 1;
        xsArraySetBool(boolList, i, xsArrayGetBool(boolList, backI));
        xsArraySetBool(boolList, backI, temp);
    }
}

/*
    Counts the number of occurrences of a value in the list.
    @param lst - list id
    @param value - value to count
    @return number of occurrences
*/
int xsBoolListCount(int lst = -1, bool value = false) {
    int count = 0;
    int size = xsArrayGetInt(lst, 0);
    int boolList = xsArrayGetInt(lst, 1);
    for (i = 0; < size) {
        if (xsArrayGetBool(boolList, i) == value) {
            count++;
        }
    }
    return (count);
}

/*
    Returns the status code of the last operation that sets it (get, pop).
    @return `cBoolListSuccess` if the last such operation succeeded, or a negative error code
*/
int xsBoolListLastError() {
    return (_boolListLastOperationStatus);
}

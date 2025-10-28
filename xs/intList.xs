extern const int cIntListSuccess = 0;
extern const int cIntListGenericError = -1;
extern const int cIntListIndexOutOfRangeError = -2;
extern const int cIntListResizeFailedError = -3;
extern const int cIntListMaxCapacityError = -4;
extern const int cIntListMaxCapacity = 999999999;
extern const int cIntListEmptyParam = -999999999;
int _intListLastOperationStatus = cIntListSuccess;

/*
    Creates a list with provided values. The first value that equals `cIntListEmptyParam` will stop further insertion.
    This Function can create a list with 12 values at the maximum, but further values can be added with other functions.
    @param v1 through v11 - value at a given index of a list
    @return created list id, or error if negative
*/
int xsIntList(int v0 = cIntListEmptyParam, int v1 = cIntListEmptyParam, int v2 = cIntListEmptyParam, int v3 = cIntListEmptyParam, int v4 = cIntListEmptyParam, int v5 = cIntListEmptyParam, int v6 = cIntListEmptyParam, int v7 = cIntListEmptyParam, int v8 = cIntListEmptyParam, int v9 = cIntListEmptyParam, int v10 = cIntListEmptyParam, int v11 = cIntListEmptyParam) {
    int lst = xsArrayCreateInt(13);
    if (lst < 0) {
        return (cIntListGenericError);
    }
    if (v0 == cIntListEmptyParam) {
        xsArraySetInt(lst, 0, 0);
        return (lst);
    }
    xsArraySetInt(lst, 1, v0);
    if (v1 == cIntListEmptyParam) {
        xsArraySetInt(lst, 0, 1);
        return (lst);
    }
    xsArraySetInt(lst, 2, v1);
    if (v2 == cIntListEmptyParam) {
        xsArraySetInt(lst, 0, 2);
        return (lst);
    }
    xsArraySetInt(lst, 3, v2);
    if (v3 == cIntListEmptyParam) {
        xsArraySetInt(lst, 0, 3);
        return (lst);
    }
    xsArraySetInt(lst, 4, v3);
    if (v4 == cIntListEmptyParam) {
        xsArraySetInt(lst, 0, 4);
        return (lst);
    }
    xsArraySetInt(lst, 5, v4);
    if (v5 == cIntListEmptyParam) {
        xsArraySetInt(lst, 0, 5);
        return (lst);
    }
    xsArraySetInt(lst, 6, v5);
    if (v6 == cIntListEmptyParam) {
        xsArraySetInt(lst, 0, 6);
        return (lst);
    }
    xsArraySetInt(lst, 7, v6);
    if (v7 == cIntListEmptyParam) {
        xsArraySetInt(lst, 0, 7);
        return (lst);
    }
    xsArraySetInt(lst, 8, v7);
    if (v8 == cIntListEmptyParam) {
        xsArraySetInt(lst, 0, 8);
        return (lst);
    }
    xsArraySetInt(lst, 9, v8);
    if (v9 == cIntListEmptyParam) {
        xsArraySetInt(lst, 0, 9);
        return (lst);
    }
    xsArraySetInt(lst, 10, v9);
    if (v10 == cIntListEmptyParam) {
        xsArraySetInt(lst, 0, 10);
        return (lst);
    }
    xsArraySetInt(lst, 11, v10);
    if (v11 == cIntListEmptyParam) {
        xsArraySetInt(lst, 0, 11);
        return (lst);
    }
    xsArraySetInt(lst, 12, v11);
    xsArraySetInt(lst, 0, 12);
    return (lst);
}

/*
    Creates empty list for int values. List is a dynamic array that grows and shrinks as values are added and removed.
    @param capacity - initial list capacity
    @return created list id, or error if negative
*/
int xsIntListCreate(int capacity = 7) {
    if ((capacity < 0) || (capacity >= cIntListMaxCapacity)) {
        return (cIntListGenericError);
    }
    int lst = xsArrayCreateInt(capacity + 1);
    if (lst < 0) {
        return (cIntListGenericError);
    }
    xsArraySetInt(lst, 0, 0);
    return (lst);
}

/*
    Creates a list from a given range.
    @param start - Start
    @param stop -
    @param step -
    @return created list id, or error if negative
*/
int xsIntListFromRange(int start = 0, int stop = 0, int step = 1) {
    if (step == 0) {
        return (cIntListGenericError);
    }
    if ((step > 0) && (start > stop)) {
        return (cIntListGenericError);
    }
    if ((step < 0) && (start < stop)) {
        return (cIntListGenericError);
    }
    int distance = 0 + abs(stop - start);
    int stepa = 0 + abs(step);
    int size = distance / stepa;
    if (size >= cIntListMaxCapacity) {
        return (cIntListGenericError);
    }
    int remain = distance % stepa;
    if (remain > 0) {
        size++;
    }
    int lst = xsArrayCreateInt(size + 1);
    if (lst < 0) {
        return (cIntListGenericError);
    }
    int i = 1;
    if (step > 0) {
        while (start < stop) {
            xsArraySetInt(lst, i, start);
            start = start + step;
            i++;
        }
    } else {
        while (start > stop) {
            xsArraySetInt(lst, i, start);
            start = start + step;
            i++;
        }
    }
    xsArraySetInt(lst, 0, size);
    return (lst);
}

int xsIntListFromRepeatedVal(int value = 0, int times = 0) {
    if ((times < 0) || (times >= cIntListMaxCapacity)) {
        return (cIntListGenericError);
    }
    int lst = xsArrayCreateInt(times + 1, value);
    if (lst < 0) {
        return (cIntListGenericError);
    }
    xsArraySetInt(lst, 0, times);
    return (lst);
}

int xsIntListFromRepeatedList(int lst = -1, int times = 0) {
    int size = xsArrayGetInt(lst, 0);
    int newCapacity = (size * times) + 1;
    if (newCapacity > cIntListMaxCapacity) {
        return (cIntListGenericError);
    }
    int newLst = xsArrayCreateInt(newCapacity);
    if (newLst < 0) {
        return (cIntListGenericError);
    }
    for (i = 1; <= size) {
        int val = xsArrayGetInt(lst, i);
        int j = i;
        while (j < newCapacity) {
            xsArraySetInt(newLst, j, val);
            j = j + size;
        }
    }
    xsArraySetInt(newLst, 0, newCapacity - 1);
    return (newLst);
}

int xsIntListFromArray(int arr = -1) {
    int arrSize = xsArrayGetSize(arr);
    int lst = xsIntListCreate(arrSize);
    if (lst < 0) {
        return (lst);
    }
    for (i = 0; < arrSize) {
        xsArraySetInt(lst, i + 1, xsArrayGetInt(arr, i));
    }
    xsArraySetInt(lst, 0, arrSize);
    return (lst);
}

int xsIntListUseArrayAsSource(int arr = -1) {
    int arrSize = xsArrayGetSize(arr);
    if ((arrSize + 1) > cIntListMaxCapacity) {
        return (cIntListMaxCapacityError);
    }
    int r = xsArrayResizeInt(arr, arrSize + 1);
    if (r < 0) {
        return (cIntListResizeFailedError);
    }
    for (i = arrSize - 1; > -1) {
        xsArraySetInt(arr, i + 1, xsArrayGetInt(arr, i));
    }
    xsArraySetInt(arr, 0, arrSize);
    return (cIntListSuccess);
}

int xsIntListGet(int lst = -1, int idx = -1) {
    int size = xsArrayGetInt(lst, 0);
    if ((idx < 0) || (idx >= size)) {
        _intListLastOperationStatus = cIntListIndexOutOfRangeError;
        return (cIntListGenericError);
    }
    _intListLastOperationStatus = cIntListSuccess;
    return (xsArrayGetInt(lst, idx + 1));
}

int xsIntListSet(int lst = -1, int idx = -1, int value = 0) {
    int size = xsArrayGetInt(lst, 0);
    if ((idx < 0) || (idx >= size)) {
        return (cIntListIndexOutOfRangeError);
    }
    xsArraySetInt(lst, idx + 1, value);
    return (cIntListSuccess);
}

int xsIntListSize(int lst = -1) {
    return (xsArrayGetInt(lst, 0));
}

int _xsIntListExtendIntArray(int lst = -1, int capacity = 0) {
    if (capacity == cIntListMaxCapacity) {
        return (cIntListMaxCapacityError);
    }
    int newCapacity = capacity * 2;
    if (newCapacity > cIntListMaxCapacity) {
        newCapacity = cIntListMaxCapacity;
    }
    int r = xsArrayResizeInt(lst, newCapacity);
    if (r != 1) {
        return (cIntListResizeFailedError);
    }
    return (cIntListSuccess);
}

int _xsIntListShrinkIntArray(int lst = -1, int size = 0, int capacity = 0) {
    if (size <= (capacity / 2)) {
        int r = xsArrayResizeInt(lst, size);
        if (r != 1) {
            return (cIntListResizeFailedError);
        }
    }
    return (cIntListSuccess);
}

string xsIntListToString(int lst = -1) {
    int size = xsArrayGetInt(lst, 0);
    string s = "[";
    for (i = 1; <= size) {
        s = s + ("" + xsArrayGetInt(lst, i));
        if (i < size) {
            s = s + ", ";
        }
    }
    s = s + "]";
    return (s);
}

int xsIntListAppend(int lst = -1, int value = 0) {
    int capacity = xsArrayGetSize(lst);
    int size = xsArrayGetInt(lst, 0);
    int nextIdx = size + 1;
    if (capacity == nextIdx) {
        int r = _xsIntListExtendIntArray(lst, capacity);
        if (r != cIntListSuccess) {
            return (r);
        }
    }
    xsArraySetInt(lst, nextIdx, value);
    xsArraySetInt(lst, 0, nextIdx);
    return (cIntListSuccess);
}

int xsIntListPop(int lst = -1, int idx = cIntListMaxCapacity) {
    int capacity = xsArrayGetSize(lst);
    int size = xsArrayGetInt(lst, 0);
    if (idx == cIntListMaxCapacity) {
        idx = size - 1;
    } else if ((idx < 0) || (idx >= size)) {
        _intListLastOperationStatus = cIntListIndexOutOfRangeError;
        return (cIntListGenericError);
    }
    int removedElem = xsArrayGetInt(lst, idx + 1);
    for (i = idx + 2; <= size) {
        xsArraySetInt(lst, i - 1, xsArrayGetInt(lst, i));
    }
    int r = _xsIntListShrinkIntArray(lst, size, capacity);
    if (r != cIntListSuccess) {
        _intListLastOperationStatus = r;
        return (cIntListGenericError);
    }
    xsArraySetInt(lst, 0, size - 1);
    _intListLastOperationStatus = cIntListSuccess;
    return (removedElem);
}

int xsIntListInsert(int lst = -1, int idx = -1, int value = 0) {
    int capacity = xsArrayGetSize(lst);
    int size = xsArrayGetInt(lst, 0);
    if ((idx < 0) || (idx > size)) {
        return (cIntListIndexOutOfRangeError);
    }
    int newSize = size + 1;
    if (capacity == newSize) {
        int r = _xsIntListExtendIntArray(lst, capacity);
        if (r != cIntListSuccess) {
            return (r);
        }
    }
    for (i = size; > idx) {
        xsArraySetInt(lst, i + 1, xsArrayGetInt(lst, i));
    }
    xsArraySetInt(lst, idx + 1, value);
    xsArraySetInt(lst, 0, newSize);
    return (cIntListSuccess);
}

int xsIntListRemove(int lst = -1, int value = -1) {
    int capacity = xsArrayGetSize(lst);
    int size = xsArrayGetInt(lst, 0);
    int foundIdx = -1;
    int i = 1;
    while ((i <= size) && (foundIdx == -1)) {
        int cVal = xsArrayGetInt(lst, i);
        if (cVal == value) {
            foundIdx = i;
        }
        i++;
    }
    if (foundIdx == -1) {
        return (cIntListGenericError);
    }
    for (j = foundIdx + 1; <= size) {
        xsArraySetInt(lst, j - 1, xsArrayGetInt(lst, j));
    }
    int r = _xsIntListShrinkIntArray(lst, size, capacity);
    if (r != cIntListSuccess) {
        return (r);
    }
    xsArraySetInt(lst, 0, size - 1);
    return (foundIdx - 1);
}

int xsIntListIndex(int lst = -1, int value = -1, int start = 0, int stop = cIntListEmptyParam) {
    int size = xsArrayGetInt(lst, 0);
    if ((stop == cIntListEmptyParam) || (stop > size)) {
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
        if (xsArrayGetInt(lst, i + 1) == value) {
            return (i);
        }
    }
    return (cIntListGenericError);
}

bool xsIntListContains(int lst = -1, int value = -1) {
    return (xsIntListIndex(lst, value) > -1);
}

bool _xsIntListCompareElem(int a = -1, int b = -1, bool reverse = false) {
    if (reverse) {
        return (a > b);
    }
    return (a < b);
}

void _xsIntListSiftDown(int lst = -1, int start = -1, int end = -1, bool reverse = false) {
    int root = start;
    while (true) {
        int child = 2 * root;
        if (child > end) {
            return;
        }
        int childVal = xsArrayGetInt(lst, child);
        int childVal1 = xsArrayGetInt(lst, child + 1);
        if (((child + 1) <= end) && _xsIntListCompareElem(childVal, childVal1, reverse)) {
            child++;
            childVal = childVal1;
        }
        int rootVal = xsArrayGetInt(lst, root);
        if (_xsIntListCompareElem(rootVal, childVal, reverse)) {
            xsArraySetInt(lst, root, childVal);
            xsArraySetInt(lst, child, rootVal);
            root = child;
        } else {
            return;
        }
    }
}

void xsIntListSort(int lst = -1, bool reverse = false) {
    int size = xsArrayGetInt(lst, 0);
    for (start = size / 2; > 0) {
        _xsIntListSiftDown(lst, start, size, reverse);
    }
    for (end = size; > 1) {
        int temp = xsArrayGetInt(lst, 1);
        xsArraySetInt(lst, 1, xsArrayGetInt(lst, end));
        xsArraySetInt(lst, end, temp);
        _xsIntListSiftDown(lst, 1, end - 1, reverse);
    }
}

int xsIntListClear(int lst = -1) {
    int capacity = xsArrayGetInt(lst, 0);
    if (capacity > 8) {
        int r = xsArrayResizeInt(lst, 8);
        if (r != 1) {
            return (cIntListResizeFailedError);
        }
    }
    xsArraySetInt(lst, 0, 0);
    return (cIntListSuccess);
}

int xsIntListCopy(int lst = -1, int start = 0, int end = cIntListMaxCapacity) {
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
    int newLst = xsArrayCreateInt(newSize + 1);
    if (newLst < 0) {
        return (cIntListGenericError);
    }
    for (i = fr; <= to) {
        xsArraySetInt(newLst, i - fr, xsArrayGetInt(lst, i));
    }
    xsArraySetInt(newLst, 0, newSize);
    return (newLst);
}

int xsIntListExtend(int source = -1, int lst = -1) {
    int sourceSize = xsArrayGetInt(source, 0);
    int toAdd = xsArrayGetInt(lst, 0);
    int capacity = xsArrayGetSize(source);
    int newSize = sourceSize + toAdd;
    if (newSize > capacity) {
        if (newSize >= cIntListMaxCapacity) {
            return (cIntListMaxCapacityError);
        }
        int r = xsArrayResizeInt(source, newSize + 1);
        if (r != 1) {
            return (cIntListResizeFailedError);
        }
    }
    for (i = 1; <= toAdd) {
        xsArraySetInt(source, i + sourceSize, xsArrayGetInt(lst, i));
    }
    xsArraySetInt(source, 0, newSize);
    return (cIntListSuccess);
}

int xsIntListExtendWithArray(int source = -1, int arr = -1) {
    int sourceSize = xsArrayGetInt(source, 0);
    int toAdd = xsArrayGetSize(arr);
    int capacity = xsArrayGetSize(source);
    int newSize = sourceSize + toAdd;
    if (newSize > capacity) {
        if ((newSize >= cIntListMaxCapacity) || (newSize < 0)) {
            return (cIntListMaxCapacityError);
        }
        int r = xsArrayResizeInt(source, newSize + 1);
        if (r != 1) {
            return (cIntListResizeFailedError);
        }
    }
    for (i = 0; < toAdd) {
        xsArraySetInt(source, (i + sourceSize) + 1, xsArrayGetInt(arr, i));
    }
    xsArraySetInt(source, 0, newSize);
    return (cIntListSuccess);
}

int xsIntListCompare(int lst1 = -1, int lst2 = -1) {
    int size1 = xsArrayGetInt(lst1, 0);
    int size2 = xsArrayGetInt(lst2, 0);
    int i = 1;
    while ((i <= size1) && (i <= size2)) {
        int v1 = xsArrayGetInt(lst1, i);
        int v2 = xsArrayGetInt(lst2, i);
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

int xsIntListCount(int lst = -1, int value = -1) {
    int count = 0;
    int size = xsArrayGetInt(lst, 0);
    for (i = 1; <= size) {
        if (xsArrayGetInt(lst, i) == value) {
            count++;
        }
    }
    return (count);
}

int xsIntListSum(int lst = -1) {
    int s = 0;
    int size = xsArrayGetInt(lst, 0);
    for (i = 1; <= size) {
        s = s + xsArrayGetInt(lst, i);
    }
    return (s);
}

int xsIntListMin(int lst = -1) {
    int size = xsArrayGetInt(lst, 0);
    if (size == 0) {
        _intListLastOperationStatus = cIntListIndexOutOfRangeError;
        return (cIntListGenericError);
    }
    int m = xsArrayGetInt(lst, 1);
    if (size == 1) {
        _intListLastOperationStatus = cIntListSuccess;
        return (m);
    }
    for (i = 2; <= size) {
        int v = xsArrayGetInt(lst, i);
        if (v < m) {
            m = v;
        }
    }
    _intListLastOperationStatus = cIntListSuccess;
    return (m);
}

int xsIntListMax(int lst = -1) {
    int size = xsArrayGetInt(lst, 0);
    if (size == 0) {
        _intListLastOperationStatus = cIntListIndexOutOfRangeError;
        return (cIntListGenericError);
    }
    int m = xsArrayGetInt(lst, 1);
    if (size == 1) {
        _intListLastOperationStatus = cIntListSuccess;
        return (m);
    }
    for (i = 2; <= size) {
        int v = xsArrayGetInt(lst, i);
        if (v > m) {
            m = v;
        }
    }
    _intListLastOperationStatus = cIntListSuccess;
    return (m);
}

int xsIntListLastError() {
    return (_intListLastOperationStatus);
}

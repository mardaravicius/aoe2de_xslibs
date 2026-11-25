extern const int cIntArraySuccess = 0;
extern const int cIntArrayGenericError = -1;
extern const int cIntArrayIndexOutOfRangeError = -2;
extern const int cIntArrayResizeFailedError = -3;
extern const int cIntArrayMaxCapacityError = -4;
extern const int cIntArrayMaxCapacity = 999999999;
extern const int cIntArrayEmptyParam = -999999999;
int _cIntArrayIntMax = -1;
int _cIntArrayIntMin = -1;
int _intArrayLastOperationStatus = cIntArraySuccess;
const int _cIntArraySortRun = 16;
int _intArraySortKeys = -1;
int _intArraySortValues = -1;

/*
    Creates an array with provided values. The first value that equals `cIntArrayEmptyParam` will stop further insertion.
    This Function can create an array with 12 values at the maximum.
    @param v0 through v11 - value at a given index of an array
    @return created array id, or `cIntArrayGenericError` on error
*/
int xsIntArray(int v0 = cIntArrayEmptyParam, int v1 = cIntArrayEmptyParam, int v2 = cIntArrayEmptyParam, int v3 = cIntArrayEmptyParam, int v4 = cIntArrayEmptyParam, int v5 = cIntArrayEmptyParam, int v6 = cIntArrayEmptyParam, int v7 = cIntArrayEmptyParam, int v8 = cIntArrayEmptyParam, int v9 = cIntArrayEmptyParam, int v10 = cIntArrayEmptyParam, int v11 = cIntArrayEmptyParam) {
    int size = 12;
    if (v0 == cIntArrayEmptyParam) {
        size = 0;
    } else if (v1 == cIntArrayEmptyParam) {
        size = 1;
    } else if (v2 == cIntArrayEmptyParam) {
        size = 2;
    } else if (v3 == cIntArrayEmptyParam) {
        size = 3;
    } else if (v4 == cIntArrayEmptyParam) {
        size = 4;
    } else if (v5 == cIntArrayEmptyParam) {
        size = 5;
    } else if (v6 == cIntArrayEmptyParam) {
        size = 6;
    } else if (v7 == cIntArrayEmptyParam) {
        size = 7;
    } else if (v8 == cIntArrayEmptyParam) {
        size = 8;
    } else if (v9 == cIntArrayEmptyParam) {
        size = 9;
    } else if (v10 == cIntArrayEmptyParam) {
        size = 10;
    } else if (v11 == cIntArrayEmptyParam) {
        size = 11;
    }
    int arr = xsArrayCreateInt(size);
    if (arr < 0) {
        return (cIntArrayGenericError);
    }
    if (size == 0) {
        return (arr);
    }
    xsArraySetInt(arr, 0, v0);
    if (size == 1) {
        return (arr);
    }
    xsArraySetInt(arr, 1, v1);
    if (size == 2) {
        return (arr);
    }
    xsArraySetInt(arr, 2, v2);
    if (size == 3) {
        return (arr);
    }
    xsArraySetInt(arr, 3, v3);
    if (size == 4) {
        return (arr);
    }
    xsArraySetInt(arr, 4, v4);
    if (size == 5) {
        return (arr);
    }
    xsArraySetInt(arr, 5, v5);
    if (size == 6) {
        return (arr);
    }
    xsArraySetInt(arr, 6, v6);
    if (size == 7) {
        return (arr);
    }
    xsArraySetInt(arr, 7, v7);
    if (size == 8) {
        return (arr);
    }
    xsArraySetInt(arr, 8, v8);
    if (size == 9) {
        return (arr);
    }
    xsArraySetInt(arr, 9, v9);
    if (size == 10) {
        return (arr);
    }
    xsArraySetInt(arr, 10, v10);
    if (size == 11) {
        return (arr);
    }
    xsArraySetInt(arr, 11, v11);
    return (arr);
}

int _xsIntArrayIntAbs(int n = 0) {
    if (n < 0) {
        return (n * -1);
    }
    return (n);
}

/*
    Creates an array from a given range.
    @param start - start of range (inclusive)
    @param stop - end of range (exclusive)
    @param step - increment between values (positive or negative, must not be zero)
    @return created array id, or `cIntArrayGenericError` on error
*/
int xsIntArrayFromRange(int start = 0, int stop = 0, int step = 1) {
    if (_cIntArrayIntMin == -1) {
        _cIntArrayIntMin = -214748364 * 10 - 8;
        _cIntArrayIntMax = 214748364 * 10 + 7;
    }
    if ((step == 0) || (step == _cIntArrayIntMin)) {
        return (cIntArrayGenericError);
    }
    int distance = 0;
    if (step > 0) {
        if (start > stop) {
            return (cIntArrayGenericError);
        }
        if ((start < 0) && (stop >= 0) && (stop > (_cIntArrayIntMax + start))) {
            return (cIntArrayGenericError);
        }
        distance = stop - start;
    } else {
        if (start < stop) {
            return (cIntArrayGenericError);
        }
        if ((start >= 0) && (stop < 0) && (start > (_cIntArrayIntMax + stop))) {
            return (cIntArrayGenericError);
        }
        distance = start - stop;
    }
    int stepA = _xsIntArrayIntAbs(step);
    int size = distance / stepA;
    if (size >= cIntArrayMaxCapacity) {
        return (cIntArrayGenericError);
    }
    if ((distance % stepA) > 0) {
        size++;
    }
    int arr = xsArrayCreateInt(size);
    if (arr < 0) {
        return (cIntArrayGenericError);
    }
    int i = 0;
    int current = start;
    while (i < size) {
        xsArraySetInt(arr, i, current);
        if (i < (size - 1)) {
            current = current + step;
        }
        i++;
    }
    return (arr);
}

/*
    Creates an array by repeating a single value.
    @param value - value to repeat
    @param times - number of times to repeat the value
    @return created array id, or `cIntArrayGenericError` on error
*/
int xsIntArrayFromRepeatedVal(int value = 0, int times = 0) {
    if ((times < 0) || (times >= cIntArrayMaxCapacity)) {
        return (cIntArrayGenericError);
    }
    int arr = xsArrayCreateInt(times, value);
    if (arr < 0) {
        return (cIntArrayGenericError);
    }
    return (arr);
}

/*
    Creates a new array by repeating all elements of the given array.
    @param arr - source array id
    @param times - number of times to repeat the array contents
    @return created array id, `cIntArrayMaxCapacityError` if the result is too large, or `cIntArrayGenericError` on other errors
*/
int xsIntArrayFromRepeatedArray(int arr = -1, int times = 0) {
    if (times < 0) {
        return (cIntArrayGenericError);
    }
    int size = xsArrayGetSize(arr);
    if ((times > 0) && (size > (cIntArrayMaxCapacity / times))) {
        return (cIntArrayMaxCapacityError);
    }
    int newSize = size * times;
    if (newSize >= cIntArrayMaxCapacity) {
        return (cIntArrayMaxCapacityError);
    }
    int newArr = xsArrayCreateInt(newSize);
    if (newArr < 0) {
        return (cIntArrayGenericError);
    }
    for (i = 0; < size) {
        int val = xsArrayGetInt(arr, i);
        int j = i;
        while (j < newSize) {
            xsArraySetInt(newArr, j, val);
            j = j + size;
        }
    }
    return (newArr);
}

/*
    Returns the index of the first occurrence of the value within the optional [start, stop) range. Negative start/stop are relative to the end.
    @param arr - array id
    @param value - value to search for
    @param start - start of search range (inclusive)
    @param stop - end of search range (exclusive), defaults to array size
    @return index of the value, or `cIntArrayGenericError` if not found
*/
int xsIntArrayIndex(int arr = -1, int value = -1, int start = 0, int stop = cIntArrayEmptyParam) {
    int size = xsArrayGetSize(arr);
    if ((stop == cIntArrayEmptyParam) || (stop > size)) {
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
        if (xsArrayGetInt(arr, i) == value) {
            return (i);
        }
    }
    return (cIntArrayGenericError);
}

/*
    Checks whether the array contains the given value.
    @param arr - array id
    @param value - value to search for
    @return true if the value is found, false otherwise
*/
bool xsIntArrayContains(int arr = -1, int value = -1) {
    return (xsIntArrayIndex(arr, value) > -1);
}

bool _xsIntArrayCompareElem(int a = -1, int b = -1, bool reverse = false) {
    if (reverse) {
        return (a > b);
    }
    return (a < b);
}

void _xsIntArrayInsertionSortWith(int arr = -1, int other = -1, int lo = 0, int hi = 0, bool reverse = false) {
    bool hasOther = other >= 0;
    for (i = lo + 1; < hi) {
        int key = xsArrayGetInt(arr, i);
        int value = 0;
        if (hasOther) {
            value = xsArrayGetInt(other, i);
        }
        int j = i - 1;
        bool shifting = true;
        while (shifting && (j >= lo)) {
            int prev = xsArrayGetInt(arr, j);
            if (_xsIntArrayCompareElem(key, prev, reverse)) {
                xsArraySetInt(arr, j + 1, prev);
                if (hasOther) {
                    xsArraySetInt(other, j + 1, xsArrayGetInt(other, j));
                }
                j--;
            } else {
                shifting = false;
            }
        }
        xsArraySetInt(arr, j + 1, key);
        if (hasOther) {
            xsArraySetInt(other, j + 1, value);
        }
    }
}

void _xsIntArraySiftDown(int arr = -1, int start = -1, int end = -1, bool reverse = false) {
    int root = start;
    int val = xsArrayGetInt(arr, root);
    bool sifting = true;
    while (sifting) {
        int child = (2 * root) + 1;
        if (child > end) {
            sifting = false;
        } else {
            int childVal = xsArrayGetInt(arr, child);
            if ((child + 1) <= end) {
                int childVal1 = xsArrayGetInt(arr, child + 1);
                if (_xsIntArrayCompareElem(childVal, childVal1, reverse)) {
                    child++;
                    childVal = childVal1;
                }
            }
            if (_xsIntArrayCompareElem(val, childVal, reverse)) {
                xsArraySetInt(arr, root, childVal);
                root = child;
            } else {
                sifting = false;
            }
        }
    }
    xsArraySetInt(arr, root, val);
}

/*
    Sorts the array in-place.
    @param arr - array id
    @param reverse - if true, sorts in descending order
*/
void xsIntArraySort(int arr = -1, bool reverse = false) {
    int size = xsArrayGetSize(arr);
    if (size <= _cIntArraySortRun) {
        _xsIntArrayInsertionSortWith(arr, -1, 0, size, reverse);
        return;
    }
    for (start = (size / 2) - 1; > -1) {
        _xsIntArraySiftDown(arr, start, size - 1, reverse);
    }
    for (end = size - 1; > 0) {
        int temp = xsArrayGetInt(arr, 0);
        xsArraySetInt(arr, 0, xsArrayGetInt(arr, end));
        xsArraySetInt(arr, end, temp);
        _xsIntArraySiftDown(arr, 0, end - 1, reverse);
    }
}

int _xsIntArrayEnsureSortBuffers(int size = 0) {
    if (_intArraySortKeys < 0) {
        _intArraySortKeys = xsArrayCreateInt(size);
        if (_intArraySortKeys < 0) {
            return (cIntArrayGenericError);
        }
    }
    if (_intArraySortValues < 0) {
        _intArraySortValues = xsArrayCreateInt(size);
        if (_intArraySortValues < 0) {
            return (cIntArrayGenericError);
        }
    }
    int r = 1;
    if (xsArrayGetSize(_intArraySortKeys) < size) {
        r = xsArrayResizeInt(_intArraySortKeys, size);
        if (r != 1) {
            return (cIntArrayResizeFailedError);
        }
    }
    if (xsArrayGetSize(_intArraySortValues) < size) {
        r = xsArrayResizeInt(_intArraySortValues, size);
        if (r != 1) {
            return (cIntArrayResizeFailedError);
        }
    }
    return (cIntArraySuccess);
}

void _xsIntArrayReleaseSortBuffers(bool releaseBuffers = true) {
    if (releaseBuffers == false) {
        return;
    }
    if (_intArraySortKeys >= 0) {
        xsArrayResizeInt(_intArraySortKeys, 0);
    }
    if (_intArraySortValues >= 0) {
        xsArrayResizeInt(_intArraySortValues, 0);
    }
}

void _xsIntArrayMergeWith(int src = -1, int srcOther = -1, int dst = -1, int dstOther = -1, int lo = 0, int mid = 0, int hi = 0, bool reverse = false) {
    int i = lo;
    int j = mid;
    int k = lo;
    if ((i < mid) && (j < hi)) {
        int left = xsArrayGetInt(src, i);
        int right = xsArrayGetInt(src, j);
        while ((i < mid) && (j < hi)) {
            if (_xsIntArrayCompareElem(right, left, reverse)) {
                xsArraySetInt(dst, k, right);
                xsArraySetInt(dstOther, k, xsArrayGetInt(srcOther, j));
                j++;
                if (j < hi) {
                    right = xsArrayGetInt(src, j);
                }
            } else {
                xsArraySetInt(dst, k, left);
                xsArraySetInt(dstOther, k, xsArrayGetInt(srcOther, i));
                i++;
                if (i < mid) {
                    left = xsArrayGetInt(src, i);
                }
            }
            k++;
        }
    }
    while (i < mid) {
        xsArraySetInt(dst, k, xsArrayGetInt(src, i));
        xsArraySetInt(dstOther, k, xsArrayGetInt(srcOther, i));
        i++;
        k++;
    }
    while (j < hi) {
        xsArraySetInt(dst, k, xsArrayGetInt(src, j));
        xsArraySetInt(dstOther, k, xsArrayGetInt(srcOther, j));
        j++;
        k++;
    }
}

/*
    Sorts the array in-place with a stable sort, and moves the elements of `other` the same way,
    so `other[i]` stays paired with `arr[i]`. Equal elements keep their original order.
    Inputs larger than 16 elements use two internal buffer arrays shared by all calls.
    @param arr - array id
    @param other - int array id of the same size as `arr`
    @param reverse - if true, sorts in descending order
    @param release_buffers - if true, resizes the internal buffers to 0 after sorting to free their memory;
        the same buffers are grown again on the next call
    @return `cIntArraySuccess` on success, `cIntArrayGenericError` if the sizes differ or buffers
        can't be created, or `cIntArrayResizeFailedError` if the buffers can't grow
*/
int xsIntArraySortWith(int arr = -1, int other = -1, bool reverse = false, bool releaseBuffers = true) {
    int size = xsArrayGetSize(arr);
    if (xsArrayGetSize(other) != size) {
        return (cIntArrayGenericError);
    }
    if (size > _cIntArraySortRun) {
        int r = _xsIntArrayEnsureSortBuffers(size);
        if (r != cIntArraySuccess) {
            _xsIntArrayReleaseSortBuffers(releaseBuffers);
            return (r);
        }
    }
    int runStart = 0;
    while (runStart < size) {
        int runEnd = runStart + _cIntArraySortRun;
        if (runEnd > size) {
            runEnd = size;
        }
        _xsIntArrayInsertionSortWith(arr, other, runStart, runEnd, reverse);
        runStart = runEnd;
    }
    if (size <= _cIntArraySortRun) {
        return (cIntArraySuccess);
    }
    int src = arr;
    int srcOther = other;
    int dst = _intArraySortKeys;
    int dstOther = _intArraySortValues;
    bool inBuffers = false;
    int width = _cIntArraySortRun;
    while (width < size) {
        int lo = 0;
        while (lo < size) {
            int mid = lo + width;
            if (mid > size) {
                mid = size;
            }
            int hi = mid + width;
            if (hi > size) {
                hi = size;
            }
            _xsIntArrayMergeWith(src, srcOther, dst, dstOther, lo, mid, hi, reverse);
            lo = hi;
        }
        int temp = src;
        src = dst;
        dst = temp;
        temp = srcOther;
        srcOther = dstOther;
        dstOther = temp;
        inBuffers = inBuffers == false;
        width = width * 2;
    }
    if (inBuffers) {
        for (i = 0; < size) {
            xsArraySetInt(arr, i, xsArrayGetInt(src, i));
            xsArraySetInt(other, i, xsArrayGetInt(srcOther, i));
        }
    }
    _xsIntArrayReleaseSortBuffers(releaseBuffers);
    return (cIntArraySuccess);
}

/*
    Returns a string representation of the array, by default in the format `[v0, v1, ...]`.
    @param arr - array id
    @param start - string prepended to the output
    @param sep - separator between elements
    @param end - string appended to the output
    @return string representation of the array
*/
string xsIntArrayToString(int arr = -1, string start = "[", string sep = ", ", string end = "]") {
    int size = xsArrayGetSize(arr);
    string s = start;
    for (i = 0; < size) {
        s = s + ("" + xsArrayGetInt(arr, i));
        if (i < (size - 1)) {
            s = s + sep;
        }
    }
    s = s + end;
    return (s);
}

/*
    Returns a copy of the array, optionally sliced by [start, end). Negative start/end are relative to the end.
    @param arr - array id
    @param start - start of slice (inclusive)
    @param end - end of slice (exclusive), defaults to array size
    @return new array id, or `cIntArrayGenericError` on error
*/
int xsIntArrayCopy(int arr = -1, int start = 0, int end = cIntArrayMaxCapacity) {
    int size = xsArrayGetSize(arr);
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
    int newArr = xsArrayCreateInt(newSize);
    if (newArr < 0) {
        return (cIntArrayGenericError);
    }
    for (i = fr; < to) {
        xsArraySetInt(newArr, i - fr, xsArrayGetInt(arr, i));
    }
    return (newArr);
}

/*
    Resizes the array to 0 to free its memory. XS can't fully delete arrays,
    so the array id stays allocated and must not be used afterwards.
    @param arr - array id
    @return `cIntArraySuccess` on success, or `cIntArrayResizeFailedError` if the resize fails
*/
int xsIntArrayDelete(int arr = -1) {
    int r = xsArrayResizeInt(arr, 0);
    if (r != 1) {
        return (cIntArrayResizeFailedError);
    }
    return (cIntArraySuccess);
}

/*
    Performs lexicographic comparison of two arrays.
    @param arr1 - first array id
    @param arr2 - second array id
    @return -1 if arr1 < arr2, 1 if arr1 > arr2, 0 if equal
*/
int xsIntArrayCompare(int arr1 = -1, int arr2 = -1) {
    int size1 = xsArrayGetSize(arr1);
    int size2 = xsArrayGetSize(arr2);
    int i = 0;
    while ((i < size1) && (i < size2)) {
        int v1 = xsArrayGetInt(arr1, i);
        int v2 = xsArrayGetInt(arr2, i);
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

/*
    Reverses the array in-place.
    @param arr - array id
*/
void xsIntArrayReverse(int arr = -1) {
    int size = xsArrayGetSize(arr);
    int mid = size / 2;
    for (i = 0; < mid) {
        int temp = xsArrayGetInt(arr, i);
        int backI = (size - i) - 1;
        xsArraySetInt(arr, i, xsArrayGetInt(arr, backI));
        xsArraySetInt(arr, backI, temp);
    }
}

/*
    Counts the number of occurrences of a value in the array.
    @param arr - array id
    @param value - value to count
    @return number of occurrences
*/
int xsIntArrayCount(int arr = -1, int value = -1) {
    int count = 0;
    int size = xsArrayGetSize(arr);
    for (i = 0; < size) {
        if (xsArrayGetInt(arr, i) == value) {
            count++;
        }
    }
    return (count);
}

/*
    Returns the sum of all elements in the array.
    @param arr - array id
    @return sum of elements
*/
int xsIntArraySum(int arr = -1) {
    int s = 0;
    int size = xsArrayGetSize(arr);
    for (i = 0; < size) {
        s = s + xsArrayGetInt(arr, i);
    }
    return (s);
}

/*
    Returns the minimum value in the array. Sets last error on failure.
    @param arr - array id
    @return minimum value, or `cIntArrayGenericError` on error
*/
int xsIntArrayMin(int arr = -1) {
    int size = xsArrayGetSize(arr);
    if (size <= 0) {
        _intArrayLastOperationStatus = cIntArrayIndexOutOfRangeError;
        return (cIntArrayGenericError);
    }
    int m = xsArrayGetInt(arr, 0);
    for (i = 1; < size) {
        int v = xsArrayGetInt(arr, i);
        if (v < m) {
            m = v;
        }
    }
    _intArrayLastOperationStatus = cIntArraySuccess;
    return (m);
}

/*
    Returns the maximum value in the array. Sets last error on failure.
    @param arr - array id
    @return maximum value, or `cIntArrayGenericError` on error
*/
int xsIntArrayMax(int arr = -1) {
    int size = xsArrayGetSize(arr);
    if (size <= 0) {
        _intArrayLastOperationStatus = cIntArrayIndexOutOfRangeError;
        return (cIntArrayGenericError);
    }
    int m = xsArrayGetInt(arr, 0);
    for (i = 1; < size) {
        int v = xsArrayGetInt(arr, i);
        if (v > m) {
            m = v;
        }
    }
    _intArrayLastOperationStatus = cIntArraySuccess;
    return (m);
}

/*
    Returns the status code of the last operation that sets it (min, max).
    @return `cIntArraySuccess` if the last such operation succeeded, or a negative error code
*/
int xsIntArrayLastError() {
    return (_intArrayLastOperationStatus);
}

/*
    Creates an array from a comma separated string, e.g. `"1,2,3"`.
    Items are trimmed, and items that cannot be parsed are skipped.
    @param items - comma separated values
    @return created array id, or `cIntArrayGenericError` on error
*/
int xsIntArrayFromString(string items = "") {
    if (strTrim(items) == "") {
        return (xsArrayCreateInt(0));
    }
    int parts = strSplit(items, ",");
    int numParts = xsArrayGetSize(parts);
    int arr = xsArrayCreateInt(numParts);
    if (arr < 0) {
        xsArrayResizeString(parts, 0);
        return (cIntArrayGenericError);
    }
    int size = 0;
    for (i = 0; < numParts) {
        string item = strTrim(xsArrayGetString(parts, i));
        int value = strToInt(item, 10, cIntArrayEmptyParam);
        if (value != cIntArrayEmptyParam) {
            xsArraySetInt(arr, size, value);
            size++;
        }
    }
    xsArrayResizeString(parts, 0);
    if (size < numParts) {
        int r = xsArrayResizeInt(arr, size);
        if (r != 1) {
            return (cIntArrayResizeFailedError);
        }
    }
    return (arr);
}

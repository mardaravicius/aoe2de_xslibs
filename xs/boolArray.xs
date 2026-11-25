extern const int cBoolArraySuccess = 0;
extern const int cBoolArrayGenericError = -1;
extern const int cBoolArrayResizeFailedError = -3;
extern const int cBoolArrayMaxCapacityError = -4;
extern const int cBoolArrayMaxCapacity = 999999999;
extern const int cBoolArrayEmptyIntParam = -999999999;
const int _cBoolArraySortRun = 16;
int _boolArraySortKeys = -1;
int _boolArraySortValues = -1;

/*
    Creates an array by repeating a single value.
    @param value - value to repeat
    @param times - number of times to repeat the value
    @return created array id, or `cBoolArrayGenericError` on error
*/
int xsBoolArrayFromRepeatedVal(bool value = false, int times = 0) {
    if ((times < 0) || (times >= cBoolArrayMaxCapacity)) {
        return (cBoolArrayGenericError);
    }
    int arr = xsArrayCreateBool(times, value);
    if (arr < 0) {
        return (cBoolArrayGenericError);
    }
    return (arr);
}

/*
    Creates a new array by repeating all elements of the given array.
    @param arr - source array id
    @param times - number of times to repeat the array contents
    @return created array id, `cBoolArrayMaxCapacityError` if the result is too large, or `cBoolArrayGenericError` on other errors
*/
int xsBoolArrayFromRepeatedArray(int arr = -1, int times = 0) {
    if (times < 0) {
        return (cBoolArrayGenericError);
    }
    int size = xsArrayGetSize(arr);
    if ((times > 0) && (size > (cBoolArrayMaxCapacity / times))) {
        return (cBoolArrayMaxCapacityError);
    }
    int newSize = size * times;
    if (newSize >= cBoolArrayMaxCapacity) {
        return (cBoolArrayMaxCapacityError);
    }
    int newArr = xsArrayCreateBool(newSize);
    if (newArr < 0) {
        return (cBoolArrayGenericError);
    }
    for (i = 0; < size) {
        bool val = xsArrayGetBool(arr, i);
        int j = i;
        while (j < newSize) {
            xsArraySetBool(newArr, j, val);
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
    @return index of the value, or `cBoolArrayGenericError` if not found
*/
int xsBoolArrayIndex(int arr = -1, bool value = false, int start = 0, int stop = cBoolArrayEmptyIntParam) {
    int size = xsArrayGetSize(arr);
    if ((stop == cBoolArrayEmptyIntParam) || (stop > size)) {
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
        if (xsArrayGetBool(arr, i) == value) {
            return (i);
        }
    }
    return (cBoolArrayGenericError);
}

/*
    Checks whether the array contains the given value.
    @param arr - array id
    @param value - value to search for
    @return true if the value is found, false otherwise
*/
bool xsBoolArrayContains(int arr = -1, bool value = false) {
    return (xsBoolArrayIndex(arr, value) > -1);
}

bool _xsBoolArrayCompareElem(bool a = false, bool b = false, bool reverse = false) {
    if (reverse) {
        return (a && (b == false));
    }
    return ((a == false) && b);
}

/*
    Sorts the array in-place.
    @param arr - array id
    @param reverse - if true, sorts in descending order
*/
void xsBoolArraySort(int arr = -1, bool reverse = false) {
    int size = xsArrayGetSize(arr);
    int numTrues = 0;
    for (i = 0; < size) {
        if (xsArrayGetBool(arr, i)) {
            numTrues++;
        }
    }
    int split = size - numTrues;
    if (reverse) {
        split = numTrues;
    }
    for (j = 0; < split) {
        xsArraySetBool(arr, j, reverse);
    }
    for (k = split; < size) {
        xsArraySetBool(arr, k, reverse == false);
    }
}

int _xsBoolArrayEnsureSortBuffers(int size = 0) {
    if (_boolArraySortKeys < 0) {
        _boolArraySortKeys = xsArrayCreateBool(size);
        if (_boolArraySortKeys < 0) {
            return (cBoolArrayGenericError);
        }
    }
    if (_boolArraySortValues < 0) {
        _boolArraySortValues = xsArrayCreateInt(size);
        if (_boolArraySortValues < 0) {
            return (cBoolArrayGenericError);
        }
    }
    int r = 1;
    if (xsArrayGetSize(_boolArraySortKeys) < size) {
        r = xsArrayResizeBool(_boolArraySortKeys, size);
        if (r != 1) {
            return (cBoolArrayResizeFailedError);
        }
    }
    if (xsArrayGetSize(_boolArraySortValues) < size) {
        r = xsArrayResizeInt(_boolArraySortValues, size);
        if (r != 1) {
            return (cBoolArrayResizeFailedError);
        }
    }
    return (cBoolArraySuccess);
}

void _xsBoolArrayReleaseSortBuffers(bool releaseBuffers = true) {
    if (releaseBuffers == false) {
        return;
    }
    if (_boolArraySortKeys >= 0) {
        xsArrayResizeBool(_boolArraySortKeys, 0);
    }
    if (_boolArraySortValues >= 0) {
        xsArrayResizeInt(_boolArraySortValues, 0);
    }
}

void _xsBoolArrayInsertionSortWith(int arr = -1, int other = -1, int lo = 0, int hi = 0, bool reverse = false) {
    for (i = lo + 1; < hi) {
        bool key = xsArrayGetBool(arr, i);
        int value = xsArrayGetInt(other, i);
        int j = i - 1;
        bool shifting = true;
        while (shifting && (j >= lo)) {
            bool prev = xsArrayGetBool(arr, j);
            if (_xsBoolArrayCompareElem(key, prev, reverse)) {
                xsArraySetBool(arr, j + 1, prev);
                xsArraySetInt(other, j + 1, xsArrayGetInt(other, j));
                j--;
            } else {
                shifting = false;
            }
        }
        xsArraySetBool(arr, j + 1, key);
        xsArraySetInt(other, j + 1, value);
    }
}

void _xsBoolArrayMergeWith(int src = -1, int srcOther = -1, int dst = -1, int dstOther = -1, int lo = 0, int mid = 0, int hi = 0, bool reverse = false) {
    int i = lo;
    int j = mid;
    int k = lo;
    if ((i < mid) && (j < hi)) {
        bool left = xsArrayGetBool(src, i);
        bool right = xsArrayGetBool(src, j);
        while ((i < mid) && (j < hi)) {
            if (_xsBoolArrayCompareElem(right, left, reverse)) {
                xsArraySetBool(dst, k, right);
                xsArraySetInt(dstOther, k, xsArrayGetInt(srcOther, j));
                j++;
                if (j < hi) {
                    right = xsArrayGetBool(src, j);
                }
            } else {
                xsArraySetBool(dst, k, left);
                xsArraySetInt(dstOther, k, xsArrayGetInt(srcOther, i));
                i++;
                if (i < mid) {
                    left = xsArrayGetBool(src, i);
                }
            }
            k++;
        }
    }
    while (i < mid) {
        xsArraySetBool(dst, k, xsArrayGetBool(src, i));
        xsArraySetInt(dstOther, k, xsArrayGetInt(srcOther, i));
        i++;
        k++;
    }
    while (j < hi) {
        xsArraySetBool(dst, k, xsArrayGetBool(src, j));
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
    @return `cBoolArraySuccess` on success, `cBoolArrayGenericError` if the sizes differ or buffers
        can't be created, or `cBoolArrayResizeFailedError` if the buffers can't grow
*/
int xsBoolArraySortWith(int arr = -1, int other = -1, bool reverse = false, bool releaseBuffers = true) {
    int size = xsArrayGetSize(arr);
    if (xsArrayGetSize(other) != size) {
        return (cBoolArrayGenericError);
    }
    if (size > _cBoolArraySortRun) {
        int r = _xsBoolArrayEnsureSortBuffers(size);
        if (r != cBoolArraySuccess) {
            _xsBoolArrayReleaseSortBuffers(releaseBuffers);
            return (r);
        }
    }
    int runStart = 0;
    while (runStart < size) {
        int runEnd = runStart + _cBoolArraySortRun;
        if (runEnd > size) {
            runEnd = size;
        }
        _xsBoolArrayInsertionSortWith(arr, other, runStart, runEnd, reverse);
        runStart = runEnd;
    }
    if (size <= _cBoolArraySortRun) {
        return (cBoolArraySuccess);
    }
    int src = arr;
    int srcOther = other;
    int dst = _boolArraySortKeys;
    int dstOther = _boolArraySortValues;
    bool inBuffers = false;
    int width = _cBoolArraySortRun;
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
            _xsBoolArrayMergeWith(src, srcOther, dst, dstOther, lo, mid, hi, reverse);
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
            xsArraySetBool(arr, i, xsArrayGetBool(src, i));
            xsArraySetInt(other, i, xsArrayGetInt(srcOther, i));
        }
    }
    _xsBoolArrayReleaseSortBuffers(releaseBuffers);
    return (cBoolArraySuccess);
}

/*
    Returns a string representation of the array, by default in the format `[true, false, ...]`.
    @param arr - array id
    @param start - string prepended to the output
    @param sep - separator between elements
    @param end - string appended to the output
    @param str_true - string used for true values
    @param str_false - string used for false values
    @return string representation of the array
*/
string xsBoolArrayToString(int arr = -1, string start = "[", string sep = ", ", string end = "]", string strTrue = "true", string strFalse = "false") {
    int size = xsArrayGetSize(arr);
    string s = start;
    for (i = 0; < size) {
        if (xsArrayGetBool(arr, i)) {
            s = s + strTrue;
        } else {
            s = s + strFalse;
        }
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
    @return new array id, or `cBoolArrayGenericError` on error
*/
int xsBoolArrayCopy(int arr = -1, int start = 0, int end = cBoolArrayMaxCapacity) {
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
    int newArr = xsArrayCreateBool(newSize);
    if (newArr < 0) {
        return (cBoolArrayGenericError);
    }
    for (i = fr; < to) {
        xsArraySetBool(newArr, i - fr, xsArrayGetBool(arr, i));
    }
    return (newArr);
}

/*
    Resizes the array to 0 to free its memory. XS can't fully delete arrays,
    so the array id stays allocated and must not be used afterwards.
    @param arr - array id
    @return `cBoolArraySuccess` on success, or `cBoolArrayResizeFailedError` if the resize fails
*/
int xsBoolArrayDelete(int arr = -1) {
    int r = xsArrayResizeBool(arr, 0);
    if (r != 1) {
        return (cBoolArrayResizeFailedError);
    }
    return (cBoolArraySuccess);
}

/*
    Performs lexicographic comparison of two arrays.
    @param arr1 - first array id
    @param arr2 - second array id
    @return -1 if arr1 < arr2, 1 if arr1 > arr2, 0 if equal
*/
int xsBoolArrayCompare(int arr1 = -1, int arr2 = -1) {
    int size1 = xsArrayGetSize(arr1);
    int size2 = xsArrayGetSize(arr2);
    int i = 0;
    while ((i < size1) && (i < size2)) {
        bool v1 = xsArrayGetBool(arr1, i);
        bool v2 = xsArrayGetBool(arr2, i);
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
    Reverses the array in-place.
    @param arr - array id
*/
void xsBoolArrayReverse(int arr = -1) {
    int size = xsArrayGetSize(arr);
    int mid = size / 2;
    for (i = 0; < mid) {
        bool temp = xsArrayGetBool(arr, i);
        int backI = (size - i) - 1;
        xsArraySetBool(arr, i, xsArrayGetBool(arr, backI));
        xsArraySetBool(arr, backI, temp);
    }
}

/*
    Counts the number of occurrences of a value in the array.
    @param arr - array id
    @param value - value to count
    @return number of occurrences
*/
int xsBoolArrayCount(int arr = -1, bool value = false) {
    int count = 0;
    int size = xsArrayGetSize(arr);
    for (i = 0; < size) {
        if (xsArrayGetBool(arr, i) == value) {
            count++;
        }
    }
    return (count);
}

/*
    Creates an array from a comma separated string, e.g. `"true,false"`.
    Items are trimmed, and items that cannot be parsed are skipped.
    @param items - comma separated values
    @return created array id, or `cBoolArrayGenericError` on error
*/
int xsBoolArrayFromString(string items = "") {
    if (strTrim(items) == "") {
        return (xsArrayCreateBool(0));
    }
    int parts = strSplit(items, ",");
    int numParts = xsArrayGetSize(parts);
    int arr = xsArrayCreateBool(numParts);
    if (arr < 0) {
        xsArrayResizeString(parts, 0);
        return (cBoolArrayGenericError);
    }
    int size = 0;
    for (i = 0; < numParts) {
        string item = strTrim(xsArrayGetString(parts, i));
        bool value = item == "true";
        if (value || (item == "false")) {
            xsArraySetBool(arr, size, value);
            size++;
        }
    }
    xsArrayResizeString(parts, 0);
    if (size < numParts) {
        int r = xsArrayResizeBool(arr, size);
        if (r != 1) {
            return (cBoolArrayResizeFailedError);
        }
    }
    return (arr);
}

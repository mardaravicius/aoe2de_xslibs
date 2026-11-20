extern const int cFloatArraySuccess = 0;
extern const int cFloatArrayGenericError = -1;
extern const float cFloatArrayGenericErrorFloat = -1.0;
extern const int cFloatArrayIndexOutOfRangeError = -2;
extern const int cFloatArrayResizeFailedError = -3;
extern const int cFloatArrayMaxCapacityError = -4;
extern const int cFloatArrayMaxCapacity = 999999999;
extern const float cFloatArrayEmptyParam = -9999999.0;
extern const int cFloatArrayEmptyIntParam = -999999999;
int _floatArrayLastOperationStatus = cFloatArraySuccess;

/*
    Creates an array with provided values. The first value that equals `cFloatArrayEmptyParam` will stop further insertion.
    This Function can create an array with 12 values at the maximum.
    @param v0 through v11 - value at a given index of an array
    @return created array id, or `cFloatArrayGenericError` on error
*/
int xsFloatArray(float v0 = cFloatArrayEmptyParam, float v1 = cFloatArrayEmptyParam, float v2 = cFloatArrayEmptyParam, float v3 = cFloatArrayEmptyParam, float v4 = cFloatArrayEmptyParam, float v5 = cFloatArrayEmptyParam, float v6 = cFloatArrayEmptyParam, float v7 = cFloatArrayEmptyParam, float v8 = cFloatArrayEmptyParam, float v9 = cFloatArrayEmptyParam, float v10 = cFloatArrayEmptyParam, float v11 = cFloatArrayEmptyParam) {
    int size = 12;
    if (v0 == cFloatArrayEmptyParam) {
        size = 0;
    } else if (v1 == cFloatArrayEmptyParam) {
        size = 1;
    } else if (v2 == cFloatArrayEmptyParam) {
        size = 2;
    } else if (v3 == cFloatArrayEmptyParam) {
        size = 3;
    } else if (v4 == cFloatArrayEmptyParam) {
        size = 4;
    } else if (v5 == cFloatArrayEmptyParam) {
        size = 5;
    } else if (v6 == cFloatArrayEmptyParam) {
        size = 6;
    } else if (v7 == cFloatArrayEmptyParam) {
        size = 7;
    } else if (v8 == cFloatArrayEmptyParam) {
        size = 8;
    } else if (v9 == cFloatArrayEmptyParam) {
        size = 9;
    } else if (v10 == cFloatArrayEmptyParam) {
        size = 10;
    } else if (v11 == cFloatArrayEmptyParam) {
        size = 11;
    }
    int arr = xsArrayCreateFloat(size);
    if (arr < 0) {
        return (cFloatArrayGenericError);
    }
    if (size == 0) {
        return (arr);
    }
    xsArraySetFloat(arr, 0, v0);
    if (size == 1) {
        return (arr);
    }
    xsArraySetFloat(arr, 1, v1);
    if (size == 2) {
        return (arr);
    }
    xsArraySetFloat(arr, 2, v2);
    if (size == 3) {
        return (arr);
    }
    xsArraySetFloat(arr, 3, v3);
    if (size == 4) {
        return (arr);
    }
    xsArraySetFloat(arr, 4, v4);
    if (size == 5) {
        return (arr);
    }
    xsArraySetFloat(arr, 5, v5);
    if (size == 6) {
        return (arr);
    }
    xsArraySetFloat(arr, 6, v6);
    if (size == 7) {
        return (arr);
    }
    xsArraySetFloat(arr, 7, v7);
    if (size == 8) {
        return (arr);
    }
    xsArraySetFloat(arr, 8, v8);
    if (size == 9) {
        return (arr);
    }
    xsArraySetFloat(arr, 9, v9);
    if (size == 10) {
        return (arr);
    }
    xsArraySetFloat(arr, 10, v10);
    if (size == 11) {
        return (arr);
    }
    xsArraySetFloat(arr, 11, v11);
    return (arr);
}

/*
    Creates an array by repeating a single value.
    @param value - value to repeat
    @param times - number of times to repeat the value
    @return created array id, or `cFloatArrayGenericError` on error
*/
int xsFloatArrayFromRepeatedVal(float value = 0.0, int times = 0) {
    if ((times < 0) || (times >= cFloatArrayMaxCapacity)) {
        return (cFloatArrayGenericError);
    }
    int arr = xsArrayCreateFloat(times, value);
    if (arr < 0) {
        return (cFloatArrayGenericError);
    }
    return (arr);
}

/*
    Creates a new array by repeating all elements of the given array.
    @param arr - source array id
    @param times - number of times to repeat the array contents
    @return created array id, `cFloatArrayMaxCapacityError` if the result is too large, or `cFloatArrayGenericError` on other errors
*/
int xsFloatArrayFromRepeatedArray(int arr = -1, int times = 0) {
    if (times < 0) {
        return (cFloatArrayGenericError);
    }
    int size = xsArrayGetSize(arr);
    if ((times > 0) && (size > (cFloatArrayMaxCapacity / times))) {
        return (cFloatArrayMaxCapacityError);
    }
    int newSize = size * times;
    if (newSize >= cFloatArrayMaxCapacity) {
        return (cFloatArrayMaxCapacityError);
    }
    int newArr = xsArrayCreateFloat(newSize);
    if (newArr < 0) {
        return (cFloatArrayGenericError);
    }
    for (i = 0; < size) {
        float val = xsArrayGetFloat(arr, i);
        int j = i;
        while (j < newSize) {
            xsArraySetFloat(newArr, j, val);
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
    @return index of the value, or `cFloatArrayGenericError` if not found
*/
int xsFloatArrayIndex(int arr = -1, float value = -1.0, int start = 0, int stop = cFloatArrayEmptyIntParam) {
    int size = xsArrayGetSize(arr);
    if ((stop == cFloatArrayEmptyIntParam) || (stop > size)) {
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
        if (xsArrayGetFloat(arr, i) == value) {
            return (i);
        }
    }
    return (cFloatArrayGenericError);
}

/*
    Checks whether the array contains the given value.
    @param arr - array id
    @param value - value to search for
    @return true if the value is found, false otherwise
*/
bool xsFloatArrayContains(int arr = -1, float value = -1.0) {
    return (xsFloatArrayIndex(arr, value) > -1);
}

bool _xsFloatArrayCompareElem(float a = -1.0, float b = -1.0, bool reverse = false) {
    if (reverse) {
        return (a > b);
    }
    return (a < b);
}

void _xsFloatArraySiftDown(int arr = -1, int start = -1, int end = -1, bool reverse = false) {
    int root = start;
    while (true) {
        int child = (2 * root) + 1;
        if (child > end) {
            return;
        }
        float childVal = xsArrayGetFloat(arr, child);
        if ((child + 1) <= end) {
            float childVal1 = xsArrayGetFloat(arr, child + 1);
            if (_xsFloatArrayCompareElem(childVal, childVal1, reverse)) {
                child++;
                childVal = childVal1;
            }
        }
        float rootVal = xsArrayGetFloat(arr, root);
        if (_xsFloatArrayCompareElem(rootVal, childVal, reverse)) {
            xsArraySetFloat(arr, root, childVal);
            xsArraySetFloat(arr, child, rootVal);
            root = child;
        } else {
            return;
        }
    }
}

/*
    Sorts the array in-place using heapsort.
    @param arr - array id
    @param reverse - if true, sorts in descending order
*/
void xsFloatArraySort(int arr = -1, bool reverse = false) {
    int size = xsArrayGetSize(arr);
    for (start = (size / 2) - 1; > -1) {
        _xsFloatArraySiftDown(arr, start, size - 1, reverse);
    }
    for (end = size - 1; > 0) {
        float temp = xsArrayGetFloat(arr, 0);
        xsArraySetFloat(arr, 0, xsArrayGetFloat(arr, end));
        xsArraySetFloat(arr, end, temp);
        _xsFloatArraySiftDown(arr, 0, end - 1, reverse);
    }
}

/*
    Returns a string representation of the array, by default in the format `[v0, v1, ...]`.
    @param arr - array id
    @param start - string prepended to the output
    @param sep - separator between elements
    @param end - string appended to the output
    @return string representation of the array
*/
string xsFloatArrayToString(int arr = -1, string start = "[", string sep = ", ", string end = "]") {
    int size = xsArrayGetSize(arr);
    string s = start;
    for (i = 0; < size) {
        s = s + ("" + xsArrayGetFloat(arr, i));
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
    @return new array id, or `cFloatArrayGenericError` on error
*/
int xsFloatArrayCopy(int arr = -1, int start = 0, int end = cFloatArrayMaxCapacity) {
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
    int newArr = xsArrayCreateFloat(newSize);
    if (newArr < 0) {
        return (cFloatArrayGenericError);
    }
    for (i = fr; < to) {
        xsArraySetFloat(newArr, i - fr, xsArrayGetFloat(arr, i));
    }
    return (newArr);
}

/*
    Resizes the array to 0 to free its memory. XS can't fully delete arrays,
    so the array id stays allocated and must not be used afterwards.
    @param arr - array id
    @return `cFloatArraySuccess` on success, or `cFloatArrayResizeFailedError` if the resize fails
*/
int xsFloatArrayDelete(int arr = -1) {
    int r = xsArrayResizeFloat(arr, 0);
    if (r != 1) {
        return (cFloatArrayResizeFailedError);
    }
    return (cFloatArraySuccess);
}

/*
    Performs lexicographic comparison of two arrays.
    @param arr1 - first array id
    @param arr2 - second array id
    @return -1 if arr1 < arr2, 1 if arr1 > arr2, 0 if equal
*/
int xsFloatArrayCompare(int arr1 = -1, int arr2 = -1) {
    int size1 = xsArrayGetSize(arr1);
    int size2 = xsArrayGetSize(arr2);
    int i = 0;
    while ((i < size1) && (i < size2)) {
        float v1 = xsArrayGetFloat(arr1, i);
        float v2 = xsArrayGetFloat(arr2, i);
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
void xsFloatArrayReverse(int arr = -1) {
    int size = xsArrayGetSize(arr);
    int mid = size / 2;
    for (i = 0; < mid) {
        float temp = xsArrayGetFloat(arr, i);
        int backI = (size - i) - 1;
        xsArraySetFloat(arr, i, xsArrayGetFloat(arr, backI));
        xsArraySetFloat(arr, backI, temp);
    }
}

/*
    Counts the number of occurrences of a value in the array.
    @param arr - array id
    @param value - value to count
    @return number of occurrences
*/
int xsFloatArrayCount(int arr = -1, float value = -1.0) {
    int count = 0;
    int size = xsArrayGetSize(arr);
    for (i = 0; < size) {
        if (xsArrayGetFloat(arr, i) == value) {
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
float xsFloatArraySum(int arr = -1) {
    float s = 0.0;
    int size = xsArrayGetSize(arr);
    for (i = 0; < size) {
        s = s + xsArrayGetFloat(arr, i);
    }
    return (s);
}

/*
    Returns the minimum value in the array. Sets last error on failure.
    @param arr - array id
    @return minimum value, or `cFloatArrayGenericErrorFloat` on error
*/
float xsFloatArrayMin(int arr = -1) {
    int size = xsArrayGetSize(arr);
    if (size <= 0) {
        _floatArrayLastOperationStatus = cFloatArrayIndexOutOfRangeError;
        return (cFloatArrayGenericErrorFloat);
    }
    float m = xsArrayGetFloat(arr, 0);
    for (i = 1; < size) {
        float v = xsArrayGetFloat(arr, i);
        if (v < m) {
            m = v;
        }
    }
    _floatArrayLastOperationStatus = cFloatArraySuccess;
    return (m);
}

/*
    Returns the maximum value in the array. Sets last error on failure.
    @param arr - array id
    @return maximum value, or `cFloatArrayGenericErrorFloat` on error
*/
float xsFloatArrayMax(int arr = -1) {
    int size = xsArrayGetSize(arr);
    if (size <= 0) {
        _floatArrayLastOperationStatus = cFloatArrayIndexOutOfRangeError;
        return (cFloatArrayGenericErrorFloat);
    }
    float m = xsArrayGetFloat(arr, 0);
    for (i = 1; < size) {
        float v = xsArrayGetFloat(arr, i);
        if (v > m) {
            m = v;
        }
    }
    _floatArrayLastOperationStatus = cFloatArraySuccess;
    return (m);
}

/*
    Returns the status code of the last operation that sets it (min, max).
    @return `cFloatArraySuccess` if the last such operation succeeded, or a negative error code
*/
int xsFloatArrayLastError() {
    return (_floatArrayLastOperationStatus);
}

/*
    Creates an array from a comma separated string, e.g. `"1.0,1.5,-2.25"`.
    Items are trimmed, and items that cannot be parsed are skipped.
    @param items - comma separated values
    @return created array id, or `cFloatArrayGenericError` on error
*/
int xsFloatArrayFromString(string items = "") {
    if (strTrim(items) == "") {
        return (xsArrayCreateFloat(0));
    }
    int parts = strSplit(items, ",");
    int numParts = xsArrayGetSize(parts);
    int arr = xsArrayCreateFloat(numParts);
    if (arr < 0) {
        xsArrayResizeString(parts, 0);
        return (cFloatArrayGenericError);
    }
    int size = 0;
    for (i = 0; < numParts) {
        string item = strTrim(xsArrayGetString(parts, i));
        float value = strToFloat(item, cFloatArrayEmptyParam);
        if (value != cFloatArrayEmptyParam) {
            xsArraySetFloat(arr, size, value);
            size++;
        }
    }
    xsArrayResizeString(parts, 0);
    if (size < numParts) {
        int r = xsArrayResizeFloat(arr, size);
        if (r != 1) {
            return (cFloatArrayResizeFailedError);
        }
    }
    return (arr);
}

extern const int cBoolArraySuccess = 0;
extern const int cBoolArrayGenericError = -1;
extern const int cBoolArrayResizeFailedError = -3;
extern const int cBoolArrayMaxCapacityError = -4;
extern const int cBoolArrayMaxCapacity = 999999999;
extern const int cBoolArrayEmptyIntParam = -999999999;

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

void _xsBoolArraySiftDown(int arr = -1, int start = -1, int end = -1, bool reverse = false) {
    int root = start;
    while (true) {
        int child = (2 * root) + 1;
        if (child > end) {
            return;
        }
        bool childVal = xsArrayGetBool(arr, child);
        if ((child + 1) <= end) {
            bool childVal1 = xsArrayGetBool(arr, child + 1);
            if (_xsBoolArrayCompareElem(childVal, childVal1, reverse)) {
                child++;
                childVal = childVal1;
            }
        }
        bool rootVal = xsArrayGetBool(arr, root);
        if (_xsBoolArrayCompareElem(rootVal, childVal, reverse)) {
            xsArraySetBool(arr, root, childVal);
            xsArraySetBool(arr, child, rootVal);
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
void xsBoolArraySort(int arr = -1, bool reverse = false) {
    int size = xsArrayGetSize(arr);
    for (start = (size / 2) - 1; > -1) {
        _xsBoolArraySiftDown(arr, start, size - 1, reverse);
    }
    for (end = size - 1; > 0) {
        bool temp = xsArrayGetBool(arr, 0);
        xsArraySetBool(arr, 0, xsArrayGetBool(arr, end));
        xsArraySetBool(arr, end, temp);
        _xsBoolArraySiftDown(arr, 0, end - 1, reverse);
    }
}

/*
    Returns a string representation of the array in the format `[true, false, ...]`.
    @param arr - array id
    @return string representation of the array
*/
string xsBoolArrayToString(int arr = -1) {
    int size = xsArrayGetSize(arr);
    string s = "[";
    for (i = 0; < size) {
        if (xsArrayGetBool(arr, i)) {
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

extern const int cStringArraySuccess = 0;
extern const int cStringArrayGenericError = -1;
extern const int cStringArrayIndexOutOfRangeError = -2;
extern const int cStringArrayResizeFailedError = -3;
extern const int cStringArrayMaxCapacityError = -4;
extern const int cStringArrayMaxCapacity = 999999999;
extern const int cStringArrayEmptyIntParam = -999999999;
int _stringArrayLastOperationStatus = cStringArraySuccess;

/*
    Creates an array with provided values. The first value that equals the default sentinel will stop further insertion.
    This Function can create an array with 12 values at the maximum.
    @param v0 through v11 - value at a given index of an array
    @return created array id, or `cStringArrayGenericError` on error
*/
int xsStringArray(string v0 = "!<[empty", string v1 = "!<[empty", string v2 = "!<[empty", string v3 = "!<[empty", string v4 = "!<[empty", string v5 = "!<[empty", string v6 = "!<[empty", string v7 = "!<[empty", string v8 = "!<[empty", string v9 = "!<[empty", string v10 = "!<[empty", string v11 = "!<[empty") {
    int size = 12;
    if (v0 == "!<[empty") {
        size = 0;
    } else if (v1 == "!<[empty") {
        size = 1;
    } else if (v2 == "!<[empty") {
        size = 2;
    } else if (v3 == "!<[empty") {
        size = 3;
    } else if (v4 == "!<[empty") {
        size = 4;
    } else if (v5 == "!<[empty") {
        size = 5;
    } else if (v6 == "!<[empty") {
        size = 6;
    } else if (v7 == "!<[empty") {
        size = 7;
    } else if (v8 == "!<[empty") {
        size = 8;
    } else if (v9 == "!<[empty") {
        size = 9;
    } else if (v10 == "!<[empty") {
        size = 10;
    } else if (v11 == "!<[empty") {
        size = 11;
    }
    int arr = xsArrayCreateString(size);
    if (arr < 0) {
        return (cStringArrayGenericError);
    }
    if (size == 0) {
        return (arr);
    }
    xsArraySetString(arr, 0, v0);
    if (size == 1) {
        return (arr);
    }
    xsArraySetString(arr, 1, v1);
    if (size == 2) {
        return (arr);
    }
    xsArraySetString(arr, 2, v2);
    if (size == 3) {
        return (arr);
    }
    xsArraySetString(arr, 3, v3);
    if (size == 4) {
        return (arr);
    }
    xsArraySetString(arr, 4, v4);
    if (size == 5) {
        return (arr);
    }
    xsArraySetString(arr, 5, v5);
    if (size == 6) {
        return (arr);
    }
    xsArraySetString(arr, 6, v6);
    if (size == 7) {
        return (arr);
    }
    xsArraySetString(arr, 7, v7);
    if (size == 8) {
        return (arr);
    }
    xsArraySetString(arr, 8, v8);
    if (size == 9) {
        return (arr);
    }
    xsArraySetString(arr, 9, v9);
    if (size == 10) {
        return (arr);
    }
    xsArraySetString(arr, 10, v10);
    if (size == 11) {
        return (arr);
    }
    xsArraySetString(arr, 11, v11);
    return (arr);
}

/*
    Creates an array by repeating a single value.
    @param value - value to repeat
    @param times - number of times to repeat the value
    @return created array id, or `cStringArrayGenericError` on error
*/
int xsStringArrayFromRepeatedVal(string value = "", int times = 0) {
    if ((times < 0) || (times >= cStringArrayMaxCapacity)) {
        return (cStringArrayGenericError);
    }
    int arr = xsArrayCreateString(times, value);
    if (arr < 0) {
        return (cStringArrayGenericError);
    }
    return (arr);
}

/*
    Creates a new array by repeating all elements of the given array.
    @param arr - source array id
    @param times - number of times to repeat the array contents
    @return created array id, `cStringArrayMaxCapacityError` if the result is too large, or `cStringArrayGenericError` on other errors
*/
int xsStringArrayFromRepeatedArray(int arr = -1, int times = 0) {
    if (times < 0) {
        return (cStringArrayGenericError);
    }
    int size = xsArrayGetSize(arr);
    if ((times > 0) && (size > (cStringArrayMaxCapacity / times))) {
        return (cStringArrayMaxCapacityError);
    }
    int newSize = size * times;
    if (newSize >= cStringArrayMaxCapacity) {
        return (cStringArrayMaxCapacityError);
    }
    int newArr = xsArrayCreateString(newSize);
    if (newArr < 0) {
        return (cStringArrayGenericError);
    }
    for (i = 0; < size) {
        string val = xsArrayGetString(arr, i);
        int j = i;
        while (j < newSize) {
            xsArraySetString(newArr, j, val);
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
    @return index of the value, or `cStringArrayGenericError` if not found
*/
int xsStringArrayIndex(int arr = -1, string value = "", int start = 0, int stop = cStringArrayEmptyIntParam) {
    int size = xsArrayGetSize(arr);
    if ((stop == cStringArrayEmptyIntParam) || (stop > size)) {
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
        if (xsArrayGetString(arr, i) == value) {
            return (i);
        }
    }
    return (cStringArrayGenericError);
}

/*
    Checks whether the array contains the given value.
    @param arr - array id
    @param value - value to search for
    @return true if the value is found, false otherwise
*/
bool xsStringArrayContains(int arr = -1, string value = "") {
    return (xsStringArrayIndex(arr, value) > -1);
}

bool _xsStringArrayCompareElem(string a = "", string b = "", bool reverse = false) {
    if (reverse) {
        return (a > b);
    }
    return (a < b);
}

void _xsStringArraySiftDown(int arr = -1, int start = -1, int end = -1, bool reverse = false) {
    int root = start;
    while (true) {
        int child = (2 * root) + 1;
        if (child > end) {
            return;
        }
        string childVal = xsArrayGetString(arr, child);
        if ((child + 1) <= end) {
            string childVal1 = xsArrayGetString(arr, child + 1);
            if (_xsStringArrayCompareElem(childVal, childVal1, reverse)) {
                child++;
                childVal = childVal1;
            }
        }
        string rootVal = xsArrayGetString(arr, root);
        if (_xsStringArrayCompareElem(rootVal, childVal, reverse)) {
            xsArraySetString(arr, root, childVal);
            xsArraySetString(arr, child, rootVal);
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
void xsStringArraySort(int arr = -1, bool reverse = false) {
    int size = xsArrayGetSize(arr);
    for (start = (size / 2) - 1; > -1) {
        _xsStringArraySiftDown(arr, start, size - 1, reverse);
    }
    for (end = size - 1; > 0) {
        string temp = xsArrayGetString(arr, 0);
        xsArraySetString(arr, 0, xsArrayGetString(arr, end));
        xsArraySetString(arr, end, temp);
        _xsStringArraySiftDown(arr, 0, end - 1, reverse);
    }
}

/*
    Returns a string representation of the array, by default in the format `["v0", "v1", ...]`.
    @param arr - array id
    @param start - string prepended to the output
    @param sep - separator between elements
    @param end - string appended to the output
    @param quote - string wrapped around string elements
    @return string representation of the array
*/
string xsStringArrayToString(int arr = -1, string start = "[", string sep = ", ", string end = "]", string quote = "\"") {
    int size = xsArrayGetSize(arr);
    string s = start;
    for (i = 0; < size) {
        s = s + ((quote + xsArrayGetString(arr, i)) + quote);
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
    @return new array id, or `cStringArrayGenericError` on error
*/
int xsStringArrayCopy(int arr = -1, int start = 0, int end = cStringArrayMaxCapacity) {
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
    int newArr = xsArrayCreateString(newSize);
    if (newArr < 0) {
        return (cStringArrayGenericError);
    }
    for (i = fr; < to) {
        xsArraySetString(newArr, i - fr, xsArrayGetString(arr, i));
    }
    return (newArr);
}

/*
    Resizes the array to 0 to free its memory. XS can't fully delete arrays,
    so the array id stays allocated and must not be used afterwards.
    @param arr - array id
    @return `cStringArraySuccess` on success, or `cStringArrayResizeFailedError` if the resize fails
*/
int xsStringArrayDelete(int arr = -1) {
    int r = xsArrayResizeString(arr, 0);
    if (r != 1) {
        return (cStringArrayResizeFailedError);
    }
    return (cStringArraySuccess);
}

/*
    Performs lexicographic comparison of two arrays.
    @param arr1 - first array id
    @param arr2 - second array id
    @return -1 if arr1 < arr2, 1 if arr1 > arr2, 0 if equal
*/
int xsStringArrayCompare(int arr1 = -1, int arr2 = -1) {
    int size1 = xsArrayGetSize(arr1);
    int size2 = xsArrayGetSize(arr2);
    int i = 0;
    while ((i < size1) && (i < size2)) {
        string v1 = xsArrayGetString(arr1, i);
        string v2 = xsArrayGetString(arr2, i);
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
void xsStringArrayReverse(int arr = -1) {
    int size = xsArrayGetSize(arr);
    int mid = size / 2;
    for (i = 0; < mid) {
        string temp = xsArrayGetString(arr, i);
        int backI = (size - i) - 1;
        xsArraySetString(arr, i, xsArrayGetString(arr, backI));
        xsArraySetString(arr, backI, temp);
    }
}

/*
    Counts the number of occurrences of a value in the array.
    @param arr - array id
    @param value - value to count
    @return number of occurrences
*/
int xsStringArrayCount(int arr = -1, string value = "") {
    int count = 0;
    int size = xsArrayGetSize(arr);
    for (i = 0; < size) {
        if (xsArrayGetString(arr, i) == value) {
            count++;
        }
    }
    return (count);
}

/*
    Returns the minimum value in the array (lexicographic). Sets last error on failure.
    @param arr - array id
    @return minimum value, or "-1" on error
*/
string xsStringArrayMin(int arr = -1) {
    int size = xsArrayGetSize(arr);
    if (size <= 0) {
        _stringArrayLastOperationStatus = cStringArrayIndexOutOfRangeError;
        return ("-1");
    }
    string m = xsArrayGetString(arr, 0);
    for (i = 1; < size) {
        string v = xsArrayGetString(arr, i);
        if (v < m) {
            m = v;
        }
    }
    _stringArrayLastOperationStatus = cStringArraySuccess;
    return (m);
}

/*
    Returns the maximum value in the array (lexicographic). Sets last error on failure.
    @param arr - array id
    @return maximum value, or "-1" on error
*/
string xsStringArrayMax(int arr = -1) {
    int size = xsArrayGetSize(arr);
    if (size <= 0) {
        _stringArrayLastOperationStatus = cStringArrayIndexOutOfRangeError;
        return ("-1");
    }
    string m = xsArrayGetString(arr, 0);
    for (i = 1; < size) {
        string v = xsArrayGetString(arr, i);
        if (v > m) {
            m = v;
        }
    }
    _stringArrayLastOperationStatus = cStringArraySuccess;
    return (m);
}

/*
    Returns the status code of the last operation that sets it (min, max).
    @return `cStringArraySuccess` if the last such operation succeeded, or a negative error code
*/
int xsStringArrayLastError() {
    return (_stringArrayLastOperationStatus);
}

int _xsStringArrayFindSeparator(string text = "", string separator = ",", int start = 0) {
    int n = strLen(text);
    bool inQuotes = false;
    for (i = start; < n) {
        string ch = strCharAt(text, i);
        if (ch == "'") {
            inQuotes = inQuotes == false;
        } else if ((ch == separator) && (inQuotes == false)) {
            return (i);
        }
    }
    return (-1);
}

int _xsStringArraySplitItems(string items = "") {
    int numParts = 1;
    int sep = _xsStringArrayFindSeparator(items, ",", 0);
    while (sep >= 0) {
        numParts++;
        sep = _xsStringArrayFindSeparator(items, ",", sep + 1);
    }
    int parts = xsArrayCreateString(numParts);
    int start = 0;
    for (i = 0; < numParts) {
        int end = _xsStringArrayFindSeparator(items, ",", start);
        if (end < 0) {
            xsArraySetString(parts, i, strRemove(items, 0, start));
        } else {
            xsArraySetString(parts, i, strSubstring(items, start, end));
        }
        start = end + 1;
    }
    return (parts);
}

bool _xsStringArrayIsQuoted(string text = "") {
    int n = strLen(text);
    if (n < 2) {
        return (false);
    }
    if ((strCharAt(text, 0) != "'") || (strCharAt(text, n - 1) != "'")) {
        return (false);
    }
    return (strIndexOf(strSubstring(text, 1, n - 1), "'") == -1);
}

/*
    Creates an array from a comma separated string, e.g. `"'a','b c'"`. Strings must be wrapped in `'` and cannot contain `'`.
    Items are trimmed, and items that cannot be parsed are skipped.
    @param items - comma separated values
    @return created array id, or `cStringArrayGenericError` on error
*/
int xsStringArrayFromString(string items = "") {
    if (strTrim(items) == "") {
        return (xsArrayCreateString(0));
    }
    int parts = _xsStringArraySplitItems(items);
    int numParts = xsArrayGetSize(parts);
    int arr = xsArrayCreateString(numParts);
    if (arr < 0) {
        xsArrayResizeString(parts, 0);
        return (cStringArrayGenericError);
    }
    int size = 0;
    for (i = 0; < numParts) {
        string item = strTrim(xsArrayGetString(parts, i));
        if (_xsStringArrayIsQuoted(item)) {
            xsArraySetString(arr, size, strSubstring(item, 1, strLen(item) - 1));
            size++;
        }
    }
    xsArrayResizeString(parts, 0);
    if (size < numParts) {
        int r = xsArrayResizeString(arr, size);
        if (r != 1) {
            return (cStringArrayResizeFailedError);
        }
    }
    return (arr);
}

extern const int cVectorArrayGenericError = -1;
extern const int cVectorArrayMaxCapacityError = -4;
extern const int cVectorArrayMaxCapacity = 999999999;
extern const vector cVectorArrayEmptyParam = vector(-9999999.0, -9999999.0, -9999999.0);
extern const int cVectorArrayEmptyIntParam = -999999999;
const float _cVectorArrayEmptyFloat = -9999999.0;

/*
    Creates an array with provided values. The first value that equals `cVectorArrayEmptyParam` will stop further insertion.
    This Function can create an array with 12 values at the maximum.
    @param v0 through v11 - value at a given index of an array
    @return created array id, or `cVectorArrayGenericError` on error
*/
int xsVectorArray(vector v0 = cVectorArrayEmptyParam, vector v1 = cVectorArrayEmptyParam, vector v2 = cVectorArrayEmptyParam, vector v3 = cVectorArrayEmptyParam, vector v4 = cVectorArrayEmptyParam, vector v5 = cVectorArrayEmptyParam, vector v6 = cVectorArrayEmptyParam, vector v7 = cVectorArrayEmptyParam, vector v8 = cVectorArrayEmptyParam, vector v9 = cVectorArrayEmptyParam, vector v10 = cVectorArrayEmptyParam, vector v11 = cVectorArrayEmptyParam) {
    int size = 12;
    if (v0 == cVectorArrayEmptyParam) {
        size = 0;
    } else if (v1 == cVectorArrayEmptyParam) {
        size = 1;
    } else if (v2 == cVectorArrayEmptyParam) {
        size = 2;
    } else if (v3 == cVectorArrayEmptyParam) {
        size = 3;
    } else if (v4 == cVectorArrayEmptyParam) {
        size = 4;
    } else if (v5 == cVectorArrayEmptyParam) {
        size = 5;
    } else if (v6 == cVectorArrayEmptyParam) {
        size = 6;
    } else if (v7 == cVectorArrayEmptyParam) {
        size = 7;
    } else if (v8 == cVectorArrayEmptyParam) {
        size = 8;
    } else if (v9 == cVectorArrayEmptyParam) {
        size = 9;
    } else if (v10 == cVectorArrayEmptyParam) {
        size = 10;
    } else if (v11 == cVectorArrayEmptyParam) {
        size = 11;
    }
    int arr = xsArrayCreateVector(size);
    if (arr < 0) {
        return (cVectorArrayGenericError);
    }
    if (size == 0) {
        return (arr);
    }
    xsArraySetVector(arr, 0, v0);
    if (size == 1) {
        return (arr);
    }
    xsArraySetVector(arr, 1, v1);
    if (size == 2) {
        return (arr);
    }
    xsArraySetVector(arr, 2, v2);
    if (size == 3) {
        return (arr);
    }
    xsArraySetVector(arr, 3, v3);
    if (size == 4) {
        return (arr);
    }
    xsArraySetVector(arr, 4, v4);
    if (size == 5) {
        return (arr);
    }
    xsArraySetVector(arr, 5, v5);
    if (size == 6) {
        return (arr);
    }
    xsArraySetVector(arr, 6, v6);
    if (size == 7) {
        return (arr);
    }
    xsArraySetVector(arr, 7, v7);
    if (size == 8) {
        return (arr);
    }
    xsArraySetVector(arr, 8, v8);
    if (size == 9) {
        return (arr);
    }
    xsArraySetVector(arr, 9, v9);
    if (size == 10) {
        return (arr);
    }
    xsArraySetVector(arr, 10, v10);
    if (size == 11) {
        return (arr);
    }
    xsArraySetVector(arr, 11, v11);
    return (arr);
}

/*
    Creates an array by repeating a single value.
    @param value - value to repeat
    @param times - number of times to repeat the value
    @return created array id, or `cVectorArrayGenericError` on error
*/
int xsVectorArrayFromRepeatedVal(vector value = vector(0.0, 0.0, 0.0), int times = 0) {
    if ((times < 0) || (times >= cVectorArrayMaxCapacity)) {
        return (cVectorArrayGenericError);
    }
    int arr = xsArrayCreateVector(times, value);
    if (arr < 0) {
        return (cVectorArrayGenericError);
    }
    return (arr);
}

/*
    Creates a new array by repeating all elements of the given array.
    @param arr - source array id
    @param times - number of times to repeat the array contents
    @return created array id, `cVectorArrayMaxCapacityError` if the result is too large, or `cVectorArrayGenericError` on other errors
*/
int xsVectorArrayFromRepeatedArray(int arr = -1, int times = 0) {
    if (times < 0) {
        return (cVectorArrayGenericError);
    }
    int size = xsArrayGetSize(arr);
    if ((times > 0) && (size > (cVectorArrayMaxCapacity / times))) {
        return (cVectorArrayMaxCapacityError);
    }
    int newSize = size * times;
    if (newSize >= cVectorArrayMaxCapacity) {
        return (cVectorArrayMaxCapacityError);
    }
    int newArr = xsArrayCreateVector(newSize);
    if (newArr < 0) {
        return (cVectorArrayGenericError);
    }
    for (i = 0; < size) {
        vector val = xsArrayGetVector(arr, i);
        int j = i;
        while (j < newSize) {
            xsArraySetVector(newArr, j, val);
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
    @return index of the value, or `cVectorArrayGenericError` if not found
*/
int xsVectorArrayIndex(int arr = -1, vector value = vector(-1.0, -1.0, -1.0), int start = 0, int stop = cVectorArrayEmptyIntParam) {
    int size = xsArrayGetSize(arr);
    if ((stop == cVectorArrayEmptyIntParam) || (stop > size)) {
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
        if (xsArrayGetVector(arr, i) == value) {
            return (i);
        }
    }
    return (cVectorArrayGenericError);
}

/*
    Checks whether the array contains the given value.
    @param arr - array id
    @param value - value to search for
    @return true if the value is found, false otherwise
*/
bool xsVectorArrayContains(int arr = -1, vector value = vector(-1.0, -1.0, -1.0)) {
    return (xsVectorArrayIndex(arr, value) > -1);
}

/*
    Returns a string representation of the array, by default in the format `[v0, v1, ...]`.
    @param arr - array id
    @param start - string prepended to the output
    @param sep - separator between elements
    @param end - string appended to the output
    @return string representation of the array
*/
string xsVectorArrayToString(int arr = -1, string start = "[", string sep = ", ", string end = "]") {
    int size = xsArrayGetSize(arr);
    string s = start;
    for (i = 0; < size) {
        s = s + ("" + xsArrayGetVector(arr, i));
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
    @return new array id, or `cVectorArrayGenericError` on error
*/
int xsVectorArrayCopy(int arr = -1, int start = 0, int end = cVectorArrayMaxCapacity) {
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
    int newArr = xsArrayCreateVector(newSize);
    if (newArr < 0) {
        return (cVectorArrayGenericError);
    }
    for (i = fr; < to) {
        xsArraySetVector(newArr, i - fr, xsArrayGetVector(arr, i));
    }
    return (newArr);
}

/*
    Reverses the array in-place.
    @param arr - array id
*/
void xsVectorArrayReverse(int arr = -1) {
    int size = xsArrayGetSize(arr);
    int mid = size / 2;
    for (i = 0; < mid) {
        vector temp = xsArrayGetVector(arr, i);
        int backI = (size - i) - 1;
        xsArraySetVector(arr, i, xsArrayGetVector(arr, backI));
        xsArraySetVector(arr, backI, temp);
    }
}

/*
    Counts the number of occurrences of a value in the array.
    @param arr - array id
    @param value - value to count
    @return number of occurrences
*/
int xsVectorArrayCount(int arr = -1, vector value = vector(-1.0, -1.0, -1.0)) {
    int count = 0;
    int size = xsArrayGetSize(arr);
    for (i = 0; < size) {
        if (xsArrayGetVector(arr, i) == value) {
            count++;
        }
    }
    return (count);
}

int _xsVectorArrayFindSeparator(string text = "", string separator = ",", int start = 0) {
    int n = strLen(text);
    bool inQuotes = false;
    bool inParens = false;
    for (i = start; < n) {
        string ch = strCharAt(text, i);
        if (ch == "'") {
            inQuotes = inQuotes == false;
        } else if (inQuotes == false) {
            if (ch == "(") {
                inParens = true;
            } else if (ch == ")") {
                inParens = false;
            } else if ((ch == separator) && (inParens == false)) {
                return (i);
            }
        }
    }
    return (-1);
}

int _xsVectorArraySplitItems(string items = "") {
    int numParts = 1;
    int sep = _xsVectorArrayFindSeparator(items, ",", 0);
    while (sep >= 0) {
        numParts++;
        sep = _xsVectorArrayFindSeparator(items, ",", sep + 1);
    }
    int parts = xsArrayCreateString(numParts);
    int start = 0;
    for (i = 0; < numParts) {
        int end = _xsVectorArrayFindSeparator(items, ",", start);
        if (end < 0) {
            xsArraySetString(parts, i, strRemove(items, 0, start));
        } else {
            xsArraySetString(parts, i, strSubstring(items, start, end));
        }
        start = end + 1;
    }
    return (parts);
}

vector _xsVectorArrayParseVector(string text = "") {
    int n = strLen(text);
    if (n < 3) {
        return (cVectorArrayEmptyParam);
    }
    if ((strSubstring(text, 0, 2) != "v(") || (strCharAt(text, n - 1) != ")")) {
        return (cVectorArrayEmptyParam);
    }
    int coords = strSplit(strSubstring(text, 2, n - 1), ",");
    if (xsArrayGetSize(coords) != 3) {
        xsArrayResizeString(coords, 0);
        return (cVectorArrayEmptyParam);
    }
    float x = strToFloat(strTrim(xsArrayGetString(coords, 0)), _cVectorArrayEmptyFloat);
    float y = strToFloat(strTrim(xsArrayGetString(coords, 1)), _cVectorArrayEmptyFloat);
    float z = strToFloat(strTrim(xsArrayGetString(coords, 2)), _cVectorArrayEmptyFloat);
    xsArrayResizeString(coords, 0);
    if ((x == _cVectorArrayEmptyFloat) || (y == _cVectorArrayEmptyFloat) || (z == _cVectorArrayEmptyFloat)) {
        return (cVectorArrayEmptyParam);
    }
    return (xsVectorSet(x, y, z));
}

/*
    Creates an array from a comma separated string, e.g. `"v(1.0,2.0,3.0),v(1.5,0.0,-2.0)"`.
    Items are trimmed, and items that cannot be parsed are skipped. Items are parsed twice because
    vector arrays can't be resized, so the array is created at its final size.
    @param items - comma separated values
    @return created array id, or `cVectorArrayGenericError` on error
*/
int xsVectorArrayFromString(string items = "") {
    if (strTrim(items) == "") {
        return (xsArrayCreateVector(0));
    }
    int parts = _xsVectorArraySplitItems(items);
    int numParts = xsArrayGetSize(parts);
    int size = 0;
    for (i = 0; < numParts) {
        if (_xsVectorArrayParseVector(strTrim(xsArrayGetString(parts, i))) != cVectorArrayEmptyParam) {
            size++;
        }
    }
    int arr = xsArrayCreateVector(size);
    if (arr < 0) {
        xsArrayResizeString(parts, 0);
        return (cVectorArrayGenericError);
    }
    int j = 0;
    for (i = 0; < numParts) {
        vector value = _xsVectorArrayParseVector(strTrim(xsArrayGetString(parts, i)));
        if (value != cVectorArrayEmptyParam) {
            xsArraySetVector(arr, j, value);
            j++;
        }
    }
    xsArrayResizeString(parts, 0);
    return (arr);
}

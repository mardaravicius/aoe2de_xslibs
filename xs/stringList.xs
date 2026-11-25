extern const int cStringListSuccess = 0;
extern const int cStringListGenericError = -1;
extern const int cStringListIndexOutOfRangeError = -2;
extern const int cStringListResizeFailedError = -3;
extern const int cStringListMaxCapacityError = -4;
extern const int cStringListMaxCapacity = 999999999;
extern const int cStringListEmptyIntParam = -999999999;
int _stringListLastOperationStatus = cStringListSuccess;
int _stringListSortKeys = -1;
int _stringListSortValues = -1;

/*
    Returns the number of elements in the list.
    @param lst - list id
    @return list size
*/
int xsStringListSize(int lst = -1) {
    return (xsArrayGetInt(lst, 0));
}

/*
    Creates empty list for string values. List is a dynamic array that grows and shrinks as values are added and removed.
    @param capacity - initial list capacity
    @return created list id, or `cStringListGenericError` on error
*/
int xsStringListCreate(int capacity = 7) {
    if ((capacity < 0) || (capacity >= cStringListMaxCapacity)) {
        return (cStringListGenericError);
    }
    int lst = xsArrayCreateInt(2, 0);
    if (lst < 0) {
        return (cStringListGenericError);
    }
    int strLst = xsArrayCreateString(capacity);
    if (strLst < 0) {
        xsArrayResizeInt(lst, 0);
        return (cStringListGenericError);
    }
    xsArraySetInt(lst, 1, strLst);
    return (lst);
}

/*
    Creates a list with provided values. The first value that equals the default sentinel will stop further insertion.
    This Function can create a list with 12 values at the maximum, but further values can be added with other functions.
    @param v0 through v11 - value at a given index of a list
    @return created list id, or `cStringListGenericError` on error
*/
int xsStringList(string v0 = "!<[empty", string v1 = "!<[empty", string v2 = "!<[empty", string v3 = "!<[empty", string v4 = "!<[empty", string v5 = "!<[empty", string v6 = "!<[empty", string v7 = "!<[empty", string v8 = "!<[empty", string v9 = "!<[empty", string v10 = "!<[empty", string v11 = "!<[empty") {
    int strLst = xsArrayCreateString(12);
    if (strLst < 0) {
        return (cStringListGenericError);
    }
    int lst = xsArrayCreateInt(2, strLst);
    if (lst < 0) {
        xsArrayResizeString(strLst, 0);
        return (cStringListGenericError);
    }
    if (v0 == "!<[empty") {
        xsArraySetInt(lst, 0, 0);
        return (lst);
    }
    xsArraySetString(strLst, 0, v0);
    if (v1 == "!<[empty") {
        xsArraySetInt(lst, 0, 1);
        return (lst);
    }
    xsArraySetString(strLst, 1, v1);
    if (v2 == "!<[empty") {
        xsArraySetInt(lst, 0, 2);
        return (lst);
    }
    xsArraySetString(strLst, 2, v2);
    if (v3 == "!<[empty") {
        xsArraySetInt(lst, 0, 3);
        return (lst);
    }
    xsArraySetString(strLst, 3, v3);
    if (v4 == "!<[empty") {
        xsArraySetInt(lst, 0, 4);
        return (lst);
    }
    xsArraySetString(strLst, 4, v4);
    if (v5 == "!<[empty") {
        xsArraySetInt(lst, 0, 5);
        return (lst);
    }
    xsArraySetString(strLst, 5, v5);
    if (v6 == "!<[empty") {
        xsArraySetInt(lst, 0, 6);
        return (lst);
    }
    xsArraySetString(strLst, 6, v6);
    if (v7 == "!<[empty") {
        xsArraySetInt(lst, 0, 7);
        return (lst);
    }
    xsArraySetString(strLst, 7, v7);
    if (v8 == "!<[empty") {
        xsArraySetInt(lst, 0, 8);
        return (lst);
    }
    xsArraySetString(strLst, 8, v8);
    if (v9 == "!<[empty") {
        xsArraySetInt(lst, 0, 9);
        return (lst);
    }
    xsArraySetString(strLst, 9, v9);
    if (v10 == "!<[empty") {
        xsArraySetInt(lst, 0, 10);
        return (lst);
    }
    xsArraySetString(strLst, 10, v10);
    if (v11 == "!<[empty") {
        xsArraySetInt(lst, 0, 11);
        return (lst);
    }
    xsArraySetString(strLst, 11, v11);
    xsArraySetInt(lst, 0, 12);
    return (lst);
}

/*
    Creates a list by repeating a single value.
    @param value - value to repeat
    @param times - number of times to repeat the value
    @return created list id, or `cStringListGenericError` on error
*/
int xsStringListFromRepeatedVal(string value = "", int times = 0) {
    if ((times < 0) || (times > cStringListMaxCapacity)) {
        return (cStringListGenericError);
    }
    int lst = xsArrayCreateInt(2, times);
    if (lst < 0) {
        return (cStringListGenericError);
    }
    int strLst = xsArrayCreateString(times, value);
    if (strLst < 0) {
        xsArrayResizeInt(lst, 0);
        return (cStringListGenericError);
    }
    xsArraySetInt(lst, 1, strLst);
    return (lst);
}

/*
    Creates a new list by repeating all elements of the given list.
    @param lst - source list id
    @param times - number of times to repeat the list contents
    @return created list id, or `cStringListGenericError` on error
*/
int xsStringListFromRepeatedList(int lst = -1, int times = 0) {
    if (times < 0) {
        return (cStringListGenericError);
    }
    int size = xsArrayGetInt(lst, 0);
    if ((times > 0) && (size > (cStringListMaxCapacity / times))) {
        return (cStringListMaxCapacityError);
    }
    int newCapacity = size * times;
    if (newCapacity > cStringListMaxCapacity) {
        return (cStringListMaxCapacityError);
    }
    int newStrLst = xsArrayCreateString(newCapacity);
    if (newStrLst < 0) {
        return (cStringListGenericError);
    }
    int newLst = xsArrayCreateInt(2, newCapacity);
    if (newLst < 0) {
        xsArrayResizeString(newStrLst, 0);
        return (cStringListGenericError);
    }
    int strLst = xsArrayGetInt(lst, 1);
    for (i = 0; < size) {
        string val = xsArrayGetString(strLst, i);
        int j = i;
        while (j < newCapacity) {
            xsArraySetString(newStrLst, j, val);
            j = j + size;
        }
    }
    xsArraySetInt(newLst, 1, newStrLst);
    return (newLst);
}

/*
    Creates a new list by copying elements from an XS array.
    @param arr - source XS array id
    @return created list id, or `cStringListGenericError` on error
*/
int xsStringListFromArray(int arr = -1) {
    int arrSize = xsArrayGetSize(arr);
    if (arrSize > cStringListMaxCapacity) {
        return (cStringListMaxCapacityError);
    }
    int newStrLst = xsArrayCreateString(arrSize);
    if (newStrLst < 0) {
        return (cStringListGenericError);
    }
    int lst = xsArrayCreateInt(2, arrSize);
    if (lst < 0) {
        xsArrayResizeString(newStrLst, 0);
        return (cStringListGenericError);
    }
    for (i = 0; < arrSize) {
        xsArraySetString(newStrLst, i, xsArrayGetString(arr, i));
    }
    xsArraySetInt(lst, 1, newStrLst);
    return (lst);
}

/*
    Wraps an existing XS string array as a list without copying elements.
    @param arr - XS string array id to use as backing storage
    @return list id, or `cStringListMaxCapacityError`/`cStringListGenericError` on error
*/
int xsStringListUseArrayAsSource(int arr = -1) {
    int arrSize = xsArrayGetSize(arr);
    if (arrSize > cStringListMaxCapacity) {
        return (cStringListMaxCapacityError);
    }
    int lst = xsArrayCreateInt(2, arrSize);
    if (lst < 0) {
        return (cStringListGenericError);
    }
    xsArraySetInt(lst, 1, arr);
    return (lst);
}

/*
    Returns the element at the given index. Sets last error on failure.
    @param lst - list id
    @param idx - zero-based index
    @return value at index, or "-1" on error
*/
string xsStringListGet(int lst = -1, int idx = -1) {
    int size = xsStringListSize(lst);
    if ((idx < 0) || (idx >= size)) {
        _stringListLastOperationStatus = cStringListIndexOutOfRangeError;
        return ("-1");
    }
    _stringListLastOperationStatus = cStringListSuccess;
    return (xsArrayGetString(xsArrayGetInt(lst, 1), idx));
}

/*
    Sets the element at the given index to a new value.
    @param lst - list id
    @param idx - zero-based index
    @param value - new value to set
    @return `cStringListSuccess` on success, or error if negative
*/
int xsStringListSet(int lst = -1, int idx = -1, string value = "") {
    int size = xsArrayGetInt(lst, 0);
    if ((idx < 0) || (idx >= size)) {
        return (cStringListIndexOutOfRangeError);
    }
    xsArraySetString(xsArrayGetInt(lst, 1), idx, value);
    return (cStringListSuccess);
}

int _xsStringListExtendStringArray(int lst = -1, int capacity = 0) {
    if (capacity >= cStringListMaxCapacity) {
        return (cStringListMaxCapacityError);
    }
    int newCapacity = 0;
    if (capacity > (cStringListMaxCapacity / 2)) {
        newCapacity = cStringListMaxCapacity;
    } else {
        newCapacity = capacity * 2;
    }
    if (newCapacity > cStringListMaxCapacity) {
        newCapacity = cStringListMaxCapacity;
    } else if (newCapacity == 0) {
        newCapacity = 8;
    }
    int r = xsArrayResizeString(lst, newCapacity);
    if (r != 1) {
        return (cStringListResizeFailedError);
    }
    return (cStringListSuccess);
}

int _xsStringListShrinkStringArray(int lst = -1, int size = 0, int capacity = 0) {
    if (size <= (capacity / 2)) {
        int r = xsArrayResizeString(lst, capacity / 2);
        if (r != 1) {
            return (cStringListResizeFailedError);
        }
    }
    return (cStringListSuccess);
}

/*
    Appends a value to the end of the list, growing the backing array if needed.
    @param lst - list id
    @param value - value to append
    @return `cStringListSuccess` on success, or error if negative
*/
int xsStringListAppend(int lst = -1, string value = "") {
    int strLst = xsArrayGetInt(lst, 1);
    int capacity = xsArrayGetSize(strLst);
    int size = xsArrayGetInt(lst, 0);
    if (capacity <= size) {
        int r = _xsStringListExtendStringArray(strLst, capacity);
        if (r != cStringListSuccess) {
            return (r);
        }
    }
    xsArraySetString(strLst, size, value);
    xsArraySetInt(lst, 0, size + 1);
    return (cStringListSuccess);
}

int _xsStringListFindSeparator(string text = "", string separator = ",", int start = 0) {
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

int _xsStringListSplitItems(string items = "") {
    int numParts = 1;
    int sep = _xsStringListFindSeparator(items, ",", 0);
    while (sep >= 0) {
        numParts++;
        sep = _xsStringListFindSeparator(items, ",", sep + 1);
    }
    int parts = xsArrayCreateString(numParts);
    int start = 0;
    for (i = 0; < numParts) {
        int end = _xsStringListFindSeparator(items, ",", start);
        if (end < 0) {
            xsArraySetString(parts, i, strRemove(items, 0, start));
        } else {
            xsArraySetString(parts, i, strSubstring(items, start, end));
        }
        start = end + 1;
    }
    return (parts);
}

bool _xsStringListIsQuoted(string text = "") {
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
    Creates a list from a comma separated string, e.g. `"'a','b c'"`. Strings must be wrapped in `'` and cannot contain `'`.
    Items are trimmed, and items that cannot be parsed are skipped.
    @param items - comma separated values
    @return created list id, or `cStringListGenericError` on error
*/
int xsStringListFromString(string items = "") {
    if (strTrim(items) == "") {
        return (xsStringListCreate());
    }
    int parts = _xsStringListSplitItems(items);
    int numParts = xsArrayGetSize(parts);
    int lst = xsStringListCreate(numParts);
    if (lst < 0) {
        xsArrayResizeString(parts, 0);
        return (cStringListGenericError);
    }
    for (i = 0; < numParts) {
        string item = strTrim(xsArrayGetString(parts, i));
        if (_xsStringListIsQuoted(item)) {
            string value = strSubstring(item, 1, strLen(item) - 1);
            xsStringListAppend(lst, value);
        }
    }
    xsArrayResizeString(parts, 0);
    return (lst);
}

/*
    Inserts a value at the given index, shifting subsequent elements to the right.
    @param lst - list id
    @param idx - zero-based index at which to insert
    @param value - value to insert
    @return `cStringListSuccess` on success, or error if negative
*/
int xsStringListInsert(int lst = -1, int idx = -1, string value = "") {
    int size = xsArrayGetInt(lst, 0);
    if ((idx < 0) || (idx > size)) {
        return (cStringListIndexOutOfRangeError);
    }
    int newSize = size + 1;
    int strLst = xsArrayGetInt(lst, 1);
    int capacity = xsArrayGetSize(strLst);
    if (capacity < newSize) {
        int r = _xsStringListExtendStringArray(strLst, capacity);
        if (r != cStringListSuccess) {
            return (r);
        }
    }
    for (i = size; > idx) {
        xsArraySetString(strLst, i, xsArrayGetString(strLst, i - 1));
    }
    xsArraySetString(strLst, idx, value);
    xsArraySetInt(lst, 0, newSize);
    return (cStringListSuccess);
}

/*
    Removes and returns the element at the given index, shifting subsequent elements to the left.
    Defaults to the last element. Sets last error on failure.
    @param lst - list id
    @param idx - zero-based index of element to remove (defaults to last)
    @return removed value, or "-1" on error
*/
string xsStringListPop(int lst = -1, int idx = cStringListMaxCapacity) {
    int strLst = xsArrayGetInt(lst, 1);
    int capacity = xsArrayGetSize(strLst);
    int size = xsArrayGetInt(lst, 0);
    if (idx == cStringListMaxCapacity) {
        idx = size - 1;
    }
    if ((idx < 0) || (idx >= size)) {
        _stringListLastOperationStatus = cStringListIndexOutOfRangeError;
        return ("-1");
    }
    string removedElem = xsArrayGetString(strLst, idx);
    for (i = idx; < size - 1) {
        xsArraySetString(strLst, i, xsArrayGetString(strLst, i + 1));
    }
    xsArraySetInt(lst, 0, size - 1);
    int r = _xsStringListShrinkStringArray(strLst, size, capacity);
    if (r != cStringListSuccess) {
        _stringListLastOperationStatus = r;
        return ("-1");
    }
    _stringListLastOperationStatus = cStringListSuccess;
    return (removedElem);
}

/*
    Removes the first occurrence of the given value from the list.
    @param lst - list id
    @param value - value to remove
    @return index of the removed element, or `cStringListGenericError` if not found
*/
int xsStringListRemove(int lst = -1, string value = "") {
    int strLst = xsArrayGetInt(lst, 1);
    int size = xsArrayGetInt(lst, 0);
    int foundIdx = -1;
    int i = 0;
    while ((i < size) && (foundIdx == -1)) {
        string cVal = xsArrayGetString(strLst, i);
        if (cVal == value) {
            foundIdx = i;
        }
        i++;
    }
    if (foundIdx == -1) {
        return (cStringListGenericError);
    }
    int newSize = size - 1;
    for (j = foundIdx; < newSize) {
        xsArraySetString(strLst, j, xsArrayGetString(strLst, j + 1));
    }
    xsArraySetInt(lst, 0, newSize);
    int capacity = xsArrayGetSize(strLst);
    int r = _xsStringListShrinkStringArray(strLst, size, capacity);
    if (r != cStringListSuccess) {
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
    @return index of the value, or `cStringListGenericError` if not found
*/
int xsStringListIndex(int lst = -1, string value = "", int start = 0, int stop = cStringListEmptyIntParam) {
    int size = xsArrayGetInt(lst, 0);
    int strLst = xsArrayGetInt(lst, 1);
    if ((stop == cStringListEmptyIntParam) || (stop > size)) {
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
        if (xsArrayGetString(strLst, i) == value) {
            return (i);
        }
    }
    return (cStringListGenericError);
}

/*
    Checks whether the list contains the given value.
    @param lst - list id
    @param value - value to search for
    @return true if the value is found, false otherwise
*/
bool xsStringListContains(int lst = -1, string value = "") {
    return (xsStringListIndex(lst, value) > -1);
}

bool _xsStringListCompareElem(string a = "", string b = "", bool reverse = false) {
    if (reverse) {
        return (a > b);
    }
    return (a < b);
}

void _xsStringListSiftDown(int lst = -1, int start = -1, int end = -1, bool reverse = false) {
    int root = start;
    while (true) {
        int child = (2 * root) + 1;
        if (child > end) {
            return;
        }
        string childVal = xsArrayGetString(lst, child);
        if ((child + 1) <= end) {
            string childVal1 = xsArrayGetString(lst, child + 1);
            if (_xsStringListCompareElem(childVal, childVal1, reverse)) {
                child++;
                childVal = childVal1;
            }
        }
        string rootVal = xsArrayGetString(lst, root);
        if (_xsStringListCompareElem(rootVal, childVal, reverse)) {
            xsArraySetString(lst, root, childVal);
            xsArraySetString(lst, child, rootVal);
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
void xsStringListSort(int lst = -1, bool reverse = false) {
    int size = xsArrayGetInt(lst, 0);
    int strLst = xsArrayGetInt(lst, 1);
    for (start = (size / 2) - 1; > -1) {
        _xsStringListSiftDown(strLst, start, size - 1, reverse);
    }
    for (end = size - 1; > 0) {
        string temp = xsArrayGetString(strLst, 0);
        xsArraySetString(strLst, 0, xsArrayGetString(strLst, end));
        xsArraySetString(strLst, end, temp);
        _xsStringListSiftDown(strLst, 0, end - 1, reverse);
    }
}

int _xsStringListEnsureSortBuffers(int keysSize = 0, int valuesSize = 0) {
    if (_stringListSortKeys < 0) {
        _stringListSortKeys = xsArrayCreateString(keysSize);
        if (_stringListSortKeys < 0) {
            return (cStringListGenericError);
        }
    }
    if (_stringListSortValues < 0) {
        _stringListSortValues = xsArrayCreateInt(valuesSize);
        if (_stringListSortValues < 0) {
            return (cStringListGenericError);
        }
    }
    int r = 1;
    if (xsArrayGetSize(_stringListSortKeys) < keysSize) {
        r = xsArrayResizeString(_stringListSortKeys, keysSize);
        if (r != 1) {
            return (cStringListResizeFailedError);
        }
    }
    if (xsArrayGetSize(_stringListSortValues) < valuesSize) {
        r = xsArrayResizeInt(_stringListSortValues, valuesSize);
        if (r != 1) {
            return (cStringListResizeFailedError);
        }
    }
    return (cStringListSuccess);
}

void _xsStringListReleaseSortBuffers(bool releaseBuffers = true) {
    if (releaseBuffers == false) {
        return;
    }
    if (_stringListSortKeys >= 0) {
        xsArrayResizeString(_stringListSortKeys, 0);
    }
    if (_stringListSortValues >= 0) {
        xsArrayResizeInt(_stringListSortValues, 0);
    }
}

void _xsStringListInsertionSortWith(int data = -1, int other = -1, int lo = 0, int hi = 0, int voff = 0, bool reverse = false) {
    for (i = lo + 1; < hi) {
        string key = xsArrayGetString(data, i);
        int value = xsArrayGetInt(other, i + voff);
        int j = i - 1;
        bool shifting = true;
        while (shifting && (j >= lo)) {
            string prev = xsArrayGetString(data, j);
            if (_xsStringListCompareElem(key, prev, reverse)) {
                xsArraySetString(data, j + 1, prev);
                xsArraySetInt(other, (j + 1) + voff, xsArrayGetInt(other, j + voff));
                j--;
            } else {
                shifting = false;
            }
        }
        xsArraySetString(data, j + 1, key);
        xsArraySetInt(other, (j + 1) + voff, value);
    }
}

void _xsStringListMergeWith(int src = -1, int srcOther = -1, int dst = -1, int dstOther = -1, int lo = 0, int mid = 0, int hi = 0, int voff = 0, bool reverse = false) {
    int i = lo;
    int j = mid;
    int k = lo;
    if ((i < mid) && (j < hi)) {
        string left = xsArrayGetString(src, i);
        string right = xsArrayGetString(src, j);
        while ((i < mid) && (j < hi)) {
            if (_xsStringListCompareElem(right, left, reverse)) {
                xsArraySetString(dst, k, right);
                xsArraySetInt(dstOther, k + voff, xsArrayGetInt(srcOther, j + voff));
                j++;
                if (j < hi) {
                    right = xsArrayGetString(src, j);
                }
            } else {
                xsArraySetString(dst, k, left);
                xsArraySetInt(dstOther, k + voff, xsArrayGetInt(srcOther, i + voff));
                i++;
                if (i < mid) {
                    left = xsArrayGetString(src, i);
                }
            }
            k++;
        }
    }
    while (i < mid) {
        xsArraySetString(dst, k, xsArrayGetString(src, i));
        xsArraySetInt(dstOther, k + voff, xsArrayGetInt(srcOther, i + voff));
        i++;
        k++;
    }
    while (j < hi) {
        xsArraySetString(dst, k, xsArrayGetString(src, j));
        xsArraySetInt(dstOther, k + voff, xsArrayGetInt(srcOther, j + voff));
        j++;
        k++;
    }
}

/*
    Sorts the list in-place using a stable merge sort, and moves the elements of `other` the same way,
    so `other[i]` stays paired with `lst[i]`. Equal elements keep their original order.
    Inputs larger than 16 elements use two internal buffer arrays shared by all calls.
    @param lst - list id
    @param other - int list id of the same size as `lst`
    @param reverse - if true, sorts in descending order
    @param release_buffers - if true, resizes the internal buffers to 0 after sorting to free their memory;
        the same buffers are grown again on the next call
    @return `cStringListSuccess` on success, `cStringListGenericError` if the sizes differ or buffers
        can't be created, or `cStringListResizeFailedError` if the buffers can't grow
*/
int xsStringListSortWith(int lst = -1, int other = -1, bool reverse = false, bool releaseBuffers = true) {
    int size = xsArrayGetInt(lst, 0);
    int data = xsArrayGetInt(lst, 1);
    int start = 0;
    int end = size;
    int voff = 1;
    if (xsArrayGetInt(other, 0) != size) {
        return (cStringListGenericError);
    }
    int run = 16;
    if (size > run) {
        int r = _xsStringListEnsureSortBuffers(end, end + voff);
        if (r != cStringListSuccess) {
            _xsStringListReleaseSortBuffers(releaseBuffers);
            return (r);
        }
    }
    int runStart = start;
    while (runStart < end) {
        int runEnd = runStart + run;
        if (runEnd > end) {
            runEnd = end;
        }
        _xsStringListInsertionSortWith(data, other, runStart, runEnd, voff, reverse);
        runStart = runEnd;
    }
    if (size <= run) {
        return (cStringListSuccess);
    }
    int src = data;
    int srcOther = other;
    int dst = _stringListSortKeys;
    int dstOther = _stringListSortValues;
    bool inBuffers = false;
    int width = run;
    while (width < size) {
        int lo = start;
        while (lo < end) {
            int mid = lo + width;
            if (mid > end) {
                mid = end;
            }
            int hi = mid + width;
            if (hi > end) {
                hi = end;
            }
            _xsStringListMergeWith(src, srcOther, dst, dstOther, lo, mid, hi, voff, reverse);
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
        for (i = start; < end) {
            xsArraySetString(data, i, xsArrayGetString(src, i));
            xsArraySetInt(other, i + voff, xsArrayGetInt(srcOther, i + voff));
        }
    }
    _xsStringListReleaseSortBuffers(releaseBuffers);
    return (cStringListSuccess);
}

/*
    Returns a string representation of the list, by default in the format `["v0", "v1", ...]`.
    @param lst - list id
    @param start - string prepended to the output
    @param sep - separator between elements
    @param end - string appended to the output
    @param quote - string wrapped around string elements
    @return string representation of the list
*/
string xsStringListToString(int lst = -1, string start = "[", string sep = ", ", string end = "]", string quote = "\"") {
    int size = xsArrayGetInt(lst, 0);
    int strLst = xsArrayGetInt(lst, 1);
    string s = start;
    for (i = 0; < size) {
        s = s + ((quote + xsArrayGetString(strLst, i)) + quote);
        if (i < (size - 1)) {
            s = s + sep;
        }
    }
    s = s + end;
    return (s);
}

/*
    Returns a copy of the list, optionally sliced by [start, end). Negative start/end are relative to the end.
    @param lst - list id
    @param start - start of slice (inclusive)
    @param end - end of slice (exclusive), defaults to list size
    @return new list id, or `cStringListGenericError` on error
*/
int xsStringListCopy(int lst = -1, int start = 0, int end = cStringListMaxCapacity) {
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
        return (cStringListGenericError);
    }
    int newStrLst = xsArrayCreateString(newSize);
    if (newStrLst < 0) {
        xsArrayResizeInt(newLst, 0);
        return (cStringListGenericError);
    }
    xsArraySetInt(newLst, 1, newStrLst);
    int strLst = xsArrayGetInt(lst, 1);
    for (i = fr; < to) {
        xsArraySetString(newStrLst, i - fr, xsArrayGetString(strLst, i));
    }
    return (newLst);
}

/*
    Appends all elements from another list to the source list.
    @param source - list id to extend
    @param lst - list id whose elements are appended
    @return `cStringListSuccess` on success, or error if negative
*/
int xsStringListExtend(int source = -1, int lst = -1) {
    int sourceSize = xsArrayGetInt(source, 0);
    int toAdd = xsArrayGetInt(lst, 0);
    int strSource = xsArrayGetInt(source, 1);
    int capacity = xsArrayGetSize(strSource);
    int newSize = sourceSize + toAdd;
    if (newSize > capacity) {
        if (newSize > cStringListMaxCapacity) {
            return (cStringListMaxCapacityError);
        }
        int r = xsArrayResizeString(strSource, newSize);
        if (r != 1) {
            return (cStringListResizeFailedError);
        }
    }
    int strList = xsArrayGetInt(lst, 1);
    for (i = 0; < toAdd) {
        xsArraySetString(strSource, i + sourceSize, xsArrayGetString(strList, i));
    }
    xsArraySetInt(source, 0, newSize);
    return (cStringListSuccess);
}

/*
    Appends all elements from an XS array to the source list.
    @param source - list id to extend
    @param arr - XS array id whose elements are appended
    @return `cStringListSuccess` on success, or error if negative
*/
int xsStringListExtendWithArray(int source = -1, int arr = -1) {
    int sourceSize = xsArrayGetInt(source, 0);
    int toAdd = xsArrayGetSize(arr);
    int strSource = xsArrayGetInt(source, 1);
    int capacity = xsArrayGetSize(strSource);
    int newSize = sourceSize + toAdd;
    if (newSize > capacity) {
        if ((newSize > cStringListMaxCapacity) || (newSize < 0)) {
            return (cStringListMaxCapacityError);
        }
        int r = xsArrayResizeString(strSource, newSize);
        if (r != 1) {
            return (cStringListResizeFailedError);
        }
    }
    for (i = 0; < toAdd) {
        xsArraySetString(strSource, i + sourceSize, xsArrayGetString(arr, i));
    }
    xsArraySetInt(source, 0, newSize);
    return (cStringListSuccess);
}

/*
    Removes all elements from the list and shrinks the backing array.
    @param lst - list id
    @return `cStringListSuccess` on success, or error if negative
*/
int xsStringListClear(int lst = -1) {
    int strList = xsArrayGetInt(lst, 1);
    int capacity = xsArrayGetSize(strList);
    if (capacity > 8) {
        int r = xsArrayResizeString(strList, 8);
        if (r != 1) {
            return (cStringListResizeFailedError);
        }
    }
    xsArraySetInt(lst, 0, 0);
    return (cStringListSuccess);
}

/*
    Resizes all arrays of the list to 0 to free their memory. XS can't fully delete arrays,
    so the list id stays allocated and must not be used afterwards.
    @param lst - list id
    @return `cStringListSuccess` on success, or `cStringListResizeFailedError` if any resize fails
*/
int xsStringListDelete(int lst = -1) {
    int r = xsArrayResizeString(xsArrayGetInt(lst, 1), 0);
    if (r != 1) {
        return (cStringListResizeFailedError);
    }
    r = xsArrayResizeInt(lst, 0);
    if (r != 1) {
        return (cStringListResizeFailedError);
    }
    return (cStringListSuccess);
}

/*
    Performs lexicographic comparison of two lists.
    @param lst1 - first list id
    @param lst2 - second list id
    @return -1 if lst1 < lst2, 1 if lst1 > lst2, 0 if equal
*/
int xsStringListCompare(int lst1 = -1, int lst2 = -1) {
    int size1 = xsArrayGetInt(lst1, 0);
    int size2 = xsArrayGetInt(lst2, 0);
    int strList1 = xsArrayGetInt(lst1, 1);
    int strList2 = xsArrayGetInt(lst2, 1);
    int i = 0;
    while ((i < size1) && (i < size2)) {
        string v1 = xsArrayGetString(strList1, i);
        string v2 = xsArrayGetString(strList2, i);
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
    Reverses the list in-place.
    @param lst - list id
*/
void xsStringListReverse(int lst = -1) {
    int size = xsArrayGetInt(lst, 0);
    int strList = xsArrayGetInt(lst, 1);
    int mid = size / 2;
    for (i = 0; < mid) {
        string temp = xsArrayGetString(strList, i);
        int backI = (size - i) - 1;
        xsArraySetString(strList, i, xsArrayGetString(strList, backI));
        xsArraySetString(strList, backI, temp);
    }
}

/*
    Counts the number of occurrences of a value in the list.
    @param lst - list id
    @param value - value to count
    @return number of occurrences
*/
int xsStringListCount(int lst = -1, string value = "") {
    int count = 0;
    int size = xsArrayGetInt(lst, 0);
    int strList = xsArrayGetInt(lst, 1);
    for (i = 0; < size) {
        if (xsArrayGetString(strList, i) == value) {
            count++;
        }
    }
    return (count);
}

/*
    Returns the minimum value in the list (lexicographic). Sets last error on failure.
    @param lst - list id
    @return minimum value, or "-1" on error
*/
string xsStringListMin(int lst = -1) {
    int size = xsArrayGetInt(lst, 0);
    if (size == 0) {
        _stringListLastOperationStatus = cStringListIndexOutOfRangeError;
        return ("-1");
    }
    int strList = xsArrayGetInt(lst, 1);
    string m = xsArrayGetString(strList, 0);
    if (size == 1) {
        _stringListLastOperationStatus = cStringListSuccess;
        return (m);
    }
    for (i = 1; < size) {
        string v = xsArrayGetString(strList, i);
        if (v < m) {
            m = v;
        }
    }
    _stringListLastOperationStatus = cStringListSuccess;
    return (m);
}

/*
    Returns the maximum value in the list (lexicographic). Sets last error on failure.
    @param lst - list id
    @return maximum value, or "-1" on error
*/
string xsStringListMax(int lst = -1) {
    int size = xsArrayGetInt(lst, 0);
    if (size == 0) {
        _stringListLastOperationStatus = cStringListIndexOutOfRangeError;
        return ("-1");
    }
    int strList = xsArrayGetInt(lst, 1);
    string m = xsArrayGetString(strList, 0);
    if (size == 1) {
        _stringListLastOperationStatus = cStringListSuccess;
        return (m);
    }
    for (i = 1; < size) {
        string v = xsArrayGetString(strList, i);
        if (v > m) {
            m = v;
        }
    }
    _stringListLastOperationStatus = cStringListSuccess;
    return (m);
}

/*
    Returns the status code of the last operation that sets it (get, pop, min, max).
    @return `cStringListSuccess` if the last such operation succeeded, or a negative error code
*/
int xsStringListLastError() {
    return (_stringListLastOperationStatus);
}

# aoe2de_xslibs

A reusable XS library pack for Age of Empires II: Definitive Edition.
It adds growable lists, `int`/`vector`/`string` dictionary variants, bitwise helpers, and a Mersenne Twister random number generator.

## Why these libraries?

XS gives you arrays, vectors, and primitive types, but larger scripts quickly run into a few missing building blocks:

- dynamic array with an api inspired by python list
- hash table with an api inspired by python dictionary
- bitwise operations as xs functions
- a pseudo-random number generator with good random distribution based on the mersenne twister algorithm

This repo packages those missing pieces as drop-in `.xs` files.
If you only want to use the libraries in a scenario, the generated files in [`xs/`](xs/) are the ones you need.
The Python source used to generate them lives in [`src/xs/`](src/xs/).

## Example usage

The example below shows the libraries working together in a small script.

```cpp
void main() {
    int scores = xsIntList(120, 85, 200, 145);
    xsIntListAppend(scores, 310);
    xsIntListAppend(scores, 25);
    
    int civUnits = xsIntIntDict(
      cBritons, 8, 
      cTeutons, 25,
      cSaracens, 282,
    );
    int unit = xsIntIntDictGet(civUnits, xsGetPlayerCivilization(1), 38);

    int roll = xsMtRandomUniformRange(1, 100);

    int bitFlag = xsBitShiftLeft(1, 8);

    xsChatData("List: " + xsIntListToString(scores));
    xsChatData("Dict: " + xsIntIntDictToString(civUnits));
    xsChatData("Roll: " + roll);
    xsChatData("Bit Flag: " + bitFlag);
}
```

### A note about handles

All lists and dictionaries are returned as an `int` handle.
You pass that handle to every follow-up function call for that object.

# Using aoe2de_xslibs

## 1. Pick the generated `.xs` files

If you only want to use the libraries in a scenario, use the files from [`xs/`](xs/).
You do not need the Python tooling for that.

| File | Provides |
|---|---|
| `intList.xs` | Dynamic list of `int` values |
| `floatList.xs` | Dynamic list of `float` values |
| `boolList.xs` | Dynamic list of `bool` values |
| `stringList.xs` | Dynamic list of `string` values |
| `vectorList.xs` | Dynamic list of `vector` values |
| `intIntDict.xs` | Hash map from `int` keys to `int` values |
| `intStringDict.xs` | Hash map from `int` keys to `string` values |
| `stringIntDict.xs` | Dictionary from `string` keys to `int` values |
| `stringVectorDict.xs` | Dictionary from `string` keys to `vector` values |
| `stringStringDict.xs` | Dictionary from `string` keys to `string` values |
| `intVectorDict.xs` | Hash map from `int` keys to `vector` values |
| `vectorIntDict.xs` | Hash map from `vector` keys to `int` values |
| `vectorStringDict.xs` | Hash map from `vector` keys to `string` values |
| `vectorVectorDict.xs` | Hash map from `vector` keys to `vector` values |
| `binaryFunctions.xs` | Bitwise helpers and MT19937 random number functions |

## 2. Add them to your script

There are three straightforward ways to use the libraries.

### Option A - Using `include`

1. Place the `.xs` files you need in a folder AoE2 DE can load scripts from, for example:
   `C:\Users\<user>\Games\Age of Empires 2 DE\<steamId>\resources\_common\xs\`

2. Include the files at the top of your script:

   ```cpp
   include "intList.xs";
   include "intIntDict.xs";
   include "binaryFunctions.xs";
   ```

### Option B - Copy and paste the file contents

Copy the contents of the generated `.xs` files you want and paste them above your `void main()` function.

### Option C - Copy and paste them into a `Script Call` Effect

Copy the contents of the generated `.xs` files into a disabled `Script Call`. 
Make sure that effect starts with some function definition (eg: `void header123(){}`) otherwise it will show up as 
red but still work.

## 3. A few rules to remember

- The list creation helpers and all dictionary constructors return an `int` handle.
- The dictionary `Keys` and `Values` helpers return raw XS arrays, not list handles.
- `xsIntIntDictKeys`/`Values` return `int[]` / `int[]`.
- `xsIntStringDictKeys`/`Values` return `int[]` / `string[]`.
- `xsStringIntDictKeys`/`Values` return `string[]` / `int[]`.
- `xsStringVectorDictKeys`/`Values` return `string[]` / `vector[]`.
- `xsStringStringDictKeys`/`Values` return `string[]` / `string[]`.
- `xsIntVectorDictKeys`/`Values` return `int[]` / `vector[]`.
- `xsVectorIntDictKeys`/`Values` return `vector[]` / `int[]`.
- `xsVectorStringDictKeys`/`Values` return `vector[]` / `string[]`.
- `xsVectorVectorDictKeys`/`Values` return `vector[]` / `vector[]`.
- There is no global initialization function for these libraries. You can use them immediately.
- `xsIntIntDict`, `xsIntStringDict`, and `xsIntVectorDict` cannot store their reserved `...EmptyKey` int sentinel as a key.
- `xsVectorIntDict`, `xsVectorStringDict`, and `xsVectorVectorDict` cannot store their reserved `...EmptyKey` vector sentinel as a key.
- `xsStringIntDict` cannot store the reserved sentinel string `!<[empty` as a key.
- `xsStringVectorDict` cannot store the reserved sentinel string `!<[empty` as a key.
- `xsStringStringDict` cannot store the reserved sentinel string `!<[empty` as a key.

## 4. Int List

`intList.xs` provides a dynamic array of 32-bit integers.
Use it when you want list-style operations such as append, insert, copy, sort, reverse, search, and aggregation.

### Constants

| Constant | Value | Meaning |
|---|---|---|
| `cIntListSuccess` | `0` | Operation succeeded |
| `cIntListGenericError` | `-1` | General failure |
| `cIntListIndexOutOfRangeError` | `-2` | Index out of bounds |
| `cIntListResizeFailedError` | `-3` | Array allocation failed |
| `cIntListMaxCapacityError` | `-4` | Exceeded maximum capacity |
| `cIntListMaxCapacity` | `999999999` | Hard upper limit |
| `cIntListEmptyParam` | `-999999999` | Internal constructor sentinel |

### API

```cpp
// Creation
int xsIntList(int v0, int v1, ..., int v11)       // up to 12 initial values
int xsIntListCreate(int capacity)
int xsIntListFromRange(int start, int stop, int step)
int xsIntListFromRepeatedVal(int value, int times)
int xsIntListFromRepeatedList(int lst, int times)
int xsIntListFromArray(int arr)
int xsIntListUseArrayAsSource(int arr)            // convert existing array in place

// Access
int    xsIntListGet(int lst, int idx)
int    xsIntListSet(int lst, int idx, int value)  // returns status code
int    xsIntListSize(int lst)

// Modification
int    xsIntListAppend(int lst, int value)
int    xsIntListInsert(int lst, int idx, int value)
int    xsIntListPop(int lst, int idx)
int    xsIntListRemove(int lst, int value)
int    xsIntListClear(int lst)
void   xsIntListReverse(int lst)
void   xsIntListSort(int lst, bool reverse)

// Search
bool   xsIntListContains(int lst, int value)
int    xsIntListIndex(int lst, int value, int start, int stop)
int    xsIntListCount(int lst, int value)

// Aggregation
int    xsIntListSum(int lst)
int    xsIntListMin(int lst)
int    xsIntListMax(int lst)

// Bulk operations
int    xsIntListCopy(int lst, int start, int end)
int    xsIntListExtend(int source, int lst)
int    xsIntListExtendWithArray(int source, int arr)
int    xsIntListCompare(int lst1, int lst2)

// Diagnostics
string xsIntListToString(int lst)
int    xsIntListLastError()
```

### Example

```cpp
void updateScores() {
    int scores = xsIntList(120, 85, 200, 145);

    xsIntListSet(scores, 2, xsIntListGet(scores, 2) + 50);
    xsIntListSort(scores, false);

    xsChatData("Leader score: " + xsIntListMax(scores));
}
```

## 5. Float List

`floatList.xs` provides a dynamic array of 32-bit floats.
It largely mirrors Int List, but there is no `xsFloatListFromRange`.

### Constants

| Constant | Value | Meaning |
|---|---|---|
| `cFloatListSuccess` | `0` | Operation succeeded |
| `cFloatListGenericError` | `-1` | General failure |
| `cFloatListGenericErrorFloat` | `-1.0` | Error return for float-valued operations |
| `cFloatListIndexOutOfRangeError` | `-2` | Index out of bounds |
| `cFloatListResizeFailedError` | `-3` | Array allocation failed |
| `cFloatListMaxCapacityError` | `-4` | Exceeded maximum capacity |
| `cFloatListMaxCapacity` | `999999999` | Hard upper limit |
| `cFloatListEmptyParam` | `-9999999.0` | Internal constructor sentinel |
| `cFloatListEmptyIntParam` | `-999999999` | Internal optional-int sentinel |

### API

```cpp
// Creation
int   xsFloatList(float v0, float v1, ..., float v11)
int   xsFloatListCreate(int capacity)
int   xsFloatListFromRepeatedVal(float value, int times)
int   xsFloatListFromRepeatedList(int lst, int times)
int   xsFloatListFromArray(int arr)
int   xsFloatListUseArrayAsSource(int arr)        // convert existing array in place

// Access
float xsFloatListGet(int lst, int idx)
int   xsFloatListSet(int lst, int idx, float value)
int   xsFloatListSize(int lst)

// Modification
int   xsFloatListAppend(int lst, float value)
int   xsFloatListInsert(int lst, int idx, float value)
float xsFloatListPop(int lst, int idx)
int   xsFloatListRemove(int lst, float value)
int   xsFloatListClear(int lst)
void  xsFloatListReverse(int lst)
void  xsFloatListSort(int lst, bool reverse)

// Search
bool  xsFloatListContains(int lst, float value)
int   xsFloatListIndex(int lst, float value, int start, int stop)
int   xsFloatListCount(int lst, float value)

// Aggregation
float xsFloatListSum(int lst)
float xsFloatListMin(int lst)
float xsFloatListMax(int lst)

// Bulk operations
int   xsFloatListCopy(int lst, int start, int end)
int   xsFloatListExtend(int source, int lst)
int   xsFloatListExtendWithArray(int source, int arr)
int   xsFloatListCompare(int lst1, int lst2)

// Diagnostics
string xsFloatListToString(int lst)
int    xsFloatListLastError()
```

### Example

```cpp
float averageRate(int rates) {
    int n = xsFloatListSize(rates);
    if (n == 0) {
        return (0.0);
    }
    return (xsFloatListSum(rates) / n);
}

void trackRates() {
    int rates = xsFloatList(1.5, 2.0, 0.75, 3.25);
    xsFloatListAppend(rates, 1.0);

    xsChatData("Average rate: " + averageRate(rates));
}
```

## 6. Bool List

`boolList.xs` provides a dynamic array of booleans.
It largely mirrors String List, but it intentionally has no `xsBoolList` convenience constructor, and bool-returning error cases use `false` plus `xsBoolListLastError()` because `false` is also a valid stored value.

### Constants

| Constant | Value | Meaning |
|---|---|---|
| `cBoolListSuccess` | `0` | Operation succeeded |
| `cBoolListGenericError` | `-1` | General failure |
| `cBoolListIndexOutOfRangeError` | `-2` | Index out of bounds |
| `cBoolListResizeFailedError` | `-3` | Array allocation failed |
| `cBoolListMaxCapacityError` | `-4` | Exceeded maximum capacity |
| `cBoolListMaxCapacity` | `999999999` | Hard upper limit |
| `cBoolListEmptyIntParam` | `-999999999` | Internal optional-int sentinel |

### API

```cpp
// Creation
int  xsBoolListCreate(int capacity)
int  xsBoolListFromRepeatedVal(bool value, int times)
int  xsBoolListFromRepeatedList(int lst, int times)
int  xsBoolListFromArray(int arr)
int  xsBoolListUseArrayAsSource(int arr)          // wrap existing bool array without copying

// Access
bool xsBoolListGet(int lst, int idx)
int  xsBoolListSet(int lst, int idx, bool value)
int  xsBoolListSize(int lst)

// Modification
int  xsBoolListAppend(int lst, bool value)
int  xsBoolListInsert(int lst, int idx, bool value)
bool xsBoolListPop(int lst, int idx)
int  xsBoolListRemove(int lst, bool value)
int  xsBoolListClear(int lst)
void xsBoolListReverse(int lst)
void xsBoolListSort(int lst, bool reverse)

// Search
bool xsBoolListContains(int lst, bool value)
int  xsBoolListIndex(int lst, bool value, int start, int stop)
int  xsBoolListCount(int lst, bool value)

// Bulk operations
int  xsBoolListCopy(int lst, int start, int end)
int  xsBoolListExtend(int source, int lst)
int  xsBoolListExtendWithArray(int source, int arr)
int  xsBoolListCompare(int lst1, int lst2)

// Diagnostics
string xsBoolListToString(int lst)
int    xsBoolListLastError()
```

### Example

```cpp
void syncFlags() {
    int flags = xsBoolListCreate(4);
    xsBoolListAppend(flags, true);
    xsBoolListAppend(flags, false);
    xsBoolListAppend(flags, true);
    xsBoolListAppend(flags, false);
    xsBoolListSort(flags, true);

    if (!xsBoolListGet(flags, 0) && xsBoolListLastError() != cBoolListSuccess) {
        xsChatData("flag lookup failed");
    }
}
```

## 7. String List

`stringList.xs` provides a dynamic array of strings.
It mostly mirrors Int List, but there is no `Sum`, `xsStringListUseArrayAsSource` wraps an existing string array without copying it, and string-returning error cases use `"-1"` plus `xsStringListLastError()` because `"-1"` is also a valid stored value.

### Constants

| Constant | Value | Meaning |
|---|---|---|
| `cStringListSuccess` | `0` | Operation succeeded |
| `cStringListGenericError` | `-1` | General failure |
| `cStringListIndexOutOfRangeError` | `-2` | Index out of bounds |
| `cStringListResizeFailedError` | `-3` | Array allocation failed |
| `cStringListMaxCapacityError` | `-4` | Exceeded maximum capacity |
| `cStringListMaxCapacity` | `999999999` | Hard upper limit |
| `cStringListEmptyIntParam` | `-999999999` | Internal optional-int sentinel |

### API

```cpp
// Creation
int    xsStringList(string v0, string v1, ..., string v11)
int    xsStringListCreate(int capacity)
int    xsStringListFromRepeatedVal(string value, int times)
int    xsStringListFromRepeatedList(int lst, int times)
int    xsStringListFromArray(int arr)
int    xsStringListUseArrayAsSource(int arr)      // wrap existing string array without copying

// Access
string xsStringListGet(int lst, int idx)
int    xsStringListSet(int lst, int idx, string value)
int    xsStringListSize(int lst)

// Modification
int    xsStringListAppend(int lst, string value)
int    xsStringListInsert(int lst, int idx, string value)
string xsStringListPop(int lst, int idx)
int    xsStringListRemove(int lst, string value)
int    xsStringListClear(int lst)
void   xsStringListReverse(int lst)
void   xsStringListSort(int lst, bool reverse)

// Search
bool   xsStringListContains(int lst, string value)
int    xsStringListIndex(int lst, string value, int start, int stop)
int    xsStringListCount(int lst, string value)
string xsStringListMin(int lst)
string xsStringListMax(int lst)

// Bulk operations
int    xsStringListCopy(int lst, int start, int end)
int    xsStringListExtend(int source, int lst)
int    xsStringListExtendWithArray(int source, int arr)
int    xsStringListCompare(int lst1, int lst2)

// Diagnostics
string xsStringListToString(int lst)
int    xsStringListLastError()
```

### Example

```cpp
void announceNames() {
    int names = xsStringList("Carol", "Alice", "Bob");
    xsStringListSort(names, false);

    int numNames = xsStringListSize(names);
    for (i = 0; < numNames) {
        xsChatData("Player: " + xsStringListGet(names, i));
    }
}
```

## 8. Vector List

`vectorList.xs` provides a dynamic array of `vector` values.
Unlike the scalar list types, it only exposes operations that make sense for vectors, so there is no sort, compare, sum, min, or max API.

### Constants

| Constant | Value | Meaning |
|---|---|---|
| `cVectorListSuccess` | `0` | Operation succeeded |
| `cVectorListGenericError` | `-1` | General failure |
| `cVectorListGenericErrorVector` | `vector(-1.0, -1.0, -1.0)` | Error return for vector-valued operations |
| `cVectorListIndexOutOfRangeError` | `-2` | Index out of bounds |
| `cVectorListResizeFailedError` | `-3` | Array allocation failed |
| `cVectorListMaxCapacityError` | `-4` | Exceeded maximum capacity |
| `cVectorListMaxCapacity` | `333333333` | Hard upper limit |
| `cVectorListEmptyParam` | `vector(-9999999.0, -9999999.0, -9999999.0)` | Internal constructor sentinel |
| `cVectorListEmptyIntParam` | `-999999999` | Internal optional-int sentinel |

### API

```cpp
// Creation
int    xsVectorList(vector v0, vector v1, ..., vector v11)
int    xsVectorListCreate(int capacity)
int    xsVectorListFromRepeatedVal(vector value, int times)
int    xsVectorListFromRepeatedList(int lst, int times)
int    xsVectorListFromArray(int arr)

// Access
vector xsVectorListGet(int lst, int idx)
int    xsVectorListSet(int lst, int idx, vector value)
int    xsVectorListSize(int lst)
int    xsVectorListCapacity(int arr)

// Modification
int    xsVectorListAppend(int lst, vector value)
int    xsVectorListInsert(int lst, int idx, vector value)
vector xsVectorListPop(int lst, int idx)
int    xsVectorListRemove(int lst, vector value)
int    xsVectorListClear(int lst)
void   xsVectorListReverse(int lst)

// Search
bool   xsVectorListContains(int lst, vector value)
int    xsVectorListIndex(int lst, vector value, int start, int stop)
int    xsVectorListCount(int lst, vector value)

// Bulk operations
int    xsVectorListCopy(int lst, int start, int end)
int    xsVectorListExtend(int source, int lst)
int    xsVectorListExtendWithArray(int source, int arr)

// Diagnostics
string xsVectorListToString(int lst)
int    xsVectorListLastError()
```

### Example

```cpp
void spawnUnitsAlongPath() {
    int waypoints = xsVectorList(
        vector(10.0, 0.0, 20.0),
        vector(30.0, 0.0, 20.0),
        vector(50.0, 0.0, 35.0)
    );

    int numWaypoints = xsVectorListSize(waypoints);
    for (i = 0; < numWaypoints) {
        vector pos = xsVectorListGet(waypoints, i);
        xsChatData("Waypoint " + i + ": " + pos);
    }
}
```

## 9. Int to Int Dictionary

`intIntDict.xs` provides a hash map from `int` keys to `int` values.
The exported implementation uses open addressing with linear probing and resizes automatically when the load factor grows past `cIntIntDictMaxLoadFactor`.

### Constants

| Constant | Value | Meaning |
|---|---|---|
| `cIntIntDictSuccess` | `0` | Operation succeeded |
| `cIntIntDictGenericError` | `-1` | General failure |
| `cIntIntDictNoKeyError` | `-2` | Key not found, or new key inserted for `Put`/`PutIfAbsent` |
| `cIntIntDictResizeFailedError` | `-3` | Resize allocation failed |
| `cIntIntDictMaxCapacityError` | `-4` | Exceeded maximum capacity |
| `cIntIntDictMaxCapacity` | `999999999` | Hard upper limit |
| `cIntIntDictMaxLoadFactor` | `0.75` | Resize trigger threshold |
| `cIntIntDictEmptyKey` | `-999999999` | Reserved empty-slot sentinel; cannot be used as a key |

### API

```cpp
// Creation
int  xsIntIntDictCreate()
int  xsIntIntDict(int k1, int v1, ..., int k6, int v6)   // up to 6 pairs

// Access
int  xsIntIntDictGet(int dct, int key, int dft)
bool xsIntIntDictContains(int dct, int key)
int  xsIntIntDictSize(int dct)

// Modification
int  xsIntIntDictPut(int dct, int key, int val)
int  xsIntIntDictPutIfAbsent(int dct, int key, int val)
int  xsIntIntDictRemove(int dct, int key)
int  xsIntIntDictClear(int dct)

// Bulk operations
int  xsIntIntDictUpdate(int source, int dct)      // copies entries from dct into source
int  xsIntIntDictCopy(int dct)
int  xsIntIntDictKeys(int dct)                    // returns a raw XS int array
int  xsIntIntDictValues(int dct)                  // returns a raw XS int array
bool xsIntIntDictEquals(int a, int b)

// Iteration
bool xsIntIntDictHasNext(int dct, bool isFirst, int prevKey)
int  xsIntIntDictNextKey(int dct, bool isFirst, int prevKey)

// Diagnostics
string xsIntIntDictToString(int dct)
int    xsIntIntDictLastError()
```

### Return-value technicalities

`xsIntIntDictPut` and `xsIntIntDictPutIfAbsent` need a quick extra check after the call because their return value alone is not enough.

- `cIntIntDictSuccess`: the key already existed, and the returned value is meaningful
- `cIntIntDictNoKeyError`: a new key was inserted
- any other negative status: the call failed

This is necessary because `cIntIntDictGenericError` (`-1`) can be both a legitimate stored value and the generic error sentinel.

### Example

```cpp
void distributeResources() {
    int budget = xsIntIntDict(1, 500, 2, 300, 3, 700);

    int current = xsIntIntDictGet(budget, 2, 0);
    xsIntIntDictPut(budget, 2, current + 100);

    bool isFirst = true;
    int prevKey = -1;

    while (xsIntIntDictHasNext(budget, isFirst, prevKey)) {
        int key = xsIntIntDictNextKey(budget, isFirst, prevKey);
        int val = xsIntIntDictGet(budget, key, 0);

        xsChatData("Player " + key + " gets " + val);

        isFirst = false;
        prevKey = key;
    }
}
```

## 10. Int to Vector Dictionary

`intVectorDict.xs` provides a hash map from `int` keys to `vector` values.
It uses the same open-addressed layout as `intIntDict.xs`, but stores vectors as raw float components.

### Constants

| Constant | Value | Meaning |
|---|---|---|
| `cIntVectorDictSuccess` | `0` | Operation succeeded |
| `cIntVectorDictGenericError` | `-1` | General failure |
| `cIntVectorDictNoKeyError` | `-2` | Key not found, or new key inserted for `Put`/`PutIfAbsent` |
| `cIntVectorDictResizeFailedError` | `-3` | Resize allocation failed |
| `cIntVectorDictMaxCapacityError` | `-4` | Exceeded maximum capacity |
| `cIntVectorDictGenericErrorVector` | `vector(-1.0, -1.0, -1.0)` | Error return for vector-valued operations |
| `cIntVectorDictMaxCapacity` | `999999997` | Hard upper limit |
| `cIntVectorDictMaxLoadFactor` | `0.75` | Resize trigger threshold |
| `cIntVectorDictEmptyKey` | `-999999999` | Reserved empty-slot sentinel; cannot be used as a key |

### API

```cpp
// Creation
int    xsIntVectorDictCreate()
int    xsIntVectorDict(int k1, vector v1, ..., int k6, vector v6)

// Access
vector xsIntVectorDictGet(int dct, int key, vector dft)
bool   xsIntVectorDictContains(int dct, int key)
int    xsIntVectorDictSize(int dct)

// Modification
vector xsIntVectorDictPut(int dct, int key, vector val)
vector xsIntVectorDictPutIfAbsent(int dct, int key, vector val)
vector xsIntVectorDictRemove(int dct, int key)
int    xsIntVectorDictClear(int dct)

// Bulk operations
int    xsIntVectorDictUpdate(int source, int dct)
int    xsIntVectorDictCopy(int dct)
int    xsIntVectorDictKeys(int dct)              // returns a raw XS int array
int    xsIntVectorDictValues(int dct)            // returns a raw XS vector array
bool   xsIntVectorDictEquals(int a, int b)

// Iteration
bool   xsIntVectorDictHasNext(int dct, bool isFirst, int prevKey)
int    xsIntVectorDictNextKey(int dct, bool isFirst, int prevKey)

// Diagnostics
string xsIntVectorDictToString(int dct)
int    xsIntVectorDictLastError()
```

### Example

```cpp
void placeCamps() {
    int camps = xsIntVectorDict(
        1, vector(12.0, 0.0, 18.0),
        2, vector(40.0, 0.0, 26.0)
    );

    vector camp = xsIntVectorDictGet(camps, 2, vector(-1.0, -1.0, -1.0));
    xsChatData("Player 2 camp: " + camp);
}
```

## 11. Int to String Dictionary

`intStringDict.xs` provides a hash map from `int` keys to `string` values.
It uses the same open-addressed layout as `intIntDict.xs`, but stores values in a parallel string array.

### Constants

| Constant | Value | Meaning |
|---|---|---|
| `cIntStringDictSuccess` | `0` | Operation succeeded |
| `cIntStringDictGenericError` | `-1` | General failure |
| `cIntStringDictNoKeyError` | `-2` | Key not found, or new key inserted for `Put`/`PutIfAbsent` |
| `cIntStringDictResizeFailedError` | `-3` | Resize allocation failed |
| `cIntStringDictMaxCapacityError` | `-4` | Exceeded maximum capacity |
| `cIntStringDictMaxCapacity` | `999999999` | Hard upper limit |
| `cIntStringDictMaxLoadFactor` | `0.75` | Resize trigger threshold |
| `cIntStringDictEmptyKey` | `-999999999` | Reserved empty-slot sentinel; cannot be used as a key |

### API

```cpp
// Creation
int    xsIntStringDictCreate()
int    xsIntStringDict(int k1, string v1, ..., int k6, string v6)

// Access
string xsIntStringDictGet(int dct, int key, string dft)
bool   xsIntStringDictContains(int dct, int key)
int    xsIntStringDictSize(int dct)

// Modification
string xsIntStringDictPut(int dct, int key, string val)
string xsIntStringDictPutIfAbsent(int dct, int key, string val)
string xsIntStringDictRemove(int dct, int key)
int    xsIntStringDictClear(int dct)

// Bulk operations
int    xsIntStringDictUpdate(int source, int dct)
int    xsIntStringDictCopy(int dct)
int    xsIntStringDictKeys(int dct)              // returns a raw XS int array
int    xsIntStringDictValues(int dct)            // returns a raw XS string array
bool   xsIntStringDictEquals(int a, int b)

// Iteration
bool   xsIntStringDictHasNext(int dct, bool isFirst, int prevKey)
int    xsIntStringDictNextKey(int dct, bool isFirst, int prevKey)

// Diagnostics
string xsIntStringDictToString(int dct)
int    xsIntStringDictLastError()
```

### Return-value technicalities

`xsIntStringDictPut`, `xsIntStringDictPutIfAbsent`, and `xsIntStringDictRemove` can all return `"-1"` in more than one situation.

- `cIntStringDictSuccess`: the operation succeeded, and the returned string is meaningful
- `cIntStringDictNoKeyError`: either the key was missing, or `Put`/`PutIfAbsent` inserted a new key
- any other negative status: the call failed

This matters because `"-1"` is also a valid stored string value.

### Example

```cpp
void namePlayers() {
    int civByPlayer = xsIntStringDict(
        1, "Britons",
        2, "Teutons",
        3, "Saracens"
    );

    string civ = xsIntStringDictGet(civByPlayer, 2, "Unknown");
    xsChatData("Player 2 civ: " + civ);
}
```

## 12. Vector to Int Dictionary

`vectorIntDict.xs` provides a hash map from `vector` keys to `int` values.
It uses direct vector equality for key lookup and reserves `cVectorIntDictEmptyKey` as the empty-slot sentinel.

### Constants

| Constant | Value | Meaning |
|---|---|---|
| `cVectorIntDictSuccess` | `0` | Operation succeeded |
| `cVectorIntDictGenericError` | `-1` | General failure |
| `cVectorIntDictNoKeyError` | `-2` | Key not found, or new key inserted for `Put`/`PutIfAbsent` |
| `cVectorIntDictResizeFailedError` | `-3` | Resize allocation failed |
| `cVectorIntDictMaxCapacityError` | `-4` | Exceeded maximum capacity |
| `cVectorIntDictGenericErrorVector` | `vector(-1.0, -1.0, -1.0)` | Error return for vector-key iteration operations |
| `cVectorIntDictMaxCapacity` | `999999997` | Hard upper limit |
| `cVectorIntDictMaxLoadFactor` | `0.75` | Resize trigger threshold |
| `cVectorIntDictEmptyKey` | `vector(-9999999.0, -9999999.0, -9999999.0)` | Reserved empty-slot sentinel; cannot be used as a key |

### API

```cpp
// Creation
int    xsVectorIntDictCreate()
int    xsVectorIntDict(vector k1, int v1, ..., vector k6, int v6)

// Access
int    xsVectorIntDictGet(int dct, vector key, int dft)
bool   xsVectorIntDictContains(int dct, vector key)
int    xsVectorIntDictSize(int dct)

// Modification
int    xsVectorIntDictPut(int dct, vector key, int val)
int    xsVectorIntDictPutIfAbsent(int dct, vector key, int val)
int    xsVectorIntDictRemove(int dct, vector key)
int    xsVectorIntDictClear(int dct)

// Bulk operations
int    xsVectorIntDictUpdate(int source, int dct)
int    xsVectorIntDictCopy(int dct)
int    xsVectorIntDictKeys(int dct)              // returns a raw XS vector array
int    xsVectorIntDictValues(int dct)            // returns a raw XS int array
bool   xsVectorIntDictEquals(int a, int b)

// Iteration
bool   xsVectorIntDictHasNext(int dct, bool isFirst, vector prevKey)
vector xsVectorIntDictNextKey(int dct, bool isFirst, vector prevKey)

// Diagnostics
string xsVectorIntDictToString(int dct)
int    xsVectorIntDictLastError()
```

### Example

```cpp
void markDangerZones() {
    int danger = xsVectorIntDict();
    xsVectorIntDictPut(danger, vector(20.0, 0.0, 20.0), 3);
    xsVectorIntDictPut(danger, vector(40.0, 0.0, 35.0), 5);

    int level = xsVectorIntDictGet(danger, vector(20.0, 0.0, 20.0), 0);
    xsChatData("Danger level: " + level);
}
```

## 13. Vector to Vector Dictionary

`vectorVectorDict.xs` provides a hash map from `vector` keys to `vector` values.
It mirrors the other dictionary variants, but both keys and values are vectors.

### Constants

| Constant | Value | Meaning |
|---|---|---|
| `cVectorVectorDictSuccess` | `0` | Operation succeeded |
| `cVectorVectorDictGenericError` | `-1` | General failure |
| `cVectorVectorDictNoKeyError` | `-2` | Key not found, or new key inserted for `Put`/`PutIfAbsent` |
| `cVectorVectorDictResizeFailedError` | `-3` | Resize allocation failed |
| `cVectorVectorDictMaxCapacityError` | `-4` | Exceeded maximum capacity |
| `cVectorVectorDictGenericErrorVector` | `vector(-1.0, -1.0, -1.0)` | Error return for vector-valued operations |
| `cVectorVectorDictMaxCapacity` | `999999997` | Hard upper limit |
| `cVectorVectorDictMaxLoadFactor` | `0.75` | Resize trigger threshold |
| `cVectorVectorDictEmptyKey` | `vector(-9999999.0, -9999999.0, -9999999.0)` | Reserved empty-slot sentinel; cannot be used as a key |

### API

```cpp
// Creation
int    xsVectorVectorDictCreate()
int    xsVectorVectorDict(vector k1, vector v1, ..., vector k6, vector v6)

// Access
vector xsVectorVectorDictGet(int dct, vector key, vector dft)
bool   xsVectorVectorDictContains(int dct, vector key)
int    xsVectorVectorDictSize(int dct)

// Modification
vector xsVectorVectorDictPut(int dct, vector key, vector val)
vector xsVectorVectorDictPutIfAbsent(int dct, vector key, vector val)
vector xsVectorVectorDictRemove(int dct, vector key)
int    xsVectorVectorDictClear(int dct)

// Bulk operations
int    xsVectorVectorDictUpdate(int source, int dct)
int    xsVectorVectorDictCopy(int dct)
int    xsVectorVectorDictKeys(int dct)           // returns a raw XS vector array
int    xsVectorVectorDictValues(int dct)         // returns a raw XS vector array
bool   xsVectorVectorDictEquals(int a, int b)

// Iteration
bool   xsVectorVectorDictHasNext(int dct, bool isFirst, vector prevKey)
vector xsVectorVectorDictNextKey(int dct, bool isFirst, vector prevKey)

// Diagnostics
string xsVectorVectorDictToString(int dct)
int    xsVectorVectorDictLastError()
```

### Example

```cpp
void remapTargets() {
    int fallback = xsVectorVectorDict(
        vector(10.0, 0.0, 10.0), vector(12.0, 0.0, 18.0),
        vector(30.0, 0.0, 15.0), vector(45.0, 0.0, 22.0)
    );

    vector next = xsVectorVectorDictGet(fallback, vector(10.0, 0.0, 10.0), vector(-1.0, -1.0, -1.0));
    xsChatData("Fallback target: " + next);
}
```

## 14. Vector to String Dictionary

`vectorStringDict.xs` provides a hash map from `vector` keys to `string` values.
It mirrors the other vector-keyed dictionary variants, but stores values in a parallel string array.

### Constants

| Constant | Value | Meaning |
|---|---|---|
| `cVectorStringDictSuccess` | `0` | Operation succeeded |
| `cVectorStringDictGenericError` | `-1` | General failure |
| `cVectorStringDictNoKeyError` | `-2` | Key not found, or new key inserted for `Put`/`PutIfAbsent` |
| `cVectorStringDictResizeFailedError` | `-3` | Resize allocation failed |
| `cVectorStringDictMaxCapacityError` | `-4` | Exceeded maximum capacity |
| `cVectorStringDictGenericErrorVector` | `vector(-1.0, -1.0, -1.0)` | Error return for vector-key iteration operations |
| `cVectorStringDictMaxCapacity` | `999999998` | Hard upper limit |
| `cVectorStringDictMaxLoadFactor` | `0.75` | Resize trigger threshold |
| `cVectorStringDictEmptyKey` | `vector(-9999999.0, -9999999.0, -9999999.0)` | Reserved empty-slot sentinel; cannot be used as a key |

### API

```cpp
// Creation
int    xsVectorStringDictCreate()
int    xsVectorStringDict(vector k1, string v1, ..., vector k6, string v6)

// Access
string xsVectorStringDictGet(int dct, vector key, string dft)
bool   xsVectorStringDictContains(int dct, vector key)
int    xsVectorStringDictSize(int dct)

// Modification
string xsVectorStringDictPut(int dct, vector key, string val)
string xsVectorStringDictPutIfAbsent(int dct, vector key, string val)
string xsVectorStringDictRemove(int dct, vector key)
int    xsVectorStringDictClear(int dct)

// Bulk operations
int    xsVectorStringDictUpdate(int source, int dct)
int    xsVectorStringDictCopy(int dct)
int    xsVectorStringDictKeys(int dct)           // returns a raw XS vector array
int    xsVectorStringDictValues(int dct)         // returns a raw XS string array
bool   xsVectorStringDictEquals(int a, int b)

// Iteration
bool   xsVectorStringDictHasNext(int dct, bool isFirst, vector prevKey)
vector xsVectorStringDictNextKey(int dct, bool isFirst, vector prevKey)

// Diagnostics
string xsVectorStringDictToString(int dct)
int    xsVectorStringDictLastError()
```

### Return-value technicalities

`xsVectorStringDictPut`, `xsVectorStringDictPutIfAbsent`, and `xsVectorStringDictRemove` can all return `"-1"` in more than one situation.

- `cVectorStringDictSuccess`: the operation succeeded, and the returned string is meaningful
- `cVectorStringDictNoKeyError`: either the key was missing, or `Put`/`PutIfAbsent` inserted a new key
- any other negative status: the call failed

This matters because `"-1"` is also a valid stored string value.

### Example

```cpp
void labelZones() {
    int labels = xsVectorStringDict(
        vector(10.0, 0.0, 10.0), "north camp",
        vector(30.0, 0.0, 18.0), "south camp"
    );

    string label = xsVectorStringDictGet(labels, vector(10.0, 0.0, 10.0), "unknown");
    xsChatData("Zone label: " + label);
}
```

## 15. Binary Operations

`binaryFunctions.xs` provides software implementations of common 32-bit bitwise operations.
Use these when you need flags, masking, shifting, or packed integer values in XS.

### API

```cpp
int xsBitAnd(int a, int b)
int xsBitOr(int a, int b)
int xsBitXor(int a, int b)
int xsBitNot(int n)
int xsBitShiftLeft(int x, int n)
int xsBitShiftRightLogical(int x, int n)
int xsBitShiftRightArithmetic(int x, int n)
```

### Example

```cpp
int pack(int high, int low) {
    return (xsBitOr(xsBitShiftLeft(high, 16), xsBitAnd(low, 65535)));
}

int unpackHigh(int packed) {
    return (xsBitShiftRightArithmetic(packed, 16));
}

int unpackLow(int packed) {
    return (xsBitAnd(packed, 65535));
}
```

## 16. Random Numbers

`binaryFunctions.xs` also includes a Mersenne Twister (`MT19937`) pseudo-random number generator.
Seed it once with `xsMtSeed`, then draw values with `xsMtRandom` or `xsMtRandomUniformRange`.

### API

```cpp
void xsMtSeed(int seed)
int  xsMtRandom()
int  xsMtRandomUniformRange(int start, int end)   // uniform int in [start, end)
```

### Example

```cpp
void randomTeams() {
    int numPlayers = 4;
    for (i = 0; < numPlayers) {
        int team = xsMtRandomUniformRange(0, 2);
        xsChatData("Player " + (i + 1) + " -> team " + team);
    }
}
```

## 17. Larger example

The example below shows `Int List`, `IntIntDict`, bitwise flags, and the MT RNG working together in one script.

```cpp
include "intList.xs";
include "intIntDict.xs";
include "binaryFunctions.xs";

void main() {
    int players = xsIntList(1, 2, 3, 4);
    int scoreByPlayer = xsIntIntDict();
    int flagsByPlayer = xsIntIntDict();

    int cFlagElite = xsBitShiftLeft(1, 0);

    int numPlayers = xsIntListSize(players);
    for (i = 0; < numPlayers) {
        int player = xsIntListGet(players, i);
        int score = 100 + xsMtRandomUniformRange(0, 76);
        int flags = 0;

        if (score >= 150) {
            flags = xsBitOr(flags, cFlagElite);
        }

        xsIntIntDictPut(scoreByPlayer, player, score);
        xsIntIntDictPut(flagsByPlayer, player, flags);
    }

    xsIntListSort(players, false);

    for (i = 0; < numPlayers) {
        int player = xsIntListGet(players, i);
        int score = xsIntIntDictGet(scoreByPlayer, player, 0);
        int flags = xsIntIntDictGet(flagsByPlayer, player, 0);

        if (xsBitAnd(flags, cFlagElite) != 0) {
            xsChatData("Player " + player + " is elite with score " + score);
        } else {
            xsChatData("Player " + player + " score: " + score);
        }
    }
}
```

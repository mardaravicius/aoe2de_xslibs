# aoe2de_xslibs

A reusable XS library pack for Age of Empires II: Definitive Edition.
It adds growable lists, an `int -> int` dictionary, bitwise helpers, and a Mersenne Twister random number generator.

## Why these libraries?

XS gives you arrays, vectors, and primitive types, but larger scripts quickly run into a few missing building blocks:

- dynamic lists
- reusable dictionary-like storage
- bitwise operations
- a convenient pseudo-random number generator

This repo packages those missing pieces as drop-in `.xs` files.
If you only want to use the libraries in a scenario, the generated files in [`xs/`](xs/) are the ones you need.
The Python source used to generate them lives in [`src/xs/`](src/xs/).

## Example usage

The example below shows the libraries working together in a small script.

```cpp
void main() {
    int scores = xsIntList(120, 85, 200, 145);
    int budget = xsIntIntDict(1, 500, 3, 300);

    xsIntListAppend(scores, 310);
    xsIntIntDictPut(budget, 7, 700);

    int roll = xsMtRandomUniformRange(1, 100);

    int cFlagActive = xsBitShiftLeft(1, 1);
    int state = xsBitOr(0, cFlagActive);

    xsChatData("Top score: " + xsIntListMax(scores));
    xsChatData("Player 3 budget: " + xsIntIntDictGet(budget, 3, 0));
    xsChatData("Roll: " + roll);

    if (xsBitAnd(state, cFlagActive) != 0) {
        xsChatData("active!");
    }
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
| `binaryFunctions.xs` | Bitwise helpers and MT19937 random number functions |

## 2. Add them to your script

There are two straightforward ways to use the libraries.

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

## 3. A few rules to remember

- The list creation helpers and `xsIntIntDict` return an `int` handle.
- `xsIntIntDictKeys` and `xsIntIntDictValues` return raw XS `int` arrays, not list handles.
- There is no global initialization function for these libraries. You can use them immediately.
- `xsIntIntDict` cannot store `cIntIntDictEmptyKey` as a key at all.

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
It mostly mirrors Int List, but there is no `Sum`, and `xsStringListUseArrayAsSource` wraps an existing string array without copying it.

### Constants

| Constant | Value | Meaning |
|---|---|---|
| `cStringListSuccess` | `0` | Operation succeeded |
| `cStringListGenericError` | `-1` | General failure |
| `cStringListIndexOutOfRangeError` | `-2` | Index out of bounds |
| `cStringListResizeFailedError` | `-3` | Array allocation failed |
| `cStringListMaxCapacityError` | `-4` | Exceeded maximum capacity |
| `cStringListMaxCapacity` | `999999999` | Hard upper limit |

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
    int names = xsStringList("Alice", "Bob", "Carol");
    xsStringListSort(names, false);

    int i = 0;
    while (i < xsStringListSize(names)) {
        xsChatData("Player: " + xsStringListGet(names, i));
        i++;
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

    int i = 0;
    while (i < xsVectorListSize(waypoints)) {
        vector pos = xsVectorListGet(waypoints, i);
        xsChatData("Waypoint " + i + ": " + pos);
        i++;
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

## 10. Binary Operations

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

## 11. Random Numbers

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
    int i = 0;
    while (i < numPlayers) {
        int team = xsMtRandomUniformRange(0, 2);
        xsChatData("Player " + (i + 1) + " -> team " + team);
        i++;
    }
}
```

## 12. Larger example

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

    int i = 0;
    while (i < xsIntListSize(players)) {
        int player = xsIntListGet(players, i);
        int score = 100 + xsMtRandomUniformRange(0, 76);
        int flags = 0;

        if (score >= 150) {
            flags = xsBitOr(flags, cFlagElite);
        }

        xsIntIntDictPut(scoreByPlayer, player, score);
        xsIntIntDictPut(flagsByPlayer, player, flags);
        i++;
    }

    xsIntListSort(players, false);

    i = 0;
    while (i < xsIntListSize(players)) {
        int player = xsIntListGet(players, i);
        int score = xsIntIntDictGet(scoreByPlayer, player, 0);
        int flags = xsIntIntDictGet(flagsByPlayer, player, 0);

        if (xsBitAnd(flags, cFlagElite) != 0) {
            xsChatData("Player " + player + " is elite with score " + score);
        } else {
            xsChatData("Player " + player + " score: " + score);
        }

        i++;
    }
}
```

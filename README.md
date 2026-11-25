# aoe2de_xslibs

A reusable XS library pack for Age of Empires II: Definitive Edition.
It adds growable lists, `int`/`float`/`vector`/`string` dictionary variants, and a xoshiro128** random number generator.

## Why these libraries?

XS gives you arrays, vectors, and primitive types, but larger scripts quickly run into a few missing building blocks:

- dynamic array with an api inspired by python list
- hash tables with an api inspired by python dictionary
- a fast pseudo-random number generator (xoshiro128**)

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

    int roll = xsXoRandomUniformRange(1, 100);

    xsChatData("List: " + xsIntListToString(scores));
    xsChatData("Dict: " + xsIntIntDictToString(civUnits));
    xsChatData("Roll: " + roll);
}
```

### A note about handles

All lists and dictionaries are returned as an `int` handle.
You pass that handle to every follow-up function call for that object.

XS cannot free arrays, so the `Delete` functions only resize the collection's arrays to 0 to release their memory.
The handle must not be used afterwards, whether `Delete` succeeded or not, and calling `Delete` twice on the same handle is undefined behavior.

# Using aoe2de_xslibs

## 1. Pick the generated `.xs` files

If you only want to use the libraries in a scenario, use the files from [`xs/`](xs/).
You do not need the Python tooling for that.

| File | Provides |
|---|---|
| `intArray.xs` | Helper functions for plain XS `int` arrays |
| `floatArray.xs` | Helper functions for plain XS `float` arrays |
| `boolArray.xs` | Helper functions for plain XS `bool` arrays |
| `stringArray.xs` | Helper functions for plain XS `string` arrays |
| `vectorArray.xs` | Helper functions for plain XS `vector` arrays |
| `intList.xs` | Dynamic list of `int` values |
| `floatList.xs` | Dynamic list of `float` values |
| `boolList.xs` | Dynamic list of `bool` values |
| `stringList.xs` | Dynamic list of `string` values |
| `vectorList.xs` | Dynamic list of `vector` values |
| `intIntDict.xs` | Hash map from `int` keys to `int` values |
| `intStringDict.xs` | Hash map from `int` keys to `string` values |
| `intVectorDict.xs` | Hash map from `int` keys to `vector` values |
| `floatIntDict.xs` | Hash map from `float` keys to `int` values |
| `floatStringDict.xs` | Hash map from `float` keys to `string` values |
| `floatVectorDict.xs` | Hash map from `float` keys to `vector` values |
| `stringIntDict.xs` | Hash map from `string` keys to `int` values |
| `stringStringDict.xs` | Hash map from `string` keys to `string` values |
| `stringVectorDict.xs` | Hash map from `string` keys to `vector` values |
| `vectorIntDict.xs` | Hash map from `vector` keys to `int` values |
| `vectorStringDict.xs` | Hash map from `vector` keys to `string` values |
| `vectorVectorDict.xs` | Hash map from `vector` keys to `vector` values |
| `random.xs` | xoshiro128** random number functions |

## 2. Add them to your script

There are three straightforward ways to use the libraries.

### Option A - Using `include`

1. Place the `.xs` files you need in a folder AoE2 DE can load scripts from, for example:
   `C:\Users\<user>\Games\Age of Empires 2 DE\<steamId>\resources\_common\xs\`

2. Include the files at the top of your script:

   ```cpp
   include "intList.xs";
   include "intIntDict.xs";
   include "random.xs";
   ```

### Option B - Copy and paste the file contents

Copy the contents of the generated `.xs` files you want and paste them above your `void main()` function.

### Option C - Copy and paste them into a `Script Call` Effect

Copy the contents of the generated `.xs` files into a disabled `Script Call`. 
Make sure that effect starts with some function definition (eg: `void header123(){}`) otherwise it will show up as 
red but still work.

## 3. A few rules to remember

- The list creation helpers and all dictionary constructors return an `int` handle.
- The array creation helpers return a plain XS array id that works with the built-in `xsArray...` functions.
- The dictionary `Keys` and `Values` helpers return raw XS arrays, not list handles.
- Pass an existing array to dictionary `Keys` or `Values` to reuse it; the helper resizes and returns that same array.
- `NextKey` returns a sentinel value when iteration ends. If that sentinel could also be a real key, check `LastError()` to distinguish "no next key" from a legitimate return value.
- `xsIntIntDictKeys`/`Values` return `int[]` / `int[]`.
- `xsIntStringDictKeys`/`Values` return `int[]` / `string[]`.
- `xsIntVectorDictKeys`/`Values` return `int[]` / `vector[]`.
- `xsFloatIntDictKeys`/`Values` return `float[]` / `int[]`.
- `xsFloatStringDictKeys`/`Values` return `float[]` / `string[]`.
- `xsFloatVectorDictKeys`/`Values` return `float[]` / `vector[]`.
- `xsStringIntDictKeys`/`Values` return `string[]` / `int[]`.
- `xsStringStringDictKeys`/`Values` return `string[]` / `string[]`.
- `xsStringVectorDictKeys`/`Values` return `string[]` / `vector[]`.
- `xsVectorIntDictKeys`/`Values` return `vector[]` / `int[]`.
- `xsVectorStringDictKeys`/`Values` return `vector[]` / `string[]`.
- `xsVectorVectorDictKeys`/`Values` return `vector[]` / `vector[]`.
- `FromString` constructors parse a comma separated string and skip items that cannot be parsed:
  `xsIntListFromString("1,2")`, `xsFloatListFromString("1.0,1.1")`, `xsBoolListFromString("true,false")`,
  `xsStringListFromString("'a','b'")`, `xsVectorListFromString("v(1.0,1.1,-3.3),v(1.0,2.0,3.0)")`, the matching array
  constructors such as `xsIntArrayFromString("1,2")` or `xsVectorArrayFromString("v(1.0,1.1,-3.3)")`, and for dictionaries
  `key:value` pairs such as `xsIntStringDictFromString("1:'a',2:'b'")` or `xsStringStringDictFromString("'abc':''")`.
  Values are parsed with `strToInt` and `strToFloat`, so floats need a decimal point (`1.0`, not `1`)
  and ints keep only their leading digits (`1.5` becomes `1`). Items are trimmed. Strings must be wrapped in `'` and cannot contain `'`, but may contain `,`, `:` and brackets.
  An unclosed `'` makes the rest of the input part of that item. Numbers equal to the module's constructor
  sentinel (for example `cIntListEmptyParam`) are treated as invalid.
  Each call leaks a small amount of memory: XS arrays cannot be deleted, so the temporary arrays used for
  splitting are only resized to zero. Avoid calling `FromString` constructors in frequently running rules.
- `SortWith` functions (for example `xsIntArraySortWith(arr, other)` or `xsStringListSortWith(lst, other)`) sort
  stably: equal values keep their original order, in both ascending and descending order. `other` is never
  sorted on its own; its elements move the same way as the sorted ones, so `other[i]` stays paired with `arr[i]`.
  `other` must be an int array for the array variants and an int list for the list variants, with the same size.
  They return `...Success`, `...GenericError` when the sizes differ or the buffers can't be created, or
  `...ResizeFailedError` when the buffers can't grow. On error neither input is changed.
  Inputs larger than 16 elements use two internal buffer arrays per module. With `releaseBuffers` set to `true`
  (the default) they are resized to zero after sorting; the same arrays are grown again on the next call, so no new
  arrays are created. Pass `false` to keep them allocated when sorting large inputs often.
- There is no global initialization function for these libraries. You can use them immediately.
- `xsIntIntDict`, `xsIntStringDict`, and `xsIntVectorDict` cannot store their reserved `...EmptyKey` int sentinel as a key.
- `xsFloatIntDict`, `xsFloatStringDict`, and `xsFloatVectorDict` cannot store their reserved `...EmptyKey` float sentinel as a key.
- The float-key dictionaries canonicalize `-0.0` to `0.0` and treat all NaN keys as the same key.
- Vector-key dictionaries do not canonicalize components; avoid NaN and signed-zero components in keys.
- `xsStringIntDict` cannot store the reserved sentinel string `!<[empty` as a key.
- `xsStringStringDict` cannot store the reserved sentinel string `!<[empty` as a key.
- `xsStringVectorDict` cannot store the reserved sentinel string `!<[empty` as a key.
- `xsVectorIntDict`, `xsVectorStringDict`, and `xsVectorVectorDict` cannot store their reserved `...EmptyKey` vector sentinel as a key.

## 4. Int Array

`intArray.xs` provides helper functions for plain XS `int` arrays, the ones created with `xsArrayCreateInt`.
The functions take and return regular array ids, so they work alongside `xsArrayGetInt`, `xsArraySetInt`,
`xsArrayGetSize` and `xsArrayResizeInt`. These built-ins are not duplicated.
The helpers never change an array's size; use `intList.xs` when you need append, insert or remove.

### Constants

| Constant | Value | Meaning |
|---|---|---|
| `cIntArraySuccess` | `0` | Operation succeeded |
| `cIntArrayGenericError` | `-1` | General failure |
| `cIntArrayIndexOutOfRangeError` | `-2` | Min or max of an empty array |
| `cIntArrayResizeFailedError` | `-3` | Array allocation failed |
| `cIntArrayMaxCapacityError` | `-4` | Exceeded maximum capacity |
| `cIntArrayMaxCapacity` | `999999999` | Hard upper limit |
| `cIntArrayEmptyParam` | `-999999999` | Internal constructor sentinel |

### API

```cpp
// Creation
int xsIntArray(int v0, int v1, ..., int v11)      // up to 12 initial values
int xsIntArrayFromString(string items)
int xsIntArrayFromRange(int start, int stop, int step)
int xsIntArrayFromRepeatedVal(int value, int times)
int xsIntArrayFromRepeatedArray(int arr, int times)

// Modification
int    xsIntArrayDelete(int arr)
void   xsIntArrayReverse(int arr)
void   xsIntArraySort(int arr, bool reverse)
int    xsIntArraySortWith(int arr, int other, bool reverse, bool releaseBuffers)  // stable; other is an int array kept paired

// Search
bool   xsIntArrayContains(int arr, int value)
int    xsIntArrayIndex(int arr, int value, int start, int stop)
int    xsIntArrayCount(int arr, int value)

// Aggregation
int    xsIntArraySum(int arr)
int    xsIntArrayMin(int arr)
int    xsIntArrayMax(int arr)

// Bulk operations
int    xsIntArrayCopy(int arr, int start, int end)
int    xsIntArrayCompare(int arr1, int arr2)

// Diagnostics
string xsIntArrayToString(int arr, string start, string sep, string end)
int    xsIntArrayLastError()                      // status of the last Min or Max call
```

### Example

```cpp
void rankUnits() {
    int units = xsIntArray(cMilitiaLine, cArcherLine, cKnightLine);
    int costs = xsIntArray(60, 45, 135);

    xsIntArraySortWith(costs, units, true);
    xsChatData("Most expensive: unit " + xsArrayGetInt(units, 0) + " for " + xsArrayGetInt(costs, 0));
    xsChatData("Has archers: " + xsIntArrayContains(units, cArcherLine));
}
```

## 5. Float Array

`floatArray.xs` provides helper functions for plain XS `float` arrays, the ones created with `xsArrayCreateFloat`.
The functions take and return regular array ids, so they work alongside `xsArrayGetFloat`, `xsArraySetFloat`,
`xsArrayGetSize` and `xsArrayResizeFloat`. These built-ins are not duplicated.
The helpers never change an array's size; use `floatList.xs` when you need append, insert or remove.

### Constants

| Constant | Value | Meaning |
|---|---|---|
| `cFloatArraySuccess` | `0` | Operation succeeded |
| `cFloatArrayGenericError` | `-1` | General failure |
| `cFloatArrayGenericErrorFloat` | `-1.0` | Float return value on error |
| `cFloatArrayIndexOutOfRangeError` | `-2` | Min or max of an empty array |
| `cFloatArrayResizeFailedError` | `-3` | Array allocation failed |
| `cFloatArrayMaxCapacityError` | `-4` | Exceeded maximum capacity |
| `cFloatArrayMaxCapacity` | `999999999` | Hard upper limit |
| `cFloatArrayEmptyParam` | `-9999999.0` | Internal constructor sentinel |
| `cFloatArrayEmptyIntParam` | `-999999999` | Internal index sentinel |

### API

```cpp
// Creation
int   xsFloatArray(float v0, float v1, ..., float v11)  // up to 12 initial values
int   xsFloatArrayFromString(string items)
int   xsFloatArrayFromRepeatedVal(float value, int times)
int   xsFloatArrayFromRepeatedArray(int arr, int times)

// Modification
int   xsFloatArrayDelete(int arr)
void  xsFloatArrayReverse(int arr)
void  xsFloatArraySort(int arr, bool reverse)
int   xsFloatArraySortWith(int arr, int other, bool reverse, bool releaseBuffers)  // stable; other is an int array kept paired

// Search
bool  xsFloatArrayContains(int arr, float value)
int   xsFloatArrayIndex(int arr, float value, int start, int stop)
int   xsFloatArrayCount(int arr, float value)

// Aggregation
float xsFloatArraySum(int arr)
float xsFloatArrayMin(int arr)
float xsFloatArrayMax(int arr)

// Bulk operations
int   xsFloatArrayCopy(int arr, int start, int end)
int   xsFloatArrayCompare(int arr1, int arr2)

// Diagnostics
string xsFloatArrayToString(int arr, string start, string sep, string end)
int    xsFloatArrayLastError()                         // status of the last Min or Max call
```

### Example

```cpp
void averageSpeed() {
    int speeds = xsFloatArray(0.96, 1.35, 1.1);

    float avg = xsFloatArraySum(speeds) / xsArrayGetSize(speeds);
    xsChatData("Average: " + avg + ", fastest: " + xsFloatArrayMax(speeds));
}
```

## 6. Bool Array

`boolArray.xs` provides helper functions for plain XS `bool` arrays, the ones created with `xsArrayCreateBool`.
The functions take and return regular array ids, so they work alongside `xsArrayGetBool`, `xsArraySetBool`,
`xsArrayGetSize` and `xsArrayResizeBool`. These built-ins are not duplicated.
The helpers never change an array's size; use `boolList.xs` when you need append, insert or remove.

Like `boolList.xs`, there is no constructor with initial values; use `xsBoolArrayFromString` or `xsBoolArrayFromRepeatedVal`.

### Constants

| Constant | Value | Meaning |
|---|---|---|
| `cBoolArraySuccess` | `0` | Operation succeeded |
| `cBoolArrayGenericError` | `-1` | General failure |
| `cBoolArrayResizeFailedError` | `-3` | Array allocation failed |
| `cBoolArrayMaxCapacityError` | `-4` | Exceeded maximum capacity |
| `cBoolArrayMaxCapacity` | `999999999` | Hard upper limit |
| `cBoolArrayEmptyIntParam` | `-999999999` | Internal index sentinel |

### API

```cpp
// Creation
int    xsBoolArrayFromString(string items)
int    xsBoolArrayFromRepeatedVal(bool value, int times)
int    xsBoolArrayFromRepeatedArray(int arr, int times)

// Modification
int    xsBoolArrayDelete(int arr)
void   xsBoolArrayReverse(int arr)
void   xsBoolArraySort(int arr, bool reverse)          // false before true
int    xsBoolArraySortWith(int arr, int other, bool reverse, bool releaseBuffers)  // stable; other is an int array kept paired

// Search
bool   xsBoolArrayContains(int arr, bool value)
int    xsBoolArrayIndex(int arr, bool value, int start, int stop)
int    xsBoolArrayCount(int arr, bool value)

// Bulk operations
int    xsBoolArrayCopy(int arr, int start, int end)
int    xsBoolArrayCompare(int arr1, int arr2)

// Diagnostics
string xsBoolArrayToString(int arr, string start, string sep, string end, string strTrue, string strFalse)
```

### Example

```cpp
void checkPlayers() {
    int alive = xsBoolArrayFromRepeatedVal(true, 8);
    xsArraySetBool(alive, 3, false);

    xsChatData("Alive: " + xsBoolArrayCount(alive, true));
}
```

## 7. String Array

`stringArray.xs` provides helper functions for plain XS `string` arrays, the ones created with `xsArrayCreateString`.
The functions take and return regular array ids, so they work alongside `xsArrayGetString`, `xsArraySetString`,
`xsArrayGetSize` and `xsArrayResizeString`. These built-ins are not duplicated.
The helpers never change an array's size; use `stringList.xs` when you need append, insert or remove.

`xsStringArray` cannot take the reserved sentinel string `!<[empty` as a value.

### Constants

| Constant | Value | Meaning |
|---|---|---|
| `cStringArraySuccess` | `0` | Operation succeeded |
| `cStringArrayGenericError` | `-1` | General failure |
| `cStringArrayIndexOutOfRangeError` | `-2` | Min or max of an empty array |
| `cStringArrayResizeFailedError` | `-3` | Array allocation failed |
| `cStringArrayMaxCapacityError` | `-4` | Exceeded maximum capacity |
| `cStringArrayMaxCapacity` | `999999999` | Hard upper limit |
| `cStringArrayEmptyIntParam` | `-999999999` | Internal index sentinel |

### API

```cpp
// Creation
int    xsStringArray(string v0, string v1, ..., string v11)  // up to 12 initial values
int    xsStringArrayFromString(string items)
int    xsStringArrayFromRepeatedVal(string value, int times)
int    xsStringArrayFromRepeatedArray(int arr, int times)

// Modification
int    xsStringArrayDelete(int arr)
void   xsStringArrayReverse(int arr)
void   xsStringArraySort(int arr, bool reverse)
int    xsStringArraySortWith(int arr, int other, bool reverse, bool releaseBuffers)  // stable; other is an int array kept paired

// Search
bool   xsStringArrayContains(int arr, string value)
int    xsStringArrayIndex(int arr, string value, int start, int stop)
int    xsStringArrayCount(int arr, string value)

// Aggregation
string xsStringArrayMin(int arr)                     // returns "-1" on error
string xsStringArrayMax(int arr)                     // returns "-1" on error

// Bulk operations
int    xsStringArrayCopy(int arr, int start, int end)
int    xsStringArrayCompare(int arr1, int arr2)

// Diagnostics
string xsStringArrayToString(int arr, string start, string sep, string end, string quote)
int    xsStringArrayLastError()                      // status of the last Min or Max call
```

### Example

```cpp
void listNames() {
    int names = xsStringArray("Tamerlane", "Joan", "Saladin");

    xsStringArraySort(names, false);
    xsChatData(xsStringArrayToString(names));
}
```

## 8. Vector Array

`vectorArray.xs` provides helper functions for plain XS `vector` arrays, the ones created with `xsArrayCreateVector`.
The functions take and return regular array ids, so they work alongside `xsArrayGetVector`, `xsArraySetVector`,
`xsArrayGetSize`. These built-ins are not duplicated.
The helpers never change an array's size; use `vectorList.xs` when you need append, insert or remove.

There is no `Delete` function because `xsArrayResizeVector` is bugged in the game.
Like `vectorList.xs`, there is no sort, compare, sum, min or max.

### Constants

| Constant | Value | Meaning |
|---|---|---|
| `cVectorArrayGenericError` | `-1` | General failure |
| `cVectorArrayMaxCapacityError` | `-4` | Exceeded maximum capacity |
| `cVectorArrayMaxCapacity` | `999999999` | Hard upper limit |
| `cVectorArrayEmptyParam` | `vector(-9999999.0, -9999999.0, -9999999.0)` | Internal constructor sentinel |
| `cVectorArrayEmptyIntParam` | `-999999999` | Internal index sentinel |

### API

```cpp
// Creation
int    xsVectorArray(vector v0, vector v1, ..., vector v11)  // up to 12 initial values
int    xsVectorArrayFromString(string items)
int    xsVectorArrayFromRepeatedVal(vector value, int times)
int    xsVectorArrayFromRepeatedArray(int arr, int times)

// Modification
void   xsVectorArrayReverse(int arr)

// Search
bool   xsVectorArrayContains(int arr, vector value)
int    xsVectorArrayIndex(int arr, vector value, int start, int stop)
int    xsVectorArrayCount(int arr, vector value)

// Bulk operations
int    xsVectorArrayCopy(int arr, int start, int end)

// Diagnostics
string xsVectorArrayToString(int arr, string start, string sep, string end)
```

### Example

```cpp
void spawnPoints() {
    int points = xsVectorArray(vector(10.0, 10.0, 0.0), vector(50.0, 10.0, 0.0), vector(10.0, 50.0, 0.0));

    xsChatData("Has center: " + xsVectorArrayContains(points, vector(30.0, 30.0, 0.0)));
}
```

## 9. Int List

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
int xsIntListFromString(string items)
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
int    xsIntListDelete(int lst)
void   xsIntListReverse(int lst)
void   xsIntListSort(int lst, bool reverse)
int    xsIntListSortWith(int lst, int other, bool reverse, bool releaseBuffers)  // stable; other is an int list kept paired

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
string xsIntListToString(int lst, string start, string sep, string end)
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

## 10. Float List

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
int   xsFloatListFromString(string items)
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
int   xsFloatListDelete(int lst)
void  xsFloatListReverse(int lst)
void  xsFloatListSort(int lst, bool reverse)
int   xsFloatListSortWith(int lst, int other, bool reverse, bool releaseBuffers)  // stable; other is an int list kept paired

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
string xsFloatListToString(int lst, string start, string sep, string end)
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

## 11. Bool List

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
int  xsBoolListFromString(string items)
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
int  xsBoolListDelete(int lst)
void xsBoolListReverse(int lst)
void xsBoolListSort(int lst, bool reverse)
int  xsBoolListSortWith(int lst, int other, bool reverse, bool releaseBuffers)  // stable; other is an int list kept paired

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
string xsBoolListToString(int lst, string start, string sep, string end, string strTrue, string strFalse)
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

## 12. String List

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
int    xsStringListFromString(string items)
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
int    xsStringListDelete(int lst)
void   xsStringListReverse(int lst)
void   xsStringListSort(int lst, bool reverse)
int    xsStringListSortWith(int lst, int other, bool reverse, bool releaseBuffers)  // stable; other is an int list kept paired

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
string xsStringListToString(int lst, string start, string sep, string end, string quote)
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

## 13. Vector List

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
int    xsVectorListFromString(string items)
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
int    xsVectorListDelete(int lst)
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
string xsVectorListToString(int lst, string start, string sep, string end)
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

## 14. Int to Int Dictionary

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
int  xsIntIntDictFromString(string items)
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
int  xsIntIntDictDelete(int dct)

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
string xsIntIntDictToString(int dct, string start, string sep, string end, string kvSep)
int    xsIntIntDictLastError()
```

### Return-value technicalities

`xsIntIntDictPut`, `xsIntIntDictPutIfAbsent`, and `xsIntIntDictRemove` need a quick extra check after the call because their return value alone is not enough.

- `cIntIntDictSuccess`: the key already existed, and the returned value is meaningful
- `cIntIntDictNoKeyError`: either the key was missing, or `Put`/`PutIfAbsent` inserted a new key
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

## 15. Int to String Dictionary

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
int    xsIntStringDictFromString(string items)
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
int    xsIntStringDictDelete(int dct)

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
string xsIntStringDictToString(int dct, string start, string sep, string end, string kvSep, string quote)
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

## 16. Int to Vector Dictionary

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
int    xsIntVectorDictFromString(string items)
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
int    xsIntVectorDictDelete(int dct)

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
string xsIntVectorDictToString(int dct, string start, string sep, string end, string kvSep)
int    xsIntVectorDictLastError()
```

### Return-value technicalities

`xsIntVectorDictPut`, `xsIntVectorDictPutIfAbsent`, and `xsIntVectorDictRemove` can all return `cIntVectorDictGenericErrorVector` in more than one situation.

- `cIntVectorDictSuccess`: the operation succeeded, and the returned vector is meaningful
- `cIntVectorDictNoKeyError`: either the key was missing, or `Put`/`PutIfAbsent` inserted a new key
- any other negative status: the call failed

This matters because `vector(-1.0, -1.0, -1.0)` is also a valid stored vector value.

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

## 17. Float to Int Dictionary

`floatIntDict.xs` provides a hash map from `float` keys to `int` values.
The exported implementation uses open addressing with linear probing and resizes automatically when the load factor grows past `cFloatIntDictMaxLoadFactor`. Signed zero keys are canonicalized to `0.0`, and all NaN keys are treated as the same key.

### Constants

| Constant | Value | Meaning |
|---|---|---|
| `cFloatIntDictSuccess` | `0` | Operation succeeded |
| `cFloatIntDictGenericError` | `-1` | General failure |
| `cFloatIntDictGenericErrorFloat` | `-1.0` | Error return for float-key iteration operations |
| `cFloatIntDictNoKeyError` | `-2` | Key not found, or new key inserted for `Put`/`PutIfAbsent` |
| `cFloatIntDictResizeFailedError` | `-3` | Resize allocation failed |
| `cFloatIntDictMaxCapacityError` | `-4` | Exceeded maximum capacity |
| `cFloatIntDictMaxCapacity` | `999999999` | Hard upper limit |
| `cFloatIntDictMaxLoadFactor` | `0.75` | Resize trigger threshold |
| `cFloatIntDictEmptyKey` | `-9999999.0` | Reserved empty-slot sentinel; cannot be used as a key |

### API

```cpp
// Creation
int   xsFloatIntDictCreate()
int   xsFloatIntDictFromString(string items)
int   xsFloatIntDict(float k1, int v1, ..., float k6, int v6)

// Access
int   xsFloatIntDictGet(int dct, float key, int dft)
bool  xsFloatIntDictContains(int dct, float key)
int   xsFloatIntDictSize(int dct)

// Modification
int   xsFloatIntDictPut(int dct, float key, int val)
int   xsFloatIntDictPutIfAbsent(int dct, float key, int val)
int   xsFloatIntDictRemove(int dct, float key)
int   xsFloatIntDictClear(int dct)
int   xsFloatIntDictDelete(int dct)

// Bulk operations
int   xsFloatIntDictUpdate(int source, int dct)
int   xsFloatIntDictCopy(int dct)
int   xsFloatIntDictKeys(int dct)               // returns a raw XS float array
int   xsFloatIntDictValues(int dct)             // returns a raw XS int array
bool  xsFloatIntDictEquals(int a, int b)

// Iteration
bool  xsFloatIntDictHasNext(int dct, bool isFirst, float prevKey)
float xsFloatIntDictNextKey(int dct, bool isFirst, float prevKey)

// Diagnostics
string xsFloatIntDictToString(int dct, string start, string sep, string end, string kvSep)
int    xsFloatIntDictLastError()
```

### Return-value technicalities

`xsFloatIntDictPut`, `xsFloatIntDictPutIfAbsent`, and `xsFloatIntDictRemove` need a quick extra check after the call because their return value alone is not enough.

- `cFloatIntDictSuccess`: the key already existed, and the returned value is meaningful
- `cFloatIntDictNoKeyError`: either the key was missing, or `Put`/`PutIfAbsent` inserted a new key
- any other negative status: the call failed

This is necessary because `cFloatIntDictGenericError` (`-1`) can be both a legitimate stored value and the generic error sentinel.

### Example

```cpp
void scoreZones() {
    int danger = xsFloatIntDict(
        1.5, 3,
        2.5, 7,
        3.5, 2
    );

    int level = xsFloatIntDictGet(danger, 2.5, 0);
    xsChatData("Danger level: " + level);
}
```

## 18. Float to String Dictionary

`floatStringDict.xs` provides a hash map from `float` keys to `string` values.
It uses the same open-addressed layout as `floatIntDict.xs`, but stores values in a parallel string array. Signed zero keys are canonicalized to `0.0`, and all NaN keys are treated as the same key.

### Constants

| Constant | Value | Meaning |
|---|---|---|
| `cFloatStringDictSuccess` | `0` | Operation succeeded |
| `cFloatStringDictGenericError` | `-1` | General failure |
| `cFloatStringDictGenericErrorFloat` | `-1.0` | Error return for float-key iteration operations |
| `cFloatStringDictNoKeyError` | `-2` | Key not found, or new key inserted for `Put`/`PutIfAbsent` |
| `cFloatStringDictResizeFailedError` | `-3` | Resize allocation failed |
| `cFloatStringDictMaxCapacityError` | `-4` | Exceeded maximum capacity |
| `cFloatStringDictMaxCapacity` | `999999999` | Hard upper limit |
| `cFloatStringDictMaxLoadFactor` | `0.75` | Resize trigger threshold |
| `cFloatStringDictEmptyKey` | `-9999999.0` | Reserved empty-slot sentinel; cannot be used as a key |

### API

```cpp
// Creation
int    xsFloatStringDictCreate()
int    xsFloatStringDictFromString(string items)
int    xsFloatStringDict(float k1, string v1, ..., float k6, string v6)

// Access
string xsFloatStringDictGet(int dct, float key, string dft)
bool   xsFloatStringDictContains(int dct, float key)
int    xsFloatStringDictSize(int dct)

// Modification
string xsFloatStringDictPut(int dct, float key, string val)
string xsFloatStringDictPutIfAbsent(int dct, float key, string val)
string xsFloatStringDictRemove(int dct, float key)
int    xsFloatStringDictClear(int dct)
int    xsFloatStringDictDelete(int dct)

// Bulk operations
int    xsFloatStringDictUpdate(int source, int dct)
int    xsFloatStringDictCopy(int dct)
int    xsFloatStringDictKeys(int dct)            // returns a raw XS float array
int    xsFloatStringDictValues(int dct)          // returns a raw XS string array
bool   xsFloatStringDictEquals(int a, int b)

// Iteration
bool   xsFloatStringDictHasNext(int dct, bool isFirst, float prevKey)
float  xsFloatStringDictNextKey(int dct, bool isFirst, float prevKey)

// Diagnostics
string xsFloatStringDictToString(int dct, string start, string sep, string end, string kvSep, string quote)
int    xsFloatStringDictLastError()
```

### Return-value technicalities

`xsFloatStringDictPut`, `xsFloatStringDictPutIfAbsent`, and `xsFloatStringDictRemove` can all return `"-1"` in more than one situation.

- `cFloatStringDictSuccess`: the operation succeeded, and the returned string is meaningful
- `cFloatStringDictNoKeyError`: either the key was missing, or `Put`/`PutIfAbsent` inserted a new key
- any other negative status: the call failed

This matters because `"-1"` is also a valid stored string value.

### Example

```cpp
void labelZones() {
    int labels = xsFloatStringDict(
        1.5, "north camp",
        2.5, "south camp"
    );

    string label = xsFloatStringDictGet(labels, 1.5, "unknown");
    xsChatData("Zone label: " + label);
}
```

## 19. Float to Vector Dictionary

`floatVectorDict.xs` provides a hash map from `float` keys to `vector` values.
It uses the same open-addressed layout as `floatIntDict.xs`, but stores vectors as raw float components. Signed zero keys are canonicalized to `0.0`, and all NaN keys are treated as the same key.

### Constants

| Constant | Value | Meaning |
|---|---|---|
| `cFloatVectorDictSuccess` | `0` | Operation succeeded |
| `cFloatVectorDictGenericError` | `-1` | General failure |
| `cFloatVectorDictNoKeyError` | `-2` | Key not found, or new key inserted for `Put`/`PutIfAbsent` |
| `cFloatVectorDictResizeFailedError` | `-3` | Resize allocation failed |
| `cFloatVectorDictMaxCapacityError` | `-4` | Exceeded maximum capacity |
| `cFloatVectorDictGenericErrorVector` | `vector(-1.0, -1.0, -1.0)` | Error return for vector-valued operations |
| `cFloatVectorDictMaxCapacity` | `999999997` | Hard upper limit |
| `cFloatVectorDictMaxLoadFactor` | `0.75` | Resize trigger threshold |
| `cFloatVectorDictEmptyKey` | `-9999999.0` | Reserved empty-slot sentinel; cannot be used as a key |

### API

```cpp
// Creation
int    xsFloatVectorDictCreate()
int    xsFloatVectorDictFromString(string items)
int    xsFloatVectorDict(float k1, vector v1, ..., float k6, vector v6)

// Access
vector xsFloatVectorDictGet(int dct, float key, vector dft)
bool   xsFloatVectorDictContains(int dct, float key)
int    xsFloatVectorDictSize(int dct)

// Modification
vector xsFloatVectorDictPut(int dct, float key, vector val)
vector xsFloatVectorDictPutIfAbsent(int dct, float key, vector val)
vector xsFloatVectorDictRemove(int dct, float key)
int    xsFloatVectorDictClear(int dct)
int    xsFloatVectorDictDelete(int dct)

// Bulk operations
int    xsFloatVectorDictUpdate(int source, int dct)
int    xsFloatVectorDictCopy(int dct)
int    xsFloatVectorDictKeys(int dct)            // returns a raw XS float array
int    xsFloatVectorDictValues(int dct)          // returns a raw XS vector array
bool   xsFloatVectorDictEquals(int a, int b)

// Iteration
bool   xsFloatVectorDictHasNext(int dct, bool isFirst, float prevKey)
float  xsFloatVectorDictNextKey(int dct, bool isFirst, float prevKey)

// Diagnostics
string xsFloatVectorDictToString(int dct, string start, string sep, string end, string kvSep)
int    xsFloatVectorDictLastError()
```

### Return-value technicalities

`xsFloatVectorDictPut`, `xsFloatVectorDictPutIfAbsent`, and `xsFloatVectorDictRemove` can all return `cFloatVectorDictGenericErrorVector` in more than one situation.

- `cFloatVectorDictSuccess`: the operation succeeded, and the returned vector is meaningful
- `cFloatVectorDictNoKeyError`: either the key was missing, or `Put`/`PutIfAbsent` inserted a new key
- any other negative status: the call failed

This matters because `vector(-1.0, -1.0, -1.0)` is also a valid stored vector value.

### Example

```cpp
void placeCamps() {
    int camps = xsFloatVectorDict(
        1.5, vector(12.0, 0.0, 18.0),
        2.5, vector(40.0, 0.0, 26.0)
    );

    vector camp = xsFloatVectorDictGet(camps, 2.5, vector(-1.0, -1.0, -1.0));
    xsChatData("Camp: " + camp);
}
```

## 20. String to Int Dictionary

`stringIntDict.xs` provides a hash map from `string` keys to `int` values.
The exported implementation uses open addressing with linear probing and resizes automatically when the load factor grows past `cStringIntDictMaxLoadFactor`. Iteration order is arbitrary.

### Constants

| Constant | Value | Meaning |
|---|---|---|
| `cStringIntDictSuccess` | `0` | Operation succeeded |
| `cStringIntDictGenericError` | `-1` | General failure |
| `cStringIntDictNoKeyError` | `-2` | Key not found, or new key inserted for `Put`/`PutIfAbsent` |
| `cStringIntDictResizeFailedError` | `-3` | Resize allocation failed |
| `cStringIntDictMaxCapacityError` | `-4` | Exceeded maximum capacity |
| `cStringIntDictMaxCapacity` | `249999998` | Hard upper limit |
| `cStringIntDictMaxLoadFactor` | `0.75` | Resize trigger threshold |

The reserved key string `!<[empty` is used internally and cannot be stored.

### API

```cpp
// Creation
int    xsStringIntDictCreate()
int    xsStringIntDictFromString(string items)
int    xsStringIntDict(string k1, int v1, ..., string k6, int v6)

// Access
int    xsStringIntDictGet(int dct, string key, int dft)
bool   xsStringIntDictContains(int dct, string key)
int    xsStringIntDictSize(int dct)

// Modification
int    xsStringIntDictPut(int dct, string key, int val)
int    xsStringIntDictPutIfAbsent(int dct, string key, int val)
int    xsStringIntDictRemove(int dct, string key)
int    xsStringIntDictClear(int dct)
int    xsStringIntDictDelete(int dct)

// Bulk operations
int    xsStringIntDictUpdate(int source, int dct)
int    xsStringIntDictCopy(int dct)
int    xsStringIntDictKeys(int dct)              // returns a raw XS string array
int    xsStringIntDictValues(int dct)            // returns a raw XS int array matching `Keys`
bool   xsStringIntDictEquals(int a, int b)

// Iteration
bool   xsStringIntDictHasNext(int dct, bool isFirst, string prevKey)
string xsStringIntDictNextKey(int dct, bool isFirst, string prevKey)

// Diagnostics
string xsStringIntDictToString(int dct, string start, string sep, string end, string kvSep, string quote)
int    xsStringIntDictLastError()
```

### Return-value technicalities

`xsStringIntDictPut`, `xsStringIntDictPutIfAbsent`, and `xsStringIntDictRemove` can all return `cStringIntDictGenericError` in more than one situation.

- `cStringIntDictSuccess`: the operation succeeded, and the returned int is meaningful
- `cStringIntDictNoKeyError`: either the key was missing, or `Put`/`PutIfAbsent` inserted a new key
- any other negative status: the call failed

This matters because `-1` is also a valid stored int value.

### Example

```cpp
void trackScoresByName() {
    int scoreByName = xsStringIntDict(
        "Alice", 1200,
        "Bob", 950,
        "Carol", 1310
    );

    int bobScore = xsStringIntDictGet(scoreByName, "Bob", 0);
    xsStringIntDictPut(scoreByName, "Bob", bobScore + 100);

    xsChatData(xsStringIntDictToString(scoreByName));
}
```

## 21. String to String Dictionary

`stringStringDict.xs` provides a hash map from `string` keys to `string` values.
The exported implementation uses open addressing with linear probing and resizes automatically when the load factor grows past `cStringStringDictMaxLoadFactor`. Iteration order is arbitrary.

### Constants

| Constant | Value | Meaning |
|---|---|---|
| `cStringStringDictSuccess` | `0` | Operation succeeded |
| `cStringStringDictGenericError` | `-1` | General failure |
| `cStringStringDictNoKeyError` | `-2` | Key not found, or new key inserted for `Put`/`PutIfAbsent` |
| `cStringStringDictResizeFailedError` | `-3` | Resize allocation failed |
| `cStringStringDictMaxCapacityError` | `-4` | Exceeded maximum capacity |
| `cStringStringDictMaxCapacity` | `333333331` | Hard upper limit |
| `cStringStringDictMaxLoadFactor` | `0.75` | Resize trigger threshold |

The reserved key string `!<[empty` is used internally and cannot be stored.

### API

```cpp
// Creation
int    xsStringStringDictCreate()
int    xsStringStringDictFromString(string items)
int    xsStringStringDict(string k1, string v1, ..., string k6, string v6)

// Access
string xsStringStringDictGet(int dct, string key, string dft)
bool   xsStringStringDictContains(int dct, string key)
int    xsStringStringDictSize(int dct)

// Modification
string xsStringStringDictPut(int dct, string key, string val)
string xsStringStringDictPutIfAbsent(int dct, string key, string val)
string xsStringStringDictRemove(int dct, string key)
int    xsStringStringDictClear(int dct)
int    xsStringStringDictDelete(int dct)

// Bulk operations
int    xsStringStringDictUpdate(int source, int dct)
int    xsStringStringDictCopy(int dct)
int    xsStringStringDictKeys(int dct)           // returns a raw XS string array
int    xsStringStringDictValues(int dct)         // returns a raw XS string array matching `Keys`
bool   xsStringStringDictEquals(int a, int b)

// Iteration
bool   xsStringStringDictHasNext(int dct, bool isFirst, string prevKey)
string xsStringStringDictNextKey(int dct, bool isFirst, string prevKey)

// Diagnostics
string xsStringStringDictToString(int dct, string start, string sep, string end, string kvSep, string quote)
int    xsStringStringDictLastError()
```

### Return-value technicalities

`xsStringStringDictPut`, `xsStringStringDictPutIfAbsent`, and `xsStringStringDictRemove` can all return `"-1"` in more than one situation.

- `cStringStringDictSuccess`: the operation succeeded, and the returned string is meaningful
- `cStringStringDictNoKeyError`: either the key was missing, or `Put`/`PutIfAbsent` inserted a new key
- any other negative status: the call failed

This matters because `"-1"` is also a valid stored string value.

### Example

```cpp
void mapAliases() {
    int aliases = xsStringStringDict(
        "Britons", "Archer civ",
        "Teutons", "Infantry civ"
    );

    string label = xsStringStringDictGet(aliases, "Britons", "Unknown");
    xsChatData("Britons: " + label);
}
```

## 22. String to Vector Dictionary

`stringVectorDict.xs` provides a hash map from `string` keys to `vector` values.
The exported implementation uses open addressing with linear probing and resizes automatically when the load factor grows past `cStringVectorDictMaxLoadFactor`. Iteration order is arbitrary.

### Constants

| Constant | Value | Meaning |
|---|---|---|
| `cStringVectorDictSuccess` | `0` | Operation succeeded |
| `cStringVectorDictGenericError` | `-1` | General failure |
| `cStringVectorDictNoKeyError` | `-2` | Key not found, or new key inserted for `Put`/`PutIfAbsent` |
| `cStringVectorDictResizeFailedError` | `-3` | Resize allocation failed |
| `cStringVectorDictMaxCapacityError` | `-4` | Exceeded maximum capacity |
| `cStringVectorDictGenericErrorVector` | `vector(-1.0, -1.0, -1.0)` | Error return for vector-valued operations |
| `cStringVectorDictMaxCapacity` | `333333330` | Hard upper limit |
| `cStringVectorDictMaxLoadFactor` | `0.75` | Resize trigger threshold |

The reserved key string `!<[empty` is used internally and cannot be stored.

### API

```cpp
// Creation
int    xsStringVectorDictCreate()
int    xsStringVectorDictFromString(string items)
int    xsStringVectorDict(string k1, vector v1, ..., string k6, vector v6)

// Access
vector xsStringVectorDictGet(int dct, string key, vector dft)
bool   xsStringVectorDictContains(int dct, string key)
int    xsStringVectorDictSize(int dct)

// Modification
vector xsStringVectorDictPut(int dct, string key, vector val)
vector xsStringVectorDictPutIfAbsent(int dct, string key, vector val)
vector xsStringVectorDictRemove(int dct, string key)
int    xsStringVectorDictClear(int dct)
int    xsStringVectorDictDelete(int dct)

// Bulk operations
int    xsStringVectorDictUpdate(int source, int dct)
int    xsStringVectorDictCopy(int dct)
int    xsStringVectorDictKeys(int dct)           // returns a raw XS string array
int    xsStringVectorDictValues(int dct)         // returns a raw XS vector array matching `Keys`
bool   xsStringVectorDictEquals(int a, int b)

// Iteration
bool   xsStringVectorDictHasNext(int dct, bool isFirst, string prevKey)
string xsStringVectorDictNextKey(int dct, bool isFirst, string prevKey)

// Diagnostics
string xsStringVectorDictToString(int dct, string start, string sep, string end, string kvSep, string quote)
int    xsStringVectorDictLastError()
```

### Return-value technicalities

`xsStringVectorDictPut`, `xsStringVectorDictPutIfAbsent`, and `xsStringVectorDictRemove` can all return `cStringVectorDictGenericErrorVector` in more than one situation.

- `cStringVectorDictSuccess`: the operation succeeded, and the returned vector is meaningful
- `cStringVectorDictNoKeyError`: either the key was missing, or `Put`/`PutIfAbsent` inserted a new key
- any other negative status: the call failed

This matters because `vector(-1.0, -1.0, -1.0)` is also a valid stored vector value.

### Example

```cpp
void placeNamedTargets() {
    int targets = xsStringVectorDict(
        "north", vector(10.0, 0.0, 30.0),
        "south", vector(10.0, 0.0, 60.0)
    );

    vector north = xsStringVectorDictGet(targets, "north", vector(-1.0, -1.0, -1.0));
    xsChatData("North target: " + north);
}
```

## 23. Vector to Int Dictionary

`vectorIntDict.xs` provides a hash map from `vector` keys to `int` values.
It uses direct vector equality for key lookup and reserves `cVectorIntDictEmptyKey` as the empty-slot sentinel. Vector keys are not canonicalized; avoid NaN and signed-zero components.

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
int    xsVectorIntDictFromString(string items)
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
int    xsVectorIntDictDelete(int dct)

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
string xsVectorIntDictToString(int dct, string start, string sep, string end, string kvSep)
int    xsVectorIntDictLastError()
```

### Return-value technicalities

`xsVectorIntDictPut`, `xsVectorIntDictPutIfAbsent`, and `xsVectorIntDictRemove` can all return `cVectorIntDictGenericError` in more than one situation.

- `cVectorIntDictSuccess`: the operation succeeded, and the returned int is meaningful
- `cVectorIntDictNoKeyError`: either the key was missing, or `Put`/`PutIfAbsent` inserted a new key
- any other negative status: the call failed

This matters because `-1` is also a valid stored int value.

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

## 24. Vector to String Dictionary

`vectorStringDict.xs` provides a hash map from `vector` keys to `string` values.
It mirrors the other vector-keyed dictionary variants, but stores values in a parallel string array. Vector keys are not canonicalized; avoid NaN and signed-zero components.

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
int    xsVectorStringDictFromString(string items)
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
int    xsVectorStringDictDelete(int dct)

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
string xsVectorStringDictToString(int dct, string start, string sep, string end, string kvSep, string quote)
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

## 25. Vector to Vector Dictionary

`vectorVectorDict.xs` provides a hash map from `vector` keys to `vector` values.
It mirrors the other dictionary variants, but both keys and values are vectors. Vector keys are not canonicalized; avoid NaN and signed-zero components.

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
int    xsVectorVectorDictFromString(string items)
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
int    xsVectorVectorDictDelete(int dct)

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
string xsVectorVectorDictToString(int dct, string start, string sep, string end, string kvSep)
int    xsVectorVectorDictLastError()
```

### Return-value technicalities

`xsVectorVectorDictPut`, `xsVectorVectorDictPutIfAbsent`, and `xsVectorVectorDictRemove` can all return `cVectorVectorDictGenericErrorVector` in more than one situation.

- `cVectorVectorDictSuccess`: the operation succeeded, and the returned vector is meaningful
- `cVectorVectorDictNoKeyError`: either the key was missing, or `Put`/`PutIfAbsent` inserted a new key
- any other negative status: the call failed

This matters because `vector(-1.0, -1.0, -1.0)` is also a valid stored vector value.

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

## 26. Random Numbers

`random.xs` provides a xoshiro128** pseudo-random number generator. Seed with `xsXoSeed`, then draw with `xsXoRandom`, `xsXoRandomFloat`, `xsXoRandomBool`, `xsXoRandomUniformRange`, or `xsXoRandomStr`.

### API

```cpp
include "random.xs";

void  xsXoSeed(int seed)
int   xsXoRandom()                                 // uniform int
float xsXoRandomFloat()                            // uniform float in [0.0, 1.0)
bool  xsXoRandomBool()                             // uniform bool
int   xsXoRandomUniformRange(int start, int end)   // uniform int in [start, end)
string xsXoRandomStr(int size = 8, string chars = "abcdefghijklmnopqrstuvwxyz0123456789")
                                                   // size uniformly picked chars; "" if chars is empty
```

### Example

```cpp
void randomTeams() {
    int numPlayers = 4;
    for (i = 0; < numPlayers) {
        int team = xsXoRandomUniformRange(0, 2);
        xsChatData("Player " + (i + 1) + " -> team " + team);
    }
}
```

## 27. Larger example

The example below shows `Int List`, `IntIntDict`, and the RNG working together in one script.

```cpp
include "intList.xs";
include "intIntDict.xs";
include "random.xs";

void main() {
    int players = xsIntList(1, 2, 3, 4);
    int scoreByPlayer = xsIntIntDict();

    int numPlayers = xsIntListSize(players);
    for (i = 0; < numPlayers) {
        int player = xsIntListGet(players, i);
        int score = 100 + xsXoRandomUniformRange(0, 76);

        xsIntIntDictPut(scoreByPlayer, player, score);
    }

    xsIntListSort(players, false);

    for (i = 0; < numPlayers) {
        int player = xsIntListGet(players, i);
        int score = xsIntIntDictGet(scoreByPlayer, player, 0);

        if (bitAnd(flags, cFlagElite) != 0) {
            xsChatData("Player " + player + " is elite with score " + score);
        } else {
            xsChatData("Player " + player + " score: " + score);
        }
    }
}
```

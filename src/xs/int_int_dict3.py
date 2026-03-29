from numpy import int32, float32

from xs_converter.functions import xs_array_create_int, xs_array_set_int, xs_array_resize_int, xs_array_get_int, \
    xs_array_get_size
from xs_converter.symbols import XsExternConst, i32range

c_int_int_dict_success: XsExternConst[int] = int32(0)
c_int_int_dict_generic_error: XsExternConst[int] = int32(-1)
c_int_int_dict_no_key_error: XsExternConst[int] = int32(-2)
c_int_int_dict_resize_failed_error: XsExternConst[int] = int32(-3)
c_int_int_dict_max_capacity_error: XsExternConst[int] = int32(-4)
c_int_int_dict_max_capacity: XsExternConst[int] = int32(999999999)
c_int_int_dict_max_load_factor: XsExternConst[float32] = float32(0.75)
c_int_int_dict_empty_key: XsExternConst[int] = int32(-999999999)
c_int_int_dict_initial_capacity: XsExternConst[int] = int32(33)
c_int_int_dict_hash_constant: XsExternConst[int] = int32(16777619)
_int_int_dict_last_operation_status: int32 = c_int_int_dict_success
_int_int_dict_temp_array: int32 = int32(-1)


def xs_int_int_dict_create() -> int32:
    """
    Creates an empty int-to-int dictionary.
    Keys equal to `c_int_int_dict_empty_key` (-999999999) are reserved as the internal empty-slot
    sentinel and cannot be stored. `put` and `put_if_absent` silently reject them.
    :return: created dict id, or `c_int_int_dict_generic_error` on error
    """
    dct: int32 = xs_array_create_int(c_int_int_dict_initial_capacity, c_int_int_dict_empty_key)
    xs_array_set_int(dct, 0, 0)
    return dct


def _xs_int_int_dict_hash(key: int32 = int32(-1), capacity: int32 = int32(0)) -> int32:
    hash: int32 = key * c_int_int_dict_hash_constant
    num_slots: int32 = (capacity - 1) // 2
    hash = hash % num_slots
    if hash < 0:
        hash += num_slots
    return (hash * 2) + 1


def _xs_int_int_dict_find_slot(dct: int32 = int32(-1), key: int32 = int32(-1),
                                capacity: int32 = int32(0)) -> int32:
    """Returns array index of slot containing key, or -1 if not found."""
    num_slots: int32 = (capacity - 1) // 2
    home: int32 = _xs_int_int_dict_hash(key, capacity)
    slot: int32 = home
    steps: int32 = int32(0)
    while steps < num_slots:
        stored_key: int32 = xs_array_get_int(dct, slot)
        if stored_key == c_int_int_dict_empty_key:
            return int32(-1)
        if stored_key == key:
            return slot
        slot += 2
        if slot >= capacity:
            slot = int32(1)
        steps += 1
    return int32(-1)


def _xs_int_int_dict_upsert(dct: int32 = int32(-1), key: int32 = int32(-1), val: int32 = int32(0),
                              capacity: int32 = int32(0)) -> int32:
    global _int_int_dict_last_operation_status
    num_slots: int32 = (capacity - 1) // 2
    home: int32 = _xs_int_int_dict_hash(key, capacity)
    slot: int32 = home
    steps: int32 = int32(0)
    while steps < num_slots:
        stored_key: int32 = xs_array_get_int(dct, slot)
        if stored_key == c_int_int_dict_empty_key:
            xs_array_set_int(dct, slot, key)
            xs_array_set_int(dct, slot + 1, val)
            _int_int_dict_last_operation_status = c_int_int_dict_no_key_error
            return c_int_int_dict_generic_error
        if stored_key == key:
            old_val: int32 = xs_array_get_int(dct, slot + 1)
            xs_array_set_int(dct, slot + 1, val)
            _int_int_dict_last_operation_status = c_int_int_dict_success
            return old_val
        slot += 2
        if slot >= capacity:
            slot = int32(1)
        steps += 1
    _int_int_dict_last_operation_status = c_int_int_dict_max_capacity_error
    return c_int_int_dict_generic_error


def _xs_int_int_dict_move_to_temp_array(dct: int32 = int32(-1), size: int32 = int32(0),
                                         capacity: int32 = int32(0)) -> int32:
    global _int_int_dict_temp_array
    temp_data_size: int32 = size * 2
    if _int_int_dict_temp_array < 0:
        _int_int_dict_temp_array = xs_array_create_int(temp_data_size, c_int_int_dict_empty_key)
        if _int_int_dict_temp_array < 0:
            return c_int_int_dict_resize_failed_error
    else:
        temp_arr_capacity: int32 = xs_array_get_size(_int_int_dict_temp_array)
        if temp_arr_capacity < temp_data_size:
            if temp_data_size > c_int_int_dict_max_capacity:
                return c_int_int_dict_max_capacity_error
            r: int32 = xs_array_resize_int(_int_int_dict_temp_array, temp_data_size)
            if r != 1:
                return c_int_int_dict_resize_failed_error
    t: int32 = int32(0)
    for i in i32range(1, capacity, 2):
        stored_key: int32 = xs_array_get_int(dct, i)
        if stored_key != c_int_int_dict_empty_key:
            xs_array_set_int(_int_int_dict_temp_array, t, stored_key)
            xs_array_set_int(_int_int_dict_temp_array, t + 1, xs_array_get_int(dct, i + 1))
            xs_array_set_int(dct, i, c_int_int_dict_empty_key)
            t += 2
    return temp_data_size


def _xs_int_int_dict_clear_new_slots(dct: int32 = int32(-1), old_capacity: int32 = int32(-1),
                                      new_capacity: int32 = int32(-1)) -> None:
    for j in i32range(old_capacity, new_capacity, 2):
        xs_array_set_int(dct, j, c_int_int_dict_empty_key)


def _xs_int_int_dict_rehash_if_needed(dct: int32 = int32(-1), size: int32 = int32(0),
                                       capacity: int32 = int32(0)) -> int32:
    global _int_int_dict_temp_array, _int_int_dict_last_operation_status
    load_factor: float = float(size) / ((capacity - 1) // 2)
    if load_factor > c_int_int_dict_max_load_factor:
        store_status: int32 = _int_int_dict_last_operation_status
        temp_data_size: int32 = _xs_int_int_dict_move_to_temp_array(dct, size, capacity)
        if temp_data_size < 0:
            _int_int_dict_last_operation_status = temp_data_size
            return c_int_int_dict_generic_error
        new_capacity: int32 = (capacity - 1) * 2 + 1
        if new_capacity > c_int_int_dict_max_capacity:
            _int_int_dict_last_operation_status = c_int_int_dict_max_capacity_error
            return c_int_int_dict_generic_error
        r: int32 = xs_array_resize_int(dct, new_capacity)
        if r != 1:
            _int_int_dict_last_operation_status = c_int_int_dict_resize_failed_error
            return c_int_int_dict_generic_error
        _xs_int_int_dict_clear_new_slots(dct, capacity, new_capacity)
        for t in i32range(0, temp_data_size, 2):
            _xs_int_int_dict_upsert(dct, xs_array_get_int(_int_int_dict_temp_array, t),
                                     xs_array_get_int(_int_int_dict_temp_array, t + 1), new_capacity)
            if _int_int_dict_last_operation_status < 0 and _int_int_dict_last_operation_status != c_int_int_dict_no_key_error:
                return c_int_int_dict_generic_error
        _int_int_dict_last_operation_status = store_status
    return c_int_int_dict_success


def xs_int_int_dict_put(dct: int32 = int32(-1), key: int32 = int32(-1), val: int32 = int32(0)) -> int32:
    """
    Inserts or updates a key-value pair. Triggers a rehash when load factor exceeds the threshold. Sets last error on completion.
    If `key` equals `c_int_int_dict_empty_key`, the call is a no-op and returns `c_int_int_dict_generic_error`
    with last error set to `c_int_int_dict_generic_error`.
    :param dct: dict id
    :param key: key to insert or update (must not equal `c_int_int_dict_empty_key`)
    :param val: value to associate with the key
    :return: previous value if the key already existed, or `c_int_int_dict_generic_error` if newly inserted or on error.
        Because -1 is both the error sentinel and a valid previous value, callers must check
        `xs_int_int_dict_last_error()` to distinguish: `c_int_int_dict_success` means the key
        existed and the returned value is valid; `c_int_int_dict_no_key_error` means a new key
        was inserted; any other negative status indicates an error.
    """
    global _int_int_dict_last_operation_status
    if key == c_int_int_dict_empty_key:
        _int_int_dict_last_operation_status = c_int_int_dict_generic_error
        return c_int_int_dict_generic_error
    size: int32 = xs_array_get_int(dct, 0)
    capacity: int32 = xs_array_get_size(dct)

    previous_value: int32 = _xs_int_int_dict_upsert(dct, key, val, capacity)
    if _int_int_dict_last_operation_status == c_int_int_dict_no_key_error:
        size += 1
        xs_array_set_int(dct, 0, size)
    elif _int_int_dict_last_operation_status == c_int_int_dict_success:
        return previous_value
    else:
        return c_int_int_dict_generic_error

    r: int32 = _xs_int_int_dict_rehash_if_needed(dct, size, capacity)
    if r != c_int_int_dict_success:
        return c_int_int_dict_generic_error
    _int_int_dict_last_operation_status = c_int_int_dict_no_key_error
    return c_int_int_dict_generic_error


def xs_int_int_dict(
        k1: int32 = c_int_int_dict_empty_key,
        v1: int32 = int32(0),
        k2: int32 = c_int_int_dict_empty_key,
        v2: int32 = int32(0),
        k3: int32 = c_int_int_dict_empty_key,
        v3: int32 = int32(0),
        k4: int32 = c_int_int_dict_empty_key,
        v4: int32 = int32(0),
        k5: int32 = c_int_int_dict_empty_key,
        v5: int32 = int32(0),
        k6: int32 = c_int_int_dict_empty_key,
        v6: int32 = int32(0),
) -> int32:
    """
    Creates a dict with provided key-value pairs. The first key that equals `c_int_int_dict_empty_key` will stop further insertion.
    This function can create a dict with 6 entries at the maximum, but further entries can be added with `xs_int_int_dict_put`.
    :param k1 through k6: key at a given position (must not equal `c_int_int_dict_empty_key`)
    :param v1 through v6: value associated with the corresponding key
    :return: created dict id, or `c_int_int_dict_generic_error` on error
    """
    dct: int32 = xs_int_int_dict_create()
    if dct < 0:
        return c_int_int_dict_generic_error
    if k1 == c_int_int_dict_empty_key:
        return dct
    xs_int_int_dict_put(dct, k1, v1)
    if k2 == c_int_int_dict_empty_key:
        return dct
    xs_int_int_dict_put(dct, k2, v2)
    if k3 == c_int_int_dict_empty_key:
        return dct
    xs_int_int_dict_put(dct, k3, v3)
    if k4 == c_int_int_dict_empty_key:
        return dct
    xs_int_int_dict_put(dct, k4, v4)
    if k5 == c_int_int_dict_empty_key:
        return dct
    xs_int_int_dict_put(dct, k5, v5)
    if k6 == c_int_int_dict_empty_key:
        return dct
    xs_int_int_dict_put(dct, k6, v6)
    return dct


def xs_int_int_dict_get(dct: int32 = int32(-1), key: int32 = int32(-1), dft: int32 = int32(-1)) -> int32:
    """
    Returns the value associated with the given key. Sets last error on completion.
    :param dct: dict id
    :param key: key to look up
    :param dft: default value returned if the key is not found
    :return: value for the key, or `dft` if not found
    """
    global _int_int_dict_last_operation_status
    capacity: int32 = xs_array_get_size(dct)
    slot: int32 = _xs_int_int_dict_find_slot(dct, key, capacity)
    if slot >= 0:
        _int_int_dict_last_operation_status = c_int_int_dict_success
        return xs_array_get_int(dct, slot + 1)
    _int_int_dict_last_operation_status = c_int_int_dict_no_key_error
    return dft


def xs_int_int_dict_remove(dct: int32 = int32(-1), key: int32 = int32(-1)) -> int32:
    """
    Removes the entry with the given key from the dict. Sets last error on completion.
    Uses backward shift deletion to maintain linear probing invariant (no tombstones).
    :param dct: dict id
    :param key: key to remove
    :return: value that was associated with the key, or `c_int_int_dict_generic_error` if not found
    """
    global _int_int_dict_last_operation_status
    size: int32 = xs_array_get_int(dct, 0)
    capacity: int32 = xs_array_get_size(dct)
    num_slots: int32 = (capacity - 1) // 2
    slot: int32 = _xs_int_int_dict_find_slot(dct, key, capacity)
    if slot < 0:
        _int_int_dict_last_operation_status = c_int_int_dict_no_key_error
        return c_int_int_dict_generic_error
    found_val: int32 = xs_array_get_int(dct, slot + 1)

    # Backward shift to restore linear probing invariant
    g: int32 = slot
    q: int32 = g + 2
    if q >= capacity:
        q = int32(1)
    shift_steps: int32 = int32(0)
    q_key: int32 = xs_array_get_int(dct, q)
    while q_key != c_int_int_dict_empty_key and shift_steps < num_slots:
        q_home: int32 = _xs_int_int_dict_hash(q_key, capacity)
        g_slot: int32 = (g - 1) // 2
        q_slot: int32 = (q - 1) // 2
        h_slot: int32 = (q_home - 1) // 2
        dist_g: int32 = (g_slot - h_slot + num_slots) % num_slots
        dist_q: int32 = (q_slot - h_slot + num_slots) % num_slots
        if dist_g < dist_q:
            xs_array_set_int(dct, g, q_key)
            xs_array_set_int(dct, g + 1, xs_array_get_int(dct, q + 1))
            g = q
        q += 2
        if q >= capacity:
            q = int32(1)
        shift_steps += 1
        q_key = xs_array_get_int(dct, q)
    xs_array_set_int(dct, g, c_int_int_dict_empty_key)
    xs_array_set_int(dct, 0, size - 1)
    _int_int_dict_last_operation_status = c_int_int_dict_success
    return found_val


def xs_int_int_dict_contains(dct: int32 = int32(-1), key: int32 = int32(-1)) -> bool:
    """
    Checks whether the dict contains the given key.
    :param dct: dict id
    :param key: key to search for
    :return: true if the key is found, false otherwise
    """
    capacity: int32 = xs_array_get_size(dct)
    return _xs_int_int_dict_find_slot(dct, key, capacity) >= 0


def xs_int_int_dict_size(dct: int32 = int32(-1)) -> int32:
    """
    Returns the number of key-value pairs in the dict.
    :param dct: dict id
    :return: dict size
    """
    return xs_array_get_int(dct, 0)


def xs_int_int_dict_clear(dct: int32 = int32(-1)) -> int32:
    """
    Removes all entries from the dict and shrinks the backing array.
    :param dct: dict id
    :return: `c_int_int_dict_success` on success, or `c_int_int_dict_generic_error` on error
    """
    capacity: int32 = xs_array_get_size(dct)
    for i in i32range(1, capacity, 2):
        xs_array_set_int(dct, i, c_int_int_dict_empty_key)
    xs_array_set_int(dct, 0, 0)
    if capacity > c_int_int_dict_initial_capacity:
        r: int32 = xs_array_resize_int(dct, c_int_int_dict_initial_capacity)
        if r != 1:
            return c_int_int_dict_generic_error
    return c_int_int_dict_success


def xs_int_int_dict_copy(dct: int32 = int32(-1)) -> int32:
    """
    Returns a deep copy of the dict.
    :param dct: dict id
    :return: new dict id, or `c_int_int_dict_resize_failed_error` on error
    """
    capacity: int32 = xs_array_get_size(dct)
    new_dct: int32 = xs_array_create_int(capacity, c_int_int_dict_empty_key)
    if new_dct < 0:
        return c_int_int_dict_resize_failed_error
    for i in i32range(1, capacity, 2):
        stored_key: int32 = xs_array_get_int(dct, i)
        if stored_key != c_int_int_dict_empty_key:
            xs_array_set_int(new_dct, i, stored_key)
            xs_array_set_int(new_dct, i + 1, xs_array_get_int(dct, i + 1))
    xs_array_set_int(new_dct, 0, xs_array_get_int(dct, 0))
    return new_dct


def xs_int_int_dict_to_string(dct: int32 = int32(-1)) -> str:
    """
    Returns a string representation of the dict in the format `{k1: v1, k2: v2, ...}`.
    :param dct: dict id
    :return: string representation of the dict
    """
    capacity: int32 = xs_array_get_size(dct)
    s: str = "{"
    key: int32 = int32(0)
    val: int32 = int32(0)
    first: bool = True
    for i in i32range(1, capacity, 2):
        key = xs_array_get_int(dct, i)
        if key != c_int_int_dict_empty_key:
            val = xs_array_get_int(dct, i + 1)
            if first:
                first = False
            else:
                s += ", "
            s += f"{key}: {val}"
    s += "}"
    return s


def xs_int_int_dict_last_error() -> int32:
    """
    Returns the status code of the last operation that sets it (put, get, remove, next_key, has_next).
    :return: `c_int_int_dict_success` if the last such operation succeeded, or a negative error code
    """
    return _int_int_dict_last_operation_status


def _xs_int_int_dict_find_next_occupied(dct: int32 = int32(-1), start: int32 = int32(1),
                                         capacity: int32 = int32(0)) -> int32:
    global _int_int_dict_last_operation_status
    slot: int32 = start
    while slot < capacity:
        stored_key: int32 = xs_array_get_int(dct, slot)
        if stored_key != c_int_int_dict_empty_key:
            _int_int_dict_last_operation_status = c_int_int_dict_success
            return stored_key
        slot += 2
    _int_int_dict_last_operation_status = c_int_int_dict_no_key_error
    return c_int_int_dict_generic_error


def xs_int_int_dict_next_key(dct: int32 = int32(-1), is_first: bool = True,
                              prev_key: int32 = int32(-1)) -> int32:
    """
    Returns the next key in the dict for stateless iteration. Sets last error on completion.
    :param dct: dict id
    :param is_first: if true, returns the first key in the dict
    :param prev_key: the previous key returned by this function (ignored if `is_first` is true)
    :return: next key, or `c_int_int_dict_generic_error` if no more keys (last error set to `c_int_int_dict_no_key_error`)
    """
    global _int_int_dict_last_operation_status
    capacity: int32 = xs_array_get_size(dct)
    if is_first:
        return _xs_int_int_dict_find_next_occupied(dct, int32(1), capacity)
    slot: int32 = _xs_int_int_dict_find_slot(dct, prev_key, capacity)
    if slot < 0:
        _int_int_dict_last_operation_status = c_int_int_dict_no_key_error
        return c_int_int_dict_generic_error
    next_start: int32 = slot + 2
    return _xs_int_int_dict_find_next_occupied(dct, next_start, capacity)


def xs_int_int_dict_has_next(dct: int32 = int32(-1), is_first: bool = True,
                              prev_key: int32 = int32(-1)) -> bool:
    """
    Checks whether there is a next key in the dict for stateless iteration.
    :param dct: dict id
    :param is_first: if true, checks whether the dict has any keys
    :param prev_key: the previous key (ignored if `is_first` is true)
    :return: true if there is a next key, false otherwise
    """
    capacity: int32 = xs_array_get_size(dct)
    start: int32 = int32(1)
    if not is_first:
        slot: int32 = _xs_int_int_dict_find_slot(dct, prev_key, capacity)
        if slot < 0:
            return False
        start = slot + 2
    while start < capacity:
        if xs_array_get_int(dct, start) != c_int_int_dict_empty_key:
            return True
        start += 2
    return False


def xs_int_int_dict_update(source: int32 = int32(-1), dct: int32 = int32(-1)) -> int32:
    """
    Inserts all key-value pairs from another dict into the source dict, overwriting existing keys.
    :param source: dict id to update
    :param dct: dict id whose entries are copied into source
    :return: `c_int_int_dict_success` on success, or a negative error code
    """
    global _int_int_dict_last_operation_status
    capacity: int32 = xs_array_get_size(dct)
    for i in i32range(1, capacity, 2):
        key: int32 = xs_array_get_int(dct, i)
        if key != c_int_int_dict_empty_key:
            xs_int_int_dict_put(source, key, xs_array_get_int(dct, i + 1))
            if _int_int_dict_last_operation_status != c_int_int_dict_success and _int_int_dict_last_operation_status != c_int_int_dict_no_key_error:
                return _int_int_dict_last_operation_status
    _int_int_dict_last_operation_status = c_int_int_dict_success
    return c_int_int_dict_success


def xs_int_int_dict_put_if_absent(dct: int32 = int32(-1), key: int32 = int32(-1),
                                   val: int32 = int32(0)) -> int32:
    """
    Inserts the key-value pair only if the key is not already present. Sets last error on completion.
    If `key` equals `c_int_int_dict_empty_key`, the call is a no-op and returns `c_int_int_dict_generic_error`
    with last error set to `c_int_int_dict_generic_error`.
    :param dct: dict id
    :param key: key to insert (must not equal `c_int_int_dict_empty_key`)
    :param val: value to associate with the key
    :return: existing value if the key was already present, or `c_int_int_dict_generic_error` if newly inserted or on error.
        Callers must check `xs_int_int_dict_last_error()` to distinguish: `c_int_int_dict_success` means the key
        already existed and the returned value is the existing one; `c_int_int_dict_no_key_error` means a new key
        was inserted; any other negative status indicates an error.
    """
    global _int_int_dict_last_operation_status
    if key == c_int_int_dict_empty_key:
        _int_int_dict_last_operation_status = c_int_int_dict_generic_error
        return c_int_int_dict_generic_error
    capacity: int32 = xs_array_get_size(dct)
    num_slots: int32 = (capacity - 1) // 2
    home: int32 = _xs_int_int_dict_hash(key, capacity)
    slot: int32 = home
    steps: int32 = int32(0)
    while steps < num_slots:
        stored_key: int32 = xs_array_get_int(dct, slot)
        if stored_key == c_int_int_dict_empty_key:
            xs_array_set_int(dct, slot, key)
            xs_array_set_int(dct, slot + 1, val)
            size: int32 = xs_array_get_int(dct, 0) + 1
            xs_array_set_int(dct, 0, size)
            r: int32 = _xs_int_int_dict_rehash_if_needed(dct, size, capacity)
            if r != c_int_int_dict_success:
                return c_int_int_dict_generic_error
            _int_int_dict_last_operation_status = c_int_int_dict_no_key_error
            return c_int_int_dict_generic_error
        if stored_key == key:
            _int_int_dict_last_operation_status = c_int_int_dict_success
            return xs_array_get_int(dct, slot + 1)
        slot += 2
        if slot >= capacity:
            slot = int32(1)
        steps += 1
    _int_int_dict_last_operation_status = c_int_int_dict_max_capacity_error
    return c_int_int_dict_generic_error


def xs_int_int_dict_keys(dct: int32 = int32(-1)) -> int32:
    """
    Returns a new int array containing all keys in the dict. Order is arbitrary.
    :param dct: dict id
    :return: array id, or `c_int_int_dict_resize_failed_error` on allocation failure
    """
    size: int32 = xs_array_get_int(dct, 0)
    arr: int32 = xs_array_create_int(size, 0)
    if arr < 0:
        return c_int_int_dict_resize_failed_error
    capacity: int32 = xs_array_get_size(dct)
    idx: int32 = int32(0)
    for i in i32range(1, capacity, 2):
        stored_key: int32 = xs_array_get_int(dct, i)
        if stored_key != c_int_int_dict_empty_key:
            xs_array_set_int(arr, idx, stored_key)
            idx += 1
    return arr


def xs_int_int_dict_values(dct: int32 = int32(-1)) -> int32:
    """
    Returns a new int array containing all values in the dict. Order matches `xs_int_int_dict_keys`.
    :param dct: dict id
    :return: array id, or `c_int_int_dict_resize_failed_error` on allocation failure
    """
    size: int32 = xs_array_get_int(dct, 0)
    arr: int32 = xs_array_create_int(size, 0)
    if arr < 0:
        return c_int_int_dict_resize_failed_error
    capacity: int32 = xs_array_get_size(dct)
    idx: int32 = int32(0)
    for i in i32range(1, capacity, 2):
        stored_key: int32 = xs_array_get_int(dct, i)
        if stored_key != c_int_int_dict_empty_key:
            xs_array_set_int(arr, idx, xs_array_get_int(dct, i + 1))
            idx += 1
    return arr


def xs_int_int_dict_equals(a: int32 = int32(-1), b: int32 = int32(-1)) -> bool:
    """
    Returns true if both dicts contain the same key-value pairs.
    :param a: first dict id
    :param b: second dict id
    :return: true if both dicts are equal, false otherwise
    """
    size_a: int32 = xs_array_get_int(a, 0)
    size_b: int32 = xs_array_get_int(b, 0)
    if size_a != size_b:
        return False
    capacity: int32 = xs_array_get_size(a)
    for i in i32range(1, capacity, 2):
        key: int32 = xs_array_get_int(a, i)
        if key != c_int_int_dict_empty_key:
            val: int32 = xs_array_get_int(a, i + 1)
            if xs_int_int_dict_get(b, key) != val:
                return False
            if xs_int_int_dict_last_error() != c_int_int_dict_success:
                return False
    return True

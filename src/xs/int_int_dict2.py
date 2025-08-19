from xs_converter.converter import PythonToXsConverter
from xs_converter.functions import xs_array_create_int, xs_array_set_int, xs_array_resize_int, xs_array_get_int, \
    xs_array_get_size
from xs_converter.symbols import XsExternConst

c_int_int_dict_success = 0
c_int_int_dict_generic_error = -1
c_int_int_dict_no_key_error = -2
c_int_int_dict_resize_failed_error = -3
c_int_int_dict_max_capacity_error = -4
c_int_int_dict_max_capacity = 999999999
c_int_int_dict_max_load_factor = 0.75
c_int_int_dict_empty_param = -999999999
c_int_int_dict_initial_num_of_buckets = 49
c_int_int_dict_initial_bucket_size = 4
c_int_int_dict_min_bucket_size = 2
c_int_int_dict_hash_constant = 16777619
_int_int_dict_last_operation_status = c_int_int_dict_success
_int_int_dict_temp_array = -1


def constants() -> None:
    c_int_int_dict_success: XsExternConst[int] = 0
    c_int_int_dict_generic_error: XsExternConst[int] = -1
    c_int_int_dict_no_key_error: XsExternConst[int] = -2
    c_int_int_dict_resize_failed_error: XsExternConst[int] = -3
    c_int_int_dict_max_capacity_error: XsExternConst[int] = -4
    c_int_int_dict_max_capacity: XsExternConst[int] = 999999999
    c_int_int_dict_max_load_factor: XsExternConst[float] = 0.75
    c_int_int_dict_empty_param: XsExternConst[int] = -999999999
    c_int_int_dict_initial_num_of_buckets: XsExternConst[int] = 49
    c_int_int_dict_initial_bucket_size: XsExternConst[int] = 4
    c_int_int_dict_min_bucket_size: XsExternConst[int] = 2
    c_int_int_dict_hash_constant: XsExternConst[int] = 16777619
    _int_int_dict_last_operation_status: int = c_int_int_dict_success
    _int_int_dict_temp_array: int = -1


def xs_int_int_dict_create() -> int:
    dct: int = xs_array_create_int(c_int_int_dict_initial_num_of_buckets, 0)
    xs_array_set_int(dct, 0, 0)
    return dct


def _xs_int_int_dict_hash(key: int = -1, capacity: int = 0) -> int:
    hash: int = key * c_int_int_dict_hash_constant
    num_of_buckets: int = (capacity - 1) // 3
    hash = hash % num_of_buckets
    if hash < 0:
        hash += num_of_buckets
    return (hash * 3) + 1


def _xs_int_int_dict_replace(dct: int = -1, key: int = -1, val: int = 0, capacity: int = 0) -> int:
    global _int_int_dict_last_operation_status
    hash: int = _xs_int_int_dict_hash(key, capacity)
    bucket_type: int = xs_array_get_int(dct, hash)
    bucket_arr: int = 0
    stored_key: int = 0
    stored_val: int = 0
    if bucket_type == 0:
        xs_array_set_int(dct, hash, 1)
        xs_array_set_int(dct, hash + 1, key)
        xs_array_set_int(dct, hash + 2, val)
        _int_int_dict_last_operation_status = c_int_int_dict_no_key_error
        return c_int_int_dict_generic_error
    elif bucket_type == 1:
        stored_key = xs_array_get_int(dct, hash + 1)
        if stored_key == key:
            stored_val = xs_array_get_int(dct, hash + 2)
            xs_array_set_int(dct, hash + 2,  val)
            _int_int_dict_last_operation_status = c_int_int_dict_success
            return stored_val
        else:
            bucket_arr = xs_array_create_int(c_int_int_dict_initial_bucket_size, 0)
            if bucket_arr < 0:
                _int_int_dict_last_operation_status = c_int_int_dict_resize_failed_error
                return c_int_int_dict_generic_error
            xs_array_set_int(bucket_arr, 0, stored_key)
            xs_array_set_int(bucket_arr, 1, xs_array_get_int(dct, hash + 2))
            xs_array_set_int(bucket_arr, 2, key)
            xs_array_set_int(bucket_arr, 3, val)
            xs_array_set_int(dct, hash, 2)
            xs_array_set_int(dct, hash + 1, bucket_arr)
            xs_array_set_int(dct, hash + 2, 4)
            _int_int_dict_last_operation_status = c_int_int_dict_no_key_error
            return c_int_int_dict_generic_error
    elif bucket_type == 2:
        bucket_arr = xs_array_get_int(dct, hash + 1)
        bucket_size: int = xs_array_get_int(dct, hash + 2)
        for i in range(0, bucket_size, 2):
            stored_key = xs_array_get_int(bucket_arr, i)
            if stored_key == key:
                stored_val = xs_array_get_int(bucket_arr, i + 1)
                xs_array_set_int(bucket_arr, i + 1, val)
                _int_int_dict_last_operation_status = c_int_int_dict_success
                return stored_val
        bucket_capacity: int = xs_array_get_size(bucket_arr)
        if bucket_capacity - bucket_size < 2:
            new_capacity: int = bucket_capacity * 2
            if new_capacity > c_int_int_dict_max_capacity:
                _int_int_dict_last_operation_status = c_int_int_dict_max_capacity_error
                return c_int_int_dict_generic_error
            r: int = xs_array_resize_int(bucket_arr, new_capacity)
            if r != 1:
                _int_int_dict_last_operation_status = c_int_int_dict_resize_failed_error
                return c_int_int_dict_generic_error

        xs_array_set_int(bucket_arr, bucket_size, key)
        xs_array_set_int(bucket_arr, bucket_size + 1, val)
        xs_array_set_int(dct, hash + 2, bucket_size + 2)
        _int_int_dict_last_operation_status = c_int_int_dict_no_key_error
        return c_int_int_dict_generic_error

    _int_int_dict_last_operation_status = c_int_int_dict_generic_error
    return c_int_int_dict_generic_error


def _xs_int_int_dict_move_to_temp_array(dct: int = -1, size: int = 0, capacity: int = 0) -> int:
    global _int_int_dict_temp_array
    temp_data_size: int = size * 2
    if _int_int_dict_temp_array < 0:
        _int_int_dict_temp_array = xs_array_create_int(temp_data_size, c_int_int_dict_empty_param)
        if _int_int_dict_temp_array < 0:
            return c_int_int_dict_resize_failed_error
    else:
        temp_arr_capacity: int = xs_array_get_size(_int_int_dict_temp_array)
        if temp_arr_capacity < temp_data_size:
            if temp_data_size > c_int_int_dict_max_capacity:
                return c_int_int_dict_max_capacity_error
            r: int = xs_array_resize_int(_int_int_dict_temp_array, temp_data_size)
            if r != 1:
                return c_int_int_dict_resize_failed_error
    t: int = 0
    for i in range(1, capacity, 3):
        bucket_type: int = xs_array_get_int(dct, i)
        if bucket_type == 1:
            xs_array_set_int(_int_int_dict_temp_array, t, xs_array_get_int(dct, i + 1))
            xs_array_set_int(_int_int_dict_temp_array, t + 1, xs_array_get_int(dct, i + 2))
            xs_array_set_int(dct, i , 0)
            t += 2
        elif bucket_type == 2:
            bucket_arr: int = xs_array_get_int(dct, i + 1)
            bucket_size: int = xs_array_get_int(dct, i + 2)
            for j in range(0, bucket_size, 2):
                stored_key: int = xs_array_get_int(bucket_arr, j)
                stored_val: int = xs_array_get_int(bucket_arr, j + 1)
                xs_array_set_int(_int_int_dict_temp_array, t, stored_key)
                xs_array_set_int(_int_int_dict_temp_array, t + 1, stored_val)
                t += 2
            xs_array_set_int(dct, i + 2, 0)
    return temp_data_size


def xs_int_int_dict_put(dct: int = -1, key: int = -1, val: int = 0) -> int:
    global _int_int_dict_temp_array, _int_int_dict_last_operation_status
    size: int = xs_array_get_int(dct, 0)
    capacity: int = xs_array_get_size(dct)

    previous_value: int = _xs_int_int_dict_replace(dct, key, val, capacity)
    if _int_int_dict_last_operation_status == c_int_int_dict_no_key_error:
        size += 1
        xs_array_set_int(dct, 0, size)
    elif _int_int_dict_last_operation_status == c_int_int_dict_success:
        return previous_value
    else:
        return c_int_int_dict_generic_error

    load_factor: float = float(size) / ((capacity - 1 ) // 3)
    if load_factor > c_int_int_dict_max_load_factor:
        store_status: int = _int_int_dict_last_operation_status
        temp_data_size: int = _xs_int_int_dict_move_to_temp_array(dct, size, capacity)
        if temp_data_size < 0:
            _int_int_dict_last_operation_status = temp_data_size
            return c_int_int_dict_generic_error
        new_capacity: int = (capacity - 1) * 2 + 1
        if new_capacity > c_int_int_dict_max_capacity:
            _int_int_dict_last_operation_status = c_int_int_dict_resize_failed_error
            return c_int_int_dict_generic_error
        r: int = xs_array_resize_int(dct, new_capacity)
        if r != 1:
            _int_int_dict_last_operation_status = c_int_int_dict_resize_failed_error
            return c_int_int_dict_generic_error
        _xs_int_int_dict_clear_arrays(dct, capacity, new_capacity)
        for t in range(0, temp_data_size, 2):
            _xs_int_int_dict_replace(dct, xs_array_get_int(_int_int_dict_temp_array, t),
                                     xs_array_get_int(_int_int_dict_temp_array, t + 1), new_capacity)
            if _int_int_dict_last_operation_status < 0 and _int_int_dict_last_operation_status != c_int_int_dict_no_key_error:
                return c_int_int_dict_generic_error
        _int_int_dict_last_operation_status = store_status
    return c_int_int_dict_generic_error


def _xs_int_int_dict_clear_arrays(dct: int = -1, capacity: int = -1, new_capacity: int = -1) -> None:
    for i in range(1, capacity, 3):
        bucket_type: int = xs_array_get_int(dct, i)
        if bucket_type == 1:
            xs_array_set_int(dct, i, 0)
        elif bucket_type == 2:
            xs_array_set_int(dct, i + 2, 0)

    for j in range(capacity, new_capacity, 3):
        xs_array_set_int(dct, j, 0)


def xs_int_int_dict(
        k1: int = c_int_int_dict_empty_param,
        v1: int = 0,
        k2: int = c_int_int_dict_empty_param,
        v2: int = 0,
        k3: int = c_int_int_dict_empty_param,
        v3: int = 0,
        k4: int = c_int_int_dict_empty_param,
        v4: int = 0,
        k5: int = c_int_int_dict_empty_param,
        v5: int = 0,
        k6: int = c_int_int_dict_empty_param,
        v6: int = 0,
) -> int:
    dct: int = xs_int_int_dict_create()
    if dct < 0:
        return c_int_int_dict_generic_error
    if k1 == c_int_int_dict_empty_param:
        return dct
    xs_int_int_dict_put(dct, k1, v1)
    if k2 == c_int_int_dict_empty_param:
        return dct
    xs_int_int_dict_put(dct, k2, v2)
    if k3 == c_int_int_dict_empty_param:
        return dct
    xs_int_int_dict_put(dct, k3, v3)
    if k4 == c_int_int_dict_empty_param:
        return dct
    xs_int_int_dict_put(dct, k4, v4)
    if k5 == c_int_int_dict_empty_param:
        return dct
    xs_int_int_dict_put(dct, k5, v5)
    if k6 == c_int_int_dict_empty_param:
        return dct
    xs_int_int_dict_put(dct, k6, v6)
    return dct


def xs_int_int_dict_get(dct: int = -1, key: int = -1, dft: int = -1) -> int:
    global _int_int_dict_last_operation_status
    capacity: int = xs_array_get_size(dct)
    hash: int = _xs_int_int_dict_hash(key, capacity)
    bucket_type: int = xs_array_get_int(dct, hash)
    if bucket_type == 0:
        _int_int_dict_last_operation_status = c_int_int_dict_no_key_error
        return dft
    elif bucket_type == 1:
        if xs_array_get_int(dct, hash + 1) == key:
            _int_int_dict_last_operation_status = c_int_int_dict_success
            return xs_array_get_int(dct, hash + 2)
        _int_int_dict_last_operation_status = c_int_int_dict_no_key_error
        return dft
    elif bucket_type == 2:
        bucket_arr: int = xs_array_get_int(dct, hash + 1)
        bucket_size: int = xs_array_get_int(dct, hash + 2)
        for j in range(0, bucket_size, 2):
            if key == xs_array_get_int(bucket_arr, j):
                _int_int_dict_last_operation_status = c_int_int_dict_success
                return xs_array_get_int(bucket_arr, j + 1)
    _int_int_dict_last_operation_status = c_int_int_dict_no_key_error
    return dft


def xs_int_int_dict_remove(dct: int = -1, key: int = -1) -> int:
    global _int_int_dict_last_operation_status, _int_int_dict_temp_array
    size: int = xs_array_get_int(dct, 0)
    capacity: int = xs_array_get_size(dct)
    hash: int = _xs_int_int_dict_hash(key, capacity)
    bucket_type: int = xs_array_get_int(dct, hash)
    stored_key: int = 0
    if bucket_type == 0:
        _int_int_dict_last_operation_status = c_int_int_dict_no_key_error
        return c_int_int_dict_generic_error
    if bucket_type == 1:
        stored_key = xs_array_get_int(dct, hash + 1)
        if stored_key == key:
            xs_array_set_int(dct, hash, 0)
            xs_array_set_int(dct, 0, size - 1)
            _int_int_dict_last_operation_status = c_int_int_dict_success
            return xs_array_get_int(dct, hash + 2)
        _int_int_dict_last_operation_status = c_int_int_dict_no_key_error
        return c_int_int_dict_generic_error
    if bucket_type == 2:
        bucket_arr: int = xs_array_get_int(dct, hash + 1)
        bucket_size: int = xs_array_get_int(dct, hash + 2)
        found: bool = False
        prev_value: int = 0
        for i in range(0, bucket_size, 2):
            stored_key = xs_array_get_int(bucket_arr, i)
            if found:
                xs_array_set_int(bucket_arr, i - 2, stored_key)
                xs_array_set_int(bucket_arr, i - 1, xs_array_get_int(bucket_arr, i + 1))
            elif stored_key == key:
                found = True
                prev_value = xs_array_get_int(bucket_arr, i + 1)
                xs_array_set_int(bucket_arr, hash + 2, bucket_size - 2)
                xs_array_set_int(dct, 0, size - 1)
        if found:
            _int_int_dict_last_operation_status = c_int_int_dict_success
            return prev_value
        _int_int_dict_last_operation_status = c_int_int_dict_no_key_error
        return c_int_int_dict_generic_error
    _int_int_dict_last_operation_status = c_int_int_dict_generic_error
    return c_int_int_dict_generic_error


def xs_int_int_dict_contains(dct: int = -1, key: int = -1) -> bool:
    capacity: int = xs_array_get_size(dct)
    hash: int = _xs_int_int_dict_hash(key, capacity)
    bucket_type: int = xs_array_get_int(dct, hash)
    if bucket_type == 0:
        return False
    if bucket_type == 1:
        return xs_array_get_int(dct, hash + 1) == key
    if bucket_type == 2:
        bucket_size: int = xs_array_get_int(dct, hash + 2)
        for j in range(0, bucket_size, 2):
            if key == xs_array_get_int(dct, j):
                return True
    return False


def xs_int_int_dict_size(dct: int = -1) -> int:
    return xs_array_get_int(dct, 0)


def xs_int_int_dict_clear(dct: int = -1) -> int:
    dict_capacity: int = xs_array_get_size(dct)
    for i in range(1, dict_capacity, 3):
        bucket_type: int = xs_array_get_int(dct, i)
        if bucket_type == 1:
            xs_array_set_int(dct, i, 0)
        elif bucket_type == 2:
            xs_array_set_int(dct, i + 2, 0)
            bucket_arr: int = xs_array_get_int(dct, i + 1)
            bucket_capacity: int = xs_array_get_size(bucket_arr)
            if bucket_capacity > c_int_int_dict_min_bucket_size:
                r1: int = xs_array_resize_int(bucket_type, c_int_int_dict_min_bucket_size)
                if r1 != 1:
                    return c_int_int_dict_generic_error
    xs_array_set_int(dct, 0, 0)
    if dict_capacity > c_int_int_dict_initial_num_of_buckets:
        r2: int = xs_array_resize_int(dct, c_int_int_dict_initial_num_of_buckets)
        if r2 != 1:
            return c_int_int_dict_generic_error
    return c_int_int_dict_success


def xs_int_int_dict_copy(dct: int = -1) -> int:
    capacity: int = xs_array_get_size(dct)
    new_dct: int = xs_array_create_int(capacity, 0)
    if new_dct < 0:
        return c_int_int_dict_resize_failed_error
    for i in range(1, capacity, 3):
        bucket_type: int = xs_array_get_int(dct, i)
        if bucket_type == 1:
            xs_array_set_int(new_dct, i, 1)
            xs_array_set_int(new_dct, i + 1, xs_array_get_int(dct, i + 1))
            xs_array_set_int(new_dct, i + 2, xs_array_get_int(dct, i + 2))
        elif bucket_type == 2:
            bucket_arr: int = xs_array_get_int(dct, i + 1)
            bucket_size: int = xs_array_get_int(dct, i + 2)
            bucket_capacity: int = xs_array_get_size(bucket_arr)
            new_bucket_arr: int = xs_array_create_int(bucket_capacity, 0)
            if new_bucket_arr < 0:
                return c_int_int_dict_resize_failed_error
            for j in range(bucket_size):
                xs_array_set_int(new_bucket_arr, j, xs_array_get_int(bucket_arr, j))
            xs_array_set_int(new_dct, i, 2)
            xs_array_set_int(new_dct, i + 1, new_bucket_arr)
            xs_array_set_int(new_dct, i + 2, bucket_size)
    xs_array_set_int(new_dct, 0, xs_array_get_int(dct, 0))
    return new_dct


def xs_int_int_dict_to_string(dct: int = -1) -> str:
    dict_size: int = xs_array_get_size(dct)
    s: str = "{"
    key: int = 0
    val: int = 0
    first: bool = True
    for i in range(1, dict_size, 3):
        bucket_type: int = xs_array_get_int(dct, i)
        if bucket_type == 1:
            key = xs_array_get_int(dct, i + 1)
            val = xs_array_get_int(dct, i + 2)
            if first:
                first = False
            else:
                s += ", "
            s += f"{key}: {val}"
        elif bucket_type == 2:
            bucket_arr: int = xs_array_get_int(dct, i + 1)
            bucket_size: int = xs_array_get_int(dct, i + 2)
            for j in range(0, bucket_size, 2):
                key = xs_array_get_int(bucket_arr, j)
                val = xs_array_get_int(bucket_arr, j + 1)
                if first:
                    first = False
                else:
                    s += ", "
                s += f"{key}: {val}"
    s += "}"
    return s


def xs_int_int_dict_last_error() -> int:
    return _int_int_dict_last_operation_status


def _xs_int_int_find_next_from_bucket(bucket: int = -1, dct: int = -1, dict_size: int = -1) -> int:
    global _int_int_dict_last_operation_status
    for i in range(bucket, dict_size, 3):
        bucket_type: int = xs_array_get_int(dct, i)
        if bucket_type == 1:
            _int_int_dict_last_operation_status = c_int_int_dict_success
            return xs_array_get_int(dct, i + 1)
        if bucket_type == 2 and xs_array_get_int(dct, i + 2) > 0:
            _int_int_dict_last_operation_status = c_int_int_dict_success
            return xs_array_get_int(xs_array_get_int(dct, i + 1), 0)
    _int_int_dict_last_operation_status = c_int_int_dict_no_key_error
    return c_int_int_dict_generic_error


def xs_int_int_dict_next_key(dct: int = -1, is_first: bool = True, prev_key: int = -1) -> int:
    global _int_int_dict_last_operation_status
    dict_size: int = xs_array_get_size(dct)
    if is_first:
        return _xs_int_int_find_next_from_bucket(1, dct, dict_size)
    hash: int = _xs_int_int_dict_hash(prev_key, dict_size)
    bucket_type: int = xs_array_get_int(dct, hash)
    if bucket_type == 2:
        bucket_arr: int = xs_array_get_int(dct, hash + 1)
        bucket_size: int = xs_array_get_int(dct, hash + 2)
        i: int = 0
        found: bool = False
        while i < bucket_size and not found:
            stored_key: int = xs_array_get_int(bucket_arr, i)
            if stored_key == prev_key:
                if i + 2 < bucket_size:
                    _int_int_dict_last_operation_status = c_int_int_dict_success
                    return xs_array_get_int(bucket_arr, i + 2)
                found = True
            i += 2
        if not found:
            _int_int_dict_last_operation_status = c_int_int_dict_no_key_error
            return c_int_int_dict_generic_error
    return _xs_int_int_find_next_from_bucket(hash + 3, dct, dict_size)


def xs_int_int_dict_has_next(dct: int = -1, is_first: bool = True, prev_key: int = -1) -> bool:
    global _int_int_dict_last_operation_status
    xs_int_int_dict_next_key(dct, is_first, prev_key)
    r: bool = _int_int_dict_last_operation_status != c_int_int_dict_no_key_error
    _int_int_dict_last_operation_status = c_int_int_dict_success
    return r


def xs_int_int_dict_update(source: int = -1, dct: int = -1) -> int:
    global _int_int_dict_last_operation_status
    key: int = xs_int_int_dict_next_key(dct)
    while xs_int_int_dict_last_error() != c_int_int_dict_no_key_error:
        val: int = xs_int_int_dict_get(dct, key)
        err: int = xs_int_int_dict_last_error()
        if err != 0:
            return err
        xs_int_int_dict_put(source, key, val)
        err = xs_int_int_dict_last_error()
        if err != 0 and err != c_int_int_dict_no_key_error:
            return err
        key = xs_int_int_dict_next_key(dct, False, key)
    _int_int_dict_last_operation_status = c_int_int_dict_success
    return c_int_int_dict_success


def test() -> None:
    pass


def int_int_dict(include_test: bool) -> (str, str):
    test()
    constants_function_xs = PythonToXsConverter.to_xs_script(
        constants,
        indent=True,
    )
    constants_xs = (constants_function_xs[constants_function_xs.find("extern"):constants_function_xs.rfind("}")]
                    .strip()
                    .replace("    ", "")
                    ) + "\n\n"
    xs = constants_xs + PythonToXsConverter.to_xs_script(
        _xs_int_int_dict_hash,
        _xs_int_int_dict_replace,
        _xs_int_int_dict_move_to_temp_array,
        _xs_int_int_dict_clear_arrays,
        xs_int_int_dict_put,
        xs_int_int_dict_create,
        xs_int_int_dict,
        xs_int_int_dict_get,
        xs_int_int_dict_remove,
        xs_int_int_dict_contains,
        xs_int_int_dict_size,
        xs_int_int_dict_clear,
        xs_int_int_dict_copy,
        _xs_int_int_find_next_from_bucket,
        xs_int_int_dict_next_key,
        xs_int_int_dict_has_next,
        xs_int_int_dict_to_string,
        xs_int_int_dict_last_error,
        xs_int_int_dict_update,
        indent=True,
    )
    constants_xs = (constants_function_xs[constants_function_xs.find("extern"):constants_function_xs.rfind("}")]
                    .strip()
                    .replace("    ", "")
                    ) + "\n\n"
    if include_test:
        xs += constants_xs + PythonToXsConverter.to_xs_script(
            test,
            indent=True,
        )
    print(xs)
    return (xs, "intIntDict")


if __name__ == '__main__':
    int_int_dict(True)

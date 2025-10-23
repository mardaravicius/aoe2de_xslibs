from numpy import int32, float32

from xs_converter.converter import PythonToXsConverter
from xs_converter.functions import xs_array_create_int, xs_array_set_int, xs_array_resize_int, xs_array_get_int, \
    xs_array_get_size
from xs_converter.symbols import XsExternConst, i32range

c_int_int_dict_success = int32(0)
c_int_int_dict_generic_error = int32(-1)
c_int_int_dict_no_key_error = int32(-2)
c_int_int_dict_resize_failed_error = int32(-3)
c_int_int_dict_max_capacity_error = int32(-4)
c_int_int_dict_max_capacity = int32(999999999)
c_int_int_dict_max_load_factor = float32(0.75)
c_int_int_dict_empty_param = int32(-999999999)
c_int_int_dict_initial_num_of_buckets = int32(17)
c_int_int_dict_initial_bucket_size = int32(3)
c_int_int_dict_min_bucket_size = int32(3)
c_int_int_dict_hash_constant = int32(16777619)
_int_int_dict_last_operation_status = c_int_int_dict_success
_c_int_int_dict_key_exists = False
_int_int_dict_temp_array = int32(-1)
_int_int_dict_iterator_prev_key = int32(-1)
_int_int_dict_iterator_prev_idx = int32(1)


def constants() -> None:
    c_int_int_dict_success: XsExternConst[int32] = int32(0)
    c_int_int_dict_generic_error: XsExternConst[int32] = int32(-1)
    c_int_int_dict_no_key_error: XsExternConst[int32] = int32(-2)
    c_int_int_dict_resize_failed_error: XsExternConst[int32] = int32(-3)
    c_int_int_dict_max_capacity_error: XsExternConst[int32] = int32(-4)
    c_int_int_dict_max_capacity: XsExternConst[int32] = int32(999999999)
    c_int_int_dict_max_load_factor: XsExternConst[float] = float32(0.75)
    c_int_int_dict_empty_param: XsExternConst[int32] = int32(-999999999)
    c_int_int_dict_initial_num_of_buckets: XsExternConst[int32] = int32(17)
    c_int_int_dict_initial_bucket_size: XsExternConst[int32] = int32(3)
    c_int_int_dict_min_bucket_size: XsExternConst[int32] = int32(3)
    c_int_int_dict_hash_constant: XsExternConst[int32] = int32(16777619)
    _int_int_dict_last_operation_status: int32 = c_int_int_dict_success
    _c_int_int_dict_key_exists: bool = False
    _int_int_dict_temp_array: int32 = int32(-1)
    _int_int_dict_iterator_prev_key: int32 = int32(-1)
    _int_int_dict_iterator_prev_idx: int32 = int32(1)


def xs_int_int_dict_create() -> int32:
    dct: int32 = xs_array_create_int(c_int_int_dict_initial_num_of_buckets, c_int_int_dict_empty_param)
    xs_array_set_int(dct, 0, 0)
    return dct


def _xs_int_int_dict_hash(key: int32 = int32(-1), num_of_buckets: int32 = int32(0)) -> int32:
    hash: int32 = key * c_int_int_dict_hash_constant
    hash = hash % num_of_buckets
    if hash < 0:
        hash = hash + num_of_buckets
    return hash + 1


def _xs_int_int_dict_replace(dct: int32 = int32(-1), key: int32 = int32(-1), val: int32 = int32(0),
                             num_of_buckets: int32 = int32(0)) -> int32:
    global _int_int_dict_last_operation_status
    hash: int32 = _xs_int_int_dict_hash(key, num_of_buckets)
    bucket: int32 = xs_array_get_int(dct, hash)
    if bucket < 0:
        bucket = xs_array_create_int(c_int_int_dict_initial_bucket_size, c_int_int_dict_empty_param)
        if bucket < 0:
            _int_int_dict_last_operation_status = c_int_int_dict_resize_failed_error
            return c_int_int_dict_generic_error
        xs_array_set_int(bucket, 1, key)
        xs_array_set_int(bucket, 2, val)
        xs_array_set_int(bucket, 0, 2)
        xs_array_set_int(dct, hash, bucket)
        _int_int_dict_last_operation_status = c_int_int_dict_no_key_error
        return c_int_int_dict_generic_error
    bucket_size: int32 = xs_array_get_int(bucket, 0)
    j: int32 = int32(1)
    found: bool = False
    found_value: int32 = c_int_int_dict_generic_error
    while j <= bucket_size and not found:
        stored_key: int32 = xs_array_get_int(bucket, j)
        if stored_key == key:
            found_value = xs_array_get_int(bucket, j + 1)
            xs_array_set_int(bucket, j + 1, val)
            found = True
        j += 2
    if not found:
        bucket_capacity: int32 = xs_array_get_size(bucket)
        if (bucket_capacity - 1 - bucket_size) < 2:
            new_bucket_capacity: int32 = (bucket_capacity - 1) * 2 + 1
            if new_bucket_capacity > c_int_int_dict_max_capacity:
                _int_int_dict_last_operation_status = c_int_int_dict_max_capacity_error
                return c_int_int_dict_generic_error
            r: int32 = xs_array_resize_int(bucket, new_bucket_capacity)
            if r != 1:
                _int_int_dict_last_operation_status = c_int_int_dict_resize_failed_error
                return c_int_int_dict_generic_error
        xs_array_set_int(bucket, bucket_size + 1, key)
        xs_array_set_int(bucket, bucket_size + 2, val)
        xs_array_set_int(bucket, 0, bucket_size + 2)
        _int_int_dict_last_operation_status = c_int_int_dict_no_key_error
    else:
        _int_int_dict_last_operation_status = c_int_int_dict_success
    return found_value


def _xs_int_int_dict_move_to_temp_array(dct: int32 = int32(-1), total_size: int32 = int32(0),
                                        dict_capacity: int32 = int32(0)) -> int32:
    global _int_int_dict_temp_array
    temp_data_size: int32 = total_size * 2
    if _int_int_dict_temp_array < 0:
        _int_int_dict_temp_array = xs_array_create_int(temp_data_size, c_int_int_dict_empty_param)
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
    for i in i32range(1, dict_capacity):
        bucket: int32 = xs_array_get_int(dct, i)
        if bucket >= 0:
            bucket_size: int32 = xs_array_get_int(bucket, 0)
            for j in i32range(1, bucket_size + 1, 2):
                stored_key: int32 = xs_array_get_int(bucket, j)
                stored_val: int32 = xs_array_get_int(bucket, j + 1)
                xs_array_set_int(_int_int_dict_temp_array, t, stored_key)
                xs_array_set_int(_int_int_dict_temp_array, t + 1, stored_val)
                t += 2
            xs_array_set_int(bucket, 0, 0)
    return temp_data_size


def xs_int_int_dict_put(dct: int32 = int32(-1), key: int32 = int32(-1), val: int32 = int32(0)) -> int32:
    global _int_int_dict_temp_array, _int_int_dict_last_operation_status
    total_size: int32 = xs_array_get_int(dct, 0)
    dict_capacity: int32 = xs_array_get_size(dct)

    previous_value: int32 = _xs_int_int_dict_replace(dct, key, val, dict_capacity - 1)
    if _int_int_dict_last_operation_status == c_int_int_dict_no_key_error:
        total_size += 1
        xs_array_set_int(dct, 0, total_size)
    elif _int_int_dict_last_operation_status == c_int_int_dict_success:
        return previous_value
    else:
        return c_int_int_dict_generic_error

    load_factor: float = float(total_size) / (dict_capacity - 1)
    if load_factor > c_int_int_dict_max_load_factor:
        store_status: int32 = _int_int_dict_last_operation_status
        temp_data_size: int32 = _xs_int_int_dict_move_to_temp_array(dct, total_size, dict_capacity)
        if temp_data_size < 0:
            _int_int_dict_last_operation_status = temp_data_size
            return c_int_int_dict_generic_error
        new_dict_capacity: int32 = (dict_capacity - 1) * 2 + 1
        if new_dict_capacity > c_int_int_dict_max_capacity:
            _int_int_dict_last_operation_status = c_int_int_dict_resize_failed_error
            return c_int_int_dict_generic_error
        r: int32 = xs_array_resize_int(dct, new_dict_capacity)
        if r != 1:
            _int_int_dict_last_operation_status = c_int_int_dict_resize_failed_error
            return c_int_int_dict_generic_error
        for b in i32range(dict_capacity, new_dict_capacity):
            xs_array_set_int(dct, b, c_int_int_dict_empty_param)
        dict_capacity = new_dict_capacity
        for t in i32range(0, temp_data_size, 2):
            _xs_int_int_dict_replace(dct, xs_array_get_int(_int_int_dict_temp_array, t),
                                     xs_array_get_int(_int_int_dict_temp_array, t + 1), dict_capacity - 1)
            if _int_int_dict_last_operation_status < 0 and _int_int_dict_last_operation_status != c_int_int_dict_no_key_error:
                return c_int_int_dict_generic_error
        _int_int_dict_last_operation_status = store_status
    return c_int_int_dict_generic_error


def xs_int_int_dict(
        k1: int32 = c_int_int_dict_empty_param,
        v1: int32 = int32(0),
        k2: int32 = c_int_int_dict_empty_param,
        v2: int32 = int32(0),
        k3: int32 = c_int_int_dict_empty_param,
        v3: int32 = int32(0),
        k4: int32 = c_int_int_dict_empty_param,
        v4: int32 = int32(0),
        k5: int32 = c_int_int_dict_empty_param,
        v5: int32 = int32(0),
        k6: int32 = c_int_int_dict_empty_param,
        v6: int32 = int32(0),
) -> int32:
    dct: int32 = xs_int_int_dict_create()
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


def xs_int_int_dict_remove(dct: int32 = int32(-1), key: int32 = int32(-1)) -> int32:
    global _int_int_dict_last_operation_status, _int_int_dict_temp_array
    total_size: int32 = xs_array_get_int(dct, 0)
    dict_capacity: int32 = xs_array_get_size(dct)
    hash: int32 = _xs_int_int_dict_hash(key, dict_capacity - 1)
    bucket: int32 = xs_array_get_int(dct, hash)
    if bucket < 0:
        _int_int_dict_last_operation_status = c_int_int_dict_no_key_error
        return c_int_int_dict_generic_error
    found: bool = False
    found_value: int32 = c_int_int_dict_generic_error
    bucket_size: int32 = xs_array_get_int(bucket, 0)
    for j in i32range(1, bucket_size + 1, 2):
        stored_key: int32 = xs_array_get_int(bucket, j)
        if found:
            xs_array_set_int(bucket, j - 2, stored_key)
            xs_array_set_int(bucket, j - 1, xs_array_get_int(bucket, j + 1))
        elif stored_key == key:
            found = True
            found_value = xs_array_get_int(bucket, j + 1)
            xs_array_set_int(bucket, 0, bucket_size - 2)
            xs_array_set_int(dct, 0, total_size - 1)
    bucket_capacity: int32 = xs_array_get_size(bucket)
    if found:
        size_threshold: int32 = (bucket_capacity - 1) // 2
        if size_threshold >= (bucket_size - 2) and bucket_capacity > c_int_int_dict_min_bucket_size:
            r: int32 = xs_array_resize_int(bucket, size_threshold + 1)
            if r != 0:
                _int_int_dict_last_operation_status = c_int_int_dict_resize_failed_error
                return c_int_int_dict_generic_error
        _int_int_dict_last_operation_status = c_int_int_dict_success
    else:
        _int_int_dict_last_operation_status = c_int_int_dict_no_key_error
    return found_value


def xs_int_int_dict_get(dct: int32 = int32(-1), key: int32 = int32(-1), dft: int32 = int32(-1)) -> int32:
    global _int_int_dict_last_operation_status
    dict_capacity: int32 = xs_array_get_size(dct)
    hash: int32 = _xs_int_int_dict_hash(key, dict_capacity - 1)
    bucket: int32 = xs_array_get_int(dct, hash)
    if bucket < 0:
        _int_int_dict_last_operation_status = c_int_int_dict_no_key_error
        return dft
    bucket_size: int32 = xs_array_get_int(bucket, 0)
    for j in i32range(1, bucket_size + 1, 2):
        stored_key: int32 = xs_array_get_int(bucket, j)
        if key == stored_key:
            _int_int_dict_last_operation_status = c_int_int_dict_success
            return xs_array_get_int(bucket, j + 1)
    _int_int_dict_last_operation_status = c_int_int_dict_no_key_error
    return dft


def xs_int_int_dict_contains(dct: int32 = int32(-1), key: int32 = int32(-1)) -> bool:
    dict_capacity: int32 = xs_array_get_size(dct)
    hash: int32 = _xs_int_int_dict_hash(key, dict_capacity - 1)
    bucket: int32 = xs_array_get_int(dct, hash)
    if bucket < 0:
        return False
    bucket_size: int32 = xs_array_get_int(bucket, 0)
    for j in i32range(1, bucket_size + 1, 2):
        stored_key: int32 = xs_array_get_int(bucket, j)
        if key == stored_key:
            return True
    return False


def xs_int_int_dict_size(dct: int32 = int32(-1)) -> int32:
    return xs_array_get_int(dct, 0)


def xs_int_int_dict_clear(dct: int32 = int32(-1)) -> int32:
    dict_capacity: int32 = xs_array_get_size(dct)
    for i in i32range(1, dict_capacity):
        bucket: int32 = xs_array_get_int(dct, i)
        if bucket >= 0:
            xs_array_set_int(bucket, 0, 0)
            bucket_capacity: int32 = xs_array_get_size(bucket)
            if bucket_capacity > c_int_int_dict_min_bucket_size:
                r1: int32 = xs_array_resize_int(bucket, c_int_int_dict_min_bucket_size)
                if r1 != 1:
                    return c_int_int_dict_generic_error
    xs_array_set_int(dct, 0, 0)
    if dict_capacity > c_int_int_dict_initial_num_of_buckets:
        r2: int32 = xs_array_resize_int(dct, c_int_int_dict_initial_num_of_buckets)
        if r2 != 1:
            return c_int_int_dict_generic_error
    return c_int_int_dict_success


def xs_int_int_dict_copy(dct: int32 = int32(-1)) -> int32:
    dict_capacity: int32 = xs_array_get_size(dct)
    new_dct: int32 = xs_array_create_int(dict_capacity, c_int_int_dict_empty_param)
    if new_dct < 0:
        return c_int_int_dict_resize_failed_error
    for i in i32range(1, dict_capacity):
        bucket: int32 = xs_array_get_int(dct, i)
        if bucket >= 0:
            bucket_capacity: int32 = xs_array_get_size(bucket)
            bucket_size: int32 = xs_array_get_int(bucket, 0)
            new_bucket: int32 = xs_array_create_int(bucket_capacity, c_int_int_dict_empty_param)
            if new_bucket < 0:
                return c_int_int_dict_resize_failed_error
            for j in i32range(bucket_size + 1):
                xs_array_set_int(new_bucket, j, xs_array_get_int(bucket, j))
            xs_array_set_int(new_dct, i, new_bucket)
    xs_array_set_int(new_dct, 0, xs_array_get_int(dct, 0))
    return new_dct


def xs_int_int_dct_iterator_start() -> None:
    global _int_int_dict_iterator_curr_idx, _int_int_dict_iterator_prev_key
    _int_int_dict_iterator_prev_idx = int32(0)
    _int_int_dict_iterator_prev_key = int32(-1)


def xs_int_int_dct_iterator_has_next(dct: int32 = int32(-1)) -> bool:
    global _int_int_dict_iterator_curr_idx
    total_size: int32 = xs_array_get_int(dct, 0)
    return _int_int_dict_iterator_prev_idx < total_size


def _xs_int_int_dct_iterator_next(dct: int32 = int32(-1), return_key: bool = True) -> int32:
    global _int_int_dict_iterator_prev_idx, _int_int_dict_iterator_prev_key, _int_int_dict_last_operation_status
    b: int32 = int32(-1)
    bucket: int32 = int32(-1)
    bucket_size: int32 = int32(-1)
    idx: int32 = int32(1)
    dict_capacity: int32 = xs_array_get_size(dct)
    found: bool = False
    stored_key: int32 = int32(-1)
    if _int_int_dict_iterator_prev_idx == 0:
        i: int32 = int32(1)
        while i < dict_capacity and not found:
            bucket = xs_array_get_int(dct, i)
            bucket_size = xs_array_get_int(bucket, 0)
            if bucket >= 0 and bucket_size > 0:
                found = True
                b = i
            i += 1
    else:
        hash: int32 = _xs_int_int_dict_hash(_int_int_dict_iterator_prev_key, dict_capacity - 1)
        bucket = xs_array_get_int(dct, hash)
        bucket_size = xs_array_get_int(bucket, 0)
        j: int32 = int32(1)
        while j <= bucket_size and not found:
            stored_key = xs_array_get_int(bucket, j)
            if _int_int_dict_iterator_prev_key == stored_key:
                idx = j + 2
                b = hash
                found = True
            j += 2
    if not found:
        _int_int_dict_iterator_prev_idx = c_int_int_dict_max_capacity
        _int_int_dict_last_operation_status = c_int_int_dict_generic_error
        return c_int_int_dict_generic_error
    for k in i32range(b, dict_capacity):
        if found:
            found = False
        else:
            bucket = xs_array_get_int(dct, k)
            bucket_size = xs_array_get_int(bucket, 0)
        if bucket >= 0:
            for l in i32range(idx, bucket_size, 2):
                stored_key = xs_array_get_int(bucket, l)
                _int_int_dict_last_operation_status = c_int_int_dict_success
                _int_int_dict_iterator_prev_idx += 1
                _int_int_dict_iterator_prev_key = stored_key
                if return_key:
                    return stored_key
                else:
                    return xs_array_get_int(bucket, l + 1)
        idx = 1
    _int_int_dict_iterator_prev_idx = c_int_int_dict_max_capacity
    _int_int_dict_last_operation_status = c_int_int_dict_generic_error
    return c_int_int_dict_generic_error


def xs_int_int_dct_iterator_next_key(dct: int32 = int32(-1)) -> int32:
    return _xs_int_int_dct_iterator_next(dct, True)


def xs_int_int_dct_iterator_next_value(dct: int32 = int32(-1)) -> int32:
    return _xs_int_int_dct_iterator_next(dct, False)


def xs_int_int_dict_to_string(dct: int32 = int32(-1)) -> str:
    dict_size: int32 = xs_array_get_size(dct)
    s: str = "{"
    first: bool = True
    for i in i32range(1, dict_size):
        bucket: int32 = xs_array_get_int(dct, i)
        if bucket >= 0:
            bucket_size: int32 = xs_array_get_int(bucket, 0)
            for j in i32range(1, bucket_size + 1, 2):
                key: int32 = xs_array_get_int(bucket, j)
                val: int32 = xs_array_get_int(bucket, j + 1)
                if first:
                    first = False
                else:
                    s += ", "
                s += f"{key}: {val}"
    s += "}"
    return s


def xs_int_int_dict_last_error() -> int32:
    return _int_int_dict_last_operation_status


def xs_int_int_dict_update(source: int32 = int32(-1), dct: int32 = int32(-1)) -> int32:
    global _int_int_dict_last_operation_status
    xs_int_int_dct_iterator_start()
    while xs_int_int_dct_iterator_has_next(dct):
        key: int32 = xs_int_int_dct_iterator_next_key(dct)
        err: int32 = xs_int_int_dict_last_error()
        if err != 0:
            return err
        val: int32 = xs_int_int_dict_get(dct, key)
        err = xs_int_int_dict_last_error()
        if err != 0:
            return err
        xs_int_int_dict_put(source, key, val)
        err = xs_int_int_dict_last_error()
        if err != 0 and err != c_int_int_dict_no_key_error:
            return err
        _int_int_dict_last_operation_status = c_int_int_dict_success
    return c_int_int_dict_success


def test() -> None:
    pass


def int_int_dict(include_test: bool) -> tuple[str, str]:
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
        xs_int_int_dict_put,
        xs_int_int_dict_create,
        xs_int_int_dict,
        xs_int_int_dict_get,
        xs_int_int_dict_remove,
        xs_int_int_dict_contains,
        xs_int_int_dict_size,
        xs_int_int_dict_clear,
        xs_int_int_dict_copy,
        xs_int_int_dct_iterator_start,
        xs_int_int_dct_iterator_has_next,
        _xs_int_int_dct_iterator_next,
        xs_int_int_dct_iterator_next_key,
        xs_int_int_dct_iterator_next_value,
        xs_int_int_dict_to_string,
        xs_int_int_dict_last_error,
        xs_int_int_dict_update,
        indent=True,
    )
    if include_test:
        xs += constants_xs + PythonToXsConverter.to_xs_script(
            test,
            indent=True,
        )
    print(xs)
    return (xs, "intIntDict")


if __name__ == "__main__":
    int_int_dict(True)

// Converts an array to pointers of pointers

#pragma once

#include "utils.h"

// Add pointers to T

template <typename T, typename T0, class ... Ts>
class add_pointers : public add_pointers<T*, Ts...>{
};

template <typename T, typename T0>
class add_pointers<T, T0>{
public:
    typedef T* type;
};

// Computes pointers size

template<typename T>
size_t _pointers_size(T l0) {
  return 1;
}

template<typename T, class ... Ts>
size_t _pointers_size(T l0, Ts ... ls) {
  return (l0+1)*_pointers_size(ls...);
}

template<typename T, class ... Ts>
size_t pointers_size(T l0, Ts ... ls) {
  return l0*_pointers_size(ls...);
}

// Fills in the pointers of pointers

template<typename T,  class Tn>
void fill_in(T* arr, T** buf, size_t vol, size_t skip, size_t coord, Tn lm1, Tn ln) {
  for(Tn i=0; i<lm1; i++) {
    buf[i] = arr + (coord*lm1 + i)*ln;
  }
}


template<typename T, class T0, class T1, class ... Ts>
void fill_in(T* arr, typename add_pointers<T**,Ts...>::type buf, size_t vol, size_t skip, size_t coord, T0 l0, T1 l1, Ts ... shape) {
  typedef typename add_pointers<T*,Ts...>::type next_T;
  vol*=l0;
  skip+=vol;
  for(T0 i=0; i<l0; i++) {
    buf[i] = (next_T) (buf+skip+(coord*l0+i)*l1);
    fill_in(arr, buf[i], vol, skip, coord*l0+i, l1, shape...);
  }
}

template<typename T, class T0>
auto to_pointers(T* arr, T0 l0) {
  return arr;
}

template<typename T, class ... Ts>
auto to_pointers(T* arr, Ts ... shape) {
  auto buffer = static_cast<typename add_pointers<T, Ts...>::type>(std::malloc(pointers_size(shape...)*sizeof(void*)));
  fill_in(arr, buffer, 1, 0, 0, shape...);
  return make_shared(buffer);
}

template<typename T, typename T0>
auto _flatten(std::vector<T> &vec, T* arr, T0 l0) {
  for(T0 i=0; i<l0; i++) {
    vec.push_back(arr[i]);
  }
  return vec;
}

template<typename T, typename T0, class ... Ts>
auto _flatten(std::vector<T> &vec, typename add_pointers<T*, Ts...>::type arr, T0 l0, Ts ... ls) {
  for(T0 i=0; i<l0; i++) {
    _flatten(vec, arr[i], ls...);
  }
  return vec;
}

template<typename T, class ... Ts>
auto flatten(T arr, Ts ... shape) {
  typedef typename remove_all_pointers<T>::type base_T;
  std::vector<base_T> v;
  v.reserve(product(shape...));
  return _flatten(v, get_pointer(arr), shape ...);
}

// A set of useful functions that are included by lyncs_cppyy
// and made available at Python level

#pragma once

// Turns a class pointer to shared_ptr
template<typename T>
std::shared_ptr<T> make_shared(T* ptr) {
  return std::shared_ptr<T>(ptr);
}

// Product of values
template<typename T>
auto product(T l0) {
  return l0;
}

template<typename T, class ... Ts>
auto product(T l0, Ts ... ls) {
  return l0*product(ls...);
}

// Removes all pointers from a type
template <typename T> class remove_all_pointers{
public:
    typedef T type;
};

template <typename T> class remove_all_pointers<T*>{
public:
    typedef typename remove_all_pointers<T>::type type;
};

template <typename T> class remove_all_pointers<std::shared_ptr<T>>{
public:
    typedef typename remove_all_pointers<T>::type type;
};

template <typename T> class remove_all_pointers<std::unique_ptr<T>>{
public:
    typedef typename remove_all_pointers<T>::type type;
};

// Get pointer
template<typename T>
auto get_pointer(T* ptr) {
  return ptr;
}

template<typename T>
auto get_pointer(std::shared_ptr<T> ptr) {
  return ptr.get();
}

template<typename T>
auto get_pointer(std::unique_ptr<T> ptr) {
  return ptr.get();
}

// Typename
template <typename T>
auto type_name(T var) {
  return typeid(var).name();
}


// Lookup method for type conversion
template <typename T>
struct CppType {
  virtual ~CppType(){}
  virtual T __cppyy__();
  operator T() {return __cppyy__();}
};

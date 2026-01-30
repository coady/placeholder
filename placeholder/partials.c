#include "Python.h"

static PyObject *
rpartial_call(PyObject *self, PyObject *left)
{
    PyObject *func = PyTuple_GetItem(self, 0);
    PyObject *right = PyTuple_GetItem(self, 1);
    if (!func || !right)
        return NULL;
    return PyObject_CallFunctionObjArgs(func, left, right, NULL);
}

static PyMethodDef rpartial_call_def = {
    .ml_name = "rpartial",
    .ml_meth = (PyCFunction)rpartial_call,
    .ml_flags = METH_O,
    .ml_doc = "Binary function with bound right argument.",
};

static PyObject *
rpartial(PyObject *module, PyObject *args)
{
    PyObject *func, *right;
    if (!PyArg_UnpackTuple(args, "rpartial", 2, 2, &func, &right))
        return NULL;
    return PyCFunction_NewEx(&rpartial_call_def, args, module);
}

static PyMethodDef partials_methods[] = {
    {"rpartial", (PyCFunction)rpartial, METH_VARARGS, "Return lambda left: func(left, right)."},
    {NULL}
};

static PyModuleDef partials_module = {
    PyModuleDef_HEAD_INIT,
    .m_name = "partials",
    .m_doc = PyDoc_STR("Partially bound binary functions."),
    .m_methods = partials_methods,
};

PyMODINIT_FUNC PyInit_partials(void)
{
    return PyModuleDef_Init(&partials_module);
}

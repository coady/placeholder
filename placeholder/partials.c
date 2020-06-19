#include "Python.h"

typedef struct {
    PyObject_HEAD
    PyObject *func;
    PyObject *arg;
} partial;

static void
partial_dealloc(partial *self)
{
    Py_XDECREF(self->func);
    Py_XDECREF(self->arg);
    Py_TYPE(self)->tp_free(self);
}

static int
partial_init(partial *self, PyObject *args, PyObject *kwargs)
{
    static char *kwlist[] = {"func", "arg", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "OO:partial", kwlist, &self->func, &self->arg))
        return -1;
    Py_XINCREF(self->func);
    Py_XINCREF(self->arg);
    return 0;
}

static PyObject *
partial_str(partial *self)
{
    return PyUnicode_FromFormat("placeholder.partial(%S, %S)", self->func, self->arg);
}

static PyObject *
partial_left(partial *self, PyObject *arg)
{
    PyObject *const args[2] = {arg, self->arg};
    return _PyObject_FastCall(self->func, (PyObject *const *) &args, 2);
}

static PyObject *
partial_right(partial *self, PyObject *arg)
{
    PyObject *const args[2] = {self->arg, arg};
    return _PyObject_FastCall(self->func, (PyObject *const *) &args, 2);
}

static PyMethodDef partial_methods[] = {
    {"left", (PyCFunction)partial_left, METH_O, "Call binary function with left arg."},
    {"right", (PyCFunction)partial_right, METH_O, "Call binary function with right arg."},
    {NULL}  /* Sentinel */
};

static PyTypeObject PartialType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "placeholder.partial",
    .tp_doc = "Partially bound binary function.",
    .tp_basicsize = sizeof(partial),
    .tp_itemsize = 0,
    .tp_flags = Py_TPFLAGS_DEFAULT,
    .tp_new = PyType_GenericNew,
    .tp_dealloc = (destructor)partial_dealloc,
    .tp_init = (initproc)partial_init,
    .tp_str = (reprfunc)partial_str,
    .tp_methods = partial_methods,
};

static PyModuleDef partialsmodule = {
    PyModuleDef_HEAD_INIT,
    .m_name = "partials",
    .m_doc = "Partially bound binary functions.",
    .m_size = -1,
};

PyMODINIT_FUNC PyInit_partials(void)
{
    if (PyType_Ready(&PartialType))
        return NULL;
    PyObject *m = PyModule_Create(&partialsmodule);
    if (!m)
        return NULL;
    Py_INCREF(&PartialType);
    if (!PyModule_AddObject(m, "partial", (PyObject *) &PartialType))
        return m;
    Py_DECREF(&PartialType);
    Py_DECREF(m);
    return NULL;
}

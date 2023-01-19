#define Py_LIMITED_API 0x03080000
#include "Python.h"

typedef struct {
    PyObject_HEAD
    PyObject *func;
    PyObject *arg;
} partial;

static void
partial_dealloc(partial *self)
{
    Py_DecRef(self->func);
    Py_DecRef(self->arg);
    PyObject_Free(self);
}

static int
partial_init(partial *self, PyObject *args, PyObject *kwargs)
{
    static char *kwlist[] = {"func", "arg", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "OO:partial", kwlist, &self->func, &self->arg))
        return -1;
    Py_IncRef(self->func);
    Py_IncRef(self->arg);
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
    return PyObject_CallFunctionObjArgs(self->func, arg, self->arg, NULL);
}

static PyObject *
partial_right(partial *self, PyObject *arg)
{
    return PyObject_CallFunctionObjArgs(self->func, self->arg, arg, NULL);
}

static PyMethodDef partial_methods[] = {
    {"left", (PyCFunction)partial_left, METH_O, "Call binary function with left arg."},
    {"right", (PyCFunction)partial_right, METH_O, "Call binary function with right arg."},
    {NULL}  /* Sentinel */
};

static PyType_Slot partial_slots[] = {
    {Py_tp_doc, PyDoc_STR("Partially bound binary function.")},
    {Py_tp_dealloc, partial_dealloc},
    {Py_tp_init, partial_init},
    {Py_tp_str, partial_str},
    {Py_tp_methods, partial_methods},
    {0, NULL}
};

static PyType_Spec partial_spec = {
    "placeholder.partial",
    sizeof(partial),
    0,
    Py_TPFLAGS_DEFAULT,
    partial_slots,
};

static int
partials_mod_exec(PyObject *module)
{
    PyObject *PartialType = PyType_FromSpec(&partial_spec);
    if (!PartialType)
        return -1;
    if (!PyModule_AddObject(module, "partial", PartialType))
        return 0;
    Py_DecRef(PartialType);
    return -1;
}

static PyModuleDef_Slot partials_slots[] = {
    {Py_mod_exec, partials_mod_exec},
    {0, NULL}
};

static PyModuleDef partialsmodule = {
    PyModuleDef_HEAD_INIT,
    .m_name = "partials",
    .m_doc = PyDoc_STR("Partially bound binary functions."),
    .m_slots = partials_slots,
};

PyMODINIT_FUNC PyInit_partials(void)
{
    return PyModuleDef_Init(&partialsmodule);
}

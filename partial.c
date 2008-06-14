/* Partial objects */
#include "Python.h"
#include "structmember.h"

typedef struct {
    PyObject_HEAD
    PyCFunction func;
    PyObject* name;
    PyObject* left;
    PyObject* right;
} partial;

static void partial_dealloc(partial* self)
{
    Py_XDECREF(self->name);
    Py_XDECREF(self->left);
    Py_XDECREF(self->right);
    self->ob_type->tp_free(self);
}

static int partial_init(partial* self, PyObject* args, PyObject* kwargs)
{
    long func = 0;
    static char* kwlist[] = {"name", "func", "left", "right", NULL};
    self->name = self->left = self->right = NULL;
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "Sl|OO:partial", kwlist, &self->name, &func, &self->left, &self->right))
        return -1;
    if (!self->left == !self->right) {
        PyErr_Format(PyExc_TypeError, "exactly one partial argument must be bound.");
        return -1;
    }
    self->func = (void*)func;
    Py_XINCREF(self->name);
    Py_XINCREF(self->left);
    Py_XINCREF(self->right);
    return 0;
}

static PyObject* partial_str(partial* self)
{
    PyObject* result = NULL;
    const char* format = self->left ? "%s(%s, )" : "%s(, %s)";
    PyObject* arg = PyObject_Str(self->left ? self->left : self->right);
    if (arg)
        result = PyString_FromFormat(format, PyString_AsString(self->name), PyString_AsString(arg));
    Py_XDECREF(arg);
    return result;
}

static PyObject* partial_call(partial* self, PyObject* args, PyObject* kwargs)
{
    PyObject* arg = NULL;
    if (!PyArg_UnpackTuple(args, "partial", 1, 1, &arg))
        return NULL;
    if (kwargs && PyDict_Size(kwargs))
        return PyErr_Format(PyExc_TypeError, "partial accepts no keyword arguments.");
    if (self->left)
        return self->func(self->left, arg);
    return self->func(arg, self->right);
}

static PyMemberDef partial_members[] = {
    {"name", T_OBJECT_EX, offsetof(partial, name), READONLY, "function name"},
    {"left", T_OBJECT_EX, offsetof(partial, left), READONLY, "left argument"},
    {"right", T_OBJECT_EX, offsetof(partial, right), READONLY, "right argument"},
    {NULL}  /* Sentinel */
};

static PyTypeObject PartialType = {
    PyObject_HEAD_INIT(NULL)
    0,                      /* ob_size */
    "partial",              /* tp_name */
    sizeof(partial),        /* tp_basicsize */
    0,                      /* tp_itemsize */
    (destructor)partial_dealloc,    /* tp_dealloc */
    0,                      /* tp_print */
    0,                      /* tp_getattr */
    0,                      /* tp_setattr */
    0,                      /* tp_compare */
    0,                      /* tp_repr */
    0,                      /* tp_as_number */
    0,                      /* tp_as_sequence */
    0,                      /* tp_as_mapping */
    0,                      /* tp_hash */
    (ternaryfunc)partial_call,  /* tp_call */
    (reprfunc)partial_str,  /* tp_str */
    0,                      /* tp_getattro */
    0,                      /* tp_setattro */
    0,                      /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT,     /* tp_flags */
    0,                      /* tp_doc */
    0,                      /* tp_traverse */
    0,                      /* tp_clear */
    0,                      /* tp_richcompare */
    0,                      /* tp_weaklistoffset */
    0,                      /* tp_iter */
    0,                      /* tp_iternext */
    0,                      /* tp_methods */
    partial_members,        /* tp_members */
    0,                      /* tp_getset */
    0,                      /* tp_base */
    0,                      /* tp_dict */
    0,                      /* tp_descr_get */
    0,                      /* tp_descr_set */
    0,                      /* tp_dictoffset */
    (initproc)partial_init, /* tp_init */
};

/* support for binary operators with a slightly different API signature */
PyObject* Number_Power(PyObject* left, PyObject* right) { return PyNumber_Power(left, right, Py_None); }

PyObject* Object_LT(PyObject* left, PyObject* right) { return PyObject_RichCompare(left, right, Py_LT); }
PyObject* Object_LE(PyObject* left, PyObject* right) { return PyObject_RichCompare(left, right, Py_LE); }
PyObject* Object_EQ(PyObject* left, PyObject* right) { return PyObject_RichCompare(left, right, Py_EQ); }
PyObject* Object_NE(PyObject* left, PyObject* right) { return PyObject_RichCompare(left, right, Py_NE); }
PyObject* Object_GT(PyObject* left, PyObject* right) { return PyObject_RichCompare(left, right, Py_GT); }
PyObject* Object_GE(PyObject* left, PyObject* right) { return PyObject_RichCompare(left, right, Py_GE); }

PyMODINIT_FUNC initpartial(void)
{
    PartialType.tp_new = PyType_GenericNew;
    if (PyType_Ready(&PartialType))
        return;
    PyObject* mod = Py_InitModule("partial", NULL);
    if (mod)
        PyModule_AddObject(mod, "partial", (PyObject*)&PartialType);
}

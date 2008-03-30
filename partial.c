/* Partial objects */
#include "Python.h"

typedef struct {
    PyObject_HEAD
    PyCFunction func;
    PyObject *left, *right;
} partial;

static void partial_dealloc(partial* self)
{
    Py_XDECREF(self->left);
    Py_XDECREF(self->right);
    self->ob_type->tp_free(self);
}

static int partial_init(partial* self, PyObject* args, PyObject* kwargs)
{
    long func = 0;
    static char* kwlist[] = {"func", "left", "right", NULL};
    self->left = self->right = NULL;
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "l|OO:partial", kwlist, &func, &self->left, &self->right))
        return -1;
    if (!self->left == !self->right) {
        PyErr_Format(PyExc_TypeError, "exactly one partial argument must be bound.");
        return -1;
    }
    self->func = (void*)func;
    Py_XINCREF(self->left);
    Py_XINCREF(self->right);
    return 0;
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

static PyTypeObject PartialType = {
    PyObject_HEAD_INIT(NULL)
    0,                      /*ob_size */
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
    0,                      /* tp_str */
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
    0,                      /* tp_members */
    0,                      /* tp_getset */
    0,                      /* tp_base */
    0,                      /* tp_dict */
    0,                      /* tp_descr_get */
    0,                      /* tp_descr_set */
    0,                      /* tp_dictoffset */
    (initproc)partial_init, /* tp_init */
    0,                      /* tp_alloc */
    PyType_GenericNew,      /* tp_new */
    0,                      /* tp_free */
    0,                      /* tp_is_gc */
};

PyMODINIT_FUNC initpartial(void)
{
    if (PyType_Ready(&PartialType))
        return;
    PyObject* mod = Py_InitModule("partial", NULL);
    if (mod)
        PyModule_AddObject(mod, "partial", (PyObject*)&PartialType);
}

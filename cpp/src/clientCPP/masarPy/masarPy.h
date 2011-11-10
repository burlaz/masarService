/* masarPy.h */
/*
 * Copyright - See the COPYRIGHT that is included with this distribution.
 * This code is distributed subject to a Software License Agreement found
 * in file LICENSE that is included with this distribution.
 */
/* Author Marty Kraimer 2011.11 */

#ifndef MASERPY_H
#define MASERPY_H
#include "requesterPy.h"


namespace epics { namespace masarService { 

class MasarPy {
public:
    MasarPy();
    ~MasarPy();
protected:
};

extern PyObject *createMasarPy(
    Masar::shared_pointer masar);

}}
#endif  /* MASERPY_H */

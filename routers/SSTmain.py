import logging
from fastapi import APIRouter

from lib.SST_list import sst_list

router=APIRouter()


@router.post('/create')
def sst_create():
    sstlist =sst_list()
    logging.debug(f'created the SST with all the required parameters')
    return 'Success'

@router.post('/update')
def sst_update():
    sstlist =sst_list()
    logging.debug(f'Updated the SST with all the required parameters')
    return 'Success'

@router.delete('/delete')
def sst_delete():
    sstlist=sst_list()
    logging.debug(f'deleted the SST')
    return 'Success'

@router.monitor('/monitor')
def sst_monitor():
    logging.debug(f'successful fetch')
    return 'Success'
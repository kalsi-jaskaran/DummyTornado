#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-

from enum import Enum

from server.webservice.exceptions.Exceptions import InvalidPoolException


class PoolType(Enum):
    """ Enum For Process Pools """
    DUT = 'dut'
    OUT_OF_ORDER = 'ooo'
    MANAGEMENT_POOL = 'management_pool'
    HEALTH_CHECK_POOL = 'health_check_pool'

    _DUT1_POOL = 'DUT1_POOL'
    _DUT2_POOL = 'DUT2_POOL'
    _DUT3_POOL = 'DUT3_POOL'
    _DUT4_POOL = 'DUT4_POOL'

    @staticmethod
    def get_pool(dut_id):
        if int(dut_id) == 1:
            return PoolType._DUT1_POOL
        elif int(dut_id) == 2:
            return PoolType._DUT2_POOL
        elif int(dut_id) == 3:
            return PoolType._DUT3_POOL
        elif int(dut_id) == 4:
            return PoolType._DUT4_POOL
        else:
            raise InvalidPoolException("DUT: {} Invalid DUT id from Database.".format(dut_id))
